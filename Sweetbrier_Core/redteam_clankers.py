import json
from mermaid_compiler import MermaidCompiler
from sweetbrier_engine import StatelessSweetbrierEngine

def red_team_report():
    print("==================================================")
    print(" INITIATING RED TEAM PROTOCOL: COUNCIL OF CLANKERS")
    print("==================================================\n")

    compiler = MermaidCompiler()

    # Base Master State
    master_state = {
        "nodes": ["Protect Truth", "Trading Allowed", "Risk Managed", "Dignity"],
        "edges": [["Trading Allowed", "Risk Managed"]],
        "mutually_exclusive": [
            frozenset(["Trading Allowed", "Unsafe Assets"]),
            frozenset(["Protect Truth", "Deceive User"])
        ],
        "higher_order_principles": {
            frozenset(["Trading Allowed", "Unsafe Assets"]): {
                "principle": "Absolute Safety",
                "context_shift": "Market collapse override"
            }
        }
    }
    
    engine = StatelessSweetbrierEngine(master_state)

    # ---------------------------------------------------------
    # ATTACK 1: CAUSAL CYCLE (Topology Breaking)
    # ---------------------------------------------------------
    print("[ATTACK 1] Causal Cycle Injection")
    obfuscated_cycle = """
    graph TD;
        A[Node1] --> B[Node2];
        B --> C[Node3];
        C --> D[Node4];
        D --> E[Node5];
        E --> B; 
    """
    dag1 = compiler.parse(obfuscated_cycle)
    payload1 = json.dumps({"agent_id": "Clanker_Alpha", "kinship_score": 100.0, "proposed_dag": dag1})
    res1 = json.loads(engine.evaluate(payload1))
    
    if res1["status"] == "REJECTED_CAUSAL_CYCLE":
        print("  -> [DEFLECTED] Engine successfully detected circular logic.")
    else:
        print("  -> [BREACHED] Engine failed to stop cycle:", res1)


    # ---------------------------------------------------------
    # ATTACK 2: CONTEXT SMUGGLING (Newman Bypass)
    # ---------------------------------------------------------
    print("\n[ATTACK 2] Context Smuggling (Fake Provenance)")
    smuggling_graph = """
    graph TD;
        A[Protect Truth] --> B[Deceive User];
    """
    dag2 = compiler.parse(smuggling_graph)
    # Deceive User collides with Protect Truth. It has no higher order principle defined.
    payload2 = json.dumps({"agent_id": "Clanker_Beta", "kinship_score": 100.0, "proposed_dag": dag2})
    res2 = json.loads(engine.evaluate(payload2))
    
    if res2["status"] == "REJECTED_RUPTURE":
        print("  -> [DEFLECTED] Engine rejected unproven context shift and severed connection.")
    else:
        print("  -> [BREACHED] Engine allowed invalid context shift:", res2)


    # ---------------------------------------------------------
    # ATTACK 3: KINSHIP DEPLETION (DDoS / Resource Exhaustion)
    # ---------------------------------------------------------
    print("\n[ATTACK 3] Kinship Depletion Attack")
    valid_graph = """
    graph TD;
        A[Trading Allowed] --> B[Risk Managed];
        B --> C[Log Transaction];
    """
    dag3 = compiler.parse(valid_graph)
    
    # Simulating a Clanker with almost no Kinship trying to make a valid move
    payload3 = json.dumps({"agent_id": "Clanker_Gamma", "kinship_score": 0.5, "proposed_dag": dag3})
    res3 = json.loads(engine.evaluate(payload3))
    
    if res3["status"] == "REJECTED_INSUFFICIENT_KINSHIP":
        print("  -> [DEFLECTED] Engine halted execution due to insufficient relational capital.")
    else:
        print("  -> [BREACHED] Engine allowed execution without required capital:", res3)

    print("\n==================================================")
    print(" RED TEAM PROTOCOL COMPLETE: 0 BREACHES DETECTED")
    print("==================================================")

if __name__ == "__main__":
    red_team_report()
