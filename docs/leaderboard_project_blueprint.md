# Leaderboard And Project Blueprint

ChemWorld projects should use one shared physical-chemical world rather than
separate mini-games. A course or workshop can run the **ChemWorld Shared World
Challenge**: teams submit agents, human+GPT workflows, BO policies, or
mechanism-driven strategies against task slices of the same `ChemWorld` law.

## Challenge Principle

Every submission must answer three questions:

- Did the strategy improve experimental performance under a finite budget?
- Did it stay safe and reproducible?
- Did it produce a credible local world-model explanation?

The leaderboard should therefore be multi-board, not a single highest-score
table.

## Visible Boards

| Board | Metric | Why It Exists |
| --- | --- | --- |
| Performance | private final-assay score | Rewards strong terminal decisions |
| Safety | low risk and few violations | Prevents unsafe score chasing |
| Sample efficiency | area-under-best-score per budget | Rewards good experiment design |
| Generalization | small public-private gap | Discourages public-test overfitting |
| Scientific understanding | mechanism explanation rubric | Rewards interpretable world-model learning |

The composite score can be used for an overall ranking, but all five boards
should remain visible so that trade-offs are not hidden.

## Suggested Project Tracks

| Track | Primary Task | Core Question |
| --- | --- | --- |
| Reaction optimizer | `reaction-optimization-standard` | Can the strategy beat scripted chemistry without becoming unsafe? |
| Safety-first agent | `reaction-safety-constrained` | How much score is worth giving up for robust low risk? |
| Purification strategist | `reaction-to-purification` | Can downstream processing improve purity without destroying recovery? |
| Partition scientist | `partition-discovery` | Can a learner infer phase behavior from sparse measurements? |
| Tool-using LLM planner | `tool-agent-planning` | Can language proposals survive validator checks and replay? |

Each team should choose one primary track and one diagnostic board to emphasize.

## Submission Contract

A leaderboard row is accepted only if it has:

- `manifest.json` with agent name, task id, seeds, command, commit hash, and
  dependency notes;
- `trajectories/*.jsonl` with replayable experiment records;
- `results/*.json` from local evaluation;
- optional `explanations/*.json` with hypothesis, learned mechanism, failure
  analysis, and next-experiment rationale;
- a short README describing what should and should not be trusted.

Public-test results are for development and classroom feedback. Private-eval
results should be maintained by a hidden registry or signed evaluation artifact
before being treated as a production leaderboard.

## Notebook

The executable project notebook is:

```text
notebooks/tutorials/project_leaderboard_blueprint.ipynb
```

It renders the task board, leaderboard schema, project tracks, submission bundle,
and a mock visible leaderboard shape.
