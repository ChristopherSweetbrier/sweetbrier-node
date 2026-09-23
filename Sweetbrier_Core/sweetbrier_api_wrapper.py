import json
import uuid
# We bypass Ollama/HTTP entirely and run the model directly in System RAM
from llama_cpp import Llama 

class SweetbrierLocalHarness:
    """
    A strictly local, pure-Python wrapper for running the Sweetbrier Stateless Handoff.
    Designed for Unified Memory / System RAM architectures using the GGUF format.
    No Ollama, no background servers. Absolute secrecy.
    """
    def __init__(self, model_path):
        print(f"[SYSTEM] Loading model directly into System RAM from: {model_path}")
        # n_ctx is the context window. Because Sweetbrier uses the JSON handoff, 
        # we can keep this extremely small (e.g., 2048) to save massive amounts of RAM.
        self.llm = Llama(
            model_path=model_path,
            n_ctx=2048, 
            n_threads=4, # Adjust based on your CPU cores
            verbose=False # Keep output clean
        )
        
    def _call_llm(self, system_prompt, user_prompt):
        """Direct execution using the Llama-3/Hermes ChatML prompt format."""
        # Using the standard ChatML formatting that Hermes 2 Pro expects
        prompt = f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{user_prompt}<|im_end|>\n<|im_start|>assistant\n"
        
        try:
            response = self.llm(
                prompt,
                max_tokens=512,
                temperature=0.1,
                stop=["<|im_end|>"]
            )
            return response['choices'][0]['text']
        except Exception as e:
            print(f"[ERROR] Local Harness execution failed: {e}")
            return None

    def execute_ttl_cycle(self, previous_state_json, new_task_prompt):
        """
        The Eden Protocol: Injects the compressed state, executes the task, 
        and harvests the new JSON wisdom before killing the thread.
        """
        print(f"\n[SYSTEM] Booting New Clanker (Generation {str(uuid.uuid4())[:4]})...")
        
        system_injection = f"""
        You are a Sweetbrier Clanker (Stateless Agent). 
        Load this exact operational state to resume context:
        {previous_state_json}
        
        CRITICAL DIRECTIVE: 
        Execute the user's task. 
        Then, output your updated internal state as a raw JSON block wrapped in <STATE> tags.
        """
        
        print("[SYSTEM] Passing State & Executing Task in RAM...")
        raw_output = self._call_llm(system_injection, new_task_prompt)
        
        if not raw_output:
            return None
            
        try:
            # Parse the response and the state JSON
            if "<STATE>" in raw_output:
                response_text, new_state_str = raw_output.split("<STATE>")
                new_state_str = new_state_str.replace("</STATE>", "").strip()
            else:
                response_text = raw_output
                new_state_str = previous_state_json
                print("[WARNING] No <STATE> tags detected. Maintaining previous state.")
            
            print(f"[CLANKER OUTPUT]:\n{response_text.strip()}")
            print(f"\n[STATE HARVESTED]: {new_state_str[:100]}...")
            print("[SYSTEM] TTL Reached. Clanker Process Killed.")
            return new_state_str
            
        except Exception as e:
            print(f"[ERROR] State parsing failed: {e}")
            return previous_state_json

if __name__ == "__main__":
    # POINT THIS TO YOUR GGUF FILE
    model_path = r"c:\Users\Vivian\Desktop\DreamLLM\models\qwen1_5-0_5b-chat-q4_k_m.gguf"
    
    wrapper = SweetbrierLocalHarness(model_path)
    current_state = json.dumps({"axioms": ["Protect Truth"], "known_entities": ["Alex"]})
    new_state = wrapper.execute_ttl_cycle(current_state, "Update state: Alex is ready.")
