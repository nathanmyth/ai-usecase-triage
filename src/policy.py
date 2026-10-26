"""Load the governance policy (policy/policy.json)."""
import json
from functools import lru_cache
from pathlib import Path

POLICY_PATH = Path(__file__).resolve().parent.parent / "policy" / "policy.json"


@lru_cache(maxsize=1)
def load_policy(path: Path = POLICY_PATH) -> dict:
    policy = json.loads(Path(path).read_text(encoding="utf-8"))
    policy["tiers"].sort(key=lambda t: t["rank"], reverse=True)
    return policy


def tier_by_id(tier_id: str) -> dict:
    for tier in load_policy()["tiers"]:
        if tier["id"] == tier_id:
            return tier
    raise KeyError(f"Unknown tier: {tier_id}")


def rank(tier_id: str) -> int:
    return tier_by_id(tier_id)["rank"]
