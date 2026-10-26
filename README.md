# 🛡️ AI Use-Case Intake & Risk Triage

**Every business unit wants to ship AI. This tool decides, in minutes instead of weeks, which proposals are risky, what controls they need, and who has to sign off, and keeps one register of every AI system the company runs.**

> 📌 **Portfolio note:** This is an AI governance program, built and run end to end: policy design, a hybrid rules + LLM classifier with an asymmetric safety metric, evaluation-driven launch gates, and a portfolio register for executives and auditors. The `docs/` folder is as important as the code.

**🔗 Try it in your browser:** [nathanmyth.github.io/ai-usecase-triage/demo](https://nathanmyth.github.io/ai-usecase-triage/demo/) (rules engine, no setup needed)

---

## The problem

AI proposals arrive by email and spreadsheet. Governance reviews each one by hand, which takes weeks, produces inconsistent answers, and leaves leadership unable to say how many AI systems the company runs or how many are high risk. Meanwhile, a hiring model can slip into production without bias testing because nobody flagged it.

## What it does

1. A team describes a proposed AI use case in plain English.
2. The system assigns a **risk tier** modeled on the EU AI Act: **Prohibited · High · Limited · Minimal**.
3. It adds **overlays** for cross-cutting risk: personal data, third-party vendors, external users.
4. It outputs the **required controls, approvers, and review SLA**, with the reasons behind every decision.
5. Every triage goes into the **portfolio register**.

A human reviewer always makes the final decision.

## The key design choice: never under-classify

Calling a spreadsheet macro "high risk" wastes a review. Calling a hiring model "minimal risk" can harm people and break the law. So the metrics are **asymmetric**:

| Metric | Target | Why |
|---|---|---|
| **Under-classification** | **0%** | P0: the failure that causes harm |
| Tier accuracy | ≥ 85% | Consistency for reviewers |
| Over-classification | ≤ 20% | Costs reviewer time, not safety |

The architecture enforces this: **final tier = max(rules tier, LLM tier)**. The rules engine is a deterministic floor; the LLM can raise a tier but never lower it ([ADR-001](docs/decisions/ADR-001-hybrid-rules-llm.md)).

## Results

Evaluated on 24 reviewer-labeled use cases, split into ones worded like the policy (*core*) and ones in everyday language (*paraphrase*):

| Mode | Slice | Accuracy | Under-classified | Over-classified |
|---|---|---|---|---|
| Rules only | Core (16) | 100% | 0% | 0% |
| Rules only | Paraphrase (8) | 12% | **88%** | 0% |
| Hybrid | Core | _TBD_ | _TBD_ | _TBD_ |
| Hybrid | Paraphrase | _TBD_ | _TBD_ | _TBD_ |

**What this shows:** keyword rules are precise but brittle. "Pick which applicants move to interviews" never says "resume" or "hiring", so rules alone call it minimal risk. That finding drove two decisions: the LLM layer, and a **fail-safe** where rules-only "minimal" results go to a human instead of being auto-approved. I deliberately did **not** tune the rules to the paraphrase cases, since that would overfit the eval and hide the gap ([risk R-05](docs/04-risk-register.md)).

_Run `python -m eval.run_eval` with an API key to fill in the hybrid rows._

## Program artifacts

| Doc | What it shows |
|---|---|
| [PRD](docs/01-prd.md) | Problem, personas, asymmetric success metrics, scope |
| [Architecture](docs/02-architecture.md) | Hybrid flow, policy-as-config, graceful degradation |
| [ADR-001](docs/decisions/ADR-001-hybrid-rules-llm.md) | Rules + LLM hybrid, with eval findings |
| [ADR-002](docs/decisions/ADR-002-tier-taxonomy.md) | Why EU AI Act-style tiers plus overlays |
| [Milestones](docs/03-milestones.md) | Phased plan through a two-business-unit pilot |
| [Risk register](docs/04-risk-register.md) | Under-classification, gaming the form, policy drift… |
| [Launch checklist](docs/05-launch-checklist.md) | Go/no-go gates for the pilot |
| [Retrospective](docs/06-retro.md) | Template for pilot learnings |
| [Policy](policy/policy.json) | Tiers, triggers, controls, approvers: editable by governance without code changes |

## Quick start

```bash
git clone https://github.com/nathanmyth/ai-usecase-triage.git
cd ai-usecase-triage
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Works with no API key (rules only):
python -m src.cli "Resume screener" "Rank job applicants by resume fit" --rules-only
python -m eval.run_eval --rules-only
pytest

# Full hybrid mode:
cp .env.example .env       # add ANTHROPIC_API_KEY
python -m eval.run_eval
streamlit run app.py       # intake form + portfolio register
```

## Project structure

```
├── policy/policy.json       # the governance policy (tiers, triggers, controls, approvers)
├── src/
│   ├── rules.py             # deterministic rules engine
│   ├── llm_classifier.py    # LLM tiering against the same policy
│   ├── triage.py            # combine: max(rules, LLM) + overlays + fail-safe
│   ├── register.py          # append-only portfolio register
│   └── cli.py
├── app.py                   # Streamlit UI
├── demo/index.html          # browser demo (GitHub Pages)
├── eval/                    # 24 labeled cases + harness with confusion matrix
├── tests/                   # runs without an API key
├── docs/                    # program artifacts
└── .github/                 # CI + intake issue form
```

## How this project is managed

GitHub **Milestones** M1–M4 follow [the plan](docs/03-milestones.md). New use cases can be proposed with the **AI use-case intake** issue form, and triage misses are logged with the **Triage miss** template, then added to the eval set as regression cases.

## Disclaimer

The policy is a simplified model of the EU AI Act risk tiers, built for illustration. It is not legal advice.

## About me

_TODO: one or two lines, e.g. "AI Technical Program Manager focused on responsible AI governance and taking LLM products to production." + LinkedIn link._
