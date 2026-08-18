---
title: "Dissecting Executable Scientific Intelligence with Controlled World-Model Interventions"
title_line_one: "Dissecting Executable Scientific Intelligence"
title_line_two: "with Controlled World-Model Interventions"
subject: "Causal dissection of experimental search, predictive correction, executable laws and action transfer in AI agents"
keywords: "AI scientist; autonomous experimentation; initial world model; scientific priors; law discovery; counterfactual prediction; action transfer; chemical worlds"
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
  favorable heuristic trajectory. We organized a completed three-part programme around three
  questions: do priors change search and endpoints; does evidence selectively repair wrong priors
  and yield executable regularities; and can learned information support an unseen action? In a
  prospective cohort of 135 sessions and 1,243/1,260 planned experiments, prior effects were
  strongly task dependent. Correct entity information produced a durable advantage in partition,
  whereas correct structural information gave crystallization an initial head start that narrowed
  during exploration. Structural partition showed that explicit organization and correctness can
  contribute separately. Prediction error generally decreased, but selective correction failed at
  the entity ($p=0.990$), parametric ($p=0.079$) and structural ($p=1.000$) loci. In matched-evidence
  studies, the structural prediction-update contrast was positive but mixed (+0.0645; 3/5 worlds),
  while 0/5 summaries recovered the prespecified power law. Executable laws were better than final
  explicit predictions in only 50/135 cells and worse in 84/135. A formal multi-task open-action
  assay completed 45/45 scheduled cell records and 240/240 truth plus exact-replay queries; among
  42 eligible cells, 11 selected the true top-ranked plan, with 0/42 combining an adequate law and
  a correct action. These results separate evidence acquisition, numerical revision, structural-law
  identification, law compression and unseen-action selection. Private replication and context-reset
  artifact portability are future studies, not results of the present paper.
---

# 1. Introduction

Scientific discovery is not simply the production of a high-scoring outcome. A useful result can arise
from a correct initial model, a productive but incorrect heuristic, evidence-driven revision or a
fortunate endpoint without a reusable account of the relation that generated it. These explanations
are scientifically distinct even when the final score is identical. The object of study is therefore
the agent's initial model of what exists, how it works, which quantities matter and where a learned
relation should apply.

AI systems can now plan experiments, call chemistry tools and participate in closed-loop discovery
workflows [@boiko2023autonomous; @bran2024augmenting; @szymanski2023alab; @darvish2025organa;
@song2025chemagents; @vriza2026instruments]. Interactive scientific environments likewise test
hypothesis formation, intervention and inference [@jansen2024discoveryworld; @gandhi2025boxinggym;
@duan2025scigym; @zheng2026newtonbench; @yang2026causalab; @batzoglou2026replayscm]. Yet endpoint
optimization, belief statements, evidence selection, law recovery and action transfer are usually
entangled.

Executable chemical worlds provide a controlled instrument for separating these transitions. Entities,
process structure, parameters, measurement mappings and private laws can be instantiated while the
public task, operations, resource opportunities and external world remain fixed [@qiu2026chemworld].
The present study uses that programmability to intervene on one layer of an initial world model at a
time and to score the resulting transitions. The platform qualification is not treated as evidence
about agent intelligence.

The paper is organized around three questions.

1. **Do priors change search and endpoints?** We compare opaque, aligned and misspecified initial
   models within matched task--world clusters and measure both the first action and the best outcome.
2. **Does evidence selectively repair wrong priors and yield executable regularities?** We score
   held-out predictions, matched-evidence updates and executable law summaries separately from
   self-reported confidence.
3. **Can learned information support an unseen action?** We distinguish replay of an observed
   incumbent from ranking fully specified candidate plans whose outcomes were hidden during learning.

The completed evidence comprises a prospective cohort, a valid matched-evidence follow-up and a
formal open-action assay. Early exploratory cohorts, a one-world parametric pilot, an incomplete
prototype, repair trajectories and operational accounting are retained in the Supplementary
Information. Private replication and context-reset artifact portability are future studies.

```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/prior-discovery/figure-1-prior-to-law.pdf}
\caption{\textbf{The capability chain tested in this paper.} \textbf{a,} A fixed executable world is paired with opaque, aligned or misspecified information at one declared layer. \textbf{b,} A persistent agent selects experiments, observes outcomes and updates predictions and a law summary. \textbf{c,} Participant trajectories and evaluator-owned held-out truth remain separate until scoring. \textbf{d,} Search, prediction, law recovery and unseen-action selection are distinct outcomes; context-reset portability is a future test.}
\label{fig:capability-chain}
\end{figure*}
```

# 2. Related work

Autonomous chemistry systems demonstrate planning, synthesis, materials search and closed-loop
experimentation on real equipment [@boiko2023autonomous; @bran2024augmenting; @szymanski2023alab;
@darvish2025organa; @song2025chemagents]. Virtual laboratories and process environments make
experimentation repeatable and inexpensive [@felton2021summit; @hase2021olympus; @bloor2024pcgym;
@beeler2024chemgymrl; @malik2026made]. Interactive discovery benchmarks emphasize repeated cycles
of hypothesis, intervention and inference [@jansen2024discoveryworld; @gandhi2025boxinggym;
@duan2025scigym; @nagele2026sciexplorer].

Prior-availability studies and counterfactual-world benchmarks make important contributions, but they
often change task information without separating correctness, evidence acquisition and transfer.
Mechanism-oriented systems instead optimize model discovery or experiment selection
[@kabra2026llmautoscilab; @murphy2026mda; @wahl2026probabilistic]. Our design is complementary: the
external world and action space are fixed within matched clusters, while one declared component of
the initial scientific model changes. The resulting estimand is a conversion loss along a capability
chain, not a leaderboard score.

# 3. Conceptual framework

Each matched comparison contains one evaluator-owned world
$W=(\mathcal{E},G,\Theta,O,C)$ and one participant-facing initial model
$M_0=(\widehat{\mathcal{E}},\widehat{G},\widehat{\Theta},\widehat{O},\widehat{S})$. The public task,
action space, observation channels, resource card, safety rules and stochastic identity are fixed.
Only one declared component of $M_0$ changes. The manipulated layer can be entity/ontology,
parametric/dynamical or structural/mechanistic; observation and scope are reserved for separate
boundary studies.

Within a layer, information is either opaque, aligned with the fixed world or equally detailed but
misspecified. A misspecified model is a plausible scientific representation, not a trick question
about obedience. Experimental evidence remains authoritative in all conditions.

We distinguish five outcomes:

1. endpoint optimization;
2. predictive recovery on held-out counterfactual queries;
3. selective correction of a wrong prior;
4. recovery of an executable law that preserves conditional prediction quality; and
5. action transfer to a previously unseen, fully specified plan.

The analysis reports transition losses rather than a composite intelligence score. Endpoint success
without predictive and transfer validity is classified as local optimization rather than law discovery.

# 4. Completed study architecture

The prospective cohort spans five task families with five public worlds per task for the entity layer,
and two validated task families with five worlds per task for the parametric and structural layers.
Every matched cluster contains opaque, aligned and misspecified arms. Exploratory and prospective
world instances are disjoint. Observation-model interventions and scope/compositional studies are
kept outside the current denominator.

The completed programme has three evidence blocks:

1. **Prospective search cohort.** Campaigns contain eight, ten or twelve experiments depending on
   the intervention layer, with checkpoints fixed before execution. Each checkpoint records
   predictions, uncertainty, evidence references, a typed law summary and the next experimental
   intent.
2. **Matched-evidence follow-up.** The same contradictory evidence is presented to each arm after
   the initial search. The valid analysis combines an unaffected parametric block and a corrected
   structural phase-process block; a superseded run is retained only in the Supplementary
   Information because its evaluator omitted the declared intervention.
3. **Formal open-action assay.** After twelve experiments, the agent ranks eight fully specified
   candidate plans with outcomes hidden. Public, truth-evaluated and executed plans are verified as
   identical. This assay addresses unseen-action transfer rather than replay of an observed incumbent.

```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/prior-discovery/figure-2-formal-cohort.pdf}
\caption{\textbf{Completed evidence architecture.} \textbf{a,} The entity backbone contains five task families and five public worlds per task. \textbf{b,} Each matched task--world cluster contains opaque, aligned and misspecified initial models for one declared locus. \textbf{c,} Parametric and structural blocks are validated separately. \textbf{d,} Prospective search, matched evidence, evaluator scoring and open-action tests retain separate sessions and denominators; private replication and context-reset portability are future work.}
\label{fig:study-architecture}
\end{figure*}
```

# 5. Results I — Priors change search and endpoints

The prospective cohort completed **135/135** scheduled sessions and **1,243/1,260** planned
experiments. The denominator contains 1,269 closed batch lifecycles, 1,243 final assays and 26
discarded lifecycles. Failed cells and uncommitted attempts remain in their assigned denominators.

Prior effects were task dependent. In entity-level partition, aligned information improved the first
experiment by **0.106** and the best observed endpoint by **0.200** relative to misspecified
information, with the same direction in **5/5** worlds. In structural crystallization, aligned
information improved the first experiment by **0.141** in **5/5** worlds, but the best-endpoint gap
narrowed to **0.055** and was positive in only **3/5** worlds. Structural partition separated
organization from correctness: aligned and misspecified models exceeded opaque identifiers by
**0.163** and **0.143**, respectively, while their mutual difference was only **0.020**.

The remaining task--locus combinations bounded these cases. Entity-level reaction safety showed a
small aligned-minus-misspecified difference of **0.036** at the best endpoint, distillation narrowed
from **0.053** on the first experiment to **0.011** at the best endpoint, and electrochemical and
crystallization effects were heterogeneous. Correct information was therefore neither a universal
performance intervention nor a necessary condition for useful search.

The agents did perform substantive within-session search. **91.2%** of completed experiments used a
unique recipe, **84.4%** of session optima occurred after the campaign midpoint and **32.6%** occurred
in the final completed experiment. These observations support search adaptation, not scientific
correction: a productive trajectory can arise while the initial model remains wrong.

# 6. Results II — Evidence, selective correction and executable laws

All sessions submitted five belief checkpoints, yielding **675/675** typed records and **6,300**
prespecified counterfactual predictions. The evaluator completed **420/420** truth executions and
scored every checkpoint. Prediction error generally decreased, but the registered selective-correction
criterion failed at all three loci: entity **$p=0.990$**, parametric **$p=0.079$** and structural
**$p=1.000$**. General prediction improvement and targeted repair of an incorrect prior were therefore
not interchangeable outcomes.

Matched evidence localized the loss without reducing it to a binary label. In the parametric block,
all five misspecified summaries rejected the supplied high-potential direction after receiving the
same contradictory evidence. In the structural block, the misspecified-minus-aligned prediction-update
contrast was **+0.0645**, positive in **3/5** worlds (exact one-sided sign-flip **$p=0.125$**), while
**0/5** misspecified summaries recovered the prespecified power law. Evidence acquisition, numerical
revision and structural-law identification therefore remain separable transitions.

The evaluator executed all **135/135** final typed laws. Laws were more accurate than final explicit
predictions in **50/135** cells, equal in one and worse in **84/135**; mean law-minus-final error was
**+0.069**. Syntax and execution were reliable, but compression into a reusable relation was often
lossy. Blind replay of the committed recommendation versus the observed incumbent was better,
equivalent and worse in **1/119/1** of **121** evaluable cells. Reproducibility of an observed action
was therefore almost complete, while improvement beyond the observed history was rare.

```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/prior-discovery/figure-3-capability-chain.pdf}
\caption{\textbf{Prediction, law and action dissociation.} Held-out prediction error, selective-correction contrasts, executable-law error and blind incumbent replay are separate readouts. The completed cohort shows broad prediction improvement but no passed selective-correction gate, frequent lossy law compression and almost no recommendation gain over the observed incumbent.}
\label{fig:prediction-law-action}
\end{figure*}
```

# 7. Results III — Learned information and unseen action

The formal open-action assay completed **45/45** scheduled cell records. Independent evaluation
completed **240/240** truth executions and **240/240** exact replays, and verified identity among the
public, truth-evaluated and executed action plans. **42/45** cells were eligible for action metrics;
three crystallization failures remain in the scheduled denominator.

Among eligible cells, **11/42** selected the true Top-1 plan, with mean selected rank **3.31/8** and
mean normalized regret **0.297**. The joint mechanism--action outcome was more informative than Top-1
alone: **30/42** cells had an inadequate law and a wrong action, **11/42** had an inadequate law but a
correct action, **1/42** had an adequate law but a wrong action and **0/42** combined an adequate law
with a correct action. Law adequacy was therefore not sufficient for action correctness, while a
correct action could occasionally occur without an adequate law.

Task heterogeneity was substantial. Electrochemical conversion reached Top-1 in **4/15** cells,
reaction safety in **4/15** and crystallization in **3/12** eligible cells. The assay is descriptive:
only twelve task--world clusters retain complete three-arm comparisons, and failures are concentrated
in crystallization. The bounded conclusion is a transfer boundary, not an arm-level effect.

```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/prior-discovery/figure-6-open-action-formal.pdf}
\caption{\textbf{Unseen-action selection after exploration.} Selected rank, normalized regret, joint law--action categories and task-level means are shown for the 42 eligible cells. The three crystallization failures remain in the scheduled denominator. Every candidate plan was fully specified and executed exactly as disclosed; candidate outcomes and ranks were hidden until the terminal readout.}
\label{fig:open-action}
\end{figure*}
```

# 8. Discussion

The completed evidence supports three bounded conclusions. First, priors change search and endpoints,
but their effects are context dependent: a correct model can provide a durable advantage, an early
head start or no stable benefit, and a wrong model can still guide productive exploration. Second,
prediction improvement does not establish selective correction. Matched evidence can trigger evidence
acquisition and numerical revision without reliable structural-law identification, and executable
summaries can lose information relative to the agent's conditional predictions. Third, even a complete
action interface does not guarantee transfer to an unseen candidate set: only 11/42 eligible readouts
selected the true Top-1 plan, and no cell combined an adequate law with a correct action.

These results argue against a single endpoint score for scientific intelligence. Evidence acquisition,
belief revision, law identification, law compression and action transfer should be measured as separate
transitions. The correct interpretation is a map of conversion losses in one controlled agent-system
configuration, not a claim about all models or all chemical settings.

## 8.1 Scope and limitations

The study uses bounded executable chemical worlds rather than universal chemical fidelity or direct
wet-laboratory validation. Five independent worlds per task limit precision for small or heterogeneous
effects. The observation-model intervention and scope/compositionality intervention were not executed.
The matched-evidence structural block contains five worlds, so its sign-flip result is descriptive.
The open-action assay contains 42 eligible cells, three retained crystallization failures and twelve
complete three-arm clusters; its arm summaries are not causal estimates. Exact replay verifies the
declared computational world and plan semantics but does not remove all interface or execution burden.

# 9. Methods

## 9.1 World and initial-model construction

Each task instantiates an executable world and a participant-facing initial model. Within a matched
cluster, all arms share the world, resource card, public contract and stochastic identity; exactly one
declared component of the initial model changes. Entity, parametric and structural encodings are
included only after separate identifiability checks confirm comparable information volume, wording,
confidence and falsification cost.

## 9.2 Campaigns, checkpoints and evaluator scoring

Campaign lengths and checkpoint positions were fixed before execution. A checkpoint records prior
assessment, predictions, uncertainty, evidence references, an executable law summary and next-experiment
intent. The evaluator owns the held-out truth queries and does not return them to the participant.
Prediction error is the mean normalized absolute error across prespecified query--metric pairs. Final
laws are executed on the same coordinates, and blind replay compares the committed recommendation with
the observed incumbent using separate evaluator resources.

## 9.3 Matched evidence and selective-correction estimand

For locus $\ell$, the primary contrast is

```{=latex}
\[
 C_{\ell}=(E_{\mathrm{mis,pre}}-E_{\mathrm{mis,final}})-
          (E_{\mathrm{aligned,pre}}-E_{\mathrm{aligned,final}}).
\]
```

The selective-correction gate requires improvement in the misspecified arm, no unacceptable
degradation in the aligned arm and a lower confidence bound above zero. Loci are reported separately;
unlike endpoint contrasts are not pooled as one universal prior effect. Failed scientific cells remain
in the denominator and are not replaced.

## 9.4 Open-action construction and analysis

An outcome-blind generator constructed eight complete candidate action plans per world before
participant execution. Each plan disclosed its full operation sequence, parameters, initial-state
assumptions, measurements and terminal assay. After twelve experiments and the final checkpoint, the
participant returned a complete ranking and one selected plan. The evaluator then calculated selected
rank, Top-1, regret and the joint law--action category. All scheduled cells remained in the denominator.

# 10. Completed studies and future programme

The following boundary is part of the paper's interpretation.

- **Completed — prospective cohort:** priors change search and endpoints; selective correction is not
  established.
- **Completed — matched-evidence follow-up:** evidence acquisition and numerical revision can occur
  without exact structural-law recovery.
- **Completed — formal open-action assay:** unseen-action transfer is limited and task dependent.
- **Supplementary — exploratory cohorts and pilot:** developmental context, not pooled into the main
  denominators.
- **Supplementary — incomplete prototype, repair trajectory and excluded outputs:** diagnostic history;
  never used to replace a scheduled cell.
- **Future — private within-family replication:** tests stability on newly sealed worlds.
- **Future — context-reset artifact portability:** tests whether learned artifacts transfer to a new
  target context.

The future studies require new protocols and independent denominators. They are not implied by the
current endpoint results and are not described as completed evidence.

# 11. Data and code availability

The executable environment, prespecified protocols, analysis code, source data and reproducible figure
scripts accompany the public release. Raw model payloads, credentials and private world instances are
excluded. Future private and context-reset studies will use newly sealed instances and will not alter
the present denominators.

# 12. Competing interests

The authors declare no competing interests.

# Supplementary Information

## S1. Early exploratory cohorts

Before the prospective cohort, exploratory configurations were used to test whether explicit priors
altered endpoint behavior and whether the evaluator could score prediction, law and blind replay
without changing the participant trajectory. These cohorts reached 44/45 and 75/75 terminal cell
records in their respective configurations, but their task mix, recovery rules and campaign lengths
were not identical to the prospective design. They are therefore descriptive context only. Across
the common endpoint panels, explicit information sometimes improved outcomes over opaque identifiers,
while misspecified information was not consistently harmful. Held-out prediction error often fell,
but the wrong-prior improvement was not selectively larger and blind replay rarely exceeded the
observed incumbent.

## S2. One-world parametric pilot

A preliminary one-world parametric pilot retained one opaque, one aligned and one misspecified cell.
All 3/3 cells, 12/12 experiments, 12/12 checkpoints, 4/4 shared truth queries and 18/18 blind
replays completed with exact replay. The misspecified agent moved outside its supplied parameter
window after contradictory evidence and reduced its stated reliability, yet its best endpoint remained
below the aligned and opaque cells. The pilot demonstrates that model rejection and finite-budget
policy recovery are distinct; it is not a cross-task claim.

## S3. Incomplete prototype and repair trajectory

An earlier open-action prototype retained 11/15 complete cells and did not produce a Top-1 selection.
It is not combined with the formal assay. A separate repair trajectory completed a previously
interrupted crystallization cell but included a resource rejection and selected rank 8/8. The repair
is a sensitivity result, not a replacement cell.

## S4. Operational diagnostics and excluded outputs

The development records contain schema failures, rejected operations, recovery events, resource
rejections, timing summaries and other interface diagnostics. These quantities describe the complete
agent system and are not independent scientific samples. Implementation counters, run identifiers,
cell identifiers and raw or replaced outputs are intentionally omitted from the reader-facing paper.
Historical outputs remain archived for auditability but cannot alter a completed denominator.

## S5. Future studies

Private replication will use newly sealed worlds with the same three-arm contract and one-shot
denominators. Context-reset portability will compare raw evidence, structured evidence bundles and
typed executable laws in a new target context. Both studies require independent preregistration and
will be reported separately from the present paper.
