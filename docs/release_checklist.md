# Release Checklist

Use this checklist before a public benchmark release.

## Code

- `python -m ruff check .`
- `python -m mypy src/chemworld`
- `python -m pytest`
- `mkdocs build --strict`

## Benchmark Contract

- Built-in tasks are listed and documented.
- Official baselines run on public tasks.
- `chemworld baselines report` has generated task-specific baseline tables.
- Public/private world split behavior is documented.
- Private-eval results, if reported, have a signed artifact from
  `chemworld private-eval sign`.
- Submission bundle validation succeeds on sample artifacts.
- Replay verification succeeds on all official trajectories.

## Data And Ethics

- Human data is anonymized before release.
- Dataset cards describe provenance, consent, and limitations.
- Private-eval parameters and salts are not committed.

## Paper Artifact

- README includes install, run, evaluate, and verify commands.
- `chemworld artifact create` has produced `artifact_summary.json`, task cards,
  schema snapshots, baseline tables, dataset examples, and reproduction scripts.
- Results include platform version, commit hash, seeds, and dependency file.
- Figures and tables can be regenerated from local artifacts.

