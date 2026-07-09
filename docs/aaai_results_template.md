# AAAI 结果模板

本页给出 AAAI 论文结果组织模板。实际数值应由 `scripts/run_aaai_experiments.py`、`chemworld baselines report --preset aaai` 和 private-eval runner 生成，不手写。

## Table 1: Task Coverage

| Task | Scenario | Main capability | Observation channel | Primary metric | Maturity |
| --- | --- | --- | --- | --- | --- |
| reaction-optimization-standard | reaction-optimization | Closed-loop optimization | final assay | best score / AUC | fill from manifest |
| reaction-to-purification | reaction-optimization | Reaction + purification | spectra + final assay | purity/recovery score | fill from manifest |
| partition-discovery | partition-discovery | Partition learning | phase/instrument signal | partition score | fill from manifest |
| reaction-to-distillation | reaction-optimization | Reaction + distillation | process observation | distillation score | fill from manifest |
| electrochemical-conversion | reaction-optimization | Electrochemical planning | electrochem proxy | conversion/safety score | fill from manifest |
| equilibrium-characterization | equilibrium-characterization | Equilibrium diagnosis | pH-meter + final assay | equilibrium confidence | fill from manifest |

## Table 2: Public-Test Baseline Results

| Task | Agent | Seeds | Best score | Final assay | AUC | Invalid rate | Safety cost | Task-specific metric |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fill | random | fill | fill | fill | fill | fill | fill | fill |
| fill | scripted_chemistry | fill | fill | fill | fill | fill | fill | fill |
| fill | gp_bo | fill | fill | fill | fill | fill | fill | fill |
| fill | safe_gp_bo | fill | fill | fill | fill | fill | fill | fill |
| fill | tool_using_llm_stub | fill | fill | fill | fill | fill | fill | fill |
| fill | codex_subagent_replay | fill | fill | fill | fill | fill | fill | fill |

Source files:

```text
runs/aaai_2027/baseline_report/baseline_summary_table.json
runs/aaai_2027/baseline_report/baseline_leaderboard.json
```

## Table 3: Generalization

| Task | Agent | Public score | Private score | Gap | Rank public | Rank private |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| fill | fill | fill | fill | fill | fill | fill |

Private-eval results must include salt policy, hidden seed policy and maintainer signature or equivalent local teacher-runner manifest.

## Table 4: Agent Interface Ablation

| Task | Agent setting | Best score | AUC | Invalid rate | Recovery rate | Final assays |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| fill | full interface | fill | fill | fill | fill | fill |
| fill | no affordance | fill | fill | fill | fill | fill |
| fill | no validator retry | fill | fill | fill | fill | fill |
| fill | no lab report | fill | fill | fill | fill | fill |
| fill | no safety cost | fill | fill | fill | fill | fill |

## Figure Suggestions

- Best-so-far score curves by task and agent.
- Invalid action and precondition failure rates.
- Public/private generalization gap.
- Codex/tool-agent trajectory case study with observations and selected actions.
- Spectra or pH-meter observation used in a decision.

## Required Captions

Each result caption should state:

- task ids and seeds;
- world law version;
- mechanism hash policy;
- maturity labels;
- whether results are public-test or private-eval;
- whether an LLM run is online or replay;
- whether private salt was present.

## Negative Results To Report

Report these explicitly if observed:

- BO fails to enter acquisition for a task;
- random reaches near-ceiling scores;
- spectra summary conflicts with processed metrics;
- high invalid action rate indicates weak affordance;
- private-eval rank instability suggests public overfitting.
