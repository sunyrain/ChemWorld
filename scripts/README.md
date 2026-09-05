# Script entry points

The `scripts/` directory contains current commands and retained reconstruction tools. The workstream
TODO and bound experiment note determine which command is appropriate; a retained runner does not
authorize a new experiment or restore a historical qualification gate.

- `audit_*.py`: read-only runtime and contract validation.
- `run_*.py`: experiment, evaluation, or focused release entry points; some serve frozen protocols.
- `build_*.py`: deterministic artifact builders; current and historical scope must remain distinct.

## Current research paths

| Work | Entry points | Authority |
| --- | --- | --- |
| First-paper release | `paper/tools/build_arxiv_release.py` | First-paper TODO and canonical manuscript |
| Work II M0/M1 development | `run_work_ii_factorial.py` | Development experiment note; separate from formal results |
| Work II M1 formal replication | `run_work_ii_factorial_replication.py` | Completed M1 note/protocol; no automatic rerun |
| Work II M3 information separation | `run_work_ii_m3_portability.py` | Completed M3 note/protocol; preserves sealed M1 source reuse |
| Work II publication | `paper/figures/prior-discovery/render_prior_discovery_figures.py`, two current paper builders | Current evidence bindings and [paper guide](../paper/README.md) |

M1/M3 are complete. The next mechanism-matching/new-condition block is design-only in the
[experiment matrix](../workstreams/flagship_tasks/WORK_II_EXPERIMENT_MATRIX.md).
The remaining sections describe retained protocol families, not a current experiment queue.

## Retained protocol and release tools

Resolve active runtime and protocol paths through `configs/current.json`; do not infer currency from a `vnext` name
or a larger version suffix.

Static S0 entry points require explicit `--protocol` paths, and LLM runs also require an explicit
`--llm-methods` path. There is no implicit development protocol or electrochemical workflow mode. Frozen formal
inputs remain immutable; historical development protocols explicitly declare `adaptive_two_stage`, while current
electrochemical S0 protocols explicitly declare `static_single_stage`. Use
`resume_static_optimization_s0.py` for an audited continuation. One-off qualification finalizers do not belong on
the active script surface.

`run_scientific_adaptation_shakedown.py` is not an active experiment roadmap. It remains temporarily as the
provider-free fixture producer for focused receipt replay, tamper, method-failure, and missing-only-resume tests;
new experiments use the staged mechanism runner. Retire the shakedown runner once that runner exposes an equivalent
mock seam instead of copying the historical implementation into tests. Current mechanism-adaptation development
stabilizes the method, execution, and statistical contracts with focused functional and scientific checks. Rebuild
the current-source Gate A chain once, only after the execution surface is stable and release freeze is authorized;
the completed fixed-world S0 campaigns remain a separate evidence track.

`scripts/evidence_pipeline.py` belongs to current-artifact maintenance and release freeze. Use `--refresh` only after
the execution-relevant surface is stable and the relevant release/current-artifact update is authorized; use
`--check` for that same integration boundary. Neither command is a prerequisite for ordinary feature development,
focused tests, or labelled development experiments. Do not repair stale historical bindings after every edit, and
do not run individual current-report generators before updating parent ledgers by hand.

Mechanism adaptation v0.3 has one staged entry point plus a required design audit. The calibrated track guarantees
an old-world reference opportunity and certifies relation coverage before scoring change attribution; static
initial-world identification and early uncalibrated nonstationarity are separate, non-gating tracks:

- `audit_mechanism_adaptation_design.py` rejects hidden targets that are not publicly selectable or not covered by
  the frozen action library;

- `run_mechanism_adaptation.py --stage gate-a` runs the environment-only identifiability certificate and never
  calls an external model;
- `run_mechanism_adaptation.py --stage campaign` executes complete changed/no-change pairs, writes one durable
  summary per arm, and supports `--resume`. This stage requires an explicitly supplied provider environment.

When common logic is worth consolidating, update the active entry point, its configuration, and focused tests in the
same change. Keep raw campaigns and provider responses outside Git.
