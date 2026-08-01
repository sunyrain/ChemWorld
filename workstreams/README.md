# Workstream evidence

Workstream reports are evidence records, not a second source tree. Current entry points are listed in
`configs/current.json`; consumers should not select a report by modification time or version-looking filename.

The evidence DAG in `scripts/evidence_pipeline.py` is the only supported generation order for current reports.
Superseded reports and raw campaign outputs are retained in Git history or external run storage, not copied into this
tree. Reports bound by a protocol, trajectory digest, or source hash remain immutable until explicitly recertified.

The active first-arXiv research specification is
`workstreams/arxiv_v1/EXPERIMENTAL_INTELLIGENCE_V1_MASTER_PLAN_ZH.md`. Its
machine-readable experiment accounting is
`workstreams/arxiv_v1/reports/experimental-intelligence-experiment-ledger-v0.1.json`.
