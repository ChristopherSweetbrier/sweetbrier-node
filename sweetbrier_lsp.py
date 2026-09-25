import sys
import re
from pygls.server import LanguageServer
from lsprotocol.types import (
    TEXT_DOCUMENT_DID_CHANGE,
    TEXT_DOCUMENT_DID_SAVE,
    TEXT_DOCUMENT_DID_OPEN,
    Diagnostic,
    DiagnosticSeverity,
    Position,
    Range,
    DidChangeTextDocumentParams,
    DidSaveTextDocumentParams,
    DidOpenTextDocumentParams
)
import networkx as nx

# We will import the compiler we wrote yesterday
from harness.mermaid_compiler import compile_mermaid_to_dag

server = LanguageServer("sweetbrier-lsp", "v1.0")

def validate_mermaid(ls: LanguageServer, uri: str, text: str):
    """
    Parses the mermaid text. If it violates the Sweetbrier structural laws 
    (e.g., contains a cycle), it sends a diagnostic error (red squiggle) to VS Code.
    """
    diagnostics = []
    
    # Only process if it actually contains a mermaid graph
    if "graph TD" not in text and "graph LR" not in text:
        ls.text_document_publish_diagnostics(uri, [])
        return

    try:
        # Compile it using your Sweetbrier engine
        G = compile_mermaid_to_dag(text)
        
        # Check Rule 1: Must be a strict Directed Acyclic Graph (No infinite loops)
        if not nx.is_directed_acyclic_graph(G):
            # Find cycles to highlight
            try:
                cycles = list(nx.find_cycle(G, orientation="original"))
                cycle_nodes = [edge[0] for edge in cycles]
                error_msg = f"Sweetbrier Epistemic Firewall Violation: Cyclic hallucination risk detected in nodes: {cycle_nodes}."
            except nx.NetworkXNoCycle:
                error_msg = "Sweetbrier Violation: Graph is not a valid DAG."

            # For now, we highlight the first line of the graph definition
            # In a production LSP, we would regex map the exact line of the offending node
            for line_num, line in enumerate(text.split('\n')):
                if "graph TD" in line or "graph LR" in line:
                    d = Diagnostic(
                        range=Range(
                            start=Position(line=line_num, character=0),
                            end=Position(line=line_num, character=len(line))
                        ),
                        message=error_msg,
                        severity=DiagnosticSeverity.Error,
                        source="Sweetbrier-Node"
                    )
                    diagnostics.append(d)
                    break
                    
    except Exception as e:
        # If the compiler crashes (bad syntax), we can also catch that
        pass

    # Send the red squiggles to VS Code
    ls.text_document_publish_diagnostics(uri, diagnostics)

@server.feature(TEXT_DOCUMENT_DID_OPEN)
def did_open(ls: LanguageServer, params: DidOpenTextDocumentParams):
    validate_mermaid(ls, params.text_document.uri, params.text_document.text)

@server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls: LanguageServer, params: DidChangeTextDocumentParams):
    text_doc = ls.workspace.get_text_document(params.text_document.uri)
    validate_mermaid(ls, params.text_document.uri, text_doc.source)

@server.feature(TEXT_DOCUMENT_DID_SAVE)
def did_save(ls: LanguageServer, params: DidSaveTextDocumentParams):
    text_doc = ls.workspace.get_text_document(params.text_document.uri)
    validate_mermaid(ls, params.text_document.uri, text_doc.source)

if __name__ == '__main__':
    print("Starting Sweetbrier Language Server on stdio...")
    server.start_io()
