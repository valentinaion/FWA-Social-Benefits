# Reference Architecture — Benefits Integrity Cloud (FWA Detection & Prevention)
### Code-build edition · grounded in *RefArch PH&SS — Enable detection and prevention for Fraud, Waste & Abuse*

This document is the technical blueprint for turning the interactive storyboard (`web/index.html`)
into a runnable, code-based demo. It maps every on-screen capability to a concrete Azure service,
SDK, and (where available) a Microsoft solution accelerator.

---

## 1. Logical architecture

```mermaid
flowchart TB
  subgraph CH["Channels"]
    PORTAL["Citizen Portal\n(React / web)"]
    OFFICER["Officer Command Center\n(React / web)"]
    M365["M365 Copilot\nOutlook · Teams"]
  end

  subgraph ID["Identity & Access — Microsoft Entra"]
    EXTID["Entra External ID"]
    VID["Entra Verified ID\n(verifiable credentials)"]
    RBAC["RBAC · Zero Trust"]
  end

  subgraph ORCH["Orchestration — Azure AI Foundry Agent Service"]
    SK["Semantic Kernel / Magentic planner"]
    direction LR
    A1["Identity Proofing Agent"]
    A2["Document Parsing Agent"]
    A3["Validation Agent"]
    A4["Face Verification Agent"]
    A5["Consistency Checker"]
    A6["Eligibility Decision Agent"]
    A7["Cyber Signals Agent"]
    A8["Prioritization Agent"]
    A9["Graph Relationship Explorer"]
    A10["Document Generator"]
    A11["Notification Agent"]
  end

  subgraph AI["Azure AI Services"]
    DI["Document Intelligence\n(OCR / extraction)"]
    VISION["Azure AI Vision\n(tamper / ELA)"]
    FACE["Azure Face\n(liveness / deepfake)"]
    CU["Content Understanding\n(multimodal)"]
    SAFETY["Content Safety"]
    AOAI["Azure OpenAI\n(GPT-4o reasoning/NLP)"]
    SEARCH["Azure AI Search\n(policy RAG)"]
    AML["Azure ML\n(risk + anomaly)"]
  end

  subgraph DATA["Unified Data Estate"]
    FABRIC["Microsoft Fabric · OneLake\nBronze→Silver→Gold"]
    COSMOS["Azure Cosmos DB\n(Gremlin graph)"]
    REDIS["Azure Cache for Redis"]
  end

  subgraph EXT["External Verification (connectors)"]
    TAX["Tax records"]
    EMP["Employment / business registry"]
    ADDR["Address / utility"]
  end

  subgraph SEC["Cyber & Governance"]
    SENTINEL["Microsoft Sentinel\nCyber Signals"]
    DEFENDER["Microsoft Defender\nThreat Intel"]
    PURVIEW["Microsoft Purview\naudit · lineage · DLP"]
    RAI["Responsible AI\nPower BI dashboards"]
  end

  subgraph SYS["Systems of Record"]
    D365["Dynamics 365\nCase Management"]
    PAY["Payments / ERP"]
  end

  PORTAL --> EXTID --> ORCH
  OFFICER --> RBAC --> ORCH
  VID --> A1
  ORCH --> AI
  ORCH --> DATA
  A5 --> EXT
  A7 --> SENTINEL
  A7 --> DEFENDER
  A9 --> COSMOS
  A6 --> PAY
  A6 --> D365
  A10 --> M365
  A11 --> M365
  ORCH --> PURVIEW
  A6 --> RAI
```

---

## 2. Component inventory (capability → service → how to build)

See `docs/capability-map.md` for the full 18-capability table. Summary of the spine:

| Layer | Component | Azure service | SDK / API | Accelerator to start from |
|-------|-----------|---------------|-----------|---------------------------|
| UI | Citizen Portal + Officer console | Azure Container Apps / Static Web Apps | React | *(prototype in `web/`)* |
| Identity | Verifiable credential + auth | Entra External ID, Verified ID | MSAL, Verified ID request API | — |
| Orchestration | Multi-agent | **Azure AI Foundry Agent Service** | Foundry SDK + Semantic Kernel | **Multi-Agent Custom Automation Engine** |
| Doc AI | OCR / extraction / tamper | Document Intelligence, AI Vision, Content Understanding | `azure-ai-documentintelligence`, `azure-ai-vision` | **Document Knowledge Mining** |
| Identity AI | Liveness / deepfake | Azure Face | Face API (liveness SDK) | **Digital Identity Analyzer** |
| Reasoning | Decisions, NLP, case gen | Azure OpenAI (GPT-4o) | `openai` / Foundry | — |
| Retrieval | Policy grounding | Azure AI Search | `azure-search-documents` | Document Knowledge Mining |
| ML | Risk score + anomaly | Azure Machine Learning | `azure-ai-ml` | — |
| Data | Lakehouse + cross-match | Microsoft Fabric / OneLake | Fabric SQL/Spark | **Unified data foundation with Fabric** |
| Graph | Relationship network | Cosmos DB (Gremlin) | `gremlinpython` | — |
| Cyber | Signal & threat intel | Sentinel + Defender | Log Analytics / MDTI API | — |
| Governance | Audit, lineage, RAI | Purview + Power BI | Purview API | **Deploy Your AI App in Production** |
| SoR | Case + payments | Dynamics 365, ERP | Dataverse API | — |

---

## 3. Scenario 1 — pre-submission block (sequence)

```mermaid
sequenceDiagram
  participant C as Citizen (Andrei)
  participant P as Citizen Portal
  participant O as Foundry Orchestrator
  participant ID as Identity Proofing Agent
  participant DP as Doc Parsing Agent
  participant VA as Validation Agent
  participant FV as Face Verification Agent
  participant CC as Consistency Checker
  participant ED as Eligibility Decision Agent
  participant PV as Purview

  C->>P: Start application
  P->>O: Begin intake (session)
  O->>ID: Request verifiable credential (Entra Verified ID)
  ID-->>O: FAIL — no verifiable credential (+risk)
  C->>P: Upload passport
  O->>DP: Extract (Document Intelligence)
  DP-->>O: Fields + image
  O->>VA: Tamper check (Azure AI Vision / ELA + EXIF)
  VA-->>O: TAMPERED portrait, edited 2d ago (+risk)
  C->>P: Upload pay stub + utility bill
  O->>CC: Cross-match employer/income (Fabric + registry)
  CC-->>O: Fictitious employer, income mismatch (+risk)
  C->>P: Join video consultation
  O->>FV: Liveness + deepfake (Azure Face)
  FV-->>O: DEEPFAKE, face mismatch (+risk)
  O->>ED: Compose decision (Azure OpenAI + thresholds)
  ED-->>O: BLOCK (risk 95) + explanation
  O->>PV: Write immutable audit + RAI explanation
  O-->>P: Submission blocked before filing
```

**Decision logic:** weighted risk score with explainable contributions
`{document_tampering:0.34, deepfake_liveness:0.26, fictitious_employer:0.20, identity_unverifiable:0.12, cross_record_mismatch:0.08}`.
Block threshold ≥ 70. Minor-mismatch band (35–55, single low-weight signal) → **auto-reconcile or human review**, never auto-block (fairness safeguard).

---

## 4. Scenario 2 — post-submission detection (sequence)

```mermaid
sequenceDiagram
  participant T as Submission telemetry
  participant F as Fabric / Sentinel
  participant CS as Cyber Signals Agent
  participant ML as Azure ML (anomaly)
  participant PR as Prioritization Agent
  participant GR as Graph Explorer (Cosmos)
  participant M as Officer (Maria)
  participant DG as Document Generator
  participant N as Notification Agent
  participant PV as Purview

  T->>F: IP, device fp, cadence, form data
  F->>CS: Stream + batch features
  CS->>ML: Score burst (same IP, <17s, bot cadence)
  ML-->>CS: Anomaly 0.97
  CS->>GR: Build relationship subgraph
  GR-->>CS: 9 applicants ↔ IP/employer/IBAN/phone
  CS->>PR: Emit cluster #4471
  PR-->>M: Rank #1 in queue (risk 97)
  M->>GR: Inspect graph (interactive)
  M->>M: DECIDE (human-in-the-loop)
  M->>F: Freeze payments (×9)
  M->>DG: Generate case file (Copilot + Word)
  M->>N: Notify Tax / Police / FIU (Purview-governed)
  M->>PV: All actions audited
```

**Cyber-signal feature vector (Scenario 2 fixtures):** see `data/scenario2-cluster.json`.
Key features: `same_source_ip`, `device_fingerprint_reuse`, `interarrival_seconds`, `fields_per_second`,
`shared_employer_unregistered`, `shared_iban_ratio`, `asn_is_hosting`.

---

## 5. Security, privacy & governance

- **Zero-Trust landing zone**, private endpoints, no public AI endpoints (pattern: *Deploy Your AI App in Production* accelerator).
- **Entra** External ID + Verified ID + RBAC; MFA for officers.
- **Purview**: immutable audit of every agent action and officer decision; data lineage Bronze→Gold; DLP on cross-agency disclosures (field-level minimization).
- **Responsible AI**: explainable risk contributions on every decision; Power BI RAI dashboards; documented fairness safeguard; human-in-the-loop on all enforcement actions.
- **Content Safety** on all generative output (case files, notifications).
- **Data minimization** in partner-agency notifications — each agency receives only authorized fields.

---

## 6. Deployment topology (demo)

```mermaid
flowchart LR
  subgraph ACA["Azure Container Apps"]
    WEB["web (static)"]
    API["orchestrator API\n(FastAPI — app/)"]
  end
  FOUNDRY["Azure AI Foundry\nAgent Service + GPT-4o"]
  AISVC["Azure AI services\n(DI · Vision · Face · Search)"]
  FAB["Fabric / OneLake"]
  COS["Cosmos DB (Gremlin)"]
  WEB --> API --> FOUNDRY --> AISVC
  API --> FAB
  API --> COS
```

- **Demo mode:** the `app/` FastAPI backend serves fixtures from `data/` so the demo runs with **zero Azure dependencies** — perfect for laptops and air-gapped rooms.
- **Live mode:** flip `DEMO_MODE=false` in `.env` and implement the `# TODO(live)` calls in `app/agents.py` against real Azure SDKs.

See `docs/build-plan.md` for the phased path from demo mode to live mode, and `infra/azure-resources.md` for the resource list.
