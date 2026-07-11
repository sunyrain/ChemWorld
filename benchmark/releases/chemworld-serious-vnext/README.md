# ChemWorld v0.4 backend candidate

This directory is a backend-only candidate, not a frozen benchmark release and not a
leaderboard evidence package. It records the World Law v0.4 task contracts, scenario cards,
runtime provider graph, integration audit, readiness state, and deterministic core golden
summaries after WF-110.

The bundle intentionally contains no baseline conclusions. `benchmark_claim_allowed` is
`false`: validity/power analysis, generalization/security evaluation, resource-matched method
protocols, and new multi-seed experiments must be completed before this backend can become a
frozen benchmark release. The existing `chemworld-serious-v1` directory remains unchanged as
historical evidence for the earlier World Law.

Rebuild the machine-generated files with:

```powershell
python scripts/audit_vnext_runtime_integration.py
python scripts/update_golden_trajectories.py
python scripts/build_vnext_backend_candidate.py
```

Verify all artifact hashes against `manifest.json`. The manifest deliberately describes a
candidate rather than pretending that an uncommitted source tree is a frozen release commit.
