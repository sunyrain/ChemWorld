# W1-V08 formal policy-control execution handoff

## Outcome

The frozen Work I known-policy matrix completed successfully under the W1-V07-qualified apparatus. One formal launch produced 30 primary campaigns and 180 closed primary lifecycles. The same-identity reliability retest produced 30 campaigns and 180 closed lifecycles outside the primary estimand. Provider calls remained zero. The independent V06 audit passed all 12 gates.

This handoff records execution and audit evidence only. W1-V09 owns scientific interpretation and reporting.

## Frozen inputs and execution

- Base commit: `716ee1ff6a5c32d987ae7cdcc6dfda9606ef5b8c`
- Branch: `work1/w1-v08-formal-policy-controls`
- Worktree: `../ChemWorld-W1-V08`
- Qualification receipt: `configs/benchmark/work_i_policy_control_formal_qualification_receipt_v0.1.json`
- Qualification receipt SHA-256: `bb3b6170e654cd74122ff719ac9a01d55bc163e8f2ca57046245139d9d3c60fa`
- Execution apparatus SHA-256: `e56f897906bfc2a345ba5d667ae08d87b07b3e886cf42a6cfbfb8383dbedb8d0`
- Runtime: CPython 3.11.15, NumPy 2.2.6 wheel `numpy-2.2.6-cp311-cp311-win_amd64.whl`, SciPy 1.17.1 wheel `scipy-1.17.1-cp311-cp311-win_amd64.whl`, `win-amd64`
- `uv.lock` SHA-256: `e79dbec48a50730499e96806b0ae7ccd989eaf67693009143b55901b6e2fc9b7`
- Formal launches: exactly one

```powershell
uv run --isolated --frozen --python 3.11.15 python scripts/run_work_i_policy_controls.py --config configs/benchmark/work_i_policy_control_matrix_v0.1.json --execute --allow-formal-execution --qualification-receipt configs/benchmark/work_i_policy_control_formal_qualification_receipt_v0.1.json --output-root workstreams/arxiv_v1/reports/work-i-policy-control-formal-v0.1
```

No source, configuration, seed, threshold, protocol, estimand, stopping rule, acceptance rule, or shared hot file was changed. No result was retuned, replaced, or regenerated after the formal launch.

## Immutable evidence

- Terminal manifest: `workstreams/arxiv_v1/reports/work-i-policy-control-formal-v0.1/matrix_manifest.json`
- Manifest semantic SHA-256: `d15c7af5084a96d579fa87de55e0177d3eb2026dc5cb651042c516251751cdcc`
- Manifest file SHA-256: `0c627f679835299d657938a28899413b596ff01aaf344290658a057252e3433e`
- Manifest bytes: 33,500
- Progress record: `workstreams/arxiv_v1/reports/work-i-policy-control-formal-v0.1/matrix_progress.json`
- Progress semantic SHA-256: `b3c4f143139041dd5c70e7d24441f46712caa7b136da9084178beb6ee93db906`
- Progress file SHA-256: `0074f33e3678685d945fcb5e27ae5a45c2ca4b535fd49b90d0d9f2d8c96f68b3`
- Progress bytes: 25,086
- Raw evidence commit: `55b7b3c1908a6bec8ee3dbc4b5e3efcbd3599ab6`

The progress self-hash closed independently. Its accepted-bundle count and ordered list matched the terminal manifest and covered the full canonical 30-cell prefix. Every bundle's semantic hash, file hash, byte count, lifecycle counts, original/retest identity, component bindings, and provider-call count validated. The terminal manifest recorded `retest_in_primary_estimand: false`.

The formal output contains 32 files totaling 40,045,374 bytes (38.190 MiB). The largest file is `bundles/cell-30-world-0004-anonymous-nominal-measure-then-threshold.json` at 2,206,614 bytes (2.104 MiB), below the 50 MiB hard stop.

## Audit

```powershell
uv run --isolated --frozen --python 3.11.15 python scripts/audit_work_i_policy_validity.py --manifest workstreams/arxiv_v1/reports/work-i-policy-control-formal-v0.1/matrix_manifest.json --output workstreams/arxiv_v1/reports/work-i-policy-control-formal-audit-v0.1.json
uv run --isolated --frozen --python 3.11.15 python scripts/audit_work_i_policy_validity.py --manifest workstreams/arxiv_v1/reports/work-i-policy-control-formal-v0.1/matrix_manifest.json --output workstreams/arxiv_v1/reports/work-i-policy-control-formal-audit-v0.1.json --check
```

- Audit: `workstreams/arxiv_v1/reports/work-i-policy-control-formal-audit-v0.1.json`
- Audit semantic SHA-256: `661d42ec74993200750f040bb4d12f4403fbc9c2c4b78aed5a9e6cc2b0c6be95`
- Audit file SHA-256: `d4c539048dd4463b5e281fe7bec014fd11e87809057b32c34a3d99b08f900b55`
- Audit bytes: 214,682
- Audit commit: `7e3337b7cbcb83248a88dceef31bcb635468d680`
- Result: `passed`; 12 of 12 gates true; `formal_execution_performed_by_auditor: false`
- Threshold branch counts: 28 final assays and 32 discards, satisfying the non-degeneracy gate

The generator and byte-exact `--check` produced the same audit. Counts were 30 campaigns, 180 closed primary lifecycles, and zero provider calls.

## Completed-output resume validation

The completed output was invoked once with the frozen formal command plus `--resume`. It returned `status: complete` with the same manifest semantic SHA-256 and counts, without entering another formal execution. Before and after snapshots both contained 32 files and 40,045,374 bytes; comparison of every relative path, byte count, and file SHA-256 found zero changes.

## Validation notes

- Formal manifest, progress, bundles, counting rules, original/retest exclusion, source bindings, resource ledgers, matched-arm gates, provider-call counts, hashes, and byte sizes: passed.
- V06 audit generation and byte-exact check: passed.
- Completed-output `--resume` no-op: passed with zero file mutations.
- `git diff --check`: passed before handoff.
- An initial custom validation probe looked for the apparatus hash at the manifest top level; inspection showed the frozen schema correctly stores it at `dependency_bindings.execution_apparatus_sha256`. The corrected read-only probe passed. No output was changed and the formal command was not rerun.

