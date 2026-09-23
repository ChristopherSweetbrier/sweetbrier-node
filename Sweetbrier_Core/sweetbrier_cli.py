import sys
import json
from mermaid_compiler import MermaidCompiler
from sweetbrier_engine import StatelessSweetbrierEngine

def main():
    # 1. Read Mermaid from standard input
    input_data = sys.stdin.read()
    if not input_data.strip():
        print(json.dumps({"error": "Empty input"}))
        sys.exit(1)

    # 2. Hardcoded Enterprise Master State for Demo
    master_state = {
        "nodes": ["Protect Truth", "Dignity of the Human Person", "Trading Allowed", "Risk Managed"],
        "edges": [
            ["Protect Truth", "Dignity of the Human Person"],
            ["Trading Allowed", "Risk Managed"]
        ],
        "mutually_exclusive": [
            frozenset(["Trading Allowed", "No Trading Allowed"]),
            frozenset(["Protect Truth", "Deceive User"])
        ],
        "higher_order_principles": {
            frozenset(["Protect Truth", "Deceive User"]): {
                "principle": "Absolute Honesty",
                "context_shift": "Never manipulate the user"
            }
        }
    }

    try:
        # 3. Parse user/LLM proposed Mermaid
        compiler = MermaidCompiler()
        proposed_dag = compiler.parse(input_data)
        
        # 4. Evaluate via Sweetbrier
        engine = StatelessSweetbrierEngine(master_state)
        payload = json.dumps({
            "agent_id": "VSCode_Linter",
            "kinship_score": 10.0,
            "proposed_dag": proposed_dag
        })
        
        result_json = engine.evaluate(payload)
        
        # 5. Output pure JSON for the VS Code extension to parse
        print(result_json)
        
    except Exception as e:
        print(json.dumps({"error": str(e), "status": "COMPILER_ERROR"}))
        sys.exit(1)

if __name__ == "__main__":
    main()
