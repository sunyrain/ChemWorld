# Local Eval Machine

This page describes how to run ChemWorld when one physical machine acts as the
teacher evaluation server and student projects are deployed on the same host.

The recommended boundary is:

```text
teacher-side runner owns ChemWorld env.reset/env.step
student-side process only returns actions
```

Students should not run `private-eval` themselves. The evaluator starts a
student process, sends sanitized task information and observations through JSON
lines, receives actions, then writes trajectories, metrics, replay verification,
and leaderboard files.

## Directory Layout

The reference implementation lives in:

```text
local_eval_server/
├── teacher_side/
│   ├── eval_machine.py
│   └── eval_config.demo.json
└── student_side/
    ├── student_agent_runtime.py
    └── team_alpha_submission/
```

`team_alpha_submission` is a sample student folder. In a real course, each team
submits a similar folder with:

- `manifest.json`;
- `agent.py`;
- `requirements.txt` or another dependency file;
- optional prompt/cache/explanation files.

## One-Command Demo

```bash
python local_eval_server/teacher_side/eval_machine.py \
  --workspace runs/local_eval_machine \
  demo
```

For a tiny smoke run:

```bash
python local_eval_server/teacher_side/eval_machine.py \
  --workspace runs/local_eval_machine \
  demo \
  --tasks reaction-to-assay \
  --seeds 0
```

The output workspace contains:

```text
runs/local_eval_machine/
├── teacher_private/eval_config.json
├── submissions/accepted/<team_id>/
├── runs/<run_id>/<team_id>/
│   ├── trajectories/*.jsonl
│   ├── results/*.json
│   ├── verify/*.json
│   └── logs/*.log
└── published/
    ├── <run_id>_leaderboard.csv
    └── <run_id>_leaderboard.json
```

## Manual Evaluation Flow

```bash
python local_eval_server/teacher_side/eval_machine.py \
  --workspace runs/local_eval_machine \
  init-demo

python local_eval_server/teacher_side/eval_machine.py \
  --workspace runs/local_eval_machine \
  validate

python local_eval_server/teacher_side/eval_machine.py \
  --workspace runs/local_eval_machine \
  run \
  --tasks reaction-to-assay \
  --seeds 0

python local_eval_server/teacher_side/eval_machine.py \
  --workspace runs/local_eval_machine \
  aggregate \
  --run-id demo_eval
```

## Security Model

This implementation simulates Docker isolation with independent folders and a
separate student subprocess. It removes private environment variables before
starting student code, but it is not a hard sandbox if students have the same
host account and filesystem permissions as the evaluator.

For a real high-stakes leaderboard, replace the subprocess launcher with Docker
or another sandbox:

- mount student code read-only;
- disable network unless explicitly allowed;
- limit CPU, memory, and wall time;
- keep `teacher_private/` outside the container mount;
- run private evaluation only after the submission deadline.

The protocol is already shaped so that the replacement is localized: swap the
student process command while keeping the teacher-side ChemWorld runner.
