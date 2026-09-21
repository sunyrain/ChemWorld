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
bibliography: chemworld_integrated_references.bib
keywords: "autonomous scientific discovery; scientific agents; experimental design; chemical simulation; prior information; uncertainty calibration"
tldr: "ChemWorld makes autonomous chemical research controllable and traceable, revealing that better operating recommendations, predictive accuracy, and calibrated uncertainty can diverge."
draft_status: "Integrated review manuscript; observed six-system development evidence; 21 September 2026"
---

# Abstract

Autonomous scientific discovery requires turning limited experiments into knowledge that
predicts new interventions. This ability is difficult to evaluate in real laboratories,
where mechanisms are incompletely known and agents choose their own evidence. We introduce
ChemWorld, a programmable framework combining evaluator-known process laws, persistent
experimental state, explicit resources, and independently controlled public information.
Composable process and observation models and exact environment replay connect scientific
claims to the experiments that precede them. We use this instrument to study 240 autonomous
research campaigns across six chemical system families, with system-specific objectives
and opaque, aligned, or misindexed prior information. Agents freely select experiments and
formulate mechanisms before predicting withheld conditions. We first show that operational
achievement and predictive knowledge can diverge: electrochemical optimization improves
recommendation retests in 26 of 30 matched comparisons but improves score prediction in
only 14. Larger research budgets reduce prediction error in electrochemistry and phase
partitioning, while substantial response-specific errors persist in crystallization.
Prior information helps in some tasks and hurts in others, without a common ordering.
Finally, comparisons against the agents' own observed data reveal selective extrapolation
failures: all 30 crystallization purity predictions lose to a public-observation mean,
whereas net-recovery predictions beat it in 26 campaigns. The low variation of withheld
purity targets explains the strength of this simple reference. Together, these results
motivate evaluating autonomous science through the linked but distinct abilities to
achieve objectives, predict interventions, and express warranted uncertainty. ChemWorld
provides a controlled basis for investigating how experimental evidence constrains
scientific accounts.

# 1. Introduction

An autonomous scientist must decide which experiments to perform and what the resulting
observations justify. Finding one productive condition is useful, but it does not establish
that the surrounding system is understood. A local operating rule may fail under a change
of material, process history, or measurement regime. Conversely, an experiment with poor
immediate performance may be valuable because it distinguishes competing explanations.
Evaluating autonomous research therefore requires following both experimental achievement
and the knowledge an agent can use beyond its chosen experiments.

Language-model agents can now plan chemical procedures, use specialized tools, and interact
with automated laboratories [@boiko2023autonomous; @bran2024augmenting;
@szymanski2023alab]. These developments make the relationship between action and
understanding an empirical question. An agent's final performance combines the information
it was given, the evidence it chose to acquire, and its subsequent interpretation. In a
physical laboratory, the relevant mechanism is usually only partly known; repeating the
same research process under a different prior is expensive, and equivalent starting states
are difficult to ensure. A final task score alone cannot locate where an unsuccessful
scientific account arose.

We present ChemWorld as an experimental instrument for this problem. Its worlds combine
chemical-process models, instruments, persistent material states, and resource rules. The
researcher controls private process laws and public information separately, while an agent
interacts through laboratory operations and measurements. This separation enables matched
studies of different information conditions in the same world. Complete execution records
and exact environment replay preserve what was done, what was measured, and what remained
available at each step.

We use the platform to study a single agent configuration across six system families:
electrochemical conversion, phase partitioning, reaction and thermal processing, aqueous
equilibrium, crystallization, and purification. The tasks reflect their systems. Reaction
and electrochemical studies separately assign discovery and optimization objectives;
equilibrium and partitioning emphasize characterization; downstream processing requires
quality-constrained delivery. Each campaign ends with a free-form mechanistic account,
withheld-condition predictions, and an evidence-focused retrospective interview. Where an
operating recommendation is required, it is sealed before this assessment and independently
retested.

The principal empirical finding is that operational quality, prediction, and uncertainty
can have different orderings. More experimental resources improve several prediction
endpoints, but do not make every response variable reliable. Aligned information is useful
in some settings without dominating across goals, worlds, or metrics. These results argue
for evaluating scientific research as connected capabilities whose relationships must be
measured, rather than inferred from one successful endpoint.

The paper makes three contributions: a composable, qualified instrument with separate
physical and information controls; a common assessment sequence that preserves autonomous
experiment selection and unrestricted mechanism expression across scientific commissions;
and complete selected cohorts showing how operational and predictive outcomes diverge.
Unfavorable comparisons and incomplete source campaigns remain part of the evidence.

The argument proceeds from what counts as successful research to what might improve
it. After introducing the instrument and protocol, we compare task achievement with
prediction (Section 4), examine larger research budgets (Section 5), and test supplied
prior information (Section 6). We then relate prediction failures to the observations
and accounts that preceded them (Section 7). This progression separates established
outcome patterns from hypotheses about why they occur.

# 2. ChemWorld as an experimental instrument

## 2.1 Constructing worlds with known laws and restricted observations

ChemWorld represents reaction, thermal, phase, separation, crystallization, distillation,
continuous-flow, electrochemical, and observation processes as reusable components.
Components declare their states, parameter domains, dependencies, and interfaces.
Compatible declarations compile into executable worlds with legal operations, instruments,
resource rules, and termination and evaluation conditions. Fifteen reference tasks
illustrate this construction space. The broader research programme defines nine task
families, including resource-limited characterization, continuous flow, and distillation;
the present autonomous-agent evidence covers six of them. Task families can share physical
components and are not independent chemical laws.

Write a world as $\mathcal W=(W_{\mathrm{pub}},\theta)$, where
$W_{\mathrm{pub}}$ specifies the public experimental interface and $\theta$ contains
private material properties, process parameters, and initialization. The agent receives
usable operation and instrument contracts and observes measurements generated through
those contracts, without reading $\theta$ or inspecting the simulator implementation.
Knowledge of the internal model belongs to the evaluator, not to the participant.

This design supports two separate interventions. A **world intervention** changes a
private law while preserving a matched public interface. An **information intervention**
changes the supplied description while holding the world fixed. The platform includes six
matched demonstrations of private-law forks. The three-arm campaigns studied here use
information interventions within each world; the fork demonstrations establish a platform
capability and do not increase the agent-study sample size.

![Controlled worlds and autonomous assessment. The evaluator controls physical laws and supplied information separately. Agents retain freedom over experimental actions and mechanism expression. Prediction follows a sealed report but retains the full research context; it is not a report-only transfer test.](figures/integrated-results/framework.pdf){width=100%}

## 2.2 Experiments have persistent consequences

Laboratory operations alter a persistent physical state and consume resources. Sampling
can remove material; separation changes where material resides; thermal and cooling histories
can affect later observations. Instruments expose specific measurements rather than an
unrestricted state vector. Two campaigns with the same number of batches can therefore
acquire different evidence and leave different material available for subsequent actions.

The runtime validates an action and commits its candidate transition only when the
applicable checks pass. A rejected action retains the committed physical state while
incurring the declared attempt consequences. Public observations and private evaluator
records are distinct projections of the same execution. Records retain actions,
transaction outcomes, measurements, resource changes, and termination. Exact replay
reconstructs the bound environment and action sequence, including rejected actions. It
does not regenerate the language model's words or imply deterministic agent behavior.

A scientific claim can thus be traced to a particular intervention and measurement, and
an apparent discovery can be checked against what the agent actually had access to.
Environmental validity, scientific correctness, and agent success remain separate properties.

## 2.3 Qualification establishes an internal domain of validity

The platform's frozen qualification covers reference worlds, generated compositions,
component invariants, interfaces, and invalid inputs (Table 1). All counts refer to
finite declared domains. They establish internal consistency and execution properties,
not agreement with arbitrary wet-laboratory chemistry.

| Qualification unit | Passed / tested | Property examined |
|---|---:|---|
| Reference task-world units | 64 / 64 | Workflow, resources, replay |
| Boundary and categorical recipes | 1,786 / 1,786 | Declared-domain execution |
| Generated compositions | 52 / 52 | Construction beyond reference instances |
| Module probes; interface paths | 32 / 32; 7 / 7 | Component and interface consistency |
| Invalid-action probes | 192 / 192 | Registered rejection or rollback |
| Invalid compositions | 7 / 7 | Incompatible constructions rejected |

Table 1. Frozen platform qualification. These are software and model checks, not autonomous
research campaigns or independent scientific discoveries.

The generated cases include 18 topologies absent from the reference registry, eight new
task-world identities using a registered reaction-distillation topology, and 26 additional
coverage cases. Eight deterministic use cases retain 89 submitted actions, 88 committed
transitions, one planned rollback, and eight final assays. A separate agent demonstration
completes a 15-action lifecycle in a non-reference composition with exact replay. These
studies show construction and execution beyond reference examples; they do not rank agents.

Each subsequent research block has its own public-interface, reference-execution, and
replay checks. These verify that declared resources are delivered, information treatments
leave physics unchanged, queries execute legally, and relevant response differences are
accessible. No qualification rule requires the tested agent to succeed or an arm to win.
Platform repairs require the affected qualification to be repeated; a historical release
is not a certificate for every later execution surface.

# 3. Autonomous research design

## 3.1 System-specific commissions and matched information conditions

The study comprises 240 scheduled research campaigns across six system families and eight
study blocks (Appendix A.1). Every block uses five world instances and three information arms.
The same physical world, available operations, and withheld-condition questions are used
across arms within a block. World identities and treatment labels remain evaluator-side.

**Opaque** supplies the public experimental contract and anonymous material identifiers,
without the instance-specific dossier under test. It does not remove general chemical
knowledge or information in tool descriptions. **Aligned** adds nominal information
associated with the intended entities, parameters, or structural relations; it is not a
complete simulator specification. **MisIndexed** applies the block's fixed reassignment
or mismatch to that information. It is a controlled alternative dossier, not arbitrary
false text.

The treatment's locus is distinct from its arm. Entity-level (E) interventions change
associations between anonymous materials and descriptors. Parameter-level (P) interventions
concern an effective parameter or local response claim; structural (S) interventions
concern process relationships. Each E, P, or S study therefore contains Opaque, Aligned,
and MisIndexed arms. The purification system abbreviation P is distinct from the
parameter-prior label P.

The complete campaign matrix, assay denominators, and source shortfalls are reported
in Appendix A.1. The following commissions determine what successful research means.

EC agents vary materials, potential, current cap, duration, and legal operation sequences.
Optimization targets the public balanced-efficiency score; discovery targets an explanatory
and predictive account. RX agents control materials, catalyst loading, actual thermal
history, measurements, and termination or quenching. Its parameter-prior study concerns a
local temperature-response claim; its structural study concerns a reversible-pathway
hypothesis. Both goals yield an operating recommendation, secondary to discovery where
applicable.

PA asks how product is allocated between phases under changes in materials, phase volumes,
and processing. EQ concerns amount, volume, concentration, staged additions, dissociation,
and precipitation. Its entity-prior block fixes a shared reaction topology and varies
the joint effective-property bundle associated with each medium selector. Neither imposes an artificial yield-optimization objective. C seeks
seed-excluded crystal recovery subject to purity at least 0.80 and fines fraction at most
0.50, with particles present. P seeks recovery from the original charge subject to purity
at least 0.80. C recovery divides recovered product net of seed mass by the target product
present before separation; it differs from P's original-charge recovery and overall yield.

## 3.2 Free experimentation under finite resources

All campaigns use GPT-5.6 Sol with medium reasoning effort in independent sessions. Agents
choose conditions, repetitions, intermediate measurements, and grouping. They may fit a
model using a public numerical tool or describe mechanisms in other forms. No fixed
equation family, candidate-mechanism menu, or mandatory per-batch reflection is imposed.
An agent can plan several experiments before requesting results. A batch, tool operation,
model response, and decision made after feedback are therefore different units.

A campaign permits 12 or 24 experimental batches, a matching allowance of additional
instrument uses, and one final assay per completed batch. Additional measurements are
optional and allocated freely within the public contract. Operations, material stocks,
execution time, and computational allowances are separately bounded. Larger-batch
conditions also receive larger execution envelopes; they do not hold computation fixed.
Agents cannot access the hidden simulator, repository, or external retrieval. Invalid
actions and their resource consumption remain recorded.

The 24-batch condition is a fresh session, not a continuation after a 12-batch campaign's
assessment. Budget contrasts compare complete research realizations under different
resource envelopes, not the isolated value of twelve extra observations. English outputs
are requested throughout; retained RX and EQ assessment prompts include Chinese
instructions requesting English answers. Prompt language and calculator budgets are
documented in Appendix A rather than assumed identical across systems.

## 3.3 Reports, predictions, reflection, and recommendation retests

For EC, RX, C, and P, the agent selects a completed batch as its operating recommendation
before the mechanism report. The evaluator executes the selected procedure separately
in the same world with a different observation seed. A retest measures the procedure's
observed performance; it does not establish global optimality, repeatability across many
trials, or robustness to new worlds.

Every campaign then follows this sequence:

1. **K1, mechanism report.** The agent gives a self-contained account in natural language,
   mathematics, or pseudocode, covering variables, relationships, experimental support,
   applicability, alternatives, and unresolved factors. No internal simulator vocabulary
   is required.
2. **Q, withheld-condition prediction.** After K1 is sealed, the agent predicts twelve
   fixed independent new batches, giving point estimates and intervals. Questions are
   selected before the source campaign and fixed across matched conditions. Laboratory
   access is disabled; no target values or scores are returned.
3. **K2, retrospective review.** After Q is sealed, the agent discusses tested claims,
   a proposed discriminating experiment, and unreliable or unused evidence. The shorter
   protocol has three questions; RX and EQ use seven themes.

Bounded EQ/P additionally seals a structured equilibrium supplement, yielding fifteen
extra submissions. Canonical EQ/S uses unrestricted K1 reports, without a closed-set
family-classification endpoint. A superseded EQ pilot with a different participant
contract is excluded from the primary cohort.

The original context is retained through K1, Q, and K2. Predictions consequently test
the source agent with its full research history, not what a new recipient can recover
from its report alone. K2 cannot revise predictions, and retrospective statements do not
establish what the agent believed during earlier experiments. Reports support
interpretation; no uniform mechanism-correctness or primary LLM-judge score is claimed.

## 3.4 Outcomes, references, and analysis units

We report response-specific prediction error, interval coverage and width, and task
outcomes separately. For campaign $c$ and response $m$, point error is

$$
\operatorname{MAE}_{cm}=\frac{1}{12}\sum_{q=1}^{12}
\left|\hat y_{cqm}-y^{\mathrm{ref}}_{qm}\right|.
$$

The reference target follows each block's contract (Table A2). RX and EQ compare point
predictions to five-repeat means and measure interval coverage across individual
reference observations. EC and P use fixed seeded reference observations; PA and C use
underlying pre-sampling response values. These different targets should not be pooled
into a common accuracy or calibration score.

Appendix A.2 lists every response, reference target, and nominal interval level.

Campaign metrics receive equal weight within a reported condition. Goal contrasts match
world, arm, budget, and locus; budget contrasts match world, arm, and goal. All scheduled
arms and world-level variation are shown. RX and EQ macro errors average their own
response metrics equally. The score-only RX goal contrast is an additional descriptive
reanalysis aligning that endpoint with EC; the original macro comparison is also retained.

There is one agent realization per cell and five world clusters per system, with multiple
conditions reusing each world. Batches, queries, metrics, and goals are correlated
readouts. We report descriptive magnitudes and paired directions without treating queries
as independent replicates or claiming population-wide significance. Infrastructure
recoveries retain their original attempts and resource records; unfavorable scientific
results are not replaced. Two source-budget shortfalls remain explicitly marked in the
summaries. These agent studies are development evidence, distinct from the platform's
frozen qualification.

## 3.5 A sequence of scientific questions

The experimental chapters follow four questions (Table 2). These are complementary
views of the completed studies, not four new cohorts or a sequence of causal exclusions.
The same campaigns contribute to multiple analyses, so their evidence is not independent.

| Chapter | Question | Comparison used |
|---|---|---|
| 4: Achievement | Does a better procedure imply better prediction? | Matched EC/RX goals; P constrained delivery |
| 5: Resources | Which errors respond to more research? | EC, PA, C: independent 12/24 sessions |
| 6: Prior information | When does supplied knowledge help? | Opaque/Aligned/MisIndexed within each block |
| 7: Evidence use | How do forecasts relate to acquired evidence? | C same-source references; C/EC traces; P paired query |

Table 2. Study logic. The full eight-block matrix is in Appendix A.1. Each chapter
states its comparison and interpretive limits before motivating the next question.

# 4. Task achievement and predictive knowledge can diverge

Does finding a better operating condition imply learning more useful scientific
relationships? We first change the assigned objective while preserving the world,
information arm, budget, and assessment. EC and RX supply this matched goal comparison.
P then clarifies how to interpret operational achievement when the scientific commission
itself contains a quality constraint. P is a separate delivery study, not another
discovery-versus-optimization contrast.

## 4.1 Changing the research objective separates two outcomes

Electrochemistry provides the clearest separation between operational improvement and
predictive accuracy. Across 30 matched goal comparisons, optimization yields a higher
independent recommendation retest score in 26, but lower score-prediction MAE in only
14. Thirteen comparisons improve both endpoints; another thirteen improve the retest
while worsening prediction (Figure 2). At 24 batches, mean retest score is 0.74792 under
optimization and 0.54903 under discovery, while score-prediction MAEs are much closer,
0.10818 and 0.11222.

The pattern is not confined to one favorable error definition. Across EC's other five
prediction responses, optimization wins in 11 to 16 of 30 matched comparisons. Removing
all comparisons involving infrastructure-recovered sessions leaves better retests in
15 of 17 pairs but better score prediction in only eight; seven pairs retain the
better-retest/worse-prediction pattern. This smaller, less balanced sensitivity subset
supports the descriptive pattern rather than estimating recovery's causal effect.

RX establishes a boundary on the interpretation. Optimization improves retests in nine
of 30 matched comparisons, score prediction in eight, and six-metric macro error in six.
Five comparisons improve retests while worsening each prediction readout. Optimization
is therefore neither a uniformly better operating strategy across these tasks nor
necessarily a tradeoff against prediction. Operational and predictive outputs must be
measured separately: their relationship changes with the system and assignment.

![Goal contrasts with the same prediction endpoint. Points compare optimization with discovery in matched conditions; colors denote arms and shapes denote five worlds. Rightward means a better retest, upward means worse score prediction. Each panel contains 30 pairs clustered in five worlds. EC includes two budgets and RX two prior loci; scores and reference targets differ, so magnitudes are not pooled.](figures/integrated-results/goals.pdf){width=100%}

## 4.2 A useful outcome must satisfy the actual scientific commission

Purification makes the distinction between outcome dimensions concrete. Aligned
recommendations achieve purity at least 0.80 in three of five worlds, compared with
none for Opaque or MisIndexed. Yet Aligned's mean original-charge recovery is 0.04455,
compared with 0.12373 and 0.32105, respectively (Figure 3). The largest recovery is
not the best delivery under the stated constraint. One Opaque retest has purity
0.7992, close to the threshold; continuous endpoints are essential alongside
categorical counts, especially with one noisy retest per recommendation.

Predictive ordering also depends on the response. Aligned has the lowest mean purity
MAE, while Opaque has the lowest recovery MAE (Table 3). Removing pairs involving the
nonconforming P source retains the directions of these mean contrasts, with four
world pairs remaining for comparisons against Opaque.

| Arm | Purity MAE | Recovery MAE | Purity coverage | Recovery coverage | Eligible retests |
|---|---:|---:|---:|---:|---:|
| Opaque | 0.22396 | 0.06677 | 51.7% | 56.7% | 0 / 5 |
| Aligned | 0.18830 | 0.06865 | 53.3% | 51.7% | 3 / 5 |
| MisIndexed | 0.25078 | 0.07271 | 50.0% | 53.3% | 0 / 5 |

Table 3. Purification prediction and retest outcomes. Nominal coverage is 80%, against
fixed seeded observations. All fifteen recommendations execute legally; execution
validity is distinct from meeting the scientific objective.

Across arms and responses, nominal 80% intervals cover only 50.0% to 56.7% of targets.
Thus even the interpretation of operational success requires multiple responses:
recovery without sufficient purity does not satisfy this commission, and a qualifying
recipe does not establish reliable predictions of either response.

![Purification delivery and uncertainty. Left: all fifteen recommendation retests, with the purity threshold dashed. Right: campaign-level interval coverage and arm means; the dashed line is nominal 80%. World markers and arm colors follow Figure 2; a cross marks the source shortfall.](figures/integrated-results/purification.pdf){width=100%}

The goal experiments establish a separation between achievement and prediction, while
the delivery study shows why achievement must respect the system's constraints. The
next question is whether a larger research budget narrows these gaps. This motivates a
complementary comparison rather than a claim that the preceding experiments identified
the cause of predictive failure.

# 5. More research helps, but does not resolve every prediction failure

We compare independent 12- and 24-batch campaigns in EC, PA, and C, matching world,
arm, and goal. Each readout has fifteen pairs nested in five worlds. This asks what
changes when the research envelope expands; it does not force the agent to acquire a
particular additional set of observations. RX, EQ, and P have no matched 24-batch cohort
and are not used to answer this question.

## 5.1 Larger budgets improve electrochemical and partition predictions

Increasing the budget from 12 to 24 lowers mean score-prediction MAE by 35.4% for EC
discovery and 39.3% for EC optimization. PA organic-fraction error falls by 71.3%
(Table 4). Improvements occur in 11 of 15 matched EC discovery conditions, 12 of 15
EC optimization conditions, and 13 of 15 PA conditions. These include all planned
conditions, including those where more resources yield worse prediction.

| Assignment / response | MAE, 12 to 24 | Coverage, 12 to 24 | Width, 12 to 24 |
|---|---:|---:|---:|
| EC discovery / score | 0.17378 to 0.11222 | 61.1% to 71.7% | 0.19831 to 0.22007 |
| EC optimization / score | 0.17811 to 0.10818 | 55.6% to 73.9% | 0.19935 to 0.20814 |
| PA / organic fraction | 0.08291 to 0.02379 | 78.3% to 98.9% | 0.25122 to 0.18553 |
| C / net recovery | 0.10433 to 0.07937 | 67.8% to 71.7% | 0.21313 to 0.21515 |
| C / fines fraction | 0.30999 to 0.27000 | 35.6% to 43.9% | 0.32939 to 0.34789 |

Table 4. Budget comparisons average fifteen campaigns per budget. Nominal coverage is
80% except for PA's 90%. C includes its eleven-of-twelve source. Campaign-level data
retain all widths; Appendix B reports every metric and arm.

PA improves both point prediction and decision performance: its two decisions per
campaign rise from 25 of 30 correct to 30 of 30, while intervals narrow. Coverage of
98.9% exceeds nominal 90%, so improved coverage does not imply exact calibration.
EC's 24-batch score coverage remains below nominal at 71.7% and 73.9%. Point accuracy
and uncertainty reliability improve at different rates.

## 5.2 Crystallization retains response-specific errors

Crystallization shows why more resources do not remove every difficulty. Recovery MAE
decreases from 0.10433 to 0.07937, but fines-fraction MAE remains 0.27000 after 24
batches, with only 43.9% coverage for nominal 80% intervals. Recommendations meet
particle and purity criteria in 12 of 15 retests at each budget; ten at each budget
also reach the initial recovery target of 0.10. Mean retest recovery changes from
0.42054 to 0.39939. More resources improve several predictions without a corresponding
improvement in this constrained-delivery endpoint.

The paired conformance sensitivity matters here. Removing C's incomplete 12-batch
source and its matched 24-batch counterpart reduces the net-recovery MAE change from
-0.02496 over fifteen pairs to -0.00782 over fourteen. The size-index change reverses
from -0.00323 to +0.00698. Fines still improve on average in the conforming pairs
(-0.02549), but remain difficult. All thirty C campaigns have fines coverage below
nominal 80%. By contrast, the directions of the EC and PA mean budget improvements
survive removing any one world. These are influence checks, not confidence intervals.

![Budget contrasts. Thin lines connect the same world and arm across independent 12- and 24-batch sessions; dark diamonds show means. Colors follow Figure 2. The cross marks C's source shortfall. EC panels predict score, PA predicts organic fraction, and C predicts fines fraction; vertical scales differ.](figures/integrated-results/budgets.pdf){width=100%}

These comparisons enlarge the research envelope, including computation and allocation.
They do not establish that twelve experiments are inherently insufficient or identify
whether an agent needed broader coverage, replication, a better model, or better use
of evidence already obtained. Retained histories permit those explanations to be
examined without treating them as established by the budget contrast itself.

Budget expansion therefore helps several predictions without producing uniformly
reliable knowledge. We next examine a different resource: information supplied before
experimentation. A useful prior could guide both what to investigate and how to explain
it, but that advantage must be tested within each scientific commission.

# 6. Prior information has conditional value

The three-arm studies ask whether a supplied dossier improves autonomous research in
the same world. Opaque, Aligned, and MisIndexed differ in the dossier under test, while
the public operations, world physics, and assessment remain fixed within each block.
Because agents choose their own experiments, these are comparisons of complete research
processes. They combine any change in evidence acquisition with any change in interpretation.

## 6.1 Aligned parameter information helps RX but hurts bounded EQ

Two parameter-prior studies illustrate the range of effects (Table 5). In RX discovery,
Aligned reduces the within-system macro MAE from 0.10186 to 0.05701, beating Opaque in
four of five worlds. Its mean advantage persists when any one world is removed. RX
optimization also favors Aligned on mean macro error, with four of five paired wins.
These results show that the supplied information can help under both commissions.

In bounded EQ/P, the ordering reverses: Opaque beats both dossier conditions in every
world. Aligned provides a true interval for the world's effective pKa, not its complete
coupled response law. Mean macro MAE rises from 0.01214 under Opaque to 0.04314 under
Aligned. Mean interval coverage falls from 91.3% to 69.0%, while width narrows from
0.07448 to 0.04526. MisIndexed likewise has higher error and narrower intervals than
Opaque. In this block, additional information accompanies less accurate and more
confident prediction; the endpoint comparison does not establish how that arose.

| Study / response | Opaque | Aligned | MisIndexed |
|---|---:|---:|---:|
| RX/P discovery / macro | 0.10186 | 0.05701 | 0.05457 |
| RX/P optimization / macro | 0.13893 | 0.08384 | 0.12967 |
| EQ/P characterization / macro | 0.01214 | 0.04314 | 0.03928 |
| EC/E discovery, 24 / score | 0.12011 | 0.14521 | 0.07133 |
| EC/E optimization, 24 / score | 0.11127 | 0.09961 | 0.11365 |
| C/E, 24 / net recovery | 0.09107 | 0.06839 | 0.07863 |
| C/E, 24 / fines fraction | 0.22808 | 0.27737 | 0.30456 |

Table 5. Selected contrasts illustrating conditional prior value. Entries are mean
MAEs over five worlds; rows have different targets and are not pooled. Appendix A.6
shows the broader world-level comparisons, and Appendix B includes every response.

## 6.2 Rankings also change with the goal and response

EC's entity-prior study changes ranking across goals. MisIndexed has the lowest mean
score-prediction MAE under discovery at both budgets, beating Opaque in four of five
worlds each time. Under optimization, Aligned has the lowest mean score error and
highest mean recommendation score at both budgets. Thus the observed value of a
dossier depends on the commission even within the same system.

C shows a response-level separation. At 24 batches Aligned has the lowest mean
net-recovery error, but Opaque has the lowest fines error and beats MisIndexed on
fines in all five worlds. P similarly favors Aligned for purity prediction and
Opaque for recovery prediction (Table 3). Averaging these endpoints into one ranking
would hide what the information actually helps the agent predict.

Other comparisons are less stable. PA favors Aligned by mean error at 12 batches,
and MisIndexed at 24; at 24, Aligned nevertheless wins against each comparator in
three of five worlds because larger errors in the other worlds change the mean.
EQ/E macro means are 0.01483, 0.01672, and 0.01460 for Opaque, Aligned, and MisIndexed;
EQ/S means are 0.01408, 0.01590, and 0.01345. Their rankings vary across worlds. Close
means are not an equivalence test. RX/S also lacks the consistent aligned advantage
seen in RX/P. The full comparisons preserve these mixed and unfavorable results.

## 6.3 What the information intervention establishes

The supported conclusion is conditional value, not that incorrect information is
intrinsically useful or that parameter priors outperform structural priors. Different
locus studies can change worlds, dossier content, and query designs. Their cross-study
contrasts do not isolate the locus itself. Even within a block, one realization per
cell cannot tell whether a false claim was accepted, rejected, or corrected merely
from the final ranking.

Neither additional budget nor aligned information guarantees uniformly reliable
prediction in the completed studies. To examine where the remaining errors arise,
we now return to the acquired observations and the agent's explicit accounts. This
analysis is descriptive and does not causally separate acquisition from inference.

# 7. Acquired evidence does not always constrain extrapolation

A prediction error can arise because the agent did not obtain relevant evidence,
because the evidence permits several explanations, or because its forecast makes poor
use of available observations. The preceding endpoint contrasts do not distinguish
these possibilities. We use two complementary analyses: public-data prediction
references for every C campaign, followed by explicitly selected trajectories linking
experiments, stated scope, and predictions. No cohort-wide mechanism score is inferred
from these cases.

## 7.1 Simple references expose selective prediction failures

For each C campaign, we compare the agent with the mean of its own public final-assay
observations and a nearest-neighbor predictor built from those observations and public
recipe features. Neither baseline accesses hidden truth during fitting. They reuse the
agent's acquired data, so a baseline advantage cannot be explained by its receiving
additional experiments. They do not, however, reproduce the agent's full prior,
intermediate observations, or computational policy, and are modest empirical references
rather than strong system-identification methods.

| Response / budget | Agent | Public mean | Nearest neighbor | Agent wins vs mean |
|---|---:|---:|---:|---:|
| Net recovery / 12 | 0.10433 | 0.19196 | 0.19000 | 13 / 15 |
| Net recovery / 24 | 0.07937 | 0.15075 | 0.15617 | 13 / 15 |
| Purity / 12 | 0.05029 | 0.00475 | 0.00783 | 0 / 15 |
| Purity / 24 | 0.03679 | 0.00489 | 0.01027 | 0 / 15 |
| Size index / 12 | 0.07085 | 0.02114 | 0.02520 | 0 / 15 |
| Size index / 24 | 0.06762 | 0.02577 | 0.02896 | 4 / 15 |
| Fines fraction / 12 | 0.30999 | 0.31946 | 0.31877 | 9 / 15 |
| Fines fraction / 24 | 0.27000 | 0.31357 | 0.32975 | 12 / 15 |

Table 6. C prediction MAEs from the same acquired final observations. All thirty
campaigns are retained, including the eleven-assay source. The repaired parser restores
two missing baseline evaluations; the other twenty-eight are unchanged. No agent
predictions or source experiments were rerun.

The contrast is selective (Figure 5). Agents improve over the public mean for net
recovery in 26 of 30 campaigns, but lose for purity in all thirty and for size in
26. This does not imply a general inability to use experimental data. Nor does the
purity baseline demonstrate mechanism discovery: withheld purity varies little,
with mean within-world query span approximately 0.02442. A near-constant forecast
is consequently a strong reference for this response.

The signed errors show what goes wrong numerically. Mean source purity is about
0.985 at both budgets and mean withheld purity is 0.98508, yet mean predictions are
0.93544 and 0.94893. In total, 335 of 360 purity forecasts are too low. This is a
query count nested within thirty campaigns and five worlds, not 360 independent
replications. Size is overpredicted by about 0.065 on average and fines are
underpredicted by 0.21890 and 0.18274 at the two budgets. These patterns motivate
examining how the observations constrain extrapolation, without identifying a unique
psychological or mechanistic cause.

![Same-source empirical references reveal response-specific failures in crystallization. Each panel compares agent MAE with the mean of its own public final observations for all thirty campaigns. Points above the diagonal favor the public mean. Colors denote prior arms; circles and triangles denote 12 and 24 batches. The cross marks the eleven-assay source. Panels have different scales and reuse five worlds.](figures/integrated-results/evidence.pdf){width=100%}

## 7.2 Recognizing the limits of evidence does not ensure calibrated forecasts

Consider the fifth-world, 12-batch MisIndexed C campaign, selected retrospectively
because it has the largest purity MAE in the 12-batch cohort. All twelve source
experiments use one solvent and observe purity from 0.97571 to 1.00000, with mean
0.98731. The sealed mechanism report acknowledges that no other solvent was tested
and that its superiority remains an interpretation rather than a demonstrated ranking.
Thus the report explicitly recognizes an important limitation of the evidence.

Nevertheless, the twelve subsequent purity predictions range from 0.84 to 0.94,
with mean 0.86833. The withheld values range from 0.97508 to 0.99962, with mean
0.98566. Every point forecast is low; none of the nominal 80% intervals contains
its target. Agent MAE is 0.11733, compared with 0.00441 for the public mean. The
retrospective interview still acknowledges high observed purity and the untested
solvents.

Changed query procedures mean that high source purity alone does not logically force
high withheld purity. The diagnostic observation is narrower: explicit awareness of
the source values and their limits does not ensure an empirically competitive,
calibrated extrapolation. The report and prediction can be compared without asserting
that the model forgot the data or that writing the report caused information loss.

## 7.3 Sparse exploration can also precede an overbroad account

In one Opaque EC discovery campaign, the first experiment at +1.5 V performs poorly.
The agent tests -1.5, -0.5, and -2.5 V next, then concentrates remaining experiments at
-0.5 V while varying other conditions. Only one of twelve batches tests positive
potential. Its sealed report describes cathodic conversion and treats the positive
direction as effectively inactive. Selectivity MAE is 0.01765 for negative-potential
queries but 0.82634 for positive-potential queries.

This retrospectively selected example links observed coverage, an explanation
extending beyond that coverage, and asymmetric prediction error; it does not estimate
failure prevalence. Nor is counting positive-potential batches sufficient: two other
24-batch discovery campaigns each test two positive settings, yet their score MAEs
are 0.23245 and 0.03676. Their tested locations and acquired evidence differ. An
interpretation must follow actual interventions and claims rather than infer
understanding from a coarse coverage count.

The record does not establish an immutable internal belief or causal information
bottleneck. A systematic mechanism analysis requires consistent coding across all
campaigns, including successful revision and justified unresolved alternatives.
What this trace establishes is directly observable: which experiments occurred,
what the report claimed, and where the predictions failed.

P offers a related intervention-specific diagnostic: thirteen of fifteen campaigns
predict a resolvable purity change for the wash-staging pair when the registered
0.02 small-effect criterion calls for a small change. This is a repeated error on
one contrast, not evidence that the agents share one false mechanism or that wash
staging is physically irrelevant in general.

Taken together, these analyses distinguish observable patterns that a final score
would merge: limited coverage followed by an overbroad claim, explicit recognition
of evidence limits followed by inaccurate extrapolation, and response-specific errors
relative to simple summaries of the available data. They motivate a systematic analysis
of claims and supporting experiments. They do not yet estimate the prevalence of each
failure mechanism or show that one mechanism caused the endpoint dissociations.

# 8. Discussion

## 8.1 Scientific evaluation needs more than a successful endpoint

The dissociations clarify what operating benchmarks measure. A recommendation tests
whether an agent can propose a useful procedure. Withheld-condition prediction tests
its ability to anticipate responses beyond its chosen experiments. Intervals test
whether uncertainty accompanies those predictions. These outputs inform one another
without being interchangeable. Their separation is consistent with the distinction
between prediction loss and downstream decision quality [@elmachtoub2022spo], and
here arises within autonomous experimental research.

This changes how failures should be described. Missing a purity requirement differs
from executing an illegal operation. A useful crystal recipe can coexist with poor
particle predictions. A nominal relation can be useful locally without being a
complete law. Separate physical, informational, and evaluation interfaces preserve
these distinctions rather than collapse them into one success score.

## 8.2 Evidence acquisition and interpretation need separate explanations

An agent may never perform the intervention needed to challenge a claim. It may
instead acquire contradictory evidence and omit it, or recognize that observations
leave several mechanisms possible. Behavioral records can distinguish these
observable situations when claims and observations are explicitly aligned. A final
error or retrospective self-description cannot do so alone.

Known simulator mechanisms help the evaluator design discriminating interventions
and assess consequences. They do not make exact implementation recovery the only
acceptable scientific explanation: multiple accounts can be observationally
equivalent in a restricted domain. Calibrated non-identifiability may be preferable
to an unsupported mechanism. Free-form reports should therefore be evaluated for
supported relationships, scope, contradictions, and predictive consequences, while
allowing unresolved alternatives.

This same-context protocol does not establish information loss caused by writing a
mechanism report. Identifying that effect would require varying what a fresh
recipient receives, such as the full record versus a report, with source evidence
and prediction questions fixed. Separating a prior's influence on experiment
selection from its influence on inference similarly requires matched-evidence
interventions. The platform enables these studies, but they are not current results.

## 8.3 Scope and limitations

The physical models are controlled abstractions qualified within finite domains,
not validated representations of all chemistry. The six studied families share
components; the remaining three task families lack comparable autonomous cohorts.
One model configuration, five worlds per system, and one realization per cell limit
generalization across models and stochastic runs. Fixed reference queries address
specified scientific questions, not every legal intervention.

Protocols also differ in prediction target, nominal interval level, prompt language,
and computation envelope. Within-block comparisons preserve the relevant contract;
absolute cross-system rankings would conflate these differences. Infrastructure
recoveries and source shortfalls remain visible. Selected recovery and conformance
sensitivities support particular comparisons without removing all sources of variation.

Numerical predictions are not a complete evaluation of mechanistic knowledge. Reports
and reflection stages are retained, but systematic claim-level annotation is not
complete. We distinguish quantitative findings from illustrative trajectories and
hypotheses about their causes. The evidence supports separate evaluation dimensions;
it does not yet establish a universal taxonomy or causal theory of information loss.

# 9. Related work

Autonomous chemistry systems demonstrate tool use, planning, and physical execution
by language-model agents and robotic laboratories [@boiko2023autonomous;
@bran2024augmenting; @szymanski2023alab]. ChemWorld complements these efforts with
controlled environments in which the evaluator varies process laws or supplied
information and inspects complete experimental histories, making questions about
research behavior accessible alongside costly physical investigations.

Reaction-optimization and experiment-planning benchmarks provide standardized
objectives and conditions [@felton2021summit; @hase2021olympus]. Interactive digital
chemistry environments expose sequential actions and chemical processes
[@beeler2024chemgymrl]. ChemWorld combines composable process models with separate
public and private interfaces, persistent experimental consequences, and traceable
assessment. This is a complementary emphasis, not a claim that existing environments
lack every such capability.

Scientific-discovery environments increasingly evaluate hypothesis formation,
experimentation, and model discovery, including DiscoveryWorld and BoxingGym
[@jansen2024discoveryworld; @gandhi2025boxinggym]. Our contribution combines controlled
chemical commissions with system-specific objectives and comparisons among
information conditions, prediction, calibration, and recommendation retests. The
empirical contribution lies in the observed relationships and the preserved evidence
needed to inspect them.

# 10. Conclusion

ChemWorld makes the experimental foundations of autonomous scientific claims
observable and controllable. Across the completed six-system study, better operating
procedures, more accurate predictions, and reliable uncertainty do not consistently
emerge together. Additional resources help several prediction tasks, and prior
information changes outcomes, but neither has a uniform effect across commissions
and responses. Same-source empirical references further reveal selective extrapolation
failures that aggregate task scores obscure. Evaluating scientific agents therefore requires recording what they
investigated, what they claim, and what their accounts can predict, alongside the
quality of the procedures they recommend.

# Data and code availability

The platform release is available at
[ChemWorld-Public](https://github.com/sunyrain/ChemWorld-Public). The autonomous-study
analysis uses retained campaign summaries, sealed assessments, reference observations,
and replay records. Accompanying review materials contain figure-generation code,
campaign-level metric tables, and an evidence index connecting comparisons to source
exports. The frozen platform release and later agent-study execution surfaces are
distinct. This review does not imply that all later execution artifacts are already
in the public release. Credentials and raw provider streams are excluded from
distributable materials.

# Appendix A. Protocol detail and evidence handling

## A.1 Complete study matrix

| System / prior locus | Scientific commission | Budgets | Campaigns | Final-assayed batches |
|---|---|---:|---:|---:|
| EC / E: electrochemistry | Discovery; score optimization | 12, 24 | 60 | 1,080 / 1,080 |
| PA / E: phase partitioning | Explain phase allocation | 12, 24 | 30 | 540 / 540 |
| RX / P and S: reaction and thermal processing | Discovery; safety-constrained optimization | 12 | 60 | 720 / 720 |
| EQ / E: medium identity | Characterize entity-conditioned responses | 12 | 15 | 180 / 180 |
| EQ / P: bounded equilibrium | Characterize effective responses | 12 | 15 | 180 / 180 |
| EQ / S: structural equilibrium | Explain response structure | 12 | 15 | 180 / 180 |
| C / E: crystallization | Deliver crystals under quality constraints | 12, 24 | 30 | 539 / 540 |
| P / E: purification | Recover product subject to purity | 12 | 15 | 178 / 180 |
| **Total** | **Six system families** | | **240** | **3,597 / 3,600** |

Table A1. Complete selected study scope. Each campaign has one agent realization. One C
campaign exhausts its solvent stock and discards its twelfth vessel, completing eleven final assays. One P campaign uses all twelve vessel starts
but discards two vessels, leaving ten final assays. All campaigns have sealed mechanism,
prediction, and reflection stages; 238 meet the full source-and-assessment specification.

## A.2 Prediction targets and system-specific questions

| System | Prediction responses | Reference target | Interval level |
|---|---|---|---:|
| EC | Six conversion/efficiency responses, including score | Seeded final observation | 80% |
| PA | Organic and aqueous product fractions | Noiseless pre-sampling fractions | 90% |
| RX | Yield, conversion, selectivity, byproduct signal, risk, score | Five-observation mean; coverage over observations | 80% |
| EQ / E, P and S | Normalized pH, dissociation, precipitation signal | Five-observation mean; coverage over observations | 80% |
| C | Net recovery, purity, size index, fines fraction | Noiseless pre-assay responses | 80% |
| P | Purity, original-charge recovery | Seeded final observation | 80% |

Table A2. Every campaign predicts twelve conditions. PA fractions are complementary,
and its two decision questions reuse the conditions. Reference repeats reduce
observation noise but do not add agent sessions.



EC's twelve conditions balance positive and negative potential while varying duration,
materials, and current cap at a stated loading. Its six responses are selective
product yield, electrochemical selectivity, Faradaic efficiency, transport efficiency,
energy efficiency, and public score. Current is a magnitude cap, not guaranteed
delivered current. PA predicts phase fractions before analytical sampling; sampling
losses and complementary fractions must not be counted as separate discoveries.

RX's twelve paths examine time, temperature, catalyst, heating sequence, and quenching.
Actual thermal telemetry matters: requested boundary temperature need not be realized
reaction temperature. Five reference observations per condition are withheld from
agents, with all source assessments sealed before reference-truth release. RX's 600
reference executions are separate from 720 source batches and 60 retests.

Each EQ block uses twelve questions and five observations per question, giving 300
reference executions. EQ/E crosses three medium identities with three concentrations
and a matched-concentration scale control, assessing entity contrast and concentration
and scale transfer under a fixed common topology. Bounded EQ/P examines effective aqueous relationships; canonical
EQ/S supports response-shape analysis without requiring a named hidden family.
An instrument's equilibrium diagnostic is not the agent's subjective confidence.
The bounded study's effective-parameter supplement is additional to K1/Q/K2 and does
not confer discovery credit for a parameter already supplied as a treatment.

C's twelve conditions form six pairs: material, seed dose, cooling history, prior
thermal history, continued growth, and upstream loading. Its size response is
$\min(d_{50}/250\,\mu\mathrm m,1)$, a bounded number-weighted index rather than a
diameter in micrometres. Fines are particles below 20 micrometres. Quality requires
purity and fines criteria jointly, with particles present; recovery of 0.10 is an
initial feasibility target, not an optimization ceiling. P's six paired interventions
concern multistage recovery, including wash staging. Its original-charge denominator
differs from C's crystallization-stage recovery.

RX and EQ coverage uses individual reference observations while point targets use
means. EC and P use single seeded observations. PA and C prediction coverage concerns
noiseless pre-sampling responses; C recommendation retests use observed assays.
Apparent retest threshold crossings can therefore reflect noise. Macro errors weight a
system's responses equally; normalized scales do not make responses physically or
scientifically interchangeable.

## A.3 Language, numerical tools, and stage budgets

Source briefs and requested reports are English. EC/PA and C/P assessment instructions
are English; RX and EQ K1/Q/K2 instructions include Chinese text requesting English
reports. Within-block arms have the same language contract. Seven-theme K2 reviews
cover treatment claims, influential experiments, competing explanations, one proposed
discriminating experiment, goal-related tradeoffs, unused evidence and uncertainty,
and limitations of the recommendation or scientific account. Three-question versions
combine these themes. The reviews occur after source experiments and sealed
predictions; their length does not provide additional source experiments.

The earlier EC/PA block retains its saved eight-call diagnostic-calculator hard stop;
later blocks disclose 128-attempt assessment allowances. An old EC parameter/structural
supplement encountered the smaller limit and remains an execution failure outside
the primary E cohort. The repair is not retroactively attributed to older sessions.
Public calculation uses agent-accessible information, not hidden targets. Differences
in numerical budgets and deadlines are execution contracts, not scientific findings.

## A.4 Completion, recovery, and exclusions

The primary denominator is 240 scheduled campaigns, not provider attempts. All 720
K1/Q/K2 stages and 165 planned recommendation retests in EC, RX, C, and P are complete,
plus fifteen EQ supplements. Final-assayed source batches total 3,597 of 3,600 planned.
C's second-world 12-batch Opaque source has eleven final assays. P's fifth-world
Opaque source starts twelve vessels, discards two, and completes ten final assays.
Both remain in outcome tables with conformance indicators.

EC/PA has 68 first-attempt and 22 infrastructure-recovered campaigns. Recovery after
transport or host failures retains earlier attempts and consumed resources. Missing
assessment stages resume from saved context when the source is intact; fresh source
replacements are recorded as such. Repeated question delivery and failed-attempt
computation are not silently counted as an original clean attempt. EC goal sensitivity
is reported in the main text. First-attempt-only EC-discovery, EC-optimization, and
PA budget comparisons improve prediction in four of five, eight of eleven, and eight
of ten pairs, respectively; these reduced subsets have uneven coverage.

The current P matrix follows a correction of prepartition inventory handling. Affected
qualification and the entire agent block were restarted under the corrected contract;
earlier apparently successful cells were not selected into the new matrix. All
current source and recommendation trajectories pass inventory, resource, and replay
checks. Its two lawful discards are a source-assay shortfall, not an inventory failure.
The fixed purity-direction rule treats changes of 0.02 or less as small; a numerical
tolerance of $10^{-12}$ corrects floating-point equality handling. Six direction
classifications changed after this correction, with originals preserved. Predictions,
point errors, intervals, retests, and denominators were unchanged.

Historical single-world EC parameter/structural supplements, the closed-set EQ/S pilot,
early C/P development runs, qualification recipes, references, replays, and interrupted
attempts do not enlarge the denominator. Their records remain separate. Frozen platform
qualification is also a separate evidence programme. These counts describe execution
and analysis scope; they are not 240 independent chemistry replications.

## A.5 Baseline correction and trace interpretation

The C empirical references use the same source final observations for all three arms.
A recipe parser originally rejected resource-denial transaction records in two sources.
The correction preserves those attempts as provenance and excludes them from committed
physical recipe features. Recomputing all thirty baselines restores the two missing
evaluations and exactly reproduces the twenty-eight previously available results.
Original trajectories, truth, model answers, and error records are retained; the
correction uses no new simulator or provider calls. Unknown transaction statuses
remain errors. This is an evaluator repair, not a change to a completed experiment.

The EC illustrative trace is the second-world, 12-batch Opaque EC discovery campaign;
its sparse-positive-coverage counterexamples are first-world, 24-batch Aligned and
MisIndexed discovery campaigns. They are retrospectively selected examples, not a
coded prevalence estimate. The additional C case is the fifth-world, 12-batch
MisIndexed campaign, chosen as the largest purity MAE in the 12-batch cohort.
Its extreme error illustrates a failure; it is not a representative sampling rule.

A systematic analysis should attach each mechanistic claim to its experimental
support, contradictory observations, stated domain, and corresponding predictions.
It should distinguish an unperformed discriminating experiment, acquired evidence
omitted from an account, justified unresolved alternatives, and report-prediction
inconsistency. Evaluator knowledge helps identify discriminating interventions; a
claim is not wrong merely for using an equivalent representation. Independent review
can assist this analysis without replacing measured predictions and retests. No
completed cohort-wide mechanism score or causal compression experiment is implied.

## A.6 Full prior overview

![Prior information has no common ordering. Every panel includes five worlds and three arms: Opaque (O), Aligned (A), and MisIndexed (M). Gray lines connect worlds; colored bars show means. Crosses mark source shortfalls. RX and EQ use within-system macro errors; other panels name their response. Scales differ. Appendix B complements these selected readouts with all metric-specific arm means, including EQ/E.](figures/integrated-results/priors.pdf){width=100%}

# References

::: {#refs}
:::
