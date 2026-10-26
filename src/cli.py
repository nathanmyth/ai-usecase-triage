"""Triage a use case from the command line.

    python -m src.cli "Resume screener" "Rank job applicants by fit for open roles"
    python -m src.cli --rules-only "Title" "Description"
"""
import argparse

from src import register
from src.triage import triage


def main() -> None:
    p = argparse.ArgumentParser(description="Triage a proposed AI use case.")
    p.add_argument("title")
    p.add_argument("description")
    p.add_argument("--rules-only", action="store_true", help="Skip the LLM layer.")
    p.add_argument("--save", action="store_true", help="Add the result to the register.")
    a = p.parse_args()

    r = triage(a.title, a.description, use_llm=not a.rules_only)
    print(f"\n{r.tier_label.upper()}  ·  {r.decision}  ·  review SLA {r.review_sla_days} days  ·  mode: {r.mode}")
    print("\nWhy:")
    for x in r.reasons:
        print(f"  - {x}")
    print("\nRequired controls:")
    for x in r.controls:
        print(f"  [ ] {x}")
    print(f"\nApprovers: {', '.join(r.approvers)}")
    if a.save:
        register.add(r)
        print("\nSaved to register.")


if __name__ == "__main__":
    main()
