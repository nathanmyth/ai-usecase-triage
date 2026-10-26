# Pilot Launch Checklist (Go / No-Go)

## Quality — P0
- [ ] Under-classification = 0% on eval set (rules only and hybrid)
- [ ] Tier accuracy ≥ 85% (hybrid)
- [ ] Over-classification ≤ 20%
- [ ] Every result shows reasons

## Policy & compliance — P0
- [ ] `policy.json` v1 signed off by AI Governance Board
- [ ] Legal review of tier mapping and disclaimer wording
- [ ] Security review of LLM data flow (no sensitive intake text retained by vendor)

## Operations — P1
- [ ] Reviewer override flow tested
- [ ] Register exported weekly to governance dashboard
- [ ] Rules-only fallback tested with LLM disabled
- [ ] Owner named for policy updates

## Pilot — P1
- [ ] Two pilot business units briefed
- [ ] Feedback channel for submitters and reviewers
- [ ] Success review scheduled 4 weeks after pilot start

## Decision
| Date | Decision | Approvers | Notes |
|---|---|---|---|
| _YYYY-MM-DD_ | _GO / NO-GO_ | _TPM, Governance lead, Legal, Security_ | |
