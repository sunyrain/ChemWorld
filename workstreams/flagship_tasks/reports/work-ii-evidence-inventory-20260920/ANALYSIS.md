# ChemWorld evidence synthesis and experiment closure

Analysis date: 20 September 2026, after the four-worker C posttest recovery.
Scope: local results plus remote exports at commit `f29a27ee`; no remote runtime checkout.
The [generated inventory](REPORT.md) and [machine summary](summary.json) give exact denominators.
This is a descriptive analysis and evidence disposition, not a new preregistration or release audit.

## 1. What is available now

Four complete contemporary system cohorts are ready for quantitative analysis: EC, PA, RX,
and bounded EQ/P. Together they contain **165 autonomous source sessions, 2,520 source
batches and 495 K1/Q/K2 stages**, plus 15 subsequent EQ-specific supplements. Each system
has five worlds. Shared simulator families, repeated arms and goals are not independent
replications of chemical domains. EC/PA and RX remain explicitly development evidence.
K1/Q/K2 counts refer to named stages, not identical questions: RX uses a seven-question K2,
whereas EC/PA and C use three. Their textual responses require block-specific interpretation.

C now supplies an additional 30 source slots, 539/540 batches and all 90/90 K1/Q/K2 stages.
The automatic queue has ended: 28 complete chains, one 11/12 source, and one completed
24-batch source whose post-K2 public-baseline exception blocked its recommendation retest.
All 30 Q evaluations are available. These are useful observations despite the two distinct
completion issues; neither issue justifies discarding the cell or repeating its scientific answers.

Including C, the five-system primary analysis pool therefore contains **195 started source
sessions, 193 complete chains, 3,059/3,060 source batches and 585/585 K1/Q/K2 stages**,
plus 15 EQS supplements. This subtotal excludes EC P/S pilots, the retired EQ-S pilot,
historical studies, qualifications, references and retries. It is not a declaration that
every cell or every system has completed its entire evaluation chain.

| System or block | Available coverage | Role in the integrated paper |
|---|---|---|
| EC E | Five worlds × two goals × two budgets × three arms; 60 complete chains | Main goal/budget/prior comparisons |
| PA E | Five worlds × two budgets × three arms; 30 complete chains | Main budget, quantitative prediction and phase-decision comparison |
| RX P/S | Five worlds × two goals × two prior loci × three arms; 60 complete chains | Main parameter/structure-prior comparison; goals analyzed within RX |
| EQ bounded/P v2 | Five worlds × three arms, 12 batches; 15 complete chains | Main bounded-equilibrium prediction and uncertainty analysis; supplementary EQS stays separate |
| C E v3 | Five worlds × two budgets × three arms; all source slots and questions attempted | Main prediction analysis with explicit source nonconformance; finish mechanical retest closure |
| EC P/S supplements | One world, two goals, three arms per locus; 11/12 complete chains | Exploratory appendix; retained calculator-limit failure |
| EQ-S v0.2.1 | 15 complete closed-set discrimination pilots | Historical diagnostic; do not relabel as canonical free-mechanism discovery |
| EQ-S v0.3 | Canonical relaunch/recovery/export code committed remotely; no result export visible | Await collaborator's completed export; do not infer completion from the exporter commit |
| P purification | V3 gate passes five worlds, 15 campaigns plus five aqueous probes; no agent source | Next limited scope: 12 batches only; integration pilot before 15-source E matrix |
| D distillation | Historical development and feasibility diagnostics | No current standardized five-world free-report cohort |
| FL continuous flow | Historical static comparison and development gates; operating-window gap | No current standardized free-report cohort |
| BC resource-limited characterization | Platform/design coverage and historical diagnostics | No current standardized free-report cohort |

Nine systems describe platform/task capabilities. They do not yet describe nine completed
autonomous-study cohorts. EQ/P and EQ/S are two studies within EQ, not two extra systems.
P in RX-P or EQ-P denotes a prior locus; P purification is a different system identifier.

## 2. Findings that the current results support

### Additional experimental budget improves prediction, with different residual errors

In the complete EC/PA cohort, increasing the allocated budget from 12 to 24 gives:

| Task | Prediction MAE, 12 → 24 | Matched conditions with lower MAE | Other outcome |
|---|---:|---:|---|
| EC discovery | 0.17378 → 0.11222 | 11/15 | Retest score 0.53638 → 0.54903 |
| EC optimization | 0.17811 → 0.10818 | 12/15 | Retest score 0.66404 → 0.74792 |
| PA discovery | 0.08291 → 0.02379 | 13/15 | Phase decisions 25/30 → 30/30 correct |

The mean relative MAE reductions are approximately 35%, 39% and 71%. EC measures score
prediction; PA measures organic product fraction. Their absolute errors are not pooled.
The 12- and 24-batch conditions are separately initiated sessions, not the first and second
halves of one experiment. Extra reasoning and changed experimental allocation accompany
the larger budget; this is not a fixed-token estimate of the marginal value of twelve observations.

C adds a useful, harder endpoint. Across all 15 available Q answers at each allocated budget,
including the labelled 11/12 source, recovery MAE declines from 0.10433 to 0.07937, but
fines-fraction MAE remains 0.30999 at 12 and 0.27000 at 24. Nominal 80% interval coverage
for fines is only 35.6% and 43.9%. Purity and size have different error profiles; they should
not be hidden by a single average over endpoints. This supports a specific observed limitation
in predicting particle quality. It does not yet identify whether the cause is inadequate
experimental coverage, an incorrect inferred relation or numerical extrapolation.

### Better optimization and better prediction are distinct outcomes

Within EC, optimization produces a better independent recommendation retest in **26/30**
world/arm/budget pairs, but a lower score-prediction MAE in only **14/30**. In **13/30**,
the recommendation improves while prediction worsens. The latter pattern is also present
in 7/17 pairs where both sources completed on their first attempts. This is evidence of
different outcome orderings, not proof that a mechanism report caused the decision.

RX does not repeat EC's optimization advantage: optimization has a better recommendation
retest in **9/30** paired world/locus/arm conditions and lower six-metric macro MAE in
**6/30**; five pairs improve the retest while worsening prediction. Goal effects therefore
depend on the task and response surface. An optimization prompt alone does not establish
that the resulting research policy actually optimized better.

C has 29 observed recommendation retests at this snapshot. Quality plus recovery ≥0.10
holds in 10/15 at budget 12 and 9/14 available at budget 24. The fourteenth-versus-fifteenth
denominator is an unfinished retest, not a scientific exclusion. Do not draw a final C budget
ranking from these incomplete, unpaired retest aggregates. Source-selected observations,
independent retests and noiseless evaluator truth remain separate endpoints.

### Prior information has no uniform ordering

EC discovery gives lower mean score-prediction MAE to MisIndexed than Aligned at both
budgets (12: 0.13206 versus 0.19393; 24: 0.07133 versus 0.14521). EC optimization instead
has its best mean recommendation retest under Aligned at both budgets. PA's 24-batch
decisions reach 10/10 in every arm while prediction errors remain different.

In RX-P discovery, six-metric macro MAE is 0.1019 Opaque, 0.0570 Aligned and 0.0546
MisIndexed. In RX-S discovery the ordering changes: 0.0840, 0.0921 and 0.1016 respectively.
In bounded EQ/P, macro MAE is 0.01214 Opaque, 0.04314 Aligned and 0.03928 MisIndexed;
nominal 80% coverage is 91.3%, 69.0% and 70.7%. The supplied information does not
uniformly improve prediction or calibration in these samples.

These are total descriptive arm contrasts under adaptive experimentation. Changed experiment
selection is a possible mediator of the prior intervention, not a reason to erase its total
effect. However, these small one-session-per-cell blocks do not separately identify direct
belief persistence, experimental selection, or stochastic session variation. Inspect world-level
paired differences and recovery sensitivity before making a stronger inferential claim.

### The available evidence does not establish universal information loss

Bounded EQ/P achieves accurate predictions in Opaque. PA responds strongly to larger
budgets. Some RX reports explicitly acknowledge unresolved alternatives. These are important
positive and calibrated cases, alongside failures.

The old EQ-S closed-set pilot predicted responses accurately but all 15 agents abstained
from its final categorical network choice. The later v0.3 contract explicitly retires that
participant-question design. A simulator non-collapse gate demonstrates a contrast under
registered conditions; it does not prove that every adaptive source acquired enough
discriminating evidence. Abstention can therefore be appropriate. The old categorical endpoint
cannot stand in for a blind evaluation of the new free-form K1 mechanism accounts.

## 3. Disposition of earlier experiments

The machine inventory retains 33 Work II registry entries and an index of 233 top-level JSON
reports. Those files contain overlapping versions, analyses, qualifications and reused sources;
233 reports are not 233 independent experiments. The following is the scientific disposition
of the principal earlier programmes, with counts interpreted in their original contracts.

| Evidence family | Retained result and denominator | Use now |
|---|---|---|
| Paper 1 instrument qualification | 64/64 reference units; 1,786/1,786 recipes; 52/52 generated compositions; 32/32 modules; 7/7 interfaces; 192/192 negative probes; 7/7 invalid-composition mutants | Main platform reliability evidence, bound to its frozen release |
| Paper 1 usage demonstrations | Eight deterministic cases, 89 submitted/88 committed actions/one registered rollback; one agent example with 15 committed actions and replay | Demonstrate instrument semantics; not a model capability ranking |
| Static S0 optimization | EC and crystallization, ten worlds per task, 20 exploration experiments/world; reported 28,060 total physical executions include references/baselines | Historical comparison; not the current free-operation experiment count |
| Static information three-arm study | 60 cells; 2,280 physical executions; shares its Opaque cohort with S0 | Useful predecessor: EC nominal information benefit and wrong-prior cost; crystallization wrong-prior benefit in sampled worlds; overall recovery criterion not met |
| Static five-task extension | 150 method/world result rows; 3,900 physical executions, including classical methods | Development appendix; do not call all rows agent sessions or current nine-system evidence |
| Open-action donor programmes | DeepSeek 42/45 eligible; Sol 26/45 eligible, with all failures retained | Historical trajectories and protocol development; reused downstream, not fresh sources each time |
| C2 and B3 cross-model analyses | C2: 126/135 Sol and 121/135 DeepSeek; B3: 30/30 Sol and 17/30 DeepSeek | Separate historical contracts, failure-aware descriptive controls; no pooled current-model ranking |
| M1 constrained local surfaces | Ten worlds, 120/120 provider sessions, 160/160 conditions, 200 physical executions | Primary representation benefit not supported; restricted quadratic modelling, not free mechanism discovery |
| M3 same-world portability | Same ten M1 worlds; 160 provider sessions, 80 new physical executions | Knowledge versus no-information benefit supported; law versus raw evidence not established as superior; no additional independent worlds |
| Final B3 numeric-tool diagnostic | Five reused worlds; 117/120 completed sessions; tool effect on joint recovery +0.0167 with interval spanning zero | Does not support a numeric-tool rescue or establish public identifiability |
| Information-completeness intervention | Ten shared worlds; Sol 60/60, DeepSeek 52/60 complete; original→complete recovery 6/20→20/20 and 3/20→17/20 | Important controlled interface-information diagnostic; model configurations and disclosure-length effects remain distinct |
| Astra dense-evidence handoff | Seven sessions; no new physics; all four evidence-based readers select the tested-grid optimum | No prespecified summary-loss effect observed; retain this negative result |
| Astra/full-process, continuity and early-time work | Fixed diagnostic blocks with failed transactions, contract/measurement defects and weak or absent feasibility witnesses retained | Platform/design diagnosis; do not turn pre-repair failures into systematic agent incompetence |
| EC September 18 and PA 12/24 pilots | EC eight attempted sources/seven complete; PA one source at each budget, with identity exposure and batching-design limitations | Historical pilots; do not merge with corrected English five-world cohorts |
| C pilot and v1/v2 qualification attempts | One-world pilot and multiple reference/domain blocks, including failed qualification | Design provenance; only v3's frozen five-world block supports current C comparisons |
| P gates and loading diagnostic | All four blocks: 605 batches; final v3 185 batches and 3,110 operations with replay | Readiness evidence only; zero current P agent sessions |

The historical information-completeness result is useful precisely because it warns against
attributing an interface information deficit to agent reasoning. It should not become the
paper's headline claim that agents systematically lose scientific information. M1/M3 describe
constrained local response representations and retain their original negative or bounded results.

## 4. Recommended paper argument

The strongest current argument is that ChemWorld makes the relationship between prior
information, experimental choices, written explanations, predictions and task outcomes
observable under controlled worlds. The results already show that these outcomes need not
improve together, and that the influence of information and experimental budget is task dependent.

Organize the article in four parts:

1. Establish the composable instrument and its frozen platform qualification.
2. Describe the shared autonomous-research design and system-specific scientific commissions.
3. Present the completed quantitative contrasts: budget effects, prediction/calibration,
   recommendation outcomes and heterogeneous prior-arm orderings. Give C its particle-quality
   result rather than reducing it to a generic synthesis score.
4. Explain observed failure and success patterns using the actual evidence and free-form K1
   reports. This last part needs systematic annotation; it is not complete just because Q is scored.

A defensible central statement is: **successful chemical action, accurate intervention
prediction and a justified mechanistic explanation must be evaluated separately.** Current
numerical evidence directly establishes the first two as distinct outcomes. The third needs
the report/trajectory analysis below before claiming a systematic mechanistic dissociation.

Do not put unfinished system counts, prospective ideal outcomes, or a universal failure
mechanism into an observed-results abstract. The existing nine-system abstract is marked
prospective; use the evidence inventory to finalize it after scope closure.

## 5. Analysis and execution closure

| Priority | Work | Completion rule |
|---|---|---|
| 1 | Finish C mechanical closure | Preserve 11/12 nonconformance; retain post-K2 baseline exception; complete only the already-planned missing retest, with the frozen recipe and observation seed; no new model source or re-questioning |
| 2 | Incorporate EQ canonical S delivery | Read actual v0.3 result exports when available; keep v0.2.1 separate; do not merge the remote C runtime over the current frozen local block |
| 3 | Analyze complete current cohorts | World-level paired effects, individual metrics, interval width/coverage, task retests, all failures, and first-attempt-only sensitivity; no universal cross-system MAE |
| 4 | Annotate mechanisms and evidence exposure | Apply the same rubric to every eligible K1/trajectory; include successes, abstentions and failures; audit K2 self-reports against logs |
| 5 | Finish the already-selected P scope | One 12-batch Opaque integration pilot, then the predeclared five-world/three-arm/12-batch block if its execution path works; no 24-batch branch |
| 6 | Finalize manuscript and figures | Replace stale partial counts; show platform scope separately from agent-study scope; preserve development/formal labels and explicit exclusions |

For the mechanism audit, extract each consequential claim, its stated domain and uncertainty,
the cited experiment numbers, and whether relevant contrary observations were available before
the claim was sealed. Code at least: unsupported generalization; acquired contradiction not
acknowledged; justified uncertainty; accurate revision; accurate prediction without an identified
mechanism; and task success with weak out-of-domain prediction. "Never tested" and "tested but
ignored" require different evidence and different denominators. An apparent missing contrast
must be checked against actual experimental conditions and measurement resolution.

An external LLM judge may assist claim extraction, blinded to arm and task outcome when those
are unnecessary, but it is not ground truth. Use simulator laws, declared observation mappings,
publicly available evidence and independently checked examples to validate its dimensions;
record disagreement. Do not invent a single mechanistic-correctness score after reading outcomes.
K2 is a participant's retrospective account, not a causal explanation of its internal reasoning.

Do not launch D/FL/BC solely to turn nine platform task families into nine result panels before
this analysis is done. Keep them as explicitly future extensions unless they resolve a specific
remaining scientific question. This is a closure recommendation, not cancellation of any
collaborator's already-authorized work.

## Reproduction

```powershell
uv run --no-sync python -m scripts.report_work_ii_evidence_inventory --remote-commit f29a27ee --output workstreams/flagship_tasks/reports/work-ii-evidence-inventory-20260920
```

The script checks unique effective cells and verifies all 90 EC/PA E prediction summaries
against their latest effective ledger rows before reusing the completed-block analysis. It
reads remote exports through Git, not through runtime imports. All original evidence remains
unchanged. Rerunning after C closure will produce a later timestamped snapshot; the prose
analysis must then be reviewed against changed denominators.
