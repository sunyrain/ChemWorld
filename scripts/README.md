# Script entry points

The `scripts/` directory contains both current maintenance commands and source-bound historical runners. Similar
files are not automatically duplicates: several reports bind the exact runner bytes in their evidence hashes.

- `manage_claims.py`: validate, create, and close repository work claims.
- `audit_*.py`: read-only contract, integrity, and evidence checks.
- `run_*.py`: versioned experiment or preflight entry points; inspect the referenced config and report before use.
- `build_*.py`: deterministic documentation, paper, or release builders.

Resolve the current runtime and protocol paths through `configs/current.json`. A filename containing `vnext` or a
larger numeric suffix does not by itself make a script current. Historical runners should be removed only after their
reports, manifests, and replay requirements have a documented migration path.

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

The former NCS audit is retained with its manuscript under `paper/archive/`; it is not a current maintenance command
or an evidence-DAG dependency.

When common logic is worth consolidating, introduce it with a new protocol/source version. Do not silently refactor a
runner already bound by a formal or diagnostic artifact hash.
