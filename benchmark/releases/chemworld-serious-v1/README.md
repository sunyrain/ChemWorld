# ChemWorld Serious Benchmark v1

This directory is the public evidence bundle for `chemworld-serious-v1`.

- `manifest.json` freezes versions, task hashes, seeds, agents, and evidence digests.
- `baseline_summary.json` reports all official baselines per task.
- `benchmark_validation.json` contains the machine-readable empirical gate.
- `response_surface_audit.json` records deterministic response-surface probes.

Validate an installed source tree with:

```bash
python scripts/check_frozen_benchmark.py
```

Scores compare experimental strategies inside ChemWorld. They are not predictions of
real chemical yields, material properties, or plant safety.
