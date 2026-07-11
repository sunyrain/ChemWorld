# ChemWorld World Law v0.4 backend candidate

This directory records the World Law v0.4 task contracts, scenario cards, runtime provider
graph, integration audit, readiness state, and deterministic core golden summaries. It is a
backend candidate, not a frozen benchmark release or leaderboard evidence package.

`benchmark_claim_allowed` remains `false`. A validated release additionally requires a
pre-registered objective-and-constraint method protocol, full classical/RL/LLM evidence,
mechanism-family and private-world generalization, a searched reference portfolio, complete
replay artifacts, and independent reproduction.

Rebuild and inspect the backend bundle with:

```powershell
python scripts/audit_vnext_runtime_integration.py
python scripts/update_golden_trajectories.py
python scripts/build_vnext_backend_candidate.py
```

The manifest binds every generated artifact by SHA-256. Passing its structural checks does not
authorize a scientific benchmark claim.
