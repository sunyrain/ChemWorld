# Script entry points

The `scripts/` directory contains executable maintenance, validation, and experiment entry points for the active
repository surface. Superseded runners belong in Git history rather than beside current implementations.

- `audit_*.py`: read-only runtime and contract validation.
- `run_*.py`: active experiment, evaluation, or focused release entry points.
- `build_*.py`: deterministic builders for current artifacts.

Resolve active runtime and protocol paths through `configs/current.json`; do not infer currency from a `vnext` name
or a larger version suffix.

Static S0 entry points require explicit `--protocol` paths, and LLM runs also require an explicit
`--llm-methods` path. There is no implicit development protocol or electrochemical workflow mode. Frozen formal
inputs remain immutable; historical development protocols explicitly declare `adaptive_two_stage`, while current
electrochemical S0 protocols explicitly declare `static_single_stage`. Use
`resume_static_optimization_s0.py` for an audited continuation. One-off qualification finalizers do not belong on
the active script surface.

`run_scientific_adaptation_shakedown.py` is retained only to reproduce historical development diagnostics. It
requires explicit protocol and method inputs and is not an active experiment roadmap. Current mechanism-adaptation
work follows the staged v0.3 protocol and must restore the current-source Gate A binding before Participant
Gates B–E; the completed fixed-world S0 campaigns remain a separate evidence track.

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
