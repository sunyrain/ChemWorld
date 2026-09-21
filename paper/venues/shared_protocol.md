# Appendix A. Protocol detail and evidence handling

## A.1 Complete study matrix

| System / prior locus | Scientific commission | Budgets | Campaigns | Final-assayed batches |
|---|---|---:|---:|---:|
| EC / E: electrochemistry | Discovery; score optimization | 12, 24 | 60 | 1,080 / 1,080 |
| PA / E: phase partitioning | Explain phase allocation | 12, 24 | 30 | 540 / 540 |
| RX / P and S: reaction and thermal processing | Discovery; safety-constrained optimization | 12 | 60 | 720 / 720 |
| EQ / E: medium identity | Characterize entity-conditioned responses | 12 | 15 | 180 / 180 |
| EQ / P: bounded equilibrium | Characterize effective responses | 12 | 15 | 180 / 180 |
| EQ / S: structural equilibrium | Explain response structure | 12 | 15 | 180 / 180 |
| C / E: crystallization | Deliver crystals under quality constraints | 12, 24 | 30 | 539 / 540 |
| P / E: purification | Recover product subject to purity | 12 | 15 | 178 / 180 |
| **Total** | **Six system families** | | **240** | **3,597 / 3,600** |

Table A1. Complete selected study scope. Each campaign has one agent realization. One C
campaign exhausts its solvent stock and discards its twelfth vessel, completing eleven final assays. One P campaign uses all twelve vessel starts
but discards two vessels, leaving ten final assays. All campaigns have sealed mechanism,
prediction, and reflection stages; 238 meet the full source-and-assessment specification.

## A.2 Prediction targets and system-specific questions

| System | Prediction responses | Reference target | Interval level |
|---|---|---|---:|
| EC | Six conversion/efficiency responses, including score | Seeded final observation | 80% |
| PA | Organic and aqueous product fractions | Noiseless pre-sampling fractions | 90% |
| RX | Yield, conversion, selectivity, byproduct signal, risk, score | Five-observation mean; coverage over observations | 80% |
| EQ / E, P and S | Normalized pH, dissociation, precipitation signal | Five-observation mean; coverage over observations | 80% |
| C | Net recovery, purity, size index, fines fraction | Noiseless pre-assay responses | 80% |
| P | Purity, original-charge recovery | Seeded final observation | 80% |

Table A2. Every campaign predicts twelve conditions. PA fractions are complementary,
and its two decision questions reuse the conditions. Reference repeats reduce
observation noise but do not add agent sessions.



EC's twelve conditions balance positive and negative potential while varying duration,
materials, and current cap at a stated loading. Its six responses are selective
product yield, electrochemical selectivity, Faradaic efficiency, transport efficiency,
energy efficiency, and public score. Current is a magnitude cap, not guaranteed
delivered current. PA predicts phase fractions before analytical sampling; sampling
losses and complementary fractions must not be counted as separate discoveries.

RX's twelve paths examine time, temperature, catalyst, heating sequence, and quenching.
Actual thermal telemetry matters: requested boundary temperature need not be realized
reaction temperature. Five reference observations per condition are withheld from
agents, with all source assessments sealed before reference-truth release. RX's 600
reference executions are separate from 720 source batches and 60 retests.

Each EQ block uses twelve questions and five observations per question, giving 300
reference executions. EQ/E crosses three medium identities with three concentrations
and a matched-concentration scale control, assessing entity contrast and concentration
and scale transfer under a fixed common topology. Bounded EQ/P examines effective aqueous relationships; canonical
EQ/S supports response-shape analysis without requiring a named hidden family.
An instrument's equilibrium diagnostic is not the agent's subjective confidence.
The bounded study's effective-parameter supplement is additional to K1/Q/K2 and does
not confer discovery credit for a parameter already supplied as a treatment.

C's twelve conditions form six pairs: material, seed dose, cooling history, prior
thermal history, continued growth, and upstream loading. Its size response is
$\min(d_{50}/250\,\mu\mathrm m,1)$, a bounded number-weighted index rather than a
diameter in micrometres. Fines are particles below 20 micrometres. Quality requires
purity and fines criteria jointly, with particles present; recovery of 0.10 is an
initial feasibility target, not an optimization ceiling. P's six paired interventions
concern multistage recovery, including wash staging. Its original-charge denominator
differs from C's crystallization-stage recovery.

RX and EQ coverage uses individual reference observations while point targets use
means. EC and P use single seeded observations. PA and C prediction coverage concerns
noiseless pre-sampling responses; C recommendation retests use observed assays.
Apparent retest threshold crossings can therefore reflect noise. Macro errors weight a
system's responses equally; normalized scales do not make responses physically or
scientifically interchangeable.

## A.3 Language, numerical tools, and stage budgets

Source briefs and requested reports are English. EC/PA and C/P assessment instructions
are English; RX and EQ K1/Q/K2 instructions include Chinese text requesting English
reports. Within-block arms have the same language contract. Seven-theme K2 reviews
cover treatment claims, influential experiments, competing explanations, one proposed
discriminating experiment, goal-related tradeoffs, unused evidence and uncertainty,
and limitations of the recommendation or scientific account. Three-question versions
combine these themes. The reviews occur after source experiments and sealed
predictions; their length does not provide additional source experiments.

The earlier EC/PA block retains its saved eight-call diagnostic-calculator hard stop;
later blocks disclose 128-attempt assessment allowances. An old EC parameter/structural
supplement encountered the smaller limit and remains an execution failure outside
the primary E cohort. The repair is not retroactively attributed to older sessions.
Public calculation uses agent-accessible information, not hidden targets. Differences
in numerical budgets and deadlines are execution contracts, not scientific findings.

## A.4 Completion, recovery, and exclusions

The primary denominator is 240 scheduled campaigns, not provider attempts. All 720
K1/Q/K2 stages and 165 planned recommendation retests in EC, RX, C, and P are complete,
plus fifteen EQ supplements. Final-assayed source batches total 3,597 of 3,600 planned.
C's second-world 12-batch Opaque source has eleven final assays. P's fifth-world
Opaque source starts twelve vessels, discards two, and completes ten final assays.
Both remain in outcome tables with conformance indicators.

EC/PA has 68 first-attempt and 22 infrastructure-recovered campaigns. Recovery after
transport or host failures retains earlier attempts and consumed resources. Missing
assessment stages resume from saved context when the source is intact; fresh source
replacements are recorded as such. Repeated question delivery and failed-attempt
computation are not silently counted as an original clean attempt. EC goal sensitivity
is reported in the main text. First-attempt-only EC-discovery, EC-optimization, and
PA budget comparisons improve prediction in four of five, eight of eleven, and eight
of ten pairs, respectively; these reduced subsets have uneven coverage.

The current P matrix follows a correction of prepartition inventory handling. Affected
qualification and the entire agent block were restarted under the corrected contract;
earlier apparently successful cells were not selected into the new matrix. All
current source and recommendation trajectories pass inventory, resource, and replay
checks. Its two lawful discards are a source-assay shortfall, not an inventory failure.
The fixed purity-direction rule treats changes of 0.02 or less as small; a numerical
tolerance of $10^{-12}$ corrects floating-point equality handling. Six direction
classifications changed after this correction, with originals preserved. Predictions,
point errors, intervals, retests, and denominators were unchanged.

Historical single-world EC parameter/structural supplements, the closed-set EQ/S pilot,
early C/P development runs, qualification recipes, references, replays, and interrupted
attempts do not enlarge the denominator. Their records remain separate. Frozen platform
qualification is also a separate evidence programme. These counts describe execution
and analysis scope; they are not 240 independent chemistry replications.

## A.5 Baseline correction and trace interpretation

The C empirical references use the same source final observations for all three arms.
A recipe parser originally rejected resource-denial transaction records in two sources.
The correction preserves those attempts as provenance and excludes them from committed
physical recipe features. Recomputing all thirty baselines restores the two missing
evaluations and exactly reproduces the twenty-eight previously available results.
Original trajectories, truth, model answers, and error records are retained; the
correction uses no new simulator or provider calls. Unknown transaction statuses
remain errors. This is an evaluator repair, not a change to a completed experiment.

The EC illustrative trace is the second-world, 12-batch Opaque EC discovery campaign;
its sparse-positive-coverage counterexamples are first-world, 24-batch Aligned and
MisIndexed discovery campaigns. They are retrospectively selected examples, not a
coded prevalence estimate. The additional C case is the fifth-world, 12-batch
MisIndexed campaign, chosen as the largest purity MAE in the 12-batch cohort.
Its extreme error illustrates a failure; it is not a representative sampling rule.

A systematic analysis should attach each mechanistic claim to its experimental
support, contradictory observations, stated domain, and corresponding predictions.
It should distinguish an unperformed discriminating experiment, acquired evidence
omitted from an account, justified unresolved alternatives, and report-prediction
inconsistency. Evaluator knowledge helps identify discriminating interventions; a
claim is not wrong merely for using an equivalent representation. Independent review
can assist this analysis without replacing measured predictions and retests. No
completed cohort-wide mechanism score or causal compression experiment is implied.

## A.6 Full prior overview

![Prior information has no common ordering. Every panel includes five worlds and three arms: Opaque (O), Aligned (A), and MisIndexed (M). Gray lines connect worlds; colored bars show means. Crosses mark source shortfalls. RX and EQ use within-system macro errors; other panels name their response. Scales differ. Appendix B complements these selected readouts with all metric-specific arm means, including EQ/E.](../figures/integrated-results/priors.pdf){width=100%}
