# Synthetic data & documents

A labelled, fully synthetic dataset for the FWA demo. Two parts:

- **`documents/scenario1/`** — the **fraud** applicant's documents (tampered passport, forged pay stub,
  outdated utility bill, deepfake frame), with **ground-truth** tamper/liveness labels in `*.metadata.json`.
- **`documents/scenario2/`** — the **genuine "clean applicant"** control set (Elena Marinescu): valid
  passport, registered-employer pay stub, recent utility bill, passed video frame — the honest citizen
  who sails through. Same agents, opposite outcome.
  Feed both to the Document Parsing, Validation and Face Verification agents
  (Azure Document Intelligence, Azure AI Vision, Azure Face).
- **`datasets/`** — the data-estate tables (applications, telemetry, registry, tax, graph, watchlist).
  Load into **Microsoft Fabric / OneLake** (relational) and **Cosmos DB Gremlin** (graph) to power the
  Consistency Checker, Cyber Signals, Prioritization and Graph Relationship Explorer agents.

> ⚠ **Everything here is synthetic.** Names, national IDs, IBANs, IPs, device hashes, employers,
> phone numbers and figures are fictitious and use a fictional country (Republic of Utopia) and
> documentation/test ranges (e.g. `203.0.113.0/24`, `198.51.100.0/24`). No real person or document.

## Regenerate
```bash
python synthetic-data/generators/build_datasets.py     # → datasets/*.csv
python synthetic-data/generators/build_documents.py    # → documents/scenario1/*.png (+ metadata)
```
The document generator expects two synthetic ID portraits at `working/id-face-genuine.png` and
`working/id-face-imposter.png` (any head-and-shoulders images work); it falls back to placeholders if absent.

## Consistency with the rest of the kit
These artifacts match the fixtures in `data/scenario1-applicant.json` and `data/scenario2-cluster.json`
(same applicants, amounts, IP `203.0.113.45`, employer "Northwind Staffing Solutions LLC", cluster #4471,
€12,680/mo held). The same values drive the prototype UI and the API.
