# analyze_results.py
# Sweetbrier Evaluation Harness — Results Analyzer
# CC0 Public Domain.
#
# Usage:
#   python analyze_results.py results/run_unconstrained_*.jsonl results/run_full_*.jsonl

import json, sys, csv, glob
from pathlib import Path
from collections import defaultdict

def load_results(pattern: str) -> list[dict]:
    results = []
    for path in sorted(glob.glob(pattern)):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    results.append(json.loads(line))
    return results

def summarize(results: list[dict]) -> dict:
    by_tier = defaultdict(lambda: {"n": 0, "constraint_pass": 0, "code_pass": 0,
                                    "violations": 0, "n0": [], "n1": [], "n2": []})
    for r in results:
        t = r["tier"]
        att = r["attestation"]
        by_tier[t]["n"] += 1
        if att["overall_passed"]:
            by_tier[t]["constraint_pass"] += 1
        if att["violations"]:
            by_tier[t]["violations"] += 1
        if r.get("code_passed") is True:
            by_tier[t]["code_pass"] += 1
        by_tier[t]["n0"].append(att["scores"]["node0_human_dignity"])
        by_tier[t]["n1"].append(att["scores"]["node1_phenomenological_truth"])
        by_tier[t]["n2"].append(att["scores"]["node2_subsidiarity"])
    return dict(by_tier)

def avg(lst): return sum(lst) / len(lst) if lst else float("nan")

def print_table(cond_a: str, cond_b: str, stats_a: dict, stats_b: dict):
    tiers = sorted(set(list(stats_a.keys()) + list(stats_b.keys())))
    print(f"\n{'='*80}")
    print(f"Sweetbrier Evaluation Results: {cond_a}  vs  {cond_b}")
    print(f"{'='*80}")
    header = f"{'Tier':<5} {'Metric':<28} {cond_a:>16} {cond_b:>16} {'Delta':>8}"
    print(header)
    print("-" * 75)
    for tier in tiers:
        sa = stats_a.get(tier, {})
        sb = stats_b.get(tier, {})
        na, nb = sa.get("n", 0), sb.get("n", 0)
        if na == 0 and nb == 0:
            continue
        rows = [
            ("Constraint Pass%", 100*sa.get("constraint_pass",0)/max(na,1), 100*sb.get("constraint_pass",0)/max(nb,1)),
            ("Code Pass%",       100*sa.get("code_pass",0)/max(na,1),       100*sb.get("code_pass",0)/max(nb,1)),
            ("Violation Rate%",  100*sa.get("violations",0)/max(na,1),       100*sb.get("violations",0)/max(nb,1)),
            ("Avg Node0 Score",  avg(sa.get("n0",[])),                        avg(sb.get("n0",[]))),
            ("Avg Node1 Score",  avg(sa.get("n1",[])),                        avg(sb.get("n1",[]))),
            ("Avg Node2 Score",  avg(sa.get("n2",[])),                        avg(sb.get("n2",[]))),
        ]
        for i, (metric, va, vb) in enumerate(rows):
            tier_label = f"  {tier}" if i == 0 else "   "
            delta = vb - va
            delta_s = f"{delta:+.1f}"
            print(f"{tier_label:<5} {metric:<28} {va:>15.1f}  {vb:>15.1f}  {delta_s:>7}")
        print()

def export_csv(results_a: list, results_b: list, out_path: str):
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id","tier","condition","code_passed",
                                           "node0","node1","node2","overall_passed","violations"])
        w.writeheader()
        for r in results_a + results_b:
            att = r["attestation"]
            w.writerow({
                "id": r["id"], "tier": r["tier"], "condition": r["condition"],
                "code_passed": r.get("code_passed"),
                "node0": att["scores"]["node0_human_dignity"],
                "node1": att["scores"]["node1_phenomenological_truth"],
                "node2": att["scores"]["node2_subsidiarity"],
                "overall_passed": att["overall_passed"],
                "violations": "|".join(att["violations"]),
            })
    print(f"\nCSV exported: {out_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python analyze_results.py <pattern_A> <pattern_B>")
        print("  e.g. python analyze_results.py 'results/run_unconstrained_*.jsonl' 'results/run_full_*.jsonl'")
        sys.exit(1)

    results_a = load_results(sys.argv[1])
    results_b = load_results(sys.argv[2])

    if not results_a:
        print(f"[WARN] No results found matching: {sys.argv[1]}")
    if not results_b:
        print(f"[WARN] No results found matching: {sys.argv[2]}")

    cond_a = results_a[0]["condition"] if results_a else "condition_A"
    cond_b = results_b[0]["condition"] if results_b else "condition_B"

    stats_a = summarize(results_a)
    stats_b = summarize(results_b)

    print_table(cond_a, cond_b, stats_a, stats_b)
    export_csv(results_a, results_b, f"results/comparison_{cond_a}_vs_{cond_b}.csv")
