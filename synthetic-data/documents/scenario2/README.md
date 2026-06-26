# Scenario-2 control documents — the genuine "clean applicant"

The legitimate counterpart to the Scenario-1 fraud set. Applicant **Elena Marinescu (A-88204)** — the
record your datasets mark as verified and auto-approved (risk 12). Use these to **show the system letting
an honest citizen through without friction**, and as **negative (genuine) samples** to confirm the agents
don't false-positive.

| File | Represents | Ground truth | Consumed by | Azure service |
|------|-----------|--------------|-------------|---------------|
| `passport-clean-elena.png` | Valid passport (VERIFIED badge) | genuine | Document Parsing / Validation | Document Intelligence · AI Vision |
| `payslip-contoso.png` | Registered-employer pay stub, income matches tax | genuine | Consistency Checker | Doc Intelligence + Fabric |
| `utility-bill-recent.png` | Recent, unaltered proof of address | genuine | Validation | Document Intelligence |
| `video-consult-frame-clean.png` | Passed liveness, face matches ID | genuine | Face Verification | Azure Face |
| `passport-clean-elena.metadata.json` | Ground-truth labels (no tampering) | — | (test oracle) | — |
| `video-session-clean.metadata.json` | Liveness passed, deepfake score 0.03 | — | (test oracle) | — |
| `application-summary.json` | Full clean application + auto-approve decision (risk 12) | — | — | — |

## The contrast (why this matters)
| | Fraud ring (Scenario 1) | Clean applicant (Scenario 2) |
|---|---|---|
| Passport | face-swap, edited metadata | genuine, VERIFIED |
| Employer | Northwind — **unregistered** | Contoso — **registered, VAT valid** |
| Income | inconsistent with tax | **matches** tax records |
| Address proof | 11 months old, altered | **recent, unaltered** |
| Video | **deepfake**, liveness failed | **live**, face matches ID |
| Outcome | **blocked** (risk 95) | **auto-approved** (risk 12) |

This pairing demonstrates the fairness safeguard: the same agents that stop organized fraud onboard a
genuine citizen instantly. All artifacts are synthetic (fictional Republic of Utopia, documentation IP ranges).
Regenerate with `python synthetic-data/generators/build_documents_scenario2.py`.
