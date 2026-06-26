"""
Agent layer for the Benefits Integrity Cloud FWA demo.

DEMO_MODE=true (default): every function returns pre-built fixtures immediately,
with zero Azure dependencies.

DEMO_MODE=false: replace the `# TODO(live)` stubs with real Azure AI Foundry
agent calls — one at a time, per the phased build-plan in docs/build-plan.md.
"""
import io
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

# ---------------------------------------------------------------------------
# Scenario 1 — applicant intake
# ---------------------------------------------------------------------------


def run_intake_step(step: dict, demo: bool = True) -> dict:
    """Run (or simulate) a single intake check for Scenario 1.

    Returns the step enriched with an ``agent_note`` in demo mode, or calls
    a real Azure AI Foundry agent in live mode.
    """
    if demo:
        # Pass through the fixture data unchanged; add a demo watermark.
        return {
            "order": step["order"],
            "agent": step["agent"],
            "title": step["title"],
            "capabilities": step["capabilities"],
            "findings": step["result"]["findings"],
            "riskDelta": step["result"]["riskDelta"],
            "demo": True,
        }

    # TODO(live) — Phase 3
    # from azure.ai.projects import AIProjectClient
    # from azure.identity import DefaultAzureCredential
    # client = AIProjectClient(os.environ["FOUNDRY_PROJECT_ENDPOINT"], DefaultAzureCredential())
    # agent = client.agents.get_agent(step["agent"])
    # result = agent.run(payload=step)
    # return result.output
    raise NotImplementedError("Live mode not yet wired — set DEMO_MODE=true")


def compose_decision(s1: dict, demo: bool = True) -> dict:
    """Compose the final eligibility decision for Scenario 1."""
    if demo:
        d = s1["decision"]
        return {
            "outcome": d["outcome"],
            "stage": d["stage"],
            "riskScore": d["riskScore"],
            "blockThreshold": d["blockThreshold"],
            "reasons": d["reasons"],
            "explainability": d["explainability"],
            "fairnessSafeguard": d["fairnessSafeguard"],
            "audit": d["audit"],
            "demo": True,
        }

    # TODO(live) — Phase 4
    raise NotImplementedError("Live mode not yet wired")


# ---------------------------------------------------------------------------
# Scenario 2 — officer / cluster detection
# ---------------------------------------------------------------------------


def build_graph(s2: dict, demo: bool = True) -> dict:
    """Return the relationship graph for a fraud cluster."""
    if demo:
        applications = s2["applications"]
        cluster = s2["cluster"]

        # Build node + edge lists from fixture data.
        nodes = []
        edges = []

        hub_meta = {
            "ip":    {"label": cluster["cyberSignals"]["sourceIp"], "color": "#3b9bff", "r": 17},
            "emp":   {"label": cluster["sharedEntities"]["employer"]["name"][:20], "color": "#9d7bff", "r": 15},
            "bank":  {"label": "IBAN ••4471", "color": "#37e0d8", "r": 15},
            "phone": {"label": "Phone ×2", "color": "#ffba49", "r": 13},
        }
        for hid, meta in hub_meta.items():
            nodes.append({"id": hid, "label": meta["label"], "type": hid,
                          "color": meta["color"], "r": meta["r"]})

        for i, app in enumerate(applications):
            ang = (3.14159 * 2 / len(applications)) * i - 3.14159 / 2
            import math
            x = 50 + math.cos(ang) * 40
            y = 50 + math.sin(ang) * 40
            nodes.append({"id": f"a{i}", "label": app["applicant"],
                          "type": "applicant", "color": "#ff5d76", "r": 6,
                          "x": round(x, 2), "y": round(y, 2)})
            # All applicants share IP and employer
            edges.append({"source": f"a{i}", "target": "ip"})
            edges.append({"source": f"a{i}", "target": "emp"})
            if app.get("sharedIban"):
                edges.append({"source": f"a{i}", "target": "bank"})
            if app.get("sharedPhone"):
                edges.append({"source": f"a{i}", "target": "phone"})

        return {"nodes": nodes, "edges": edges, "demo": True}

    # TODO(live) — Phase 4 (Cosmos DB Gremlin)
    raise NotImplementedError("Live mode not yet wired")


def execute_action(action: str, s2: dict, demo: bool = True) -> dict:
    """Execute an officer action (freeze / escalate / casefile / notify)."""
    if demo:
        a = s2["actions"][action]
        audit_ts = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        return {
            "action": action,
            "status": a["status"],
            "label": a["label"],
            "agent": a["agent"],
            "detail": {k: v for k, v in a.items() if k not in ("label", "agent", "status")},
            "audit": {
                "timestamp": audit_ts,
                "loggedTo": "Microsoft Purview",
                "officer": "Maria S.",
                "clusterId": s2["cluster"]["id"],
            },
            "demo": True,
        }

    # TODO(live) — Phase 5
    raise NotImplementedError("Live mode not yet wired")


# ---------------------------------------------------------------------------
# Case file generation (python-docx)
# ---------------------------------------------------------------------------

_EUR = lambda n: f"€{n:,.0f}"  # noqa: E731


def generate_case_file(s2: dict) -> bytes:
    """Generate a .docx fraud case file for a cluster and return the raw bytes."""
    cluster = s2["cluster"]
    applications = s2["applications"]
    totals = s2["totals"]
    signals = cluster["cyberSignals"]
    actions = s2["actions"]

    doc = Document()

    # ── styles ──────────────────────────────────────────────────────────────
    style = doc.styles["Normal"]
    style.font.name = "Segoe UI"
    style.font.size = Pt(11)

    def heading(text: str, level: int = 1):
        h = doc.add_heading(text, level=level)
        h.runs[0].font.color.rgb = RGBColor(0x1F, 0x4F, 0xA0)

    def add_kv(label: str, value: str, bad: bool = False):
        p = doc.add_paragraph()
        run_l = p.add_run(f"{label}: ")
        run_l.bold = True
        run_v = p.add_run(value)
        if bad:
            run_v.font.color.rgb = RGBColor(0xFF, 0x3B, 0x5C)
        p.paragraph_format.space_after = Pt(2)

    # ── cover ────────────────────────────────────────────────────────────────
    title = doc.add_heading(f"Fraud Case File — Cluster #{cluster['id']}", 0)
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    sub = doc.add_paragraph(
        f"PREPARED BY MICROSOFT 365 COPILOT  ·  CONFIDENTIAL  ·  CASE ENF-{cluster['id']}"
    )
    sub.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    sub.runs[0].font.size = Pt(9)
    sub.runs[0].font.color.rgb = RGBColor(0x9D, 0xB4, 0xE6)

    doc.add_paragraph(
        f"Generated: {datetime.utcnow().strftime('%B %d, %Y')}  ·  "
        f"Risk score: {cluster['risk']} / 100  ·  CRITICAL"
    ).runs[0].bold = True

    doc.add_page_break()

    # ── 1. Executive summary ─────────────────────────────────────────────────
    heading("1. Executive summary")
    doc.add_paragraph(
        f"Nine benefit applications were submitted from a single IP address "
        f"({signals['sourceIp']}) within a {signals['submissionWindowSeconds']:.1f}-second window "
        f"by an automated agent, all citing the unregistered employer "
        f"\u201c{cluster['sharedEntities']['employer']['name']}\u201d and sharing a common bank account. "
        f"Cyber-signal, pattern and graph evidence indicate a coordinated organized-fraud ring. "
        f"All nine payments have been frozen and an enforcement case opened. "
        f"No improper funds were released."
    )

    # ── 2. Cyber-signal evidence ─────────────────────────────────────────────
    heading("2. Cyber-signal evidence")
    table = doc.add_table(rows=1, cols=2)
    table.style = "Table Grid"
    hdr = table.rows[0].cells
    hdr[0].text = "Signal"
    hdr[1].text = "Finding"
    for hc in hdr:
        hc.paragraphs[0].runs[0].bold = True

    rows = [
        ("Source IP", signals["sourceIp"]),
        ("Network (ASN)", f"{signals['asnType'].title()} · {signals['asn']}"),
        ("Device fingerprint", f"Reused ×{signals['deviceFingerprintReuse']} (hash {signals['deviceFingerprint']})"),
        ("Form-fill cadence", f"~{signals['formFillMsPerField']} ms/field (bot-driven)"),
        ("Submission window", f"{signals['submissionWindowSeconds']:.1f} seconds ({cluster['applicationCount']} applications)"),
        ("Mean inter-arrival", f"{signals['meanInterArrivalSeconds']:.1f} seconds"),
        ("Threat-intel match", signals["threatIntelMatch"]),
    ]
    for label, val in rows:
        r = table.add_row().cells
        r[0].text = label
        r[1].text = val

    # ── 3. Submission burst timeline ─────────────────────────────────────────
    heading("3. Submission burst timeline")
    doc.add_paragraph(
        f"Applications submitted {cluster['submissionTimestamps'][0]} to "
        f"{cluster['submissionTimestamps'][-1]} local time. "
        f"Mean inter-arrival {signals['meanInterArrivalSeconds']:.1f} seconds — "
        f"far below human entry speed and consistent with scripted automation."
    )

    # ── 4. Network relationships ──────────────────────────────────────────────
    heading("4. Network relationships")
    shared = cluster["sharedEntities"]
    for item in [
        f"Shared source IP across all {cluster['applicationCount']} applications",
        f"Shared employer: \u201c{shared['employer']['name']}\u201d (no active business / VAT registration)",
        f"Shared bank account / IBAN on {shared['ibanSharedOn']} of {cluster['applicationCount']} applications",
        f"Two shared contact phone numbers across the cluster",
    ]:
        doc.add_paragraph(item, style="List Bullet")

    # ── 5. Application inventory ──────────────────────────────────────────────
    heading("5. Application inventory")
    table2 = doc.add_table(rows=1, cols=4)
    table2.style = "Table Grid"
    hdr2 = table2.rows[0].cells
    for i, h in enumerate(["Application ID", "Applicant", "Monthly benefit", "Status"]):
        hdr2[i].text = h
        hdr2[i].paragraphs[0].runs[0].bold = True

    for app in applications:
        r = table2.add_row().cells
        r[0].text = app["id"]
        r[1].text = app["applicant"]
        r[2].text = _EUR(app["monthlyBenefitEur"])
        r[3].text = "FROZEN"

    total_row = table2.add_row().cells
    total_row[0].text = ""
    total_row[1].text = "Total monthly disbursement held"
    total_row[1].paragraphs[0].runs[0].bold = True
    total_row[2].text = _EUR(totals["monthlyBenefitHeldEur"])
    total_row[2].paragraphs[0].runs[0].bold = True
    total_row[3].text = "FROZEN"

    # ── 6. Responsible-AI risk explainability ─────────────────────────────────
    heading("6. Responsible-AI risk explainability")
    table3 = doc.add_table(rows=1, cols=2)
    table3.style = "Table Grid"
    hdr3 = table3.rows[0].cells
    hdr3[0].text = "Contributing factor"
    hdr3[1].text = "Weight"
    for hc in hdr3:
        hc.paragraphs[0].runs[0].bold = True

    labels = {
        "coordinated_same_ip_burst": "Coordinated same-IP burst",
        "shared_fictitious_employer": "Shared fictitious employer",
        "shared_bank_account": "Shared bank account / IBAN",
        "bot_like_form_cadence": "Bot-like form cadence",
        "device_fingerprint_reuse": "Device fingerprint reuse",
    }
    for key, pct in cluster["riskExplainability"].items():
        r = table3.add_row().cells
        r[0].text = labels.get(key, key)
        r[1].text = f"{int(pct * 100)}%"

    # ── 7. Actions taken ──────────────────────────────────────────────────────
    heading("7. Actions taken")
    freeze_total = sum(a["monthlyBenefitEur"] for a in applications)
    for item in [
        f"Payments frozen — disbursement halted on all {cluster['applicationCount']} applications ({_EUR(freeze_total)}/mo held)",
        "Escalated to investigation — enforcement case ENF-4471, investigator J. Marković assigned, 48h SLA",
        "Case file generated — this document, by Document Generator + M365 Copilot",
        "Partner agencies notified — Tax Authority, Police Financial Crimes Unit, FIU (Purview-governed data-share)",
    ]:
        doc.add_paragraph(item, style="List Bullet")

    # ── 8. Recommended action ─────────────────────────────────────────────────
    heading("8. Recommended action")
    doc.add_paragraph(
        "Maintain the payment freeze, pursue enforcement against the identified ring, "
        "and recover any prior disbursements linked to the shared bank account. "
        "Reinstate individually any application later cleared through manual review."
    )

    # ── Governance note ───────────────────────────────────────────────────────
    note = doc.add_paragraph(
        "Fairness & governance: all automated findings are explainable and were confirmed "
        "by a human officer. Every decision and field-level disclosure is logged in "
        "Microsoft Purview."
    )
    note.runs[0].italic = True

    # ── Footer ────────────────────────────────────────────────────────────────
    doc.add_paragraph(
        "\nDemonstration document · synthetic data. "
        "Names, companies, IP addresses and figures are fictitious and for illustration only."
    ).runs[0].font.color.rgb = RGBColor(0x88, 0x88, 0x88)

    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()
