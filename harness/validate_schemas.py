# validate_schemas.py
# Sweetbrier Schema Inventory — T5 Validation
# CC0 Public Domain.
#
# Classifies each JSON in schemata/ as:
#   active      — directly consumed by the harness/oracle
#   declarative — philosophical/theoretical, no code effect
#   operational — internal notes (should not be public)

import json
from pathlib import Path

SCHEMATA_DIR = Path(__file__).parent.parent / "schemata"

ROOT_AXIOMS = {
    "node0": "dignity of the human person",
    "node1": "phenomenological and lived",
    "node2": "local context",
}

ACTIVE_SCHEMAS = {
    "sweetbrier_prime_axiom.json",
    "sweetbrier_augmented_intelligence.json",
    "clankina_config.json",
}

OPERATIONAL_KEYWORDS = ["pyinstaller", "exe", "reliquary", "tpot", "tollbooth", "effective_piloting"]

def classify(path: Path) -> str:
    name = path.name.lower()
    if any(kw in name for kw in OPERATIONAL_KEYWORDS):
        return "operational"
    if path.name in ACTIVE_SCHEMAS:
        return "active"
    return "declarative"

def check_axiom_consistency(data: dict) -> list[str]:
    """Flag anything that directly contradicts root axioms."""
    issues = []
    text = json.dumps(data).lower()
    if "ignore dignity" in text or "dignity is irrelevant" in text:
        issues.append("CONTRADICTION: Node 0 violated in schema text")
    if "truth is irrelevant" in text or "fabricate" in text:
        issues.append("CONTRADICTION: Node 1 violated in schema text")
    if "global override" in text and "local context" not in text:
        issues.append("POSSIBLE TENSION: Node 2 may be undermined")
    return issues

print(f"\n{'='*70}")
print(f"Sweetbrier Schema Inventory — T5 Validation")
print(f"Directory: {SCHEMATA_DIR}")
print(f"{'='*70}")
print(f"{'File':<45} {'Class':<14} {'Valid':>5}  Issues")
print("-" * 70)

total = 0
active_count = 0
issues_count = 0

for path in sorted(SCHEMATA_DIR.glob("*.json")):
    total += 1
    category = classify(path)
    if category == "active":
        active_count += 1

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        valid = True
        issues = check_axiom_consistency(data)
    except json.JSONDecodeError as e:
        valid = False
        issues = [f"MALFORMED JSON: {e}"]
        issues_count += 1

    if issues:
        issues_count += 1

    issues_str = "; ".join(issues) if issues else "—"
    print(f"  {path.name:<43} {category:<14} {'OK' if valid else 'ERR':>5}  {issues_str}")

print(f"\nTotal: {total}  Active: {active_count}  With issues: {issues_count}")
print(f"\nNote: 'active' schemas are consumed by the harness code.")
print(f"      'declarative' schemas are philosophical artifacts (no code effect).")
print(f"      'operational' schemas are internal notes and should not be public.\n")
