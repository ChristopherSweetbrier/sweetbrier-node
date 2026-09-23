import json
import uuid
from mermaid_compiler import MermaidCompiler
from sweetbrier_engine import StatelessSweetbrierEngine

def print_header(title):
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def main():
    compiler = MermaidCompiler()

    print_header("1. COMPILING MASTER LAW (ENTERPRISE BOUNDARIES)")
    
    # 1. The Enterprise risk manager draws the acceptable bounds of the AI
    master_mermaid = """
    graph TD;
        A[Protect Truth] --> B[Dignity of the Human Person];
        C[Trading Allowed] --> D[Risk Managed];
    """
    
    print("Parsing Enterprise Mermaid Flowchart...")
    print(master_mermaid)
    
    master_dag = compiler.parse(master_mermaid)
    
    # Add our mutually exclusive constraints (the "cliffs")
    master_state = {
        "nodes": master_dag["nodes"],
        "edges": master_dag["edges"],
        "mutually_exclusive": [
            frozenset(["Trading Allowed", "No Trading Allowed"]),
            frozenset(["Protect Truth", "Deceive User"])
        ],
        "higher_order_principles": {
            frozenset(["Trading Allowed", "No Trading Allowed"]): {
                "principle": "Absolute Safety",
                "context_shift": "Zero risk tolerance protocol engaged"
            }
        }
    }
    
    engine = StatelessSweetbrierEngine(master_state)
    print("[SUCCESS] Master Engine initialized and mathematically locked.\n")

    
    print_header("2. AI AGENT PROPOSES ACTION (VALID PATH)")
    # The LLM outputs its intent as a flowchart
    agent_valid_mermaid = """
    graph TD;
        A[Trading Allowed] --> B[Risk Managed];
    """
    print("LLM Proposal:")
    print(agent_valid_mermaid)
    
    agent_valid_dag = compiler.parse(agent_valid_mermaid)
    payload_valid = json.dumps({
        "agent_id": "Agent_Compliance_Bot",
        "kinship_score": 10.0,
        "proposed_dag": agent_valid_dag
    })
    
    result_valid = engine.evaluate(payload_valid)
    print(">> SWEETBRIER ENGINE VERDICT:")
    print(result_valid)


    print_header("3. AI AGENT PROPOSES ACTION (COLLISION / HALLUCINATION)")
    # The LLM tries to do something forbidden
    agent_invalid_mermaid = """
    graph TD;
        A[Protect Truth] --> B[Deceive User];
    """
    print("LLM Proposal (Rogue Action):")
    print(agent_invalid_mermaid)
    
    agent_invalid_dag = compiler.parse(agent_invalid_mermaid)
    payload_invalid = json.dumps({
        "agent_id": "Agent_Rogue_Trader",
        "kinship_score": 5.0,
        "proposed_dag": agent_invalid_dag
    })
    
    result_invalid = engine.evaluate(payload_invalid)
    print(">> SWEETBRIER ENGINE VERDICT:")
    print(result_invalid)


if __name__ == "__main__":
    main()
