# Benchmark Paper Artifact

The paper artifact should be reproducible from a clean checkout.

Recommended structure:

```text
artifact/
  README.md
  environment.yml or requirements.txt
  tasks/
  submissions/
  results/
  figures/
  notebooks/
```

Minimum commands:

```bash
chemworld tasks list
chemworld suite --task reaction-optimization-standard --agent random
chemworld suite --task reaction-optimization-standard --agent gp_bo
chemworld leaderboard --results runs/suite/*/results/*.json
chemworld submission validate submissions/example
```

The artifact should report mean score, safety-aware score, sample efficiency,
public/private gap where applicable, and mechanism explanation rubric scores
when used.

