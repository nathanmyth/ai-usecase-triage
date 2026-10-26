# ADR-001: Hybrid triage with rules as a safety floor

**Status:** Accepted · **Date:** _YYYY-MM-DD_ · **Decider:** _Your name_

## Context
Triage must be fast and consistent, and above all must never under-classify a high-risk use case (PRD R1).

## Options
| Option | Pros | Cons |
|---|---|---|
| A. Rules only (keyword triggers) | Deterministic, explainable, free, auditable | Misses paraphrases ("rank applicants" vs. "resume screening") |
| B. LLM only | Understands paraphrase and context | Non-deterministic; can under-classify; hard to audit |
| **C. Hybrid: final tier = max(rules, LLM)** | Rules guarantee a floor; LLM catches what rules miss | Over-classification rises; two systems to maintain |

## Decision
**Option C.** The LLM may raise the tier, but never lower it below the rules result.

## Consequences
- Under-classification can only happen if *both* systems miss. The eval measures each one separately so we can see which layer is doing the work.
- Over-classification will be higher than either system alone. We accept that: it costs reviewer time, not safety. Tracked against the ≤ 20% target.
## Findings from the rules-only eval (24 labeled cases)

| Slice | n | Accuracy | Under-classified | Over-classified |
|---|---|---|---|---|
| Core (policy wording) | 16 | 100% | 0% | 0% |
| Paraphrase (everyday wording) | 8 | 12% | 88% | 0% |
| **Overall** | 24 | 71% | 29% | 0% |

Rules are precise but brittle. "Pick which applicants move to interviews" never says "resume" or "hiring", so it was tiered minimal. This confirms the hybrid decision.

**Follow-up decisions:**
1. **Don't tune triggers to the paraphrase cases.** That would overfit to the eval set (risk R-05) and hide the real gap.
2. **Fail-safe in rules-only mode:** a "minimal" result is routed to a human reviewer instead of auto-approved.
3. **Launch gate:** the hybrid must reach 0% under-classification on *both* slices before pilot.

- Rule triggers that cause repeated over-classification get tuned in `policy.json`, through a reviewed pull request.
