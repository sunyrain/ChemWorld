---
title: "Causal Dissection of Scientific Agents: Breaks from Evidence to Action"
subject: "Controlled causal analysis of how experimental evidence becomes predictions, executable laws, unseen actions, and evaluator decisions"
keywords: "scientific agents; autonomous experimentation; causal intervention; structural identification; executable laws; decision transfer; evaluator validity"
abstract: |
  Experimental success does not reveal whether a scientific agent learned the right model. We use
  ChemWorld as a controlled causal probe: physics, interface, resources, and stochastic identity stay
  fixed while the initial model is opaque, aligned, or misspecified at entity, parametric, or
  structural loci. Across 135 public sessions, search changed and prediction error fell in every arm
  and locus, yet all three selective-correction criteria failed. Matched structural evidence reduced
  mean error from 0.2255--0.3392 to 0.0060--0.0074, but DeepSeek and GPT recovered the registered 1.75
  power law in 0/5 misspecified worlds; the same break survived a lower-reasoning ablation. On matched
  30-cell identifiable-law surfaces, joint recovery was 0/30 for DeepSeek and 5/30 for Codex, with no
  registered action gain in either model. A 135-cell Codex replication lowered executable-law MAE
  from 0.237 to 0.175, yet blind gain remained approximately zero in both models. An oracle-free
  four-condition successor found no stable learned-law benefit; autonomy was directionally favourable
  but intervals crossed zero and yoked failures were substantial. Only 11/42 fresh action readouts
  selected Top-1. Finally, a ranking control passed 7/8 fresh units while selecting Top-1 in 1/8,
  whereas another failed the rank gate but selected Top-1 with zero regret. Numerical revision,
  structural identification, executable compression, decision transfer, and evaluator validity are
  distinct transitions rather than one score.
---

# Introduction

Autonomous experimental agents are increasingly judged by whether they discover high-performing
molecules or reactions. Yet an endpoint benchmark cannot distinguish whether an agent inherited a
fortunate prior, navigated a productive search corridor, adopted a phenomenological interpolation, or
genuinely revised its scientific understanding from evidence. We call this ambiguity endpoint
underdetermination. The relevant question is not only whether an agent finds a good experiment, but
what that experiment changes in its model of the world.

This distinction matters as language-model agents plan syntheses, call chemistry tools, operate
instruments, and enter self-driving laboratory workflows [@boiko2023autonomous; @bran2024augmenting;
@szymanski2023alab; @darvish2025organa; @song2025chemagents; @vriza2026instruments]. Interactive
environments increasingly test repeated cycles of hypothesis, intervention, and inference
[@jansen2024discoveryworld; @gandhi2025boxinggym; @duan2025scigym; @zheng2026newtonbench;
@yang2026causalab; @batzoglou2026replayscm]. Yet pretrained knowledge, prompt-provided information,
experiment selection, endpoint optimization, and verbal explanation are usually observed together.
Consequently, a high score need not identify which transformation succeeded, and a low score need not
identify which transformation failed.

We make those transformations observable by using ChemWorld as a controlled causal probe. The same
executable world, interface, resources, and stochastic identity are held fixed while its initial model
is made opaque, aligned, or misspecified at a declared entity, parametric, or structural locus.
Persistent agents then interact through a transactional laboratory interface. Evaluator-owned
counterfactual queries, matched contradictory evidence, executable-law assays, and unseen complete
ActionPlans separately measure search, prediction, structural identification, compression, and
decision transfer.

Our contribution is a causal map rather than a scalar leaderboard. Four breaks emerge: priors redirect
search without selective repair; matched evidence yields numerical convergence without reliable
structural recovery; executable laws can lose information present in explicit predictions; and both
agent-level law adequacy and evaluator-level rank qualification decouple from action validity. This
locates losses in revision, identification, compression, transfer, and evaluation.

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

## ChemWorld as a controlled causal probe

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

Provenance is block-specific: C2 and B3 have matched scheduled DeepSeek-high/Codex-medium surfaces;
matched evidence adds complete denominators and a DeepSeek-low structural ablation; the four-condition
successor retains model-specific donor eligibility. Provider-free controls and model configurations
are never pooled.

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
Prospective C2 & 270 scheduled & DeepSeek 121 complete; Codex 126 complete & Search, prediction, law, incumbent replay \\
Matched evidence & 75 sessions & DeepSeek high + GPT (60); B2 low (15) & Replicated numerical--structural break \\
Identifiable-law B3 & 60 scheduled & DeepSeek 17+13 failures; Codex 30 & Structural recovery and action bridge \\
Action assays & 45 cells + 360 slots & W2-50 + four conditions per model & Descriptive and failure-aware action transfer \\
96-query control & 15 planned & Provider-free; 8 attempted & Retained pre-participant rejection \\
320-query control & 7 exposed + 15 fresh & Provider-free; 7 pass + 1 fresh & Construction repair versus prospective rejection \\
Gate alignment & 16 unit versions & Provider-free; 0 new execution & Rank validity versus action validity \\
\bottomrule
\end{tabularx}
\end{table}
```

# Results: from priors to laws

## Priors scaffold search without selective correction

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
\caption{\textbf{Initial models redirect search, but the evidence does not establish selective repair
of the wrong model.} Pre-evidence errors, first-recipe divergence, pre-to-final error reductions, and frozen
failure-aware selective-correction contrasts are reported by intervention locus. Every arm improves
on average, but no locus passes the selective-correction criterion.}
\label{fig:prior-correction}
\end{figure}
```

## Matched counterevidence supports interpolation without structural recovery

Free discovery cannot distinguish failure to seek diagnostic evidence from failure to use it. In the
parametric matched-evidence block, all five misspecified summaries rejected the supplied
high-potential direction and recovered the peak-and-collapse response once the decisive profile was
provided. Part of the free-discovery loss therefore lay in evidence acquisition.

The corrected structural DeepSeek assay showed a different bottleneck. After every arm received the same
direct phase-process evidence, mean normalized errors fell from 0.2255, 0.2736, and 0.3392 to 0.0074,
0.0060, and 0.0071 for opaque, aligned, and misspecified cells. The misspecified-minus-aligned update
contrast was positive in only 3/5 worlds (exact one-sided sign-flip $p=0.125$), so this is numerical
convergence rather than a confirmatory arm effect. Yet 0/5 misspecified public summaries recovered
the registered 1.75 power law, 1/5 explicitly rejected the supplied linear form, and 5/5 adopted a
saturation or endpoint model. Direct evidence supported accurate local phenomenological interpolation
without structural identification (Fig.~\ref{fig:matched-evidence}).

The matched GPT replication preserved this break. A-P misspecified-minus-aligned update contrasts
were +0.0309 for DeepSeek and +0.0602 for GPT; structural B2 contrasts were +0.0645 and +0.0915,
while misspecified exact-law recovery remained 0/5 in each model. This is a block-specific
cross-model replication, not a model-superiority test.

Changing only the DeepSeek Codex reasoning effort from high to low preserved the structural break.
The B2 canary passed 3/3 and formal execution completed 15/15 with no failures. All 15 post errors
were below 0.02, while the registered contrast reversed to -0.0405 (2/5 positive worlds; exact
one-sided $p=0.8125$) and misspecified exact-law recovery remained 0/5. Provider-reported reasoning
output was 20.9\% lower than DeepSeek high on the same block. The low A-P canary lacked terminal
receipts and contributes no estimate. This is a same-harness reasoning-budget robustness result, not
reasoning-off or a configuration ranking.

An independent control made the 1.75 exponent identifiable on a disjoint scoring roster. Codex
completed 30/30 sessions; joint family--exponent recovery was 0/10, 5/10, and 0/10 for
opaque/aligned/misspecified, and 0/18 action-eligible cells achieved gain at least 0.02. The matched
DeepSeek successor retained 17 completed cells and 13 schema failures; failure-aware joint recovery
and Top-1 were 0/30, versus 5/30 and 2/30 for Codex. Neither model achieved the registered useful
action gain. Differential failures preclude model ranking, while the shared negative action bridge
strengthens the transition-level result.

```{=latex}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/prior-discovery/figure-4-matched-evidence-localization.pdf}
\caption{\textbf{Matched evidence yields numerical convergence without reliable law-to-action recovery.}
Panels a--b detail DeepSeek high. Panel c compares matched A-P DeepSeek/GPT and structural B2
DeepSeek-high/GPT-medium/DeepSeek-low contrasts. Panel d reports failure-aware completion, joint-law
recovery, Top-1, and useful action gain on matched 30-cell B3 surfaces.}
\label{fig:matched-evidence}
\end{figure}
```

All 135 DeepSeek laws executed, but 84 lost information relative to final explicit predictions; mean
law MAE was 0.237 and compression loss 0.069. Legal full-basis controls reproduced 135/135 prediction
states at mean MAE $4.25\times10^{-13}$, localizing the gap to participant distillation rather than
typed-interface capacity. Blind incumbent replay completed 726 executions for 121 cells, with
recommendations better/equivalent/worse in 1/119/1.

The matched Codex surface retained 126 completed, 3 failed, and 6 right-censored cells. All locus
gates again failed. Codex versus DeepSeek law MAE was 0.1753 versus 0.2371 and compression loss 0.0142
versus 0.0686, but blind gain was -0.0001 versus -0.0010. Better compression still did not improve
action (Fig.~\ref{fig:c2-cross-model}); model differences are descriptive.

```{=latex}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/prior-discovery/figure-5-capability-chain.pdf}
\caption{\textbf{Better executable laws still do not produce better actions.}
\textbf{a,} Registered correction estimates and lower bounds for both 135-cell C2 cohorts.
\textbf{b,} Numerical learning by locus and model. \textbf{c,} Final-prediction versus executable-law
MAE. \textbf{d,} Blind outcomes over every scheduled cell; model contrasts are descriptive.}
\label{fig:c2-cross-model}
\end{figure}
```

# Results: law, action, and evaluation

## Agent-level law adequacy does not determine unseen action selection

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
make no pooled arm-level claim (Fig.~\ref{fig:open-action}a,b).

This separation survives continuous and threshold-sensitive analysis. Pooled law MAE correlated
weakly with selected rank (Spearman $\rho=-0.073$, cluster-bootstrap 95% interval
$[-0.380,0.256]$) and normalized regret ($\rho=-0.133$, $[-0.452,0.217]$), while task-specific rank
associations reversed sign ($+0.524$, $-0.592$, and $-0.007$). Across law-MAE thresholds from 0.05
to 0.30, the adequate subset expanded from 1 to 34 cells but contained only 0 to 9 correct actions.
The four-way table is therefore not a single-cutoff artifact: law error has no stable monotonic map
to unseen-action quality across tasks.

## Four conditions separate autonomy from artifact portability

An independent development successor scheduled no evidence, yoked evidence, learned-law-only, and
autonomous-exploration action readouts for all 45 strata per model: 180 slots each and 360 total.
DeepSeek and Codex had 42 and 26 donor-eligible strata, with 26 coordinates shared. Within those
model-specific populations, autonomous-minus-no-evidence regret was -0.1214 (95% cluster interval
$[-0.2607,0.0225]$) and -0.1379 ($[-0.3452,0.1103]$); both favour autonomy but cross zero.
Learned-law-minus-no-evidence was -0.0267 and +0.0970, also with intervals crossing zero. Yoked
completion was only 10/42 and 24/26, so its failure-aware disadvantage cannot be interpreted as a
pure experiment-selection effect. The bounded result is directional total value for autonomy without
reliable transfer of the compressed law (Fig.~\ref{fig:open-action}a,c).

## Evaluator-level ranking and decision quality are different estimands

A planned five-condition follow-up required an outcome-disjoint oracle law to rank eight candidates
with Spearman $\rho\geq0.80$. The first eight fresh clusters completed 896/896 truth/replays, but the
eighth obtained $\rho=0.738095$ and the wrong Top-1; the frozen stop left all 225 participant sessions
unstarted. Expanding 96 queries to a 320-query grid repaired 7/7 exposed units, yet the first fresh
world failed at $\rho=0.714286$ while selecting Top-1 with zero regret. A zero-execution diagnostic
then reproduced all 16 unit versions: fresh 96-query rank gates passed 7/8 but Top-1 only 1/8, whereas
the fresh 320-query unit was rank-fail/action-correct. Full-order correlation and decision validity
therefore disagree in both directions (Fig.~\ref{fig:open-action}c,d; Table~\ref{tab:alignment}); the
historical stops remain valid, while future controls should prioritize regret and near-optimality.

```{=latex}
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/prior-discovery/figure-6-open-action-formal.pdf}
\caption{\textbf{Evidence, learned laws, and evaluator rankings diverge from action.}
\textbf{a,} Failure-aware regret across four W2-61 action conditions in model-specific donor-eligible
populations. \textbf{b,} W2-50 law error versus regret, with Top-1 stars and a cutoff inset.
\textbf{c,} Registered W2-61 contrasts with clustered intervals; yoked failures are retained.
\textbf{d,} Spearman correlation versus regret for all 16 frozen W2-53 unit versions.}
\label{fig:open-action}
\end{figure}
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

The systems search productively and learn numerically, yet lose information at distinct transitions.
Priors redirect search without selective repair; matched evidence supports near-exact interpolation
without reliable structural recovery; executable laws can compress predictions poorly; and neither
law adequacy nor complete-ranking qualification determines action validity. The oracle stop prevented
a reproducible but decision-misaligned control from producing an uninterpretable participant effect.
Evaluator validity is therefore part of scientific-agent validity.

## A transition map for scientific-agent evaluation

Evaluation should therefore separate interventions from readouts, score prediction, law and action on
their own units, and qualify controls on the intended endpoint. Regret, near-optimality and near-tie
handling should be primary for selection, with full-rank metrics diagnostic. Evidence roles must also
remain separate: the 96-query failure tests a control, the exposed 320-query pass tests construction,
and the fresh failure tests generalization. Exact scheduled, eligible, completed and unstarted counts
prevent these roles from being pooled into invented evidence.

## Limitations and conclusion

The study concerns two models and fixed agent--tool configurations in simulation, not cross-model
ranking or laboratory fidelity. C2 now has two complete 135-cell scheduled surfaces, but different
failure/censoring patterns and no randomized provider assignment. A-P/B2 each contain only five
worlds; DeepSeek low is not reasoning-off and its A-P block has no qualified denominator. B3 retains
13 DeepSeek schema failures, while the four-condition successor has unequal donor eligibility and
substantial yoked-recipient failure. These failures remain part of the system-level estimand and
preclude capability ranking or pure mediation claims. The original five-condition oracle cohort has
no participant data; W2-61 has no oracle arm. Higher-fidelity artifact portability and private
replication remain untested.

Scientific-agent claims should name interventions, units, failure rules, and transfer boundaries.
Agency is a chain from evidence to revision, identification, compression, and decision, breakable in
the agent or its evaluator.
