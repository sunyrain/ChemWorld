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
- Public/private world split behavior is documented.
- Submission bundle validation succeeds on sample artifacts.
- Replay verification succeeds on all official trajectories.

## Data And Ethics

- Human data is anonymized before release.
- Dataset cards describe provenance, consent, and limitations.
- Private-eval parameters and salts are not committed.

## Paper Artifact

- README includes install, run, evaluate, and verify commands.
- Results include platform version, commit hash, seeds, and dependency file.
- Figures and tables can be regenerated from local artifacts.

