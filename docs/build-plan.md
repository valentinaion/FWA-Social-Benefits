# Build Plan — from storyboard to code-based demo

A phased path. **Phase 1 gets you a runnable demo with zero Azure dependencies** (fixtures only).
Later phases swap fixtures for live Azure services, one agent at a time.

## Phase 0 — Storyboard ✅ (done)
- Interactive prototype (`web/index.html`) — clickable narrative, both scenarios, downloadable case file.
- Demo script (`docs/demo-script.md`) and this reference architecture.

## Phase 1 — Runnable demo skeleton (1–2 days)
**Goal:** the prototype talks to a real API serving fixtures.
- [ ] Stand up `app/` FastAPI backend (`DEMO_MODE=true`) — already scaffolded.
- [ ] Serve `web/index.html` from the API; replace inline fixtures with `fetch()` to the API.
- [ ] Endpoints return `data/scenario1-applicant.json` and `data/scenario2-cluster.json`.
- [ ] Containerize (`Dockerfile`) and run on Azure Container Apps.
- **Exit:** the full demo runs end-to-end against the API, no Azure keys needed.

## Phase 2 — Agent orchestration (3–5 days)
**Goal:** real multi-agent flow, still with mocked tool outputs.
- [ ] Deploy **Multi-Agent Custom Automation Engine** accelerator (Foundry + Semantic Kernel).
- [ ] Define the 11 agents from `agents/agent-manifest.json` as Foundry agents.
- [ ] Implement the Scenario-1 orchestration (intake → 5 agents → eligibility decision).
- [ ] Implement the Scenario-2 detection pipeline (cyber signals → prioritization → graph).
- **Exit:** decisions are produced by the agent graph, not hard-coded.

## Phase 3 — Live document & identity AI (1–2 weeks)
- [ ] Document Parsing → **Document Intelligence** (real OCR on sample docs).
- [ ] Validation → **Azure AI Vision** tamper/ELA + EXIF on the sample passport.
- [ ] Face Verification → **Azure Face** liveness (use the liveness SDK + a sample deepfake clip).
- [ ] Identity Proofing → **Entra Verified ID** issue/verify flow.
- [ ] Leverage **Digital Identity Analyzer** + **Document Knowledge Mining** accelerators.
- **Exit:** Scenario 1 runs on real AI for the document & identity checks.

## Phase 4 — Data estate, graph & cyber signals (1–2 weeks)
- [ ] **Fabric / OneLake** medallion; load synthetic tax/employment/registry tables; wire Consistency Checker cross-match.
- [ ] **Cosmos DB (Gremlin)** graph; load the cluster; power the Graph Explorer.
- [ ] **Sentinel + Defender**: ingest submission telemetry; analytics rule for same-IP burst; **Azure ML** anomaly endpoint.
- **Exit:** Scenario 2 runs on real graph + cyber-signal detection.

## Phase 5 — Action, governance & productivity (1 week)
- [ ] Freeze → payments/ERP stub; Escalate → **Dynamics 365** case; Notify → **Notification Agent** + Graph.
- [ ] Case file → **M365 Copilot** / Document Generator (real Word generation; the `.docx` generator in this repo is a starting point).
- [ ] **Purview** audit + lineage; **Power BI** RAI dashboard; Content Safety on generative output.
- **Exit:** full human-in-the-loop action set with audit + explainability.

## Phase 6 — Hardening & polish (ongoing)
- [ ] Apply **Deploy Your AI App in Production** (private endpoints, Zero-Trust, WAF).
- [ ] Foundry evaluations for the decision agent (accuracy, fairness, groundedness).
- [ ] Load/perf test the burst-detection path.

## Suggested team & stack
- **Frontend:** React + Vite (or keep the static prototype for early phases).
- **Backend/orchestration:** Python (FastAPI) or .NET; Semantic Kernel on Foundry.
- **Data:** Fabric, Cosmos DB (Gremlin), Redis.
- **IaC:** Bicep (see `infra/`).
- Ideal as a **Public Sector AI Hackathon** project — see `aka.ms/PrepareforPSAIHackathon`.

## Definition of done (demo)
A presenter can run both scenarios live; Scenario 1 blocks on real document+face AI; Scenario 2 detects
the burst via real graph+anomaly; all four officer actions execute with a downloadable case file and a
Purview audit trail; 18/18 capabilities demonstrably exercised.
