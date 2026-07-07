# Safety And Cost

Reward, score, cost, and leaderboard score are different channels.

- `reward`: online scalar returned by Gymnasium `step`.
- `score`: visible or estimated task performance from the current observation.
- `leaderboard_score`: final-assay score used for official ranking.
- `cost`: safe-RL style constraint signal.

`info` includes:

```python
info["cost"]
info["cost_components"]
info["constraint_budget_remaining"]
```

Cost components are:

- safety risk;
- high cost;
- precondition failure;
- constitution failure.

Safety-aware tasks use the task-level `safety_limit`, not a hard-coded global
threshold.
