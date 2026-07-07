# Demos

The `examples/` directory contains small scripts that exercise the current
research platform without requiring a web service or external API.

## Manual Event Sequence

```bash
python examples/demo_manual_event_sequence.py
```

This runs one explicit reactor workflow:

- add solvent;
- add reagent;
- add catalyst;
- heat with a stirring speed;
- take an HPLC measurement;
- wait;
- terminate;
- run a final assay.

It prints the public observation after each operation plus constraint flags.

For the downstream workflow, run the `reaction-to-purification` task with the
scripted chemistry baseline:

```bash
chemworld run --task reaction-to-purification --agent scripted_chemistry
```

## Baseline Comparison

```bash
python examples/demo_compare_baselines.py
```

This runs a tiny local suite for `random`, `scripted_chemistry`, and `lhs` on
`public-test` and `private-eval`, then prints leaderboard rows with mean score,
uncertainty fields, and `public_private_gap`. It writes local JSONL trajectories
under `runs/demos/baseline_compare/`.

## Verify And Inspect

```bash
python examples/demo_verify_and_inspect.py
```

This generates one random-agent trajectory, replays it with `verify_records`,
and prints the active physical constitution rules. It writes the trajectory to
`runs/demos/verify_random.jsonl`.

## CLI Equivalents

```bash
chemworld tasks list
chemworld inspect-constitution --env ChemWorld
chemworld run --task reaction-to-assay --agent random
chemworld verify --constitution --submission runs/random_ChemWorld_public-dev_balanced_seed0.jsonl
chemworld suite --task reaction-optimization-standard --agent scripted_chemistry
chemworld submission init runs/submissions/example --task-id reaction-optimization-standard
```

The submission example creates a skeleton. Add trajectories and result JSON
files before running `chemworld submission validate`.

## Local Eval Machine

```bash
python local_eval_server/teacher_side/eval_machine.py \
  --workspace runs/local_eval_machine \
  demo \
  --tasks reaction-to-assay \
  --seeds 0
```

This simulates a teacher-side evaluator and a student-side submission process on
the same host. The teacher process owns `ChemWorld`; the student process only
receives observations and returns actions. See [Local Eval Machine](local_eval_machine.md).

## Notebook Walkthrough

```bash
python -m pip install -e ".[dev,notebooks]"
jupyter notebook notebooks/full_workflow_demo.ipynb
jupyter notebook notebooks/physics_sanity_check.ipynb
jupyter notebook notebooks/tutorials/day_01_enter_virtual_lab.ipynb
```

The full workflow notebook demonstrates environment inspection, physical
constitution, manual event sequence, trajectory logging, evaluation, replay
verification, suite execution, leaderboard aggregation, and LLM replay
integration. The physics sanity notebook scans temperature, time,
catalyst-solvent interactions, and concentration-risk trade-offs.

## Twelve-Day Tutorial

The `notebooks/tutorials/` directory contains twelve executed notebooks for a
progressive short course:

- Day 1: first closed-loop virtual experiment;
- Day 2: ontology, units, and physical constitution;
- Day 3: instruments and partial observability;
- Day 4: mechanism scans and chemical intuition;
- Day 5: local surrogate-model learning;
- Day 6: baseline suites, BO/safe BO smoke baselines, and public/private
  leaderboard;
- Day 7: capstone trajectory replaying the selected best candidate, evaluation,
  verification, and explanation.
- Day 8: GPT-style structured planning and validator repair;
- Day 9: Bayesian optimization and safe Bayesian optimization;
- Day 10: public leaderboard challenge submissions;
- Day 11: private-world generalization and overfitting diagnosis;
- Day 12: Demo Day artifact with performance, mechanism, and reproducibility
  scores.
- Project blueprint: shared-world leaderboard design, project tracks, submission
  bundle shape, and visible multi-board scoring.

Start with `notebooks/tutorials/README.md`, then open the notebooks in order
with the `Python (ChemWorld)` kernel.

