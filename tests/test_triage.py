"""Tests run in rules-only mode, with no API key."""
import pytest

from eval.run_eval import run
from src.policy import load_policy
from src.triage import triage


@pytest.mark.parametrize("title,desc,tier", [
    ("Resume screener", "Rank candidates by resume fit", "high"),
    ("Support bot", "A chatbot that answers customer questions", "limited"),
    ("Mood monitor", "Emotion recognition on employee webcams", "prohibited"),
    ("Forecasting", "Forecast inventory demand per warehouse", "minimal"),
])
def test_rules_tiers(title, desc, tier):
    assert triage(title, desc, use_llm=False).tier == tier


def test_strictest_tier_wins():
    r = triage("HR bot", "A chatbot that screens job applicant resumes", use_llm=False)
    assert r.tier == "high"


def test_overlays_add_controls_and_approvers():
    r = triage("Notes", "Summarize employee data from a third-party vendor tool", use_llm=False)
    assert "Personal data" in r.overlays and "Third-party model or vendor" in r.overlays
    assert "Data Protection Officer" in r.approvers
    assert any("DPIA" in c for c in r.controls)


def test_rules_only_minimal_is_not_auto_approved():
    r = triage("Forecasting", "Forecast inventory demand", use_llm=False)
    assert r.decision == "Human review required"


def test_policy_tiers_are_complete():
    ids = {t["id"] for t in load_policy()["tiers"]}
    assert ids == {"prohibited", "high", "limited", "minimal"}


def test_core_eval_floor():
    """Regression guard: rules must stay perfect on policy-worded cases."""
    core = run(use_llm=False)["by_split"]["core"]
    assert core["under_classification"] == 0
    assert core["accuracy"] == 1.0
