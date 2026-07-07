# ChemWorld-Bench Twelve-Day Tutorial

Open the notebooks in order with the `Python (ChemWorld)` kernel.

```bash
python -m pip install -e ".[dev,notebooks]"
python -m ipykernel install --user --name chemworld --display-name "Python (ChemWorld)"
```

## Schedule

| Day | Notebook | Focus |
| --- | --- | --- |
| 1 | `day_01_enter_virtual_lab.ipynb` | First closed-loop virtual experiment |
| 2 | `day_02_ontology_and_constitution.ipynb` | Ontology, units, and executable physical constitution |
| 3 | `day_03_observation_and_instruments.ipynb` | Instrument observations and partial observability |
| 4 | `day_04_mechanism_scans.ipynb` | Temperature, time, catalyst-solvent, and risk scans |
| 5 | `day_05_surrogate_modeling.ipynb` | Local surrogate model learning and recommendation |
| 6 | `day_06_baselines_and_leaderboard.ipynb` | Random/LHS/scripted/BO/safe BO suites, metrics, and public/private leaderboard |
| 7 | `day_07_capstone_artifact.ipynb` | Replay the selected best candidate as a reproducible trajectory, then evaluate, verify, and explain it |
| 8 | `day_08_gpt_planner_and_validation.ipynb` | GPT-style structured proposals, validator repair, and experimental testing |
| 9 | `day_09_bayesian_optimization.ipynb` | BO and safe BO convergence, risk, and sample efficiency |
| 10 | `day_10_public_leaderboard_challenge.ipynb` | Public-test submission rehearsal with verified JSONL trajectories |
| 11 | `day_11_private_generalization.ipynb` | Public/private transfer, gaps, and overfitting diagnosis |
| 12 | `day_12_demo_day_artifact.ipynb` | Demo Day artifact with performance, mechanism, and reproducibility scores |
| Project | `project_leaderboard_blueprint.ipynb` | Shared World Challenge design, visible leaderboard boards, project tracks, and submission contract |

The notebooks use executable SVG diagrams and plots generated from the current
environment. No external image files or online services are required.

## Course-ready notes

- Failed action preconditions produce empty observations and explicit error messages.
- `final_assay` is a terminal scoring event and is used once per official trajectory.
- Day 4 uses valid recipe time bounds and includes a time-scan sanity assertion.
- Day 6 uses five teaching seeds and exposes the formal 30-seed benchmark target.
- Day 7 uses the same split and seed for candidate selection and official replay.
- Day 8-12 extend the course from tool use to GPT-assisted planning,
  optimization, public/private evaluation, and final research artifacts.
- `project_leaderboard_blueprint.ipynb` turns the sequence into a course or
  workshop leaderboard without turning tasks into separate mini-games.
