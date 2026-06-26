"""
Benefits Integrity Cloud — FWA demo orchestrator API.

DEMO_MODE=true (default): serves fixtures from /data — runs with zero Azure dependencies.
DEMO_MODE=false: wire the `# TODO(live)` calls in agents.py to real Azure services.

Run:  uvicorn app.main:app --reload --port 8000   (from the repo root)
Then open http://localhost:8000  (serves web/index.html)
"""
import io
import json
import os
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

from . import agents

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() != "false"

app = FastAPI(title="Benefits Integrity Cloud — FWA Demo API", version="1.0.0")


def load(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


S1 = load("scenario1-applicant.json")
S2 = load("scenario2-cluster.json")
S3 = load("scenario3-genuine.json")

CAPABILITIES = [
    "docintel", "content", "vision", "face", "safety", "verid", "openai", "aml",
    "sentinel", "defender", "graph", "fabric", "foundry", "copstudio", "m365",
    "powerbi", "purview", "rai",
]


@app.get("/api/capabilities")
def capabilities():
    return {"total": len(CAPABILITIES), "capabilities": CAPABILITIES}


# ---------- Scenario 1 — applicant intake ----------
@app.post("/api/scenario1/session")
def s1_session():
    return {"sessionId": "demo-session", "applicant": S1["applicant"]}


@app.post("/api/scenario1/step/{order}")
def s1_step(order: int):
    steps = S1["steps"]
    if order < 1 or order > len(steps):
        raise HTTPException(404, "no such step")
    step = agents.run_intake_step(steps[order - 1], demo=DEMO_MODE)
    cumulative = min(95, sum(s["result"]["riskDelta"] for s in steps[:order]))
    return {**step, "cumulativeRisk": cumulative}


@app.get("/api/scenario1/decision")
def s1_decision():
    return agents.compose_decision(S1, demo=DEMO_MODE)


# ---------- Scenario 1 — upload-based analysis (accepts file, returns fixtures) ----------
@app.post("/api/scenario1/analyze/{step}")
async def s1_analyze(step: int, file: UploadFile = File(None)):
    """Accepts an uploaded document and returns fixture-based AI findings.
    In DEMO_MODE the file content is ignored; in live mode it would be forwarded
    to Azure AI Document Intelligence / Vision / Face.
    """
    steps = S1["steps"]
    if step < 1 or step > len(steps):
        raise HTTPException(404, "no such step")
    result = agents.run_intake_step(steps[step - 1], demo=DEMO_MODE)
    cumulative = min(95, sum(s["result"]["riskDelta"] for s in steps[:step]))
    return {**result, "cumulativeRisk": cumulative}


# ---------- Scenario 2 — officer detection ----------
@app.get("/api/officer/queue")
def officer_queue():
    return {"queue": S2["queue"]}


@app.get("/api/officer/clusters/{cid}")
def cluster_detail(cid: str):
    if cid not in (S2["cluster"]["id"], f"#{S2['cluster']['id']}", "4471"):
        raise HTTPException(404, "unknown cluster")
    c = S2["cluster"]
    return {
        "cluster": c,
        "applications": S2["applications"],
        "totals": S2["totals"],
        "timestamps": c["submissionTimestamps"],
    }


@app.get("/api/officer/clusters/{cid}/graph")
def cluster_graph(cid: str):
    return agents.build_graph(S2, demo=DEMO_MODE)


@app.post("/api/officer/clusters/{cid}/actions/{action}")
def officer_action(cid: str, action: str):
    if action not in S2["actions"]:
        raise HTTPException(400, "unknown action")
    return agents.execute_action(action, S2, demo=DEMO_MODE)


@app.get("/api/officer/clusters/{cid}/casefile")
def download_casefile(cid: str):
    buf = agents.generate_case_file(S2)
    headers = {"Content-Disposition": 'attachment; filename="Fraud-Case-File-Cluster-4471.docx"'}
    return StreamingResponse(
        io.BytesIO(buf),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers=headers,
    )


# ---------- Scenario 3 — genuine applicant (upload-based) ----------
@app.post("/api/scenario3/analyze/{step}")
async def s3_analyze(step: int, file: UploadFile = File(None)):
    """Same as scenario1/analyze but returns clean/passing fixture data for the genuine applicant."""
    steps = S3["steps"]
    if step < 1 or step > len(steps):
        raise HTTPException(404, "no such step")
    s = steps[step - 1]
    r = s["result"]
    cumulative = sum(st["result"]["riskDelta"] for st in steps[:step])
    return {
        "order": step,
        "agent": s["agent"],
        "title": s["title"],
        "capabilities": s["capabilities"],
        "findings": r["findings"],
        "riskDelta": r["riskDelta"],
        "ok": r.get("ok", True),
        "cumulativeRisk": cumulative,
        "demo": True,
    }


@app.get("/api/scenario3/decision")
def s3_decision():
    return S3["decision"]


# ---------- static prototype UI (mount last so /api wins) ----------
# Serve synthetic sample documents at /docs/<scenario>/<filename>
SYNTH_DOCS = ROOT / "synthetic-data" / "documents"
if SYNTH_DOCS.exists():
    app.mount("/docs", StaticFiles(directory=str(SYNTH_DOCS)), name="docs")

WEB = ROOT / "web"
if WEB.exists():
    app.mount("/", StaticFiles(directory=str(WEB), html=True), name="web")
