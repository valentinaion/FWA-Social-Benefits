# Demo Script — Fraud, Waste & Abuse Detection & Prevention
### Microsoft Public Sector · Health & Social Services
**Codename:** Benefits Integrity Cloud  ·  **Runtime:** 8–12 min live, or self-running guided mode
**Storyboard reference:** `web/index.html` (the interactive prototype)

> All names, documents, companies, IPs and figures in this demo are **synthetic** and for illustration only.

---

## 0. Setup & framing (before you click — 60s)

**Say:**
> "Governments pay out trillions in benefits every year. A small fraction is lost to fraud — but increasingly that fraud is *organized*: crime networks using fake identities, forged documents, and now deepfakes to extract improper payments at scale.
>
> Today I'll show you two personas — an **applicant** and a **social services officer** — and how Microsoft AI works for both: stopping fraud *before* a payment is ever made, while letting genuine citizens through effortlessly. Everything you see maps to our Public Health & Social Services reference architecture for Fraud, Waste & Abuse."

**Do:** Open `index.html`. Land on the **Overview**. Point to the 4 KPIs and the **18-capability map** (greyed out — "watch these light up").

**Key message:** *Prevention over recovery. Genuine citizens unaffected. Every decision explainable and human-led.*

---

## Scenario 1 — "Stopped before submission" (Applicant · ~4 min)

> Maps to RefArch stage **1 — Intake & Enrollment** and **2 — Risk Scoring & Screening**.

**Say:**
> "Meet our applicant, Andrei. What the system *doesn't* know yet — but we do — is that Andrei is a member of an organized fraud ring. Let's watch him apply."

**Do:** Switch to the **Applicant** tab. Note the amber banner: *known to audience as a ring member.*

Click **Run next check →** six times. Narrate each beat as the agents fire and the **live fraud-risk gauge** climbs:

| # | On screen | Talk track | Capability lit |
|---|-----------|-----------|----------------|
| 1 | Identity proofing | "We start with identity. We ask for a **verifiable credential** through Microsoft Entra Verified ID — not a self-typed name. Andrei can't produce one." | Entra Verified ID, AI Foundry |
| 2 | Passport upload | "He uploads a passport. **Document Intelligence** reads it instantly — but **Azure AI Vision** sees what a human can't: the portrait was **face-swapped**. Error-Level Analysis lights up the spliced region; metadata shows it was edited two days ago." | Document Intelligence, AI Vision, Content Understanding |
| 3 | Pay stub | "Proof of income — a pay stub from *Northwind Staffing Solutions*. We cross-match against the business registry and tax records in **Microsoft Fabric**. The employer **doesn't legally exist**, and the document is synthetic." | Document Intelligence, Azure OpenAI, Fabric |
| 4 | Utility bill | "Proof of address — but it's 11 months old and the name field was altered. Outside policy, and tampered." | Document Intelligence, AI Vision |
| 5 | Video consult | "Now the remote consultation. Andrei uses a **deepfake** on camera. **Azure Face** liveness detection isn't fooled — no natural micro-expressions, frame-level GAN artifacts, and the face doesn't match even the (already forged) ID." | Azure Face, Content Safety, AI Vision |
| 6 | Decision | "**Azure AI Foundry** orchestrates every agent's finding into one decision — and **blocks the claim before it is ever submitted.** No payment instruction was ever created." | AI Foundry, Azure OpenAI, Responsible AI, Purview, Power BI |

**Do:** Let the **verdict banner** render. Read the reasons. Point to the **Responsible-AI explainability bars**.

**Say (the punch line):**
> "Two things matter here. First — this was stopped at the *door*, not clawed back months later. Second — see this fairness note: a *genuine* applicant with a blurry scan or a minor mismatch isn't blocked; they're auto-reconciled or sent to a human. The system is tuned to protect honest citizens *and* the treasury. And every decision is logged to **Microsoft Purview**."

---

## Scenario 2 — "The coordinated ring" (Officer · ~4 min)

> Maps to RefArch stage **4 — Continuous Monitoring** and **5 — Investigation & Enforcement**.

**Say:**
> "No system catches 100% at intake. So we also watch what's *already* submitted. This is the officer's view — Maria, a Benefits Integrity Analyst."

**Do:** Switch to the **Officer** tab. The **Prioritization Agent** has ranked the queue. Point to the hot case at the top.

**Say:**
> "Top of her queue: **Cluster #4471** — nine applications the **Cyber Signals Agent** has linked together."

**Do:** Click the cluster. Walk the three evidence panels:

1. **Cyber signals** — "Same source IP. A hosting/VPN network. The *same device fingerprint* reused nine times. Form fields filled in ~74 milliseconds each — no human types that fast. This is a **bot**."
2. **Burst timeline** — "All nine submitted inside **16.8 seconds**. Watch them drop onto the timeline." (the dots animate)
3. **Relationship graph** — "And here's the network. **Graph analytics on Azure Cosmos DB** links all nine applicants to a shared IP, the same fake employer, a shared bank account, and shared phones. Click any applicant…" *(click a node — shared edges highlight)* "…and the ring lights up."

**Say:**
> "Minutes — not weeks. Now Maria decides. **Human in the loop** — the AI recommends, the officer acts."

**Do:** Click the four decision actions in order and narrate each rich panel:

- **🧊 Freeze payments** — "All nine payments flip to **FROZEN**. €12,680 a month held — nothing leaves the treasury."
- **🚨 Escalate to investigation** — "An enforcement case opens in **Dynamics 365**, an investigator is assigned, evidence auto-attached."
- **📄 Generate case file** — "**M365 Copilot** drafts the full case file from all the evidence…" *(preview appears)* "…and we can **download it right here.**" *(click Download — hand out the .docx)*
- **📨 Notify partner agencies** — "Secure, **Purview-governed** alerts to the tax authority, police financial-crimes unit, and the FIU — each gets only the fields they're authorized to see."

**Do:** Point to the **'Actions taken (4/4)'** counter, the **Purview audit trail**, and the **'Case fully actioned'** banner.

---

## Close — "From recovery to prevention" (~60s)

**Do:** Either finish naturally or click **▶ Play the story** earlier to run the whole thing hands-free for a recording.

**Say:**
> "One unified data estate. A team of AI agents. Fraud stopped at the source, genuine citizens served faster, and every decision explainable, governed, and human-led. That's the shift — from chasing money after it's gone, to **preventing the loss in real time.** And it's all built on services you already own in the Microsoft Cloud."

**Capability scoreboard:** by the end, **18 / 18** capabilities are lit.

---

## Talk-track cheat sheet (one-liners)

- *"Prevention, not recovery."*
- *"Genuine citizens unaffected — fairness is engineered in."*
- *"The AI recommends; a human decides; Purview remembers."*
- *"Minutes, not weeks."*
- *"Everything here maps to the PH&SS reference architecture — and to solution accelerators you can deploy today."*

## Anticipated questions

| Question | Answer |
|----------|--------|
| Is this real or mocked? | The prototype is synthetic. The **kit** (this package) shows exactly how to build it for real on Azure AI Foundry + Azure AI services. |
| How do you avoid false positives on honest people? | Risk thresholds + human-in-the-loop + auto-reconciliation of minor mismatches. Low-risk cases auto-approve (see queue item #A-88204). |
| Data residency / compliance? | Entra, Purview, sovereign/Zero-Trust landing zone; GDPR/CCPA controls. See `docs/reference-architecture.md` §Security. |
| Explainability? | Responsible-AI feature contributions surface on every decision; Power BI RAI dashboards for oversight. |
| How fast to build? | See `docs/build-plan.md` — leverages 5 existing solution accelerators. |
