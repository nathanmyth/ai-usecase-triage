"""Combine rules and LLM into one triage result (ADR-001: final tier = max(rules, LLM))."""
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone

from src import llm_classifier, rules
from src.policy import load_policy, rank, tier_by_id


@dataclass
class Triage:
    title: str
    description: str
    tier: str
    tier_label: str
    decision: str
    reasons: list[str]
    controls: list[str]
    approvers: list[str]
    overlays: list[str]
    review_sla_days: int
    rules_tier: str
    llm_tier: str | None = None
    mode: str = "rules-only"
    policy_version: str = ""
    triaged_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds"))

    def to_dict(self) -> dict:
        return asdict(self)


def _unique(items):
    return list(dict.fromkeys(items))


def triage(title: str, description: str, use_llm: bool = True) -> Triage:
    text = f"{title}\n{description}"
    policy = load_policy()
    r = rules.classify(text)

    reasons = [f'Rules: "{m["trigger"]}" → {m["category"]} ({tier_by_id(m["tier"])["label"]})' for m in r.matches]
    llm_tier, mode = None, "rules-only"
    if use_llm and llm_classifier.available():
        res = llm_classifier.classify(text)
        llm_tier, mode = res.tier, "hybrid"
        reasons += [f"LLM: {x}" for x in res.reasons]

    final = r.tier if llm_tier is None or rank(r.tier) >= rank(llm_tier) else llm_tier
    tier = tier_by_id(final)
    if not reasons:
        reasons = ["No higher-risk triggers found"]

    controls, approvers = list(tier["controls"]), list(tier["approvers"])
    for ov in r.overlays:
        spec = next(o for o in policy["overlays"] if o["id"] == ov["id"])
        controls += spec["controls"]
        approvers += spec["approvers"]
        reasons.append(f'Overlay: "{ov["trigger"]}" → {ov["label"]}')

    decision = tier["decision"]
    if mode == "rules-only" and final == "minimal":
        # Rules miss paraphrased risks (see ADR-001 findings), so don't auto-approve on rules alone.
        decision = "Human review required"
        reasons.append("Fail-safe: rules-only mode can miss paraphrased risks, so a reviewer must confirm")

    return Triage(
        title=title, description=description, tier=final, tier_label=tier["label"],
        decision=decision, reasons=reasons, controls=_unique(controls),
        approvers=_unique(approvers), overlays=[o["label"] for o in r.overlays],
        review_sla_days=tier["review_sla_days"], rules_tier=r.tier, llm_tier=llm_tier,
        mode=mode, policy_version=policy["version"],
    )
