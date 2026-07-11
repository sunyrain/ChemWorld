# Local Eval Server

> Security boundary: the bundled evaluator uses trusted local subprocesses. It is not a
> sandbox and must not execute untrusted third-party submissions without an external
> container/runtime that disables network access and limits filesystem and process privileges.

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

The teacher now constructs reset/act/update messages from explicit public-field allowlists,
recursively rejects hidden/debug/private-task-text/traceback/absolute-path content, limits
message and response sizes, and validates student responses against the request-specific JSON
schema. Student tracebacks remain teacher-private and are reduced to a generic protocol error.
The world/evaluation seed is not included in public task metadata; student randomness receives
a separately configured public agent seed (zero by default).

These controls minimize the JSONL interaction surface; they do not change the threat model.
The local subprocess can still access host resources allowed by the operating system. Unknown
third-party code requires an external no-network, read-only, low-privilege container with CPU,
memory, PID, and wall-time limits.

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
