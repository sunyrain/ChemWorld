# Research formation: coverage extension and matched quench controls

W2-251, 2026-10-14. The user explicitly authorizes both blocks and their analysis/publication.
This note fixes their designs before new data production. W2-249's 48 sources and four
incomplete posttest chains remain unchanged. No model RNG seed is available or claimed.

## A. Complete the coverage matrix

Question: how do the existing formation/transfer observations vary across all five worlds
and the original Opaque, Aligned and MisIndexed information conditions?

| Additional coverage | Worlds | Arms | Repeats | Sessions |
| --- | --- | --- | ---: | ---: |
| EQ/P | W01–W05 | MisIndexed | 3 | 15 |
| C/E | W01–W05 | MisIndexed | 3 | 15 |
| C/E | W02, W04 | Opaque, Aligned | 3 | 12 |

Fixed new denominators: **42 sources, 504 source batches, 126 K1/Q/K2 + 15 EQS =
141 posttests**, up to 27 original recommendation retests. The combined descriptive view
contains **90 sources, 1,080 batches, 315 posttests**; retained failures remain missing,
not scheduled replacements. Each cell has three fresh model sessions, not independent
worlds or controlled model sampling seeds. Worlds and keyed observation mappings are fixed.

Reuse W2-249's original EQ-v2/C-v3 inputs, Sol medium provider, 12-batch budgets, notebook
role/tools, source and posttest resource limits, sealed query order, evaluators and goals.
No hints about quench, low concentrations, old outcomes or the causal study reach agents.
The two rounds are separate cohorts; date/provider drift may confound newly added arms
with earlier arms. Report cohorts and missingness explicitly, never call the combined
view a concurrently randomized 90-session study.

Queue is fixed before launch: world order rotates by two worlds each repeat; system order
EQ then C; arm order O/A/M, M/A/O, A/O/M; retain only missing cells. Four isolated workers
refill slots in this order. Every source launches once. Ordinary provider/participant failures
remain terminal outcomes and the queue continues. Uncaught executor, reference or replay
defects stop new launches and drain active workers. No outcome-selected retries or budget
extension. Preserve the original source time limits (EQ 5,400 s; C 3,600 s).

Reuse all 336 W2-249 host-only reference batches and execute only the missing C-W02/W04
references: **24 new batches / 2 trajectories**, giving 360 available reference batches.
Shared copies are not new executions. Existing reference inputs and execution semantics
are unchanged; no global release certificate regeneration is required.

Readouts retain original EQ error/interval/concentration metrics, C purity/recovery/fines,
quality classification, thermal contrast and recommendation retests; notebook coverage,
public revision timing, all rejected actions, replay, resource usage and missing stages.
Report each session, each world/arm's mean/SD/range and world-equal O/A/M contrasts with
observed denominators. No required direction or performance gain defines success.

## B. Matched quench operation intervention

Question: holding the rest of a retained recipe fixed, what does inserting/removing the
quench operation do to particle quality and seed-excluded recovery in the virtual worlds?
This is an environment intervention, not an intervention on the agent's judgment.

Coverage fixed without screening new outcomes: **all 18 W2-249 C recommendations × all
five original worlds × quench present/absent = 90 pairs / 180 single-batch trajectories**.
Recommendations include all originally unsuccessful recipes. Cross-world executions are
the declared transport test; the 18 original-world pairs are separately identified.

Use the committed recommendation recipe, including its material quantities, operation
arguments/order, measurements, residence times and crystal seeds. If it contains one
quench, its existing position defines insertion; the absent arm deletes exactly that
action. Otherwise insert one quench immediately before the first seed_crystals or
cool_crystallize action. All other actions must be identical after deleting quench.
No policy adapts after the intervention, and no invalid recipe is repaired mid-block.

Both arms start from the same world and initial state, use keyed observation seed 303,
Opaque public information and the original 12-batch resource envelope for the single
recipe (as in recommendation retesting). Primary paired outcomes use noiseless evaluator
truth, so action-position changes in noisy measurements do not define the effect.
The intervention includes quench's temperature change, reaction-stop flag, time and
resource costs. It does not isolate cooling rate, nucleation, or temperature alone.

Record before/after temperature, species, reaction-stop state, particle population and
resource ledger around all operations through a read-only observer; preserve direct
cooling diagnostics and full exact replay. Primary outcomes: paired changes in fines,
purity, size, recovery, quality feasibility and quality-plus-recovery feasibility, using
the original particles-present / purity≥0.80 / fines≤0.50 / recovery≥0.10 rules.
Report paired values and failures for every recipe/world, with original-world and
transport results distinct. Deterministic repetitions do not increase independent n.

Legally rejected operations, resource exhaustion or absent particles remain intervention
outcomes; no zero imputation for missing final measurements. Replay/platform defects stop
execution. Opposite/no effects are valid results. This can establish the effect of the
operation in the specified virtual recipes, not a human laboratory law or the reason an
agent formed its interpretation.

## Outputs and execution

One executor on main; four model workers plus one separate sequential provider-free
quench process. Print progress every 30 seconds, counts/throughput/ETA or operation liveness.
Run through the locked environment. Commit the stable runner/note once before execution;
preserve runtime, recipes and inputs in the local run root. No manuscript/PDF changes.

Parent raw root: `D:/Projects/ChemWorld-local-research/20261013-research-formation/attempt-01`.
New raw root: `D:/Projects/ChemWorld-local-research/20261014-research-extension/attempt-01`.
Quench raw root: sibling `quench-attempt-01`. Raw provider payloads and credentials stay
outside Git. Publish sanitized 42-source and combined 90-source counts, per-session notes
and posttests, per-pair causal data, failures and readable summaries under
`reports/research-extension-20261014/`. Existing W2-249 files are never overwritten.

## Completion (2026-10-14)

42/42 new sources terminal; 40 full chains, 503/504 batches, 136/141 stages. Quench: 180/180 trajectories, 90 pairs, 75 valid pairs. All failures retained. [Results](reports/research-extension-20261014/REVIEW.md).
