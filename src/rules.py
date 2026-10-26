"""Deterministic rules engine: match policy trigger phrases in the intake text."""
import re
from dataclasses import dataclass, field

from src.policy import load_policy


@dataclass
class RulesResult:
    tier: str
    matches: list[dict] = field(default_factory=list)   # [{"tier", "category", "trigger"}]
    overlays: list[dict] = field(default_factory=list)  # [{"id", "label", "trigger"}]


def _find(phrase: str, text: str) -> bool:
    # Match at a word start; triggers like "recruit" or "diagnos" also match longer words.
    return re.search(r"(?<!\w)" + re.escape(phrase.lower()), text) is not None


def classify(text: str) -> RulesResult:
    text = text.lower()
    policy = load_policy()
    matches = [
        {"tier": tier["id"], "category": cat["name"], "trigger": trig}
        for tier in policy["tiers"]
        for cat in tier["categories"]
        for trig in cat["triggers"]
        if _find(trig, text)
    ]
    # Tiers are sorted highest rank first, so the first match is the strictest.
    tier = matches[0]["tier"] if matches else "minimal"

    overlays = []
    for ov in policy["overlays"]:
        hit = next((t for t in ov["triggers"] if _find(t, text)), None)
        if hit:
            overlays.append({"id": ov["id"], "label": ov["label"], "trigger": hit})

    return RulesResult(tier=tier, matches=matches, overlays=overlays)
