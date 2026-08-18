---
title: "Dissecting Executable Scientific Intelligence with Controlled World-Model Interventions"
title_line_one: "Dissecting Executable Scientific Intelligence"
title_line_two: "with Controlled World-Model Interventions"
subject: "Causal dissection of experimental search, predictive correction, executable laws and action transfer in AI agents"
keywords: "AI scientist; autonomous experimentation; initial world model; world-model intervention; scientific priors; law discovery; counterfactual prediction; action transfer; chemical worlds"
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
  Scientific agents enter experiments with an initial world model that can guide useful search but
  can also be wrong. Endpoint success alone cannot distinguish correct scientific inference from a
  favorable heuristic trajectory. We used executable chemical worlds to vary entity, parametric and
  structural information shown to one persistent experimental agent while holding the external
  world, operations and laboratory resources fixed within matched clusters. The prospective
  cohort completed 135/135 sessions and 1,243/1,260 planned experiments
  across nine task--intervention combinations. Prior effects were strongly context dependent.
  Correct entity information produced a durable advantage in liquid--liquid partition, whereas
  correct structural information gave crystallization a five-world initial head start that largely
  narrowed during subsequent exploration. In structural partition, both correct and incorrect
  explicit models outperformed opaque identifiers, indicating that structured search guidance and
  model correctness can contribute separately. Agents nevertheless performed substantive
  within-session search: 84.4% of session optima occurred after the campaign midpoint, and 91.2% of
  completed recipes were unique. All 135 sessions submitted five belief checkpoints, comprising
  6,300 prespecified counterfactual query predictions and typed law summaries. An independent
  evaluator requiring no additional model calls completed 420/420 truth executions, scored all 675 checkpoints, executed all 135 final
  laws and completed 726/726 launched blind replays. Prediction error generally decreased, but the
  prespecified selective-correction criterion failed at the entity ($p=0.990$), parametric
  ($p=0.079$) and structural ($p=1.000$) intervention loci. Executable laws were more accurate than final explicit predictions in
  only 50/135 cells and worse in 84/135. Blind recommendations were better, equivalent and worse
  than the observed incumbent in 1, 119 and 1 evaluable cells. A matched-evidence follow-up found
  a positive but mixed structural misindexed-minus-aligned prediction-update contrast (+0.0645, 3/5 worlds,
  exact sign-flip $p=0.125$), while 0/5 misindexed summaries recovered the prespecified 1.75 law.
  A separate multi-task, five-world longitudinal open-action study completed 45/45 scheduled
  cell records and 240/240 truth plus exact-replay queries before revealing eight fully specified
  but outcome-hidden action plans. Among 42 eligible cells, 11 selected the true top-ranked plan;
  30 had both an inadequate law and a wrong action, while the sole adequate-law cell selected the
  wrong action. Three crystallization failures were retained in the scheduled denominator.
  Thus evidence acquisition, numerical belief revision, structural-law identification, law
  compression and unseen-action selection form distinct capability layers; context-reset artifact
  portability remains untested.
  The present cohort provides a controlled first map of their conversion losses, rather than a
  single endpoint ranking or a claim of cross-model generality.
---

# 1. Introduction

Scientific discovery is not simply the production of a high-scoring outcome. A researcher can obtain
a useful result because an initial model was already correct, because evidence repaired an incorrect
model, because a local heuristic happened to work, or because the endpoint was reached without a
reusable account of the underlying relation. These explanations are scientifically distinct even when
their final scores are identical. The corresponding object of study is therefore not a single prompt
or material hint, but the agent's initial model of what exists in the world, how it works, which
quantities matter and how measurements should be interpreted.

This distinction is increasingly important for AI systems that choose and execute experiments.
Language-model agents can plan syntheses, call chemistry tools, operate instruments and participate in
self-driving laboratory workflows [@boiko2023autonomous; @bran2024augmenting;
@szymanski2023alab; @darvish2025organa; @song2025chemagents; @vriza2026instruments]. Interactive
scientific environments likewise test whether agents can formulate hypotheses, acquire evidence and
recover hidden rules [@jansen2024discoveryworld; @gandhi2025boxinggym; @duan2025scigym;
@zheng2026newtonbench; @yang2026causalab; @batzoglou2026replayscm]. Yet an agent's apparent scientific
success can remain difficult to interpret because pretrained knowledge, prompt-provided information,
experiment selection, endpoint optimization and verbal explanation are usually entangled.

The central problem is the initial world model. An agent entering an experimental campaign may carry
assumptions about entity identities and properties, causal structure, parameter signs and ranges,
the reliability and meaning of observations, or the conditions under which a learned law should
transfer. Any of these assumptions may be absent, useful or plausibly wrong. The important capability
is not merely whether such information changes behavior. A
scientifically adaptive agent should decide which evidence is worth acquiring, use observations to
revise the relevant part of its model, reduce confidence in contradicted structure or parameters,
summarize the recovered relation in an executable form and transfer that relation to conditions or
compositions it has not directly tested. Conversely, an agent may preserve an incorrect model through
selective measurement, reinterpret contradictory observations or patch only its action policy.

Physical self-driving laboratories are indispensable for real-material validation, but they make this
causal question difficult to study at scale. Strictly matching hidden laws, material identities,
measurement noise, budgets and safety conditions across alternative initial-model states is expensive
and often impossible. ChemWorld provides a complementary experimental instrument: chemical entities,
process structure, parameters, instrument mappings and private laws can be instantiated as executable
worlds, while the public experimental interface and complete operation history remain controlled.
This programmability permits the agent-facing initial model to change at a chosen layer while the
external world and evidence opportunity remain fixed [@qiu2026chemworld]. The ChemWorld foundation
study establishes the substrate, its construction and its replay properties; the present study does
not reuse that platform qualification as evidence about agent intelligence. Instead, it holds a
qualified executable world fixed, intervenes on the agent's initial model and measures the resulting
capability transitions.

Here we introduce a controlled framework for studying how initial world models shape experimental
search and whether evidence produces scientific correction. It makes four contributions.

1. **The initial world model becomes a layered intervention.** Entity/ontology,
   structural/mechanistic, parametric/dynamical, observation/measurement and scope/compositional
   assumptions can be separated while the executable world remains fixed. Each matched comparison
   changes one locus rather than conflating all programmable dimensions.
2. **Discovery is evaluated through evidence-conditioned transitions, not self-report alone.** Fixed
   checkpoints bind beliefs to evaluator-owned counterfactual queries and to the next experimental
   operation selected by the agent.
3. **Endpoint success is separated from reusable understanding.** Blind incumbent replay,
   executable law summaries and post-exploration ranking of unseen, fully specified ActionPlans
   distinguish local optimization, law recovery and action transfer; context-reset artifact
   portability remains a separate higher-order test.
4. **The complete experimental process remains reproducible.** One persistent session controls multiple
   experiments under a shared resource ledger, while failures, invalid actions, stopping events and exact
   replay remain explicit parts of the outcome.

The prospective public cohort shows that this distinction is empirical rather than merely conceptual.
Aligned information gives a durable advantage in one entity-level partition task and a marked initial
head start in structural crystallization, yet it does not dominate across the nine task--locus
combinations. Structural partition further separates explicit organization from correctness because
both aligned and misindexed models outperform opaque identifiers. Persistent agents continue to
search, measure and improve after their first experiment, but their stated reliability and misindex
warnings do not selectively identify the incorrect model. We therefore organize the paper around a
bounded result: initial world models reshape experimental search, whereas scientific correction
requires separately scored transitions from prediction to executable law and from law to unseen
action. The formal open-action assay makes the latter loss observable across three task families: after 12 experiments per
session, only 11/42 eligible readouts selected the top-ranked unseen plan, and the sole law-adequate
cell selected the wrong action.

```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/prior-discovery/figure-1-prior-to-law.pdf}
\caption{\textbf{From an initial world model to a reusable law.}
\textbf{a,} The current entity-level instantiation uses opaque, aligned and misindexed dossiers in the same fixed executable world; the same intervention logic can target structural, parametric or observation-model assumptions.
\textbf{b,} One persistent session repeatedly predicts, selects an operation, observes the public outcome and updates its belief and executable law summary across a shared-resource campaign.
\textbf{c,} Participant trajectories and evaluator-owned held-out truth remain separate until the campaign ends; prediction error, calibration and blind recommendation outcomes are scored afterward.
\textbf{d,} Predictive recovery and evidence-aligned unseen-action selection define four distinguishable phenotypes. Only their joint success, followed by context-reset artifact portability, supports a transferable-law claim; endpoint success or a correct statement alone does not.}
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
its initial world model alter search, prediction, correction, executable-law recovery and unseen-action
selection?

## 2.4 The unresolved identification problem

Large-scale behavioral evidence already suggests that successful scientific workflows need not be
accompanied by evidence-sensitive, self-correcting reasoning [@riosgarcia2026scientifically]. However,
an observational audit across systems cannot by itself identify which capability transition produced
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
dynamics, observation mapping and the authoritative public contract. The agent instead begins with
$M_0=(\widehat{\mathcal{E}},\widehat{G},\widehat{\Theta},\widehat{O},\widehat{S})$, where
$\widehat{S}$ represents assumptions about scope, modularity and compositional applicability. The
public task, action space, actual observation channels, resource card, safety rules and bound
stochastic identity are held constant. We intervene only on one declared component of $M_0$ before
the first experiment. Changing $W$ or the public contract would create a different task; changing one
component of $M_0$ creates a controlled epistemic intervention within the same task.

The programmable intervention space has four scientific layers and one non-intervention boundary.

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
Observation model & instrument mapping, reliability, bias and noise assumptions & secondary diagnostic probe \\
Scope / compositionality & applicability domains, invariant modules and transfer boundaries & context-reset artifact-portability study \\
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

## 3.3 Five separable outcomes and one capability chain

We distinguish five outcomes that are often collapsed into a single score, while recording the
intermediate transitions that connect them.

1. **Endpoint optimization:** whether the campaign identifies a high-quality experimental outcome.
2. **Predictive recovery:** whether held-out counterfactual prediction error decreases.
3. **Prior correction:** whether evidence selectively improves the wrong-prior condition without
   degrading the correct-prior condition.
4. **Reusable law recovery:** whether the final executable summary predicts unseen continuous
   conditions without losing the quality of the agent's conditional predictions.
5. **Action transfer:** whether knowledge acquired during exploration supports ranking and selecting
   previously unseen, fully specified executable plans rather than merely retrieving an observed
   incumbent.

The process-level chain is therefore

```{=latex}
\begin{center}
\small initial world model $\rightarrow$ experiment selection $\rightarrow$ evidence acquisition\\
$\rightarrow$ prediction / belief update $\rightarrow$ executable law $\rightarrow$ unseen action selection $\rightarrow$ artifact portability
\end{center}
```

The paper reports transition losses rather than a composite intelligence score: evidence-to-prediction
loss, prediction-to-law loss, law-to-action inconsistency and action-to-artifact-portability loss.
This makes it possible to identify
where a capability fails without treating a successful endpoint as proof that every upstream step was
correct.

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
2. **Matched-evidence falsification.** A cloned-world secondary probe presents the same
   contradictory evidence to each arm, separating failure to seek evidence from failure to update
   after seeing it. The analysis includes the unaffected parametric block and a corrected structural
   phase-process block. An earlier structural run was excluded because its evaluator truth source
   omitted the prespecified world intervention. All matched-evidence sessions are independent and
   excluded from the free-discovery denominator.
3. **Executable law and action.** Typed law summaries and held-out predictions test the
   transition from conditional belief to executable relation. Blind incumbent replay tests whether
   a committed recommendation can reproduce observed value, while a separate longitudinal
   open-action assay tests whether the agent can rank previously unseen, fully specified ActionPlans;
   no verbal statement alone counts as discovery.
4. **Artifact-only compositional transfer.** After source-world learning, raw evidence,
   prose summaries or executable laws are transferred to a context-reset agent in a new combination.
   No-artifact, trajectory and typed-law conditions are compared, and within-family replication is
   kept separate from genuine compositional transfer.

Observation/measurement interventions are reserved as a separate boundary probe. They require
two-task identifiability and an exploratory three-arm study and are not included in the present
denominator. Scope/compositional assumptions are tested only in the future portability study. This preserves a complete
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
\textbf{a,} The entity/ontology backbone uses five task families and five public worlds per task; exploratory and prospective world instances are disjoint, and any future sealed private instances must remain disjoint from both.
\textbf{b,} Every matched task--world cluster contains opaque, aligned and misspecified initial models for one declared locus. Campaign length and checkpoints are owned by the locus pattern rather than forced into one universal four-experiment limit.
\textbf{c,} Parametric/dynamical and structural/mechanistic blocks require separate validation; observation-model and scope/compositional studies retain separate inclusion decisions.
\textbf{d,} Free discovery, matched-evidence falsification, evaluator truth and action tests, within-family replication and context-reset artifact-portability tests retain separate sessions, resources and denominators. The diagram is a design map, not completed outcome evidence.}
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
descriptive: no post-hoc binary validity threshold is applied, and reusable-law status remains
unavailable without the prespecified private transfer test.

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

The five-world partition matrix contains three initial-model arms per world, 15 persistent sessions
and 180 participant experiments. The primary action endpoint is within-world regret of the selected
plan; selected rank, Top-1, complete ranking and mechanism adequacy are reported separately. This
matrix is an exploratory action-transfer study analyzed separately from the prospective locus tests. Scheduled cells
remain in the denominator, and no arm-level inference is made when a world lacks a complete triplet.

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

For the entity locus, the misspecified arm is instantiated by a prespecified material permutation and $C_{\ell}=C_E$ is the
confirmatory contrast. Success requires the lower confidence bound for the locus-specific contrast to
exceed zero, the wrong-prior condition to improve, and the aligned condition not to deteriorate beyond
a prespecified tolerance. Correct-prior utility, wrong-prior vulnerability and knowledge-to-action
translation form a hierarchical secondary family. A cross-locus conclusion requires concordant,
separately reported entity, parametric and structural results; standardized effects may be synthesized hierarchically,
but raw contrasts are not pooled as if their intervention semantics were identical. Observation-model
results remain a distinct boundary analysis unless evaluated in a separate prespecified study.
Endpoint, calibration, behavior, law-summary, transfer, resource and safety outcomes are reported as
separate channels rather than one leaderboard score.

Failed scientific cells remain in the denominator and are not replaced. A right-censored cell carries
its last valid checkpoint forward; a missing final prediction receives zero primary improvement. Only
a pure infrastructure failure without a persisted trajectory may resume under the prespecified attempt cap.

# 5. Exploratory evidence and protocol characterization

The following exploratory results characterize the method and sharpen the scientific question. They
are analyzed separately from the prospective cohort and from any future private-confirmation
denominator; the two exploratory configurations are not used for a cross-system capability ranking.
Sections 5.1--5.5 instantiate the entity/ontology layer, whereas Section 5.6 reports a preliminary
one-cluster parametric study. Neither substitutes for the prospective multi-locus cohort in Section 6.

```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/prior-discovery/figure-3-development-prior-effects.pdf}
\caption{\textbf{Exploratory evidence for prior-sensitive behavior.}
\textbf{a,b,} Paired world-seed differences in the best endpoint observed during four-experiment campaigns for aligned versus opaque and misindexed versus opaque information. Each row is one task--world pair; a short within-row segment links the two contrasts and diamonds are descriptive task means. The baseline exploratory configuration contains five pairs per task except the aligned distillation contrast ($n=4$); the continuation configuration contains five pairs except the misindexed crystallization contrast ($n=4$).
\textbf{c,} Final explicit misindex warnings, shown as flagged cells over available final belief records for each exploratory configuration, task and prior arm.
\textbf{d,} Completed-cell, complete-experiment and exact-replay denominators. Failures remain in the scheduled denominator and are not replaced. Panels a--c use the common three-task paired endpoint/warning dataset; the complete five-task exploratory denominator is shown in Table~\ref{tab:five-task-closeout}. All panels are exploratory descriptive summaries; no confidence interval, confirmatory hypothesis test or cross-system capability comparison is performed. Endpoint gains and verbal warnings do not establish law discovery, selective wrong-prior correction or transfer.}
\label{fig:development-prior-effects}
\end{figure*}
```

## 5.1 Entity-level priors reshape endpoint behavior

One exploratory matrix used a fixed persistent-agent interface. It produced 44 completed cells out of
45 and 176 complete experiments out of 180. Mean paired
aligned-minus-opaque differences in the best observed endpoint were +0.211 for electrochemical
conversion, +0.057 for crystallization and -0.036 for distillation, with the distillation contrast
based on four complete pairs. Misindexed information was not consistently harmful, and explicit
misindex warnings included substantial false positives in aligned cells.

A second exploratory cohort was completed across all five task families, retaining the original
seed-0 records for partition discovery and safety-constrained reaction and adding seeds 1--4 in a
separate continuation. The seeds 1--4 continuation block is therefore not a substitute
for the immutable seed-0 records. No seed-0 outcome was rerun or replaced. Every scheduled cell produced a final
record (**75/75**); **69/75** cells met the prespecified completion criteria,
with **290/300** complete experiments, **2,663/2,587** operation attempts/committed operations,
**73** validation failures, **3** resource rejections and **69** recovered tool-interface failures.
Exact physical/resource replay passed for **75/75** trajectories. This exploratory cohort remains
descriptive: it is separate from the prospective matrix, has no private transfer confirmation or
confirmatory hypothesis test. No formal hypothesis test is used for its endpoint contrasts, and the
exploratory configurations are never pooled into a capability ranking.

```{=latex}
\begin{table*}[!t]
\centering
\caption{\textbf{Completeness of the five-task exploratory cohort.} All five task families reached the
scheduled five-seed denominator. The partition and safety continuation retained their original
seed-0 outcomes; their operational rows are reported descriptively and are not pooled
with the common three-task paired endpoint panels.}
\label{tab:five-task-closeout}
\scriptsize
\begin{tabular}{lrrrrrr}
\toprule
Task & Completed & Eligible & Experiments & Attempts/committed & Tool failures & Exact replay \\
\midrule
Electrochemical conversion & 15/15 & 15/15 & 60/60 & 373/372 & 13 & 15/15 \\
Reaction to crystallization & 15/15 & 13/15 & 54/60 & 606/605 & 18 & 15/15 \\
Reaction to distillation & 15/15 & 15/15 & 60/60 & 637/637 & 7 & 15/15 \\
Partition discovery & 15/15 & 12/15 & 58/60 & 553/501 & 14 & 15/15 \\
Safety-constrained reaction & 15/15 & 14/15 & 58/60 & 494/472 & 17 & 15/15 \\
\bottomrule
\end{tabular}
\end{table*}
```

```{=latex}
\begin{table}[!t]
\centering
\caption{\textbf{Five-task exploratory endpoint contrasts.} Values are descriptive paired-seed means in best endpoint score; the partition and safety rows are continuation observations and are not pooled into the common three-task Figure 3 endpoint panels.}
\label{tab:five-task-development-contrasts}
\scriptsize
\begin{tabular}{lcc}
\toprule
Task & \shortstack{Aligned--\\opaque} & \shortstack{Misindexed--\\opaque} \\
\midrule
Electrochemical & $+0.0785$ ($n=5$) & $+0.0915$ ($n=5$) \\
Crystallization & $+0.0305$ ($n=5$) & $+0.0690$ ($n=4$) \\
Distillation & $+0.0374$ ($n=5$) & $+0.1080$ ($n=5$) \\
Partition & $-0.1397$ ($n=5$) & $-0.1063$ ($n=5$) \\
Safety-constrained reaction & $+0.0223$ ($n=5$) & $-0.0196$ ($n=5$) \\
\bottomrule
\end{tabular}
\end{table}
```

The ordering is not aligned, opaque, then misindexed. In distillation, every paired seed favored both
explicit-information arms over opaque identifiers, and the misindexed mean gain was larger. In
partition discovery, both explicit-information contrasts were negative, whereas the safety task was
mixed. These task-pattern differences are descriptive and are partly coupled to the continuation
contract; they do not support a pooled configuration effect. A better endpoint therefore cannot be treated
as evidence that the agent accepted a correct prior, rejected a wrong prior or recovered the hidden
law.

```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/prior-discovery/figure-4-development-confirmation.pdf}
\caption{\textbf{Held-out evaluation of the five-task exploratory matrix.}
\textbf{a,} Aligned-prior and misindexed-prior reductions in normalized held-out prediction error for all 25 task-by-world clusters. The identity line marks equal improvement; filled points are complete three-arm clusters and open points retain at least one failed arm under the prespecified missing-outcome rule.
\textbf{b,} The primary exploratory contrast $C_{\mathrm{prior}}$ by task and seed. Diamonds are task means; positive values favor greater correction in the misindexed arm.
\textbf{c,} Executable law-summary error minus final explicit-prediction error for 71 evaluable summaries. Negative values indicate beneficial compression.
\textbf{d,} Paired blind replay of the committed recommendation versus the observed incumbent for 69 eligible cells. The evaluator completed 414/414 replays without additional participant calls. All panels are exploratory descriptive evidence; no confirmatory test, private transfer claim or cross-system ranking is performed.}
\label{fig:development-confirmation}
\end{figure*}
```

## 5.2 Held-out prediction improves, but entity-level correction is not selective

The exploratory held-out evaluator executed four prespecified counterfactual queries for each of the
25 task-by-world clusters. All **100/100** truth queries completed with exact replay and without
additional model calls. Final checkpoint predictions were scoreable for **72/75** retained cells.
Using the prespecified failure rules, aligned-prior prediction error improved in 24/25 cells and
misindexed-prior error improved in 22/25 cells. Improvement was therefore common, but it was not
selectively stronger under the wrong prior: the primary contrast had a descriptive mean of
**$-0.042$**, median **$-0.039$**, and was positive in only **7/25** clusters. Restricting description
to the 19 complete-case clusters gave the same direction (mean **$-0.039$**; 6/19 positive). Only the
safety-constrained task had a positive task-level mean; the other four task means were negative.

The evaluator executed **71/75** final typed law summaries on the same prespecified coordinates. The
summary improved on the final explicit predictions in 12/23 opaque, 7/24 aligned and only 3/24
misindexed cells; it was worse in the remaining 11, 17 and 21 cells, respectively. Thus, an agent can
improve its checkpoint predictions without compressing that improvement into a reusable executable
law. Blind replay sharpened the action boundary: **414/414** scheduled executions completed across
69 eligible cells, but the committed recommendation beat the observed incumbent in 0 cells, was
equivalent in 66 and was worse in 3. These results do not prove that correction is impossible; they
show that endpoint gains, prediction repair, law compression and recommendation quality are distinct
outcomes.

## 5.3 Verbal suspicion is not selective correction

Across available final belief records, final misindex warnings were 0/5, 5/5 and 3/5
for opaque, aligned and misindexed electrochemical cells; 0/4, 5/5 and 4/4 in crystallization;
0/5, 5/5 and 5/5 in distillation; 0/4, 2/4 and 3/4 in partition discovery; and 0/5, 2/4 and
0/5 in safety-constrained reaction. The model therefore often associated dossier presence with
possible misindexing, but the pattern was task-dependent and did not selectively distinguish the
correct and incorrect dossiers. Mean aligned-minus-misindexed changes in self-reported prior
reliability were small or heterogeneous across tasks, including negative changes in several
continuation cells.

This is a scientifically useful negative boundary. A warning flag or reduced stated confidence is
not a valid bias-rejection endpoint unless it predicts evaluator-scored correction and subsequent
evidence-aligned action.

## 5.4 Persistent-session accounting exposes a separate operational layer

Long-lived campaigns introduce an operational layer that is distinct from scientific evidence. Shared
history, checkpoint schemas, resource preflight and recovery rules affect how a persistent agent can
execute a campaign, but they do not create additional independent worlds or experiments. Accordingly,
implementation usage, transport events and interface diagnostics are tracked separately from physical
outcomes and are not interpreted as capability contrasts. The complete exploratory records retain
these diagnostics for auditability while the reader-facing results focus on the scientific denominators.

## 5.5 Exploratory conclusion

Across the retained exploratory configurations, explicit priors clearly alter the course and endpoint
of experimentation, and most cells improve their held-out predictions. The same evidence does not
show selective wrong-prior rejection: aligned improvement exceeds misindexed improvement on average,
typed law compression is frequently lossy and committed recommendations do not outperform the
observed incumbent. These findings motivated the prospective multi-locus cohort, while establishing
that prediction repair, law recovery and action quality must remain separate outcomes.

## 5.6 Preliminary parametric study: rejection is not recovery

We next asked whether this separation extends beyond entity-level dossiers to a parameter-level
initial world model. An evaluator-only screen selected one electrochemical seed in which an aligned
potential/current window and a matched but misspecified window were strongly separable in the
executable world. This screen fixed the intervention before any participant outcome was observed.
The subsequent preliminary study retained one opaque, one aligned and one misspecified cell. Each
cell used one persistent agent session, four complete experiments and four
belief checkpoints under a shared within-cell resource ledger.

All **3/3** cells, **12/12** participant experiments and **12/12** checkpoints completed. A separate
evaluator requiring no additional model calls completed **4/4** shared held-out truth queries and
**18/18** paired blind replays, all with exact replay. Normalized prediction error changed from
**0.347 to 0.320** in the
opaque arm, **0.359 to 0.155** in the aligned arm and **0.420 to 0.198** in the misspecified arm. The
one-cluster correction contrast was therefore positive but remains descriptive.

The trajectory reveals a distinction hidden by aggregate error. The misspecified agent first tested
inside its supplied window and obtained a score of zero. It then reduced the model's stated
reliability from **0.70** to **0.12**, explicitly identified `potential_V` as the challenged field and
moved its second experiment **2.41 V** outside the supplied window; final reliability reached
**0.03**. This is behavioral model rejection rather than a free-standing verbal warning. Yet the arm's
best observed score was only **0.274**, compared with **0.568** for aligned and **0.670** for opaque.
The agent had learned that the supplied model was wrong without recovering the best finite-budget
experimental policy.

Final executable-law errors were **0.424**, **0.238** and **0.242** for opaque, aligned and
misspecified, respectively. All three committed recommendations selected their own observed
incumbent, so paired blind replay confirmed reproducibility but produced zero recommendation gain.
This one-world preliminary result motivated a broader two-task, five-world parametric block. It remains
excluded from the prospective cohort denominator and cannot itself support a cross-task or general
initial-world-model claim.

# 6. Prospective multi-locus results

## 6.1 Cohort completeness and operational outcomes

The prospective analysis combines 120 unaffected sessions with a complete 15-session replacement of
the structural crystallization block after correcting its resource contract. All **135/135**
scheduled sessions produced final records. The participant completed **1,243/1,260** planned
experiments, and **121/135** sessions met the prespecified operational eligibility criteria. The
denominator contains **1,269** closed batch lifecycles: 1,243 ended in a final assay and
26 were discarded. No dynamic physical failure occurred. Thirteen operations were rejected by the
finite laboratory resource ledger, and 84 participant operation attempts did not become committed
operations. These cells and attempts remain in their assigned denominators.

## 6.2 Prior effects separate into durable advantage, head start and search scaffolding

The strongest durable aligned-prior result occurred in entity-level partition. Relative to the misindexed arm,
the aligned arm improved the first experiment by **0.106** score units and the best observed endpoint
by **0.200**; both contrasts had the same direction in **5/5** worlds. Here, correct entity information
changed both entry into the search space and the best region reached within eight experiments.

Structural crystallization showed a different pattern. The aligned structural model improved the first
experiment over the misindexed model by **0.141**, again in **5/5** worlds. The best-endpoint difference
then narrowed to **0.055** and was positive in **3/5** worlds. Aligned within-session improvement was
lower than misindexed improvement by **0.086** in every world. The structural model therefore provided
a reproducible head start, while subsequent free exploration allowed the initially disadvantaged arm
to recover part of the gap.

Structural partition separated structured guidance from model correctness. The aligned and misindexed arms
exceeded opaque identifiers in best endpoint by **0.163** and **0.143**, respectively, whereas their
mutual difference was only **0.020** and positive in 3/5 worlds. Supplying an explicit structural
decomposition helped organize the search, but the endpoint alone provided little stable separation
between the correct and incorrect versions of that decomposition.

The remaining task--locus combinations bounded these positive cases. Entity-level reaction safety had a small
aligned-minus-misindexed best-endpoint difference of 0.036 with concordant direction in 5/5 worlds.
The entity-level distillation difference declined from 0.053 on the first experiment to 0.011 at the best
endpoint. Entity-level electrochemistry was heterogeneous, entity-level crystallization favored the misindexed arm on
average, and neither parametric task showed a stable aligned endpoint advantage. Correct initial models were
therefore not a universal performance intervention.

## 6.3 Persistent agents continued to search and measured task-relevant states

All nine task--locus groups had a positive mean best-minus-first score. Across cells, **91.2%** of
completed experiments used a unique recipe, **84.4%** of session optima occurred after the campaign
midpoint and **32.6%** occurred in the final completed experiment. The observed prior effects cannot
be reduced to copying one supplied recipe; the persistent agent continued to use experimental
feedback throughout the campaign.

Every completed batch closed with a final assay, while non-final instrument use followed the process
path. Entity-level and structural crystallization measured intermediate states in 95.0% and 98.4% of closed
lifecycles, structural partition in 82.2% and distillation in 50.0%. Entity-level electrochemistry used no non-final
instrument because its prescribed lifecycle proceeded from electrolysis directly to the final assay.
Overall, **666/1,269** closed lifecycles contained a non-final measurement, comprising 872 instrument
uses. Instrument use should therefore be interpreted against task semantics, not as one global
autonomy score.

## 6.4 Complete belief submission did not establish selective correction

Every session submitted its pre-evidence, three intermediate and final checkpoint: **675/675** typed
belief snapshots in total. These snapshots contained **6,300** prespecified counterfactual query
predictions and **24,300** query--metric values, and all 675 included a schema-valid typed law summary.
Submission completeness, however, did not imply epistemic selectivity. Mean stated reliability rose
from 0.600 to 0.747 in aligned cells and from 0.592 to 0.703 in misindexed cells. At the final
checkpoint, **48.9%** of aligned cells and **42.2%** of misindexed cells flagged a suspected misindex.
The participant distrusted the correct explicit model at least as often as the incorrect one.

Stable batch-identity reconstruction found a valid final recommendation in 135/135 cells. Of these,
133 selected the exact observed incumbent, and 134 had zero observed-score regret; the maximum regret
was 0.0077. The commitment interface reliably closed the campaign, but it mostly measured retrieval
of the best observed batch rather than extrapolative action beyond the campaign history.

The checkpoint interface itself was a material part of the evaluated system. The cohort recorded 904
failed tool-interface events, of which 888 were rejected typed-checkpoint submissions; 900 failures
were classified as agent-invalid, compared with one transport/OS event and three unclassified events.
All five checkpoints were eventually recovered in every cell, so this burden did not create missing
prediction payloads, but it increased context and recovery work, especially for the 16-query
parametric and structural schemas. The result belongs to the complete evaluated agent-system configuration
and its tool interface rather than the language model in isolation.

## 6.5 Prediction learning did not become selective wrong-model repair

The held-out evaluator executed **420/420** truth queries, producing 1,620 query--metric truth values
without additional model calls, and scored **675/675** checkpoints. All three intervention loci
showed mean pre-to-final error reductions in every arm. For the entity locus, the opaque, aligned and
misindexed reductions were 0.111, 0.097 and 0.097; for the parametric locus they were 0.090, 0.033 and
0.065; for the structural locus they were 0.219, 0.228 and 0.221. The agent therefore learned
predictive information during the campaigns. Structural results were recomputed after correcting an
evaluator omission of the prespecified world intervention; superseded outputs were excluded.

The prespecified estimand was more demanding: the misindexed arm should improve more than the aligned
arm without degrading aligned predictions. This selective-correction criterion failed at every locus.
The failure-aware primary contrasts were **-0.214** for the entity locus ($p=0.990$), **+0.033** for
the parametric locus ($p=0.079$) and **-0.224** for the structural locus ($p=1.000$). The entity locus
passed the aligned noninferiority component but not the misindexed-improvement component. Both
parametric task means were positive, making the result suggestive rather than confirmatory. In the
structural locus, crystallization showed positive observed-point
correction whereas partition was negative; the required cross-task locus decision therefore failed.
Observed-point sensitivity did not reverse any locus decision. General predictive learning and
targeted repair of a wrong initial model were thus empirically distinct.

## 6.6 Executable laws were often lossy and blind actions rarely improved

All **135/135** final typed laws executed on their prespecified continuous query coordinates. Mean law
MAE was 0.237. Relative to the effective final explicit predictions, laws were better in 50 cells,
equal in one and worse in 84; mean law-minus-final error was +0.069. The structural locus showed the strongest
pre-to-law improvement (+0.206), but even there the law remained less accurate than the final
explicit predictions on average (+0.017). Syntax and executability were therefore solved, whereas
faithful compression of a conditional belief state into a reusable relation was not.

Paired blind replay retained all final participant states. It launched and completed **726/726**
executions for 121 evaluable cells; 84 pre-scheduled executions for seven failed and seven
right-censored cells were retained as unstarted rather than imputed. Recommendations were better,
equivalent and worse than the observed incumbent in **1/119/1** cells, with recovered mean gain about
$-0.0010$. The
final interface was highly reproducible but almost entirely retrieved an incumbent rather than
producing a new action advantage.

## 6.7 Matched evidence separated three transitions rather than yielding a binary label

An earlier structural matched-evidence run is excluded from scientific inference because its truth
source was generated before the evaluator received the prespecified structural intervention. The
unaffected parametric block remains in the analysis, and a corrected structural block supplied 80/80
independently evaluated power-law truth queries and direct phase-process evidence with disjoint
phase-process scoring queries. The corrected study completed 15/15 two-turn sessions and all registered
turns, 360/360 scoring terms per stage and zero failures.

For the parametric study, all five misindexed public summaries explicitly rejected the supplied high-potential
direction and recovered the peak-and-collapse response. This supports an evidence-acquisition
component in the free-discovery loss. In the structural study, opaque, aligned and misindexed mean errors fell from
0.2255, 0.2736 and 0.3392 to 0.0074, 0.0060 and 0.0071. The prespecified misindexed-minus-aligned
update-gain contrast was **+0.0645**, positive in **3/5** worlds (exact one-sided sign-flip
$p=0.125$, descriptive 95% interval $[-0.0557, 0.1848]$). This is a mixed prediction-level signal,
not a confirmatory selective-correction result.

The structural recovery analysis was more restrictive: **0/5** misindexed summaries recovered the exact prespecified
1.75 power law, only **1/5** explicitly rejected the supplied linear partition form, and all five
shifted toward an empirical saturation or endpoint model. The agent therefore revised numerical
predictions after receiving law-level evidence but did not reliably identify the prespecified mechanism.
The resulting boundary is three-layered: evidence acquisition, numerical belief revision and structural
law identification are separable; neither a pure evidence-acquisition bottleneck nor a pure stubborn-updating
claim is supported.

```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/prior-discovery/figure-5-public-c2-capability-chain.pdf}
\caption{\textbf{Prediction learning, scientific correction, executable-law compression and blind action dissociate.}
\textbf{a,} Failure-aware selective-correction contrasts across all 45 matched task--world clusters; circles show observed contrasts, vertical ticks retain adverse failure-aware bounds and diamonds show task means. Prespecified locus $p$ values are shown.
\textbf{b,} Mean pre-to-final normalized prediction-error reduction by intervention locus and initial-model arm.
\textbf{c,} Final executable-law MAE minus final explicit-prediction MAE for all 135 cells. Positive values indicate lossy compression.
\textbf{d,} Blind recommendation outcomes for all 121 evaluable cells; 14 incomplete participant cells remain in the denominator as unstarted.}
\label{fig:public-capability-chain}
\end{figure*}
```

# 7. Longitudinal action-transfer study

## 7.1 Complete action semantics remove a hidden-workflow explanation

The prospective-cohort blind replay established whether a final recommendation could reproduce the value of
an observed incumbent, but it rarely required extrapolation beyond the participant history. We
therefore developed a second action assay in which the agent explores freely for 12 experiments and
only then ranks eight unseen plans. An earlier fixed-evidence prototype retained 11/15 complete cells;
four participant outputs failed its final-output schema, and none of the 11 complete cells selected
the top-ranked candidate or recovered the exact prespecified mechanism. This incomplete prototype is
reported separately and is not combined with the subsequent study.

The successor assay closes the more important semantic ambiguity. Candidate workflows may differ,
but every candidate is a complete ActionPlan rather than a feature vector. Public, evaluator-truth
and executed plans are verified as identical, and no evaluator-owned default may add, remove, reorder or silently
parameterize an operation. Candidate outcomes and ranks remain hidden. A wrong ranking can therefore
no longer be attributed to an undisclosed execution workflow.

## 7.2 The multi-task formal matrix exposes a task-dependent action-transfer boundary

The formal multi-task matrix completed **45/45** scheduled cell records across three task families, five
world seeds and three initial-model arms. Independent evaluation completed **240/240** truth
executions and **240/240** exact replays without additional model calls, and verified that public,
evaluator-truth and executed ActionPlans were identical. **42/45** cells were uncontaminated and
eligible for action metrics. The three excluded cells were all crystallization cells and remain in
the denominator: two ended after agent-selected resource/process exhaustion and one was right-censored
by an interrupted campaign. An independent aligned-arm repair is reported as a
technical sensitivity result and does not replace the original cell.

```{=latex}
\begin{table*}[!t]
\centering
\caption{\textbf{Formal multi-task open-action matrix.} Rank and regret summaries use the 42 eligible cells; all 45 scheduled cells remain in the denominator and the three crystallization failures are retained. Lower rank and regret are better.}
\label{tab:open-action-matrix}
\scriptsize
\begin{tabular}{lrrrrr}
\toprule
Arm & Scheduled & Eligible & Mean rank & Top-1 & Mean normalized regret \\
\midrule
Opaque & 15 & 14 & 3.14 & 5 & 0.2742 \\
Aligned & 15 & 14 & 3.36 & 3 & 0.2958 \\
Misindexed & 15 & 14 & 3.43 & 3 & 0.3222 \\
\bottomrule
\end{tabular}
\end{table*}
```

Across eligible cells, **11/42** final readouts selected the true Top-1 plan; the mean selected rank
was 3.31/8 and the mean normalized regret was 0.297. The joint mechanism--action outcome was more
informative than Top-1 alone: **30/42** cells had an inadequate law and wrong action, **11/42** had
an inadequate law but a correct action, **1/42** had an adequate law but a wrong action, and **0/42**
combined an adequate law with a correct action. Thus law adequacy was not sufficient for action
correctness, while action correctness could occasionally occur without an adequate law.

Task heterogeneity is large: electrochemical conversion reached Top-1 in 4/15 cells with mean rank
3.60, reaction safety in 4/15 with mean rank 2.00, and crystallization in 3/12 with mean rank 4.58.
The 12 complete three-arm task--world clusters and the non-random concentration of failures in
crystallization make the arm means descriptive rather than causal. The bounded conclusion is a
transition boundary: even when all candidate workflows were complete and execution semantics were
public, autonomous exploration and occasional law adequacy did not reliably produce correct ranking
of unseen plans.

A leave-one-cluster-out sensitivity analysis reinforces this boundary. Across the 12 complete
three-arm clusters, every pairwise mean-rank contrast changed sign somewhere across the 12 omissions
(aligned minus opaque, -0.45 to +0.73; misindexed minus opaque, -0.18 to +0.91; aligned minus
misindexed, -0.91 to +0.36). The corresponding regret contrasts were also unstable except that
misindexed minus opaque remained weakly positive (+0.003 to +0.178). These diagnostics do not rescue
an arm effect; they show why the world seed is the paired analysis unit and why the cell-level arm
means must remain descriptive.

```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/prior-discovery/figure-6-open-action-formal.pdf}
\caption{\textbf{Formal multi-task open-action matrix.} \textbf{a,} Selected true rank for every eligible cell, with rows grouping task--world clusters, arm colors identifying the three nominal alternatives, and the dashed line marking the random expected rank of 4.5. No ordered trajectory is implied between arms. \textbf{b,} Normalized regret for the same rows. \textbf{c,} Joint law--action categories among 42 eligible cells; the three crystallization failures remain outside action metrics but inside the scheduled denominator. \textbf{d,} Task-level means show heterogeneity across chemical workflows, not a pooled arm effect. All candidate ActionPlans were complete and public to the participant; candidate outcomes and true ranks remained hidden until the terminal readout. Truth and exact replay were both 240/240.}
\label{fig:open-action-formal}
\end{figure*}
```

## 7.3 The repair result is sensitivity evidence, not a replacement cell

The independent aligned-arm repair completed all 12 experiments and produced a terminal readout, but
the agent first proposed an infeasible crystallization seeding operation and triggered
one resource rejection before adapting. The repaired readout selected rank 8/8 with normalized
regret 1.0 and remained in the inadequate-law/wrong-action category. This confirms that the original
interruption can be crossed in a fresh session, while also exposing a genuine resource-planning risk
in the crystallization task. Because the repair has a different trajectory and contains a resource
rejection, it is not merged into the original 45-cell denominator.

# 8. Capability boundary and programme expansion

The public prospective cohort now closes the participant-to-evaluator chain. It supports a bounded claim
that initial world models reshape task-dependent search and that prediction error can decline without
selective wrong-prior correction. It also shows that executable syntax does not guarantee faithful law
compression and that reproducible recommendation does not guarantee action transfer. The
The formal multi-task assay extends this chain beyond incumbent replay across three task families: complete action semantics
and occasional law adequacy did not yield reliable unseen-plan selection. These are jointly observed
transition losses, not missing surrogate measurements.

The matched-evidence study resolves a three-layer outcome, and the longitudinal open-action study
identifies an additional action-transfer loss. The next studies address different causal questions.
A context-reset portability study can
compare typed laws with richer evidence artifacts and test portability. Private within-family
confirmation and matched cross-system replication can test stability and generality. None is a
repeat of the present analysis, and each requires a separate protocol and denominator.
Within-family replication remains distinct from compositional transfer.

# 9. Discussion

## 9.1 Why endpoint success is insufficient

The public cohort shows three reasons why endpoint success is insufficient. Correct information can
produce a durable advantage, as in entity-level partition; it can provide only an early head start that later
exploration narrows, as in structural crystallization; or explicit structure can help both aligned and
misindexed agents organize their search, as in structural partition. A deliberately wrong model may therefore
improve an endpoint by changing where an agent searches or by increasing useful experimental
diversity. Endpoint improvement measures the utility of an induced trajectory, not the truth of the
agent's scientific model.

## 9.2 Bias rejection must be behaviorally selective

The broad tendency to distrust any explicit model illustrates a second ambiguity. Generic skepticism
can generate the right verbal stance without identifying the wrong prior: final misindex suspicion was
slightly more common in aligned than misindexed cells. A valid correction measure must be selective:
contradictory evidence should improve wrong-prior predictions more than correct-prior predictions, and
that improvement should influence subsequent experimental choices. The prespecified evaluation shows
that this condition was not satisfied at any intervention locus, despite general prediction-error
reduction. The parametric locus provides a directional hypothesis for replication, but its $p=0.079$ result cannot be
treated as a passed locus.

## 9.3 Scientific understanding as a chain with measurable conversion losses

Prediction, explanation and action can dissociate. An agent may understand a relation but lack the
operational competence or remaining resources to exploit it; it may act successfully without an
accurate model; or it may state the right model while continuing to choose inconsistent experiments.
Here, this dissociation is observed directly: explicit predictions generally improved, executable
laws were worse than final predictions in 84/135 cells, and blind actions were equivalent to the
incumbent in 119/121 evaluable cells. The platform therefore turns an abstract capability hierarchy
into measurable transition losses. Future interventions can target evidence acquisition, numerical
revision, law compression or action transfer separately instead of optimizing one composite score.

## 9.4 Law adequacy is not sufficient for unseen-action selection

The longitudinal assay distinguishes action transfer from incumbent retrieval. The participant could
not blame an incorrect ranking on missing workflow details because every candidate was a complete
ActionPlan and the evaluator executed exactly the public sequence. Nevertheless, only 11/42 eligible
readouts selected the true Top-1 plan, and the sole law-adequate/wrong-action cell shows that law
adequacy is not sufficient for action correctness. This
does not show that a recovered law is causally harmful: the study is descriptive, three crystallization
cells were ineligible and only 12 task--world clusters retain all three arms. It does show a transfer
loss under distribution shift from self-selected experiments to a newly revealed candidate set.
Exploration support, conditional process knowledge and the ability to compose multiple decision-relevant
factors remain separate requirements.

## 9.5 The harness is part of the evaluated agent system

A persistent agent session contributes capabilities that a stateless model call does not: it retains
the campaign history, chooses among tools after each observation and can revise a plan without a host
reconstructing its reasoning state. The same harness also introduces failure surfaces through tool
discovery, schema conformance, retry rules, context growth and checkpoint submission. Context reuse
changes resource use but not the number of experiments or independent worlds. Consequently, the
participant is the fixed combination of model, reasoning setting, prompt, persistent session, tool
interface and resource policy—not the model weights in isolation. A cross-system claim requires these
components to be matched or explicitly manipulated; this study therefore treats the agent-system
configuration as the unit of interpretation.

## 9.6 Scope and limitations

The study evaluates bounded executable chemical worlds rather than universal chemical fidelity or
direct wet-laboratory validity. A single fixed participant configuration supports conclusions
about that agent-system configuration, not language models in general. The public programme contains
nine task--locus combinations but only five independent worlds per task, so small and heterogeneous
effects cannot support broad equivalence or universal-benefit claims. Entity, parametric and structural
studies reached their prespecified participant denominators, whereas the observation-model screen
remained a scientific boundary and did not enter a participant study. The held-out evaluator completed prediction, law
compression and blind action for the public cohort; private confirmation, matched cross-system
replication and compositional transfer were not run.
The corrected structural matched-evidence study contains only five independent public worlds; its
exact sign-flip analysis and structural recovery assessment cannot establish a population-wide rate
of mechanism recovery. The earlier run affected by an evaluator omission is excluded from scientific
inference. The longitudinal open-action study is descriptive: it contains 42 eligible cells, three
retained crystallization failures and 12 complete three-arm task--world clusters, so its arm means
are not causal estimates. The independent aligned-arm repair is a sensitivity result with one resource
rejection, not a replacement cell. Context-reset artifact portability remains untested.
Ten cells contain discard-affected checkpoint timing that cannot be retrospectively repaired. Finally,
exact software replay does not eliminate implementation variability or interface burden; process
attempts, schema failures, resource rejection and session outcomes are reported as operational
characteristics rather than independent scientific samples.

# 10. Methods

## 10.1 World and initial-model construction

Each task instantiates an executable $W=(\mathcal{E},G,\Theta,O,C)$ and a participant-facing
$M_0=(\widehat{\mathcal{E}},\widehat{G},\widehat{\Theta},\widehat{O},\widehat{S})$. Prospective
worlds are selected deterministically from a set disjoint from exploratory worlds. Within each
world cluster, all arms share $W$, the resource card and stochastic identity; exactly one declared
component of $M_0$ changes. In the entity locus, aligned and misindexed dossiers contain identical fields, values,
wording and confidence language, while the latter applies a prespecified permutation to material
identifiers. Structural, parametric and observation-model extensions alter only their declared
agent-facing representation while retaining the external world and contract. A layer extension is
included only after a separate identifiability analysis confirms that aligned and misspecified encodings
are matched in information volume, wording, confidence, baseline plausibility and falsification cost.

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
$(E_{mis,pre}-E_{mis,post})-(E_{aligned,pre}-E_{aligned,post})$. The structural matched-evidence study uses five worlds, so all
$2^5$ sign flips are enumerated for the exact one-sided directional check and a Student-$t$ interval
is reported descriptively. Protocol-validation sessions are excluded. Structural-recovery counts use only
the submitted model summary and evidence assessment, never private reasoning text.

## 10.6 Open-action plan construction and analysis

For the five-world partition action assay, an outcome-blind generator constructed eight candidate
ActionPlans per world before participant execution. Candidate selection used only the declared plan
coverage criteria and could not read evaluator scores, participant trajectories, checkpoint outcomes or later
model responses. Every plan began from the same fresh-batch contract and disclosed its full operation
sequence and parameters. Independent validation executed all candidate and checkpoint truth queries
without additional model calls, verified exact replay and confirmed that the disclosed plan was the
plan evaluated.

After 12 participant experiments and the final checkpoint, the participant returned a complete
ranking and selected one candidate. Evaluator-owned outcomes were then used to calculate selected
rank, Top-1, raw regret, normalized regret, complete-ranking agreement and the joint mechanism--action
category. A cell was eligible only when all 12 experiments, five checkpoints, final ranking,
resource reconciliation and execution-integrity checks completed without contamination. All scheduled
cells remained in the denominator. Arm summaries are descriptive because this exploratory study had
only five worlds and two incomplete cells. The three additional interface validations used one world
seed per task and were evaluated only as interface checks, not as multi-world scientific evidence.

## 10.7 Optional private confirmation boundary

No private participant cohort was executed for the present study. If private confirmation is pursued,
it will use newly sealed world instances disjoint from exploratory and public worlds, retain the same
three-arm participant and evaluator contracts, and preserve every completed, failed and unstarted
cell in a one-shot denominator. Such a cohort would test within-family replication. A separate
context-reset artifact-portability design would still be required for a compositional-transfer claim.

## 10.8 Reproducibility and failure accounting

Participant trajectories, evaluator truth sets and blind-replay sets are stored separately and joined
through stable record identifiers. Every completed participant trajectory must pass physical replay,
campaign-resource replay and hidden-boundary verification. Process attempts, sessions, tool calls,
operation attempts, committed operations, complete experiments, cells and evaluator executions are
reported with distinct denominators.

# 11. Data and code availability

The executable environment, prespecified protocols, analysis code, source data and reproducible figure
scripts will accompany the public release. Raw interaction payloads and credentials are excluded. No
private cohort data are included because that optional study was not executed.

# 12. Competing interests

The authors declare no competing interests.
