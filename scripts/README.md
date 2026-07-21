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

When common logic is worth consolidating, introduce it with a new protocol/source version. Do not silently refactor a
runner already bound by a formal or diagnostic artifact hash.
