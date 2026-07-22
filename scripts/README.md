# Script entry points

The `scripts/` directory contains executable maintenance, validation, and experiment entry points for the active
repository surface. Superseded runners belong in Git history rather than beside current implementations.

- `audit_*.py`: read-only runtime and contract validation.
- `run_*.py`: active experiment, evaluation, or focused release entry points.
- `build_*.py`: deterministic builders for current artifacts.

Resolve active runtime and protocol paths through `configs/current.json`; do not infer currency from a `vnext` name
or a larger version suffix.

Use `python scripts/evidence_pipeline.py --refresh` to regenerate the current deterministic evidence in dependency
order, and `python scripts/evidence_pipeline.py --check` to reject stale bindings without rewriting files. Do not run
individual current-report generators and then update parent ledgers by hand.

Mechanism adaptation v0.2.1 has one staged entry point plus a required design audit:

- `audit_mechanism_adaptation_design.py` rejects hidden targets that are not publicly selectable or not covered by
  the frozen action library;

- `run_mechanism_adaptation_v0_2.py --stage gate-a` runs the environment-only identifiability certificate and never
  calls an external model;
- `run_mechanism_adaptation_v0_2.py --stage campaign` executes complete changed/no-change pairs, writes one durable
  summary per arm, and supports `--resume`. This stage requires an explicitly supplied provider environment.

When common logic is worth consolidating, update the active entry point, its configuration, and focused tests in the
same change. Keep raw campaigns and provider responses outside Git.
