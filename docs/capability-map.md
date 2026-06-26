# Capability Map — 18 Microsoft AI capabilities → build targets

Every capability that lights up in the storyboard, mapped to a concrete service, the SDK/API to call,
the scenario(s) it appears in, and the accelerator to start from.

| # | Capability (UI label) | Azure / Microsoft service | SDK / API | Scenario | Accelerator |
|---|------------------------|---------------------------|-----------|----------|-------------|
| 1 | Document Intelligence | Azure AI Document Intelligence | `azure-ai-documentintelligence` (prebuilt-idDocument, layout) | 1 | Document Knowledge Mining |
| 2 | Content Understanding | Azure AI Content Understanding | Content Understanding API (multimodal) | 1 | Document Knowledge Mining |
| 3 | AI Vision · tamper detection | Azure AI Vision | Image Analysis 4.0 + custom ELA/EXIF check | 1 | Digital Identity Analyzer |
| 4 | Azure Face · liveness/deepfake | Azure Face | Face Liveness Detection SDK | 1 | Digital Identity Analyzer |
| 5 | Content Safety | Azure AI Content Safety | `azure-ai-contentsafety` | 1 | — |
| 6 | Entra Verified ID | Microsoft Entra Verified ID | Verified ID Request Service API | 1 | — |
| 7 | Azure OpenAI · reasoning/NLP | Azure OpenAI (GPT-4o) | `openai` / Foundry inference | 1,2 | — |
| 8 | Azure ML · risk + anomaly | Azure Machine Learning | `azure-ai-ml`, online endpoint | 1,2 | — |
| 9 | Sentinel · Cyber Signals | Microsoft Sentinel | Log Analytics / KQL, analytics rules | 2 | — |
| 10 | Defender · threat intel | Microsoft Defender TI | MDTI API | 2 | — |
| 11 | Graph analytics | Azure Cosmos DB (Gremlin) | `gremlinpython` | 2 | — |
| 12 | Fabric · OneLake | Microsoft Fabric | Lakehouse SQL / Spark, shortcuts, mirroring | 1,2 | Unified data foundation with Fabric |
| 13 | AI Foundry · multi-agent | Azure AI Foundry Agent Service | Foundry SDK + Semantic Kernel | 1,2 | Multi-Agent Custom Automation Engine |
| 14 | Copilot Studio | Microsoft Copilot Studio | Low-code agents / topics | 2 | — |
| 15 | M365 Copilot | Microsoft 365 Copilot | Graph + Copilot connectors | 2 | — |
| 16 | Power BI · RAI dashboards | Power BI | RAI report templates | 1,2 | — |
| 17 | Microsoft Purview | Microsoft Purview | Purview audit / lineage / DLP APIs | 1,2 | Deploy Your AI App in Production |
| 18 | Responsible AI · explainability | RAI toolbox + Foundry evals | feature-contribution output | 1,2 | — |

## Agents → capabilities

| Agent | Primary capabilities |
|-------|----------------------|
| Identity Proofing | 6 Verified ID, 13 Foundry |
| Document Parsing | 1 Doc Intelligence, 2 Content Understanding |
| Validation | 3 AI Vision, 1 Doc Intelligence |
| Face Verification | 4 Azure Face, 5 Content Safety |
| Consistency Checker | 7 Azure OpenAI, 12 Fabric, external connectors |
| Eligibility Decision | 7 Azure OpenAI, 8 Azure ML, 16/18 RAI, 17 Purview |
| Cyber Signals | 9 Sentinel, 10 Defender, 8 Azure ML |
| Prioritization | 8 Azure ML |
| Graph Relationship Explorer | 11 Cosmos graph |
| Document Generator | 15 M365 Copilot, 14 Copilot Studio, 7 Azure OpenAI |
| Notification | 15 M365 Copilot, 17 Purview |

## Solution accelerators (deploy first, customize second)

1. **Multi-Agent Custom Automation Engine** — the orchestration backbone (Foundry + Semantic Kernel).
2. **Document Knowledge Mining** — ingestion, OCR, extraction, RAG over policies & documents.
3. **Digital Identity Analyzer** — document parsing + face verification + eligibility agents.
4. **Unified data foundation with Fabric** — OneLake medallion, cross-match data estate.
5. **Deploy Your AI App in Production** — WAF-aligned, Zero-Trust, private-endpoint hardening.
