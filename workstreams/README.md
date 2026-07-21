# Workstream evidence

Workstream reports are evidence records, not a second source tree. Current entry points are listed in
`configs/current.json`; consumers should not select a report by modification time or version-looking filename.

Each `reports/archive/` directory contains superseded, orphaned, or exploratory diagnostics retained for provenance.
Archived reports are excluded from current claims unless a document cites them explicitly. Moving a report into an
archive changes its repository role, not its original result, so its contents remain unchanged.

Reports bound by a protocol, release manifest, trajectory digest, or source hash are immutable. Raw runs and provider
receipts remain outside Git by default and require a manifested retention decision before cleanup.
