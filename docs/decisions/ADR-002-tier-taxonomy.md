# ADR-002: Four risk tiers modeled on the EU AI Act

**Status:** Accepted · **Date:** _YYYY-MM-DD_ · **Decider:** _Your name_

## Context
We need a tier scheme that business teams understand, that maps to regulation, and that drives concrete controls.

## Options
| Option | Pros | Cons |
|---|---|---|
| A. Internal Low / Medium / High | Simple | No link to regulation; "Medium" becomes a dumping ground |
| **B. EU AI Act-style: Prohibited / High / Limited / Minimal** | Maps to the most detailed AI regulation; each tier has clear obligations | EU-specific language; needs legal review for other regions |
| C. NIST AI RMF profiles only | US-aligned, flexible | A framework, not a tiering scheme; doesn't say what's required per tier |

## Decision
**Option B** for tiering, with **overlays** (personal data, third-party vendor, external users) that add controls on top of the tier. NIST AI RMF's Govern / Map / Measure / Manage functions organize the controls themselves.

## Consequences
- Policy is a simplification of the regulation. The disclaimer in `policy.json` and the README says so; Legal owns the mapping.
- Overlays keep the tier list short while still catching privacy and vendor risk, which cut across every tier.
