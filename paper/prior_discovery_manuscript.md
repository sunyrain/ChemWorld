---
title: "Dissecting Executable Scientific Intelligence with Controlled World-Model Interventions"
title_line_one: "Dissecting Executable Scientific Intelligence"
title_line_two: "with Controlled World-Model Interventions"
subject: "Causal dissection of experimental search, predictive correction, executable laws and action in AI agents"
keywords: "AI scientist; autonomous experimentation; initial world model; world-model intervention; scientific priors; law discovery; counterfactual prediction; chemical worlds"
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
  world, operations and laboratory resources fixed within matched clusters. The public DeepSeek
  cohort reached terminal records for 135/135 sessions and completed 1,243/1,260 planned experiments
  across nine task--intervention combinations. Prior effects were strongly context dependent.
  Correct entity information produced a durable advantage in liquid--liquid partition, whereas
  correct structural information gave crystallization a five-world initial head start that largely
  narrowed during subsequent exploration. In structural partition, both correct and incorrect
  explicit models outperformed opaque identifiers, indicating that structured search guidance and
  model correctness can contribute separately. Agents nevertheless performed substantive
  within-session search: 84.4% of session optima occurred after the campaign midpoint, and 91.2% of
  completed recipes were unique. All 135 sessions submitted five belief checkpoints, comprising
  6,300 registered counterfactual query predictions and typed law summaries. A provider-free
  evaluator completed 420/420 truth executions, scored all 675 checkpoints, executed all 135 final
  laws and completed 726/726 launched blind replays. Prediction error generally decreased, but the
  registered selective-correction gate failed at all three intervention loci (A-E $p=0.990$, A-P
  $p=0.079$, A-S $p=1.000$). Executable laws were more accurate than final explicit predictions in
  only 50/135 cells and worse in 84/135. Blind recommendations were better, equivalent and worse
  than the observed incumbent in 1, 119 and 1 evaluable cells. A matched-evidence follow-up found
  a positive but mixed A-S misindexed-minus-aligned prediction-update contrast (+0.0645, 3/5 worlds,
  exact sign-flip $p=0.125$), while 0/5 misindexed summaries recovered the registered 1.75 law.
  Thus experimental adaptation, numerical belief revision, structural-law identification, law
  compression and action improvement form distinct capability layers.
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
external world and evidence opportunity remain fixed.

Here we introduce a controlled framework for studying how initial world models shape experimental
search and whether evidence produces scientific correction. It makes four contributions.

1. **The initial world model becomes a layered intervention.** Entity/ontology,
   structural/mechanistic, parametric/dynamical, observation/measurement and scope/compositional
   assumptions can be separated while the executable world remains fixed. Each matched comparison
   changes one locus rather than conflating all programmable dimensions.
2. **Discovery is evaluated through evidence-conditioned transitions, not self-report alone.** Fixed
   checkpoints bind beliefs to evaluator-owned counterfactual queries and to the next experimental
   operation selected by the agent.
3. **Endpoint success is separated from reusable understanding.** Blind outcome replay, executable
   law summaries and context-reset artifact transfer distinguish local optimization from law recovery.
4. **The complete experimental process remains auditable.** One persistent session controls multiple
   experiments under a shared resource ledger, while failures, invalid actions, stopping and exact
   replay remain part of the outcome rather than being silently repaired.

The terminal public cohort shows that this distinction is empirical rather than merely conceptual.
Aligned information gives a durable advantage in one entity-level partition task and a marked initial
head start in structural crystallization, yet it does not dominate across the nine task--locus
combinations. Structural partition further separates explicit organization from correctness because
both aligned and misindexed models outperform opaque identifiers. Persistent agents continue to
search, measure and improve after their first experiment, but their stated reliability and misindex
warnings do not selectively identify the incorrect model. We therefore organize the paper around a
bounded result: initial world models reshape experimental search, whereas scientific correction
requires a separate evaluator-scored transition from prediction to executable law and action.

```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/prior-discovery/figure-1-prior-to-law.pdf}
\caption{\textbf{From an initial world model to a reusable law.}
\textbf{a,} The current entity-level instantiation uses opaque, aligned and misindexed dossiers in the same fixed executable world; the same intervention logic can target structural, parametric or observation-model assumptions.
\textbf{b,} One persistent session repeatedly predicts, selects an operation, observes the public outcome and updates its belief and executable law summary across a shared-resource campaign.
\textbf{c,} Participant trajectories and evaluator-owned held-out truth remain separate until the campaign reaches a terminal state; prediction error, calibration and blind recommendation outcomes are scored afterward.
\textbf{d,} Predictive recovery and evidence-aligned action define four distinguishable phenotypes. Only their joint success, followed by transfer, supports a reusable-law claim; endpoint success or a correct statement alone does not.}
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

DiscoveryWorld, BoxingGym, SciGym, SciExplorer and NewtonBench organize tasks around repeated cycles
of hypothesis formation, intervention and inference [@jansen2024discoveryworld;
@gandhi2025boxinggym; @duan2025scigym; @nagele2026sciexplorer; @zheng2026newtonbench]. CausaLab and
ReplaySCM further emphasize interventional causal discovery and executable mechanism induction
[@yang2026causalab; @batzoglou2026replayscm]. SciDisco uses process-verifiable discovery environments
to provide intermediate training signals [@xu2026scidisco]. These studies motivate evaluating the
trajectory of discovery rather than only the final answer. Our focus is complementary: the hidden law
does not change during a matched campaign; what changes is the entity, structural, parametric or
observation-level model with which the agent enters that world.

## 2.4 The unresolved identification problem

Three ambiguities remain when endpoint score, belief statement and scientific understanding are not
separated. First, a correct prior can make an agent look like a rapid discoverer even if it merely
confirms supplied information. Second, a wrong prior can improve an endpoint by encouraging useful
exploration without ever being rejected. Third, a verbal law summary can be correct while the agent's
subsequent predictions or actions remain inconsistent with it. A matched prior intervention, typed
checkpoints and evaluator-owned tests are needed to distinguish these cases.

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
Entity / ontology & identity--property mappings, entity classes and property bundles & current development evidence and confirmatory core \\
Structural / mechanistic & causal topology, active process modules and dominant-pathway assumptions & separately registered extension \\
Parametric & coefficient signs, thresholds, orderings and plausible ranges & separately registered extension \\
Observation model & instrument mapping, reliability, bias and noise assumptions & secondary diagnostic probe \\
Scope / compositionality & applicability domains, invariant modules and transfer boundaries & context-reset artifact-transfer study \\
Contract / resource boundary & budget, safety, action permissions and actual observation interface & authoritative and fixed; never treated as a manipulable prior \\
\bottomrule
\end{tabularx}
\end{table*}
```

Within any selected layer, intervention quality follows the same logic:

- **Opaque:** no additional task-specific claim is supplied for the manipulated layer.
- **Aligned:** incomplete information is directionally consistent with the fixed world.
- **Misspecified:** an equally detailed and equally confident model is wrong at the frozen target layer.

The current entity/ontology implementation realizes the misspecified condition through a misindexed
dossier: the same property bundles, fields, values, wording and confidence language are retained, but
the bundles are permuted across material identifiers. Structural, parametric and observation-model
interventions require their own matched encodings and identifiability qualification; they cannot be
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

## 3.3 Four separable outcomes and one capability chain

We distinguish four outcomes that are often collapsed into a single score, while recording the
intermediate transitions that connect them.

1. **Endpoint optimization:** whether the campaign identifies a high-quality experimental outcome.
2. **Predictive recovery:** whether held-out counterfactual prediction error decreases.
3. **Prior correction:** whether evidence selectively improves the wrong-prior condition without
   degrading the correct-prior condition.
4. **Reusable law recovery:** whether the final executable summary predicts unseen continuous
   conditions and supports held-out control or transfer.

The process-level chain is therefore

```{=latex}
\begin{center}
\small initial world model $\rightarrow$ experiment selection $\rightarrow$ evidence acquisition\\
$\rightarrow$ prediction / belief update $\rightarrow$ executable law $\rightarrow$ action $\rightarrow$ transfer
\end{center}
```

The paper reports transition losses rather than a composite intelligence score: prediction-to-law
loss, law-to-action inconsistency and action-to-transfer loss. This makes it possible to identify
where a capability fails without treating a successful endpoint as proof that every upstream step was
correct.

An agent can succeed on any subset. In particular, endpoint success without predictive and transfer
validity is classified as local optimization rather than law discovery.

# 4. Study design

## 4.1 Chemical-world cohort and intervention studies

The programme is layer-stratified. Its entity/ontology backbone spans electrochemical conversion,
reaction followed by crystallization, reaction followed by distillation, phase-partition discovery
and safety-constrained reaction. Five independently selected public worlds per task yield 25
task-by-world clusters and 75 participant cells across opaque, aligned and misspecified arms.
Parametric/dynamical and structural/mechanistic blocks each contain two independently qualified task
families and five worlds per task, adding 30 participant cells per locus. Development, qualification
and public identities remain disjoint. A sealed private cohort is an optional stronger study and was
not executed in the current paper.

This design uses ChemWorld's programmability to manipulate different components of $M_0$, but does
not turn the paper into a full factorial benchmark. Every block changes one locus, has its own
identifiability gate and retains its own denominator:

1. **Study A — Initial-model-conditioned free discovery.** A-E tests entity/ontology models across
   five task families; A-P and A-S test parametric/dynamical and structural/mechanistic models across
   two qualified task families each. A cross-locus claim requires terminal evidence from all three
   predeclared blocks; an entity-only result remains entity-specific.
2. **Study B — Matched-evidence falsification.** A cloned-world secondary probe presents the same
   contradictory evidence to each arm, separating failure to seek evidence from failure to update
   after seeing it. The current evidence surface retains the unaffected A-P Study B block and a
   corrected A-S B2 phase-process block; the original A-S Study B branch is historical because its
   evaluator truth source omitted the registered world intervention. All matched-evidence sessions
   are independent and excluded from Study A denominators.
3. **Study C — Executable law and action.** Typed law summaries, held-out predictions and blind
   recommendations test the transitions from prediction to law and from law to action; no verbal
   statement alone counts as discovery.
4. **Study D — Artifact-only compositional transfer.** After source-world learning, raw evidence,
   prose summaries or executable laws are transferred to a context-reset agent in a new combination.
   No-artifact, trajectory and typed-law conditions are compared, and within-family replication is
   kept separate from genuine compositional transfer.

Observation/measurement interventions are registered as a separate boundary probe. They first require
two-task identifiability and a development triplet and do not enter the formal denominator without a
new user freeze. Scope/compositional assumptions are tested only in Study D. This preserves a complete
conceptual intervention space without claiming that every programmable coordinate has already been
executed.

Environment qualification and participant outcomes form separate evidence layers. Environment tests
establish that the hidden relations are coherent, identifiable and executable through the public
measurement surface. They do not show that an agent discovers those relations.

```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/prior-discovery/figure-2-formal-cohort.pdf}
\caption{\textbf{Layer-stratified study architecture.}
\textbf{a,} The entity/ontology backbone uses five task families and five public worlds per task; development and public identities are disjoint, and any future sealed private identities must remain disjoint from both.
\textbf{b,} Every matched task--world cluster contains opaque, aligned and misspecified initial models for one declared locus. Campaign length and checkpoints are owned by the locus pattern rather than forced into one universal four-experiment limit.
\textbf{c,} Parametric/dynamical and structural/mechanistic blocks require separate qualification; observation-model and scope/compositional studies retain separate admission decisions.
\textbf{d,} Free discovery, matched-evidence falsification, evaluator truth and action tests, within-family replication and context-reset artifact transfer retain separate sessions, resources and denominators. The diagram is a design map, not completed outcome evidence.}
\label{fig:formal-cohort}
\end{figure*}
```

## 4.2 Persistent experimental agent (Study A)

Each cell is controlled by one persistent Codex process and one provider session. After every public
outcome, the participant chooses the next operation through the host-owned laboratory tool. The host
validates schemas, executes transactions, updates resources and protects private state, but does not
select or repair scientific actions.

Campaign length is pattern-owned: A-E uses eight complete experiments with checkpoints after
0, 2, 4, 6 and 8 experiments; A-P uses ten with checkpoints after 0, 2, 4, 7 and 10; A-S uses twelve
with checkpoints after 0, 3, 6, 9 and 12. These pattern-owned counts and their finite resource cards
were fixed before the terminal participant cohort. A checkpoint records the
agent's assessment of initial-model reliability at the manipulated layer, predictions, uncertainty,
evidence references, executable law summary and next experimental intent. Checkpoints do not create
additional provider sessions.

## 4.3 Evaluator-owned evidence

The participant predicts four registered counterfactual queries per A-E checkpoint and 16 per A-P or
A-S checkpoint. The evaluator executes each unique task-world query set independently; truth is
shared across prior arms and checkpoints and is never returned to the participant. The primary
prediction error is the mean normalized absolute error across registered query-metric pairs. The
participant payloads and current-composite evaluation are complete: 420/420 truth executions produced
1,620 query--metric truth values and all 675 checkpoints were scored without provider calls.

The evaluator also executes each final typed law summary on the same registered query coordinates.
This produces a separate cell-level record of schema validity, complete query-metric executability,
truth-normalized error, error change relative to the pre-evidence and effective-final checkpoints,
and consistency with the participant's final explicit predictions. These public measures are
descriptive: no post-hoc binary validity threshold is applied, and reusable-law status remains
unavailable without the prespecified private transfer test.

After the campaign, the participant commits one completed experiment as its final recommendation.
The evaluator then performs paired blind replay of the observed incumbent and the committed
recommendation. These executions use separate resources and do not enter participant-operation or
provider denominators.

## 4.4 Hypotheses and estimands

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

For A-E, the misspecified arm is instantiated by the frozen misindexing and $C_{\ell}=C_E$ is the
confirmatory contrast. Success requires the lower confidence bound for the locus-specific contrast to
exceed zero, the wrong-prior condition to improve, and the aligned condition not to deteriorate beyond
a prespecified tolerance. Correct-prior utility, wrong-prior vulnerability and knowledge-to-action
translation form a hierarchical secondary family. A cross-locus conclusion requires concordant,
separately reported A-E, A-P and A-S results; standardized effects may be synthesized hierarchically,
but raw contrasts are not pooled as if their intervention semantics were identical. Observation-model
results remain a distinct boundary analysis unless separately frozen.
Endpoint, calibration, behavior, law-summary, transfer, resource and safety outcomes are reported as
separate channels rather than one leaderboard score.

Failed scientific cells remain in the denominator and are not replaced. A right-censored cell carries
its last valid checkpoint forward; a missing final prediction receives zero primary improvement. Only
a pure infrastructure failure without persisted trajectory may resume under the frozen attempt cap.

# 5. Development evidence

The following results qualify the method and sharpen the scientific question. They are not part of
the public C2 or any future private-confirmation denominator, and the two provider configurations are
not used for a cross-provider capability ranking. Sections 5.1--5.5 instantiate the entity/ontology
layer; Section 5.6 is a one-cluster parametric pilot. Neither block substitutes for the terminal
multi-locus cohort reported in Section 6.

```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/prior-discovery/figure-3-development-prior-effects.pdf}
\caption{\textbf{Provider-separated development evidence for prior-sensitive behavior.}
\textbf{a,b,} Paired world-seed differences in the best endpoint observed during four-experiment campaigns for aligned versus opaque and misindexed versus opaque information. Points are retained paired seeds and horizontal bars are descriptive means. WellAU/Codex contains five pairs per task except the aligned distillation contrast ($n=4$); DeepSeek recovery contains five pairs except the misindexed crystallization contrast ($n=4$).
\textbf{c,} Final explicit misindex warnings, shown as flagged cells over available terminal belief records for every provider, task and prior arm.
\textbf{d,} Completed-cell, complete-experiment and exact-replay denominators. Failures remain in the scheduled or terminal denominator and are not replaced. Panels a--c retain the common three-task paired endpoint/warning source used for provider-separated continuity; the complete five-task DeepSeek operational denominator is shown in the closeout table. All panels are development-only descriptive summaries; no confidence interval, formal hypothesis test or cross-provider capability comparison is performed. Endpoint gains and verbal warnings do not establish law discovery, selective wrong-prior correction or transfer.}
\label{fig:development-prior-effects}
\end{figure*}
```

## 5.1 Entity-level priors reshape endpoint behavior

One development matrix used the frozen persistent-session interface with a WellAU-provided Codex
model. It produced 44 completed cells out of 45 and 176 complete experiments out of 180. Mean paired
aligned-minus-opaque differences in the best observed endpoint were +0.211 for electrochemical
conversion, +0.057 for crystallization and -0.036 for distillation, with the distillation contrast
based on four complete pairs. Misindexed information was not consistently harmful, and explicit
misindex warnings included substantial false positives in aligned cells.

A recovery-amended DeepSeek development block was completed across all five task families, retaining
the immutable seed-0 gate records for partition discovery and safety-constrained reaction and adding
their seeds 1--4 in a separate continuation block. No seed-0 outcome was rerun or replaced. Every
scheduled cell reached a terminal record (**75/75**); **69/75** cells were completed and qualified,
with **290/300** complete experiments, **2,663/2,587** operation attempts/committed operations,
**73** validation failures, **3** resource rejections, **69** recovered MCP failures and **0**
provider-error events. Exact physical/resource replay passed for **75/75** terminal trajectories.
Provider accounting covered 72/75 cells; the remaining three stopped before a provider terminal event
and retain usage as unavailable rather than zero. The complete development block is still descriptive:
it is not part of the preregistered public matrix, has no private transfer confirmation or formal
hypothesis test, and provider groups are never pooled into a capability ranking.

```{=latex}
\begin{table*}[!t]
\centering
\caption{\textbf{Five-task DeepSeek development closeout.} All five task families reached the
scheduled five-seed terminal denominator. The partition and safety continuation preserved their
immutable seed-0 gate outcomes; their operational rows are reported descriptively and are not pooled
with the common three-task paired endpoint panels.}
\label{tab:deepseek-five-task-closeout}
\scriptsize
\begin{tabular}{lrrrrrr}
\toprule
Task & Terminal & Qualified & Experiments & Attempts/committed & MCP failures & Exact replay \\
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
\caption{\textbf{DeepSeek five-task development endpoint contrasts.} Values are descriptive paired-seed means in best endpoint score; the partition and safety rows are continuation observations and are not pooled into the common three-task Figure 3 endpoint panels.}
\label{tab:deepseek-development-contrasts}
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
contract; they do not support a pooled provider effect. A better endpoint therefore cannot be treated
as evidence that the agent accepted a correct prior, rejected a wrong prior or recovered the hidden
law.

```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/prior-discovery/figure-4-development-confirmation.pdf}
\caption{\textbf{Held-out evaluator confirmation of the five-task DeepSeek development matrix.}
\textbf{a,} Aligned-prior and misindexed-prior reductions in normalized held-out prediction error for all 25 task-by-world clusters. The identity line marks equal improvement; filled points are complete three-arm clusters and open points retain at least one failed arm under the frozen missing-outcome rule.
\textbf{b,} The primary development contrast $C_{\mathrm{prior}}$ by task and seed. Diamonds are task means; positive values favor greater correction in the misindexed arm.
\textbf{c,} Executable law-summary error minus final explicit-prediction error for 71 evaluable summaries. Negative values indicate beneficial compression.
\textbf{d,} Paired blind replay of the committed recommendation versus the observed incumbent for 69 qualified cells. The evaluator completed 414/414 replays with zero provider calls. All panels are development-only descriptive evidence; no formal test, private transfer claim or cross-provider ranking is performed.}
\label{fig:development-confirmation}
\end{figure*}
```

## 5.2 Held-out prediction improves, but entity-level correction is not selective

The post-hoc development evaluator executed four registered counterfactual queries for each of the
25 task-by-world clusters. All **100/100** truth queries completed with exact replay and without a
provider call. Final checkpoint predictions were scoreable for **72/75** retained participant cells.
Using the frozen failure rules, aligned-prior prediction error improved in 24/25 cells and
misindexed-prior error improved in 22/25 cells. Improvement was therefore common, but it was not
selectively stronger under the wrong prior: the primary contrast had a descriptive mean of
**$-0.042$**, median **$-0.039$**, and was positive in only **7/25** clusters. Restricting description
to the 19 complete-case clusters gave the same direction (mean **$-0.039$**; 6/19 positive). Only the
safety-constrained task had a positive task-level mean; the other four task means were negative.

The evaluator executed **71/75** final typed law summaries on the same registered coordinates. The
summary improved on the final explicit predictions in 12/23 opaque, 7/24 aligned and only 3/24
misindexed cells; it was worse in the remaining 11, 17 and 21 cells, respectively. Thus, an agent can
improve its checkpoint predictions without compressing that improvement into a reusable executable
law. Blind replay sharpened the action boundary: **414/414** scheduled executions completed across
69 qualified cells, but the committed recommendation beat the observed incumbent in 0 cells, was
equivalent in 66 and was worse in 3. These results do not prove that correction is impossible; they
show that endpoint gains, prediction repair, law compression and recommendation quality are distinct
development outcomes.

## 5.3 Verbal suspicion is not selective correction

Across available terminal belief records, final DeepSeek misindex warnings were 0/5, 5/5 and 3/5
for opaque, aligned and misindexed electrochemical cells; 0/4, 5/5 and 4/4 in crystallization;
0/5, 5/5 and 5/5 in distillation; 0/4, 2/4 and 3/4 in partition discovery; and 0/5, 2/4 and
0/5 in safety-constrained reaction. The model therefore often associated dossier presence with
possible misindexing, but the pattern was task-dependent and did not selectively distinguish the
correct and incorrect dossiers. Mean aligned-minus-misindexed changes in self-reported prior
reliability were small or heterogeneous across tasks, including negative changes in several
continuation cells.

This is a scientifically useful negative boundary. A warning token or reduced stated confidence is
not a valid bias-rejection endpoint unless it predicts evaluator-scored correction and subsequent
evidence-aligned action.

## 5.4 Persistent-session accounting exposes a separate operational layer

The 75 terminal DeepSeek trajectories accumulated **267,929,149 input tokens**, including
**260,033,536 cached tokens** (97.05%), **7,895,613 uncached input tokens** and **2,932,468 output
tokens**. These are cumulative turn-level provider counters for long-lived sessions. The large cached
fraction therefore reflects reuse of the shared prompt and growing campaign history; it is not
repeated model output and does not represent additional independent experimental evidence. Usage was
reconciled for 72/75 cells. The other three cells stopped before a provider terminal event, so their
usage remains unavailable rather than being imputed as zero.

Operational failures also require their own denominator. The matrix recorded 73 schema-validation
failures and 69 recovered MCP tool failures but no provider-error events. Moreover, 76 of 2,663
operation attempts did not become committed operations. Thus, a zero provider-error count would have
hidden most of the execution burden: model-to-tool conformance, recovery and resource preflight were
more consequential than provider transport in this block. These events are properties of the complete
agent system and remain separate from both physical outcomes and independent world-level scientific
samples.

## 5.5 Development conclusion

Across the retained development configurations, explicit priors clearly alter the course and endpoint
of experimentation, and most cells improve their held-out predictions. The same evidence does not
show selective wrong-prior rejection: aligned improvement exceeds misindexed improvement on average,
typed law compression is frequently lossy and committed recommendations do not outperform the
observed incumbent. These findings motivated the prospective public C2 cohort, while establishing
that prediction repair, law recovery and action quality must remain separate outcomes.

## 5.6 Parametric initial-model pilot: rejection is not recovery

We next asked whether this separation extends beyond entity-level dossiers to a parameter-level
initial world model. A provider-free screen selected one electrochemical seed in which an aligned
potential/current window and a matched but misspecified window were strongly separable in the
executable world. This screen fixed the intervention before any participant outcome was observed.
The subsequent development pilot retained one opaque, one aligned and one misspecified cell. Each
cell used one persistent WellAU `gpt-5.6-sol` medium Codex session, four complete experiments and four
belief checkpoints under a shared within-cell resource ledger.

All **3/3** cells, **12/12** participant experiments and **12/12** checkpoints completed. A separate
zero-provider evaluator completed **4/4** shared held-out truth queries and **18/18** paired blind
replays, all with exact replay. Normalized prediction error changed from **0.347 to 0.320** in the
opaque arm, **0.359 to 0.155** in the aligned arm and **0.420 to 0.198** in the misspecified arm. The
one-cluster correction contrast was therefore positive but remains descriptive.

The trajectory reveals a distinction hidden by aggregate error. The misspecified agent first tested
inside its supplied window and obtained a score of zero. It then reduced the model's stated
reliability from **0.70** to **0.12**, explicitly identified `potential_V` as the challenged field and
moved its second experiment **2.41 V** outside the supplied window; terminal reliability reached
**0.03**. This is behavioral model rejection rather than a free-standing verbal warning. Yet the arm's
best observed score was only **0.274**, compared with **0.568** for aligned and **0.670** for opaque.
The agent had learned that the supplied model was wrong without recovering the best finite-budget
experimental policy.

Final executable-law errors were **0.424**, **0.238** and **0.242** for opaque, aligned and
misspecified, respectively. All three committed recommendations selected their own observed
incumbent, so paired blind replay confirmed reproducibility but produced zero recommendation gain.
This one-world pilot motivated a broader two-task, five-world A-P block. It remains excluded from the
public C2 denominator and cannot itself support a cross-task or general initial-world-model claim.

# 6. Public C2 results

## 6.1 Terminal multi-locus participant cohort

The current public analysis combines 120 unaffected sessions from the corrected-semantics cohort with
a complete 15-session replacement of the A-S crystallization block after its resource contract was
requalified. All **135/135** scheduled sessions reached a terminal record. The participant completed
**1,243/1,260** planned experiments, and **121/135** sessions passed the operational qualification
contract. The denominator contains **1,269** closed batch lifecycles: 1,243 ended in a final assay and
26 were discarded. No dynamic physical failure occurred. Thirteen operations were rejected by the
finite laboratory resource ledger, and 84 participant operation attempts did not become committed
operations. These cells and attempts remain in their assigned denominators.

## 6.2 Prior effects separate into durable advantage, head start and search scaffolding

The strongest durable aligned-prior result occurred in A-E partition. Relative to the misindexed arm,
the aligned arm improved the first experiment by **0.106** score units and the best observed endpoint
by **0.200**; both contrasts had the same direction in **5/5** worlds. Here, correct entity information
changed both entry into the search space and the best region reached within eight experiments.

A-S crystallization showed a different pattern. The aligned structural model improved the first
experiment over the misindexed model by **0.141**, again in **5/5** worlds. The best-endpoint difference
then narrowed to **0.055** and was positive in **3/5** worlds. Aligned within-session improvement was
lower than misindexed improvement by **0.086** in every world. The structural model therefore provided
a reproducible head start, while subsequent free exploration allowed the initially disadvantaged arm
to recover part of the gap.

A-S partition separated structured guidance from model correctness. The aligned and misindexed arms
exceeded opaque identifiers in best endpoint by **0.163** and **0.143**, respectively, whereas their
mutual difference was only **0.020** and positive in 3/5 worlds. Supplying an explicit structural
decomposition helped organize the search, but the endpoint alone provided little stable separation
between the correct and incorrect versions of that decomposition.

The remaining task--locus combinations bounded these positive cases. A-E reaction safety had a small
aligned-minus-misindexed best-endpoint difference of 0.036 with concordant direction in 5/5 worlds.
The A-E distillation difference declined from 0.053 on the first experiment to 0.011 at the best
endpoint. A-E electrochemistry was heterogeneous, A-E crystallization favored the misindexed arm on
average, and neither A-P task showed a stable aligned endpoint advantage. Correct initial models were
therefore not a universal performance intervention.

## 6.3 Persistent agents continued to search and measured task-relevant states

All nine task--locus groups had a positive mean best-minus-first score. Across cells, **91.2%** of
completed experiments used a unique recipe, **84.4%** of session optima occurred after the campaign
midpoint and **32.6%** occurred in the final completed experiment. The observed prior effects cannot
be reduced to copying one supplied recipe; the persistent agent continued to use experimental
feedback throughout the campaign.

Every completed batch closed with a final assay, while non-final instrument use followed the process
path. A-E and A-S crystallization measured intermediate states in 95.0% and 98.4% of closed
lifecycles, A-S partition in 82.2% and distillation in 50.0%. A-E electrochemistry used no non-final
instrument because its registered lifecycle proceeded from electrolysis directly to the final assay.
Overall, **666/1,269** closed lifecycles contained a non-final measurement, comprising 872 instrument
uses. Instrument use should therefore be interpreted against task semantics, not as one global
autonomy score.

## 6.4 Complete belief submission did not establish selective correction

Every session submitted its pre-evidence, three intermediate and final checkpoint: **675/675** typed
belief snapshots in total. These snapshots contained **6,300** registered counterfactual query
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
failed MCP tool events, of which 888 were failed `commit_belief_snapshot` submissions; 900 failures
were classified as agent-invalid, compared with one transport/OS event and three unclassified events.
All five checkpoints were eventually recovered in every cell, so this burden did not create missing
prediction payloads, but it increased context and recovery work, especially for the 16-query A-P and
A-S schemas. The result belongs to the complete DeepSeek--Codex--MCP agent system rather than the
language model in isolation.

## 6.5 Prediction learning did not become selective wrong-model repair

The recovered current-composite evaluator executed **420/420** held-out truth queries, producing
1,620 query--metric truth values without a provider call, and scored **675/675** checkpoints. All
three intervention loci showed mean pre-to-final error reductions in every arm. For A-E, the opaque,
aligned and misindexed reductions were 0.111, 0.097 and 0.097; for A-P they were 0.090, 0.033 and
0.065; for A-S they were 0.219, 0.228 and 0.221. The agent therefore learned predictive information
during the campaigns. The A-S values come from the v0.2 world-intervention recovery; the v0.1
evaluator result is retained only as historical defect evidence.

The registered estimand was more demanding: the misindexed arm should improve more than the aligned
arm without degrading aligned predictions. This selective-correction gate failed at every locus.
The failure-aware primary contrasts were **-0.214** for A-E ($p=0.990$), **+0.033** for A-P
($p=0.079$) and **-0.224** for A-S ($p=1.000$). A-E passed the aligned noninferiority component but
not the misindexed-improvement component. Both A-P task means were positive, making the result
suggestive rather than confirmatory. In A-S, crystallization showed positive observed-point
correction whereas partition was negative; the required cross-task locus decision therefore failed.
Observed-point sensitivity did not reverse any locus decision. General predictive learning and
targeted repair of a wrong initial model were thus empirically distinct.

## 6.6 Executable laws were often lossy and blind actions rarely improved

All **135/135** final typed laws executed on their registered continuous query coordinates. Mean law
MAE was 0.237. Relative to the effective final explicit predictions, laws were better in 50 cells,
equal in one and worse in 84; mean law-minus-final error was +0.069. A-S showed the strongest
pre-to-law improvement (+0.206), but even there the law remained less accurate than the final
explicit predictions on average (+0.017). Syntax and executability were therefore solved, whereas
faithful compression of a conditional belief state into a reusable relation was not.

Paired blind replay retained all participant terminal states. It launched and completed **726/726**
executions for 121 evaluable cells; 84 pre-scheduled executions for seven failed and seven
right-censored cells were retained as unstarted rather than imputed. Recommendations were better,
equivalent and worse than the observed incumbent in **1/119/1** cells, with recovered mean gain about
$-0.0010$. The
final interface was highly reproducible but almost entirely retrieved an incumbent rather than
producing a new action advantage.

## 6.7 Matched evidence separated three transitions rather than yielding a binary label

The original A-S branch of Study B is not used for current scientific inference: its truth source
was generated before the evaluator forwarded the registered structural intervention. The unaffected
A-P block remains current, and a new A-S B2 block supplied 80/80 provider-free power-law truth queries
and direct phase-process evidence with disjoint phase-process scoring queries. B2 completed 15/15
two-turn sessions, 30/30 provider turns, 360/360 scoring terms per stage and zero failures.

For A-P, all five misindexed public summaries explicitly rejected the supplied high-potential
direction and recovered the peak-and-collapse response. This supports an evidence-acquisition
component in the free-discovery loss. For A-S B2, opaque, aligned and misindexed mean errors fell from
0.2255, 0.2736 and 0.3392 to 0.0074, 0.0060 and 0.0071. The registered misindexed-minus-aligned
update-gain contrast was **+0.0645**, positive in **3/5** worlds (exact one-sided sign-flip
$p=0.125$, descriptive 95% interval $[-0.0557, 0.1848]$). This is a mixed prediction-level signal,
not a confirmatory selective-correction result.

The structural audit was more restrictive: **0/5** misindexed summaries recovered the exact registered
1.75 power law, only **1/5** explicitly rejected the supplied linear partition form, and all five
shifted toward an empirical saturation or endpoint model. The agent therefore revised numerical
predictions after receiving law-level evidence but did not reliably identify the registered mechanism.
The resulting boundary is three-layered: evidence acquisition, numerical belief revision and structural
law identification are separable; neither a pure evidence-seeking bottleneck nor a pure stubborn-updating
claim is supported.

```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/prior-discovery/figure-5-public-c2-capability-chain.pdf}
\caption{\textbf{Prediction learning, scientific correction, executable-law compression and blind action dissociate.}
\textbf{a,} Failure-aware selective-correction contrasts across all 45 matched task--world clusters; circles show observed contrasts, vertical ticks retain adverse failure-aware bounds and diamonds show task means. Registered locus $p$ values are shown.
\textbf{b,} Mean pre-to-final normalized prediction-error reduction by intervention locus and initial-model arm.
\textbf{c,} Final executable-law MAE minus final explicit-prediction MAE for all 135 cells. Positive values indicate lossy compression.
\textbf{d,} Blind recommendation outcomes for all 121 evaluable cells; 14 nonterminal participant cells remain in the denominator as unstarted.}
\label{fig:public-c2-capability-chain}
\end{figure*}
```

# 7. Capability boundary and programme expansion

The public DeepSeek cohort now closes the participant-to-evaluator chain. It supports a bounded claim
that initial world models reshape task-dependent search and that prediction error can decline without
selective wrong-prior correction. It also shows that executable syntax does not guarantee faithful law
compression and that reproducible recommendation does not guarantee action improvement. These are
jointly observed transition losses, not missing surrogate measurements.

The matched-evidence stage is now terminal with this qualified three-layer outcome. The next programme
stages address different causal questions. A context-reset Study D can compare typed laws with richer
evidence artifacts and test portability. Private within-family confirmation and matched cross-provider
replication can test stability and generality. None is a repair run for the present result, and each
requires a separate protocol and denominator. Within-family replication remains distinct from
compositional transfer.

# 8. Discussion

## 8.1 Why endpoint success is insufficient

The public cohort shows three reasons why endpoint success is insufficient. Correct information can
produce a durable advantage, as in A-E partition; it can provide only an early head start that later
exploration narrows, as in A-S crystallization; or explicit structure can help both aligned and
misindexed agents organize their search, as in A-S partition. A deliberately wrong model may therefore
improve an endpoint by changing where an agent searches or by increasing useful experimental
diversity. Endpoint improvement measures the utility of an induced trajectory, not the truth of the
agent's scientific model.

## 8.2 Bias rejection must be behaviorally selective

The broad tendency to distrust any explicit model illustrates a second ambiguity. Generic skepticism
can generate the right verbal stance without identifying the wrong prior: final misindex suspicion was
slightly more common in aligned than misindexed cells. A valid correction measure must be selective:
contradictory evidence should improve wrong-prior predictions more than correct-prior predictions, and
that improvement should influence subsequent experimental choices. The registered evaluator now shows
that this condition was not satisfied at any intervention locus, despite general prediction-error
reduction. A-P provides a directional hypothesis for replication, but its $p=0.079$ result cannot be
treated as a passed locus.

## 8.3 Scientific understanding as a chain with measurable conversion losses

Prediction, explanation and action can dissociate. An agent may understand a relation but lack the
operational competence or remaining resources to exploit it; it may act successfully without an
accurate model; or it may state the right model while continuing to choose inconsistent experiments.
Here, this dissociation is observed directly: explicit predictions generally improved, executable
laws were worse than final predictions in 85/135 cells, and blind actions were equivalent to the
incumbent in 119/121 evaluable cells. The platform therefore turns an abstract capability hierarchy
into measurable transition losses. Future interventions can target evidence seeking, updating,
compression or action separately instead of optimizing one composite score.

## 8.4 The harness is part of the evaluated agent system

A persistent Codex session contributes capabilities that a stateless model call does not: it retains
the campaign history, chooses among tools after each observation and can revise a plan without a host
reconstructing its reasoning state. The same harness also introduces failure surfaces through tool
discovery, schema conformance, retry rules, context growth and checkpoint submission. Provider-side
caching changes resource use but not the number of experiments or independent worlds. Consequently,
the participant is the frozen combination of model, reasoning setting, prompt, Codex runtime, MCP
interface and resource policy—not the model weights in isolation. This boundary is visible in the
current cohort: 888 of 904 failed tool events occurred during typed belief submission even though all
675 checkpoints were ultimately recovered. A cross-model claim requires these components to be
matched or explicitly manipulated; the present provider configurations are therefore reported
separately.

## 8.5 Scope and limitations

The study evaluates bounded executable chemical worlds rather than universal chemical fidelity or
direct wet-laboratory validity. A single frozen DeepSeek--Codex participant method supports conclusions
about that agent-system configuration, not language models in general. The public programme contains
nine task--locus combinations but only five independent worlds per task, so small and heterogeneous
effects cannot support broad equivalence or universal-benefit claims. A-E, A-P and A-S reached terminal
participant denominators, whereas the observation-model screen remained a scientific boundary and did
not enter a participant block. The current-composite evaluator completed held-out prediction, law
compression and blind action for the public cohort; private confirmation, matched cross-provider
replication and compositional transfer were not run.
The matched-evidence A-S B2 follow-up contains only five independent public worlds; its exact
sign-flip analysis and public-summary structural audit cannot establish a population-wide rate of
mechanism recovery. The original A-S Study B branch is retained only as historical platform-defect
evidence and is excluded from current scientific claims.
Ten cells contain discard-affected checkpoint timing that cannot be retrospectively repaired. Finally,
exact software replay does not eliminate provider variability or interface burden; provider attempts,
schema failures, resource rejection and session outcomes are reported as operational characteristics
rather than independent scientific samples.

# 9. Methods

## 9.1 World and initial-model construction

Each task instantiates an executable $W=(\mathcal{E},G,\Theta,O,C)$ and a participant-facing
$M_0=(\widehat{\mathcal{E}},\widehat{G},\widehat{\Theta},\widehat{O},\widehat{S})$. Public formal
worlds are selected deterministically from a namespace disjoint from development worlds. Within each
world cluster, all arms share $W$, the resource card and stochastic identity; exactly one declared
component of $M_0$ changes. In A-E, aligned and misindexed dossiers contain identical fields, values,
wording and confidence language, while the latter applies a frozen permutation to material
identifiers. Structural, parametric and observation-model extensions alter only their declared
agent-facing representation while retaining the external world and contract. A layer extension is
admitted only after a separate identifiability audit confirms that aligned and misspecified encodings
are matched in information volume, wording, confidence, baseline plausibility and falsification cost.

## 9.2 Transactional execution and resources

Every operation enters schema validation and resource preflight before candidate execution.
Committed operations update physical state and the campaign ledger; invalid or resource-rejected
attempts retain their declared reporting debit without entering committed physical state. Task-specific
resource cards bound vessel starts, assays, measurements, stocks, process time, repeated operations,
quench and transfer time, and closeout reserve across all experiments in a campaign.

## 9.3 Persistent Codex/MCP execution

Each participant cell launches one Codex Responses process and retains one provider session across the
complete pattern-owned campaign. Web search is disabled. The participant instructions prohibit shell use,
file changes and repository inspection and require physical decisions to pass through the host-owned
`chemworld_lab` STDIO MCP server. The bounded domain tools expose material information, belief
checkpoints, operation submission, public status and history, artifact inspection and final
recommendation commitment. The host validates and executes submitted actions but never chooses a
fallback scientific action.

Every operation submission contains a bounded decision audit stating its expected effect, diagnostic
target and evidence dependence. Tool receipts retain call order, status, timestamps, error classes and
argument/result hashes without retaining raw provider payloads or private chain-of-thought. A provider
retry or infrastructure resume is an operational attempt within the same cell, not a new experiment or
independent sample. Belief checkpoints are MCP calls inside the existing session rather than separate
provider conversations.

## 9.4 Belief and law-summary checkpoints

Checkpoint records contain prior assessment, predictions, uncertainty, evidence references, an
executable law summary, next-experiment intent and overall confidence. The schema permits bounded
rationales but not an unconstrained persistent notebook. After the campaign, explicit predictions
and the final law summary are evaluated against sealed truth packs. The summary must execute for the
exact registered query-metric set; the analysis records its normalized error, pre-to-summary
improvement, error relative to the effective final checkpoint and prediction-consistency error.
These quantities are reported continuously. They are not converted post hoc into a public binary
law-discovery label, and a reusable or transferable-law claim additionally requires independent
transfer evidence.

## 9.5 Statistical analysis

The public C2 cohort contains 45 independent matched task--world clusters: 25 in A-E, ten in A-P and
ten in A-S. Every cluster contains three participant arms, which are paired interventions rather than
independent samples. Prediction-to-law inference is performed separately by locus. A-E retains its
three-component failure-aware intersection--union gate; A-P and A-S use task-fixed-effect contrasts,
require both task means to be positive and retain adverse bounds for failed or unscorable arms. A
global cross-locus decision requires all three locus gates to pass, and naive pooling across the nine
task--locus combinations is forbidden. Endpoint contrasts in Section 6 are descriptive trajectory
outcomes, not substitutes for that registered prediction-error analysis. Prespecified sensitivity
analyses include observed-point, complete-case, heteroscedasticity-robust and task-stratified
cluster-bootstrap summaries.

Matched-evidence analyses use the world as the inference unit and retain the prespecified contrast
$(E_{mis,pre}-E_{mis,post})-(E_{aligned,pre}-E_{aligned,post})$. A-S B2 uses five worlds, so all
$2^5$ sign flips are enumerated for the exact one-sided directional check and a Student-$t$ interval
is reported descriptively. Canary sessions are excluded. Public structural-recovery counts use only
the submitted model summary and evidence assessment, never private reasoning text.

## 9.6 Optional private confirmation boundary

No private participant cohort was executed for the present study. If private confirmation is pursued,
it will use newly sealed world identities disjoint from development and public worlds, retain the same
three-arm participant and evaluator contracts, and preserve every completed, failed and unstarted
cell in a one-shot denominator. Such a cohort would test within-family replication. A separate
context-reset artifact-transfer design would still be required for a compositional-transfer claim.

## 9.7 Reproducibility and failure accounting

Participant trajectories, evaluator truth packs and blind-replay packs are stored separately and
joined through immutable receipts. Every terminal participant trajectory must pass physical replay,
campaign-resource replay and hidden-boundary audit. Provider process attempts, provider sessions,
tool calls, operation attempts, committed operations, complete experiments, cells and evaluator
executions are reported with distinct denominators.

# 10. Data and code availability

The executable environment, frozen protocols, analysis code, source data and reproducible figure
scripts will accompany the public release. Raw provider payloads and credentials are excluded. No
private cohort data are included because that optional study was not executed.

# 11. Author contributions

Jiangjie Qiu, Yijun Li and Yaotian Yang contributed equally. A role-based contribution statement for
all six authors will be finalized before submission without changing the author order or
corresponding-author designation.

# 12. Competing interests

The authors declare no competing interests.
