# Benchmark Paper Artifact

The paper artifact should be reproducible from a clean checkout.

Generate a local artifact with:

```bash
chemworld artifact create \
  --output-dir artifact/release \
  --tasks reaction-to-assay \
  --agents scripted_chemistry \
  --seeds 0
```

For a release, expand `--tasks`, `--agents`, and `--seeds` to the full public
benchmark suite. The command creates this structure:

```text
artifact/
  README.md
  metadata.json
  artifact_summary.json
  scripts/
    reproduce_public_artifact.ps1
  tasks/
    task_cards.json
    scenario_cards.json
    world_law.json
  schemas/
    action_schema.json
    recipe_schema.json
    trajectory_schema.json
  baseline_report/
    baseline_results.json
    baseline_leaderboard.json
    baseline_report.json
  dataset_examples/
    *_example.jsonl
    *_example_dataset.jsonl
    dataset_card.json
```

Minimum commands:

```bash
chemworld tasks list
chemworld baselines report --tasks reaction-optimization-standard --agents random
chemworld artifact create --output-dir artifact/release
chemworld submission validate submissions/example
```

The artifact should report mean score, safety-aware score, sample efficiency,
public/private gap where applicable, and mechanism explanation rubric scores
when used.

