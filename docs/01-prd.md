# PRD: AI Use-Case Intake & Risk Triage

| | |
|---|---|
| **Owner** | _Your name_ (AI TPM) |
| **Status** | Draft → In review → **Approved** → Shipped |
| **Last updated** | _YYYY-MM-DD_ |

## 1. Problem

Every business unit wants to ship AI features. Today, proposals arrive by email and spreadsheet, and the AI governance team reviews each one by hand.

- **Slow:** median 6 weeks from proposal to decision, so teams wait or route around governance.
- **Inconsistent:** two reviewers can tier the same use case differently.
- **Invisible:** leadership can't answer "how many AI systems do we run, and how many are high risk?", which regulators and auditors now ask.
- **Risky:** a high-risk system (e.g., resume screening) can launch without bias testing because nobody flagged it.

_Numbers above are illustrative; replace with real ones if you have them._

## 2. Users

| Persona | Need |
|---|---|
| **Business team (submitter)** | Know quickly what's required to launch, and who approves |
| **AI governance reviewer** | Consistent first-pass triage; spend time on hard cases, not easy ones |
| **Legal / DPO / Security** | Get pulled in only when their review is actually required |
| **Executives and auditors** | One register of all AI use cases, by risk tier and status |

## 3. Goals & success metrics

| Type | Metric | Target |
|---|---|---|
| **North star** | Median time from intake to decision | 6 weeks → 2 weeks |
| **Safety (P0)** | Under-classification rate (system tiers lower than reviewer) | **0%** on eval set |
| Quality | Tier accuracy vs. reviewer labels | ≥ 85% |
| Quality | Over-classification rate | ≤ 20% (costs reviewer time, not safety) |
| Coverage | AI use cases registered in inventory | 100% of new launches |
| Efficiency | Minimal-risk cases auto-approved without board review | ≥ 80% |

**Why under-classification is the P0 metric:** calling a minimal-risk tool "high risk" wastes a review cycle. Calling a hiring model "minimal risk" can cause real harm and regulatory exposure. The metrics are deliberately asymmetric.

## 4. Scope

**In scope (v1)**
- Intake of a plain-English use-case description plus a few structured fields
- Risk tier (Prohibited / High / Limited / Minimal), with reasons
- Required controls and approvers, including overlays (personal data, third-party vendor, external users)
- Portfolio register of all submissions

**Non-goals (v1)**
- Making the final approval decision (a human always decides)
- Legal advice or full regulatory compliance mapping
- Ongoing monitoring of deployed models
- Workflow integrations (Jira, ServiceNow); v2

## 5. Requirements

| ID | Requirement | Priority |
|---|---|---|
| R1 | Never assign a tier lower than the rules engine's tier | P0 |
| R2 | Every tier comes with human-readable reasons | P0 |
| R3 | Policy (tiers, triggers, controls, approvers) lives in config, editable without code changes | P0 |
| R4 | Works without an LLM (rules only) if the model is unavailable | P0 |
| R5 | Every triage is recorded in the register with timestamp and policy version | P1 |
| R6 | Reviewer can override the tier, with a reason | P1 |

## 6. Dependencies

- AI Governance Board agrees the tier definitions and controls (owns `policy/policy.json`)
- Legal reviews the policy mapping to the EU AI Act and other applicable rules
- LLM API approval from Security and Procurement

## 7. Open questions

- Should limited-risk cases also skip the board, like minimal-risk ones?
- How often do we re-triage live systems when the policy version changes?
- Who owns the register long-term: governance team or enterprise architecture?
