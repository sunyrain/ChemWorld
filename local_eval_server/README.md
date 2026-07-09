# Local Eval Server

This directory simulates a two-sided ChemWorld evaluation machine:

- `teacher_side/`: owns ChemWorld, private salts, seeds, trajectories, metrics,
  replay verification, and leaderboard publication.
- `student_side/`: contains the runtime that would be placed in a student Docker
  image plus a small example submission.

The important boundary is:

```text
teacher runner owns env.reset/env.step
student process only receives sanitized task_info/history/observation and returns action
```

## Demo

From the repository root:

```bash
python local_eval_server/teacher_side/eval_machine.py \
  --workspace runs/local_eval_machine \
  demo
```

This creates:

```text
runs/local_eval_machine/
├── teacher_private/eval_config.json
├── submissions/accepted/team_alpha/
├── runs/demo_eval/team_alpha/
│   ├── trajectories/
│   ├── results/
│   ├── verify/
│   └── logs/
└── published/
    ├── demo_eval_leaderboard.csv
    └── demo_eval_leaderboard.json
```

## Manual Flow

```bash
python local_eval_server/teacher_side/eval_machine.py --workspace runs/local_eval_machine init-demo
python local_eval_server/teacher_side/eval_machine.py --workspace runs/local_eval_machine validate
python local_eval_server/teacher_side/eval_machine.py --workspace runs/local_eval_machine run --tasks reaction-to-assay --seeds 0
python local_eval_server/teacher_side/eval_machine.py --workspace runs/local_eval_machine summarize --run-id demo_eval
```

For a real course, replace `team_alpha_submission` with student folders under
`submissions/incoming/`, replace the demo private salt, and run private
evaluation only after the submission deadline.
