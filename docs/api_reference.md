# API Reference

This page summarizes the public APIs intended for external benchmark users.

## Environment

```python
import gymnasium as gym
import chemworld

env = gym.make(
    "ChemWorld",
    task_id="reaction-optimization-standard",
    seed=0,
)
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(action)
```

Task-free construction is mainly useful for development. Benchmark claims
should use `task_id`.

## Tasks

```python
from chemworld.tasks import get_task, list_tasks

task = get_task("reaction-optimization-standard")
print(task.to_dict())
```

Each task records `world_law_id`, scenario id, initial-state id, allowed
operations, allowed instruments, observation policy, termination policy, and
success metrics.

## Wrappers

```python
from chemworld.wrappers import ActionMaskWrapper, SafetyCostWrapper
```

`ActionMaskWrapper` adds task-aware `valid_operations`, `action_mask`, and
invalid-reason summaries. `SafetyCostWrapper` adds safe-RL style cost signals
without changing the Gymnasium five-tuple return.

## Agents

Agents implement:

```python
reset(task_info, seed)
act(history)
update(action, observation, reward, info)
```

## Trajectories

Use `TrajectoryLogger` for JSONL logs and `validate_records` before evaluation.

```python
from chemworld.data.logging import load_jsonl
from chemworld.data.validation import validate_records
from chemworld.eval.metrics import evaluate_records

records = load_jsonl("run.jsonl")
validate_records(records)
result = evaluate_records(records)
```

