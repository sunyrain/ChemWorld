# Release Checklist

Use this checklist before a public benchmark release or paper artifact freeze.

## Code Gate

```bash
python -m ruff check .
python -m mypy src/chemworld
python -m pytest
python -m mkdocs build --strict
```

## Environment Self-Consistency Gate

```bash
python scripts/audit_environment_consistency.py --tasks all --seeds 0 1 2
```

Required result:

- zero replay failures;
- zero constitution failures;
- zero invalid smoke steps;
- zero spectra failures;
- documented warnings only for known design risks.

## Documentation Gate

- Homepage points to the current architecture, task registry, benchmark
  protocol, tutorial, and audit pages.
- MkDocs navigation is grouped by reader goal.
- `Current Progress` reflects the current branch, not historical migration
  notes.
- Task docs clearly distinguish `campaign` and `single_experiment`.
- Task cards are generated from the registry and are not hand-written copies.
- Known proxy/lite/reference-validated maturity boundaries are visible.
- `mkdocs build --strict` succeeds.
- UTF-8 scan has no obvious mojibake markers.

## Benchmark Contract

- Built-in tasks are listed and documented.
- Task cards include scenario, split, budget, seed policy, episode mode,
  allowed operations, instruments, metrics, and maturity metadata.
- Broad exploratory task profiles are explicitly marked as exploratory and
  proxy-allowed.
- Release tasks expose only operations needed by their task profile.
- Submission bundle validation succeeds on sample artifacts.
- Replay verification succeeds on all official trajectories.

## Baseline Artifacts

Generate per-task baseline tables:

```bash
chemworld baselines report \
  --tasks reaction-optimization-standard reaction-to-distillation \
  --agents random scripted_chemistry gp_bo safe_gp_bo \
  --seeds 0 1 2 \
  --output-dir runs/baseline_report
```

The frozen report must include:

- command used;
- platform version;
- commit hash;
- dependency metadata;
- seeds;
- agent manifests;
- task maturity metadata;
- mean, standard error, safety/cost metrics, and confidence intervals when
  available.

## Private Eval

- Private salts and hidden parameters are not committed.
- Reported private-eval results have a signed maintainer artifact.
- The artifact stores salt hash and signature, not the secret salt.

## Data And Ethics

- Human data is anonymized before release.
- Consent and data-use boundaries are documented.
- Dataset cards describe provenance, task ids, seeds, agent manifests,
  limitations, license, and privacy status.

## Paper Artifact

```bash
chemworld artifact create --output-dir artifact/release
```

The paper artifact should include:

- README with install, run, evaluate, and verify commands;
- schema snapshots;
- task cards;
- baseline tables;
- dataset examples;
- self-consistency audit summary;
- reproduction scripts;
- platform version, commit hash, seeds, and dependency file.
