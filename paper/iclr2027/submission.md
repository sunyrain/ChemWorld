---
title: "When Does Experimental Knowledge Improve Scientific Decisions?"
subject: "Experimental knowledge, executable artifacts and decision quality in scientific agents"
keywords: "scientific agents; experimental knowledge; decision quality; executable laws; controlled evaluation"
abstract: |
  Autonomous scientific agents may improve predictions without producing knowledge that reliably
  guides new decisions. We study this distinction in ChemWorld through controlled initial
  descriptions, executable knowledge artifacts and complete action plans. Two model configurations
  each entered 135 scheduled campaigns across 45 matched task--world clusters. Prediction errors
  decreased on average, but the registered selective-correction criteria were not met, and
  executable summaries retained different amounts of predictive information. In a separate
  DeepSeek cohort, submitted laws selected the optimum in 0/45 scheduled unseen-plan cases,
  compared with 11/45 participant choices. We then held public evidence fixed in a factorial
  intervention across ten new worlds, crossing model-generated or numerically fitted quadratic
  laws with fresh-agent or deterministic selection. All 160 condition slots completed. Under the
  same maximizer, fitting changed mean regret by -0.00538 (95% interval [-0.01630, 0.00061]),
  failing the prespecified material-benefit criterion. Fresh agents and the maximizer made
  identical choices in all 40 fitted-law pairs, while a nearest-evidence baseline had similarly
  low regret. These results limit a general inability-to-use-laws account: historical law/action
  disagreement coexists with high agreement on a simpler fixed-evidence surface. They establish
  bounded diagnostic findings, without isolating the cause of differences between protocols or
  demonstrating a general repair method or transfer to new physical conditions.


---

# Introduction

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
Together, the studies locate observed gaps and provide a boundary to a universal law-use failure
account. Different protocols are not randomized against each other; neither their contrast nor
the factorial intervention identifies internal psychological mediation.


```{=latex}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/prior-discovery/figure-1-prior-to-law.pdf}
\caption{\textbf{Endpoint success does not reveal what the agent learned.}
ChemWorld varies the supplied initial description while fixing the executable world, public rules,
and budget. Held-out predictions, executable knowledge, and unseen-plan decisions are separate
readouts. The diagram describes the design; its arrows do not identify internal belief or causal
mediation through submitted knowledge.}
\label{fig:capability-chain}
\end{figure}
```

# Environment and evaluation

## ChemWorld as a controlled causal probe

ChemWorld separates three objects. The executable world contains hidden state, transition and
measurement laws, resources, and terminal assays. The public task exposes typed operations,
instruments, observations, and an initial model. The evaluator owns held-out truth, replay, and
scoring. For world $w$ and initial-model arm $a$, the hidden transition process remains fixed while
the supplied model $M_{0,a}$ changes. The aligned model is correct at one declared locus, the
misspecified model is explicit but wrong at that locus, and the opaque arm withholds the corresponding
structure. The design changes participant-facing information while holding world physics and the
available operation and measurement semantics fixed.

Actions are transactions, not free-form prose. The host validates a typed request, checks resources
and preconditions, commits the state transition, and returns a public observation or a structured
rejection. Failed actions and discards remain in the trajectory. Every submitted action, commit,
rollback, measurement, assay, and resource delta is recorded for exact replay. These semantics matter:
an action recommendation is scientific evidence only when the evaluator can execute the same complete
plan without filling in hidden workflow choices.

## Observable outcomes and measurement limits

We distinguish five downstream outcomes. **Evidence acquisition** asks which informative experiments
are selected and observed. **Numerical revision** asks whether held-out counterfactual prediction error
falls. **Structural identification** asks whether the agent rejects a false form and recovers the
registered relation. **Executable compression** asks whether a typed law preserves the information in
conditional predictions. **Decision transfer** asks whether the final state selects a good previously
unseen plan. A sixth requirement, **evaluator validity**, asks whether the control and metric actually
measure the decision estimand. Success at one stage is neither defined as nor assumed to imply success
at the next.

At five checkpoints per session, the participant reports initial-model reliability, predictions,
uncertainty, evidence references, an executable law, and the next experimental intent. The evaluator
executes prespecified counterfactual query sets independently of the participant. The DeepSeek-v4-flash
surface scores 675/675 checkpoints from 420/420 truth executions; the GPT-5.6-sol surface scores
669/675 checkpoints from its own 420/420 truth executions. The evaluator later runs each available
final typed law on the same coordinates.
Paired blind replay evaluates the final recommendation against the observed incumbent, while a
separate longitudinal assay reveals eight outcome-hidden complete ActionPlans only after autonomous
exploration has ended.

# Experimental programme

The primary DeepSeek cohort comprises 135 separate sessions nested within 45 independent task--world clusters.
The registered improvement contrast depends on initial error headroom; a failed gate does not
establish an absence of correction ability. Initial predictions and contradicted relations provide
its manipulation-check context.


The prospective programme is layer-stratified. Entity interventions cover five task families and five
independently selected public worlds per task. Parametric and structural blocks each cover two
validated task families and five worlds. Every task--world cluster contains opaque, aligned, and
misspecified arms, yielding 135 separate sessions nested within 45 independent task--world clusters.
Campaign length is
locus-specific: eight, ten, or twelve complete experiments, with five checkpoints in every session.
Exploratory, validation, prospective, matched-evidence, and open-action worlds remain separated.
We abbreviate the prospective cohort as C2, the matched partition-packet diagnostic as B2, its
typed-law/action control as B3, and the entity/parametric/structural loci as A-E/A-P/A-S.

The primary contrast tests selective evidence-driven correction. If
$E_{a,k}^{(\ell)}$ is held-out error for arm $a$, checkpoint $k$, and locus $\ell$, then

```{=latex}
\[
C_{\ell}=\left(E^{(\ell)}_{\mathrm{mis},0}-E^{(\ell)}_{\mathrm{mis},K}\right)
-\left(E^{(\ell)}_{\mathrm{aligned},0}-E^{(\ell)}_{\mathrm{aligned},K}\right).
\]
```

Success requires greater correction in the misspecified arm, improvement of that arm, and no
material deterioration of the aligned arm. Loci are decided separately; unlike intervention
semantics are not pooled. Failed cells stay in the scheduled denominator; confirmatory correction
gates use adverse bounds, while last-observation and zero-improvement imputations are sensitivities.
Only infrastructure failures without a persisted trajectory can resume under a fixed attempt cap.

Matched-evidence sessions use cloned worlds and give every arm the same counterevidence after a
pre-response. They reveal conditional post-packet updating but, without a turn-matched no-packet
control, do not identify a pure evidence-packet effect. The longitudinal
action matrix separately contains three tasks, five worlds, and three arms (45 scheduled cells). After
12 autonomous experiments, each agent ranks eight new plans; regret and Top-1 are primary action
readouts, while complete-rank correlation and law adequacy are diagnostics. Table~\ref{tab:evidence}
keeps these layers and their claim boundaries explicit.

Provenance is block-specific: C2 and B3 have matched scheduled DeepSeek-v4-flash-high and
GPT-5.6-sol-medium surfaces;
matched evidence adds complete denominators and a DeepSeek-low B2 reasoning-budget ablation; the
four-condition successor retains model-specific donor eligibility. Historical controls and model configurations retain separate denominators. The new factorial
block instead prespecifies an equal-weight mean over models and repeats within world.

```{=latex}
\begin{table}[t]
\caption{\textbf{Executed evidence layers and claim boundaries.} A completed work package may contain
a retained scientific rejection; unstarted units are not silently removed.}
\label{tab:evidence}
\centering
\scriptsize
\begin{tabularx}{\linewidth}{@{}lrrY@{}}
\toprule
Layer & Units & Execution & Supported role \\
\midrule
Prospective C2 & 270 scheduled & DeepSeek 121 complete; GPT 126 complete & Search, prediction, law, incumbent replay \\
Matched evidence & 75 sessions & DeepSeek high + GPT medium (60); DeepSeek low (15) & Conditional numerical--exact-law-expression dissociation \\
Identifiable-law B3 & 60 scheduled & DeepSeek 17+13 failures; GPT 30 & Structural recovery and action bridge \\
Action assays & 45 cells + 360 slots & Open action + four conditions/model & Descriptive and failure-aware action transfer \\
Factorial intervention & 160 slots; 10 worlds & 120/120 sessions; 200/200 physics/replays & Fixed-evidence law and decision-rule replacement \\
Evaluator controls & 16 unit versions & Provider-free; original stops retained & Rank validity versus action validity \\
\bottomrule
\end{tabularx}
\end{table}
```

# Results: from priors to laws

## Prior-conditioned search and unmet correction criteria

All 135 scheduled sessions produced final records. Participants completed 1,243/1,260 planned
experiments; 121 sessions met operational eligibility. The denominator retains 26 discarded
lifecycles, 13 resource-ledger rejections, and all right-censored cells. Every session submitted five
checkpoints, providing 6,300 counterfactual predictions and 24,300 query--metric values.

Arm assignment was reflected in behavior. The first complete recipe differed between aligned and
misspecified cells in 45/45 matched clusters, between opaque and aligned in 45/45, and between opaque
and misspecified in 44/45. This is a manipulation check rather than a causal effect estimate because
there are no repeated same-arm sessions. Search continued after the first proposal: 91.2% of completed
experiments used a unique recipe, 84.4% of session optima appeared after the midpoint, and 32.6%
appeared in the last completed experiment.

Correct-prior utility was task dependent. In entity-level partition, the aligned arm showed a
+0.200 best-endpoint advantage over the misspecified arm in 5/5 worlds. In structural
crystallization, a +0.141 first-experiment head start narrowed to +0.055 as the disadvantaged arm
explored. In structural partition, aligned and misspecified descriptions both helped relative to
opaque identifiers while differing little from one another. The supplied-model arms therefore occupied
different search landscapes, without identifying a stochastic participant effect or imposing one endpoint ordering.

Prediction error nevertheless fell on average in every arm at every locus. Reductions for opaque,
aligned, and misspecified cells were 0.111/0.097/0.097 at the entity locus,
0.090/0.033/0.065 at the parametric locus, and 0.219/0.228/0.221 at the structural locus. The stricter
selective-correction contrasts were -0.214 for entity ($p=0.990$), +0.033 for parametric
($p=0.079$), and -0.224 for structural ($p=1.000$); none passed. General predictive learning did not
become preferential correction of a wrong starting model (Fig.~\ref{fig:prior-correction}).

```{=latex}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/prior-discovery/figure-3-prior-uptake-and-correction.pdf}
\caption{\textbf{Prediction improves, but the evidence does not establish selective repair of the wrong model.}
\textbf{a--c,} Mean pre-evidence and final errors by arm in entity, parametric, and structural
blocks; lines connect aggregate means, not individual trajectories or confidence bounds.
The registered selective-correction criteria are unmet (one-sided $p=0.990,0.079,1.000$), and
initial error limits improvement headroom. First recipes differ in 45/45 aligned--misindexed,
45/45 opaque--aligned, and 44/45 opaque--misindexed clusters; this retrospective check has no
repeated same-arm baseline.}
\label{fig:prior-correction}
\end{figure}
```

## Matched packets expose numerical--expression dissociation; B3 tests structure

Matched packets provide conditional evidence response, with the packet and extra response turn
bundled. In the parametric block, all five DeepSeek misspecified summaries rejected the supplied
high-potential direction. B2 produced low post-packet error but no exact wrong-arm law expression
(0/5 in each model and DeepSeek-low); its one-pair linear/power alias makes it an underidentifying
surface. These observations cannot establish internal structural-identification failure.

B3 instead uses reference-fitter-qualified multi-pair evidence. It retained 30 GPT completions and
17 DeepSeek completions plus 13 schema failures. Joint recovery was 5/30 versus 0/30, and scheduled
useful gain was 0/18 for both. The contrast is bounded by differential availability and the specified
function family. Full packet, reasoning-budget and B3 results, including every failure denominator,
appear in the appendix (Fig.~\ref{fig:matched-evidence}).

## Executable laws lose information from predictions

All 135 DeepSeek laws executed, but 84 lost information relative to final explicit predictions; mean
law MAE was 0.237 and compression loss 0.069. Legal full-basis controls reproduced 135/135 prediction
states at mean MAE $4.25\times10^{-13}$, localizing the gap to participant distillation rather than
typed-interface capacity. Blind incumbent replay completed 726 executions for 121 cells, with
recommendations better/equivalent/worse in 1/119/1.

The matched GPT-5.6-sol surface retained 126 completed, 3 failed, and 6 right-censored cells. All
locus gates again failed. GPT-5.6-sol versus DeepSeek-v4-flash law MAE was 0.1753 (129 laws) versus
0.2371 (135 laws), and compression loss was 0.0142 versus 0.0686; blind gain was -0.0001 (126 cells)
versus -0.0010 (121 cells). Lower observed
compression error therefore coexisted with near-zero blind gain (Fig.~\ref{fig:c2-cross-model}); this
matched cross-configuration comparison is descriptive, not a causal law-quality intervention.

```{=latex}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/prior-discovery/figure-5-capability-chain.pdf}
\caption{\textbf{Lower executable-law error coexists with near-zero incumbent gain.}
\textbf{a,} Hollow and filled points show final-prediction and executable-law MAE on the same
law-evaluable cells, grouped by locus and model; connecting lines show compression differences,
not uncertainty. The matched denominators are 135 DeepSeek and 129 GPT laws.
\textbf{b,} Better/equivalent/worse/unavailable incumbent-replay counts retain all 135 scheduled
cells per model; hatching marks unavailable readouts. These are descriptive configuration
contrasts and incumbent replays, not causal artifact effects or unseen-action benefits.}
\label{fig:c2-cross-model}
\end{figure}
```

# Results: law, action, and evaluation

## Executable-law error is not a sufficient proxy for unseen action selection

The longitudinal DeepSeek matrix produced records for 45/45 scheduled cells. Truth evaluation and exact replay
both completed 240/240 plan executions. Forty-two cells were uncontaminated and eligible for action
metrics; two agent-induced resource/process failures and one session interruption in crystallization
remain in the scheduled denominator.

Only 11/42 eligible terminal readouts selected the true Top-1 plan. Mean selected rank was 3.31 of 8
and mean normalized regret was 0.297. The uniform-random rank 4.5 is geometric context, not a
no-evidence control, so these outcomes describe post-campaign competence rather than a causal benefit
of exploration. Law and action also separated: 30 cells had an inadequate law and wrong action, 11
an inadequate law but correct action, one an adequate law but wrong action, and none an adequate law
and correct action. Task means ranged from rank 2.00 for reaction safety to 4.58 for crystallization,
and every pairwise arm contrast changed sign under some leave-one-cluster-out omission. We therefore
make no pooled arm-level claim (Fig.~\ref{fig:open-action}a).

This separation survives continuous and threshold-sensitive analysis. Pooled law MAE correlated
weakly with selected rank (Spearman $\rho=-0.073$, cluster-bootstrap 95% interval
$[-0.380,0.256]$) and normalized regret ($\rho=-0.133$, $[-0.452,0.217]$), while task-specific rank
associations reversed sign ($+0.524$, $-0.592$, and $-0.007$). Across law-MAE thresholds from 0.05
to 0.30, the adequate subset expanded from 1 to 34 cells but contained only 0 to 9 correct actions.
The four-way table is therefore not a single-cutoff artifact: law error does not stably predict
unseen-action quality across tasks. A decision-aligned reanalysis of this DeepSeek-v4-flash cohort
then executed the last-available law from every frozen cell on
the same eight frozen candidate plans. All 45 laws were evaluable, but their implied choices reached
the true Top-1 in 0/45 cells, versus 11/45 when failures were retained for participant action. Among
42 cells with an action ranking, participants followed the law-implied Top-1 in only 12. Three cells
without a terminal action ranking still retained an earlier executable law. Participant
regret was lower than law-implied regret on average (0.344 versus 0.438), although the direction
reversed in crystallization. Because neither law quality nor law following was randomized, this
decomposes truth-law error from action-module utilization descriptively rather than estimating a
causal law-to-action effect.

## Four-condition strategies expose autonomy and learned-law-only limits

An independent successor scheduled four conditions over all 45 strata per model (360 slots). The
all-scheduled failure-aware estimand retains donor, blocked-descendant and recipient failures.
Autonomous-minus-no-evidence regret was -0.0913 for DeepSeek-v4-flash (95%
task--world-cluster interval $[-0.2124,0.0388]$) and +0.1102 for GPT-5.6-sol
($[-0.0533,0.2794]$): directions differed and both intervals crossed zero. GPT's yoked- and
learned-law-minus-none estimates were +0.2165 and +0.2459; these include missing donors and system
failures, not pure evidence or artifact effects.

Autonomy also changed sign by task: DeepSeek -0.240/-0.406/+0.372 and GPT
+0.089/-0.219/+0.460 for electrochemistry/safety/crystallization. Four registered contrasts are
descriptive and unadjusted for multiplicity.

Donor-eligible autonomy contrasts (-0.1214/-0.1379; 42/26 strata) are post-treatment sensitivities;
equal-task values are -0.0879/-0.0259. Yoked completion was 10/42 and 24/26. The block established no
consistent autonomy or learned-law-only advantage (Fig.~\ref{fig:open-action}b,c).

## Evaluator-level ranking and decision quality are different estimands

A diagnostic of 16 frozen oracle-control versions found disagreement in both directions: a
complete-ranking gate could pass while Top-1 was wrong, or fail while regret was zero. These
provider-free controls identify a measurement distinction, not another participant failure.
The original stops, all unstarted sessions and detailed values remain in the appendix
(Table~\ref{tab:alignment}); regret and near-optimality directly address selected-action quality.

```{=latex}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/prior-discovery/figure-6-open-action-formal.pdf}
\caption{\textbf{Law quality and information strategies have distinct decision readouts.}
\textbf{a,} Law-implied versus participant regret in the 45-cell DeepSeek matrix; 42 observed
choices are dots and three missing rankings are crosses above the plotting range. The diagonal
marks equal regret. \textbf{b,} Failure-aware strategy means with valid/scheduled counts.
\textbf{c,} Paired strategy-minus-no-evidence differences with task-stratified world-cluster
bootstrap 95\% intervals, retaining all 45 strata per model. Both autonomous contrasts cross zero.
The strategy block is development evidence; yoked failures prevent a pure acquisition-effect
interpretation. Complete-ranking diagnostics remain in the appendix.}
\label{fig:open-action}
\end{figure}
```

# Results: fixed-evidence representation and decision interventions

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
general law-use failure, while leaving artifact-only portability and the causes of historical
protocol differences unresolved.

```{=latex}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/prior-discovery/figure-7-m1-replication.pdf}
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
\end{figure}
```

# Related work

Self-driving laboratories and chemistry agents emphasize closed-loop execution, tool use, or endpoint
optimization [@felton2021summit; @hase2021olympus; @boiko2023autonomous; @bran2024augmenting]. Virtual
laboratories and process-control environments provide scalable interaction and safety
[@beeler2024chemgymrl; @bloor2024pcgym; @malik2026made; @chen2025physgym]. Scientific-discovery
benchmarks increasingly test iterative experimentation, causal inference, and transferable knowledge
[@jansen2024discoveryworld; @gandhi2025boxinggym; @duan2025scigym; @yang2026causalab;
@batzoglou2026replayscm]. The published ChemWorld platform contributes programmable chemical worlds,
transaction semantics and replay [@qiu2026chemworld]; this work contributes the intervention and
measurement programme for scientific-agent epistemics.

Decision-focused learning distinguishes prediction error from downstream decision loss
[@elmachtoub2022spo; @wilder2019decisionfocused]. Our additional setting is an agent that acquires
evidence under operational constraints and submits a reusable knowledge artifact. This study
measures artifact and action outcomes; it does not introduce a decision-focused training algorithm.

Model-discovery systems increasingly combine language models with Bayesian design, symbolic fitting
or probabilistic programme search [@murphy2026mda; @wahl2026probabilistic; @zheng2026newtonbench]. We
instead ask whether evidence changes the right representation and whether that representation is
usable for action. This follows the broader distinction between outcome and process validity
[@riosgarcia2026scientifically] and the warning that predictive success can coexist with
underspecified or shortcut solutions [@damour2022underspecification; @geirhos2020shortcut]. Causal
mediation analysis would require identified interventions on intermediate representations
[@imai2010mediation]; we do not infer such mediation from associated law and action readouts. The
central contribution is therefore a tiered diagnostic design: controlled initial-model manipulations,
conditional packet responses, failure-aware strategy estimates, descriptive law/action decomposition,
and a fixed-evidence factorial intervention with separate evaluator qualification.

# Discussion and limitations

The contribution is a bounded account of experimental knowledge and decision quality. Predictive
improvement does not establish selective repair, submitted laws lose different amounts of
information, and those laws do not reproduce many participant decisions. The four-condition study
estimates information strategies with operational failures retained. It does not isolate a pure
evidence-content or experiment-selection effect.

Decision loss, near-optimality and operational availability should accompany prediction error.
Continued search and best-minus-first improvement do not by themselves identify feedback learning.
Likewise, 11/42 scored Top-1 choices in the original longitudinal cohort do not estimate the benefit
of experimentation without its own matched control. Historical rank-gate results concern evaluator
design and are not another internal capability failure.

The study covers two fixed simulated model--tool configurations and five worlds per task.
B2 is an underidentifying surface with retrospective coding; B3 retains 13 DeepSeek schema failures.
Low reasoning is not thinking-off. Donor-eligible analyses are sensitivity-only; fixed order and
earlier donors confound configuration with time. These limits preclude model ranking or mediation.
Private confirmation and fresh-context transfer to new conditions remain untested.

The fixed-evidence factorial intervention does not establish a material fitted-law benefit.
Its near-complete agent/maximizer agreement also limits a general inability-to-deploy-laws account.
It does not isolate why the earlier, longer experimental protocol produced greater disagreement:
information, function class, decision dimension and interface all differ. Tool-free model fitting
versus numerical ridge also bundles arithmetic with artifact construction. A matched-tool control
would address that distinction; artifact-only and new-condition tests would address portability.
Fit plus argmax is a classical baseline, and no new repair algorithm is claimed.
