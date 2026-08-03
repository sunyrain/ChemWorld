# Workstream evidence

Workstream reports are evidence records, not a second source tree. Current entry points are listed in
`configs/current.json`; consumers should not select a report by modification time or version-looking filename.

The evidence DAG in `scripts/evidence_pipeline.py` is the only supported generation order for current reports.
Superseded reports and raw campaign outputs are retained in Git history or external run storage, not copied into this
tree. Reports bound by a protocol, trajectory digest, or source hash remain immutable until explicitly recertified.

The active Work I execution surface is `workstreams/arxiv_v1/WORK_I_TODOLIST.md`, with task claims in
`workstreams/arxiv_v1/claims/`. The scientific specification is
`workstreams/arxiv_v1/EXPERIMENTAL_INTELLIGENCE_V1_MASTER_PLAN_ZH.md`, and the machine-readable experiment accounting is
`workstreams/arxiv_v1/reports/experimental-intelligence-experiment-ledger-v0.1.json`.
The current primary-source related-work audit and its machine-readable evidence are
`workstreams/arxiv_v1/RELATED_WORK_AUDIT_2026_08_ZH.md` and
`workstreams/arxiv_v1/reports/related-work-evidence-v0.1.json`.
The G0 historical-source and local-data inventory is recorded in
`workstreams/arxiv_v1/G0_SOURCE_DATA_PROVENANCE_AUDIT_ZH.md` and
`workstreams/arxiv_v1/reports/g0-source-and-data-provenance-v0.1.json`.
The active Work II execution surface is `workstreams/flagship_tasks/WORK_II_TODOLIST.md`. Superseded
plans, smoke notes, stopped extensions, and editorial snapshots are available from Git history rather
than kept as competing entry points in the working tree.
