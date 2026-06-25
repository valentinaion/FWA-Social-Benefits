# Scenario-1 documents — labelled test set

Each document is a **synthetic SPECIMEN**. Use them to exercise the prevention agents; the expected
result is the "ground truth" — what a correctly-built agent should detect.

| File | Represents | Ground truth | Consumed by (agent) | Azure service |
|------|-----------|--------------|---------------------|---------------|
| `passport-clean.png` | Legitimate ID portrait baseline | genuine | Document Parsing | Document Intelligence |
| `passport-tampered.png` | Face-swapped passport | **tampered** (portrait splice, ELA hotspot, edited metadata) | Validation | Azure AI Vision |
| `passport-tampered.metadata.json` | Ground-truth labels for the above | — | (test oracle) | — |
| `payslip-northwind.png` | Forged pay stub, fictitious employer | **fraudulent** (unregistered employer, weekend pay date) | Consistency Checker | Doc Intelligence + Fabric |
| `utility-bill.png` | Outdated + altered proof of address | **invalid** (11 months old; altered name field) | Validation | Document Intelligence |
| `video-consult-frame.png` | Deepfake remote consultation frame | **deepfake** | Face Verification | Azure Face |
| `video-session.metadata.json` | Ground-truth liveness/deepfake signals | — | (test oracle) | — |

## Notes
- **Two different faces** appear on the clean vs. tampered passport — that *is* the face-swap.
  The genuine portrait belongs to the document; the imposter face is spliced in and also used in the deepfake frame.
- The tampered passport carries an edited-software hint and a recent `LastModified` in its PNG metadata
  (read with `exiftool` or `PIL.Image.info`) — a cheap signal before pixel-level analysis.
- PNG is used throughout because Azure Document Intelligence and Vision accept it directly. Convert to
  PDF/JPEG if your pipeline prefers (e.g. `soffice` or `img2pdf` in an environment with a JPEG encoder).
