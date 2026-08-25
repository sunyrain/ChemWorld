---
title: "From Evidence to Action: Diagnosing Scientific Agents Across Experimentation, Law Formation, and Decision Transfer"
subject: "Controlled diagnosis of evidence acquisition, predictive revision, executable-law formation, unseen action selection, and evaluator validity"
keywords: "scientific agents; autonomous experimentation; executable laws; action selection; evaluator validity"
abstract: |
  Scientific agents are often evaluated by the best outcome reached during an experimental campaign,
  conflating evidence acquisition, predictive revision, law formation, and action selection. We study
  these transformations separately in ChemWorld, a suite of resource-bounded chemical environments
  with persistent state, complete executable action plans, held-out prediction queries, typed laws,
  and exact replay. Across 135 public agent sessions spanning entity, parametric, and structural
  initial-model interventions, agents frequently improved outcomes and predictions within a session,
  yet the value of a correct prior was task dependent and executable-law fidelity remained limited.
  Controlled matched-evidence studies showed that direct counterevidence could correct numerical
  predictions without reliably recovering the registered structural law. In fresh multi-task action
  selection, only 11 of 42 eligible sessions chose the true best unseen plan. Finally, the oracle
  control itself failed to align with the decision estimand: a 96-query oracle passed a complete-rank
  correlation gate in 7 of 8 fresh units but selected the true top action in only 1, whereas a
  320-query oracle failed the same gate on its first new world despite selecting the true best action
  with zero regret. Evidence acquisition, numerical revision, structural identification, action
  transfer, and evaluator validity are therefore distinct requirements for trustworthy scientific
  agents.
---

# Introduction

An experimental agent can succeed without learning the right science. It may inherit a correct model,
stumble into a productive region, or patch its actions while retaining a false explanation of the
world. An endpoint benchmark assigns the same success to all three cases. For a scientific agent,
however, they represent different capabilities: prior knowledge, local optimization, and
evidence-driven correction. The relevant question is not only whether an agent finds a good
experiment, but what that experiment changes in its model of the world.

This distinction matters as language-model agents plan syntheses, call chemistry tools, operate
instruments, and enter self-driving laboratory workflows [@boiko2023autonomous; @bran2024augmenting;
@szymanski2023alab; @darvish2025organa; @song2025chemagents; @vriza2026instruments]. Interactive
environments increasingly test repeated cycles of hypothesis, intervention, and inference
[@jansen2024discoveryworld; @gandhi2025boxinggym; @duan2025scigym; @zheng2026newtonbench;
@yang2026causalab; @batzoglou2026replayscm]. Yet pretrained knowledge, prompt-provided information,
experiment selection, endpoint optimization, and verbal explanation are usually observed together.
Consequently, a high score need not identify which transformation succeeded, and a low score need not
identify which transformation failed.

We make those transformations observable by intervening on the agent's initial world model while
holding the executable world fixed. The same hidden world is presented with an opaque, aligned, or
misspecified model at a declared entity, parametric, or structural locus. Persistent agents then
interact through a transactional laboratory interface. Evaluator-owned counterfactual queries,
matched contradictory evidence, executable-law assays, and unseen complete ActionPlans separately
measure search, prediction, structural identification, compression, and decision transfer.

Our contribution is an evidence-to-action diagnostic rather than another scalar leaderboard.
First, a 135-session prospective programme shows that priors redirect trajectories and that all arms
learn predictively, while the registered selective-correction criterion fails at every locus. Second,
matched evidence localizes the structural bottleneck: numerical predictions converge near truth, yet
the registered power law is recovered in 0/5 misspecified worlds. Third, a 45-cell multi-task assay
shows only 11/42 eligible terminal selections at true Top-1. Finally, qualification of a planned
causal action-transfer control reveals evaluator misalignment: complete-ranking correlation and
decision quality disagree in both directions. The result is a capability chain with empirically
distinct failure locations, including failure in the evaluator itself.

```{=latex}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/prior-discovery/figure-1-prior-to-law.pdf}
\caption{\textbf{Endpoint success underdetermines scientific competence.}
The same outcome can arise from a correct prior, local search, or evidence-driven model correction.
ChemWorld intervenes on the initial model while holding the executable world fixed, then evaluates
the transitions from evidence to predictions, executable laws, and unseen actions.}
\label{fig:capability-chain}
\end{figure}
```

# Environment and evaluation

## Fixed world, programmable initial model

ChemWorld separates three objects. The executable world contains hidden state, transition and
measurement laws, resources, and terminal assays. The public task exposes typed operations,
instruments, observations, and an initial model. The evaluator owns held-out truth, replay, and
scoring. For world $w$ and initial-model arm $a$, the hidden transition process remains fixed while
the supplied model $M_{0,a}$ changes. The aligned model is correct at one declared locus, the
misspecified model is explicit but wrong at that locus, and the opaque arm withholds the corresponding
structure. Because operations and measurements remain identical, differences can be attributed to
information supplied to the complete agent--tool system rather than to different physics.

Actions are transactions, not free-form prose. The host validates a typed request, checks resources
and preconditions, commits the state transition, and returns a public observation or a structured
rejection. Failed actions and discards remain in the trajectory. Every submitted action, commit,
rollback, measurement, assay, and resource delta is recorded for exact replay. These semantics matter:
an action recommendation is scientific evidence only when the evaluator can execute the same complete
plan without filling in hidden workflow choices.

## Five-stage capability chain

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
executes prespecified counterfactual query sets independently of the participant. It scores 675/675
checkpoints from 420/420 truth executions and later runs each final typed law on the same coordinates.
Paired blind replay evaluates the final recommendation against the observed incumbent, while a
separate longitudinal assay reveals eight outcome-hidden complete ActionPlans only after autonomous
exploration has ended.

# Experimental programme

The prospective programme is layer-stratified. Entity interventions cover five task families and five
independently selected public worlds per task. Parametric and structural blocks each cover two
validated task families and five worlds. Every task--world cluster contains opaque, aligned, and
misspecified arms, yielding 45 clusters and 135 independent persistent sessions. Campaign length is
locus-specific: eight, ten, or twelve complete experiments, with five checkpoints in every session.
Exploratory, validation, prospective, matched-evidence, and open-action worlds remain separated.

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
semantics are not pooled. Failed scientific cells stay in their scheduled denominator, with the last
valid checkpoint carried forward for right-censoring and zero primary improvement assigned when the
final prediction is missing. Only a pure infrastructure failure without a persisted trajectory can
resume under a fixed attempt cap.

Matched-evidence sessions use cloned worlds and provide the same decisive counterevidence to every
arm, separating failure to seek evidence from failure to update after seeing it. The longitudinal
action matrix separately contains three tasks, five worlds, and three arms (45 scheduled cells). After
12 autonomous experiments, each agent ranks eight new plans; regret and Top-1 are primary action
readouts, while complete-rank correlation and law adequacy are diagnostics. Table~\ref{tab:evidence}
keeps these layers and their claim boundaries explicit.

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
Prospective priors & 135 sessions & 1,243/1,260 experiments & Search, prediction, law, incumbent replay \\
Matched evidence & 30 sessions & fixed evidence packets & Numerical update versus structural recovery \\
Open action & 45 cells & 42 eligible; 240/240 truth/replay & Descriptive unseen-plan selection \\
96-query control & 15 planned & 8 attempted; 896/896 truth/replay & Retained pre-participant rejection \\
320-query control & 7 exposed + 15 fresh & 7 exposed pass; 1 fresh attempted & Construction repair versus prospective rejection \\
Gate alignment & 16 unit versions & 0 new execution & Rank validity versus action validity \\
\bottomrule
\end{tabularx}
\end{table}
```

# Results: from priors to laws

## Priors redirect search but do not guarantee selective correction

All 135 scheduled sessions produced final records. Participants completed 1,243/1,260 planned
experiments; 121 sessions met operational eligibility. The denominator retains 26 discarded
lifecycles, 13 resource-ledger rejections, and all right-censored cells. Every session submitted five
checkpoints, providing 6,300 counterfactual predictions and 24,300 query--metric values.

The intervention reached behavior. The first complete recipe differed between aligned and
misspecified cells in 45/45 matched clusters, between opaque and aligned in 45/45, and between opaque
and misspecified in 44/45. This is a manipulation check rather than a causal effect estimate because
there are no repeated same-arm sessions. Search continued after the first proposal: 91.2% of completed
experiments used a unique recipe, 84.4% of session optima appeared after the midpoint, and 32.6%
appeared in the last completed experiment.

Correct-prior utility was task dependent. In entity-level partition, aligned information produced a
+0.200 best-endpoint advantage over the misspecified arm in 5/5 worlds. In structural
crystallization, a +0.141 first-experiment head start narrowed to +0.055 as the disadvantaged arm
explored. In structural partition, aligned and misspecified descriptions both helped relative to
opaque identifiers while differing little from one another. A correct model therefore altered the
search landscape without imposing one endpoint ordering.

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
\caption{\textbf{Initial models redirect search, but evidence does not selectively repair the wrong
model.} Pre-evidence errors, first-recipe divergence, pre-to-final error reductions, and frozen
failure-aware selective-correction contrasts are reported by intervention locus. Every arm improves
on average, but no locus passes the selective-correction criterion.}
\label{fig:prior-correction}
\end{figure}
```

## Matched evidence separates numerical revision from structural identification

Free discovery cannot distinguish failure to seek diagnostic evidence from failure to use it. In the
parametric matched-evidence block, all five misspecified summaries rejected the supplied
high-potential direction and recovered the peak-and-collapse response once the decisive profile was
provided. Part of the free-discovery loss therefore lay in evidence acquisition.

The corrected structural assay showed a different bottleneck. After every arm received the same
direct phase-process evidence, mean normalized errors fell from 0.2255, 0.2736, and 0.3392 to 0.0074,
0.0060, and 0.0071 for opaque, aligned, and misspecified cells. The misspecified-minus-aligned update
contrast was positive in only 3/5 worlds (exact one-sided sign-flip $p=0.125$), so this is numerical
convergence rather than a confirmatory arm effect. Yet 0/5 misspecified public summaries recovered
the registered 1.75 power law, 1/5 explicitly rejected the supplied linear form, and 5/5 adopted a
saturation or endpoint model. Direct evidence supported accurate local prediction without structural
identification (Fig.~\ref{fig:matched-evidence}).

```{=latex}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/prior-discovery/figure-4-matched-evidence-localization.pdf}
\caption{\textbf{Matched evidence restores numerical predictions without structural recovery.}
All 15 corrected structural cells receive identical evidence and converge near truth. Across the five
misspecified worlds, exact recovery of the registered power law is absent despite low post-evidence
error.}
\label{fig:matched-evidence}
\end{figure}
```

All 135 final typed laws executed on their prespecified coordinates, but executability did not
preserve the information in conditional predictions. Mean law error was 0.237; relative to effective
final predictions, laws were better in 50 cells, equal in one, and worse in 84, with mean
law-minus-prediction error +0.069. Typed syntax solved execution coverage, not faithful scientific
compression. Paired blind replay likewise tested only incumbent retrieval: 726/726 executions
completed for 121 evaluable cells, with recommendations better/equivalent/worse in 1/119/1 cells.
Selection beyond the observed campaign required a separate assay.

# Results: laws to actions

## Selection among unseen complete plans is partial

The longitudinal matrix produced records for 45/45 scheduled cells. Truth evaluation and exact replay
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
make no pooled arm-level claim (Fig.~\ref{fig:open-action}).

```{=latex}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/prior-discovery/figure-6-open-action-formal.pdf}
\caption{\textbf{Terminal selection of unseen plans is partial and task dependent.}
Selected true rank, normalized regret, joint law--action categories, and task-level mean ranks are
shown for 42 eligible cells. Three retained crystallization failures remain in the 45-cell scheduled
denominator. The random-rank line is not an experimental control.}
\label{fig:open-action}
\end{figure}
```

## The oracle gate does not equal the action estimand

A planned five-condition causal follow-up required a provider-free oracle law to rank the eight
candidates with Spearman $\rho\geq0.80$ before any participant was called. The first eight of 15 fresh
clusters completed 896/896 truth executions and exact replays. Candidate-opportunity gates passed
8/8, but the eighth oracle obtained $\rho=0.738095$ and disagreed on Top-1. The frozen stop rule left
seven clusters, the operational canary, all 225 participant sessions, and 540 planned participant
experiments unstarted. This is a rejection of the control construction, not an estimated participant
effect.

We then isolated grid coverage while retaining the fitted ExtraTrees family and the correlation
threshold. Expanding from 96 queries to 64 global plus 256 candidate-neighborhood queries repaired all
four historical failures: 7/7 exposed construction units passed with 2,352/2,352 truth executions and
exact replays, and minimum $\rho$ was 0.857143. Prospective validity did not follow. The first new
electrochemical world completed 336/336 truth executions and replays but obtained $\rho=0.714286$,
triggering the same stop boundary and leaving 14 fresh clusters unstarted. Nevertheless, this oracle
selected the true Top-1 action with normalized regret zero.

A frozen zero-execution diagnostic reproduced the original rank and Top-1 outcomes for all 16
completed 96- and 320-query unit versions. Among the eight fresh 96-query units, the rank gate passed
7/8 but Top-1 was correct in only 1/8 and within 0.01 of optimum in 3/8; six were
rank-pass/action-wrong. The fresh 320-query unit was rank-fail/action-correct. Thus global-order
correlation and decision validity disagree bidirectionally. The historical gates and stops remain
valid for their protocols, but future controls must prospectively prioritize regret, near-optimal
selection, and near-tie-aware ordering, retaining full-ranking correlation as a secondary diagnostic.

For eight candidates without ties, Spearman correlation is
$\rho=1-\sum_i d_i^2/84$, where $d_i$ is the displacement of candidate $i$ between predicted and true
ranks. The retained 96-query failure, $\rho=0.738095$, therefore represents
$\sum_i d_i^2=22$; the fresh 320-query failure, $\rho=0.714286$, represents 24. The scalar says how
much the full ordering moved, not where the displacement occurred. The former selected the wrong
Top-1 while the latter preserved it exactly, making the estimand mismatch concrete rather than merely
threshold dependent.

```{=latex}
\begin{table}[t]
\caption{\textbf{Complete-ranking gates and action endpoints are different estimands.}}
\label{tab:alignment}
\centering
\scriptsize
\begin{tabular}{@{}lrrrr@{}}
\toprule
Frozen block & $n$ & Rank pass & Top-1 & $\leq0.01$ regret \\
\midrule
Fresh 96-query & 8 & 7 & 1 & 3 \\
Exposed 320-query & 7 & 7 & 4 & 6 \\
Fresh 320-query & 1 & 0 & 1 & 1 \\
\bottomrule
\end{tabular}
\end{table}
```

# Related work

Self-driving laboratories and chemistry agents emphasize closed-loop execution, tool use, or endpoint
optimization [@felton2021summit; @hase2021olympus; @boiko2023autonomous; @bran2024augmenting]. Virtual
laboratories and process-control environments provide scalable interaction and safety
[@beeler2024chemgymrl; @bloor2024pcgym; @malik2026made; @chen2025physgym]. Scientific-discovery
benchmarks increasingly test iterative experimentation, causal inference, and transferable knowledge
[@jansen2024discoveryworld; @gandhi2025boxinggym; @duan2025scigym; @yang2026causalab;
@batzoglou2026replayscm]. ChemWorld complements these directions by making the initial model an
experimental variable and by evaluating each transformation from evidence to action with
evaluator-owned truth and exact replay. The central distinction is diagnostic: endpoint success,
prediction learning, law recovery, and action quality are not interchangeable readouts.

# Discussion and limitations

The evaluated system frequently searches productively and learns numerically, but its transformations
lose information at different locations. Correct priors alter trajectories without a general endpoint
advantage. Free evidence reduces prediction error without selectively repairing wrong priors. Direct
matched evidence can yield near-exact numerical revision while structural recovery fails. Typed laws
can execute yet compress predictions poorly, and a thresholded law does not guarantee the correct
unseen action. These are not multiple scores for one latent ability; they are distinct capabilities
with different interventions and denominators.

The oracle study extends this diagnosis to the harness. A metric can be reproducible and still be
misaligned with the intended decision. Spearman correlation rewards ordering across all candidates,
whereas the causal follow-up needs a positive control for selected action and decision loss. Stopping
before participant execution prevented a weak control from producing an uninterpretable effect. More
generally, evaluator validity is part of scientific-agent validity, not a post-hoc implementation
detail.

## Implications for scientific-agent benchmarks

The capability chain suggests three design requirements. First, benchmarks should separate the
intervention from the readout. Manipulating prior information, supplying matched evidence, or hiding
candidate outcomes answers different questions and therefore requires different independent units.
Checkpoint predictions, law execution, and action regret should remain distinct even when a composite
score would be convenient. This makes it possible to tell whether a failure arose in acquisition,
revision, representation, or transfer.

Second, positive controls should qualify on the endpoint used by the intended contrast. A law can be
outcome-disjoint, exactly replayable, and strongly correlated with a full ranking while still choosing
the wrong action. Conversely, a decision can be optimal despite moderate errors elsewhere in the
ordering. For selection problems, regret and near-optimality should be primary, with full-rank metrics
used to diagnose how much additional structure was preserved. Near ties should be declared before
execution so that metric choice cannot respond to an unfavorable world.

Third, the evidence record must preserve failed and unstarted units. The 96-query failure is evidence
about a control; the 320-query exposed pass is evidence about construction; the first prospective
320-query failure is evidence about generalization. Pooling them would erase the distinction between
repairing known cases and succeeding on fresh cases. Likewise, treating stopped participant sessions
as zero-valued effects would invent data. Explicit scheduled, eligible, attempted, completed, and
unstarted denominators make negative results usable without turning them into claims they cannot
support.

## Limitations and conclusion

The evidence is deliberately bounded. It concerns one complete agent--tool configuration in simulated
chemical worlds, not a cross-model ranking or a claim about laboratory fidelity. Some contrasts have
only five independent worlds. The open-action matrix has no no-evidence or pre-exploration action
baseline and therefore supports no causal action-transfer effect. The planned five-condition cohort
has zero participant data because its control failed before execution. A single-stratum development
pilot of reduced conditions ended with the yoked session right-censored after five of six turns and is
not used for causal or arm-level inference. Context-reset artifact portability, private-world
replication, and cross-provider generalization remain untested.

The practical implication is to evaluate a scientific agent as a sequence of transformations. Each
claim should name its intervention, unit, readout, failure rule, and transfer boundary. On this basis,
scientific agency is not an endpoint score: it is evidence acquisition, numerical revision,
structural identification, executable compression, and decision transfer, qualified by an evaluator
that measures the action actually at stake.
