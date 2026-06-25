# Agent Specifications

Eleven agents orchestrated by **Azure AI Foundry Agent Service** (Semantic Kernel / Magentic planner),
with a human-in-the-loop gate on every enforcement action. Machine-readable definitions live in
`agent-manifest.json`; this file gives each agent's contract and a starter system prompt.

> Convention: each agent returns a typed result and a `riskDelta` (Scenario 1) or a structured
> finding (Scenario 2). The orchestrator accumulates risk and composes the final decision.

---

## Scenario 1 — Prevention pipeline (intake)

### Identity Proofing Agent
- **Goal:** require a verifiable credential before anything else.
- **Tool:** Entra Verified ID request/verify.
- **Returns:** `{ credentialVerified: bool, issuer: string|null, riskDelta }`
- **System prompt (starter):**
  > "You gate benefit intake. Request a verifiable credential via Entra Verified ID. If the applicant cannot present a credential from a trusted issuer, mark `credentialVerified=false` and raise risk. Never accept a self-asserted identity as verified."

### Document Parsing Agent
- **Goal:** turn document images into structured fields.
- **Tools:** Document Intelligence (`prebuilt-idDocument`, `prebuilt-layout`), Content Understanding for mixed media.
- **Returns:** `{ docType, fields:{...}, image, confidence }`

### Validation Agent
- **Goal:** detect tampering, forgery, expiry; reconcile vs applicant input.
- **Tools:** Azure AI Vision; custom Error-Level-Analysis + EXIF/metadata inspector.
- **Returns:** `{ tampered: bool, regions:[...], metadataEdited: date|null, expired: bool, findings:[...], riskDelta }`
- **Fairness rule:** a single low-confidence blur is **not** tampering — emit `review`, not `block`.

### Face Verification Agent
- **Goal:** liveness + deepfake detection; match to ID portrait.
- **Tools:** Azure Face Liveness SDK; Content Safety.
- **Returns:** `{ live: bool, deepfakeScore: float, faceMatch: bool, findings:[...], riskDelta }`

### Consistency Checker
- **Goal:** cross-match employer/income/residency against authoritative data.
- **Tools:** Fabric lakehouse query; external verification connectors (tax, employment, business registry).
- **Returns:** `{ employerRegistered: bool, incomeMatch: bool, findings:[...], riskDelta }`

### Eligibility Decision Agent
- **Goal:** compose the final, explainable decision.
- **Tools:** Azure OpenAI (reasoning), Azure ML risk endpoint, RAI explainer, Purview audit writer.
- **Decision policy:**
  - `risk >= 70` → **block** (pre-submission)
  - `35 <= risk < 70` with only low-weight signals → **human review** / auto-reconcile
  - `risk < 35` → **auto-approve**
- **Returns:** `{ decision: "approve"|"review"|"block", riskScore, contributions:{...}, explanation, auditRecord }`

---

## Scenario 2 — Detection pipeline (post-submission)

### Cyber Signals Agent
- **Goal:** find coordinated/automated bursts.
- **Tools:** Sentinel KQL over submission telemetry; Defender Threat Intel; Azure ML anomaly endpoint.
- **Detects:** same source IP, device-fingerprint reuse, sub-human form cadence, tight inter-arrival window, hosting/VPN ASN.
- **Returns:** `{ clusterId, signals:{...}, anomalyScore }`

### Prioritization Agent
- **Goal:** rank the officer queue by fraud likelihood.
- **Returns:** `{ queue:[{caseId, risk, reason, agent}] }`

### Graph Relationship Explorer
- **Goal:** build/traverse the relationship network.
- **Tool:** Cosmos DB Gremlin.
- **Returns:** `{ nodes:[...], edges:[...], sharedEntities:[...] }`

### Document Generator
- **Goal:** compile the case file.
- **Tools:** M365 Copilot / Azure OpenAI; Word generator (the repo's `.docx` builder is a starting point).
- **Returns:** `{ caseFileUri, sections:[...] }`

### Notification Agent
- **Goal:** governed, minimized partner-agency alerts.
- **Tools:** Microsoft Graph mail; Purview DLP for field minimization.
- **Returns:** `{ dispatched:[{agency, status, fieldsShared}], auditRecord }`
