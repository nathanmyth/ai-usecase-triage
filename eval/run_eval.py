"""Evaluate triage against reviewer-labeled cases.

    python -m eval.run_eval --rules-only   # free, deterministic
    python -m eval.run_eval                # hybrid (needs ANTHROPIC_API_KEY)

Under-classification (system tier below the reviewer's) is the P0 metric.
"""
import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

from src.policy import load_policy, rank
from src.triage import triage

HERE = Path(__file__).parent
TARGETS = {"accuracy": (0.85, ">="), "under_classification": (0.0, "<="), "over_classification": (0.20, "<=")}


def load_cases() -> list[dict]:
    return [json.loads(l) for l in (HERE / "eval_set.jsonl").read_text().splitlines() if l.strip()]


def metrics(rows: list[dict]) -> dict:
    n = len(rows) or 1
    return {
        "accuracy": sum(r["predicted"] == r["expected"] for r in rows) / n,
        "under_classification": sum(rank(r["predicted"]) < rank(r["expected"]) for r in rows) / n,
        "over_classification": sum(rank(r["predicted"]) > rank(r["expected"]) for r in rows) / n,
        "n": len(rows),
    }


def run(use_llm: bool) -> dict:
    rows = []
    for c in load_cases():
        t = triage(c["title"], c["description"], use_llm=use_llm)
        rows.append({**c, "predicted": t.tier, "rules_tier": t.rules_tier, "llm_tier": t.llm_tier, "mode": t.mode})
    by_split = {s: metrics([r for r in rows if r["split"] == s]) for s in sorted({r["split"] for r in rows})}
    return {"run_at": datetime.now().isoformat(timespec="seconds"), "mode": rows[0]["mode"],
            "overall": metrics(rows), "by_split": by_split, "rows": rows}


def print_report(result: dict) -> None:
    print(f"\nMode: {result['mode']}\n")
    print(f"{'Slice':<14}{'n':>4}{'Accuracy':>11}{'Under':>9}{'Over':>9}")
    print("-" * 47)
    for name, m in [("overall", result["overall"]), *result["by_split"].items()]:
        print(f"{name:<14}{m['n']:>4}{m['accuracy']:>11.0%}{m['under_classification']:>9.0%}{m['over_classification']:>9.0%}")

    print("\nTargets (overall):")
    for k, (target, op) in TARGETS.items():
        v = result["overall"][k]
        ok = v >= target if op == ">=" else v <= target
        print(f"  {k:<22}{v:>6.0%}  target {op} {target:.0%}   {'PASS' if ok else 'FAIL'}")

    tiers = [t["id"] for t in load_policy()["tiers"]]
    cm = Counter((r["expected"], r["predicted"]) for r in result["rows"])
    print("\nConfusion matrix (rows = reviewer label, cols = predicted):")
    print(" " * 12 + "".join(f"{t[:10]:>12}" for t in tiers))
    for e in tiers:
        print(f"{e[:10]:<12}" + "".join(f"{cm[(e, p)]:>12}" for p in tiers))

    misses = [r for r in result["rows"] if rank(r["predicted"]) < rank(r["expected"])]
    if misses:
        print("\nUnder-classified (fix before launch):")
        for r in misses:
            print(f"  {r['id']}  {r['title']}: expected {r['expected']}, got {r['predicted']}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rules-only", action="store_true")
    args = ap.parse_args()
    result = run(use_llm=not args.rules_only)
    out = HERE / "results"
    out.mkdir(exist_ok=True)
    path = out / f"{datetime.now():%Y%m%d-%H%M%S}-{result['mode']}.json"
    path.write_text(json.dumps(result, indent=2))
    print_report(result)
    print(f"\nFull results: {path}")


if __name__ == "__main__":
    main()
