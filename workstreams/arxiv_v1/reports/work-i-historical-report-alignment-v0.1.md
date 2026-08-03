# Work I historical report alignment

Status: **target_reports_aligned_global_refresh_queued**  
Receipt SHA-256: `301a3316654c38a3b273db57cdebb589026f90683a92b8e3da5632a5e0d3ced1`

Both historical generated reports are tracked, byte-identical to their Git index
entries, and selected by matching content hashes in the current evidence DAG.

| Acceptance item | Verified value |
| --- | ---: |
| Runtime-domain candidates | 237 |
| Validator-valid candidates | 235 |
| Runtime-committed executions | 235 |
| Runtime-domain findings | 0 |
| Public-boundary probes passed | 35/35 |
| Semantic-invariance paired runs | 12/12 |

The runtime report's embedded source commit is retained as historical generation
provenance. It is not used as the current selector; current identity is bound by the
report path and SHA-256 in `configs/current.json`.

No historical report, current registry, global evidence DAG, or release manifest was
rewritten by W1-M03. The target reports have no unexplained byte or binding drift.

The repository-wide evidence checker already reported a stale executable-source
fingerprint on the claimed main baseline. That explained integration drift is queued
for coordinator-owned W1-M05/W1-M06 work; it is not a target-report mismatch and is
outside W1-M03's hot-file authority.
