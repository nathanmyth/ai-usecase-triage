# Architecture

## Flow

```
Intake (form / CLI)
      │  description + fields
      ▼
┌──────────────────┐        ┌──────────────────┐
│  Rules engine    │        │  LLM classifier  │  (optional; skipped with no API key)
│  policy triggers │        │  tier + reasons  │
└────────┬─────────┘        └────────┬─────────┘
         │ floor tier                │ suggested tier
         └──────────┬────────────────┘
                    ▼
          Combine: final = max(rules, LLM)     ← "never under-classify" (ADR-001)
                    │
                    ▼
     Overlays (personal data, vendor, external users)
                    │
                    ▼
   Triage result: tier, reasons, controls, approvers, SLA
                    │
                    ▼
        Register (data/register.jsonl) → portfolio view
```

## Components

| Component | File | Notes |
|---|---|---|
| Policy | `policy/policy.json` | Tiers, triggers, controls, approvers, overlays. Owned by governance, versioned in git |
| Rules engine | `src/rules.py` | Phrase matching against policy triggers; deterministic and explainable |
| LLM classifier | `src/llm_classifier.py` | Reads the same policy; returns JSON with tier and reasons |
| Combiner | `src/triage.py` | Takes the stricter tier; merges reasons, controls, approvers |
| Register | `src/register.py` | Append-only JSONL log of triage results |
| UI | `app.py` | Streamlit: intake form + portfolio register |
| Browser demo | `demo/index.html` | Rules engine in JavaScript, runs on GitHub Pages |
| Eval | `eval/run_eval.py` | Accuracy, under- and over-classification, confusion matrix |

## Design principles

1. **Policy as config.** Governance edits `policy.json`; no code change needed to add a trigger or control.
2. **Asymmetric safety.** The LLM can raise a tier, never lower it below the rules floor.
3. **Graceful degradation.** No API key or model outage → rules-only triage still works.
4. **Explainability.** Every tier lists the exact trigger phrases or LLM reasons behind it.
