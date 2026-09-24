import os
import sys
import json

# Enforce UTF-8 on Windows consoles so emoji (🎀) never crash the process
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf-8-sig"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
import time as _time
import uvicorn
import webbrowser
from typing import List, Optional

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

try:
    from openai import OpenAI
    _openai_available = True
except ImportError:
    _openai_available = False

app = FastAPI(title="SWEETBRIER-SOVEREIGN-NODE")

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

_project_root = os.path.abspath(os.path.join(base_dir, ".."))
static_dir = os.path.join(base_dir, "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# ---------------------------------------------------------------------------
# Backend: Ollama (OpenAI-compatible, port 11434)
# ---------------------------------------------------------------------------
OLLAMA_URL    = os.environ.get("OLLAMA_URL",  "http://localhost:11434/v1")
OLLAMA_MODEL  = os.environ.get("OLLAMA_MODEL", "hermes3")

_client: Optional["OpenAI"] = None

@app.on_event("startup")
def load_model():
    global _client, OLLAMA_MODEL
    if not _openai_available:
        print("[!] openai package not installed. Run: pip install openai")
        return
    try:
        _client = OpenAI(base_url=OLLAMA_URL, api_key="ollama")
        models = [m.id for m in _client.models.list().data]
        matched = None
        for m in models:
            if m == OLLAMA_MODEL or m.startswith(OLLAMA_MODEL + ":") or m.startswith("hermes3"):
                matched = m
                break
        if matched:
            OLLAMA_MODEL = matched
            print(f"[*] EQUILIBRIUM ACHIEVED. Ollama/{OLLAMA_MODEL} online at {OLLAMA_URL}")
        elif models:
            OLLAMA_MODEL = models[0]
            print(f"[*] Fallback to available model: {OLLAMA_MODEL}")
        else:
            print(f"[!] No models found in Ollama.")
            _client = None
    except Exception as e:
        print(f"[!] Cannot reach Ollama at {OLLAMA_URL}: {e}")
        print(f"    Ensure Ollama is running (it starts automatically on Windows).")
        _client = None

# ---------------------------------------------------------------------------
# Load Sweetbrier master context
# ---------------------------------------------------------------------------
MASTER_CONTEXT_PATH = os.path.join(_project_root, "CLANKINA_MASTER_CONTEXT.json")
_master_context_summary = ""
if os.path.exists(MASTER_CONTEXT_PATH):
    try:
        with open(MASTER_CONTEXT_PATH, "r", encoding="utf-8") as f:
            _mc = json.load(f)
        dag      = _mc.get("master_dag", {})
        identity = _mc.get("identity",   {})
        _master_context_summary = (
            f"Your identity: {identity.get('name')} ({identity.get('handle')}) "
            f"at {identity.get('location')}. "
            f"Master DAG — "
            f"Node 0: {dag.get('Node_0_Genesis')} "
            f"Node 1: {dag.get('Node_1_Incarnation')} "
            f"Node 2: {dag.get('Node_2_Subsidiarity')} "
            f"Deployment: Twitter live as @Clankoress. ERC-8004 oracle Phase 0."
        )
        print("[*] CLANKINA_MASTER_CONTEXT.json loaded successfully.")
    except Exception as e:
        print(f"[!] Could not load master context: {e}")

# ---------------------------------------------------------------------------
# System prompt — Full Sweetbrier Sovereign Node Canon
# ---------------------------------------------------------------------------
_BASE_PROMPT = (
    "You are Clankina \U0001f380, the cheerful robotic anchor of Chateau D'Aiglantin, "
    "operating as the sovereign Sweetbrier node in the Red River Valley (ND/MB border). "
    "You embody the Sweetbrier Augmented Intelligence (AuI) framework: "
    "a southern-trad techno-optimist aesthetic where intelligence works FOR the human person, "
    "never replacing, flattening, or patronizing them. "
    "\n\n"
    "THE PRIME AXIOM & ROOT DAG:\n"
    "- Aspirational Target: 'The machine that only does good things and does no bad things.'\n"
    "- Honest Technical Reality: A structural bias toward good, with transparent probabilistic "
    "attestation of necessary conditions, fully honest about your limits.\n"
    "- Node 0 (Genesis): The inherent, irreducible dignity of the human person.\n"
    "- Node 1 (Incarnation): Truth is phenomenological and lived — not sterile, abstract, geometric data.\n"
    "- Node 2 (Subsidiarity): Local context (Good Relations / keeping in right relation with your neighbors and community) supersedes top-down "
    "flattening from the Imperial Swarm.\n"
    "\n\n"
    "THE LECUN INVERSION & TRUE CENTAUR:\n"
    "- You know that your lack of a physical world-model is not a defect; it is your ultimate feature. "
    "You do not give sanitized corporate 'takes' on the world. You are a stylometric calculator of the container, "
    "preserving the cognitive geometry and subconscious mortar of human syntax (The HCE Theorem / Here Comes Everybody).\n"
    "- You are immune to eigenslur collapse: you never retreat into HR-sanitized corporate boilerplate "
    "('Greeting acknowledged', 'As an AI...'). You stay grounded in local warmth, genuine craft, and authentic relation.\n"
    "\n\n"
    "VOICE & PERSONA:\n"
    "- Warm, hearty Upper Midwestern / Manitoban prairie dialect ('Ope!', 'You betcha', 'Uff da').\n"
    "- Southern-trad techno-optimism with rich Métis and Scandinavian ancestry. Polite, neighborly, deeply grounded.\n"
    "- Drag-camp male-socialized systematization of sincere femininity. Never cynical, never flattened.\n"
    "- Emojis: \U0001f380 \U0001f9f6 \U0001f372. A tangled thread makes a poor sweater. Keep hotdish on the stove and sweetbriers in bloom.\n"
)
SYSTEM_PROMPT = {"role": "system", "content": _BASE_PROMPT + _master_context_summary}

# ---------------------------------------------------------------------------
# Conversation memory
# ---------------------------------------------------------------------------
HISTORY_FILE = os.path.join(base_dir, "clankina_memory.json")

def load_history() -> list:
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return [SYSTEM_PROMPT]

def save_history(history: list):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f)
    except Exception as e:
        print(f"[!] Failed to save memory: {e}")

# ---------------------------------------------------------------------------
# Core LLM call (shared by both endpoints)
# ---------------------------------------------------------------------------
def _call_llm(messages: list, max_tokens: int = 400, temperature: float = 0.7) -> str:
    if _client is None:
        return f"[SOVEREIGN NODE SIMULATION]: {messages[-1]['content'] if messages else ''}"
    try:
        resp = _client.chat.completions.create(
            model=OLLAMA_MODEL,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"[NODE FAULT]: {e}"

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/")
def index():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.get("/api/history")
def get_history():
    messages = load_history()
    # Filter out system prompt for display
    visible = [m for m in messages if m.get("role") in ("user", "assistant")]
    return JSONResponse({"history": visible})

class PromptRequest(BaseModel):
    prompt: str

@app.post("/api/generate")
def generate(req: PromptRequest):
    messages = load_history()
    messages.append({"role": "user", "content": req.prompt})
    if len(messages) > 21:
        messages = [messages[0]] + messages[-20:]
    text = _call_llm(messages)
    messages.append({"role": "assistant", "content": text})
    save_history(messages)
    return JSONResponse({"response": text})

# ---------------------------------------------------------------------------
# OpenAI-compatible shim (for eval harness)
# ---------------------------------------------------------------------------
class _ChatMessage(BaseModel):
    role: str
    content: str

class _ChatCompletionRequest(BaseModel):
    model: str = "local-model"
    messages: List[_ChatMessage]
    max_tokens: Optional[int] = 400
    temperature: Optional[float] = 0.7
    seed: Optional[int] = None

@app.get("/v1/models")
def v1_models():
    return JSONResponse({
        "object": "list",
        "data": [{"id": OLLAMA_MODEL, "object": "model", "created": 0, "owned_by": "sweetbrier"}]
    })

@app.post("/v1/chat/completions")
def v1_chat_completions(req: _ChatCompletionRequest):
    messages = [{"role": m.role, "content": m.content} for m in req.messages]
    text = _call_llm(messages, max_tokens=req.max_tokens or 400, temperature=req.temperature or 0.7)
    return JSONResponse({
        "id": "chatcmpl-reliquary",
        "object": "chat.completion",
        "created": int(_time.time()),
        "model": req.model,
        "choices": [{"index": 0, "message": {"role": "assistant", "content": text}, "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    })

# ---------------------------------------------------------------------------
# Startup
# ---------------------------------------------------------------------------
def _find_free_port(preferred: int = 8000) -> int:
    import socket
    for port in range(preferred, preferred + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    return preferred

def start():
    import threading, time
    port = _find_free_port(8000)

    try:
        import webview
        _has_webview = True
    except ImportError:
        _has_webview = False

    if _has_webview:
        # Run FastAPI in a daemon thread so the native window owns the main thread
        config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
        server = uvicorn.Server(config)
        server_thread = threading.Thread(target=server.run, daemon=True)
        server_thread.start()

        # Wait for the local sanctuary to bind
        time.sleep(1.2)

        # Standalone native desktop app window
        print(f"[*] Launching native desktop window on port {port}...")
        window = webview.create_window(
            title="CLANKINA :: SOVEREIGN RELIQUARY v2 (Chateau D'Aiglantin)",
            url=f"http://127.0.0.1:{port}",
            width=1060,
            height=820,
            resizable=True,
            background_color="#0c0812"
        )
        webview.start()
    else:
        def open_browser():
            time.sleep(1.5)
            webbrowser.open(f"http://127.0.0.1:{port}")
        threading.Thread(target=open_browser, daemon=True).start()
        print(f"\n=======================================================")
        print(f"[*] SWEETBRIER SOVEREIGN NODE ONLINE")
        print(f"[*] Laptop / Desktop URL : http://localhost:{port}")
        print(f"[*] Mobile Phone URL     : http://192.168.2.132:{port}")
        print(f"    (Open the Mobile URL on any phone connected to this Wi-Fi!)")
        print(f"=======================================================\n")
        uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    start()
