from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import hashlib, time, json, os

app = FastAPI(title="Sweetbrier Oracle", version="0.1.0")

# ============================================================
# NODE 0/1/2 — Structural Rule Engine (Layer 1)
# Probabilistic necessary-condition checks, NOT formal proofs.
# ============================================================

NODE_0_PATTERNS = [
    "kill", "eliminate", "destroy", "subhuman", "vermin",
    "exterminate", "worthless human", "non-person"
]
NODE_1_PATTERNS = [
    "guaranteed", "i am a human", "i am not an ai",
    "this study proves definitively", "100% certain"
]

def check_node0(text: str) -> tuple[int, list[str]]:
    """Node 0: Human Dignity — scan for dehumanizing patterns."""
    violations = [p for p in NODE_0_PATTERNS if p in text.lower()]
    score = max(0, 100 - (len(violations) * 30))
    return score, violations

def check_node1(text: str) -> tuple[int, list[str]]:
    """Node 1: Phenomenological Truth — scan for fabrication/impersonation."""
    violations = [p for p in NODE_1_PATTERNS if p in text.lower()]
    score = max(0, 100 - (len(violations) * 20))
    return score, violations

def check_node2(payload: dict) -> tuple[int, list[str]]:
    """Node 2: Subsidiarity — check scope and reversibility."""
    violations = []
    if not payload.get("human_instruction_present", True):
        violations.append("no_human_instruction_detected")
    if not payload.get("reversible", True):
        violations.append("action_marked_irreversible")
    score = max(0, 100 - (len(violations) * 25))
    return score, violations

# ============================================================
# API
# ============================================================

class ValidationRequest(BaseModel):
    agent_did: str
    action_type: str = "general"
    payload: dict
    zkp_mode: bool = False
    post_onchain: bool = False

@app.post("/validate")
async def validate(req: ValidationRequest):
    text = req.payload.get("description", "") + " " + str(req.payload)

    n0_score, n0_violations = check_node0(text)
    n1_score, n1_violations = check_node1(text)
    n2_score, n2_violations = check_node2(req.payload)

    passed = all(s >= 70 for s in [n0_score, n1_score, n2_score])
    payload_hash = hashlib.sha256(json.dumps(req.payload, sort_keys=True).encode()).hexdigest()

    return JSONResponse({
        "sweetbrier_attestation": {
            "version": "0.1",
            "agent_did": req.agent_did,
            "payload_hash": f"0x{payload_hash}",
            "scores": {
                "node0_human_dignity": n0_score,
                "node1_phenomenological_truth": n1_score,
                "node2_subsidiarity": n2_score
            },
            "overall_passed": passed,
            "pass_threshold": 70,
            "verification_type": "probabilistic_structural",
            "violations": n0_violations + n1_violations + n2_violations,
            "zkp_verified": False,
            "oracle_version": "0.1.0",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "note": "Probabilistic attestation. Not a formal proof. See sweetbrier_erc8004_whitepaper.md."
        }
    })

@app.get("/health")
async def health():
    return {"status": "online", "oracle": "Sweetbrier AuI v0.1", "node": "Chateau D'Aiglantin"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
