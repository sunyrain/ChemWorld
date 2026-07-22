# ChemWorld current roadmap

Updated: 2026-07-22

This file lists only current decisions and executable next steps. Historical plans and negative
runs remain available through Git history and versioned reports; they are not repeated here.

## Current project position

- ChemWorld is an Agent capability evaluation and training environment for physical-chemistry
  world-model behavior. It does not train or update hosted model weights during evaluation.
- The principal scientific question is mechanism adaptation: can an Agent use physical-chemistry
  feedback to detect a hidden-law change, identify its operational family, choose diagnostic
  interventions, and recover performance under a fixed experiment budget?
- The runtime/backend candidate validates against its current contract. A clean-tree release
  attestation remains a separate release step.
- The general formal benchmark remains sealed at method freeze until its declared method artifacts
  exist and pass their own gates. Its 0/6 readiness state must not block environment-side mechanism
  identifiability work.
- There is no active NCS manuscript. The 2026-07-21 working draft is historical material under
  `paper/archive/ncs-working-draft-2026-07-21/`.

## Active target

### 1. Mechanism adaptation v0.2.1

- [x] Freeze the six-gate protocol and paired changed/no-change matrix.
- [x] Implement the leakage-resistant mechanism-distribution Agent contract.
- [x] Implement a resumable end-to-end runner for paired DeepSeek campaigns.
- [x] Freeze a Gate A plan over real public environment observations.
- [x] Add a fail-closed action/intervention/observation design audit. The engine supports `catalyst`, `solvent`, and
  `electrolyte_profile`; each task must still expose at least two legal choices and the Gate A library must cover all
  moved indices.
- [x] Replace the unreachable electrochemical `solvent` target with `electrolyte_profile`; archive the v0.2 Gate A
  result as invalid design evidence.
- [x] Rerun Gate A v0.2.1. Electrochemical families are 30/30 at budget four. Overall active-oracle accuracy is 0.895
  (Wilson lower bound 0.846), but the Gate remains failed because reaction no-change, rate-law, and material-family
  recall lower bounds remain below 0.70.
- [ ] Diagnose reaction-task overlap under a newly versioned plan without changing the frozen v0.2.1 result. Compare
  shared-world nuisance models, relational catalyst pairs, and budgets 4/6/8 before selecting v0.2.2.
- [ ] Run a minimal public provider pilot only after a newly versioned Gate A passes.
- [ ] Implement/report Gate 0 integrity and leakage evidence for completed provider trajectories.
- [ ] Run paired no-change detection analysis for Gate B.
- [ ] Run local-prefix feedback response plus paired campaign utility for Gate C.
- [ ] Run frozen/open-loop/adaptive/oracle recovery comparisons for Gate D.
- [ ] Report autonomous and assisted scientific scores separately for Gate E.

Gate A interpretation is strict: a pass establishes that the environment is identifiable by the
budget-matched evaluator-side oracle. It does not establish that DeepSeek or another Agent discovers
the mechanism. A failure blocks Agent-level mechanism-discovery interpretation until the task design
or budget is revised in a newly versioned protocol.

### 2. Live LLM v0.4.11

- [x] Use v0.4.11 as the only current live-LLM development target in code, current registry, and
  method-freeze inputs.
- [ ] Keep older v0.4.8–v0.4.10 reports immutable as source-bound diagnostics.
- [ ] Do not resume older caches into v0.4.11.
- [ ] After Gate A, decide whether to spend provider budget on the complete six-cell candidate
  screen or remove live LLMs from the general formal method set.

### 3. Evidence and release hygiene

- [x] Use `scripts/evidence_pipeline.py` as the unique current-evidence DAG generator/checker.
- [x] Remove the archived NCS manuscript from the current evidence DAG.
- [x] Testing policy: audit only the code paths and contracts affected by a change. Do not run the complete repository
  test suite unless explicitly requested.
- [x] Refresh the DAG after Gate A v0.2.1; 28 nodes pass with zero stale bindings.
- [x] Run full-repository Ruff and 63 high-relevance mechanism/runtime/evidence tests. The complete pytest suite did
  not finish within either the 15-minute coverage or 20-minute no-coverage execution limit and returned no failure
  summary; treat full-suite status as incomplete, not passed.
- [ ] Commit the integrated change on a clean tree, regenerate source-attested backend artifacts,
  and only then issue a clean release attestation.

## Commands

```powershell
# Environment-only identifiability certificate; no provider calls
.\.venv\Scripts\python.exe scripts\run_mechanism_adaptation_v0_2.py --stage gate-a

# One complete changed/no-change public pilot pair; requires DEEPSEEK_API_KEY
.\.venv\Scripts\python.exe scripts\run_mechanism_adaptation_v0_2.py `
  --stage campaign --pair-limit 1 --resume

# Regenerate and verify current evidence
.\.venv\Scripts\python.exe scripts\evidence_pipeline.py --refresh
.\.venv\Scripts\python.exe scripts\evidence_pipeline.py --check
```

## Claim boundary

Until all required mechanism gates pass, allowed language is limited to benchmark/environment
capability, protocol completeness, identifiability diagnostics, and explicitly labeled development
results. Do not claim reliable mechanism discovery, formal model ranking, or publication readiness.
