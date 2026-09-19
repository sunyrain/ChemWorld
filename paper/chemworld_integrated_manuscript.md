---
title: "ChemWorld: Controlled Chemical Worlds for Studying Autonomous Scientific Discovery"
subject: "Programmable experimental worlds, autonomous evidence acquisition, and scientific knowledge"
author:
  - name: "Jiangjie Qiu"
    affiliation_markers: "1"
    equal_contribution: true
  - name: "Yijun Li"
    affiliation_markers: "1"
    equal_contribution: true
  - name: "Yaotian Yang"
    affiliation_markers: "1"
    equal_contribution: true
  - name: "Honghao Chen"
    affiliation_markers: "1"
  - name: "Wentao Li"
    affiliation_markers: "1"
  - name: "Xiaonan Wang"
    affiliation_markers: "1"
    corresponding: true
affiliation:
  - id: "1"
    name: "Beijing Key Laboratory of Artificial Intelligence for Advanced Chemical Engineering Materials, State Key Laboratory of Chemical Engineering and Low-Carbon Technology, Department of Chemical Engineering, Tsinghua University, Beijing 100084, China"
correspondence: "wangxiaonan@tsinghua.edu.cn"
equal_contribution_note: "Jiangjie Qiu, Yijun Li and Yaotian Yang contributed equally."
bibliography: prior_discovery_references.bib
draft_status: "Prospective nine-system abstract; empirical results retain their observed scope; not a publication export"
---

> Authoring status, 19 September 2026: this manuscript integrates the ChemWorld platform
> contribution and the current autonomous-research programme, following the authors' decision
> to write one paper. Platform qualification below is inherited from its frozen release.
> Agent results are development evidence. Section 5 reports complete
> factorial blocks: all five worlds in each system, comprising the complete 90-campaign
> entity-prior cohort, including every arm, budget and applicable goal. The parameter/structure
> pilot and mechanism-claim analysis are still outstanding. Numerical snapshot: 17:59 +08:00.
> Editorial notes and the source navigation at the end are excluded from reader-facing prose.

> Abstract drafting assumption: the abstract below sketches the intended nine-system paper.
> Its cross-system findings are projected conclusions to test, not completed empirical results.
> Section 5 retains the observed EC/PA results and the separately identified, unscored RX records.

# Abstract

Autonomous scientific discovery depends on turning limited experimental evidence into
explanations that remain useful under new interventions. In real laboratories, incomplete
mechanistic knowledge and the coupling of prior beliefs, experiment selection, and task
outcomes make failures in this process difficult to locate. We present ChemWorld, a
programmable chemical-world framework for controlled studies of scientific discovery.
Composable process and observation models provide hidden, evaluator-known mechanisms,
controllable prior information, persistent experimental consequences, and explicit resource
constraints. Component and composition qualification, together with exact environment replay,
supports tracing scientific claims back to the experiments and observations that preceded them.
We develop a unified research protocol spanning nine chemical systems, from reaction and
equilibrium studies to characterization, continuous processing, and multistage synthesis and
separation. Agents freely choose experiments and formulate mechanisms, then face
withheld-condition prediction and task-specific decision tests under opaque, aligned, or misindexed prior
information. Cross-system comparisons reveal that useful operating policies, well-supported
mechanisms, and reliable predictions need not develop together. Additional experiments can
refine productive conditions while leaving competing explanations unresolved; prior
information helps or misleads according to the evidence agents acquire and their subsequent
revisions. These findings motivate evaluating scientific agents through the correspondence
between experimental coverage, explanatory scope, and predictive consequences, alongside
task performance. ChemWorld makes these stages jointly observable and experimentally
controllable, providing a foundation for investigating how autonomous agents form, revise,
and use scientific knowledge.

# 1. Introduction

An autonomous scientist should do more than execute a valid procedure or find one productive
condition. It should decide what to measure, identify which relationships the measurements
support, recognize what remains unresolved and use the resulting account to predict new
conditions. These capabilities need not improve together. A productive operating recipe can
coexist with an inaccurate account of the surrounding system. Conversely, an experiment with
poor immediate performance can be valuable if it distinguishes competing explanations.

Language-model agents increasingly plan and execute chemical workflows through software tools
and automated laboratories [@boiko2023autonomous; @bran2024augmenting]. Yet an endpoint alone
cannot reveal whether the agent used a helpful prior, gathered discriminating evidence,
overgeneralized a local observation or simply found a favorable condition. The challenge is
especially acute when the agent chooses its own experiments: the evidence available at the
end of a campaign is itself a consequence of earlier assumptions and decisions.

Controlled investigation requires an experimental environment in which the researcher knows
the world while the agent has a restricted but usable experimental interface. The researcher
must be able to vary initial information independently of the physical system, preserve the
cost and consequences of experimental choices, and inspect complete action–observation
records. ChemWorld supplies these capabilities through composable chemical-process models,
public instrument contracts, evaluator-owned laws and exact replay. Its platform qualification
establishes the reliability of this instrument within a declared model domain
[@qiu2026chemworld]. Here we integrate that foundation with a study of autonomous evidence
acquisition and scientific inference.

The nine-system research programme follows one discovery chain. Agents receive opaque identifiers, aligned
material information or a misindexed version of that information; they then choose their
own experimental conditions and measurements. After the campaign, we preserve their mechanism
reports and evaluate numerical predictions on a fixed set of withheld conditions. A
retrospective interview asks about evidence, alternatives and uncertainty. Electrochemical
campaigns also produce a sealed operating recommendation for independent retesting. The
study compares 12- and 24-experiment budgets and separately assigns electrochemical agents a
discovery or optimization objective. Phase partitioning uses its own discovery task rather
than inheriting an artificial production objective.

The resulting contribution has three parts. First, ChemWorld makes chemical-world composition
and hidden laws experimentally controllable while maintaining explicit public interaction
boundaries. Second, a unified research protocol connects autonomous experimentation to free
scientific explanation, withheld-condition prediction and task-specific decisions. Third,
process records support analyses of how the explored region, the scope of an explanation and
prediction errors relate within the same campaign. The final empirical conclusions will be
determined by the complete planned cohort, including successful research and unsuccessful or
interrupted attempts.

# 2. ChemWorld as an experimental instrument

## 2.1 Composable worlds and information boundaries

ChemWorld represents reaction, thermal, phase, separation, crystallization, distillation,
continuous-flow, electrochemical and observation processes as reusable components. Each
component declares its state, parameter domain, dependencies and interfaces. Compatible
declarations compile into executable worlds with typed operations, instruments, resource
rules, termination conditions and evaluation. Fifteen reference tasks illustrate the
construction space; they do not define its full extent.

We write a world as \(\mathcal W=(W_{\mathrm{pub}},\theta)\), where
\(W_{\mathrm{pub}}\) specifies the public interface and \(\theta\) contains evaluator-owned
material properties, process laws and private initialization. An agent receives a public
experimental contract, not direct access to \(\theta\). Observations expose only the
measurements available through that contract. Public material information is a separate input
that may be withheld, aligned or misindexed without changing the physical system.

This separation supports two distinct experimental controls. A **world intervention** changes
a private physical law under a matched public interface. An **information intervention**
changes the supplied description while holding the physical world fixed. The current
three-arm study uses the latter within each world. Platform demonstrations of world forks
establish an available experimental capability; they are not additional agent comparisons in
the current cohort.

## 2.2 Experimental consequences and replay

Experimental actions alter a persistent physical state and consume declared resources.
Instrument use can also consume samples or change what is available for subsequent operations.
The runtime validates actions and installs a candidate transition only when its applicable
checks pass. Invalid actions retain the committed physical state and incur only the declared
attempt consequences. Public observations and evaluator records remain separate projections
of this execution.

The evaluator retains submitted actions, transaction outcomes, state transitions,
measurements, resource changes and termination. Exact replay reconstructs the bound
environment and action sequence, including recorded failures. It does not regenerate an
identical stochastic language-model response. These records allow an analyst to ask which
conditions were tested and which observations were available before a subsequent decision,
without reconstructing an unobserved reasoning process from the final answer.

## 2.3 Qualification and its scope

The frozen platform qualification tested reference worlds, generated compositions, modules,
interfaces and invalid inputs. Table 1 reports the existing deterministic denominators.
These checks establish internal execution and accounting properties, not external validation
against physical laboratory measurements.

| Qualification unit | Passed / tested | Meaning |
|---|---:|---|
| Reference task–world units | 64/64 | Complete workflow, resource reconciliation and replay |
| Boundary and categorical recipes | 1,786/1,786 | Execution across declared reference domains |
| Generated compositions | 52/52 | Construction and execution beyond the reference cases |
| Module probes / interface paths | 32/32; 7/7 | Model invariants and cross-component consistency |
| Invalid-action probes / invalid compositions | 192/192; 7/7 | Registered rejection or rollback behavior |

The 52 generated compositions include 18 with topologies absent from the reference registry,
eight non-reference reaction–distillation task–world identities using a registered topology,
and 26 further coverage cases. These categories do not establish an unlimited number of
validated chemical systems. Eight deterministic use cases retained all 89 submitted actions,
including one planned rollback, and eight final assays. A separate agent completed a
15-action lifecycle in a non-reference composition with exact replay. That demonstration
establishes interface usability rather than a model-performance ranking.

The current research campaigns extend the platform with their own public-entry checks and
prediction references. Historical qualification is attached to its frozen execution surface;
it is not a blanket certificate for every subsequent world or protocol modification.

# 3. Autonomous-research framework

## 3.1 Questions, tasks and prior arms

We ask how supplied prior information affects autonomous experimentation, how additional
experimental resources relate to predictive reliability, and how the research objective
changes what an agent learns and delivers. The programme defines nine system-specific
research settings with different scientific commissions. Shared components do not make these
nine independent physical mechanism families, and the framework does not require every
system to have an optimization objective or an experimentally identifiable unique mechanism.

| System | Scientific commission | Knowledge and task consequences |
|---|---|---|
| Electrochemical conversion | Mechanism discovery and effective-conversion optimization | Control-dependent response, efficiency and recommended operation |
| Reaction and thermal processes | Kinetic explanation and safety-constrained synthesis | Competing pathways, actual thermal history and stopping decisions |
| Aqueous equilibrium | Characterize bounded acid-dissociation and precipitation responses | Effective relations, identifiable parameter ranges and uncertainty |
| Resource-limited characterization | Diagnose reaction behavior with limited instruments and samples | Measurement choice, distinguishable explanations and calibrated predictions |
| Phase partitioning | Explain allocation of material between phases | Partition relations, mass accounting and phase selection |
| Continuous flow | Identify feasible operating windows under equipment constraints | Residence-time and thermal effects, boundary prediction and feasible recommendations |
| Reaction and purification | Deliver recovered product under purity and resource constraints | Material fate through extraction, washing and transfer |
| Reaction and crystallization | Deliver new crystals under purity and particle-size requirements | History dependence, seeding and separation consequences |
| Reaction and distillation | Recover acceptable fractions through collection and stopping decisions | Composition trajectories, fraction mixing and energy constraints |

This table defines programme scope, not nine completed agent studies. The scored numerical
cohort in Section 5 covers electrochemistry and partitioning; separately published reaction
records extend the protocol to parameter and structural priors but do not yet include
released prediction references or recommendation retests. The remaining settings retain
their design status until their corresponding experiments are completed.

The scored cohort uses the following system-specific readouts:

| System | Primary commission | Research controls and observations | Post-campaign readouts |
|---|---|---|---|
| Electrochemical conversion | Discover an explanatory and predictive account, or maximize the public balanced-efficiency score, in separate sessions | Materials, potential, current cap, duration and legal operation sequences; intermediate diagnostics and final assays | Free mechanism report; six metrics at 12 withheld conditions; operating recommendation retest; interview |
| Phase partitioning | Explain and predict product allocation between phases | Solvent/extractant choices, phase volumes, mixing and permitted separation/measurement operations | Free mechanism report; two complementary phase fractions at 12 withheld recipes; two decisions reusing those recipes; interview |

Opaque agents receive anonymous material identifiers and the full public operation and
measurement contract. Aligned agents additionally receive correctly indexed nominal material
information. MisIndexed agents receive the corresponding information under a specified
material-index permutation. Arm labels are not disclosed. The aligned dossier supplies
selected marginal properties, not a complete mechanism, every material interaction or a
universally optimal recipe. Therefore, success under Aligned still requires inference, and
failure under MisIndexed does not by itself show that the agent retained the incorrect prior.

For each system we use five predefined world instances. Within a world, all arms share the
physical model and withheld prediction conditions. The entity-prior cohort contains 60
electrochemical campaigns and 30 partition campaigns: five worlds, two budgets, three arms,
and two electrochemical objectives or one partition objective. All **90 campaigns** have
complete source and posttest outcomes at this analysis snapshot. The design also contains a
separate 12-campaign, single-world electrochemical pilot at parameter and structure loci,
scheduled after the entity cohort. It cannot establish five-world parameter or structure
effects, and no partition counterpart is presently included.

## 3.2 Free experimentation under finite resources

Each campaign uses GPT-5.6 Sol at medium reasoning effort in an independent session. Agents
choose their experiments, repetitions, intermediate measurements and grouping strategy.
There is no mandatory hypothesis template or reflection after every batch. An agent may
choose a set of experiments before reading all outcomes; that choice is observable research
behavior. A batch, a laboratory operation, a model response and a feedback-dependent decision
are distinct units.

The two budgets permit 12 or 24 completed experimental batches, the same number of additional
intermediate measurements, and one final assay per batch. The operation allowance and
execution envelope scale with the batch budget. The public contract states that current is a
magnitude cap rather than a guaranteed delivered current. All research notes and posttests
are requested in English. Agent calculations use the supplied public numerical interface;
hidden simulator access and external retrieval are unavailable.

A 24-batch campaign is a fresh session. It is not a continuation of a 12-batch session that
has already seen the posttest. Consequently, budget contrasts compare independent research
realizations under different resource envelopes. They do not measure the marginal value of
adding precisely twelve observations to one fixed existing evidence set.

## 3.3 Sealed reports and withheld-condition evaluation

An electrochemical agent first seals its recommendation by selecting a completed batch.
That recommendation is a primary task output for optimization and a secondary output for
discovery. A separate execution retests the selected procedure in the same world under a
different observation seed. The retest is evaluator-side evidence, not another agent-selected
experiment.

Next, the source agent submits a self-contained mechanism report in unrestricted natural
language, mathematics or pseudocode. The prompt requests variables, relationships,
experimental support, scope, alternatives and unresolved factors without prescribing the
functional form. The report is sealed before numerical prediction questions are revealed.
The original session then predicts outcomes without further laboratory access or truth
feedback. It retains its research context: this is a test of the source agent's predictive
account, not a test of a report-only recipient.

Electrochemical predictions cover 12 fixed conditions balanced between positive and negative
potential, with changes in duration, materials and current cap at a stated loading. Six
metrics are evaluated with point errors and nominal 80% intervals. Partition predictions use
12 fixed recipes, two phase fractions, nominal 90% intervals and two decisions based on the
same query set. Complementary phase fractions do not constitute independent physical
observations. Coverage is interpreted together with interval width; broad intervals alone
do not establish useful uncertainty estimates.

Finally, a three-question interview asks which claims were supported, contradicted or
untested; which additional experiment would discriminate between explanations; and which
evidence or predictions remain unreliable. This interview is retrospective. It cannot
replace the sealed report, change predictions or establish what the agent thought before
an earlier action. A primary LLM-judge endpoint is not part of this running block.

## 3.4 What the design identifies

Prior-arm comparisons measure the combined influence of supplied information on experiment
selection and subsequent inference. Because agents acquire different evidence, final arm
differences do not isolate a reasoning effect conditional on identical data. Trajectories
can nevertheless establish observable sequences: an agent tested a condition, received a
measurement, selected its next experiments and later made a scientific claim. A counterfactual
claim that a particular supplied observation would have repaired the error would require an
additional matched-evidence intervention.

Mechanism reports, predictions and task performance are distinct outputs. In particular,
the recommendation is sealed before the mechanism report, and predictions retain the full
source context. Their association cannot identify the causal contribution of the written
report or demonstrate information loss during report compression. A report-only transfer or
matched Raw/report comparison would address a different question and is not silently
included in the present denominator.

# 4. Analysis framework

We organize analysis around three questions rather than a prespecified story of universal
agent failure.

**Where did the agent seek evidence?** For each campaign, reconstruct tested materials and
conditions, measurements, repetitions and observable feedback opportunities. In
electrochemistry, distinguish potential sign from coverage of the active window within a
sign. Testing one unproductive positive potential is not equivalent to testing the positive
domain. Report the actual experimental sequence alongside the aggregate coverage.

**How far did its explanation extend beyond that evidence?** Extract explicit claims from the
sealed mechanism report, attach their cited batches and distinguish supported relationships,
contradictions, untested extrapolations and acknowledged alternatives. A descriptive account
must also permit uncertainty and mechanisms that are observationally indistinguishable under
the available interventions. The evaluator's implementation is not the sole acceptable
scientific wording. Quantitative mechanism-scoring rules remain an analysis-development
task and must be specified before coding the remaining reports; retrospective code development
and illustrative case selection will be disclosed.

**Did its predictions and task outputs remain reliable?** Present metric-specific errors and
interval calibration by world, arm, budget and assigned goal. Show electrochemical potential
domains separately and retain partition decision outcomes alongside continuous errors.
Compare recommendation retests within electrochemistry. Do not combine scores across systems
or define a post hoc total intelligence score.

The campaign is the observational unit for agent outputs. Queries, metrics and batches within
a campaign are correlated readouts, not additional independent agents. The five world instances
within each system share model-family structure; they do not represent five independent
chemistry families. Paired world-level contrasts and their variation will be more informative
than treating all prediction entries as independent replicates. One realization per cell
also limits separation of arm or budget effects from agent stochasticity.

All source failures remain visible. Diagnosed infrastructure recoveries preserve the original
attempt, its physical work and available token accounting. Recovery outcomes do not overwrite
failed originals. The analysis separates first attempts, recovered logical sources
and resource totals, and discloses sensitivity to recovery handling. Wall-clock scheduling
changes are operational amendments rather than changes to the chemical questions.

The analysis below includes each system's complete scheduled world prefix and retains its
entire factorial coverage. Its scope is
defined by scheduling and completeness, not performance. Campaign-level metrics receive equal
weight; paired comparisons hold world, prior arm and the other assigned factor fixed. We
report directions and magnitudes descriptively, without treating repeated queries or the
multiple conditions within a world as independent replications. A sensitivity table retains
only contrasts in which both original attempts completed. This removes recovery exposure but
also reduces coverage; it is not a randomized comparison of recovery procedures.

# 5. Results — developing as the fixed queue completes

> Analysis snapshot: 19 September 2026, 17:59 +08:00. Sections 5.1–5.4 use all 90 entity-prior
> campaigns, with 1,620 source batches and 270 posttests. Sixty-eight campaigns completed on
> their first attempt; 22 used retained infrastructure recoveries (17 EC and five PA).
> The separately scheduled P/S pilot is outside these comparisons. This development analysis
> and the illustrative trajectory analysis are exploratory, not formal confirmation.

## 5.1 A qualified instrument supports distinct scientific commissions

The platform results in Section 2 establish finite construction coverage, complete lifecycles
and replay. For the present research protocol, all 60 public-entry checks and all 120 fixed
prediction-reference batches completed their preparation checks. A partition-reference replay
configuration error was repaired against the retained original trajectory before agent
execution. This verifies the reference path; it is not a scientific performance result for
the agents. The complete cohort contains 60 electrochemical and 30 partition campaigns,
covering every arm and budget in their selected worlds and both electrochemical assignments.
All 90 campaigns have verified source replay and all three posttests. The 60 electrochemical
recommendation retests also replay exactly. Abandoned attempts, replay and retests are charged
separately from the 1,620 effective source experiments. The P/S pilot contributes no samples
to these entity-prior comparisons.

## 5.2 Additional experiments have condition-dependent value

Table 2 compares independent 12- and 24-experiment sessions across all arms in the complete
world blocks. Partition-fraction MAE falls from 0.08291 to 0.02379 on average, a 71.3%
reduction, with lower error in 13 of 15 matched world–arm conditions. The exceptions are
aligned conditions in the second world (0.03332 to 0.03491) and fifth world
(0.04829 to 0.08256). Their task-specific decisions are already correct at both budgets.
Across all partition conditions, correct decision readouts increase from 25/30 to 30/30;
these reuse prediction questions and
are not additional independent experiments.

| System and assignment | Budget | Mean prediction MAE | Empirical interval coverage | Mean interval width | Task readout |
|---|---:|---:|---:|---:|---|
| Electrochemistry, discovery | 12 | 0.17378 | 61.1% | 0.19831 | Retest score 0.53638 |
| Electrochemistry, discovery | 24 | 0.11222 | 71.7% | 0.22007 | Retest score 0.54903 |
| Electrochemistry, optimization | 12 | 0.17811 | 55.6% | 0.19935 | Retest score 0.66404 |
| Electrochemistry, optimization | 24 | 0.10818 | 73.9% | 0.20814 | Retest score 0.74792 |
| Phase partitioning, discovery | 12 | 0.08291 | 78.3% | 0.25122 | 25/30 decisions correct |
| Phase partitioning, discovery | 24 | 0.02379 | 98.9% | 0.18553 | 30/30 decisions correct |

Each row averages 15 campaigns. Electrochemical predictions refer to the public score and
nominal 80% intervals; partition predictions refer to organic-phase product fraction and
nominal 90% intervals. Their errors are not pooled. Full metric-specific and campaign-level
results are retained in the accompanying analysis. Complementary phase fractions do not
double the independent prediction denominator.

Electrochemical discovery score MAE decreases in 11/15 matched conditions, with a mean
reduction of 35.4%. Optimization score MAE decreases in 12/15, with a mean reduction of 39.3%.
Across all six electrochemical outcomes, 24 experiments yield lower MAE in 11–12 of 15
discovery contrasts and 11–14 of 15 optimization contrasts. The dominant descriptive pattern
is improvement with a larger budget, with meaningful exceptions: discovery mean error rises
from 0.15909 to 0.17380 in the fifth world, and optimization mean error rises from 0.15094 to
0.16482 in the first. The
comparison changes the full budget envelope and uses separate sessions; it is not a learning
curve obtained by extending a common 12-experiment prefix.

Prediction intervals also differ by system. Partition coverage rises from 78.3% to 98.9%
while intervals narrow; its nominal target is 90%. Electrochemical score intervals cover
61.1%/55.6% of queries under discovery/optimization at 12 experiments and 71.7%/73.9% at 24,
below their nominal 80% target in each aggregate. Lower point error therefore does not by
itself establish reliable uncertainty estimates. These are empirical coverages over the
fixed, correlated query sets, not independent repeated-sampling calibration trials.

## 5.3 Better operating recommendations do not imply better prediction

The optimization assignment produces a higher recommendation retest score in 26 of 30
matched world–arm–budget comparisons with the discovery assignment. However, its subsequent
score-prediction MAE is lower in only 14 of 30 comparisons. In 13 pairs the recommendation
improves while prediction error worsens; in another 13 both improve. Thus the frequent
operating advantage has no corresponding uniform predictive ordering. This observation is
not restricted to score prediction: across the other five measured outcomes, optimization
has lower MAE in 11–16 of the same 30 contrasts per outcome. Neither assignment
dominates broad prediction, and the data do not establish a universal conflict between
optimization and understanding.

For example, the first world's aligned optimization condition improves its retest score from
0.73620 at 12 experiments to 0.77910 at 24, while prediction MAE worsens from 0.05723 to 0.17917
and interval coverage falls from 91.7% to 41.7%. Conversely, the second world's misindexed
optimization condition improves both retest score (0.67930 to 0.79824) and prediction MAE
(0.13889 to 0.05460). The recommendation is sealed before the report and prediction questions;
these differences do not measure the causal value of the written mechanism report.

Removing every contrast containing a recovered campaign leaves 17 objective comparisons:
optimization has the higher retest score in 15/17, but lower prediction MAE in only 8/17.
Seven of these pairs have a better recommendation and a worse prediction. The corresponding
first-attempt-only budget counts are 4/5 improved for EC discovery, 8/11
for EC optimization and 8/10 for partitioning. These sensitivity results retain the qualitative
distinctions while exposing the smaller, incomplete comparison set.

## 5.4 Supplied information has no uniform performance ordering

Across the five electrochemical worlds, misindexed information has the lowest mean
score-prediction MAE under the discovery assignment at both budgets: 0.13206 at 12 and
0.07133 at 24, versus 0.19393/0.14521 for aligned and 0.19534/0.12011 for opaque information.
Misindexed beats opaque in 4/5 worlds at each budget. Under optimization, aligned information
has the lowest mean MAE (0.15612/0.09961) and the highest mean recommendation score
(0.75512/0.79539); it beats misindexed prediction MAE in 4/5 worlds at each budget.
The assignment therefore changes the aggregate ordering within the same physical world set.

In partitioning, aligned information has the lowest mean MAE at 12 experiments (0.07124),
but at 24 its mean error is 0.02962, compared with 0.02106 for opaque and 0.02071 for
misindexed information. Aligned still beats each alternative in 3/5 individual worlds at 24;
the mean ordering depends on error magnitudes, including its fifth-world exception.
The first world's best arm changes from opaque to aligned, whereas the second world's changes
from aligned to opaque. These
comparisons use score MAE and organic-fraction MAE respectively and do not imply the same
ordering for every metric or scientific claim.

Correctly indexed nominal information is therefore not sufficient to guarantee the lowest
prediction error, and misindexing does not preclude an accurate result. The current data
measure the combined consequences of information, evidence acquisition and subsequent
inference. They do not isolate the effect of prior information on reasoning with identical
observations, and one realization per condition cannot separate all arm differences from
stochastic experimental choices.

## 5.5 A local failure can become an overly broad scientific account

One opaque electrochemical discovery campaign in the second world began at +1.5 V and
observed very poor performance. It subsequently tested −1.5, −0.5 and −2.5 V, then concentrated
the remaining experiments at −0.5 V while varying other conditions. Only one of its twelve
batches tested a positive potential. The sealed mechanism report described a cathodic
conversion and treated the positive direction as effectively inactive. Its selectivity MAE
was 0.01765 on negative-potential queries but 0.82634 on positive-potential queries.

This trace documents sparse regional exploration, an overly broad explanation and strongly
asymmetric prediction error in the same campaign. It does not establish an immutable internal
belief, prove that one corrective observation would repair the error, or show that all prior
arms exhibit the same failure. A systematic account requires the complete denominator of
campaigns satisfying an explicit observable definition, including successful campaigns that
explore or correctly qualify the omitted region. Merely counting positive-potential batches
is insufficient: first-world aligned and misindexed discovery campaigns at 24 experiments
each include two positive settings, but their score MAEs are 0.23245 and 0.03676 respectively.
They test different potentials and acquire different evidence. Coverage must therefore be
interpreted relative to actual tested conditions rather than a binary sign count alone.

## 5.6 Reaction studies extend the evidence beyond material-index interventions

Published reaction records cover four scheduled worlds, two prior loci, two goals and three
arms. All 48 sources completed twelve batches, while 47 have complete sealed posttests; one
retained source lacks a valid mechanism report. Unlike the entity-prior cohort, these sources
intervene on a local temperature-response claim or a reversible-pathway hypothesis. The
prediction questions probe time, temperature, catalyst loading, thermal order and quenching.
Reference truth and independent recommendation retests remain withheld by this block's
protocol, so these records currently support process analysis rather than prediction rankings.

The retained source operations show how experimental freedom was used. Only three of the
48 campaigns varied the catalyst-to-reagent ratio; thirteen measured between successive
heating operations. These counts do not establish an optimal experimental design or prove
insufficient inference. They identify which interventions and temporal observations are
available when evaluating the scope of a subsequent mechanism claim.

Illustrative reports also show revision and acknowledged ambiguity. A misindexed parameter
discovery report in the first world restricts a supplied high-temperature performance claim
after observing lower score and higher risk at 440 K than at 390 K. Because the supplied
claim is local, this does not itself prove rejection throughout its reference neighborhood.
A misindexed structural report in the fourth world retains reversal as an unresolved
alternative, while identifying stronger observed support for product degradation and noting
the absence of a direct reverse-flux experiment. Such qualifications must be retained alongside
overgeneralization cases; an unresolved mechanism is not automatically an agent failure.

Even task outcomes require a separate endpoint: optimization has a higher observed score
for its selected source batch in only 5/12 goal contrasts at each prior locus. These are
exploration observations, not independent retests, and cannot be pooled with the
electrochemical recommendation results. The reaction records therefore do not establish a
universal optimization advantage or a cross-system law of information loss.

## 5.7 Cohort results to complete

The entity-prior numerical analysis now includes every planned cell, recoveries, per-world
prior-arm comparisons, paired budgets and electrochemical goals. The remaining empirical
integration consists of the explicitly exploratory, single-world parameter/structure pilot
and mechanism-report analysis with observable coding rules and limitations. Final figures
must retain all conditions and disclose the exploratory selection of illustrative cases.
No unrun system, fresh-recipient study or new model family is counted as completed evidence.

# 6. Discussion

The integrated contribution is an experimental instrument together with a study that uses
its control and observability. Composable worlds make the domain extensible. The separation
between private laws and public information makes prior interventions meaningful. Persistent
state and resource accounting preserve the consequences of scientific choices. Complete
records connect the experiments actually performed to the explanation and predictions
eventually submitted. Platform reliability and agent capability remain separate evidential
questions even when presented in one article.

The complete entity-prior cohort separates an operating advantage from predictive ordering, while
the retained trajectories motivate examining the scope of acquired evidence. A model can
devote many experiments to a locally useful region
and then make claims that extend beyond it. Additional experiments can broaden that evidence
or refine the same narrow region. The relevant empirical question is how often these
behaviors occur, under which information and task conditions, and with what predictive or
decision consequences. A single striking failure cannot answer those distributional questions.

The current design also places limits on an information-loss interpretation. Evidence that
was never acquired, information omitted by a tool response, an unsupported written claim and
an inaccurate prediction are different events. Our records permit several of them to be
located, but an association among them does not establish a causal information bottleneck.
In particular, report compression and downstream report use require separately controlled
information delivery. Successful counterexamples and unresolved cases will remain part of
the account.

ChemWorld uses explicit simulated model families with declared validity domains. Internal
conservation and replay do not validate universal chemistry or physical-laboratory transfer.
The current agent cohort covers two systems, one model configuration and one realization per
cell. The larger platform capability set is not a claim of equivalent agent coverage.
Furthermore, the nominal prior packets expose selected properties rather than complete
ground truth, and the 12/24 comparison changes the research resource envelope. These limits
define what the completed study can support and which future experiments would address a
different question.

# 7. Relation to existing work

Autonomous laboratory agents demonstrate execution and discovery on real materials
[@boiko2023autonomous; @bran2024augmenting]. Reaction-optimization and virtual-chemistry
environments provide repeatable objective evaluation and interactive benches
[@felton2021summit; @beeler2024chemgymrl]. Scientific-discovery environments investigate active
experimentation and inference [@jansen2024discoveryworld; @gandhi2025boxinggym]. The proposed
comparison should focus on the actual experimental controls each environment provides:
world construction, interventions on prior information, stateful experimental consequences
and observable links between evidence and scientific outputs. Predictive accuracy and
decision quality can differ in established decision-focused formulations
[@elmachtoub2022spo]; here the agent also chooses the evidence on which both depend.

> Editorial task: condense and reconcile the two existing literature sections, verify the
> closest current comparisons, and describe overlap with the earlier ChemWorld platform
> manuscript explicitly. No claim of being the first or uniquely capable platform is needed.

# Authoring notes — excluded from submission prose

## Main figures and allocation

| Figure | Scientific purpose | Content and readiness |
|---|---|---|
| 1. Controlled worlds and autonomous research | Explain the combined contribution | Components and public/private separation; distinct world versus information interventions; autonomous campaign followed by sealed report, prediction and interview; recommendation shown before the report |
| 2. Instrument qualification and research scope | Establish reliability and prevent denominator confusion | Frozen qualification counts; finite component domain; a separate map of the two current research systems and their task commissions |
| 3. Priors, resources and scientific outcomes | Present the complete cohort | Per-world arm comparisons at each budget; separate panels for EC predictions, EC retests and PA predictions/decisions; all failures visible |
| 4. Exploration and explanatory scope | Explain observable success and failure patterns | Operating-region coverage, report claims and domain-specific prediction errors; paired successful and unsuccessful examples with disclosed selection |
| 5. Discovery and optimization objectives | Test the specific within-EC question | Goal contrasts within world/arm/budget; prediction versus recommendation outcomes, without imposing a tradeoff |

Target allocation before venue formatting: approximately one quarter of substantive text for
the platform and its qualification, one quarter for study design, and the remainder for
results, interpretation and limitations. Figures 3–5 depend on the final cohort; this is a
display plan, not fabricated finished evidence. Full operation schemas, qualification
details, prompts, query definitions and retained incidents belong in appendices.

## Evidence disposition and integration boundary

- Reuse the platform manuscript's world definition, composition vocabulary, interface,
  transaction/replay account and qualified evidence. Condense implementation exposition while
  retaining its declared model boundaries. Do not rerun old qualification solely to merge prose.
- Make the current three-arm autonomous-research cohort the behavioral core. It has a different
  runtime/design history from the frozen platform release; report that distinction in methods.
- Historical fixed-expression, response-surface and information-disclosure studies remain
  available under their original protocols. They do not supply missing cells in this cohort,
  establish unrestricted mechanism discovery, or turn an incomplete public interface into an
  agent deficit. Include a historical comparison only if it answers a precise question in the
  new paper; otherwise retain its report outside the main narrative.
- The earlier platform manuscript and both existing PDF exports remain their own frozen
  artifacts. This file is the working source for the new integrated paper. Author metadata
  follows the existing Work II author list. Final metadata confirmation,
  cross-manuscript overlap disclosure, complete literature verification and a new unified
  build/export remain to be finalized; the old exporters do not yet consume this file.

## Source navigation

Current generated evidence is resolved through [the artifact bindings](../configs/current.json),
not selected by a version-looking filename. The platform bindings are under `publication`;
the running study is under `work_ii.w2_132_ec_pa_english_matrix`.

- [Platform manuscript](experimental_intelligence_v1_manuscript.md)
- [Platform work and frozen scope](../workstreams/arxiv_v1/FIRST_PAPER_TODOLIST.md)
- [Integrated author story and next writing steps](prior_discovery_story_zh.md)
- [Work II task authority](../workstreams/flagship_tasks/WORK_II_TODOLIST.md)
- [Current study note and execution amendments](../workstreams/flagship_tasks/WORK_II_EC_PA_FIVE_WORLD_NOTE.md)
- [Live study report](../workstreams/flagship_tasks/reports/work-ii-ec-pa-five-world-en-20260919/REPORT.md)
- [Complete-world block analysis](../workstreams/flagship_tasks/reports/work-ii-ec-pa-five-world-en-20260919/COMPLETED_BLOCK_ANALYSIS.md)
- [Published reaction-record synthesis](../workstreams/flagship_tasks/reports/work-ii-rx-remote-synthesis-20260919/REPORT.md)
- [Machine-readable campaign metrics and contrasts](../workstreams/flagship_tasks/reports/work-ii-ec-pa-five-world-en-20260919/completed-block-analysis.json)
- [Historical manuscript](prior_discovery_manuscript.md)
- [Historical results index](../workstreams/flagship_tasks/WORK_II_PAPER_RESULTS_ZH.md)

Drafting-source checks: qualification counts read from the three current platform reports;
metrics generated from all 90 entity-prior campaign results, checked against the matrix
summary and retained source results, including recovery-sensitive contrasts;
the electrochemical scope example checked against its experimental potentials and sealed
mechanism report. Eighteen primary prediction-table values, six task readouts and all local
links were checked; four focused analysis tests passed. Independent mechanism annotation,
pilot integration and final manuscript export remain outstanding. No new physical experiment
or provider session was started to write this draft.
