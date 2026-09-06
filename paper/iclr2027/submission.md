---
title: "When Does Experimental Knowledge Improve Scientific Decisions?"
subject: "Experimental knowledge, executable artifacts and decision quality in scientific agents"
keywords: "scientific agents; experimental knowledge; decision quality; executable laws; controlled evaluation"
abstract: |
  Scientific agents can improve experimental outcomes without converting that experience into
  accurate, executable and useful knowledge. We measure four observable conversion questions in
  ChemWorld: search to selective correction, numerical prediction to structure, predictions to
  executable laws, and laws to unseen decisions. Two model configurations each entered 135
  campaigns across 45 matched task--world clusters. Prediction errors fell, selective-correction
  criteria remained unmet, and executable summaries lost predictive information. A final 120-session
  minimal-interface diagnostic retained 117 valid completions, yet recovered the joint family and
  exponent in 0/80 opaque or misspecified cases. Optional numerics changed recovery by +1.67
  percentage points (95% interval [-8.33, 10.00]); all recoveries retained an already-correct prior.
  In a separate DeepSeek cohort, laws selected the optimum in 0/45 unseen-plan cases versus 11/45
  participant choices. These differences are conditional: a ten-world representation/decision
  intervention found no supported material fitted-law benefit and complete fitted-law
  agent/maximizer agreement. Delivering model laws alone to fresh recipients on new same-world
  candidates reduced regret by 0.13723 relative to task information alone, while nearest-evidence
  retrieval attained zero regret. Together these results separate conversion losses from success
  conditions; they do not establish four internal causal failures, universal agent deficits,
  retrieval superiority or transfer to changed physical conditions.


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

We organize the study around four observable conversion questions: **F1**, experimental
search to selective correction; **F2**, numerical prediction to structural identification;
**F3**, conditional predictions to executable laws; and **F4**, submitted laws to unseen-plan
decisions. Each question uses its own protocol, denominator and failure accounting. The four
questions do not form an identified internal causal chain, and success at one readout does not
substitute for measuring the next.

The primary study used a fixed DeepSeek-v4-flash experimental-agent configuration, with
135 scheduled cells nested within 45 task--world clusters; a GPT-5.6-sol successor used the same
scientific surface. A final matched-packet experiment adds minimal submissions and optional
numerics to test F2 with fewer submission demands. We also cross law source with decision rule
under fixed evidence, then deliver laws independently of raw evidence to fresh recipients.
These interventions establish conditions for agreement and useful knowledge, bounding a general
law-use failure account without identifying the causes of historical cross-protocol differences.


```{=latex}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/prior-discovery/figure-1-prior-to-law.pdf}
\caption{\textbf{Endpoint success does not reveal what the agent learned.}
ChemWorld varies the supplied initial description while fixing the executable world, public rules,
and budget. Four conversion questions separately assess correction, structure, law fidelity and unseen decisions. The diagram describes the design; its arrows do not identify internal belief or causal
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

C2 and B3 retain matched scheduled surfaces for both configurations; matched evidence adds a
DeepSeek-low B2 ablation. Historical controls preserve configuration-specific denominators.
The two artifact interventions prespecify equal-weight model/repeat means within world.

```{=latex}
\begin{table}[t]
\caption{\textbf{Executed evidence layers and claim boundaries.} A completed work package may contain
a retained scientific rejection; unstarted units are not silently removed.}
\label{tab:evidence}
\centering
\footnotesize
\setlength{\tabcolsep}{4pt}
\begin{tabularx}{\linewidth}{@{}p{0.19\linewidth}p{0.19\linewidth}p{0.27\linewidth}Y@{}}
\toprule
Layer & Units & Execution & Supported role \\
\midrule
Prospective C2 & 270 scheduled & DeepSeek 121 complete; GPT 126 complete & Search, prediction, law, incumbent replay \\
Matched evidence & 75 sessions & DeepSeek high + GPT medium (60); DeepSeek low (15) & Conditional numerical--exact-law-expression dissociation \\
Historical B3 & 60 scheduled & DeepSeek 17+13 failures; GPT 30 & Structural recovery and action bridge \\
Minimal-interface diagnostic & 120 scheduled; 5 reused worlds & 117 complete; 3 failures & Structure and optional-numerics availability \\
Action assays & 45 cells + 360 slots & Open action + four conditions/model & Descriptive and failure-aware action transfer \\
Factorial intervention & 160 slots; 10 worlds & 120/120 sessions; 200/200 physics/replays & Fixed-evidence law and decision-rule replacement \\
Information separation & 160 slots; 10 reused worlds & 160/160 sessions; 80/80 physics/replays & Same-world artifact-only decision utility \\
Evaluator controls & 16 unit versions & Provider-free; original stops retained & Rank validity versus action validity \\
\bottomrule
\end{tabularx}
\end{table}
```

# Results: four observable conversion questions

## F1: Prior-conditioned search and unmet correction criteria

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
($p=0.079$), and -0.224 for structural ($p=1.000$); none passed. These criteria did not establish
preferential correction of a wrong starting model (Fig.~\ref{fig:prior-correction}).

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

## F2: Matched packets expose numerical--expression dissociation

Matched packets provide conditional evidence response, with the packet and extra response turn
bundled. In the parametric block, all five DeepSeek misspecified summaries rejected the supplied
high-potential direction. B2 produced low post-packet error but no exact wrong-arm law expression
(0/5 in each model and DeepSeek-low); its one-pair linear/power alias makes it an underidentifying
surface. These observations cannot establish internal structural-identification failure.

Historical B3 retained 30 GPT completions and 17 DeepSeek completions plus 13 schema
failures; joint recovery was 5/30 versus 0/30 and useful gain 0/18 for both. The reference fitter
used privileged simulation, so its qualification does not prove public-only identifiability.
Historical controls and their failures remain in the appendix (Fig.~\ref{fig:matched-evidence}).

A final independent diagnostic reused all five B3 worlds, three priors, two model
configurations and two repeats, now crossing optional numerics with a minimal submission.
All 120 sessions were attempted; 117 completed and three failed. Mean prediction error fell
on the 29/30/29/29 available pairs for GPT off/on and DeepSeek off/on, respectively. Yet joint
family/exponent recovery was 0/80 across opaque and misspecified priors (78 valid completions).
All 17 successes were aligned-prior retention: GPT off/on 6/10 and 7/10, DeepSeek 2/10 and 2/10.
The prespecified tool-on minus tool-off contrast was +1.67 percentage points, with a five-world
95% bootstrap interval [-8.33, 10.00]. This supports neither a clear improvement nor equivalence.
Tool uptake differed: GPT used numerics in 0/30 enabled sessions, DeepSeek in 20/30. The result
therefore estimates availability in these systems, not a forced-computation effect. The historical
reference fitter used a privileged simulator; public-only identifiability remains unproven.
This block reduces the observed submission-failure burden without randomly isolating a schema
effect, and does not replace free-form law compression or the longitudinal action assay.

```{=latex}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/prior-discovery/figure-9-final-diagnostic.pdf}
\caption{\textbf{Valid submissions and optional numerics do not ensure structural recovery.}
\textbf{a,} Joint family/exponent success by prior, model and tool availability; each point retains
ten scheduled sessions. All successes are in the aligned-prior stratum, where the correct law was
supplied. \textbf{b,} Paired effects in five reused worlds and the equally weighted mean with its
prespecified approximate 95\% interval. Tool availability is the intervention: GPT used it in
0/30 sessions and DeepSeek in 20/30. Three failures remain in the denominator.}
\label{fig:final-diagnostic}
\end{figure}
```

## F3: Executable laws lose information from predictions

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

## F4: Submitted laws and unseen-plan decisions can disagree

The longitudinal DeepSeek cohort retained 45 scheduled cases and 42 terminal rankings, with
240/240 hidden plan evaluations and exact replays. Last-available laws selected the Top-1 plan
in 0/45 cases, compared with 11/45 participant choices; participants followed their law in
12/42 available rankings. Failure-aware participant/law regret was 0.344/0.438. Law error had
weak pooled association with regret, and task-specific associations reversed sign. An artifact
is thus an incomplete behavioral proxy on this protocol; neither law following nor law quality
was randomized, and the original cohort lacks a no-evidence action control.

A separate development successor retained four strategies over 45 strata per model (360 slots).
Autonomy-minus-none regret was -0.0913 for DeepSeek (95% interval [-0.2124, 0.0388]) and +0.1102
for GPT ([-0.0533, 0.2794]). Both intervals cross zero and include donor and delivery failures;
they do not isolate a pure acquisition effect. Completed-donor sensitivities, all failures and
the descriptive law/action decomposition appear in the appendix (Fig.~\ref{fig:open-action}).
Ranking-gate versus decision-loss disagreement is separately an evaluator diagnostic, not a
fourth internal participant fault (Table~\ref{tab:alignment}).

# Success conditions: controlled artifact and information interventions

## Fixed-evidence representation and decision replacement

The factorial assay fixes twelve public experiments per world and crosses model-generated (L)
or public-ridge-fitted (F) quadratics with fresh-agent (A) or deterministic-maximizer (X) choice.
Two tasks, five new worlds per task and two repeats per model yield forty source states nested
within ten worlds. Sources never see the eight terminal candidates; recipients receive the
evidence, candidates and designated law. All 120 sessions, 160 conditions and 200 physical
executions with exact replay completed without failure or replacement.

F-X minus L-X regret was -0.00538 (95\% world-bootstrap interval [-0.01630, 0.00061]); the upper
endpoint did not fall below the prespecified -0.01 material-benefit threshold. Task means were
-0.01087 in electrochemistry and +0.00010 in crystallization, with the substantial negative effect
concentrated in one world. Figure~\ref{fig:m1-replication} in the appendix shows all world effects
and five registered contrasts. The fixed utility scale is one; models and repeats are averaged
within world, and five worlds per task limit the bootstrap approximation.

Agent/maximizer choices agreed in 39/40 model-law and 40/40 fitted-law pairs. The latter's
zero-width bootstrap interval describes observed equality, not population equivalence.
Fitted-maximizer regret was 0.00425, versus 0.00354 for nearest public evidence and 0.11109 for
uniform-random expected choice. There was no observed advantage over retrieval. This bounds a
general law-use failure account, but the co-delivered raw evidence prevents an artifact-only
interpretation; the causes of historical cross-protocol disagreement remain unidentified.

## Information separation reveals independent artifact value

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
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/prior-discovery/figure-8-m3-portability.pdf}
\caption{\textbf{Artifacts support fresh decisions, while retrieval remains a strong baseline.}
\textbf{a,} Dots show world means over two models and two repeats per information condition;
diamonds show task means. All 160 selections are available. Nearest evidence has zero regret in
all ten worlds. \textbf{b,} Colored points show paired world effects; black diamonds and lines
show means and prespecified intervals (95\% primary; 99\% for five secondary comparisons).
The dotted primary reference is -0.01. L/F denote model-generated/fitted laws supplied without
raw observations. These are new candidate plans in the ten reused worlds, not new physical
mechanisms or additional independent replication worlds.}
\label{fig:m3-portability}
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
a fixed-evidence factorial intervention, and information-separated artifact deployment
with separate evaluator qualification.

# Discussion and limitations

These studies distinguish artifact fidelity, behavioral agreement and independent decision value.
Historical prediction gains did not establish selective repair, and submitted laws often differed
from participant choices. The fixed-evidence intervention found high agent/maximizer agreement
without a supported material fitted-law benefit. Information separation then established that a
compact model law can help a fresh recipient on new plans in the same worlds. Raw evidence also
helped, and nearest retrieval achieved zero regret; this is a bounded knowledge-utility result,
without demonstrated superiority or a new repair algorithm.

The information comparison evaluates deployment strategies, including context quantity and
computation. Matching recipient tools does not remove the original tool-free-model versus
numerical-ridge difference at source. Five worlds per task support approximate intervals, and
reuse does not add independent replication worlds. Effects differ substantially by task. The
protocols also differ in information, function class, decision dimension and interface; their
contrast does not isolate a single cause or internal psychological mediation. Private confirmation,
new-physical-condition transfer and independent-backend replication remain untested.

Historical controls retain additional limits. B2 is underidentifying; historical B3 retains 13
DeepSeek schema failures. The minimal-interface diagnostic retains three failures and a tool
effect interval crossing zero; absent GPT tool uptake limits any arithmetic interpretation.
Its privileged reference qualification does not establish public-only identifiability. Low reasoning is not thinking-off. Donor-eligible analyses are sensitivity-only,
and fixed order and earlier donors confound configuration with time. The earlier four-condition
strategy study retains delivery failures and cannot isolate pure acquisition. Decision loss,
near-optimality, availability and source/deployment costs should therefore remain separate;
best-minus-first gains alone do not establish feedback learning or experimental savings.
