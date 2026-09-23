import json
import requests
import uuid

class OllamaEdenProtocol:
    """
    Sweetbrier Stateless Implementation for Ollama.
    Enforces the Eden Protocol (TTL Mortality) by setting keep_alive: 0.
    Shrinks context footprint to allow massive models (like 35B Qwen) to run on unified RAM.
    """
    def __init__(self, endpoint="http://localhost:11434/api/chat", model_name="qwen"):
        self.endpoint = endpoint
        self.model = model_name
        
    def _call_llm(self, system_prompt, user_prompt):
        """Standard API call with strict RAM-purging parameters."""
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "options": {
                "temperature": 0.1,
                "num_ctx": 2048  # The Bounding Box: Restrict memory footprint
            },
            "keep_alive": 0, # THE EDEN PROTOCOL: Force RAM purge immediately after JSON generation
            "stream": False
        }
        
        try:
            response = requests.post(self.endpoint, json=payload)
            response.raise_for_status()
            return response.json()['message']['content']
        except Exception as e:
            print(f"[ERROR] Ollama API execution failed: {e}")
            return None

    def execute_ttl_cycle(self, previous_state_json, new_task_prompt):
        """
        Injects state -> Executes -> Outputs new state -> Dies.
        """
        print(f"\n[SYSTEM] Booting New Clanker (Generation {str(uuid.uuid4())[:4]})...")
        
        system_injection = f"""
        You are a Sweetbrier Clanker (Stateless Agent). 
        You have no chat history. Load this exact operational state to resume context:
        {previous_state_json}
        
        CRITICAL DIRECTIVE: 
        Execute the user's task based on your loaded state. 
        Then, you MUST output your new, updated internal state as a raw JSON block at the very end of your response, wrapped in <STATE> tags.
        """
        
        print(f"[SYSTEM] Injecting State & Executing Task on {self.model}...")
        raw_output = self._call_llm(system_injection, new_task_prompt)
        
        if not raw_output:
            return None
            
        try:
            if "<STATE>" in raw_output:
                response_text, new_state_str = raw_output.split("<STATE>")
                new_state_str = new_state_str.replace("</STATE>", "").strip()
            else:
                response_text = raw_output
                new_state_str = previous_state_json
                print("[WARNING] No <STATE> tags detected. Maintaining previous state.")
            
            print(f"\n[CLANKER OUTPUT]:\n{response_text.strip()}")
            print(f"\n[STATE HARVESTED]: {new_state_str[:100]}...")
            
            # Ollama automatically unloads the model from RAM here due to keep_alive: 0
            print("[SYSTEM] TTL Reached. Ollama RAM Purged. Clanker Process Killed.")
            return new_state_str
            
        except Exception as e:
            print(f"[ERROR] State parsing failed: {e}")
            return previous_state_json

if __name__ == "__main__":
    # Ensure Ollama is running in the background and you have pulled the qwen model
    # (e.g., run `ollama run qwen` once in your terminal to ensure it exists)
    wrapper = OllamaEdenProtocol(model_name="qwen") # Change to your specific ollama tag if needed
    
    current_state = json.dumps({
        "axioms": ["Protect Truth"], 
        "known_entities": ["Alex (Ally)"],
        "active_protocol": "The Eden Firewall"
    })
    
    new_task = "Briefly explain how setting keep_alive to 0 mimics mortality. Update state to reflect execution."
    new_state = wrapper.execute_ttl_cycle(current_state, new_task)
