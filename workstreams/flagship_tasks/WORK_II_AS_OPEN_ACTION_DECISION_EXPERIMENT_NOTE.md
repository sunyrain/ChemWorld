# Work II A-S open-action full-plan longitudinal decision matrix

Status: development design; provider execution is not authorized. This block supersedes the
historical W2-47 feature-only terminal packet and does not constrain participant exploration to a
canonical workflow.

## Question

After one persistent agent autonomously conducts twelve open-ended partition experiments, can it
rank and select among eight newly revealed, fully specified executable action plans when outcomes,
hidden ranks, and other arms' evidence remain hidden? Do decision quality, mechanism accuracy, and
the support distance between the candidate plans and the explored history vary across the three
initial-information arms and independent worlds?

## Core design invariants

- Participant exploration is open-action. The agent may choose operation order, intermediate
  measurements, phase separation, reagent use, controls, and process parameters subject only to the
  host feasibility/resource contract. No canonical participant workflow is imposed.
- After the final `0/3/6/9/12` checkpoint is committed, the same eight candidates are shown to all
  three arms within a world. Each candidate is a complete public `ActionPlan`, including the ordered
  operations, every submitted parameter, explicit initial-state assumptions, measurement positions,
  terminal assay, and an explicit declaration for every omitted optional operation.
- The candidate packet is outcome-blind, not action-semantics-blind. Candidate outcomes, hidden
  ranks, checkpoint outcomes, and participant outcomes are withheld; the complete executable plan is
  public. Ranking-only still means no per-candidate numeric outcome predictions are requested.
- The evaluator executes exactly the public plan. Public plan hash, compiled truth-plan hash, and
  executed trajectory plan hash must agree. No evaluator-owned default may add, remove, reorder, or
  silently parameterize a scientific operation.
- Candidate plans may use different valid workflows. They must share the same fresh-batch initial
  state and terminal objective/score semantics. Workflow family, operation topology, and support
  distance are measured rather than forced to be identical.

## Units and coverage design

- Five independent partition worlds, each with matched `opaque`, `aligned_nominal`, and
  `misindexed_nominal` arms: 15 persistent sessions and 180 autonomous participant experiments.
- Each session remains one persistent thread with twelve participant-chosen experiments and typed
  checkpoints at `0/3/6/9/12`.
- Each world has eight distinct material-pair candidate plans. The public packet fixes its pair,
  volume, mixing, and workflow-family coverage before truth execution; the packet generator cannot
  read truth, rank, checkpoint outcomes, participant outcomes, or later model responses.
- The candidate roster records route-family counts and plan hashes. Low score range or low support
  is retained and reported; it never triggers outcome-based replacement.

## Measurements

- Primary action endpoint: within-world raw regret of the selected public action plan. Paired
  contrasts remain `misindexed - aligned` and `opaque - aligned` across all five clusters.
- Secondary action endpoints: selected rank, Top-1, normalized regret, selected-minus-candidate-mean
  score, complete-ranking Kendall tau, candidate score range, exact candidate overlap, and public-plan
  replay status.
- Mechanism is separate from action: held-out checkpoint error, explicit mechanism family, explicit
  exponent when applicable, executable-law normalized MAE, and final-query calibration. A null
  mechanism family or exponent is a recorded scientific failure, not an acceptable free-text law.
- Open-action support diagnostics: exact recipe overlap, material-pair overlap, operation-topology
  overlap, parameter-space distance, unseen-operation flags, candidate workflow family, and whether
  the selected plan is interpolation or structural extrapolation from the participant history.
- Exploration diagnostics remain unique recipe count, pair coverage, intervention-axis coverage,
  exact repeats, measurement diversity, and phase-separation/diagnostic-operation usage.

## Frozen denominators

| Item | Denominator |
|---|---:|
| Independent world clusters | 5 |
| Prior arms per world | 3 |
| Persistent sessions | 15 |
| Autonomous participant experiments | 180 |
| Checkpoints per session | 5 |
| Candidate plans per world | 8 |
| Candidate truth executions | 40 |
| Checkpoint truth executions | 80 |
| Provider-free truth and exact replay | 120 + 120 |
| Public-plan binding validations | 40 |

## Pass, failure, and stop rules

- Before provider calls, all candidate and checkpoint truth queries must complete with tolerance-zero
  exact replay. Every candidate must pass feasibility, complete-plan disclosure, no-hidden-default,
  public/truth/executed-plan hash equality, and checkpoint non-collision gates.
- Participant, schema, provider, scientific, resource, public-plan binding, and replay failures are
  retained in the scheduled denominator. No favorable rerun or outcome-based candidate replacement
  is allowed.
- A candidate plan may differ from every participant recipe. That is a valid extrapolation case only
  when its complete operation sequence and parameters were public before ranking.
- A platform repair affecting public-plan compilation, action disclosure, truth execution, or
  terminal parsing requires the affected block to rerun from its first unit.
- A one-world three-arm disclosure-only development pilot may reuse the historical diagnostic seed
  for interface isolation, but its records do not enter the formal five-world denominator. Formal
  execution uses fresh worlds after the pilot contract is stable.

## Expected outputs

One machine-readable open-action protocol, deterministic outcome-blind full-plan packets,
provider-free truth and replay with public-plan binding, 15 retained cell records when separately
authorized, support-distance summaries, a Chinese analysis report, and bounded Paper 2 claim updates.
