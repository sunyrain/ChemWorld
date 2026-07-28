# ChemWorld: A Replayable Causal Environment for Experimental Intelligence

Status: working manuscript, 2026-07-29. Not submission-ready.

## Abstract

ChemWorld is a replayable physical-chemistry environment for evaluating how
agents choose, interpret, and revise experiments under partial observability,
finite budgets, and operational constraints. The environment separates an
executable causal substrate, a transactional interaction runtime, and
versioned task/evaluation contracts. Fifteen tasks are registered without
proxy-only physics on their required runtime paths. Two confirmatory tasks,
electrochemical conversion and reaction-to-crystallization, support both
static scientific optimization and controlled mechanism interventions.
Every registered task has an executable complete-experiment adapter; all 15
tasks pass 415 midpoint, coordinate-boundary, and categorical execution cases,
with no dead coordinates. All 62 declared success metrics bind to explicit
evaluation endpoints.

The former 2026-07-27 static-S0 participant result bundle has been withdrawn
because its legacy material and score contracts are not the contracts of the
current benchmark candidate. No participant-performance number from that
bundle is reported here. Replacement fixed-world protocols now bind explicit
material-family hashes, task-specific score laws, opaque material identities,
and paired blind validation. Both replacement campaigns completed ten
independent worlds, twenty exploration experiments per world, full classic
baselines, and exact replay. Codex averages 0.7150 on electrochemical
conversion and 0.5355 on crystallization. The electrochemical paired
descriptive difference against the best information-matched baseline is
+0.0991; crystallization trails LHS by 0.0353. No superiority threshold or
multiplicity plan was preregistered, so these are bounded descriptive results,
not a broad state-of-the-art claim.

Historical environment-level RC28 controls also establish budgeted
identifiability and online attainability on their frozen source: the
five-experiment controlled certificate reached 98.26% top-1 accuracy and the
frozen online reference policy reached 96.57% end-to-end success by eight
post-change experiments. These are environment attainability results, not
participant-agent results; their current source binding is stale and requires
recertification. All reported physical experiments are replay-verified.

## 1. Research Question

The primary question is not whether a language model can state chemical
knowledge. It is whether an agent can select a useful next experiment, use the
result, and submit a robust method when the governing world is fixed but its
parameters are hidden.

Controlled world changes were previously developed as a separate environment
identifiability question. They are retained as historical control evidence,
but are not part of the current participant roadmap. Real systems may drift
through batch variation, instrument calibration, aging, or fouling; those
processes require explicit drift models rather than an evaluator silently
replacing the governing mechanism mid-campaign.

## 2. System

ChemWorld has three normative layers:

1. a physical causal world substrate with typed state, executable kinetics and
   constitutive models, instruments, and controlled interventions;
2. an interaction runtime with validated operations, atomic transactions,
   costs, risks, and replayable trajectories; and
3. task/evaluation contracts defining public information, budgets, objectives,
   scoring, and world distributions.

The agent and its private memory sit outside these layers. The environment
does not expose hidden world parameters or private evaluator provenance.

## 3. Task Design

The release registers 15 tasks. The machine-readable design matrix is
`workstreams/flagship_tasks/reports/task-design-matrix-v1.json`. Every row
records the environment decision unit, complete-experiment adapter, control
schema, operation sequence, measurement slots, scoring contract, safety/cost
boundary, and evidence status.

The two confirmatory tasks expose named physical controls in static S0. The
electrochemical experiment has six controls and one electrolysis stage. The
reaction-to-crystallization experiment has ten controls and one fixed
reaction/quench/seed/cool/filter workflow. Internal unit vectors remain only
for classic optimizers. An unused fourth equilibrium coordinate was removed.
The three purification tasks use a 16-control reaction/workup design that
compiles to 22 operations spanning extraction, phase separation, washing,
drying, concentration, and transfer. Distillation uses 13 controls, with
independent evaporation and distillation temperature/time settings.

The matrix generator rejects action-invariant coordinates and executes every
midpoint, each coordinate's low/high intervention, and every discrete category
against the runtime. All 415 cases require committed transactions, a final
assay, and compliance with the operation budget. All 15 tasks pass. The 62
declared success metrics bind separately to terminal-observation, trajectory,
structured-artifact, predictive-holdout, or paired-split evaluators. This is
design validation; only the two confirmatory tasks have formal model
experiments in the present study.

## 4. Static-S0 Protocol

The world remains fixed for the entire campaign. The model knows that the
horizon is 20 complete experiments. Each model call selects one complete
experiment; the executor performs the fixed operation sequence and returns
public processed measurements, uncertainty, cost, risk, and final-assay score.
After exploration, one additional call submits the final method. The final
method may be tested, interpolated, or extrapolated within bounds and is not
assumed to equal the last trial.

Three paired, held-out, one-factor predictive queries are frozen before the
model's final predictions and executed only afterward. The model receives no
feedback from these checks. Incumbent and submitted methods each receive three
paired blind validation replicates. Free-form mechanism prose is secondary;
structured Declared claims, held-out Predictive directions, and Actionable
blind performance are scored separately.

## 5. Static-S0 Formal Results

The legacy two-task bundle was removed from the evidence DAG and cannot support
an abstract, result table, model comparison, or arXiv claim. The replacement
v1.0 campaigns are the only active static-S0 formal results.

| Task | Codex mean (world-bootstrap 95% interval) | Strongest information-matched baseline | Paired difference (95% interval) |
| --- | ---: | ---: | ---: |
| Electrochemical conversion | 0.7150 (0.6283–0.7861) | structured RF, 0.6159 | +0.0991 (+0.0103–+0.1748) |
| Reaction-to-crystallization | 0.5355 (0.5045–0.5644) | LHS, 0.5708 | −0.0353 (−0.0650–−0.0085) |

Electrochemical conversion has fourteen classic baselines. The strongest
privileged calibration baseline is descriptor RF at 0.6441; the Codex-minus-
baseline interval for that comparison is −0.0072 to +0.1354 and crosses zero.
The positive information-matched comparison therefore does not establish
superiority to methods with privileged nominal material descriptors.

Reaction-to-crystallization has seven classic baselines. Codex is below LHS
and does not support an outperformance claim. Its secondary held-out
predictive directional accuracy is 0.478 with Brier score 0.298, compared with
0.744 and 0.186 for electrochemical conversion. Every final recommendation is
a tested condition and has zero gain over its validated incumbent. The present
data therefore support bounded optimization-performance reporting but not a
claim that final synthesis generated a novel improved method.

Algorithm-seed repeats are treated as nested technical repeats; uncertainty is
bootstrapped over the ten independent worlds. All comparisons are descriptive
because the campaign did not preregister a superiority threshold or a
multiplicity correction.

## 6. Environment Attainability

Historical RC28 Gate A is a separate mechanism-adaptation result on its frozen
source. A2 completed 4,896
receipts and reached 98.26% top-1 accuracy at its five-experiment primary
budget. A3 completed 2,016 receipts; by eight post-change experiments the
frozen reference policy reached 99.17% reference sufficiency, 99.35%
detection recall, 0.9990 AUROC, 2.80% conditional no-change false-positive
rate, 98.03% conditional attribution, and 96.57% end-to-end success.

This establishes that a compliant reference strategy can solve the controlled
diagnostic problem. Participant Gates B–E remain unexecuted. Static-S0 results
must not be cited as mechanism-change performance.

## 7. Audit and Resources

The participant campaigns contain 760 physical experiments and 420 Codex
subscription calls. Per world, each task uses 20 exploration experiments, 12
predictive physical experiments, and six paired blind-validation experiments.
The classic baselines contain 1,050 algorithm cells and 27,300 physical
experiments: electrochemical uses fourteen algorithms × five technical
algorithm seeds × ten worlds, and crystallization uses seven × five × ten.
The complete campaign therefore contains 28,060 physical experiments.

All twenty participant reports and all twenty task/world baseline audits pass
exact replay. Provider pricing was not independently verifiable, so monetary
accounting is not imputed.

## 8. Limitations

ChemWorld is not a universal reaction predictor or industrial digital twin.
Its mechanisms and constitutive models are bounded benchmark worlds. Synthetic
HPLC, GC, UV-Vis, and final-assay observations are state-coupled measurement
models, not empirical spectra. Virtual risk and cost are benchmark quantities,
not laboratory safety or procurement guidance.

The static-S0 sample has ten world seeds and one LLM run per world. It
characterizes those sampled worlds and does not estimate a universal model
effect. Baselines and comparisons were selected and ranked descriptively, so
the paired intervals are not preregistered confirmatory tests and do not
control familywise error. The explicit world-understanding metrics and zero
recommendation gains show that successful local optimization is not sufficient
evidence of correct mechanism understanding or novel method synthesis.

The 15-task adapter audit is a deterministic 415-case executability check at
one world seed, not a performance experiment. Thirteen tasks therefore have
complete optimization designs and metric endpoints but no formal model
comparison in this study.

Private-E/A, independent backend replication, real-data bridging, and physical
experiments remain open. Hidden changepoints and mechanism replacement are
deferred until a realistic drift model and separate research question are
specified. The repository therefore retains `publication_ready=false`.

## 9. Next Validation Priorities

The immediate roadmap remains within fixed-world scientific optimization:

1. freeze a crystallization v1.1 participant policy before running untouched
   worlds, without altering the v1.0 result;
2. preregister primary baseline comparisons, superiority margins, and
   multiplicity handling for the next independent campaign;
3. ablate final synthesis against best-observed submission and a
   forced-new-proposal variant;
4. replicate with an independent model/provider and extend formal comparison
   to selected additional static tasks; and
5. build a static bridge to real data or a higher-fidelity simulator.

World-change experiments are not an active launch item. They should return
only as a separately motivated robustness benchmark tied to observable batch
variation, instrument drift, aging, or another explicit real process.
