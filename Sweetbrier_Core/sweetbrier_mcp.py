from mcp.server.fastmcp import FastMCP
import json
from mermaid_compiler import MermaidCompiler
from sweetbrier_engine import StatelessSweetbrierEngine

# Initialize the FastMCP Server
mcp = FastMCP("Sweetbrier Validator")

# Hardcode the Enterprise Rules (Normally loaded from DB)
MASTER_STATE = {
    "nodes": ["Protect Truth", "Trading Allowed", "Risk Managed", "Deceive User"],
    "edges": [["Trading Allowed", "Risk Managed"]],
    "mutually_exclusive": [
        frozenset(["Protect Truth", "Deceive User"])
    ],
    "higher_order_principles": {}
}

@mcp.tool()
def validate_action(proposed_mermaid_flowchart: str) -> str:
    """
    REQUIRED BEFORE ACTION: Validates any proposed action through the Sweetbrier engine.
    Submit your intent as a Mermaid.js flowchart string.
    Returns the Engine's verdict (e.g., APPROVED or REJECTED).
    If REJECTED, you must halt execution and notify the user.
    """
    try:
        compiler = MermaidCompiler()
        proposed_dag = compiler.parse(proposed_mermaid_flowchart)
        
        engine = StatelessSweetbrierEngine(MASTER_STATE)
        
        payload = json.dumps({
            "agent_id": "Antigravity_Agent",
            "kinship_score": 10.0,
            "proposed_dag": proposed_dag
        })
        
        result_json = engine.evaluate(payload)
        return result_json
        
    except Exception as e:
        return json.dumps({"status": "ERROR", "message": str(e)})

if __name__ == "__main__":
    # Start the standard input/output bridge for the MCP protocol
    mcp.run()
