from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import networkx as nx
import sys
import os

# Ensure the harness module can be imported from the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from harness.mermaid_compiler import compile_mermaid_to_dag

app = FastAPI(
    title="Sweetbrier Node API",
    description="Deterministic topological circuit breaker and causal pre-filter for LLMs.",
    version="1.0.0"
)

class MermaidRequest(BaseModel):
    text: str

class ValidationResponse(BaseModel):
    valid: bool
    is_dag: bool
    nodes: list[str]
    edges: list[list[str]]
    error: str | None = None
    cycles: list[list[str]] | None = None

@app.post("/validate", response_model=ValidationResponse)
def validate_topology(request: MermaidRequest):
    try:
        # Compile text to graph
        G = compile_mermaid_to_dag(request.text)
        nodes = list(G.nodes)
        edges = [list(edge) for edge in G.edges]
        
        # Check causal topology (DAG)
        if nx.is_directed_acyclic_graph(G):
            return ValidationResponse(
                valid=True,
                is_dag=True,
                nodes=nodes,
                edges=edges,
                error=None,
                cycles=None
            )
        else:
            # Extract the exact cyclic hallucination
            try:
                cycles = list(nx.find_cycle(G, orientation="original"))
                cycle_edges = [[u, v] for u, v, _ in cycles]
                error_msg = "Topological Violation: Cyclic causality detected."
            except nx.NetworkXNoCycle:
                cycle_edges = []
                error_msg = "Topological Violation: Invalid structure."

            return ValidationResponse(
                valid=False,
                is_dag=False,
                nodes=nodes,
                edges=edges,
                error=error_msg,
                cycles=cycle_edges
            )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Compilation error: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "Sweetbrier Middleware is online."}
