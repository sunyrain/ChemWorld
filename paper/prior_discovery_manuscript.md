---
title: "From Evidence to Action: Diagnosing Scientific Agents Across Experimentation, Law Formation, and Decision Transfer"
title_line_one: "From Evidence to Action"
title_line_two: "Diagnosing Scientific Agents Across Experimentation, Law Formation, and Decision Transfer"
subject: "Controlled diagnosis of evidence acquisition, predictive revision, executable-law formation, unseen action selection and evaluator validity in scientific agents"
keywords: "AI scientist; autonomous experimentation; scientific agency; model correction; executable law; unseen action selection; evaluator validity; chemical worlds"
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
  Scientific agents are often evaluated by the best outcome reached during an experimental campaign,
  conflating evidence acquisition, predictive revision, law formation and action selection. We study
  these transformations separately in ChemWorld, a suite of resource-bounded chemical environments
  with persistent state, complete executable action plans, held-out prediction queries, typed laws and
  exact replay. Across 135 public agent sessions spanning entity, parametric and structural
  initial-model interventions, agents frequently improved outcomes and predictions within a session,
  yet the value of a correct prior was strongly task dependent and executable-law fidelity remained
  limited. Controlled matched-evidence studies showed that direct counterevidence could correct
  numerical predictions without reliably recovering the registered structural law. In fresh
  multi-task action selection, only 11 of 42 eligible sessions chose the true best unseen plan.
  Finally, we found that the oracle control itself must match the decision estimand: a 96-query oracle
  passed a complete-ranking correlation gate in 7 of 8 fresh units but selected the true top action in
  only 1, whereas a 320-query oracle failed the same gate on its first new world despite selecting the
  true best action with zero regret. These results establish evidence acquisition, numerical revision,
  structural identification, action transfer and evaluator validity as distinct requirements for
  trustworthy scientific agents.
---

# 1. Introduction

An experimental agent can succeed without learning the right science. It may inherit a correct model,
stumble into a productive region or patch its actions while retaining a false explanation of the
world. An endpoint benchmark assigns the same success to all three cases. For scientific agents,
however, they represent fundamentally different capabilities: prior knowledge, local optimization
and evidence-driven correction. The question is not whether an AI scientist finds a good experiment,
but what that experiment changes in its model of the world.

This distinction is becoming consequential as language-model agents plan syntheses, call chemistry
tools, operate instruments and participate in self-driving laboratory workflows
[@boiko2023autonomous; @bran2024augmenting; @szymanski2023alab; @darvish2025organa;
@song2025chemagents; @vriza2026instruments]. Interactive environments likewise test repeated cycles of
hypothesis formation, intervention and inference [@jansen2024discoveryworld; @gandhi2025boxinggym;
@duan2025scigym; @zheng2026newtonbench; @yang2026causalab; @batzoglou2026replayscm]. Yet apparent
scientific success remains difficult to interpret because pretrained knowledge, prompt-provided
information, experiment selection, endpoint optimization and verbal explanation are usually observed
together. A useful outcome does not reveal whether evidence changed where an agent searched, improved
its counterfactual predictions, weakened a contradicted model, produced an executable relation or
supported a decision under conditions it had not encountered.

The unresolved problem is one of identification. Physical autonomous laboratories establish
consequential experimental competence, while virtual discovery environments make repeated studies
scalable. Neither setting generally provides the matched counterfactual needed here: the same
executable world encountered by agents that receive equally explicit but differently correct initial
models. Without that comparison, a correct prior can masquerade as rapid discovery, a wrong prior can
improve an endpoint by encouraging useful exploration without ever being rejected, and a plausible
verbal law can remain inconsistent with the agent's predictions or actions. Scientific correction
therefore cannot be inferred from endpoint score or self-report alone.

We address this problem by treating the agent's initial world model as an experimental variable.
ChemWorld allows the external chemistry, action space, observations, resources and stochastic identity
to remain fixed while the agent-facing description is made opaque, aligned with the world or
systematically misspecified at one declared locus [@qiu2026chemworld]. The intervention can target
entity identity, dynamical parameters or process structure. One persistent agent then conducts a
shared-resource campaign, and evaluator-owned counterfactuals measure how the intervention propagates
through experiment selection, prediction, explicit model revision and terminal action. The ChemWorld
foundation study establishes the executable substrate and its replay properties; those platform
qualifications are not reused here as evidence of agent capability.

We applied this design to a fixed DeepSeek-V4-Flash experimental-agent configuration across 45 matched
task--world clusters and 135 prospective campaigns. Fixed checkpoints bound the participant's beliefs
to independently evaluated predictions and typed executable summaries. Matched-evidence sessions
separate failure to acquire diagnostic evidence from failure to revise a model after seeing it. Blind
incumbent replay tests reproducibility of a committed observed action, while a separate multi-task
  assay reveals eight complete, previously unseen ActionPlans only after autonomous exploration and
  measures terminal ranking without hidden workflow defaults. A five-condition follow-up was designed
  to compare no evidence, yoked evidence, autonomous exploration, a transferred learned law and a
  provider-free oracle law, but its oracle control failed the frozen rank gate in a fresh formal world
  before any participant session began. Expanding the oracle fitting grid from 96 to 320 queries
  repaired exposed construction failures but did not restore prospective complete-ranking validity.
  A frozen reanalysis then showed that rank-gate success and correct action were not interchangeable.
  These outcomes distinguish experimental search, predictive learning, selective model correction,
  executable-summary fidelity, unseen action selection and evaluator validity rather than collapsing
  them into one score.

The resulting picture is not a single success or failure. Initial models altered search in
reproducible but task-dependent ways. Experimental evidence generally improved predictions, yet did
not selectively repair the wrong initial model at any intervention layer. Direct contradictory
evidence could produce accurate numerical revision without recovery of the governing structure, and
executable summaries often discarded information present in explicit predictions. Finally, the agent
showed partial and strongly task-dependent ability to rank unseen plans, but successful action was not
aligned with thresholded law adequacy. Scientific agency therefore behaved as a set of separable
transitions rather than a scalar capability. By holding the world fixed while intervening on the
agent's starting model, the framework shifts evaluation from whether an agent finds a good experiment
to identifying which scientific transformations its evidence actually supports.

```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/prior-discovery/figure-1-prior-to-law.pdf}
\caption{\textbf{Endpoint success does not reveal what the agent learned.}
\textbf{a,} The current entity-level instantiation uses opaque, aligned and misindexed dossiers in the same fixed executable world; the same intervention logic can target structural, parametric or observation-model assumptions.
\textbf{b,} One persistent session repeatedly predicts, selects an operation, observes the public outcome and updates its belief and executable law summary across a shared-resource campaign.
\textbf{c,} Participant trajectories and evaluator-owned held-out truth remain separate until the campaign ends; prediction error, calibration and blind recommendation outcomes are scored afterward.
\textbf{d,} Predictive recovery and evidence-aligned unseen-plan selection define four distinguishable phenotypes. Endpoint success or a correct statement alone does not identify which conversion succeeded.}
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
4. **Executable-law consistency:** whether the final typed summary executes on prespecified held-out
   coordinates and preserves the quality of the agent's conditional predictions.
5. **Unseen-plan selection:** whether the terminal agent state supports ranking and selecting
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
4. **Future artifact portability (not executed).** After source-world learning, raw evidence,
   prose summaries or executable laws could be transferred to a context-reset agent in a new
   combination. This future study is not part of the present evidence, and within-family replication
   remains separate from compositional transfer.

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
\textbf{a,} The entity/ontology backbone uses five task families and five independently selected public worlds per task.
\textbf{b,} Every matched task--world cluster contains opaque, aligned and misspecified initial models for one declared locus. Campaign length and checkpoints are owned by the locus pattern rather than forced into one universal four-experiment limit.
\textbf{c,} Executed free-discovery, matched-evidence, law and unseen-plan assays retain separate sessions, evidence and denominators; context-reset portability is shown in grey as future work.
\textbf{d,} The prospective entity, parametric and structural blocks total 45 task--world clusters, 135 sessions and 1,260 planned experiments. The diagram is a design map, not outcome evidence.}
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

The formal multi-task matrix contains three task families, five worlds per task and three initial-model
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

Failed scientific cells remain in the denominator and are not replaced. A right-censored cell carries
its last valid checkpoint forward; a missing final prediction receives zero primary improvement. Only
a pure infrastructure failure without a persisted trajectory may resume under the prespecified attempt cap.

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
not compete with the main causal narrative.

# 6. Causal dissection of the evidence-to-law chain

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

## 6.2 The prior intervention enters the trajectory but does not impose one performance ordering

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
measurement, comprising 872 instrument uses. The intervention changed the trajectory, and the agent
continued to collect and use public outcomes.

Those trajectory changes produced three recurring endpoint patterns. In entity-level partition,
aligned information produced a durable advantage over the misspecified arm: +0.106 on the first
experiment and +0.200 at the best endpoint, both concordant in 5/5 worlds. In structural
crystallization, the aligned model gave a +0.141 first-experiment head start in 5/5 worlds, but the
best-endpoint gap narrowed to +0.055 as the initially disadvantaged arm explored. In structural
partition, both aligned and misspecified descriptions outperformed opaque identifiers while differing
little from one another, consistent with shared search scaffolding rather than correct-model utility.
The remaining task--locus groups were heterogeneous. A correct initial model was therefore neither a
universal advantage nor a stable endpoint ordering.

## 6.3 Prediction learning does not become selective wrong-model repair

All three intervention loci showed mean pre-to-final prediction-error reductions in every arm. For
the entity locus, reductions were 0.111, 0.097 and 0.097 for opaque, aligned and misspecified cells;
for the parametric locus they were 0.090, 0.033 and 0.065; and for the structural locus they were
0.219, 0.228 and 0.221. The agent acquired predictive information during free discovery.

The prespecified causal estimand was stricter. Evidence should improve the misspecified arm more than
the aligned arm while preserving aligned performance. This selective-correction criterion failed at
all three loci. Failure-aware contrasts were **-0.214** for entity ($p=0.990$), **+0.033** for
parametric ($p=0.079$) and **-0.224** for structural ($p=1.000$). The positive parametric direction is
a replication hypothesis, not a passed locus. Structural crystallization and partition also pointed
in opposite directions, defeating the required cross-task structural decision. General predictive
learning and selective correction of a wrong starting model are thus empirically different
transitions.

```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/prior-discovery/figure-3-prior-uptake-and-correction.pdf}
\caption{\textbf{Initial models redirect search, but evidence does not selectively repair the wrong model.}
\textbf{a,} Mean pre-evidence normalized prediction error by locus and initial-model arm; correctness does not impose a uniform starting-error ordering.
\textbf{b,} Fraction of 45 matched task--world clusters in which the first complete experimental recipe differs between each pair of arms. This retrospective manipulation check has no repeated same-arm baseline.
\textbf{c,} Mean pre-to-final prediction-error reduction. Every arm improves at every locus.
\textbf{d,} Prespecified failure-aware selective-correction contrasts and locus $p$ values. Positive values favor greater repair in the misspecified arm; no locus passed.}
\label{fig:prior-uptake-correction}
\end{figure*}
```

## 6.4 Matched evidence localizes the structural bottleneck

Free discovery cannot by itself distinguish failure to seek diagnostic evidence from failure to use
evidence once obtained. The matched-evidence assay holds the evidence itself fixed. In the parametric
block, all five misspecified summaries rejected the supplied high-potential direction and recovered
the peak-and-collapse response. The free-discovery loss therefore contains an evidence-acquisition
component: when the decisive response profile was supplied, the agent could recognize it.

The corrected structural assay produced a sharper dissociation. After all three arms received the
same direct phase-process evidence, mean normalized errors fell from 0.2255, 0.2736 and 0.3392 to
**0.0074, 0.0060 and 0.0071** for opaque, aligned and misspecified cells. The misspecified-minus-aligned
update-gain contrast was +0.0645, but only 3/5 worlds were positive (exact one-sided sign-flip
$p=0.125$; descriptive 95% interval $[-0.0557,0.1848]$). This is numerical convergence under matched
evidence, not a confirmatory arm effect.

Structural identification nevertheless failed. **0/5** misspecified public summaries recovered the
prespecified 1.75 power law, only **1/5** explicitly rejected the supplied linear form, and **5/5**
shifted to a saturation or endpoint model. Direct evidence was sufficient for accurate local
prediction but not for identifying the governing relation. Evidence acquisition, numerical belief
revision and structural-law identification are therefore separate transitions. The intervention is
causal at the starting prior; this downstream localization is a diagnostic dissociation, not a causal
mediation analysis.

```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/prior-discovery/figure-4-matched-evidence-localization.pdf}
\caption{\textbf{Matched evidence restores numerical predictions without structural identification.}
\textbf{a,} Pre-to-post structural prediction errors for all 15 corrected matched-evidence cells; every arm receives identical direct phase-process evidence.
\textbf{b,} Post-evidence errors converge near zero in opaque, aligned and misspecified cells.
\textbf{c,} Misspecified-minus-aligned update-gain contrasts across five independent worlds; the dashed line is the mean and the five-world result is non-confirmatory.
\textbf{d,} Public-summary recovery among the five misspecified cells. Numerical convergence and saturation-style empirical models are universal, whereas explicit rejection of the linear prior is rare and exact 1.75-law recovery is absent.}
\label{fig:matched-evidence-localization}
\end{figure*}
```

## 6.5 Executable syntax does not guarantee faithful scientific compression

All **135/135** final typed laws executed on their prespecified continuous coordinates, but
executability did not preserve the information in the agent's conditional predictions. Mean law MAE
was 0.237. Relative to the effective final predictions, executable laws were better in 50 cells,
equal in one and worse in 84; mean law-minus-final error was +0.069. Even in the structural locus,
where pre-to-law improvement was largest, law error remained higher than final explicit-prediction
error on average. The typed interface solved syntax and coverage, not faithful model compression.

Paired blind replay tested a still narrower claim: whether the final commitment reproduced the value
of an observed incumbent. It completed **726/726** executions for 121 evaluable cells; the 14 failed
or right-censored cells remained as unstarted. Recommendations were better, equivalent and worse than
the incumbent in **1/119/1** cells. This demonstrates reliable incumbent retrieval, not selection
beyond the observed campaign. A separate assay is required for unseen plans.

The checkpoint interface is part of this evaluated system. Although all checkpoints were eventually
recovered, 888 typed-checkpoint submissions were rejected before acceptance. This burden did not
remove prediction payloads, but it increased context and recovery work. Results therefore apply to
the complete agent--tool configuration rather than the base language model alone.

```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/prior-discovery/figure-5-capability-chain.pdf}
\caption{\textbf{Predictive learning, selective correction, executable-law compression and incumbent replay dissociate.}
\textbf{a,} Failure-aware selective-correction contrasts across all 45 matched task--world clusters; circles show observed contrasts, vertical ticks retain adverse failure-aware bounds and diamonds show task means. Prespecified locus $p$ values are shown.
\textbf{b,} Mean pre-to-final normalized prediction-error reduction by intervention locus and initial-model arm.
\textbf{c,} Final executable-law MAE minus final explicit-prediction MAE for all 135 cells. Positive values indicate lossy compression.
\textbf{d,} Blind incumbent-replay outcomes for all 121 evaluable cells; 14 incomplete participant cells remain in the denominator as unstarted.}
\label{fig:public-capability-chain}
\end{figure*}
```

# 7. Terminal selection among unseen experimental plans

## 7.1 Complete plan semantics remove a hidden-workflow explanation

Blind incumbent replay asks whether a recommendation can reproduce an observed batch; it does not
test decisions outside the campaign history. We therefore used a second assay in which the agent
first explores freely for 12 experiments and only then ranks eight unseen plans. Every candidate is a
complete ActionPlan, including ordered operations, submitted parameters, measurement positions and
terminal assay. Public, evaluator-truth and executed plans were verified as identical, and no
evaluator-owned default could silently alter a workflow. Candidate outcomes and ranks remained
hidden. An incorrect ranking therefore cannot be attributed to undisclosed execution semantics.

## 7.2 Terminal selection is partial and strongly task dependent

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

Across eligible cells, **11/42** terminal readouts selected the true Top-1 plan; mean selected rank was
3.31/8 and mean normalized regret was 0.297. The uniform-random rank of 4.5 is a geometric reference,
not a causal baseline: the design contains neither a no-evidence action arm nor a pre-exploration
ranking from the same agent. The study therefore describes post-campaign selection competence but
does not estimate how much exploration or a recovered law caused it.

The joint mechanism--action result exposes the boundary more sharply. **30/42** cells had an
inadequate law and wrong action, **11/42** had an inadequate law but correct action, **1/42** had an
adequate law but wrong action, and **0/42** combined an adequate law with a correct action. The single
law-adequate/wrong-action cell is a counterexample to logical guarantee, not a population estimate of
law sufficiency; correct action also occurred without thresholded law adequacy.

Performance varied substantially by task. Electrochemical conversion reached Top-1 in 4/15 cells
with mean rank 3.60, reaction safety in 4/15 with mean rank 2.00, and crystallization in 3/12 with mean
rank 4.58. Every pairwise arm-rank contrast changed sign under some leave-one-cluster-out omission.
Arm means are therefore descriptive, not causal. The bounded result is that complete public action
semantics and autonomous exploration did not yield uniformly reliable ranking of unseen plans.

```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/prior-discovery/figure-6-open-action-formal.pdf}
\caption{\textbf{Action selection and evaluator validity separate.}
\textbf{a,} Selected true rank for 42 eligible W2-50 cells; three crystallization failures remain in the 45-cell scheduled denominator and the random-rank line is not an experimental control.
\textbf{b,} Joint law--action categories for the same cells.
\textbf{c,} W2-51 and W2-52 qualification funnels retain passed, scientifically rejected and unstarted units; exposed construction and fresh qualification are separate evidence roles, and participant execution is zero.
\textbf{d,} Complete-ranking Spearman correlation and normalized regret for all 16 frozen W2-53 unit versions. Stars mark Top-1 selection; the panel adds no execution and changes no historical stop decision.}
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

## 7.4 The causal action-transfer follow-up failed before participant execution

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

## 7.5 A denser oracle grid repairs exposed failures but not prospective ranking

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

## 7.6 Complete-ranking validity and action validity are different estimands

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

# 8. A transition map of scientific agency

The experiments replace a scalar notion of scientific success with a transition map. The controlled
intervention is the correctness of the agent's initial model. Downstream, the study observes whether
that perturbation changes search, whether acquired evidence changes counterfactual predictions,
whether those predictions can be compressed into an executable relation and whether the final state
supports selection among unseen plans. A failure at one transition need not erase competence at
another.

For the evaluated agent system, the map contains five robust boundaries. Initial models redirect
search but do not confer a general endpoint advantage. Free experimentation improves predictions but
does not selectively repair the wrong starting model. Direct matched evidence can produce near-exact
numerical revision without structural-law recovery. Executable summaries and terminal decisions each
lose information in different ways. Finally, complete-ranking validity does not determine action
validity. These are not five versions of the same score; they are
empirically separable transformations.

The map also defines the next experiments without making them part of the current result.
Context-reset artifact portability is required to test whether a learned representation survives
outside the source conversation. We attempted to add no-evidence, yoked-evidence and artifact-only
ranking controls for unseen-plan selection, but the oracle-law control did not qualify in a fresh
formal world. Any future causal action-transfer study therefore requires a new control construction
that first demonstrates robust fresh-world decision validity under action-aligned endpoints. Private
within-family replication and matched
cross-system studies would test stability and generality. Each is a distinct estimand with its own
denominator.

# 9. Discussion

## 9.1 The scientific object is a transformation, not an endpoint

Endpoint success answers whether a trajectory found something useful. It does not identify why.
Entity-level partition, structural crystallization and structural partition demonstrate three
different routes to a good result: durable utility from correct information, a head start later
narrowed by exploration, and search scaffolding supplied by both correct and incorrect structure.
Even a wrong model may improve an endpoint by redirecting exploration. Endpoint score is therefore a
property of an induced trajectory, not a direct measure of the truth of the agent's internal model.

The initial-prior intervention supplies the missing causal comparison. Because the world, public
contract, tools, resources and task identity are fixed within matched clusters, differences among
arms can be attributed to the starting epistemic condition under the evaluated agent configuration.
That claim ends at the intervention. Prediction, law and action results locate observed downstream
dissociations; they are not causal mediation estimates of how one hidden internal state produced the
next.

## 9.2 Matched evidence separates acquisition, revision and identification

The most informative result is not simply that selective correction failed. It is where the failure
moves when evidence is controlled. In free discovery, the agent may fail because it never acquires the
decisive observation. Parametric matched evidence shows that this matters: all five misspecified
agents rejected the supplied direction once the peak-and-collapse response was placed in front of
them. Yet the corrected structural study goes further. Identical direct evidence drove numerical
prediction error near zero in every arm, while none of the five misspecified summaries recovered the
governing 1.75-power relation.

Accurate interpolation after diagnostic evidence is thus not equivalent to structural
identification. An agent can revise numbers, adopt a useful empirical saturation description and
still fail to express the mechanism that generated the evidence. This distinction matters for
scientific use because structural representations support counterfactual reasoning, communication and
reuse in ways that a locally fitted endpoint model may not. The experiment does not establish a
population rate of mechanism recovery; it demonstrates an identifiable transition that larger
studies can target.

## 9.3 Scientific representations lose information on the way to action

The executable-law interface reveals another conversion loss. Every submitted law executed, but 84
of 135 were less accurate than the corresponding final explicit predictions. Formal validity is
therefore not faithful scientific compression. The agent may hold a conditional collection of
predictions that cannot be preserved in one compact submitted relation.

The unseen-plan assay exposes a different boundary. Complete public ActionPlans remove hidden workflow
defaults as an explanation, yet selection remains task dependent and thresholded law adequacy does
not align cleanly with correct action. Because the study lacks a pre-exploration or no-evidence
ranking baseline, this is not evidence for or against a causal action-transfer effect. It is evidence
about the terminal state reached by the full campaign: some unseen plans are ranked well, but the
ability is uneven and does not reduce to the submitted law.

The failed five-condition preparation sets a second boundary. A nominally oracle artifact is not a
valid positive control merely because its fitting procedure is outcome-disjoint or succeeds in
development worlds; it must preserve the decision-relevant ordering in the fresh worlds where the
causal comparison is made. Stopping before participant execution prevents a weak control from turning
an uninterpretable contrast into an apparent action-transfer effect.

The 96- versus 320-query diagnostic sharpens this point. Global ordering and decision quality can
disagree in both directions: most fresh 96-query units passed the correlation gate while selecting the
wrong action, whereas the first fresh 320-query unit failed the gate while selecting the optimum.
Evaluator validity is therefore part of scientific-agent validity. A control should be qualified on
the estimand needed by the causal contrast, not on a convenient surrogate that can succeed or fail for
decision-irrelevant parts of the ranking.

## 9.4 The harness is part of the scientific system

Persistent sessions provide memory, repeated tool choice and belief revision that stateless calls do
not. They also create failure surfaces through schema conformance, context growth, recovery rules and
finite resources. All checkpoints were eventually recovered, but the large number of rejected typed
submissions shows that the measurement interface affects the trajectory being measured. The
participant is therefore the fixed combination of model, reasoning setting, prompt, persistent
session, tools and resource policy. Cross-system comparisons must match or explicitly manipulate
those components rather than attributing the result to model weights alone.

## 9.5 Scope and limitations

ChemWorld provides bounded executable causal worlds, not universal chemical fidelity or direct
wet-laboratory validation. One fixed DeepSeek-V4-Flash agent configuration supports conclusions about
that system, not language models in general. The prospective programme spans nine task--locus
combinations but only five independent worlds per task. Observation-model interventions, private
confirmation, cross-system replication and context-reset artifact portability were not executed.

The corrected structural matched-evidence result contains five worlds and is explicitly
non-confirmatory. The earlier structural run affected by an evaluator omission is excluded. The
unseen-plan study has 42 eligible cells, three retained crystallization failures and only 12 complete
three-arm clusters; arm means are descriptive. Its random-rank line is not an experimental control.
The separate five-condition follow-up produced no participant data: one of the first eight formal
oracle controls failed its frozen rank criterion, and the remaining seven clusters were not started.
The denser oracle construction passed only on seven exposed units and its prospective qualification
stopped after the first new world; the rank/action alignment result is a retrospective diagnostic over
16 completed unit versions, not a new causal participant study. The single-stratum matched extension
pilot is development-only and does not repair the missing five-condition estimate.
Ten prospective cells also contain discard-affected checkpoint timing that cannot be repaired
retrospectively. Exact software replay preserves execution semantics but does not erase interface
burden or implementation variability.

## 9.6 Conclusion

The question is not whether an AI scientist finds a good experiment, but what that experiment changes
in its model of the world. Controlled interventions on the starting model, evaluator-owned
counterfactuals and matched evidence make those changes separately observable. In the present agent,
search, prediction, selective correction, structural identification, executable compression and
terminal decision do not rise and fall together, and the evaluator's complete-ranking gate does not
substitute for decision validity. Scientific agency is not a score; it is a sequence of evidence-driven
transformations whose failures can occur in the agent or in the control used to evaluate it.

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
cell in a one-shot denominator. Such a cohort would test within-family replication. A separate
context-reset artifact-portability design would still be required for a compositional-transfer claim.

## 10.8 Reproducibility and failure accounting

Participant trajectories, evaluator truth sets and blind-replay sets are stored separately and joined
through stable record identifiers. Every completed participant trajectory must pass physical replay,
campaign-resource replay and hidden-boundary verification. Process attempts, sessions, tool calls,
operation attempts, committed operations, complete experiments, cells and evaluator executions are
reported with distinct denominators.

# 11. Data and code availability

The current source release contains the executable environment, prespecified protocols, analysis code,
source data and reproducible figure scripts used for this manuscript. The fixed agent-system
configuration, prompt contract, reasoning setting and sampling parameters are bound in the release
metadata. Raw interaction payloads and credentials are excluded, and no private cohort data are
included because that optional study was not executed.

# 12. Competing interests

The authors declare no competing interests.
