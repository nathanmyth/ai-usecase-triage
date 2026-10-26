# Risk Register

L = likelihood, I = impact (High / Medium / Low). Reviewed weekly.

| ID | Risk | L | I | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|
| R-01 | **Under-classification:** a high-risk use case is tiered minimal and launches without controls | M | H | Rules floor (ADR-001); under-classification is the P0 eval metric; human reviewer confirms every high/prohibited tier | TPM | 🟡 Open |
| R-02 | **Gaming the form:** submitters word proposals to avoid triggers | M | H | LLM layer reads intent, not just keywords; random audit of 10% of minimal-tier approvals | Governance | 🟡 Open |
| R-03 | **Policy drift:** regulation changes and `policy.json` lags | M | M | Legal reviews policy quarterly; policy version stamped on every triage record | Legal | 🟡 Open |
| R-04 | **Over-classification fatigue:** too many false "high risk" flags, so teams lose trust | M | M | Track over-classification rate; tune triggers via reviewed PRs | TPM | 🟡 Open |
| R-05 | **Rules overfit to eval set:** triggers written with the eval cases in view | H | M | Hold out new real intakes from pilot as a second eval set; report both | TPM | 🟡 Open |
| R-06 | **Treated as legal advice:** teams skip Legal because "the tool said limited" | L | H | Disclaimer in UI and outputs; tool recommends, humans decide | Legal | 🟢 Monitoring |
| R-07 | **Sensitive data in intake text** sent to an external LLM | M | M | Guidance on intake form; vendor contract with no-training terms; rules-only mode available | Security | 🟡 Open |
| R-08 | **Low adoption:** teams keep using email | M | H | Make the register the only route to production approval; exec sponsor | Exec sponsor | 🟡 Open |
