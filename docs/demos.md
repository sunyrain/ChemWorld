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
chemworld inspect-constitution --env BatchReactorWorld
chemworld run --env BatchReactorWorld --agent random --budget 8 --seed 11
chemworld verify --constitution --submission runs/random_BatchReactorWorld_public-dev_balanced_seed11.jsonl
chemworld suite --env BatchReactorWorld --agent scripted_chemistry --world-splits public-test private-eval --seeds 0 --budget 12
```

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

Start with `notebooks/tutorials/README.md`, then open the notebooks in order
with the `Python (ChemWorld)` kernel.
