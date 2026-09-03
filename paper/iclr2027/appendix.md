# Appendix

## Environment semantics and intervention construction

An executable world is a stateful transition system with typed operations, measurement functions,
finite resources, terminal assays, and an evaluator-only truth surface. A task publishes the operation
and instrument contracts while withholding the latent state and registered relations. A scenario
binds a world, public task description, resource card, and initial model. Initial-model arms alter one
declared information locus without changing the transition process, measurement process, candidate
actions, or evaluator truth.

The entity locus changes material identity or ontology. The parametric locus changes a quantitative
response model while preserving the declared entities. The structural locus changes the functional
form used to describe a mechanism. Aligned and misspecified models are matched in explicitness so
that a contrast is not merely information versus no information. The opaque arm exposes the same
laboratory interface but withholds the intervened model component. Exploratory, validation,
prospective, and private world selections are disjoint by construction.

### Task--locus roster and world splits

The nine prospective task--locus combinations are fixed before participant execution. The entity
intervention swaps matched nominal descriptor rows while leaving physical identity fixed. Parametric
and structural interventions replace only the declared response component; all other task text,
tools, resources, queries, and world state remain matched.

```{=latex}
\begin{table}[h]
\caption{\textbf{Nine prospective task--locus combinations.} ``Registered target'' names the
component manipulated in the initial model, not information revealed by the evaluator.}
\label{tab:task-roster}
\centering
\scriptsize
\begin{tabularx}{\linewidth}{@{}llYY@{}}
\toprule
Locus & Task & Registered target & Held-out diagnostic \\
\midrule
Entity & Electrochemical conversion & solvent identity descriptors & conversion/selectivity response \\
Entity & Reaction--crystallization & solvent identity descriptors & reaction and crystal outcomes \\
Entity & Reaction--distillation & solvent identity descriptors & reaction and separation outcomes \\
Entity & Partition discovery & extractant identity descriptors & phase-partition outcomes \\
Entity & Reaction safety & catalyst identity descriptors & yield, kinetics, and risk \\
Parametric & Electrochemical conversion & quantitative potential-response direction & peak-and-collapse profile \\
Parametric & Reaction safety & quantitative catalyst/thermal response & productive versus hazardous regime \\
Structural & Partition discovery & linear versus power-form phase relation & registered exponent $1.75$ \\
Structural & Reaction--crystallization & pathway/topology and accumulation form & multistage outcome surface \\
\bottomrule
\end{tabularx}
\end{table}
```

Development and qualification use seeds 0--4 and never enter the prospective denominator. Public
worlds are five task-specific SHA-256-derived identities per task; their values are fixed in the
released configuration. The private split is bound by a commitment but was not unsealed or executed.
Matched-evidence and action studies use separately frozen public surfaces. Sessions sharing a
task--world but differing in prior arm are repeated measurements within one inference cluster.

### Metrics and registered correction gates

For prediction or executable law $f$, truth $y$, registered query--metric pairs $j=1,\ldots,J$, and
fixed positive metric scale $s_j$ (one for bounded metrics unless overridden), normalized error is

```{=latex}
\[
E(f)=\frac{1}{J}\sum_{j=1}^{J}\min\!\left(\frac{|f_j-y_j|}{s_j},1\right).
\]
```

For candidate scores $q_i$, selected candidate $a$, best $q_{\max}$, and worst $q_{\min}$,
normalized regret is $(q_{\max}-q_a)/(q_{\max}-q_{\min})$, with zero assigned when the packet range
is numerically zero. A missing or invalid terminal ranking receives failure-aware regret one and
Top-1 zero. Near-optimal selection means raw regret at most 0.01; pairwise ordering excludes truth
pairs separated by less than 0.01.

Let $I_a=E_{a,0}-E_{a,K}$ and $C=I_{\mathrm{mis}}-I_{\mathrm{aligned}}$. The entity gate is a
three-component intersection--union test at one-sided $\alpha=0.05$: the lower bound for $C$ must
exceed zero, misspecified improvement must exceed zero, and aligned improvement must exceed the
non-inferiority margin $-0.05$. Parametric and structural gates use equal-task fixed-effect estimates
of $C$, require the one-sided lower bound above zero and positive direction in every included task.
For an incomplete cell, confirmatory bounds use the adverse interval $[-1,+1]$ for arm improvement;
the corresponding contrast can therefore span $[-2,+2]$. Last-observation-carried-forward and zero
improvement are observed-point sensitivities only and do not generate the confirmatory $p$ values.

## Persistent execution and checkpoints

Each participant cell is one persistent agent process. At every turn, the agent may call only the
public laboratory tools. The host validates schemas and preconditions, applies resource accounting,
commits successful transactions, and returns public observations. It does not choose or repair an
experiment on the participant's behalf. Entity, parametric, and structural campaigns permit eight,
ten, and twelve complete experiments, respectively. Checkpoints occur at experiments
0/2/4/6/8, 0/2/4/7/10, and 0/3/6/9/12.

Every checkpoint records model-reliability judgements, query predictions, uncertainty, public
evidence references, a typed executable law, and the intended next experiment. Checkpoint repair is
part of the evaluated interface burden. All eventually yielded valid records, but rejected attempts
remain in the process log and resource accounting.

### System, prompt, tool, and budget contract

`DeepSeek-v4-flash` with `reasoning_effort=high` supplies the primary DeepSeek C2, matched-evidence,
B3-successor, and action surfaces; the same model at `low` supplies only the completed B2
reasoning-budget ablation. `GPT-5.6-sol` with `reasoning_effort=medium` supplies the matched GPT
replications. Both run through the Codex session harness; “Codex” therefore denotes execution
infrastructure, not a third participant model. Provider aliases, run dates, receipt counts, and usage
fields remain in the retained internal records rather than the anonymous supplement. The supplement
retains sanitized model/configuration labels, scheduled completion denominators, and derived resource
summaries. Temperature is not exposed or set by the harness. Request timeout is 1,200 s; finalization
timeout is 600 s; progress is emitted every 30 s.

Each C2 cell receives one task/scenario prompt, the same public operation schemas, the arm-specific
initial model, and no evaluator truth. A persistent transcript spans the complete campaign. The fixed
8/10/12-experiment budgets allow at most 96/110/168 operation attempts, 480k/600k/720k uncached input
tokens, 128k/160k/192k output tokens, and 7,200/7,200/9,000 s wall time, respectively. Each cell uses
at most two provider calls within the same session; infrastructure-only resume is capped once, while
any persisted scientific trajectory forbids replacement. Matched-evidence assays use exactly two
same-thread turns: a pre-evidence submission and a post-packet submission. The supplement includes
the exact static system prompts, selected prompt-generating function sources, public protocol
projections, representative strict response schemas, and the executable-law contract.
The package also contains all 45 sanitized B2 public summaries, the retrospective expression-coding
function, three-configuration all-arm counts, and the participant-visible B2 identifiability audit.

### Executable-law schema and ActionPlan construction

A law contains one metric equation for every required metric, an intercept, identity or logistic link,
output bounds, evidence references, confidence, applicability, and limitations. Each metric permits at
most 64 terms drawn from linear, quadratic, cubic, pairwise interaction, categorical indicator, and
category-conditional linear/quadratic/cubic bases. Terms may reference only the task's registered
feature IDs; evidence references may name only participant-visible assays. The production parser and
executor score the law directly, so prose that cannot be parsed does not silently receive a law score.

Terminal candidates are eight complete, compiler-valid ActionPlans selected from a registered
16-query public-feature roster without reading outcomes. Each packet declares every ordered operation
and parameter, fresh initial state, measurement positions, terminal assay, omitted optional operation,
and objective. The other eight rows form the disjoint prediction/oracle-fit roster. Public-plan,
truth-plan, and replay hashes must agree exactly. Candidate outcomes and evaluator ranks remain hidden
until scoring.

## Evaluator-owned prediction and law assays

Entity checkpoints contain four prespecified counterfactual queries; parametric and structural
checkpoints contain sixteen. The evaluator executes each unique task--world query independently, never
returns its truth to the participant, and shares truth across prior arms and checkpoints. The primary
readout is mean normalized absolute error across registered query--metric pairs. The executed cohort
contains 420/420 truth executions, 1,620 query--metric truth values, 675/675 checkpoints, 6,300
predictions, and 24,300 scored values.

Final typed laws are executed on the same registered coordinates. Schema validity, coordinate
coverage, truth-normalized error, change from pre-evidence and effective-final checkpoints, and
consistency with explicit final predictions are retained separately. This assay establishes
executability and in-domain compression only. Reusability would require new coordinates or transfer
to a context-reset process.

The matched GPT-5.6-sol evaluator uses the identical 45-cluster, nine-task, three-arm C2 surface.
DeepSeek-v4-flash and GPT-5.6-sol have 121/135 and 126/135 completed cells. Their exact evaluator
denominators are 675/675 versus 669/675 scored checkpoints, 135/135 versus 129/135 executable laws,
and 121/135 versus 126/135 cells with evaluable blind gain. Overall mean prediction improvement is
0.1198/0.1329, final prediction error is 0.1685/0.1614, law MAE is 0.2371/0.1753, law compression
loss is 0.0686/0.0142, and blind gain is -0.0010/-0.0001. GPT-minus-DeepSeek paired descriptive
differences are +0.0131 for prediction improvement, -0.0071 for final error, -0.0648 for law MAE,
and -0.0579 for compression loss. Both models fail all three registered selective-correction gates.

## Typed-law capacity and distillation controls

To distinguish participant compression failure from an underpowered output schema, we refitted each
of the 135 complete final prediction vectors with legal identity-link laws over the registered
feature coordinates and allowed basis functions. A full-basis fit used up to 64 terms per metric. A
term-matched fit used exactly the participant's submitted term budget for each metric. A
leave-one-query-out fit withheld each registered query in turn and predicted it from all remaining
queries. Every fitted law was parsed and executed by the production law evaluator; independently
computed design-matrix predictions had to agree with executor output within $10^{-10}$.

The participant laws differed from their own final predictions by mean MAE 0.1539. Full-basis fits
reproduced 135/135 final prediction states with mean MAE $4.25\times10^{-13}$; term-matched fits
reduced the error to 0.0114 and leave-one-query-out fits reached 0.0788. The control uses the same
registered coordinate domain and therefore tests representation capacity and distillation, not
global mechanistic identification or transfer.

## Failure-aware inference

The unit of prospective inference is the independently selected task--world cluster, not a checkpoint,
query, experiment, or replay. The three prior arms within a cluster are matched. Locus-specific
selective-correction contrasts are computed first and are not pooled across different intervention
semantics. Failed scientific cells remain assigned. Confirmatory correction bounds assign an
incomplete post-outcome the adverse improvement range $[-1,+1]$; last-observation-carried-forward and
zero improvement are observed-point sensitivities only. Infrastructure recovery is allowed only when
no scientific trajectory has persisted and only under the fixed attempt limit.

The matched-evidence B2 contrast has five independent worlds. Its interval and exact
one-sided sign-flip result are descriptive because the block was designed to localize a transition,
not to establish a population-level arm effect. Recipe divergence is likewise a manipulation check:
without repeated same-arm sessions, provider stochasticity cannot be separated from intervention
sensitivity at exact-recipe resolution.

DeepSeek and GPT-5.6-sol medium used identical matched-evidence worlds, arms, evidence packets,
queries, and scoring rules. Each completed 15/15 A-P and 15/15 A-S B2 formal sessions with no failed
cells; canaries were excluded. A-P misspecified-minus-aligned update contrasts were 0.0309 and
0.0602, with 3/5 and 5/5 positive worlds. A-S B2 contrasts were 0.0645 and 0.0915, with 3/5 and 4/5
positive worlds; misspecified exact 1.75-law expression was 0/5 in both models. Configurations are
reported separately, and no model-superiority test is performed.

The B2 exact-law counts are retrospective keyword coding of public `model_summary` and
`evidence_assessment` fields; no typed family or exponent field was preregistered. A later
participant-visible audit found that evidence and scoring fixed one nominal solvent/extractant pair,
did not expose the base partition coefficient, and admitted an exact alias between the 1.75-power law
and a free-coefficient linear law (coefficient multiplier 3.13588). A constant endpoint baseline
obtained mean scoring MAE 0.00649, while the aligned DeepSeek-high exact-law positive control was only
1/5 and failed its readout criterion. B2 therefore supports conditional low post-packet error and lack
of stable exact-law expression on an underidentifying surface, not a participant-level
structural-identification failure. The separate B3 control below supplies that identifiable test.

The reasoning-budget ablation kept the DeepSeek model, Codex harness, prompts, schemas, public
packets, worlds, and evaluator fixed while changing only `reasoning_effort` from high to low. It is
not provider-level thinking-off, which would require a different direct-controller harness. The B2
interface canary passed 3/3 and the formal block completed 15/15 sessions, 30/30 turns, 15/15
same-thread continuations, and 360/360 pre plus 360/360 post scoring terms, with no failed session or
infrastructure predecessor. Mean post errors were 0.0067/0.0069/0.0069 for
opaque/aligned/misspecified. The registered contrast was -0.0405, with 2/5 positive worlds, exact
one-sided $p=0.8125$, and descriptive interval [-0.1559, 0.0749]. Misspecified exact 1.75-law
expression remained 0/5; all five misspecified post errors were at most 0.02. Aligned exact-law
expression was 1/5 for DeepSeek high, 0/5 for GPT medium, and 2/5 for DeepSeek low, reinforcing that
the free-text expression readout itself lacks a strong positive control.

Provider-reported DeepSeek reasoning output was 506,637 tokens at high effort and 400,639 at low
effort on the matched B2 block, a 20.9\% reduction. These resource fields are descriptive within the
DeepSeek provider and are not compared with GPT accounting. The separate low-effort A-P canary was
platform-defective: progress events existed, but terminal cell receipts and a canary summary did not.
It is retained as an unscored partial; A-P low formal execution remained 0/15 and supplies no effect
estimate.

## Reference-fitter-identifiable law and action control

The independent B3 control used five frozen public structural-partition worlds, the same opaque,
aligned, and misspecified prior arms, and two independent fresh GPT-5.6-sol medium sessions per arm
and world. Provider-free development qualification selected eight evidence rows spanning four
nominal pairs and a disjoint eight-query scoring/action roster. Public truth was executed before any
participant call. All five worlds entered family, exponent, prediction, Top-1, rank, and regret
denominators; action gain was scored only in the three worlds whose best candidate exceeded the
visible evidence incumbent by at least 0.02. The evidence and scoring rosters, five worlds, three
arms, two replicates, 0.10 exponent tolerance, and 0.02 opportunity threshold were frozen before
participant execution.

A three-session canary tested only two-turn schema validity, packet identity, same-thread continuity,
typed law fields, the exact scoring denominator, and selection of an unexecuted candidate. It passed
3/3 and did not enter the formal scientific denominator. The full 30-cell block then completed
30/30 with no failed cells or replacement. All sessions preserved same-thread continuity and returned
60/60 completed formal turn receipts. The canary and formal blocks together used 33 provider session
attempts, 66/66 completed turn receipts, zero retries, zero tool events, and zero participant physical
experiments. One formal post turn recorded a transient provider error event before returning a
completed receipt; the event remains in the resource ledger and the cell remains completed.

Joint structural recovery required both the registered power family and exponent error at most 0.10.
Counts for opaque, aligned, and misspecified arms were 0/10, 5/10, and 0/10. The corresponding mean
post-evidence errors were 0.0367, 0.0215, and 0.0378. The aligned world-mean exponent error was lower
than each comparator in all five worlds. Top-1 counts were 0/10, 2/10, and 0/10; both Top-1 choices
came from one action-ineligible world. None of the 18 action-eligible cells reached gain 0.02,
including neither of the two action-eligible cells with joint structural recovery. A matched DeepSeek
B3 successor then started from its first cell on the same scientific surface and retained every
scheduled outcome. It completed 17/30 cells; 13/30 were participant-schema failures. Failure-aware
joint recovery was 0/30, Top-1 was 0/30, and mean regret was 0.9579; completed-cell post MAE was
0.0928. The corresponding GPT-5.6-sol values were 5/30, 2/30, 0.7594, and 0.0320. Useful-gain
success was 0/13 versus 0/18 among completed evaluable opportunities and 0/18 for both models on the
fixed scheduled-opportunity denominator, with failures and unavailable rows counted as zero. The
matched comparison is descriptive because model configuration was not randomized and schema-failure
patterns differed.

## Cross-model successor denominators

Historical stopped partials and stop boundaries remain immutable. They are not continued, pooled, or
converted into successful cells. Each successor instead starts at its first scheduled unit with a
complete failure-aware denominator.

The GPT-5.6-sol C2 successor scheduled all 135 task--world--prior cells and terminated with 126 completed,
3 failed, and 6 right-censored sessions, completing 1,253/1,260 participant experiments. Its
provider-free evaluator completed 420/420 truth executions, scored 669/675 checkpoints and 129/135
laws, and launched 756/810 scheduled blind executions; 54 remained unstarted. The matched 135-cell
DeepSeek/GPT analysis uses task--world cluster bootstrap intervals and never interprets model
differences as provider effects.

The DeepSeek B3 successor similarly schedules 30 cells and retains 17 completed plus 13
participant-schema failures. Its historical canary is excluded rather than spliced into the new
denominator. The GPT B3 cohort remains the independent completed 30-cell block described above.

The four-condition action successor schedules 45 strata by four conditions for each model: 180 slots
per model and 360 total. DeepSeek reuses 45 immutable autonomous donors, of which 42 are eligible;
GPT-5.6-sol creates a separate 45-donor cohort, of which 26 are eligible. No-evidence is scheduled for
all strata, while yoked and learned-law recipients require the corresponding donor. Missing-donor
descendants remain `not_started_due_to_missing_donor`. The primary analysis is the model-specific
all-scheduled failure-aware strategy estimand over all 45 strata. DeepSeek/GPT
autonomy-minus-no-evidence estimates are -0.0913 and +0.1102 with clustered intervals
[-0.2124, 0.0388] and [-0.0533, 0.2794]. Donor-eligible estimates (-0.1214/-0.1379) are
availability-conditioned sensitivities because eligibility is post-treatment; equal-task
sensitivities are -0.0879 for DeepSeek and -0.0259 for GPT. The cross-model common donor-eligible population contains 26 strata from 13
task--world clusters. Yoked completion is 10/42 for DeepSeek and 24/26 for GPT, so autonomous--yoked contrasts mix
scientific action quality with recipient-system failure and are not pure experiment-selection effects.
The autonomous-minus-no-evidence task estimates were -0.2398/-0.4060/+0.3720 for DeepSeek and
+0.0891/-0.2191/+0.4605 for GPT over electrochemistry/safety/crystallization, respectively. Thus the
pooled direction masks strong task heterogeneity. All four registered contrasts and their bootstrap
intervals are descriptive and were not multiplicity-adjusted. Conditions followed fixed manifest and
dependency order rather than randomization or counterbalancing; DeepSeek autonomous donors also
predated their recipients. Provider/time drift and condition-order effects are therefore not separable.

### Recovery and composite provenance

Platform repair never changed a scientific question, coverage set, metric, or gate after observing an
outcome. Affected blocks restarted from their first affected unit; discarded or superseded records
remain in the failure timeline and do not enter the current estimate.

```{=latex}
\begin{table}[h]
\caption{\textbf{Defect and recovery provenance for current publication surfaces.}}
\label{tab:provenance}
\centering
\scriptsize
\begin{tabularx}{\linewidth}{@{}lYYY@{}}
\toprule
Surface & Retained incident & Recovery boundary & Current inclusion \\
\midrule
DeepSeek C2 & one 15-cell shard affected by runtime/evaluator defects & whole shard restarted; evaluator rerun over the full composite & 120 unaffected cells plus one 15-cell replacement shard \\
GPT C2 & no inherited stopped cell & new 135-cell block from cell 1 & all 135 scheduled outcomes \\
DeepSeek B3 & historical three-cell canary failed schema & independent 30-cell successor from cell 1 & 17 complete plus 13 schema failures \\
Four-condition yoked & duplicate field deletion caused recipient KeyError & entire yoked condition restarted from its first admitted unit & recovered condition only; original failures retained in timeline \\
Oracle grids & path-length and evidence-reference limits & identical scientific block restarted after platform repair & only complete version-specific qualification blocks \\
\bottomrule
\end{tabularx}
\end{table}
```

The four-condition report remains a prospective development experiment rather than confirmatory evidence; the
reanalysis does not rename it formal evidence. The DeepSeek C2 current composite is reported as a
composite, not as one uninterrupted launch. Exact source bindings and excluded incident counts are in
the supplement.

## Complete-plan action assay

In each open-action cell, a persistent agent performs twelve autonomous experiments and commits
checkpoints after 0, 3, 6, 9, and 12 experiments. The host then reveals eight unseen ActionPlans. Each
plan specifies ordered operations, all submitted parameters, initial-state assumptions, intermediate
measurement positions, terminal assay, and declared omitted operations. Candidate outcomes, ranks,
and other-arm evidence stay hidden. The evaluator verifies identity of disclosed, truth-evaluated,
and replayed plans.

The primary endpoint is normalized regret of the selected plan within its task--world candidate set.
Selected rank, Top-1, pairwise ordering, and law adequacy are secondary or diagnostic. Forty-five
cells were scheduled across three tasks, five worlds, and three initial-model arms. Forty-two were
eligible. The two agent-induced resource/process failures and one provider interruption are retained
as failures in the scheduled denominator and are not replaced. An independent repair is reported only
as sensitivity evidence because it follows a new trajectory.

The continuous law--action analysis used only those same 42 originally eligible cells; the three
failures stayed in the 45-cell scheduled denominator and were not imputed. Pearson and Spearman
associations were computed pooled and by task. Uncertainty resampled the 15 frozen task--world
clusters, retaining all eligible arms within a sampled cluster, with 10,000 bootstrap replicates and
seed 20260827. The pooled Spearman coefficients were $-0.073$ for law MAE versus selected rank and
$-0.133$ for law MAE versus normalized regret, with cluster-bootstrap 95% intervals
$[-0.380,0.256]$ and $[-0.452,0.217]$. A prespecified sensitivity table swept law-MAE thresholds
0.05, 0.075, 0.10, 0.15, 0.20, 0.25, and 0.30 without selecting a cutoff from action outcomes.

A decision-aligned reanalysis used the last-available executable law from all 45 frozen
DeepSeek-v4-flash longitudinal cells and reconstructed the same eight candidate feature packets
without new participant, truth, or physics execution. Three cells had no terminal action ranking but
retained an earlier executable law. For each law,
truth-law error is the normalized regret of its implied Top-1. Action-utilization delta is participant
regret minus law-implied regret. All 45 laws executed; none implied the true Top-1, whereas participant
action selected Top-1 in 11/45 scheduled cells. Among 42 cells with a valid participant ranking, the
participant followed the law-implied Top-1 in 12. Mean law-implied and participant regret were 0.438
and 0.344. This is a descriptive decomposition: neither law quality nor law use was randomized.

## Oracle-control qualification

The unexecuted causal follow-up crossed three tasks, five worlds, three priors, and five conditions:
no evidence, stepwise yoked evidence, autonomous exploration, learned law in a fresh context, and a
provider-free oracle law. The planned denominator was 225 participant sessions, 45 autonomous donors,
and 540 donor experiments. Participant execution required every fresh task--world oracle to pass
candidate opportunity checks and to attain Spearman rank correlation at least 0.80 over the eight
candidate plans using fit data disjoint from candidate outcomes.

The 96-query qualification stopped after eight of fifteen clusters. It completed 896/896 truth
executions and exact replays, with eight candidate gates and seven oracle rank gates passing. The
retained crystallization failure had $\rho=0.738095$, Top-1 disagreement, and zero fit/candidate
overlap. No operational canary or participant session began.

This failure initiated a transparent development sequence rather than a retrospective threshold
change. Version 0.2 first failed on a fresh electrochemical world at $\rho=0.785714$. Version 0.3
added exact typed-law distillation but failed on a fresh crystallization world at $\rho=0.595238$.
Version 0.4 fixed an ExtraTrees predictor: it replayed all 25 exposed construction worlds successfully,
then stopped after five fresh units when the fifth reached only $\rho=0.785714$ (four pass, one fail,
ten unstarted). Each version used a newly held-out fresh surface, stopped at its first registered
failure, read no candidate outcomes during fitting, and made zero provider calls. These attempts are
not pooled into a success rate and do not modify the original stop decision.

The 320-query construction held the fitted ExtraTrees family fixed while expanding coverage to 64
global and 256 candidate-neighborhood queries. A platform-defective partial caused by an
evidence-reference schema limit was retained and not reused. After the contract repair, an independent
construction run completed 2,352/2,352 truth executions and replays across seven exposed units, passing all seven and
repairing four historical failures. The first prospective world then completed 336/336 executions and
replays but failed at $\rho=0.714286$; the remaining fourteen were not started. Candidate outcomes
were never read during fitting.

The gate-alignment analysis added no execution. It re-read sixteen frozen unit versions and exactly
reproduced their original Spearman and Top-1 values. Its action endpoints were Top-1, normalized
regret, selection within 0.01 of optimum, and near-tie-aware pair ordering. It did not alter any
historical result, threshold, or stop decision.

For eight candidates without ties, $\rho=1-\sum_i d_i^2/84$. Thus the retained 96-query failure at
$\rho=0.738095$ has $\sum_i d_i^2=22$, whereas the fresh 320-query failure at $\rho=0.714286$ has 24.
The scalar measures total displacement, not whether the best action moved.

```{=latex}
\begin{table}[h]
\caption{\textbf{Complete-ranking gates and action endpoints are different estimands.}}
\label{tab:alignment}
\centering
\small
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

## Additional scope boundaries

The study covers simulated chemistry and two fixed agent--tool configurations, not laboratory fidelity
or universal chemical coverage. C2 and B3 have matched scheduled surfaces; A-P/B2 have complete
separate denominators plus a B2-only DeepSeek-low ablation. Differential failures and non-random
provider assignment prohibit model ordering. The public cohort is not private confirmation, and
high-fidelity artifact portability remains untested. The autonomous open-action cohort lacks a
same-agent no-evidence baseline; the oracle-free successor adds four information strategies, but
donor/recipient failures limit mediation claims. The
original five-condition oracle cohort remains unexecuted.
