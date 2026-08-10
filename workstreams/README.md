# Workstream evidence

Workstream reports are evidence records, not a second source tree. Current entry points are listed in
`configs/current.json`; consumers should not select a report by modification time or version-looking filename.

The evidence DAG in `scripts/evidence_pipeline.py` is the only supported generation order for current reports.
Superseded reports and raw campaign outputs are retained in Git history or external run storage, not copied into this
tree. Reports bound by a protocol, trajectory digest, or source hash remain immutable until explicitly recertified.

The active first-paper entry point is `workstreams/arxiv_v1/FIRST_PAPER_TODOLIST.md`; the short
orientation page is `workstreams/arxiv_v1/README.md`. The retired Work I task matrix, claims,
integration queue, story handoffs and review files are historical records and must not be used to
claim new work or restore old ownership. Some remain at their original paths because frozen reports
or legacy tools refer to them.

The former master plan, readiness/provenance/incident audits and related-work audit are legacy
evidence inputs, not current execution plans. The machine-readable historical experiment accounting
remains at `workstreams/arxiv_v1/reports/experimental-intelligence-experiment-ledger-v0.1.json`.
The active Work II execution surface is `workstreams/flagship_tasks/WORK_II_TODOLIST.md`. Superseded
plans, smoke notes, stopped extensions, and editorial snapshots are available from Git history rather
than kept as competing entry points in the working tree.

The current Work II manuscript draft is `paper/prior_discovery_manuscript.md`, with its display plan
in `paper/prior_discovery_display_items.md`. The next real-provider gate is the three-arm current-method
qualification experiment recorded at
`workstreams/flagship_tasks/experiments/work-ii-current-method-qualification-triplet.md`; the exact
non-secret route, pricing and budget inputs needed to authorize it are summarized in
`workstreams/flagship_tasks/reports/work-ii-formal-launch-decision-brief.md`.
