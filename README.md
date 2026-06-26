# Benefits Integrity Cloud — FWA Detection & Prevention
### Interactive demo · Microsoft Public Sector (Health & Social Services)

An interactive demo showing how Microsoft AI detects and prevents fraud, waste & abuse across the benefits lifecycle. Stops an organized crime ring using fake identities, forged documents and deepfakes — while genuine applicants pass through effortlessly.

> **All data is synthetic.** Names, documents, employers, IPs and figures are fictitious.

---

## Quick start (60 seconds, no Azure needed)

**Windows:**
```bat
start.bat
```

**Mac / Linux:**
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r app/requirements.txt
uvicorn app.main:app --port 8000
```

Then open **http://localhost:8000**

---

## What's in the demo

Three interactive scenarios:

| Scenario | Persona | What it shows |
|---|---|---|
| 01 · Prevention | Applicant (covert fraud-ring member) | Blocked pre-submission: tampered passport, forged pay stub, deepfake video |
| 02 · Fair access | Genuine applicant (Elena) | Same agents, all checks pass — auto-approved at risk 12 |
| 03 · Detection | Social Services Officer | Coordinated burst detected: 9 apps, same IP, 17 seconds — freeze, escalate, case file, notify |

18 Microsoft AI capabilities light up as you move through each scenario.

---

## API endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/capabilities` | List 18 AI capabilities |
| POST | `/api/scenario1/session` | Begin applicant intake session |
| POST | `/api/scenario1/step/{1..5}` | Run next intake check — returns findings + risk delta |
| GET | `/api/scenario1/decision` | Final eligibility decision + explainability |
| GET | `/api/officer/queue` | Risk-ranked case queue |
| GET | `/api/officer/clusters/4471` | Cluster investigation detail |
| GET | `/api/officer/clusters/4471/graph` | Relationship graph (nodes + edges) |
| POST | `/api/officer/clusters/4471/actions/{freeze\|escalate\|casefile\|notify}` | Officer action |
| GET | `/api/officer/clusters/4471/casefile` | Download generated .docx case file |

Interactive API docs: **http://localhost:8000/api/docs**

---

## Repo structure

```
├── app/
│   ├── main.py          FastAPI orchestrator — serves the API + the UI
│   ├── agents.py        Agent layer (DEMO_MODE fixtures + live TODO stubs)
│   └── requirements.txt
├── data/
│   ├── scenario1-applicant.json
│   └── scenario2-cluster.json
├── web/
│   └── index.html       Interactive prototype (all 3 scenarios, guided tour)
├── docs/                Demo script, reference architecture, capability map, build plan
├── agents/              Agent manifest + specifications (machine-readable)
├── api/                 OpenAPI contract
├── synthetic-data/      Labelled documents + data-estate CSVs + generators
├── start.bat            One-click start (Windows)
└── Dockerfile
```

## Going live

Set `DEMO_MODE=false` in `.env` and implement the `# TODO(live)` stubs in `app/agents.py` one agent at a time. See `docs/build-plan.md` for the phased path to real Azure AI Foundry agents.

Grounded in *RefArch PH&SS — Enable detection and prevention for Fraud, Waste & Abuse*.
