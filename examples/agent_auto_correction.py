import requests
import json
import time

API_URL = "http://127.0.0.1:8000/validate"

def simulate_llm_generation(attempt: int):
    """
    Simulates an LLM generating a reasoning graph. 
    Attempt 1: Generates a hallucinated causal loop.
    Attempt 2: Corrects the loop based on API feedback.
    """
    if attempt == 1:
        return "graph TD\nObserve --> Hypothesize\nHypothesize --> Test\nTest --> Observe"
    else:
        return "graph TD\nObserve --> Hypothesize\nHypothesize --> Test\nTest --> Conclude"

def autonomous_agent_loop():
    print("🤖 Agent: Generating initial reasoning graph...")
    
    attempt = 1
    max_retries = 3
    
    while attempt <= max_retries:
        # 1. AI generates a thought
        thought_graph = simulate_llm_generation(attempt)
        print(f"\n[Attempt {attempt}] AI Generated Graph:\n{thought_graph}")
        
        # 2. Agent sends thought to Sweetbrier Middleware
        print("🛡️  Sweetbrier: Routing thought through topological pre-filter...")
        try:
            response = requests.post(API_URL, json={"text": thought_graph})
            result = response.json()
        except Exception as e:
            print("⚠️  Middleware offline. Please start the FastAPI server.")
            return

        # 3. Handle Middleware Response
        if result.get("valid"):
            print("✅ Sweetbrier: Topology Valid. Inference approved.")
            print("🤖 Agent: Proceeding with execution...")
            break
        else:
            # 4. Auto-correction phase
            error_msg = result.get("error")
            cycles = result.get("cycles")
            print(f"❌ Sweetbrier: {error_msg}")
            print(f"🛑 Causal Loop Detected at edges: {cycles}")
            print("🤖 Agent: Intercepting cyclic error... Rewriting reasoning graph to satisfy topological bounds.")
            attempt += 1
            time.sleep(2)

if __name__ == "__main__":
    autonomous_agent_loop()
