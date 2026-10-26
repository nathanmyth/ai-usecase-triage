"""LLM classifier: reads the same policy and returns a tier with reasons."""
import json
import os
import re
from dataclasses import dataclass

from src.policy import load_policy

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

MODEL = os.getenv("LLM_MODEL", "claude-haiku-5-5")


@dataclass
class LLMResult:
    tier: str
    reasons: list[str]


def available() -> bool:
    return bool(os.getenv("ANTHROPIC_API_KEY"))


def _policy_brief() -> str:
    lines = []
    for tier in load_policy()["tiers"]:
        cats = "; ".join(c["name"] for c in tier["categories"]) or "everything else"
        lines.append(f'- "{tier["id"]}" ({tier["label"]}): {tier["summary"]} Categories: {cats}.')
    return "\n".join(lines)


SYSTEM = """You are an AI governance analyst. Classify a proposed AI use case into exactly one risk tier.

Tiers (strictest first):
{tiers}

Rules:
- Judge what the system actually does and who it affects, not the wording used.
- If a case could fit two tiers, choose the stricter one.
- Reply with JSON only: {{"tier": "<tier id>", "reasons": ["<short reason>", "..."]}}"""


def classify(text: str) -> LLMResult:
    import anthropic

    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=MODEL,
        max_tokens=300,
        system=SYSTEM.format(tiers=_policy_brief()),
        messages=[{"role": "user", "content": f"Proposed AI use case:\n{text}"}],
    )
    raw = "".join(b.text for b in resp.content if b.type == "text")
    match = re.search(r"\{.*\}", raw, re.S)
    data = json.loads(match.group(0)) if match else {}
    valid = {t["id"] for t in load_policy()["tiers"]}
    tier = data.get("tier") if data.get("tier") in valid else "high"  # unparseable → fail safe
    return LLMResult(tier=tier, reasons=list(data.get("reasons", []))[:4])
