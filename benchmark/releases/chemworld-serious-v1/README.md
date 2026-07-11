# ChemWorld Serious v1 (historical candidate)

This directory preserves the candidate evidence bundle created for the earlier World Law v0.3
and task contract 0.5. It is retained for provenance and regression testing; it is not the
current World Law v0.4 release and must not be presented as a validated leaderboard.

- `manifest.json` records versions, task hashes, seeds, methods, and artifact digests.
- `baseline_summary.json` stores the historical baseline summary.
- `benchmark_validation.json` stores the gate used at the time.
- `response_surface_audit.json` stores deterministic response-surface probes.

Validate bundle integrity with:

```bash
python scripts/check_frozen_benchmark.py
```

Integrity only proves that the historical files still match their manifest. Scores describe
strategies inside the matching ChemWorld version and are not predictions of real yields,
material properties, process performance, or safety.
