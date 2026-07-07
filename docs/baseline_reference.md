# Baseline Reference

Official baselines should be reported per task rather than merged into one
global table.

| Task Family | Reference Baselines |
| --- | --- |
| Reaction optimization | random, LHS, scripted chemistry, GP BO, RF EI, safe GP BO |
| Safety constrained | random, scripted chemistry, safe GP BO |
| Reaction to purification | random event planner, scripted chemistry |
| Partition discovery | random, scripted chemistry, LLM replay |
| Low budget characterization | random, LHS, GP BO |
| Tool-agent planning | LLM replay, tool-using LLM stub |

LLM entries are reproducibility adapters, not claims that ChemWorld already has
a validated autonomous chemical agent. Online LLM results must report model
name, date, prompt, temperature, cost, cache policy, and replay artifact.

The default BO baselines now use `n_initial=4`. The primary reaction task uses
`budget=72`, which gives recipe-based BO enough final-assay observations to
enter acquisition instead of spending the whole episode on initialization.

Reference tables should include mean, standard error, safety violations,
public/private gap when available, and the exact platform version and command.
