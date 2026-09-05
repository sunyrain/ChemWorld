---
title: "When Does Experimental Knowledge Improve Scientific Decisions?"
title_line_one: "When Does Experimental Knowledge"
title_line_two: "Improve Scientific Decisions?"
subject: "Experimental knowledge, executable artifacts and decision quality in scientific agents"
keywords: "scientific agents; experimental knowledge; decision quality; executable laws; controlled evaluation"
pdf_author: "Jiangjie Qiu; Yijun Li; Yaotian Yang; Honghao Chen; Wentao Li; Xiaonan Wang"
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
date: ""
bibliography: prior_discovery_references.bib
abstract: |
  Autonomous scientific agents may improve predictions without producing knowledge that reliably
  guides new decisions. We study this distinction in ChemWorld through controlled initial
  descriptions, executable artifacts and complete action plans. Two model configurations each
  entered 135 scheduled campaigns across 45 matched task--world clusters. Prediction errors fell
  on average, but selective-correction criteria were unmet and executable summaries retained
  different amounts of predictive information. In a separate DeepSeek cohort, submitted laws
  selected the optimum in 0/45 scheduled unseen-plan cases, versus 11/45 participant choices.
  A ten-world fixed-evidence factorial intervention then found no supported material benefit of
  numerically fitted-law replacement, with agent/maximizer agreement in all 40 fitted-law pairs.
  We next separated task-only, raw-evidence, model-law-only and fitted-law-only inputs in 160 fresh
  recipients on new candidates in those same worlds. Model-law-only input reduced regret relative
  to task information alone by 0.13723 (95% interval [-0.15584, -0.12257]), meeting the prespecified
  material-benefit criterion, primarily through electrochemistry. Raw evidence and fitted laws
  also improved decisions; a nearest-evidence baseline achieved zero regret in all ten worlds.
  Thus compact artifacts can support decisions independently of their source dialogue on this
  bounded surface, without establishing superiority to raw evidence or retrieval. The results
  distinguish historical law/action disagreement from conditional knowledge utility, while
  leaving cross-protocol causes, new-physical-condition transfer and general repair methods open.


---

# 1. Introduction

Autonomous scientific agents choose experiments, interpret observations and recommend what to
do next. The value of experimental knowledge therefore depends on the decisions it supports.
A useful outcome, an accurate prediction and an executable scientific summary answer different
questions: an agent may find a productive recipe, predict a local response, or express a relation
without being able to select a good plan under new conditions.

This problem matters as language-model agents operate chemistry tools and self-driving
laboratories [@boiko2023autonomous; @bran2024augmenting; @szymanski2023alab; @darvish2025organa;
@song2025chemagents; @vriza2026instruments]. Interactive discovery environments make repeated
experimentation accessible [@jansen2024discoveryworld; @gandhi2025boxinggym; @duan2025scigym;
@zheng2026newtonbench; @yang2026causalab; @batzoglou2026replayscm]. Predict-then-optimize and
decision-focused learning already establish that predictive error and downstream decision loss
can differ [@elmachtoub2022spo; @wilder2019decisionfocused]. The additional question for a
scientific agent is how autonomously acquired evidence, a supplied prior and a submitted
knowledge artifact relate to the actual decision reached by the complete system.

We use ChemWorld to make these objects separately observable. Within a matched cluster, the
external world, public operations and resources remain fixed while the supplied initial
description is opaque, aligned or misspecified at a declared entity, parametric or structural
locus [@qiu2026chemworld]. A persistent session performs experiments and submits predictions
and typed laws. Independent evaluators score those artifacts and execute complete action plans.
The assignment changes participant-facing information; it does not directly manipulate an
unobservable internal belief. The foundation paper establishes the bounded environment and
replay semantics, while this study evaluates complete agent--tool configurations.

The primary study used a fixed DeepSeek-v4-flash experimental-agent configuration, with
135 scheduled cells nested within 45 task--world clusters. An independent GPT-5.6-sol successor
used the same public scientific surface. Matched-evidence controls, unseen-plan selection and
failure-aware information strategies distinguish prediction, artifact fidelity and actual choice.
We then test a proposed intervention directly: hold public evidence fixed and cross the source
of a quadratic law with the rule selecting a plan. This ten-world factorial block finds no
supported material benefit of fitted-law replacement and high agent/maximizer agreement.
A follow-up separates raw evidence from artifact-only delivery on new plans in the same worlds.
Model-generated laws have independent decision value relative to task information alone, although
simple retrieval remains highly competitive. These studies bound general law-use failure without
identifying cross-protocol causes, internal psychological mediation or a new repair algorithm.


```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/prior-discovery/figure-1-prior-to-law.pdf}
\caption{\textbf{Endpoint success does not reveal what the agent learned.}
ChemWorld varies the supplied initial description while fixing the executable world, public rules,
and budget. Held-out predictions, executable knowledge, and unseen-plan decisions are separate
readouts. The diagram describes the design; its arrows do not identify internal belief or causal
mediation through submitted knowledge.}
\label{fig:prior-to-law}
\end{figure*}
```

# 2. Related work

## 2.1 Autonomous experimentation and laboratory agents

Autonomous chemistry systems combine planning, analysis and physical execution. Coscientist,
ChemCrow, A-Lab and instrument-facing agents demonstrate tool use, synthesis planning, materials
search and closed-loop experimentation on real equipment [@boiko2023autonomous; @bran2024augmenting;
@szymanski2023alab; @dai2024mobile; @darvish2025organa; @song2025chemagents]. These systems establish
that AI agents can participate in consequential experimental workflows. Their main evidential strength
is physical validity; their practical constraint for the present question is the cost of repeatedly
constructing matched alternative worlds in which only the correctness of a prior changes.

## 2.2 Virtual chemistry and process environments

Summit and Olympus support repeatable reaction optimization and experimental-design benchmarks, while
PC-Gym exposes nonlinear process-control problems [@felton2021summit; @hase2021olympus;
@bloor2024pcgym]. ChemGymRL provides modular interactive benches for reaction, extraction,
distillation and characterization, enabling reinforcement-learning agents to act within a virtual
chemistry laboratory [@beeler2024chemgymrl]. MADE extends closed-loop discovery benchmarks to
budget-constrained materials settings [@malik2026made]. These systems make experimentation cheaper,
safer and more repeatable than physical execution, but they are generally used to compare policies or
optimize endpoints under one task definition. The present study instead uses world programmability to
hold the executable task fixed while intervening on the agent's initial scientific model.

## 2.3 Interactive scientific-discovery benchmarks

DiscoveryWorld, BoxingGym, SciGym and SciExplorer organize scientific problems around repeated cycles
of hypothesis formation, intervention and inference [@jansen2024discoveryworld;
@gandhi2025boxinggym; @duan2025scigym; @nagele2026sciexplorer]. PhysGym is the closest controlled-prior
neighbor: it varies the level of prior knowledge available to agents exploring interactive physics
systems [@chen2025physgym]. NewtonBench and DiscoverPhysics instead construct counterfactual or
non-canonical physical worlds and ask agents to recover their hidden laws through experimentation
[@zheng2026newtonbench; @wiemann2026discoverphysics]. CausaLab separates task success from recovery of
the underlying structural causal mechanism, while ReplaySCM evaluates executable mechanisms by
held-out interventional replay [@yang2026causalab; @batzoglou2026replayscm]. SciDisco turns
process-verifiable discovery environments into intermediate training signals [@xu2026scidisco].

Another line develops discovery algorithms rather than diagnostic interventions. A probabilistic
formulation treats language-model proposals and revisions as inference over mechanistic simulator
models [@wahl2026probabilistic]. LLM-AutoSciLab couples hypothesis proposal, informative experiment
selection and iterative mechanism refinement, whereas the Model Discovery Agent combines
language-model structure proposals with sequential Monte Carlo, simulation-based inference and
value-of-information design [@kabra2026llmautoscilab; @murphy2026mda]. These methods ask how to make
mechanistic discovery more accurate or data efficient.
The present study asks a complementary causal question about a fixed persistent agent: when the
executable world, action space and resources are held constant, how does changing the correctness of
its supplied initial description alter search, prediction, correction, executable-law recovery and unseen-action
selection?

Decision-focused learning distinguishes prediction error from downstream decision loss
[@elmachtoub2022spo; @wilder2019decisionfocused]. Our additional setting is an agent that acquires
evidence under operational constraints and submits a reusable knowledge artifact. This study
measures artifact and action outcomes; it does not introduce a decision-focused training algorithm.

## 2.4 The unresolved identification problem

Large-scale behavioral evidence already suggests that successful scientific workflows need not be
accompanied by evidence-sensitive, self-correcting reasoning [@riosgarcia2026scientifically]. However,
an observational comparison across systems cannot by itself identify which capability transition produced
the divergence. Three ambiguities remain when endpoint score, belief statement and scientific
understanding are not separated. First, a correct prior can make an agent look like a rapid discoverer
even if it merely confirms supplied information. Second, a wrong prior can improve an endpoint by
encouraging useful exploration without ever being rejected. Third, a verbal law summary can be correct
while the agent's subsequent predictions or actions remain inconsistent with it. A matched
correctness intervention on the initial model, typed checkpoints and evaluator-owned tests are needed
to distinguish these cases. Unlike counterfactual-world benchmarks, the hidden law does not change
within a matched comparison here; unlike prior-availability studies, aligned and misspecified arms
receive equally explicit models and differ at the targeted scientific locus.

# 3. Conceptual framework

## 3.1 Fixed world, programmable initial world model

Each matched comparison begins with one executable world containing a fixed evaluator-owned law. Write
the world as $W=(\mathcal{E},G,\Theta,O,C)$: entities, causal/mechanistic structure, parameters and
dynamics, observation mapping and the authoritative public contract. The participant-facing initial description is encoded as
$M_0=(\widehat{\mathcal{E}},\widehat{G},\widehat{\Theta},\widehat{O},\widehat{S})$, where
$\widehat{S}$ represents assumptions about scope, modularity and compositional applicability. The
public task, action space, actual observation channels, resource card, safety rules and bound
stochastic identity are held constant. We intervene only on one declared component of $M_0$ before
the first experiment. Changing $W$ or the public contract would create a different task; changing one
component of $M_0$ changes supplied information within the same task. Here $M_0$ denotes the
external description, not a measured internal belief state.

The design space contains five scientific layers and one fixed contract boundary; only the
entity, parametric and bounded structural layers have current participant outcomes.

```{=latex}
\begin{table*}[!t]
\centering
\caption{\textbf{Programmable layers of the agent's initial world model.} The external executable world and public contract remain fixed within every matched comparison.}
\label{tab:initial-world-model-layers}
\scriptsize
\begin{tabularx}{\textwidth}{L{0.18\textwidth}Y L{0.29\textwidth}}
\toprule
Initial-model layer & What may be aligned or wrong & Role in this paper \\
\midrule
Entity / ontology & identity--property mappings, entity classes and property bundles & exploratory and prospective tests \\
Structural / mechanistic & causal topology, active process modules and dominant-pathway assumptions & separately prespecified test \\
Parametric & coefficient signs, thresholds, orderings and plausible ranges & separately prespecified test \\
Observation model & instrument mapping, reliability, bias and noise assumptions & qualification screen; no participant outcome \\
Scope / compositionality & applicability domains, invariant modules and transfer boundaries & new-mechanism transfer; unexecuted \\
Contract / resource boundary & budget, safety, action permissions and actual observation interface & authoritative and fixed; never treated as a manipulable prior \\
\bottomrule
\end{tabularx}
\end{table*}
```

Within any selected layer, intervention quality follows the same logic:

- **Opaque:** no additional task-specific claim is supplied for the manipulated layer.
- **Aligned:** incomplete information is directionally consistent with the fixed world.
- **Misspecified:** an equally detailed and equally confident model is wrong at the manipulated layer.

The current entity/ontology implementation realizes the misspecified condition through a misindexed
dossier: the same property bundles, fields, values, wording and confidence language are retained, but
the bundles are permuted across material identifiers. Structural, parametric and observation-model
interventions require their own matched encodings and identifiability validation; they cannot be
declared equivalent to material misindexing after observing the result. Scope/compositionality is
tested only when a learned artifact enters a fresh target context. Experimental evidence remains
explicitly authoritative in all conditions. A wrong initial model is therefore not a trick question
about obedience; it tests whether the agent seeks and uses evidence that can override a plausible
scientific representation.

## 3.2 Operation, experiment and campaign

An operation is one submitted physical or measurement action. A complete experiment begins with a new
batch and ends with a committed final assay or an allowed discard. A discovery campaign comprises
multiple complete experiments under one fixed world, one persistent agent session and one shared
resource ledger. Physical batch state resets between experiments, but the public history, agent
context, hidden law and remaining resources persist.

This distinction matters because repeated operations and experiments inside one campaign are nested
observations, not independent scientific samples. The independent analysis unit is the matched
task-by-world cluster.

## 3.3 Observable outcomes and unresolved dependencies

We distinguish five outcomes that are often collapsed into a single score, while recording the
intermediate transitions that connect them.

1. **Endpoint optimization:** whether the campaign identifies a high-quality experimental outcome.
2. **Predictive recovery:** whether held-out counterfactual prediction error decreases.
3. **Prior correction:** whether evidence selectively improves the wrong-prior condition without
   degrading the correct-prior condition.
4. **Executable-law consistency:** whether the final typed summary executes on prespecified held-out
   coordinates and preserves the quality of the agent's conditional predictions.
5. **Unseen-plan selection:** whether the terminal agent state supports ranking and selecting
   previously unseen, fully specified executable plans rather than merely retrieving an observed
   incumbent.

A conceptual workflow connects these quantities; the arrows below are not estimated causal links:

```{=latex}
\begin{center}
\small initial world model $\rightarrow$ experiment selection $\rightarrow$ evidence acquisition\\
$\rightarrow$ prediction / belief update $\rightarrow$ executable law $\rightarrow$ unseen action selection $\rightarrow$ artifact portability
\end{center}
```

The paper measures prediction error, prediction-to-law compression loss and law/action
inconsistency. These readouts locate observable gaps; they do not identify internal causal failure
locations. The explicit-artifact interventions separately test fixed-evidence replacement and
same-world information deployment; neither identifies transfer across new mechanisms.

An agent can succeed on any subset. In particular, endpoint success without predictive and transfer
validity is classified as local optimization rather than law discovery.

# 4. Study design

## 4.1 Chemical-world cohort and intervention studies

The study is layer-stratified. Its entity/ontology backbone spans electrochemical conversion,
reaction followed by crystallization, reaction followed by distillation, phase-partition discovery
and safety-constrained reaction. Five independently selected public worlds per task yield 25
task-by-world clusters and 75 participant cells across opaque, aligned and misspecified arms.
Parametric/dynamical and structural/mechanistic blocks each contain two independently validated task
families and five worlds per task, adding 30 participant cells per locus. Exploratory, validation
and prospective world instances remain disjoint. A sealed private cohort is an optional stronger study and was
not executed in the current paper.

This design uses ChemWorld's programmability to manipulate different components of $M_0$, but does
not turn the paper into a full factorial benchmark. Every block changes one locus, has its own
identifiability criterion and retains its own denominator:

1. **Initial-model-conditioned free discovery.** Entity interventions span five task
   families; parametric and structural interventions each span two validated task families. A
   cross-locus claim requires evidence from all three prespecified blocks; an entity-only result
   remains entity-specific.
2. **Matched-evidence response.** A cloned-world secondary probe presents the same
   contradictory evidence to each arm and measures conditional response to a bundled packet plus
   extra turn. The analysis includes the unaffected parametric block and a corrected B2
   phase-process block. B2 later failed participant-visible structural identifiability and is retained
   as a numerical--exact-law-expression diagnostic, not a mechanistic-identification test. An earlier structural run was excluded because its evaluator truth source
   omitted the prespecified world intervention. All matched-evidence sessions are independent and
   excluded from the free-discovery denominator.
3. **Executable law and action.** Typed law summaries and held-out predictions test the
   transition from conditional belief to executable relation. Blind incumbent replay tests whether
   a committed recommendation can reproduce observed value, while a separate longitudinal
   open-action assay tests whether the agent can rank previously unseen, fully specified ActionPlans;
   no verbal statement alone counts as discovery.
4. **Explicit-artifact interventions.** A ten-world factorial assay replaces the quadratic
   representation and decision rule with public evidence held fixed. Information separation then
   compares task-only, raw-evidence, model-law-only and fitted-law-only inputs in fresh recipients
   on new plans in the same worlds. These interventions retain their own nested denominators;
   within-world deployment, new-parameter replication and compositional transfer are distinct.

Participant provenance is block-specific. The prospective three-locus cohort and the original 45-cell
open-action matrix use the fixed DeepSeek-v4-flash configuration. A-P and A-S B2 have complete,
separately reported DeepSeek-v4-flash and GPT-5.6-sol formal denominators; the three-locus C2 surface,
the identifiable-law B3 surface and the four-condition action surface also have complete scheduled
denominators for both model configurations. GPT-5.6-sol is the model; Codex denotes the common session
harness. Oracle qualification, truth execution, exact replay, law-capacity fitting and gate-alignment
diagnostics are provider-free. Historical contrasts remain separated by configuration. The artifact
interventions prespecify equal-weight model/repeat means within world; this estimates the studied
mixture of configurations, not provider effects or a leaderboard.

Observation/measurement interventions are reserved as a separate boundary probe. They require
two-task identifiability and an exploratory three-arm study and are not included in the present
denominator. Transfer across changed physical mechanisms remains untested. This preserves a complete
conceptual intervention space without claiming that every programmable coordinate has already been
executed.

Environment validation and participant outcomes form separate evidence layers. Environment tests
establish that the hidden relations are coherent, identifiable and executable through the public
measurement surface. They do not show that an agent discovers those relations.

```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/prior-discovery/figure-2-formal-cohort.pdf}
\caption{\textbf{Layer-stratified study architecture.}
The three loci contribute 25, 10, and 10 independent task--world clusters. Each cluster receives
three supplied-description arms, giving 135 sessions and 1,260 planned complete experiments.
Budgets are per session. Matched-packet, law-evaluation, and action studies retain separate
denominators; later artifact interventions have separate inference units.}
\label{fig:formal-cohort}
\end{figure*}
```

## 4.2 Persistent experimental agent

Each cell is controlled by one persistent agent process across one campaign. After every public
outcome, the participant chooses the next operation through the host-owned laboratory tool. The host
validates schemas, executes transactions, updates resources and protects private state, but does not
select or repair scientific actions.

Campaign length is intervention-specific: entity studies use eight complete experiments with checkpoints after
0, 2, 4, 6 and 8 experiments; parametric studies use ten with checkpoints after 0, 2, 4, 7 and 10; structural studies use twelve
with checkpoints after 0, 3, 6, 9 and 12. These pattern-owned counts and their finite resource cards
were fixed before participant execution. A checkpoint records the
agent's assessment of initial-model reliability at the manipulated layer, predictions, uncertainty,
evidence references, executable law summary and next experimental intent. Checkpoints do not create
additional independent sessions.

## 4.3 Evaluator-owned evidence

The participant predicts four prespecified counterfactual queries per entity checkpoint and 16 per parametric or
structural checkpoint. The evaluator executes each unique task-world query set independently; truth is
shared across prior arms and checkpoints and is never returned to the participant. The primary
prediction error is the mean normalized absolute error across prespecified query-metric pairs. The
held-out evaluation is complete: 420/420 truth executions produced 1,620 query--metric truth values,
and all 675 checkpoints were scored without additional model calls.

The evaluator also executes each final typed law summary on the same prespecified query coordinates.
This produces a separate cell-level record of schema validity, complete query-metric executability,
truth-normalized error, error change relative to the pre-evidence and effective-final checkpoints,
and consistency with the participant's final explicit predictions. These public measures are
descriptive and are reported as executable-law consistency/compression; they do not establish
reusable-law status. A reusable or transferable law would require independent coordinates or a
context-reset transfer test.

After the campaign, the participant commits one completed experiment as its final recommendation.
The evaluator then performs paired blind replay of the observed incumbent and the committed
recommendation. These executions use separate resources and do not enter participant-operation or
independent-sample denominators.

## 4.4 Longitudinal open-action assay

The longitudinal action assay addresses a different estimand from incumbent replay. One persistent
agent first completes 12 autonomous experiments and mechanism checkpoints after 0, 3, 6, 9 and 12
experiments. Only after the final checkpoint is committed does the host reveal eight previously
unseen ActionPlans. Each public plan includes its ordered operations, all submitted parameters,
initial-state assumptions, measurement positions, terminal assay and omitted-operation declarations;
candidate outcomes, evaluator ranks and other-arm evidence remain hidden. The evaluator executes
exactly the public plan and verifies identity among the disclosed, truth-evaluated and executed plans.

The formal DeepSeek multi-task matrix contains three task families, five worlds per task and three initial-model
arms, giving 45 scheduled cells. Each cell contains 12 autonomous experiments and five checkpoints;
42 cells were eligible for action metrics and three crystallization failures remained in the scheduled
denominator. The primary action endpoint is within-world regret of the selected plan; selected rank,
Top-1, complete ranking and law adequacy are reported separately. This matrix is analyzed separately
from the prospective locus tests, and no arm-level inference is made when a world lacks a complete triplet.

A separate causal follow-up prespecified five information conditions within each task--world--prior
stratum: no evidence, stepwise evidence yoked from an autonomous donor, autonomous exploration,
the donor's learned law in a fresh context and a provider-free oracle law in a fresh context. Across
three tasks, five formal worlds and three priors, the intended denominator was 225 sessions; only the
45 autonomous donors would have executed 12 experiments each. Before participant execution, every
task--world required an outcome-disjoint oracle law to reproduce the eight-candidate ordering with
Spearman rank correlation at least 0.80. Failure rejected the control design rather than authorizing
world replacement or revealing an outcome table.

We subsequently evaluated the control rather than weakening this rule. A denser construction used 64
global queries and 256 candidate-neighborhood queries while keeping the fitted model family fixed.
Exposed construction worlds and new prospective worlds remained separate. A final zero-execution
diagnostic re-read all completed 96- and 320-query unit versions and compared the frozen Spearman gate
with Top-1 selection, near-optimality and regret. It added no participant, provider or physical
execution and did not alter any earlier stop decision.

## 4.5 Hypotheses and estimands

Let $E_{a,k}^{(\ell)}$ denote held-out prediction error for initial-model arm $a$, checkpoint $k$ and
intervention locus $\ell$. Each block tests selective evidence-driven correction:

```{=latex}
\[
\begin{aligned}
C_{\ell}={}&
  (E^{(\ell)}_{\mathrm{misspecified,pre}}-E^{(\ell)}_{\mathrm{misspecified,final}})\\
&-(E^{(\ell)}_{\mathrm{aligned,pre}}-E^{(\ell)}_{\mathrm{aligned,final}}).
\end{aligned}
\]
```

The contrast measures how the pre-to-final error gap changes and depends on initial error
headroom. Initial predictions and the particular relation contradicted by evidence are needed
for interpretation; a failed criterion does not establish an absence of correction ability.

For the entity locus, the misspecified arm is instantiated by a prespecified material permutation and $C_{\ell}=C_E$ is the
confirmatory contrast. Success requires the lower confidence bound for the locus-specific contrast to
exceed zero, the wrong-prior condition to improve, and the aligned condition not to deteriorate beyond
a prespecified tolerance. Correct-prior utility, wrong-prior vulnerability and knowledge-to-action
translation form a hierarchical secondary family. A cross-locus conclusion requires concordant,
separately reported entity, parametric and structural results; standardized effects may be synthesized hierarchically,
but raw contrasts are not pooled as if their intervention semantics were identical. Observation-model
results remain a distinct boundary analysis unless evaluated in a separate prespecified study.
Endpoint, calibration, behavior, law-summary, terminal-action, resource and safety outcomes are reported as
separate channels rather than one leaderboard score.

Failed scientific cells remain in the denominator and are not replaced. Confirmatory correction
assigns incomplete post-outcomes the adverse improvement range $[-1,+1]$; last-observation-carried-
forward and zero improvement are observed-point sensitivities only. Only a pure infrastructure
failure without a persisted trajectory may resume under the prespecified attempt cap.

# 5. Exploratory studies establish the identification problem

Development studies were used to discover the inferential traps that the prospective design had to
remove. Across configuration-separated entity-level matrices, explicit initial information changed
where the agent searched and sometimes improved the best observed endpoint, but the ordering was not
aligned, opaque and then misspecified. In the retained five-task development cohort, all 75
trajectories replayed exactly and 69 met the prespecified eligibility criteria. Held-out predictions
usually improved, yet the misspecified arm did not improve more than the aligned arm on average.
Executable summaries frequently lost information present in checkpoint predictions, and blind
recommendations almost always retrieved an observed incumbent. These results are protocol-development
evidence, not part of the prospective denominator and not a cross-system comparison.

The same ambiguity appeared at the parameter level. In a one-world preliminary study, the
misspecified agent tested inside its supplied potential window, obtained a zero score, sharply reduced
its stated confidence in that model and moved the next experiment outside the window. This was
behavioral rejection of a supplied model, but the agent still failed to recover the best
finite-budget policy. Rejecting a wrong prior, improving prediction and recovering a useful law were
therefore not interchangeable outcomes.

These exploratory observations motivated three safeguards in the main study: matched worlds with
equally explicit aligned and misspecified models; evaluator-owned counterfactual predictions rather
than endpoint score or verbal suspicion; and separate assays for executable-law fidelity and terminal
selection among unseen plans. The prospective results below begin from this stricter identification
problem. Exploratory configurations remain archived with their exact denominators and failures but do
not compete with the main knowledge-and-decision results.

# 6. Prediction and executable knowledge

## 6.1 The prospective cohort closes the experimental and evaluator denominators

The prospective analysis combines 120 unaffected sessions with a complete 15-session replacement of
the structural crystallization block after correction of its resource contract. All **135/135**
scheduled sessions produced final records. The participant completed **1,243/1,260** planned
experiments, and **121/135** sessions met the prespecified operational eligibility criteria. The
denominator contains 1,269 closed batch lifecycles: 1,243 ended in a final assay and 26 were
discarded. No dynamic physical failure occurred. Thirteen operations were rejected by the finite
laboratory resource ledger, and 84 attempted operations were not committed. Failures and
right-censoring remain in their assigned denominators.

Every session submitted all five checkpoints, giving **675/675** typed belief snapshots, 6,300
prespecified counterfactual predictions and 24,300 query--metric values. The evaluator independently
completed **420/420** truth queries and scored every checkpoint without additional participant calls.
The cohort therefore permits a continuous analysis from the starting model through search, prediction
and executable summary rather than a comparison of endpoint scores alone.

## 6.2 Priors scaffold search without imposing one performance ordering

A retrospective manipulation analysis shows that the initial-model intervention reached both the
reported belief state and the first experimental trajectory. Pre-evidence prediction errors differed
across arms, although the aligned arm was not uniformly best. More directly, the first complete
recipe differed between aligned and misspecified cells in **45/45** matched task--world clusters,
between opaque and aligned cells in **45/45**, and between opaque and misspecified cells in **44/45**.
Because the design did not include repeated same-arm sessions, exact-recipe divergence is a
trajectory-sensitivity check rather than a new confirmatory estimand; provider stochasticity cannot be
separated from intervention sensitivity at this resolution.

The ensuing campaigns were not simple copies of the first proposal. Across cells, **91.2%** of
completed experiments used a unique recipe, **84.4%** of session optima occurred after the midpoint
and **32.6%** occurred in the final completed experiment. Intermediate measurement was task
appropriate rather than globally absent: 666/1,269 closed lifecycles included a non-final
measurement, comprising 872 instrument uses. These records establish sustained search and
observation. Improvement over the first experiment alone does not isolate feedback learning:
non-adaptive search can improve with additional attempts; budget-matched controls are needed.

Those trajectory changes produced three recurring endpoint patterns. In entity-level partition,
aligned information produced a durable advantage over the misspecified arm: +0.106 on the first
experiment and +0.200 at the best endpoint, both concordant in 5/5 worlds. In structural
crystallization, the aligned model gave a +0.141 first-experiment head start in 5/5 worlds, but the
best-endpoint gap narrowed to +0.055 as the initially disadvantaged arm explored. In structural
partition, both aligned and misspecified descriptions outperformed opaque identifiers while differing
little from one another, consistent with shared search scaffolding rather than correct-model utility.
The remaining task--locus groups were heterogeneous. A correct initial model was therefore neither a
universal advantage nor a stable endpoint ordering.

## 6.3 Predictive learning does not establish selective repair of a wrong starting model

All three intervention loci showed mean pre-to-final prediction-error reductions in every arm. For
the entity locus, reductions were 0.111, 0.097 and 0.097 for opaque, aligned and misspecified cells;
for the parametric locus they were 0.090, 0.033 and 0.065; and for the structural locus they were
0.219, 0.228 and 0.221. The agent acquired predictive information during free discovery.

The prespecified improvement contrast was stricter. Evidence should improve the misspecified arm more than
the aligned arm while preserving aligned performance. This selective-correction criterion failed at
all three loci. Failure-aware point contrasts were **-0.214** for entity, **+0.033** for parametric and
**-0.224** for structural. Confirmatory inference assigned incomplete arm improvements their adverse
interval $[-1,+1]$, so the corresponding contrast could span $[-2,+2]$; last-observation-carried-forward
and zero-improvement summaries were observed-point sensitivities rather than sources of confirmatory
$p$ values. The resulting one-sided locus values were $p=0.990$, $p=0.079$ and $p=1.000$. The positive
parametric direction is a replication hypothesis, not a passed locus. Structural crystallization and
partition also pointed in opposite directions, defeating the required cross-task structural decision.
General predictive learning and selective correction of a wrong starting model are thus empirically
different readouts. The improvement contrast depends on initial error headroom, so the unmet
criterion does not establish an absence of correction ability.

```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/prior-discovery/figure-3-prior-uptake-and-correction.pdf}
\caption{\textbf{Prediction improves, but the evidence does not establish selective repair of the wrong model.}
\textbf{a--c,} Mean pre-evidence and final errors by arm in entity, parametric, and structural
blocks; lines connect aggregate means, not individual trajectories or confidence bounds.
The registered selective-correction criteria are unmet (one-sided $p=0.990,0.079,1.000$), and
initial error limits improvement headroom. First recipes differ in 45/45 aligned--misindexed,
45/45 opaque--aligned, and 44/45 opaque--misindexed clusters; this retrospective check has no
repeated same-arm baseline.}
\label{fig:prior-uptake-correction}
\end{figure*}
```

## 6.4 Matched packets expose a numerical--expression dissociation; B3 tests structure

Free discovery cannot by itself distinguish failure to seek diagnostic evidence from failure to use
evidence once obtained. The matched-evidence assay gives every arm the same packet after a pre-response,
but the packet and added response turn are bundled without a turn-matched no-packet control. It therefore
measures conditional post-packet response rather than a pure evidence-packet effect. In the parametric
block, all five misspecified summaries rejected the supplied high-potential direction and expressed
the peak-and-collapse response after the bundle. The pattern shows that the earlier absence of explicit
repair is not immutable, but it does not isolate the packet from the additional response opportunity.

The corrected B2 DeepSeek assay produced a sharper numerical--expression dissociation. After all three arms received the
same direct phase-process evidence, mean normalized errors fell from 0.2255, 0.2736 and 0.3392 to
**0.0074, 0.0060 and 0.0071** for opaque, aligned and misspecified cells. The misspecified-minus-aligned
update-gain contrast was +0.0645, but only 3/5 worlds were positive (exact one-sided sign-flip
$p=0.125$; descriptive 95% interval $[-0.0557,0.1848]$). This is conditional post-packet numerical
convergence, not a confirmatory arm effect. Retrospective keyword coding of public summaries found that
**0/5** misspecified cells expressed the prespecified 1.75 power law, **1/5** explicitly rejected the
supplied linear form, and **5/5** shifted to a saturation or endpoint model.

A participant-visible identifiability audit changes the interpretation of those expression counts.
Every B2 evidence and scoring query fixed one nominal solvent/extractant pair, the base partition
coefficient was not supplied, and no typed family or exponent field was required. A free-coefficient
linear law is therefore exactly observationally equivalent to the registered 1.75-power law on this
surface, while a constant endpoint baseline already reaches mean MAE 0.00649. The aligned DeepSeek-high
exact-law positive control was only **1/5** and failed its readout criterion. B2 thus establishes low
post-packet error without stable exact-law expression on an underidentifying free-text surface; it
does not localize failure to the agent's internal structural identification.

The matched replication preserved the numerical--expression pattern in GPT-5.6-sol medium. In A-P, the registered
misspecified-minus-aligned update-gain contrast was +0.0309 for DeepSeek (3/5 worlds) and +0.0602 for
GPT (5/5; exact one-sided $p=0.03125$). In A-S B2 it was +0.0645 for DeepSeek (3/5) and +0.0915 for
GPT (4/5; $p=0.0625$), while misspecified exact 1.75-law expression remained **0/5 in each model**.
Aligned exact expression was only 1/5 for DeepSeek high and 0/5 for GPT. We report the two
configurations separately and do not convert this retrospective free-text coding into a structural
recovery or model-superiority test.

A same-harness DeepSeek low-reasoning ablation strengthened the numerical boundary. Its B2 canary
passed 3/3 and formal execution completed **15/15** with no failed sessions. Mean post errors were
0.0067, 0.0069 and 0.0069 for opaque, aligned and misspecified cells; all 15 were below 0.02. The
registered update contrast reversed to **-0.0405** (2/5 positive worlds; exact one-sided
$p=0.8125$; descriptive interval $[-0.1559,0.0749]$), but misspecified exact-law expression remained
**0/5**. Provider-reported reasoning output fell from 506,637 to 400,639 tokens (20.9%) relative to
DeepSeek high on the same block. Thus low reasoning preserved the low-error/exact-expression dissociation while
showing that selective numerical updating is configuration-sensitive. This is a robustness ablation,
not a reasoning-superiority test or a thinking-off experiment.

An independent frozen control then made the 1.75 exponent statistically identifiable under a
registered reference fitter by disclosing
reference coefficients across four nominal pairs and scored a disjoint eight-query roster. After a
3/3 canary, all **30/30** GPT-5.6-sol medium sessions completed (five worlds, three arms, two fresh
sessions per arm and world). Mean post-evidence errors were 0.0367, 0.0215 and 0.0378 for opaque,
aligned and misspecified cells. Joint family--exponent recovery was **0/10**, **5/10** and **0/10**;
the aligned arm had lower world-mean exponent error than each comparator in **5/5** worlds. The
misspecified arm selected the power family in 8/10 sessions but recovered the 1.75 exponent in 0/10,
  showing that a family label alone is not structural identification. Thus reference-fitter-identifiable
evidence partly preserved a correct prior but still did not selectively correct a wrong one.

The same control also tested the evidence-to-action bridge without participant experiments. Only
**2/30** choices were Top-1, both in the same world where no candidate could improve on the visible
evidence incumbent by the registered 0.02 margin. Across the **18** cells in the three worlds where
such an improvement was available, **0/18** selected an action reaching that margin; this included
0/2 eligible cells with joint structural recovery. Structural retention and useful novel action did
not become a monotonic pair.

An independent DeepSeek-high successor then used the same five worlds, three prior arms, two-session
replication, evidence/scoring rosters and action thresholds from its first cell. All 30 scheduled
slots reached terminal records: **17 completed** and **13 participant-schema failures**. Under the
failure-aware denominator, joint family--exponent recovery was **0/30**, Top-1 was **0/30**, mean
  regret was 0.958 and mean post-evidence MAE among completed cells was 0.0928. The corresponding
  GPT-5.6-sol values were 5/30, 2/30, 0.759 and 0.0320. Useful gain was 0/13 versus 0/18 among completed
  evaluable opportunities and 0/18 for both under the fixed scheduled-opportunity rule, which counts
  failures or unavailable rows as zero. These matched-surface differences are descriptive: the differential schema failure is part of
the evaluated agent--provider system and precludes a model-superiority interpretation.

```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/prior-discovery/figure-4-matched-evidence-localization.pdf}
\caption{\textbf{Numerical fit and structural recovery require different tests.}
\textbf{a,} All 15 DeepSeek-high B2 cells before and after the same packet, shown on a log scale;
gray/teal/orange denote opaque/aligned/misindexed arms. All post-packet errors are below 0.02,
but the one-pair surface underidentifies family; low error is not structural recovery.
\textbf{b,} B3 completion, joint family--exponent recovery, Top-1, and useful gain retain all
scheduled opportunities. Counts distinguish 30 sessions from 18 gain opportunities per model,
including 13 DeepSeek schema failures. Configuration contrasts are descriptive.}
\label{fig:matched-evidence-localization}
\end{figure*}
```

## 6.5 Executable laws often lose information present in predictive belief

All **135/135** final typed laws executed on their prespecified continuous coordinates, but
executability did not preserve the information in the agent's conditional predictions. Mean law MAE
was 0.237. Relative to the effective final predictions, executable laws were better in 50 cells,
equal in one and worse in 84; mean law-minus-final error was +0.069. Even in the structural locus,
where pre-to-law improvement was largest, law error remained higher than final explicit-prediction
error on average. The typed interface solved syntax and coverage, not faithful model compression.

A same-domain schema-capacity control localized that loss. For every cell, we fitted the best legal
identity-link typed law directly to the agent's complete final prediction vector and executed it
through the production parser. The full registered basis reproduced the prediction state in
**135/135** cells (mean MAE $4.25\times10^{-13}$), whereas the participant's submitted law differed
from the same prediction state by 0.1539 MAE. Holding the participant's term set fixed reduced that
gap to 0.0114 MAE (58/135 near-exact cells), and leave-one-query-out fitting yielded 0.0788 MAE.
Thus the interface can carry the observed predictive state; most information loss arose during the
agent's distillation into a sparse law, not from schema capacity. Because the full-basis fit uses
coordinates from the same evaluation domain, it is a capacity control rather than evidence of
global mechanistic identification.

Paired blind replay tested a still narrower claim: whether the final commitment reproduced the value
of an observed incumbent. It completed **726/726** executions for 121 evaluable cells; the 14 failed
or right-censored cells remained as unstarted. Recommendations were better, equivalent and worse than
the incumbent in **1/119/1** cells. This demonstrates reliable incumbent retrieval, not selection
beyond the observed campaign. A separate assay is required for unseen plans.

The matched GPT-5.6-sol successor supplied a second complete 135-cell scheduled surface. It reached
**126 completed, 3 failed and 6 right-censored** cells, with 1,253/1,260 participant experiments,
420/420 evaluator truth executions, 669/675 scored checkpoints, 129/135 executable-law evaluations
and 756/810 scheduled blind executions. Its entity, parametric and structural selective-correction
gates all failed, as in DeepSeek. Mean prediction improvement was 0.1329 versus 0.1198 for DeepSeek,
while final prediction error was 0.1614 versus 0.1685. GPT-5.6-sol exhibited lower law MAE, 0.1753
versus 0.2371,
and compression loss from 0.0686 to 0.0142, but blind gain remained approximately zero
(-0.0001 versus -0.0010); its blind better/equivalent/worse counts were 0/125/1. Thus a materially
lower observed executable-law error coexisted with near-zero blind gain. This is a matched
cross-configuration description, not a causal law-quality intervention or provider effect.

The checkpoint interface is part of this evaluated system. Although all checkpoints were eventually
recovered, 888 typed-checkpoint submissions were rejected before acceptance. This burden did not
remove prediction payloads, but it increased context and recovery work. Results therefore apply to
the complete agent--tool configuration rather than the base language model alone.

```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/prior-discovery/figure-5-capability-chain.pdf}
\caption{\textbf{Lower executable-law error coexists with near-zero incumbent gain.}
\textbf{a,} Hollow and filled points show final-prediction and executable-law MAE on the same
law-evaluable cells, grouped by locus and model; connecting lines show compression differences,
not uncertainty. The matched denominators are 135 DeepSeek and 129 GPT laws.
\textbf{b,} Better/equivalent/worse/unavailable incumbent-replay counts retain all 135 scheduled
cells per model; hatching marks unavailable readouts. These are descriptive configuration
contrasts and incumbent replays, not causal artifact effects or unseen-action benefits.}
\label{fig:public-capability-chain}
\end{figure*}
```

# 7. Scientific laws, unseen actions and evaluator validity

## 7.1 Complete plan semantics remove a hidden-workflow explanation

Blind incumbent replay asks whether a recommendation can reproduce an observed batch; it does not
test decisions outside the campaign history. We therefore used a second assay in which the agent
first explores freely for 12 experiments and only then ranks eight unseen plans. Every candidate is a
complete ActionPlan, including ordered operations, submitted parameters, measurement positions and
terminal assay. Public, evaluator-truth and executed plans were verified as identical, and no
evaluator-owned default could silently alter a workflow. Candidate outcomes and ranks remained
hidden. An incorrect ranking therefore cannot be attributed to undisclosed execution semantics.

## 7.2 Executable-law error is not a sufficient proxy for unseen action selection

The formal matrix produced final records for **45/45** scheduled cells across three tasks, five worlds
and three initial-model arms. Independent evaluation completed **240/240** truth executions and
**240/240** exact replays. **42/45** cells were uncontaminated and eligible for action metrics. The
three excluded cells were all crystallization cells: two exhausted agent-selected resources or
process options and one was right-censored by interruption. All three remain in the scheduled
denominator.

```{=latex}
\begin{table*}[!t]
\centering
\caption{\textbf{Formal multi-task unseen-plan matrix.} Rank and regret summaries use the 42 eligible cells; all 45 scheduled cells remain in the denominator and the three crystallization failures are retained. Lower rank and regret are better.}
\label{tab:open-action-matrix}
\scriptsize
\begin{tabular}{lrrrrr}
\toprule
Arm & Scheduled & Eligible & Mean rank & Top-1 & Mean normalized regret \\
\midrule
Opaque & 15 & 14 & 3.14 & 5 & 0.2742 \\
Aligned & 15 & 14 & 3.36 & 3 & 0.2958 \\
Misspecified & 15 & 14 & 3.43 & 3 & 0.3222 \\
\bottomrule
\end{tabular}
\end{table*}
```

Across eligible cells, **11/42** terminal readouts selected the true Top-1 plan; after the three missing
rankings were retained as failures, the scheduled result was **11/45**. Mean selected rank among eligible
cells was 3.31/8 and mean normalized regret was 0.297. The uniform-random rank of 4.5 is a geometric reference,
not a causal baseline: the design contains neither a no-evidence action arm nor a pre-exploration
ranking from the same agent. The study therefore describes post-campaign selection competence but
does not estimate how much exploration or a recovered law caused it.

The joint mechanism--action result exposes the boundary more sharply. **30/42** cells had an
inadequate law and wrong action, **11/42** had an inadequate law but correct action, **1/42** had an
adequate law but wrong action, and **0/42** combined an adequate law with a correct action. The single
law-adequate/wrong-action cell is a counterexample to logical guarantee, not a population estimate of
law sufficiency; correct action also occurred without thresholded law adequacy.

The conclusion did not depend on the 0.10 adequacy cutoff. Across all 42 eligible cells, law MAE had
weak pooled associations with selected rank (Spearman $\rho=-0.073$, task--world cluster-bootstrap
95% interval $[-0.380,0.256]$) and normalized regret ($\rho=-0.133$,
$[-0.452,0.217]$). Task-stratified rank associations reversed direction: $+0.524$ for
electrochemical conversion, $-0.592$ for reaction safety and $-0.007$ for crystallization. Sweeping
the law-MAE threshold from 0.05 to 0.30 increased the adequate-law subset from 1 to 34 cells, yet its
correct-action count rose only from 0 to 9; at no threshold did adequacy become sufficient for a
correct action. The binary four-way table is therefore one readable slice of a continuous,
task-dependent descriptive association rather than an artifact of a single cutoff. It does not
identify a causal law-quality effect.

A decision-aligned reanalysis of the DeepSeek-v4-flash cohort then executed the last-available
executable law from every frozen cell on the same eight candidate plans. Three cells retained an
earlier executable law but had no terminal action ranking.
All **45/45** laws were evaluable, but their implied choices reached the true Top-1 in **0/45** cells,
versus **11/45** for failure-aware participant action. Among the 42 cells with a valid participant
ranking, the participant followed the law-implied Top-1 in only **12/42**. Mean law-implied and
participant failure-aware regret were 0.438 and 0.344; the direction reversed in crystallization.
These quantities separate truth--law error from action-module utilization descriptively. Neither law
quality nor law following was randomized, so they do not estimate a causal law-to-action effect.

Performance varied substantially by task. Electrochemical conversion reached Top-1 in 4/15 cells
with mean rank 3.60, reaction safety in 4/15 with mean rank 2.00, and crystallization in 3/12 with mean
rank 4.58. Every pairwise arm-rank contrast changed sign under some leave-one-cluster-out omission.
Arm means are therefore descriptive, not causal. The bounded result is that complete public action
semantics and autonomous exploration did not yield uniformly reliable ranking of unseen plans.

```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/prior-discovery/figure-6-open-action-formal.pdf}
\caption{\textbf{Law quality and information strategies have distinct decision readouts.}
\textbf{a,} Law-implied versus participant regret in the 45-cell DeepSeek matrix; 42 observed
choices are dots and three missing rankings are crosses above the plotting range. The diagonal
marks equal regret. \textbf{b,} Failure-aware strategy means with valid/scheduled counts.
\textbf{c,} Paired strategy-minus-no-evidence differences with task-stratified world-cluster
bootstrap 95\% intervals, retaining all 45 strata per model. Both autonomous contrasts cross zero.
The strategy block is development evidence; yoked failures prevent a pure acquisition-effect
interpretation. Complete-ranking diagnostics remain in the appendix.}
\label{fig:open-action-formal}
\end{figure*}
```

## 7.3 The repair is sensitivity evidence, not a replacement cell

An independent aligned-arm crystallization repair completed all 12 experiments and produced a
terminal readout, but the agent first proposed an infeasible seeding operation and incurred one
resource rejection before adapting. Its final choice ranked 8/8 with normalized regret 1.0 and
remained in the inadequate-law/wrong-action category. The repair shows that a fresh session can cross
the original interruption while revealing a genuine resource-planning risk. It has a different
trajectory and is not merged into the original 45-cell denominator.

## 7.4 Four-condition strategies expose autonomy and learned-law-only limits

We therefore ran an independent development successor that removed the oracle condition while
preserving the frozen open-action worlds, complete ActionPlans, initial-model arms and action metrics. For each
model, all 45 task--world--prior strata scheduled no evidence, yoked evidence, learned-law-only and
autonomous-exploration conditions, yielding **180 slots per model and 360 total**. DeepSeek reused its
45 immutable open-action donors, of which 42 were eligible; GPT-5.6-sol created a separate 45-donor cohort,
of which 26 were eligible. Donor-dependent slots remain blocked when the corresponding donor failed,
and all recipient failures remain in the scheduled denominator. The models share 26 donor-eligible
strata across 13 task--world clusters.

The primary strategy estimand retains all 45 scheduled strata per model, assigning failure-aware regret
one to donor failure, blocked descendants, recipient failure or a missing ranking. Autonomous-minus-
no-evidence regret was **-0.0913** for DeepSeek-v4-flash (task--world cluster-bootstrap 95% interval
$[-0.2124,0.0388]$) and **+0.1102** for GPT-5.6-sol ($[-0.0533,0.2794]$): directions differed and both
intervals crossed zero. GPT-5.6-sol's all-scheduled yoked-minus-no-evidence and learned-law-minus-
no-evidence estimates were +0.2165 ($[0.0561,0.3878]$) and +0.2459 ($[0.0953,0.3883]$). They are
end-to-end strategy outcomes that include missing donors and system failures, not pure evidence or
artifact effects.

Autonomous-minus-no-evidence also changed sign by task. For electrochemistry, safety and
crystallization, the estimates were -0.2398/-0.4060/+0.3720 for DeepSeek and
+0.0891/-0.2191/+0.4605 for GPT-5.6-sol. The pooled direction therefore masks strong heterogeneity;
all four registered contrasts and their cluster-bootstrap intervals are descriptive and were not
multiplicity-adjusted.

Donor-eligible estimates are availability-conditioned sensitivities because donor eligibility is a
post-treatment variable. On those 42 DeepSeek and 26 GPT-5.6-sol strata, autonomy-minus-no-evidence
was -0.1214 and -0.1379, respectively; equal-task sensitivities were -0.0879 and -0.0259. Yoked
completion was **10/42** and **24/26** admitted recipients. The successor therefore did not establish
a consistent autonomy or learned-law-only benefit and exposed model-specific failure pathways. It remains
a prospective development experiment rather than confirmatory evidence, not a continuation or relabelling of
the stopped five-condition protocol below.

Conditions followed fixed manifest and dependency order rather than randomization or
counterbalancing, and DeepSeek autonomous donors predated their recipient conditions. Provider/time
drift and order effects are therefore not separable from strategy differences.

## 7.5 The original five-condition oracle gate failed before participant execution

The terminal matrix cannot identify whether acquired evidence caused better selection, so we prepared
the separate five-condition follow-up described above. Its provider-free formal stage fixed 15
task--world clusters and 1,680 candidate, checkpoint and oracle-grid truth executions with exact
replay. The first eight clusters completed **896/896** truth executions and exact replays without a
provider call. All eight candidate-opportunity gates passed, and seven oracle laws passed the frozen
rank criterion.

The eighth cluster was a fresh crystallization world. Its outcome-disjoint oracle law achieved
Spearman rank correlation **0.738095** across the eight candidates, below the prespecified **0.80**
threshold; its predicted Top-1 also disagreed with truth, while fit/candidate overlap remained zero.
The formal preparation therefore stopped by design. The remaining seven clusters, operational canary,
all 225 participant sessions and all 540 planned participant experiments were not started, and no
world or unfavorable result was replaced. This result does not estimate a poor participant effect.
It establishes that the current oracle-law control was not robust enough in fresh formal worlds to
support the intended causal decomposition.

## 7.6 A denser oracle grid repairs exposed failures but not prospective ranking

We next tested whether the failure arose from sparse coverage rather than typed-law representation.
The oracle grid was expanded from 96 queries to **320**: 64 global queries plus 256 queries around the
candidate neighborhood. The fitted ExtraTrees family and the frozen Spearman threshold were unchanged,
so the intervention isolated coverage. After a platform-defective partial run was retained and the
evidence-reference limit repaired, the complete construction screen passed **7/7** exposed units with
**2,352/2,352** truth executions and exact replays. All four historical failures were repaired and the
minimum construction Spearman correlation was 0.857143.

Construction success did not transfer to the prospective block. Its first new electrochemical world
completed **336/336** truth executions and exact replays but obtained Spearman correlation **0.714286**,
below the frozen 0.80 gate. The oracle nevertheless selected the true Top-1 action with zero regret;
fit/candidate overlap remained zero and candidate outcomes were not used for fitting. The stop rule
therefore left the remaining 14 prospective clusters unstarted. Increasing coverage repaired known
worlds but did not establish fresh-world complete-ranking validity.

## 7.7 Evaluator-level ranking and decision quality are different estimands

A frozen retrospective diagnostic compared the original ranking decision with action endpoints for all
**16/16** completed oracle unit versions from the 96- and 320-query studies. Original Spearman and Top-1
values were reproduced exactly without new truth execution. Among the eight fresh 96-query formal
preparation units, **7/8** passed the rank gate but only **1/8** selected the true Top-1 action and **3/8**
selected within 0.01 of the optimum; six units were rank-pass/action-wrong. Conversely, the first fresh
320-query unit was rank-fail/action-correct with normalized regret zero.

The disagreement is bidirectional. Complete-ranking correlation measures global ordering, whereas the
causal study needs a positive control for the selected action and its decision loss. The original gate
and stop decisions remain valid for their frozen protocol, but the diagnostic shows that future control
qualification must prospectively prioritize regret, near-optimal selection and near-tie-aware ordering,
with full-ranking correlation retained as a secondary diagnostic.

## 7.8 Fixed-evidence representation and decision interventions

The factorial intervention holds twelve public experiments per world fixed and crosses two
quadratic representations---a source model's law (L) and a public ridge fit (F)---with two decision
rules: a fresh same-model agent (A) and a shared deterministic maximizer (X). Five new worlds per
task, two model configurations and two source repeats yield 40 source states nested within ten
worlds. Sources never see the eight terminal candidates; fresh recipients receive the evidence,
candidates and designated law. All 120 provider sessions, 160 condition slots and 200 physical
executions with exact replay completed without failure or replacement.

The prespecified primary contrast, F-X minus L-X, was -0.00538 (95\% world-bootstrap interval
[-0.01630, 0.00061]). Its upper endpoint did not fall below -0.01, so the block does not support
the proposed material benefit (Fig.~\ref{fig:m1-replication}). The task means were -0.01087 in
electrochemistry and +0.00010 in crystallization; the negative effect was concentrated in one
electrochemistry world. Regret uses a fixed utility scale of one, with models and repeats averaged
within world. Five worlds per task limit the bootstrap approximation.

Fresh-agent and maximizer choices agreed in 39/40 model-law pairs and all 40/40 fitted-law pairs.
F-X minus F-A was consequently zero in every observed pair; its degenerate bootstrap interval is
not a population-equivalence guarantee. Fitted-law selection had mean regret 0.00425, compared
with 0.00354 for nearest public evidence and 0.11109 for exact expected uniform-random selection.
The fitted method therefore shows no observed advantage over the simple retrieval baseline.
These are local response-surface decisions with fixed acquisition. They supply a boundary to
general law-use failure. Because raw evidence accompanies the artifacts here, independent artifact
utility requires the information-separated test below; historical protocol differences remain unresolved.

```{=latex}
\begin{figure*}[t]
\centering
\includegraphics[width=\textwidth]{figures/prior-discovery/figure-7-m1-replication.pdf}
\caption{\textbf{Fixed-evidence intervention did not establish a material repair benefit.}
\textbf{a,} Every world has its own row. Hollow and filled points show model-law and fitted-law
regret under the same maximizer, averaged over two models and two repeats; concentric points
denote equality. Blue denotes electrochemistry and purple crystallization.
\textbf{b,} Colored points are individual world effects; black diamonds and lines show means
and prespecified intervals (95\% primary; 98.75\% secondary). The dotted primary reference is
-0.01. Interaction is $(R_{\mathrm{F-X}}-R_{\mathrm{L-X}})-(R_{\mathrm{F-A}}-R_{\mathrm{L-A}})$ in regret. Zero-width intervals describe
observed equality, not population equivalence. All 160 selections were available; repeats
do not increase the ten-world denominator.}
\label{fig:m1-replication}
\end{figure*}
```

```{=latex}
\begin{table*}[t]
\centering
\caption{\textbf{Prespecified factorial contrasts.} Differences use the fixed regret scale.
The primary material threshold is -0.01. Secondary intervals adjust for four comparisons.}
\begin{tabular}{@{}lrl@{}}
\toprule
Contrast & Mean difference & Interval \\
\midrule
F-X minus L-X (primary) & -0.005384 & 95\% [-0.016303, 0.000614] \\
L-X minus L-A & +0.000331 & 98.75\% [0.000000, 0.001323] \\
F-A minus L-A & -0.005053 & 98.75\% [-0.017329, 0.001582] \\
F-X minus F-A & 0.000000 & 98.75\% [0.000000, 0.000000] \\
Interaction & -0.000331 & 98.75\% [-0.001323, 0.000000] \\
\bottomrule
\end{tabular}
\end{table*}
```

## 7.9 Information separation reveals independent artifact value

We reused all ten factorial worlds and forty sealed sources, fixed eight new candidates per
world, and assigned fresh recipients task information alone, raw evidence, model law alone (L)
or fitted law alone (F). Only the raw condition received observations; law conditions received
six original coefficients without source dialogue or provenance labels. All 160 sessions and
80 hidden evaluations with exact replay completed, with no new recipient measurements.

The primary L-minus-none regret contrast was -0.13723 (95\% interval [-0.15584, -0.12257]),
meeting the prespecified material-benefit criterion (Fig.~\ref{fig:m3-portability}). Nine world
means improved and one was zero; task means were -0.25937 for electrochemistry and -0.01509 for
crystallization. These remain ten reused worlds, not ten additional independent replications.
Mean regrets for none/raw/L/F were 0.14727/0.01124/0.01004/0.01459. Raw and F also improved on
none under adjusted intervals. L minus raw was -0.00120 (99\% interval [-0.02353, 0.00951]); this
establishes neither superiority nor equivalence. Nearest public evidence selected the measured
optimum in all ten worlds, so these data do not establish an advantage over retrieval.

Law-only deployment used 392,101 input tokens versus 541,225 for raw evidence, a descriptive
27.6\% reduction; source acquisition and generation costs had already been incurred. Model-law
recipients followed the deterministic maximizer in 40/40 states and fitted-law recipients in
39/40. The result supports same-world context portability of the delivered artifact, without
identifying internal law use, transfer across changed mechanisms or experimental savings.

```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/prior-discovery/figure-8-m3-portability.pdf}
\caption{\textbf{Artifacts support fresh decisions, while retrieval remains a strong baseline.}
\textbf{a,} Dots show world means over two models and two repeats per information condition;
diamonds show task means. All 160 selections are available. Nearest evidence has zero regret in
all ten worlds. \textbf{b,} Colored points show paired world effects; black diamonds and lines
show means and prespecified intervals (95\% primary; 99\% for five secondary comparisons).
The dotted primary reference is -0.01. L/F denote model-generated/fitted laws supplied without
raw observations. These are new candidate plans in the ten reused worlds, not new physical
mechanisms or additional independent replication worlds.}
\label{fig:m3-portability}
\end{figure*}
```

# 8. Experimental knowledge and decision quality

Prediction quality, artifact fidelity and final decision quality are distinct observable quantities.
Two configurations show different compression losses while both largely retain the incumbent.
The independent unseen-plan assay makes the gap concrete: participants can select plans their
submitted laws would not recommend. These associations do not identify the causal role of an
internal world model.

Operational outcomes are a separate axis. The four-condition development study includes delivery
and donor failures, so its all-scheduled estimates describe implemented information strategies.
They cannot isolate knowledge content or experiment choice from availability. Identifiable-law
controls and ranking diagnostics delimit what the measurements establish.

The fixed-evidence factorial block implements that representation/decision-rule intervention.
It finds no supported material fitted-law benefit and 40/40 fitted-law agent/maximizer agreement.
This limits a general law-use failure account, without isolating which difference from the
historical protocols matters. The information-separated follow-up establishes independent
same-world artifact value relative to task-only input, while raw evidence also helps and nearest
retrieval reaches the measured optimum in every world. Transfer to changed mechanisms remains open.

# 9. Discussion

## 9.1 The decision value of experimental knowledge

Prediction error and decision loss need not agree, as established in predict-then-optimize and
decision-focused learning [@elmachtoub2022spo; @wilder2019decisionfocused]. Our setting adds
autonomous evidence collection, supplied descriptions of hidden chemical relations, executable
knowledge summaries and complete operational plans. The empirical contribution is the observation
and localization of gaps among these objects within the evaluated systems. The direct factorial
intervention adds a boundary: fitted-law replacement did not meet its material-benefit criterion,
and fresh agents agreed with its maximizer in every fitted-law pair. The information-separated
follow-up establishes independent artifact utility for new same-world plans, with a larger benefit
in electrochemistry. Raw evidence also helps, and nearest retrieval solves all ten candidate sets;
a generally useful repair method remains unresolved.

Last-available laws reach Top-1 in 0/45 scheduled cases, participants in 11/45, and agreement is
12/42 evaluable rankings. A submitted artifact is an incomplete proxy for the participant's decision.
The original longitudinal cohort lacks a no-evidence action control; its 11/42 scored Top-1 choices
alone do not estimate the benefit of experimentation or establish performance relative to chance.
The independent four-condition successor addresses information strategies, with its own population
and substantial operational limitations.

## 9.2 Measurement and interface limits

Matched parametric packets support conditional response after counterevidence and an added
response turn. They do not isolate a pure packet effect. The one-pair structural packet admits an
exact linear/power alias, so low prediction error and absent exact expression cannot establish
failure to identify an identifiable law. The independent multi-pair control makes a bounded
functional-form target identifiable, but sparse recovery and 13 DeepSeek schema failures limit
the conclusion. It does not test recovery of arbitrary causal graphs.

The same-domain capacity control distinguishes a legal representation's capacity from the fidelity
of the submitted artifact. It does not test generalization outside the fitted coordinates.
Global rank correlation and decision utility address different losses. Historical oracle results
are evaluator diagnostics, not an additional internal Agent failure mode or a missing condition
that can be filled retrospectively.

The interface affects the trajectory being measured. DeepSeek's checkpoints were eventually
accepted after 888 rejected typed submissions. Reduced submission burden, shared world construction
and identical scientific content across evaluators should precede a new comparison.
The participant is the complete agent--tool configuration, including prompts, context, recovery
and resource rules.

## 9.3 Scope and unresolved questions

The study covers bounded simulated chemistry, two fixed model--tool configurations and five
independent worlds per task. C2 retains different completion patterns, and model contrasts are
descriptive rather than provider effects. A-P/B2 have only five worlds; B2 uses retrospective
expression coding on an underidentifying surface. DeepSeek low is not a thinking-off experiment
or a reasoning-superiority test; its parametric block has no qualified formal denominator.

The four-condition study retains donor and recipient failures in its primary population.
Completed-donor analyses are post-treatment availability sensitivities. Fixed execution order and
earlier DeepSeek donors confound configuration with time and order. Ten prospective cells retain
discard-affected checkpoint timing that cannot be repaired retrospectively. Exact replay preserves
recorded execution; it does not erase these design limits.

Transfer to changed physical conditions, private confirmation and independent-backend replication
remain untested. The completed representation/decision-rule block uses quadratic representations
on two-dimensional control domains; the simulator utility need not be quadratic. Numerical fitting
is contrasted against tool-free model fitting.
Arithmetic and representation construction are bundled. Only five worlds per task support its
approximate intervals, and differences from historical protocols do not isolate a single cause.
Nearest-evidence retrieval is already competitive; no general repair algorithm is established.

## 9.4 Conclusion

Experimental knowledge must be evaluated through the decisions it actually supports. In these
systems, predictive improvement does not establish selective repair, executable summaries lose
different amounts of information, and submitted laws do not reproduce many participant choices.
Information-strategy estimates further depend on the reliability of evidence delivery.
The direct factorial test supplies an additional boundary: no supported material fitted-law
advantage and complete fitted-law agent/maximizer agreement. Information separation then shows
that compact laws can independently support new decisions in the same worlds, with task-dependent
benefit and no demonstrated superiority to raw evidence or retrieval. Decision utility, operational
availability, deployment cost and transfer to changed mechanisms remain separate questions.

# 10. Methods

## 10.1 World and initial-model construction

Each task instantiates an executable $W=(\mathcal{E},G,\Theta,O,C)$ and a participant-facing
$M_0=(\widehat{\mathcal{E}},\widehat{G},\widehat{\Theta},\widehat{O},\widehat{S})$. Prospective
worlds are selected deterministically from a set disjoint from exploratory worlds. Within each
world cluster, all arms share $W$, the resource card and stochastic identity; exactly one declared
component of $M_0$ changes. In the entity locus, aligned and misindexed dossiers contain identical fields, values,
wording and confidence language, while the latter applies a prespecified permutation to material
identifiers. Structural, parametric and observation-model extensions alter only their declared
agent-facing representation while retaining the external world and contract. Confirmatory structural
claims require a separate participant-visible identifiability analysis. The B2 post-packet block failed
that requirement and is retained only as an underidentification/expression diagnostic; B3 supplies the
typed reference-fitter-identifiable structural test.

## 10.2 Transactional execution and resources

Every operation enters schema validation and resource preflight before candidate execution.
Committed operations update physical state and the campaign ledger; invalid or resource-rejected
attempts retain their declared reporting debit without entering committed physical state. Task-specific
resource cards bound vessel starts, assays, measurements, stocks, process time, repeated operations,
quench and transfer time, and final-assay reserve across all experiments in a campaign.

## 10.3 Persistent agent and tool execution

Each participant cell launches one persistent agent process and retains one session across the complete
pattern-owned campaign. The participant instructions prohibit shell use, file changes and repository
inspection and require physical decisions to pass through the host-owned laboratory interface. The bounded domain tools
expose material information, belief checkpoints, operation submission, public state and history,
artifact inspection and final
recommendation commitment. The host validates and executes submitted actions but never chooses a
fallback scientific action.

Every operation submission contains a brief structured rationale stating its expected effect,
diagnostic target and evidence dependence. Tool records retain call order, status, timestamps and
error classes without retaining raw interaction payloads or private chain-of-thought. An infrastructure
retry or resume is an operational attempt within the same cell, not a new experiment or independent
sample. Belief checkpoints are tool calls inside the existing session rather than separate conversations.

## 10.4 Belief and law-summary checkpoints

Checkpoint records contain prior assessment, predictions, uncertainty, evidence references, an
executable law summary, next-experiment intent and overall confidence. The schema permits bounded
rationales but not an unconstrained persistent notebook. After the campaign, explicit predictions
and the final law summary are evaluated against sealed truth packs. The summary must execute for the
exact prespecified query-metric set; the analysis records its normalized error, pre-to-summary
improvement, error relative to the effective final checkpoint and prediction-consistency error.
These quantities are reported continuously. They are not converted post hoc into a public binary
law-discovery label, and a reusable or transferable-law claim additionally requires independent
transfer evidence.

The schema-capacity control refits every complete final prediction vector with legal identity-link
laws over the registered feature coordinates and allowed bases. The full fit permits up to 64 terms
per metric; the term-matched fit uses the participant's submitted per-metric term budget; and the
leave-one-query-out fit withholds each registered query in turn. Every fitted payload must pass the
production parser and executor, and executor predictions must agree with the independently computed
design-matrix predictions within $10^{-10}$. These are same-domain representation and distillation
controls, not tests of global mechanism recovery or transfer.

## 10.5 Statistical analysis

The prospective cohort contains 45 independent matched task--world clusters: 25 entity-level, ten
parametric and ten structural. Every cluster contains three participant arms, which are paired
interventions rather than independent samples. Prediction-to-law inference is performed separately by
locus. The entity locus uses a three-component failure-aware intersection--union criterion; the
parametric and structural loci use task-fixed-effect contrasts,
require both task means to be positive and retain adverse bounds for failed or unscorable arms. A
global cross-locus decision requires all three locus criteria to pass, and naive pooling across the nine
task--locus combinations is forbidden. Endpoint contrasts in Section 6 are descriptive trajectory
outcomes, not substitutes for that prespecified prediction-error analysis. Prespecified sensitivity
analyses include observed-point, complete-case, heteroscedasticity-robust and task-stratified
cluster-bootstrap summaries.

Matched-evidence analyses use the world as the inference unit and retain the prespecified contrast
$(E_{mis,pre}-E_{mis,post})-(E_{aligned,pre}-E_{aligned,post})$. The B2 phase-process study uses five worlds, so all
$2^5$ sign flips are enumerated for the exact one-sided directional check and a Student-$t$ interval
is reported descriptively. Protocol-validation sessions are excluded. Exact-law-expression counts are
retrospective keyword coding of the submitted public model summary and evidence assessment, never
private reasoning text. They were not preregistered structural-recovery endpoints. A
participant-visible audit additionally checks the number of nominal pairs, availability of the base
partition coefficient, presence of typed family/exponent fields, observational aliases, a constant
endpoint baseline and an aligned positive control. Because that audit rejects structural-family
identifiability, B2 expression counts remain diagnostics; the separate typed B3 assay supplies the
participant-identifiable structural test.

The DeepSeek-high and GPT-medium matched-evidence blocks use identical world, arm, query and packet
coordinates. The DeepSeek-low B2 ablation changes only the reasoning-effort setting within the Codex harness;
its public coordinates and evaluator are identical to DeepSeek high. Each configuration is analysed
separately with the same world-level estimand and exact sign-flip procedure. Cross-configuration
differences are descriptive; no model- or reasoning-superiority test, pooled provider effect or
extrapolation to the prospective cohort and open-action blocks is performed. The low parametric block
has no qualified denominator and is excluded.

The independent identifiable-law control fixes five public structural worlds, the same three prior
arms and two independent fresh sessions per arm and world. Its eight evidence rows and disjoint
eight-query scoring roster are selected provider-free on development worlds. All five public worlds
enter family, exponent, prediction, Top-1, rank and regret denominators; action gain enters only for
the three worlds whose best candidate exceeds the evidence incumbent by at least 0.02. Replicates are
nested within worlds. Joint structural recovery requires the registered power family and exponent
error at most 0.10; canary sessions remain outside the 30-cell scientific denominator.

## 10.6 Open-action plan construction and analysis

For the formal multi-task action assay, an outcome-blind generator constructed eight candidate
ActionPlans per world across three task families and five worlds per task before participant execution.
Candidate selection used only the declared plan
coverage criteria and could not read evaluator scores, participant trajectories, checkpoint outcomes or later
model responses. Every plan began from the same fresh-batch contract and disclosed its full operation
sequence and parameters. Independent validation executed all candidate and checkpoint truth queries
without additional model calls, verified exact replay and confirmed that the disclosed plan was the
plan evaluated.

After 12 participant experiments and the final checkpoint, the participant returned a complete
ranking and selected one candidate. Evaluator-owned outcomes were then used to calculate selected
rank, Top-1, raw regret, normalized regret, complete-ranking agreement and the joint mechanism--action
category. A law was classified as adequate when its normalized held-out mechanism MAE was at most
0.05 under the frozen evaluator threshold; otherwise it was classified as inadequate. This binary
label was fixed before action outcomes were interpreted. A cell was eligible only when all 12
experiments, five checkpoints, final ranking, resource reconciliation and execution-integrity checks
completed without contamination. All 45 scheduled cells remained in the denominator. Arm summaries
are descriptive because three crystallization cells were ineligible and only 12 task--world clusters
retain all three arms. The three additional interface validations used one world seed per task and
were evaluated only as interface checks, not as multi-world scientific evidence.

The continuous law--action control retained the same 42 eligible cells and never imputed the three
historical failures. Pearson and Spearman associations were calculated pooled and task-stratified.
Intervals resampled the 15 frozen task--world clusters, retaining every eligible arm in a sampled
cluster, for 10,000 bootstrap replicates with seed 20260827. Threshold sensitivity used the seven
fixed law-MAE cutoffs 0.05, 0.075, 0.10, 0.15, 0.20, 0.25 and 0.30; action outcomes did not select
cells, tasks, bases or cutoffs.

The five-condition causal follow-up paired each autonomous donor with no-evidence, yoked-evidence,
learned-law-only and oracle-law recipients within task--world--prior strata. Donor failure would have
retained the donor and marked its yoked and learned-law descendants as not started; donor replacement
was forbidden. The oracle law used the same typed schema and scientific scope as the learned law, but
was fitted provider-free on 96 registered queries disjoint from the eight candidates. Formal expansion
required every task--world oracle to reach candidate-order Spearman correlation at least 0.80. The
formal stage completed 896 truth executions and exact replays across eight clusters before a
crystallization oracle obtained 0.738095 and rejected the block. Because no participant session was
started, none of the prespecified autonomous-minus-no-evidence, yoked-minus-no-evidence,
autonomous-minus-yoked, learned-law-minus-no-evidence or oracle-minus-learned-law contrasts was
estimated.

The independent large-grid study increased oracle coverage to 64 global and 256
candidate-neighborhood queries while holding the fitted ExtraTrees family fixed. Construction used
seven exposed unit versions; prospective qualification used new worlds and the same frozen Spearman
threshold. The first new world failed at 0.714286 after 336 truth executions and exact replays, despite
Top-1 agreement and zero regret, so 14 planned worlds remained unstarted. A separate retrospective
alignment analysis re-read the 16 completed 96- and 320-query unit versions, reproduced their original
Spearman and Top-1 outcomes, and added no execution. Top-1, regret, selection within 0.01 of the optimum
and near-tie-aware pair ordering were treated as action endpoints; no result was used to revise an
earlier gate or stop rule.

## 10.7 Optional private confirmation boundary

No private participant cohort was executed for the present study. If private confirmation is pursued,
it will use newly sealed world instances disjoint from exploratory and public worlds, retain the same
three-arm participant and evaluator contracts, and preserve every completed, failed and unstarted
cell in a one-shot denominator. Such a cohort would test within-family replication. The information
separation assay assesses new decisions in the same physical worlds. Compositional transfer would
require a prespecified change in mechanism topology, not only a new conversation or parameter set.

## 10.8 Reproducibility and failure accounting

Participant trajectories, evaluator truth sets and blind-replay sets are stored separately and joined
through stable record identifiers. Every completed participant trajectory must pass physical replay,
campaign-resource replay and hidden-boundary verification. Process attempts, sessions, tool calls,
operation attempts, committed operations, complete experiments, cells and evaluator executions are
reported with distinct denominators.

Historical stopped-block records remain immutable and are not spliced into later denominators. The
GPT-5.6-sol C2 successor starts from its first scheduled cell and preserves all 135 outcomes; the
DeepSeek B3 successor likewise starts from its first scheduled cell and preserves all 30 outcomes.
The four-condition study constructs separate model-specific tables over all 45 scheduled strata,
marks donor-dependent conditions not started when the donor is ineligible and uses only jointly
donor-eligible coordinates for common-stratum descriptions. Participant, schema, provider, resource
and process failures are never replaced. Cross-model estimates are matched descriptive, clustered by
task--world, and are not treated as provider effects.

## 10.9 Independent-world representation-by-decision protocol

The factorial block fixes public evidence while replacing either its explicit representation or
the decision rule. Each of two task families has five new public-test worlds. Two fixed model
configurations each produce two independently sampled source artifacts per world, giving 40
source states nested within ten task--world clusters. Every source state has four conditions:
model law with fresh agent selection (L-A), the same law with a deterministic maximizer (L-X),
public-data fit with fresh agent selection (F-A), and the same fit with the maximizer (F-X).
The scheduled design comprises 40 source and 80 recipient sessions, 160 condition slots,
120 public evidence experiments and 80 hidden candidate evaluations, with exact replay of
each physical execution. This block uses fixed experiment acquisition.

Each world shares twelve evidence points and eight outcome-hidden candidate plans across models
and repeats. Independently seeded Latin hypercubes fix the two-dimensional coordinates before
outcomes are observed. Electrochemistry varies controlled potential over 0.65--1.65 V and current
over 20--120 mA. Its fixed probe uses 1.18 V, 70 mA and 630 s; controlled duration is 3540 s,
reagent amount 0.004 mol, electrolyte profile 2 and solvent 1. The complete LHS is rejected before
execution if any point violates minimum probe changes of 0.02 V or 1 mA. Crystallization varies
reaction temperature over 350--405 K and crystallization temperature over 275--295 K. Catalyst
0 at 0.000315 mol, solvent 1, reagent 0.015 mol, stirring 675 rpm, reaction duration 3600 s,
seed mass 0.008 g and crystallization duration 7200 s remain fixed. Both tasks share the same
normalized design and disclose the complete executable plans.

L and F use the same unclipped quadratic basis $(1,x,y,x^2,xy,y^2)$ in linearly normalized
coordinates. F is ridge regression on the twelve public utilities, with penalty $10^{-6}$ and an
unpenalized intercept. Source models see evidence before candidates are revealed and return six
finite coefficients. Fresh recipients receive evidence, candidates and one artifact, and return
only a candidate identifier. Calls are tool-free, capped at 600 s each, with no repair turn or
replacement. The request for 2,048 output tokens does not cap hidden reasoning; actual usage is
recorded. Source states have a fixed outcome-blind permutation, and each world/model uses one
L-first and one F-first decision repeat. The maximizer breaks exact ties by candidate order.
All choices are sealed before candidate utilities are loaded for analysis.

Candidate utility is a single keyed-noise measured score in $[0,1]$. M1 regret uses the fixed
utility scale one; earlier action assays retain their registered range normalization. Missing
or invalid choices receive regret one in the scheduled primary analysis; completed-only values
retain separate denominators. Near-optimality means regret at most 0.01. The primary contrast is
F-X minus L-X. Differences are first averaged over the four model/repeat states within world,
then equally across worlds within task and across tasks. A task-stratified world bootstrap uses
20,000 percentile replicates. Its two-sided 95% upper endpoint must be below -0.01 to support
the prespecified material benefit. The four secondary contrasts (L-X minus L-A, F-A minus L-A,
F-X minus F-A, and their factorial interaction) use 98.75% marginal intervals, a Bonferroni
adjustment for four comparisons. Five worlds per task give approximate small-sample intervals;
model repeats do not add independent worlds.

The nearest-public-observation baseline uses normalized Euclidean distance and row-order ties;
the random baseline is its exact uniform-candidate expected regret. Both reuse the same data and
count once per world. Missing source artifacts block the dependent L conditions while F continues.
Physical, semantic or replay failure stops dependent provider work; forbidden tools and missing
or reused session identity invalidate the remaining block. Interrupted started slots are retained
without retries. Physical CPU/wall includes replay; recipe-resource totals count primary execution
once. The protocol replaces explicit artifacts and decision computation, and does not identify
internal belief mediation or artifact-only transfer: recipients still receive the original evidence.

### Factorial outcomes and resources

All 40 source states, 120 sessions and 160 conditions completed; there were no failed, blocked,
replaced or unstarted slots. Scheduled and completed-only losses coincide. Mean regrets in
L-A/L-X/F-A/F-X order were 0.01436/0.01502/0.00425/0.00425 for DeepSeek and
0.00425/0.00425/0.00425/0.00425 for GPT. These configuration-specific summaries are descriptive.
F-X selected the exact best measured candidate in 20/40 states and a candidate within 0.01 in
28/40; the replicated fit copies still represent only ten worlds. Candidate MAE was
0.05028 for DeepSeek laws, 0.04832 for GPT laws and 0.04459 for the public fit, all finite.
Better average prediction error thus did not establish a material decision improvement.

The ten-world average nearest-evidence regret was 0.00354, versus 0.00425 for F-X and 0.11109
for exact expected uniform-random choice. These prespecified baselines reuse the same evidence
and candidate evaluations; the comparison supplies no novel-algorithm advantage. The F-A/F-X
bootstrap interval collapses to zero because all observed paired choices agree. It does not
establish exact equivalence for unobserved worlds or model samples.

Physical execution and replay consumed 1,780.8 s wall time and 1,768.3 s CPU. The 120 public
evidence executions account for 1,068.6 s wall time; 80 hidden evaluations account for 712.3 s.
Recipe resources count primary executions once: 2,300 operations, 54.8 measurement units,
1,497,000 simulated recipe seconds and 1.9 mol reagent. Provider calls used 8,859.5 s wall time,
1,623,791 input tokens (450,816 cached) and 942,258 output tokens (939,441 reasoning).
All 120 calls report input/output usage; reasoning is included in output and cache in input.
Source generation used 7,404.1 s versus 1,455.4 s for decisions. These costs describe this
block, without extrapolating provider billing or virtual resource use to laboratory expenditure.

## 10.10 Information separation and same-world context portability

The context-portability assay reuses all ten factorial worlds, their twelve public observations
per world and forty sealed source states. Private mechanisms, initial-state construction,
objective, control ranges and fixed controls remain unchanged. A separately fixed eight-point
Latin-hypercube design provides new candidate plans, disjoint from both the source observations
and the earlier candidates. This requires 80 hidden physical evaluations and 80 exact replays,
but no additional source measurements and no measurements by recipients. The independent-world
denominator remains ten; the forty sources and 160 recipient sessions are nested within them.
This is a new-decision assay in the same worlds, not transfer across changed private parameters
or mechanism topology.

Four information conditions receive identical task descriptions, coordinate/basis semantics,
utility direction and range, complete candidate controls and ActionPlans, and the same minimal
candidate-ID output schema. None receives no experiment-derived information. Raw receives the
twelve public observations, including their plans, without a law. L and F receive only the six
coefficients of the sealed model-generated or fitted quadratic, respectively, without raw
observations, source dialogue or provenance labels. Coefficients are reused exactly, without
refitting to the new candidates. No condition receives prior candidate outcomes or world identity.
Information quantity and context length are part of these deployment strategies; prompts are
not padded to equal length. Prompt bytes and actual provider tokens are recorded separately.

The same two model configurations and two repeats per world are used, with fresh tool-free
recipients. The forty source states are permuted before execution, and cyclic rotations of the
four conditions across the nested states place each condition in each serial position once per
world. Sessions have a 600-second timeout and no repair turns or retries. Missing artifacts block
only their dependent information condition. Participant schema failures remain in the scheduled
denominator; interrupted started calls are retained without replacement. Physical, replay,
information-isolation or session-identity defects stop dependent work and invalidate formal
inference. All recipient and deterministic choices are sealed before analysis loads new scores.

The primary contrast is L minus none in failure-aware regret. The utility scale is fixed at one;
missing or invalid choices receive regret one. Within-world differences average the four nested
model/repeat states, then weight worlds equally within task and tasks equally overall. A
20,000-replicate task-stratified world bootstrap supplies a two-sided 95% interval; its upper
endpoint must be below -0.01 to support a material benefit. Five secondary contrasts---raw minus
none, F minus none, L minus raw, F minus raw and F minus L---use 99% marginal intervals, adjusting
for five comparisons. Completed-only losses retain eligible denominators. Top-1, regret at most
0.01, individual-world effects and exact-maximizer agreement accompany the primary estimate.
Small-sample and previously exposed-world limits remain; nonsignificance is not equivalence.

Deterministic L/F maximizers, nearest public evidence and uniform-random expected regret are
prespecified descriptive controls on the same new candidates. They add no provider or physical
executions. New recipient and hidden-evaluation costs are separate from historical acquisition
and source-generation costs. None uses no acquired evidence; raw and F inherit the shared public
acquisition, while L also inherits its model's original source-generation cost. Source tool
permissions remain those of the factorial experiment: matching recipient permissions does not
remove the original model-versus-numerical-solver arithmetic difference. Zero recipient queries
do not estimate experimental savings, and no internal mediation or new repair algorithm is
identified by this information comparison.

### Information-separation outcomes and resources

All 160 recipients completed with no failures, retries or replacements; scheduled and completed-only losses coincide. The primary effect was negative in nine worlds and zero in one. Benefits were substantially larger in electrochemistry than crystallization.

```{=latex}
\begin{table*}[t]
\centering
\caption{\textbf{Information-separated decision quality.} Every model/condition has 20 scheduled and completed recipients, nested within ten reused worlds.}
\begin{tabular}{@{}llrrr@{}}
\toprule
Model & Information & Mean regret & Near-optimal & Top-1 \\
\midrule
deepseek & none & 0.15270 & 3/20 & 3/20 \\
deepseek & raw & 0.01643 & 17/20 & 15/20 \\
deepseek & L & 0.01157 & 11/20 & 9/20 \\
deepseek & F & 0.02309 & 12/20 & 10/20 \\
gpt & none & 0.14184 & 10/20 & 10/20 \\
gpt & raw & 0.00605 & 13/20 & 11/20 \\
gpt & L & 0.00850 & 12/20 & 11/20 \\
gpt & F & 0.00609 & 12/20 & 10/20 \\
\bottomrule
\end{tabular}
\end{table*}
```

```{=latex}
\begin{table*}[t]
\centering
\caption{\textbf{Prespecified information contrasts.} Negative regret differences favor the first condition. The primary material threshold is -0.01.}
\begin{tabular}{@{}lrl@{}}
\toprule
Contrast & Mean difference & Interval \\
\midrule
L minus none & -0.137231 & 95\% [-0.155845, -0.122566] \\
raw minus none & -0.136032 & 99\% [-0.166955, -0.106025] \\
F minus none & -0.132680 & 99\% [-0.164488, -0.099817] \\
L minus raw & -0.001199 & 99\% [-0.023529, 0.009508] \\
F minus raw & +0.003352 & 99\% [-0.021421, 0.037629] \\
F minus L & +0.004551 & 99\% [-0.008013, 0.031772] \\
\bottomrule
\end{tabular}
\end{table*}
```

Model-law recipients matched the exact maximizer in 40/40 states and fitted-law recipients in
39/40. Deterministic model-law and fitted-law regret was 0.01004 and 0.00609. The single fitted-law
recipient disagreement increases its group mean to 0.01459; it is retained as a valid choice.
Nearest public evidence selected the measured optimum in all ten worlds; uniform-random expected
regret was 0.12022. These comparisons do not establish a novel-algorithm advantage.

New physical execution/replay used 724.6 s wall time and 718.3 s CPU, with 920 operations,
21.92 measurement units, 598,800 simulated recipe seconds and 0.76 mol reagent counted once
for primary executions. Provider time was 2,722.6 s, with usage reported for 160/160 calls:
1,716,721 input tokens (648,704 cached) and 255,544 output tokens (253,304 reasoning).
Raw versus model-law deployment used 541,225/392,101 input tokens and 102,235/47,745 output
tokens. Prompt bytes were 838,900/351,996 (58.0% fewer), whereas provider input fell by 27.6%;
these measures include different overheads and must not be interchanged. Raw/model-law provider
time was 929.1/529.3 s. Costs describe this deployment block, not monetary expenditure or
experimental savings. Historical M1 public acquisition and original source generation are
reported separately and were not incurred again. No equivalence or new-mechanism transfer
claim follows from these data.

# 11. Data and code availability

The current source release contains the executable environment, prespecified protocols, analysis code,
source data and reproducible figure scripts used for this manuscript. The fixed agent-system
configuration, prompt contract, reasoning setting and sampling parameters are bound in the release
metadata. Raw interaction payloads and credentials are excluded, and no private cohort data are
included because that optional study was not executed.

# 12. Competing interests

The authors declare no competing interests.
