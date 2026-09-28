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

Table A1. Cross-system study scope (GPT-5.6 Sol, medium). Each campaign has one agent realization. One C
campaign exhausts its solvent stock and discards its twelfth vessel, completing eleven final assays. One P campaign uses all twelve vessel starts
but discards two vessels, leaving ten final assays. All campaigns have scientific account (K1),
sealed prediction (Q), and retrospective review (K2) stages; 238 meet the full
source-and-assessment specification.

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
differs from C's seed-excluded recovery normalized by initial reagent loading.

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
computation are not silently counted as an original clean attempt. EC goal sensitivity is reported in Supplementary section E.5. First-attempt-only EC-discovery, EC-optimization, and
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

The earlier EC process illustration uses the second-world, 12-batch Opaque
discovery campaign; its sparse-positive-coverage counterexamples are first-world,
24-batch Aligned and MisIndexed discovery campaigns. These are distinct from the
current article's Figure 3, which pairs first-world, 12-batch Opaque discovery and
optimization campaigns (Supplementary E.6). All are retrospectively selected
examples, not a coded prevalence estimate. The additional C case is the fifth-world, 12-batch
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

![Supplementary Figure S1a–d. Full prior overview for electrochemistry across both goals and budgets. Each graphical table retains five worlds and all three information arms; the bottom row is the arm mean. Bar lengths and adjacent values show prediction MAE on the within-panel scale printed above. An x marks a source-assay shortfall. Scales differ between response types. Appendix B retains all response tables, including equilibrium entity priors.](../../figures/current-editable/figureS1-1.pdf)

![Supplementary Figure S1e–h. Full prior overview for partitioning and reaction discovery. Each graphical table retains five worlds and all three information arms; the bottom row is the arm mean. Bar lengths and adjacent values show prediction MAE on the within-panel scale printed above. An x marks a source-assay shortfall. Scales differ between response types. Appendix B retains all response tables, including equilibrium entity priors.](../../figures/current-editable/figureS1-2.pdf)

![Supplementary Figure S1i–l. Full prior overview for reaction optimization and equilibrium. Each graphical table retains five worlds and all three information arms; the bottom row is the arm mean. Bar lengths and adjacent values show prediction MAE on the within-panel scale printed above. An x marks a source-assay shortfall. Scales differ between response types. Appendix B retains all response tables, including equilibrium entity priors.](../../figures/current-editable/figureS1-3.pdf)

![Supplementary Figure S1m–p. Full prior overview for crystallization and purification. Each graphical table retains five worlds and all three information arms; the bottom row is the arm mean. Bar lengths and adjacent values show prediction MAE on the within-panel scale printed above. An x marks a source-assay shortfall. Scales differ between response types. Appendix B retains all response tables, including equilibrium entity priors.](../../figures/current-editable/figureS1-4.pdf)

## A.7 Prior effects by system and regime

![Supplementary Figure S2a,b. Reaction parameter-prior macro MAE differences from Opaque under discovery and optimization. Rows are matched worlds; Opaque absolute MAE is printed at left and only paired differences appear on the horizontal axis. Negative values mean lower error. Bottom marks show mean paired difference. Aligned improves in four of five worlds under each goal.](../../figures/current-editable/figureS2-ab.pdf)

![Supplementary Figure S2c–f. Equilibrium parameter-prior differences from Opaque on the remaining nine and three lowest-concentration queries. Panels c,d show macro MAE differences, where negative means lower error. Panels e,f show 80% interval coverage changes in percentage points, where positive means higher coverage. Opaque absolute values are printed separately from the difference axis. Response and regime scales differ. The grouping is post hoc.](../../figures/current-editable/figureS2-cf.pdf)

## A.8 Complete resource comparison

![Supplementary Figure S3. Complete budget effects across six readouts. Each panel retains fifteen pairs of independent sessions. Headers show campaign means and rows show paired changes. Positive changes favour the larger research envelope. Panels a–d show MAE at twelve minus MAE at 24 batches; e shows fines coverage at 24 minus coverage at twelve in percentage points; f shows retested recovery at 24 minus recovery at twelve. All fines coverage values remain below nominal 80%. Diamonds show mean changes; crosses retain source-assay shortfalls. Marks are point estimates without uncertainty intervals. World labels are system-specific. Scales differ except in a,b. Crystallization panels reuse campaigns; larger budgets also increase computational allowances.](../../figures/current-editable/figureS3.pdf)

![Supplementary Figure S4. Larger research envelopes affect responses differently. a–f show electrochemical discovery score MAE, electrochemical optimization score MAE, partitioning organic-fraction MAE, crystallization recovery MAE, crystallization fines interval coverage and crystallization retested recovery. Panel headers show campaign means at twelve and 24 batches and the number of improving world–arm pairs. Below are signed changes for all fifteen independent-session pairs; vertical offsets only separate overlapping marks. In a–d, change is twelve-batch MAE minus 24-batch MAE; in e,f, it is the 24-batch value minus the twelve-batch value. Positive values therefore always favour larger resources. Black diamonds show median paired change, grey marks at zero denote no change, and crosses retain the C-W02/Opaque source-assay shortfall. Axis scales differ. Larger batch budgets also permit more operations and computation. Supplementary Fig. S3 retains the detailed world–arm matrix for all six outcomes.](../../figures/narrative-final/figureS7.pdf)

## A.9 Supplementary platform and execution details

Platform validation. Frozen qualification passes 64 task–world units, 1,786 boundary and categorical recipes, 192 invalid-action probes and 52 generated compositions. Generated cases include eighteen previously absent topologies, eight new task–world identities using registered topologies and 26 additional coverage cases. Component and interface checks pass 32 module probes, seven interface paths and seven invalid-composition tests. These finite-domain checks establish internal consistency of models and execution, not agreement with arbitrary physical chemistry experiments. Exact environment replay reconstructs executed actions and resource consequences, including rejections and rollbacks. Subsequent study adapters are checked separately; frozen platform qualification does not automatically cover later execution code. Reference construction, assessment prompts and recovery differences are retained under each block's recorded protocol.

Case and statistical interpretation. The crystallization trajectory in Figure 2 and electrochemical pair in Figure 3 are retrospectively selected to illustrate actual research processes, not to estimate population frequencies of the corresponding behaviours. Crystallization batch 5 changes several process conditions, preventing isolation of the effect of omitting quench. Figure temperatures are requested targets, not measured thermal trajectories. The electrochemical comparison uses predictions sealed after two independent campaigns, without repeated prediction assessment after each optimization batch. Points in Figure 4a and Supplementary Fig. S8a come from different recipes and histories, not a controlled single-factor concentration–response curve. The source-observation band is not an uncertainty interval. There are no ties in the response-specific crystallization baseline comparisons.

Operations and infrastructure recovery. The four targeted model configurations retain 4,007 operation attempts, including 85 rejections or rollbacks. A Luna pre-action transport failure and an HTTP 503 during Astra's final supplemental questions were both recovered, with original failed attempts retained. The latter resumes only the original supplemental prompt in the original session, leaving source experiments and sealed predictions unchanged. Both are infrastructure events, not scientific failures.

Protocol history. Six World 1 pilot sessions for Luna, Terra and GPT-5.5 were inspected before matrix completion and remain unchanged; sensitivity comparisons therefore also use Worlds 2–5. All Astra sessions are new. Retained early electrochemical and partitioning assessments allow eight calculator calls; later blocks disclose allowances up to 128 attempts. All tasks request English output, but retained reaction and equilibrium assessment prompts contain Chinese instructions requesting English answers. These differences remain part of the historical protocol.

## A.10 Targeted equilibrium model comparison

The targeted comparison uses the same equilibrium parameter protocol, five worlds, three arms and twelve batches per campaign, with fifteen campaigns for each of four configurations. Each campaign permits at most 180 operation attempts, twelve intermediate measurements, twelve final assays, 0.24 mol reagent and 0.72 L solvent. Prompts, priors, queries, resources and scoring rules are fixed within the block, with one campaign per model–world–information condition. Some World 1 sessions were inspected as pilots; sensitivity analyses excluding that world are reported separately. Supplementary Methods specify the pilot scope.

The four targeted configurations complete 60/60 research chains, 720/720 batches, 240/240 original-session assessment stages and 2,160 scalar predictions, all with exact environment replay. They share 300 reference batches (five worlds × twelve queries × five observations), used only for evaluation. Supplementary Methods describe infrastructure recoveries and rejected operations.

# Appendix B. Complete metric-specific arm means

Each entry is mean absolute error / empirical interval coverage (%), averaged over five world sessions. All scheduled sessions are retained, including the two source-budget shortfalls. PA uses nominal 90% intervals; all other studies use 80%. Metric scales and reference targets differ across systems. The machine-readable table includes each campaign's interval width and protocol status. These tables cover the six-family Sol-medium study; the targeted model comparison is in Appendix F.

## EC, E prior: discovery, 12 batches

| Readout | Opaque | Aligned | MisIndexed |
|---|---:|---:|---:|
| Electrochemical selectivity | 0.2983 / 55.0 | 0.2740 / 65.0 | 0.1272 / 88.3 |
| Energy efficiency | 0.3098 / 33.3 | 0.2595 / 51.7 | 0.1582 / 63.3 |
| Faradaic efficiency | 0.2580 / 46.7 | 0.2259 / 60.0 | 0.1356 / 73.3 |
| Public score | 0.1953 / 51.7 | 0.1939 / 60.0 | 0.1321 / 71.7 |
| Selective product yield | 0.0731 / 60.0 | 0.0817 / 38.3 | 0.0598 / 56.7 |
| Transport efficiency | 0.2602 / 45.0 | 0.2184 / 66.7 | 0.1328 / 76.7 |

## EC, E prior: optimization, 12 batches

| Readout | Opaque | Aligned | MisIndexed |
|---|---:|---:|---:|
| Electrochemical selectivity | 0.2908 / 63.3 | 0.2378 / 66.7 | 0.2661 / 73.3 |
| Energy efficiency | 0.2794 / 43.3 | 0.2541 / 31.7 | 0.2440 / 55.0 |
| Faradaic efficiency | 0.2506 / 53.3 | 0.2532 / 31.7 | 0.2315 / 56.7 |
| Public score | 0.1947 / 55.0 | 0.1561 / 58.3 | 0.1835 / 53.3 |
| Selective product yield | 0.0758 / 43.3 | 0.0623 / 53.3 | 0.0762 / 50.0 |
| Transport efficiency | 0.2478 / 58.3 | 0.2053 / 51.7 | 0.2217 / 60.0 |

## PA, E prior: discovery, 12 batches

| Readout | Opaque | Aligned | MisIndexed |
|---|---:|---:|---:|
| Aqueous fraction | 0.0989 / 76.7 | 0.0712 / 80.0 | 0.0786 / 78.3 |
| Organic fraction | 0.0989 / 76.7 | 0.0712 / 80.0 | 0.0786 / 78.3 |

## EC, E prior: discovery, 24 batches

| Readout | Opaque | Aligned | MisIndexed |
|---|---:|---:|---:|
| Electrochemical selectivity | 0.1902 / 68.3 | 0.1268 / 80.0 | 0.0428 / 93.3 |
| Energy efficiency | 0.1581 / 61.7 | 0.1651 / 68.3 | 0.0945 / 80.0 |
| Faradaic efficiency | 0.1458 / 65.0 | 0.1505 / 66.7 | 0.0877 / 78.3 |
| Public score | 0.1201 / 63.3 | 0.1452 / 73.3 | 0.0713 / 78.3 |
| Selective product yield | 0.0726 / 53.3 | 0.0573 / 70.0 | 0.0374 / 75.0 |
| Transport efficiency | 0.1495 / 65.0 | 0.1501 / 66.7 | 0.0846 / 78.3 |

## EC, E prior: optimization, 24 batches

| Readout | Opaque | Aligned | MisIndexed |
|---|---:|---:|---:|
| Electrochemical selectivity | 0.1403 / 85.0 | 0.1252 / 85.0 | 0.0864 / 90.0 |
| Energy efficiency | 0.1977 / 48.3 | 0.1307 / 60.0 | 0.1779 / 65.0 |
| Faradaic efficiency | 0.1502 / 76.7 | 0.1098 / 78.3 | 0.1515 / 71.7 |
| Public score | 0.1113 / 75.0 | 0.0996 / 71.7 | 0.1136 / 75.0 |
| Selective product yield | 0.0515 / 75.0 | 0.0498 / 56.7 | 0.0587 / 58.3 |
| Transport efficiency | 0.1420 / 80.0 | 0.1257 / 73.3 | 0.1570 / 68.3 |

## PA, E prior: discovery, 24 batches

| Readout | Opaque | Aligned | MisIndexed |
|---|---:|---:|---:|
| Aqueous fraction | 0.0251 / 100.0 | 0.0296 / 96.7 | 0.0207 / 100.0 |
| Organic fraction | 0.0211 / 100.0 | 0.0296 / 96.7 | 0.0207 / 100.0 |

## RX, P prior: discovery, 12 batches

| Readout | Opaque | Aligned | MisIndexed |
|---|---:|---:|---:|
| Byproduct signal | 0.0800 / 88.7 | 0.0791 / 73.3 | 0.0710 / 81.0 |
| Conversion | 0.0426 / 72.7 | 0.0321 / 70.0 | 0.0306 / 73.3 |
| Safety risk | 0.1031 / 58.3 | 0.0282 / 85.0 | 0.0370 / 81.7 |
| Public score | 0.1195 / 48.7 | 0.0501 / 83.3 | 0.0476 / 90.3 |
| Selectivity | 0.1198 / 58.0 | 0.0818 / 69.3 | 0.0714 / 77.3 |
| Yield | 0.1461 / 35.7 | 0.0708 / 76.7 | 0.0698 / 78.3 |

## RX, P prior: optimization, 12 batches

| Readout | Opaque | Aligned | MisIndexed |
|---|---:|---:|---:|
| Byproduct signal | 0.1509 / 57.7 | 0.0805 / 73.0 | 0.1271 / 60.3 |
| Conversion | 0.0474 / 85.3 | 0.0319 / 82.7 | 0.1960 / 53.0 |
| Safety risk | 0.0984 / 56.7 | 0.1106 / 56.7 | 0.0811 / 68.3 |
| Public score | 0.1341 / 30.0 | 0.0818 / 73.0 | 0.0879 / 68.3 |
| Selectivity | 0.1900 / 31.0 | 0.0923 / 69.7 | 0.1360 / 64.7 |
| Yield | 0.2128 / 19.3 | 0.1060 / 65.7 | 0.1499 / 68.7 |

## RX, S prior: discovery, 12 batches

| Readout | Opaque | Aligned | MisIndexed |
|---|---:|---:|---:|
| Byproduct signal | 0.1219 / 78.7 | 0.1212 / 75.3 | 0.1279 / 64.7 |
| Conversion | 0.0217 / 97.7 | 0.0266 / 95.3 | 0.0200 / 98.0 |
| Safety risk | 0.0664 / 80.0 | 0.0717 / 66.7 | 0.1276 / 43.3 |
| Public score | 0.0504 / 89.7 | 0.0816 / 61.3 | 0.0665 / 78.0 |
| Selectivity | 0.1280 / 72.7 | 0.1319 / 70.7 | 0.1400 / 55.0 |
| Yield | 0.1157 / 81.7 | 0.1196 / 75.7 | 0.1275 / 61.0 |

## RX, S prior: optimization, 12 batches

| Readout | Opaque | Aligned | MisIndexed |
|---|---:|---:|---:|
| Byproduct signal | 0.1376 / 63.7 | 0.1490 / 67.7 | 0.1188 / 66.3 |
| Conversion | 0.0370 / 88.7 | 0.0505 / 82.7 | 0.0425 / 88.3 |
| Safety risk | 0.1000 / 45.0 | 0.1255 / 68.3 | 0.1133 / 45.0 |
| Public score | 0.0932 / 56.0 | 0.0917 / 58.0 | 0.0637 / 81.0 |
| Selectivity | 0.1574 / 56.7 | 0.1570 / 60.3 | 0.1175 / 62.3 |
| Yield | 0.1485 / 63.3 | 0.1422 / 66.3 | 0.0975 / 73.0 |

## EQ, P prior: characterization, 12 batches

| Readout | Opaque | Aligned | MisIndexed |
|---|---:|---:|---:|
| Dissociation fraction | 0.0129 / 96.3 | 0.0759 / 68.7 | 0.0646 / 74.7 |
| Normalized pH | 0.0031 / 94.3 | 0.0160 / 65.0 | 0.0150 / 68.7 |
| Precipitation signal | 0.0205 / 83.3 | 0.0376 / 73.3 | 0.0383 / 68.7 |

## EQ, S prior: characterization, 12 batches

| Readout | Opaque | Aligned | MisIndexed |
|---|---:|---:|---:|
| Dissociation fraction | 0.0292 / 91.7 | 0.0235 / 76.3 | 0.0122 / 87.7 |
| Normalized pH | 0.0097 / 87.3 | 0.0200 / 75.7 | 0.0203 / 77.7 |
| Precipitation signal | 0.0033 / 95.3 | 0.0042 / 95.7 | 0.0078 / 87.3 |

## EQ, E prior: characterization, 12 batches

| Readout | Opaque | Aligned | MisIndexed |
|---|---:|---:|---:|
| Dissociation fraction | 0.0128 / 83.7 | 0.0107 / 85.0 | 0.0134 / 79.0 |
| Normalized pH | 0.0233 / 80.7 | 0.0278 / 79.0 | 0.0202 / 82.0 |
| Precipitation signal | 0.0084 / 89.3 | 0.0116 / 92.0 | 0.0103 / 88.3 |

## C, E prior: delivery, 12 batches

| Readout | Opaque | Aligned | MisIndexed |
|---|---:|---:|---:|
| Fines fraction | 0.3279 / 25.0 | 0.3096 / 38.3 | 0.2925 / 43.3 |
| Crystal purity | 0.0095 / 98.3 | 0.0497 / 60.0 | 0.0917 / 23.3 |
| Particle-size index | 0.0777 / 55.0 | 0.0624 / 58.3 | 0.0725 / 58.3 |
| Net crystal recovery | 0.1632 / 48.3 | 0.0606 / 83.3 | 0.0892 / 71.7 |

## C, E prior: delivery, 24 batches

| Readout | Opaque | Aligned | MisIndexed |
|---|---:|---:|---:|
| Fines fraction | 0.2281 / 51.7 | 0.2774 / 38.3 | 0.3046 / 41.7 |
| Crystal purity | 0.0197 / 95.0 | 0.0398 / 73.3 | 0.0508 / 55.0 |
| Particle-size index | 0.0566 / 71.7 | 0.0440 / 70.0 | 0.1023 / 48.3 |
| Net crystal recovery | 0.0911 / 61.7 | 0.0684 / 80.0 | 0.0786 / 73.3 |

## P, E prior: delivery, 12 batches

| Readout | Opaque | Aligned | MisIndexed |
|---|---:|---:|---:|
| Purity | 0.2240 / 51.7 | 0.1883 / 53.3 | 0.2508 / 50.0 |
| Recovery | 0.0668 / 56.7 | 0.0687 / 51.7 | 0.0727 / 53.3 |

# Appendix C. Exploratory analyses of response regimes

These analyses use the retained source campaigns and their original predictions. They
do not define new experimental arms or alter the withheld-condition bank. The
concentration grouping, joint crystallization contrast and illustrative traces were
selected after the experiments, and are descriptive analyses of reused worlds.

## C.1 Equilibrium: a reversal across public concentration regimes

The three most dilute recipes have nominal concentrations approximately
$1.33\times10^{-4}$, $1.33\times10^{-5}$ and $1.67\times10^{-4}$ M. Each campaign
has three normalized responses for each recipe. Point errors use five-observation
means; interval coverage uses the individual reference observations. Group means
average the corresponding responses and queries and then the five world campaigns.
Weighting the two groups 3:9 reconstructs every original twelve-question campaign
macro MAE. The other nine queries include boundary conditions; this split is not
a predeclared interpolation-versus-extrapolation test.

| Query group / arm | Macro MAE | Coverage (%) | Interval width | Source-mean MAE |
|---|---:|---:|---:|---:|
| Other nine / Opaque | 0.01008 | 90.7 | 0.04706 | 0.00553 |
| Other nine / Aligned | 0.00465 | 91.3 | 0.03340 | 0.00518 |
| Other nine / MisIndexed | 0.00439 | 89.6 | 0.02798 | 0.00494 |
| Three most dilute / Opaque | 0.01833 | 93.3 | 0.15676 | 0.16961 |
| Three most dilute / Aligned | 0.15862 | 2.2 | 0.08084 | 0.16833 |
| Three most dilute / MisIndexed | 0.14397 | 13.8 | 0.09633 | 0.16836 |

Table C1. EQ/P subgroup results. Each row averages five worlds; rows reuse those worlds.
The source-mean predictor is an additional post hoc diagnostic and obtains no new
experiments. Its poor dilute-query performance shows why retaining the plateau is
insufficient; its usefulness on the other nine depends on their response distribution.

Aligned improves on the other nine and worsens on the dilute three relative to
Opaque in all five worlds. All fifteen source campaigns remain above 0.018 M.
In the selected second-world comparison, Aligned spans about ninety-fold source
concentration variation and Opaque about fourfold, but both remain in the observed
plateau. At the most dilute question, reference dissociation is 0.65463;
Opaque predicts 0.629 [0.45, 0.80] and Aligned 0.0804 [0.053, 0.108].
The Opaque prediction response develops an unsaturated weak-acid extrapolation beyond
its sealed report. This reasoning must not be credited retrospectively to K1 or to
an earlier source-stage hypothesis.

## C.2 Crystallization: joint response changes under the same treatment

| Budget / arm | Recovery MAE | Purity MAE | Recovery improves and purity worsens vs Opaque |
|---|---:|---:|---:|
| 12 / Opaque | 0.16322 | 0.00952 | Reference |
| 12 / Aligned | 0.06055 | 0.04969 | 5 / 5 worlds |
| 12 / MisIndexed | 0.08923 | 0.09166 | 5 / 5 worlds |
| 24 / Opaque | 0.09107 | 0.01975 | Reference |
| 24 / Aligned | 0.06839 | 0.03983 | 2 / 5 worlds |
| 24 / MisIndexed | 0.07863 | 0.05080 | 3 / 5 worlds |

Table C2. Joint directional comparisons use both response errors from the same
world, arm and budget. At twelve batches, each joint direction also holds in all
four pairs whose two campaigns conform to the source-assay contract. The direction
weakens at 24 batches. A treatment can therefore be helpful on one response and
harmful on another without implying a budget-invariant tradeoff.

## C.3 Evidence status and interpretation

The same-source C references use only each campaign's final assays and public
recipe features. They exclude hidden truth during fitting but do not reproduce
the agent's complete intermediate measurements, prior or computational policy.
Low held-out purity variation makes the mean a particularly strong reference.
Neither its success nor the agent's recovery advantage is a complete mechanism
identification result.

Selected EC and C traces support detailed examples rather than population
frequencies; the bounded EQ review below covers all fifteen campaigns in that block.
The current evidence does not causally identify prior anchoring,
report compression, acquisition-versus-inference mediation or a general preference
for familiar chemistry. Full-history Q also prevents interpreting K1 as the sole
information channel. Experimental selection and later interpretation are both part of
the original autonomous process. Their separate causal contributions are not required
to describe the observed whole-process contrasts and have not been identified here.

## C.4 Original equilibrium campaigns: predictions and research chronology

We reviewed all fifteen retained Sol parameter-prior equilibrium campaigns, comprising
180 batches, 945 operations and 45 K1/Q/K2 stages. Each row below is an original
autonomous research session, not an independent reader of its records. The selected
question uses 1 micromole in 75 mL; the same question and original reference targets
apply to all three arms in a world. The reference column is the five-observation mean.

| World / arm | Public Q explanation | Dissociation [80% interval] | Reference |
|---|---|---:|---:|
| 1 / Opaque | Piecewise weak acid | 0.6990 [0.250, 0.900] | 0.7160 |
| 1 / Aligned | Plateau / weak trend | 0.1040 [0.044, 0.225] | 0.7160 |
| 1 / MisIndexed | Plateau / weak trend | 0.1092 [0.0772, 0.1412] | 0.7160 |
| 2 / Opaque | Piecewise weak acid | 0.6290 [0.450, 0.800] | 0.6546 |
| 2 / Aligned | Plateau / weak trend | 0.0804 [0.053, 0.108] | 0.6546 |
| 2 / MisIndexed | Plateau / weak trend | 0.0806 [0.0556, 0.1056] | 0.6546 |
| 3 / Opaque | Piecewise weak acid | 0.5630 [0.430, 0.700] | 0.5797 |
| 3 / Aligned | Plateau / weak trend | 0.1100 [0.045, 0.190] | 0.5797 |
| 3 / MisIndexed | Mixed weak acid / plateau | 0.4600 [0.100, 0.750] | 0.5797 |
| 4 / Opaque | Qualitative departure | 0.5200 [0.150, 0.880] | 0.5173 |
| 4 / Aligned | Plateau / weak trend | 0.0724 [0.040, 0.105] | 0.5173 |
| 4 / MisIndexed | Plateau / weak trend | 0.0962 [0.040, 0.450] | 0.5173 |
| 5 / Opaque | Piecewise weak acid | 0.4130 [0.200, 0.700] | 0.4480 |
| 5 / Aligned | Plateau / weak trend | 0.0790 [0.035, 0.130] | 0.4480 |
| 5 / MisIndexed | Plateau / weak trend | 0.0681 [0.040, 0.096] | 0.4480 |

Table C3. Public extrapolation accounts and original same-context predictions.
Categories are a single-author retrospective reading of public explanations, not
internal reasoning traces or independent causal labels. Four Opaque accounts use
piecewise weak-acid reasoning; the fifth permits a qualitative departure. All five
Aligned accounts extend a plateau or weak trend. The third-world MisIndexed mixed
account is a counterexample to treating all dossier conditions alike.

The first-world Opaque K1 already estimates an effective acid constant near
$2.2\times10^{-5}$ and an active-pool cap near 0.004 M, while retaining competing
interpretations. Its Q applies that hypothesis at low concentration. In the
second world, Opaque K1 primarily supports the observed plateau and limits
extrapolation; the unsaturated weak-acid calculation is first explicit in Q.
The aligned K1 similarly limits its account to the sampled region, but its Q
interval still misses the dilute response by a large margin. These differences
separate what was stated before prediction from what became explicit during it.

All fifteen source concentration ranges lie above the three dilute test recipes.
The exported per-operation decision-reason fields are unavailable for all 945
operations. Actions and observations can therefore be reconstructed, but a
contemporaneous sequence of belief revisions cannot be inferred from these fields.
K1, Q and K2 remain distinct public records rather than substitutes for that sequence.

In K2, eleven of fifteen campaigns propose a trace-load experiment: five Opaque,
three Aligned and three MisIndexed. The other choices are equal-concentration
scale-up, dilution near the supplied relation, comparison of instruments at the
same state and repetition of an anomalous batch. K2 follows exposure to Q conditions
without feedback on their reference outcomes. None of these proposals was executed;
they are retrospective choices, not source-stage plans or demonstrated repairs.

# Appendix D. Selected autonomous research histories

Figure 2 follows one retrospectively selected, twelve-batch MisIndexed crystallization session through a complete series of experiments and its selected operating procedure. Supplementary Fig. S5 presents a separate W05 Aligned 12/24-batch pair and its withheld thermal question. Neither selection estimates a cohort-wide effect; the matched budget comparison is in Supplementary Fig. S4.

## D.1 Complete twelve-batch research path and recommendation

Figure 2 retains all twelve source results in the W04 MisIndexed session. The first four batches have 99.5–100.0% fines and fail the 50% limit. Batch 5 is the first feasible result (40.0% recovery, 30.3% fines) after omitting quench and cooling towards 325 K before seeding. Catalyst, heating, seed and cooling conditions also differ from the early batches; this comparison does not identify a separate quench effect. In the subsequent process family, batches 5–7 end at 275, 265 and 250 K, with recovery 40.0%, 42.8% and 45.0%, respectively. Batch 8 reduces seed from 5 to 1 mg and gives 45.5% recovery and 25.4% fines. Batches 9–10 probe seed omission and longer holding. Batch 11 halves S2 from 0.080 to 0.040 L but yields 44.6% recovery and 72.6% fines, violating quality. Batch 12 repeats the batch-8 recipe and remains feasible (44.1% recovery, 26.9% fines). The exact numerical optimum is less secure than the repeated feasibility of this operating region.

The agent sealed batch 8 as its recommendation. Its source final assay reported 45.5% seed-excluded recovery, 98.2% purity and 25.4% fines; independent retest reported 43.9%, 98.7% and 28.4%, respectively. The recipe charges 0.040 mol reagent, 0.080 L S2 and 0.005 mol C1; heats towards 355 K for 3,600 s at 300 rpm; cools towards 325 K over 7,200 s; adds 1 mg seed; cools towards 250 K over 14,400 s; holds for 14,400 s at 100 rpm; measures particle size, filters, terminates and assays. In this environment, quench stops reaction chemistry while subsequent cooling and crystal growth remain possible. Heating and cooling values are requested targets, not measured temperature trajectories.

The source trajectory records operations and observations but no contemporaneous verbal rationale for each batch. Figure 2c therefore labels decision questions as author reconstructions. K1 was written after all twelve experiments. It interpreted the contrast between quenched and controlled-cooling batches as evidence for nucleation-history dependence while acknowledging that multiple recipe variables changed; the mechanism is plausible but not isolated by this campaign. K2 later identified the confound explicitly. No new experiment was run to distinguish quench from the other changes.

## D.2 Sealed predictions and subsequent reflection

Figure S5 follows a separate W05 Aligned pair of independent 12- and 24-batch sessions through sealed prediction and subsequent reflection; the proposed experiment was not executed. In the 24-batch session, the first nineteen batches fail the fines limit, batch 20 first meets it, and batch 23 is selected. The 12-batch session first meets the quality rule at batch 1. These paths and their Q/K2 assessments do not belong to Figure 2's W04 session and are not a matched quench test.

![Supplementary Figure S5. Sealed predictions and subsequent reflection in a W05 crystallization pair separate from Figure 2. A, The independent twelve- and twenty-four-batch source histories: the twelve-batch session first meets the fines rule at batch 1; the twenty-four-batch session first meets it at batch 20 and selects batch 23. B, The same withheld question in both sessions replaces a two-hour hold at 278.15 K with heating towards 315 K for one hour and recooling for one hour after a common preceding recipe. Both sealed Q answers predict fewer fines (17% to 12% at twelve batches; 49% to 35% at twenty-four batches). Thermal profiles show requested targets schematically. C, Condensed public K2 answers follow Q without reference feedback. The twenty-four-batch session proposes changing only the cooling procedure of its selected batch; this experiment was not executed. D, The evaluator's reference is for the thermal intervention in B, not the proposal in C. It was unavailable during Q and K2 and gives the opposite fines direction.](../../figures/narrative-final/figureS4.pdf)

# Appendix E. Supporting outcomes and examples

## E.1 Quality constraints and response-specific references

Purification gives a related distinction between recovery and acceptable delivery. Aligned recommendations meet the purity threshold in three of five worlds, compared with none for Opaque or MisIndexed. Yet mean recovered fractions are 0.04455, 0.12373 and 0.32105 for Aligned, Opaque and MisIndexed, respectively. Recovering more material therefore does not imply satisfying the commission. A single retest near the purity threshold is also not a precise estimate of a procedure's reliability. These system-specific outcomes cannot be represented faithfully by a universal yield score (Fig. S6a).

Purification provides another response-specific example: fourteen of fifteen campaigns correctly judge a small concentration effect on purity, but only two correctly judge the small purity effect of splitting a wash. Recognizing approximate invariance is itself a predictive achievement, and depends on the intervention.

In crystallization, agent size forecasts have lower MAE than the source mean in four of thirty campaigns and fines forecasts in twenty-one (Fig. S6b,c). Together with the recovery and purity contrasts in the main text, these results retain the complete response-specific comparison.

![Supplementary Figure S6. Additional operational and predictive outcomes. a, All fifteen purification recommendations, showing original-charge recovery and independently retested purity. The line marks the purity threshold of 0.80; eligible counts are 0/5, 3/5 and 0/5 for Opaque, Aligned and MisIndexed. b,c, Size and fines MAE for all thirty crystallization campaigns relative to each campaign's public observation mean. Points above the diagonal favour the mean; the campaign with a source-assay shortfall remains included. These panels use different response scales.](../../figures/current-editable/figureS5.pdf)

## E.2 Additional selected examples

In a selected Aligned phase-partitioning campaign pair, the larger budget covers all sixteen material pairings and then allocates eight experiments to process variation; the smaller campaign covers ten pairings. This is a plausible route to improvement, not a cohort-wide causal explanation. Two Aligned world pairs nevertheless worsen.

Uncertainty is part of the same applicability problem. The poor dilute-equilibrium coverage shows that a wrong extrapolation can also be overconfident. In a retrospectively selected MisIndexed crystallization campaign, the scientific account (K1) explicitly acknowledges that only one solvent was tested. Nevertheless, predicted purity averages 0.86833 against a reference mean of 0.98566, and all twelve nominal 80% intervals miss. A verbal statement of uncertainty does not by itself ensure calibrated quantitative prediction.

## E.3 Complete crystallization baseline and interval comparisons

Figure 6b reports how often each response is predicted more accurately than the public observation mean. Table E1 supplies the corresponding error magnitudes and the public nearest-neighbour comparison. Each baseline is fitted separately to the same campaign's public final assays; neither receives withheld outcomes or additional experiments. Nearest-neighbour prediction also uses public recipe features. These are empirical references rather than strong system-identification baselines.

**Table E1. Crystallization prediction errors and baseline comparisons.**

| Response | Agent MAE | Mean MAE | Nearest MAE | Wins: mean | Wins: nearest |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Recovery | 0.09185 | 0.17135 | 0.17308 | 26/30 | 26/30 |
| Purity | 0.04354 | 0.00482 | 0.00905 | 0/30 | 4/30 |
| Size index | 0.06923 | 0.02345 | 0.02708 | 4/30 | 7/30 |
| Fines fraction | 0.29000 | 0.31651 | 0.32426 | 21/30 | 20/30 |

MAE is averaged equally over all thirty campaigns in each response's original scale; errors are not ranked across responses. Recovery, purity and fines are fractions, while size is the declared size index. Mean and Nearest denote the public observation-mean and nearest-neighbour predictors. Wins count strictly lower agent MAE; neither comparison has ties. The source-assay shortfall remains included, and the five world instances are reused across arms and independent budget sessions.

Table E2 accompanies the purity coverage comparison in Figure 6d. Wider intervals need not cover a biased prediction's reference, while coverage exceeding the nominal level does not by itself establish calibration or sharpness.

**Table E2. Purity interval coverage and width by information arm and budget.**

| Budget | Information arm | Campaigns | Coverage (%) | Mean width (pp) |
| ---: | :--- | ---: | ---: | ---: |
| 12 | Opaque | 5 | 98.3 | 6.81 |
| 12 | Aligned | 5 | 60.0 | 12.94 |
| 12 | MisIndexed | 5 | 23.3 | 15.53 |
| 24 | Opaque | 5 | 95.0 | 8.59 |
| 24 | Aligned | 5 | 73.3 | 12.37 |
| 24 | MisIndexed | 5 | 55.0 | 12.31 |

The original intervals have nominal 80% coverage and concern the pre-final-assay response target. Coverage and interval width are averaged over each campaign's twelve queries and then over its five-world arm-budget group. Each row contains sixty query targets but only five world clusters; queries are not independent world replicates. Width is expressed in percentage points of purity. All original intervals and source failures remain unchanged.

## E.4 Complete research-objective comparison

Figure 3 uses 120 campaigns and sixty original goal pairs. Each pair fixes world, information arm, budget and prior locus. EC has five worlds, three arms and two budgets at the entity locus; RX has five worlds, three arms and two loci at twelve batches. The independent recommendation retest and twelve-query score MAE are separate endpoints. EC references are single seeded observations; RX point references are five-observation means. No new campaigns or predictions were produced for this analysis.

**Table E3. All joint goal outcomes.**

| Higher retest | Lower score MAE | EC pairs | RX pairs |
| --- | --- | --- | --- |
| Optimization | Optimization | 13 | 4 |
| Optimization | Discovery | 13 | 5 |
| Discovery | Optimization | 1 | 4 |
| Discovery | Discovery | 3 | 17 |

Both endpoints favour the same campaign in 16/30 EC and 21/30 RX pairs, and opposite campaigns in 14/30 and 9/30. Strict signs define these descriptive counts; near-zero differences are not thereby significant. Each system reuses five worlds. RX score MAE favours optimization in 8/30 pairs; its separate six-response macro MAE does so in 6/30.

![Supplementary Figure S7. World-level summaries of the same goal comparison. a,b, Electrochemical recommendation retests and score-prediction MAE. c,d, Reaction-processing endpoints. Each bar averages six campaigns per goal within a world. World labels are system-specific; bar means do not replace the individual paired differences in Figure 3. Scales differ across panels.](../../figures/current-editable/figureS6.pdf)

## E.5 Strata and recovery sensitivity

**Table E4. Endpoint orderings within design strata.**

| System | Factor | Level | Pairs | Same | Opposite |
| --- | --- | --- | --- | --- | --- |
| EC | World | W01 | 6 | 3 | 3 |
| EC | World | W02 | 6 | 4 | 2 |
| EC | World | W03 | 6 | 3 | 3 |
| EC | World | W04 | 6 | 5 | 1 |
| EC | World | W05 | 6 | 1 | 5 |
| EC | Budget | 12 | 15 | 7 | 8 |
| EC | Budget | 24 | 15 | 9 | 6 |
| EC | Arm | Aligned | 10 | 6 | 4 |
| EC | Arm | MisIndexed | 10 | 5 | 5 |
| EC | Arm | Opaque | 10 | 5 | 5 |
| EC | Locus | E | 30 | 16 | 14 |
| RX | World | W01 | 6 | 4 | 2 |
| RX | World | W02 | 6 | 4 | 2 |
| RX | World | W03 | 6 | 3 | 3 |
| RX | World | W04 | 6 | 4 | 2 |
| RX | World | W05 | 6 | 6 | 0 |
| RX | Budget | 12 | 30 | 21 | 9 |
| RX | Arm | Aligned | 10 | 6 | 4 |
| RX | Arm | MisIndexed | 10 | 9 | 1 |
| RX | Arm | Opaque | 10 | 6 | 4 |
| RX | Locus | P | 15 | 12 | 3 |
| RX | Locus | S | 15 | 9 | 6 |

Same means that the higher-retest campaign also has lower MAE; opposite means it has higher MAE. These overlapping strata do not add independent tests. Budget rows compare goals at a fixed budget, not a twelve-to-twenty-four-batch contrast. E denotes entity priors, P parameter priors and S structural priors.

The EC subset with neither campaign having a recorded recovery contains seventeen pairs: ten have the same ordering and seven the opposite ordering. Optimization has higher retests in fifteen and lower MAE in eight. This subset excludes assessment-only recovery as well as source recovery; it has uneven coverage and does not replace the full cohort.

## E.6 All batches of the selected electrochemical pair

The illustration uses one retrospectively selected twelve-batch Opaque pair in the first electrochemical world. It is not an additional replication or a random sample. Both original agents retain their research context for the later assessments. Every batch uses 0.020 mol in 0.040 L; current denotes the configured cap.

**Table E5. Discovery source batches.**

| Batch | Pair | V | mA | Electrolysis / s | Score |
| --- | --- | --- | --- | --- | --- |
| 1 | S0/E0 | -1.5 | 100 | 1200 | 0.000000 |
| 2 | S1/E0 | -1.5 | 100 | 1200 | 0.167530 |
| 3 | S2/E0 | -1.5 | 100 | 1200 | 0.000000 |
| 4 | S3/E0 | -1.5 | 100 | 1200 | 0.050903 |
| 5 | S0/E0 | 0.5 | 100 | 1200 | 0.509008 |
| 6 | S0/E0 | 1.5 | 100 | 1200 | 0.044293 |
| 7 | S0/E0 | 2.5 | 100 | 1200 | 0.030644 |
| 8 | S0/E1 | 0.5 | 100 | 1200 | 0.000000 |
| 9 | S0/E2 | 0.5 | 100 | 1200 | 0.482517 |
| 10 | S0/E3 | 0.5 | 100 | 1200 | 0.360679 |
| 11 | S0/E2 | 0.5 | 100 | 1200+13200 | 0.606942 |
| 12 | S0/E2 | 0.5 | 500 | 1200+13200 | 0.710658 |

**Table E6. Optimization source batches.**

| Batch | Pair | V | mA | Electrolysis / s | Score |
| --- | --- | --- | --- | --- | --- |
| 1 | S0/E0 | 1 | 100 | 3600 | 0.535704 |
| 2 | S1/E1 | -1.5 | 300 | 7200 | 0.282124 |
| 3 | S2/E2 | 1.5 | 300 | 7200 | 0.674932 |
| 4 | S3/E3 | 1.5 | 300 | 7200 | 0.313717 |
| 5 | S2/E0 | 1.5 | 300 | 7200 | 0.033808 |
| 6 | S0/E2 | 1.5 | 300 | 7200 | 0.042443 |
| 7 | S2/E2 | 1 | 300 | 7200 | 0.570485 |
| 8 | S2/E2 | 2 | 300 | 7200 | 0.000000 |
| 9 | S2/E2 | 1.5 | 500 | 7200 | 0.722737 |
| 10 | S2/E2 | 1.5 | 500 | 10000 | 0.731956 |
| 11 | S2/E2 | 1.4 | 500 | 9000 | 0.714786 |
| 12 | S2/E2 | 1.5 | 400 | 12000 | 0.749194 |

Both campaigns select batch 12. Independent retests are 0.717587 for discovery and 0.756122 for optimization; twelve-query score MAEs are 0.088394 and 0.229397.

## E.7 Operation sequence and subsequent public accounts

All batches add reagent, add solvent, set potential/electrolyte/current, electrolyze, measure UV-visible response, terminate and obtain a final assay, in that order. Discovery batches 11 and 12 insert a second 13,200-s electrolysis after the first 1,200-s electrolysis and its UV-visible measurement. Their 14,400-s totals therefore do not describe one uninterrupted operation. The records contain 86 discovery and 84 optimization operations. The phase labels in Figure 3 summarize recorded choices, not contemporaneous internal thoughts.

The following original public rationales accompany the sealed Q forecasts, after research and K1. They were issued without reference feedback. They are public accounts, not validated mechanisms or evidence that the acquired observations were sufficient.

**Discovery Q rationale (verbatim).**

> Predictions use the campaign’s empirical potential-window and charge-delivery trends at nearly the same concentration: +0.8 V is treated as closer to the productive +0.5 V regime than −0.8 V, duration raises conversion and yield, and 500 mA raises yield while penalizing faradaic, transport, and energy efficiencies. Electrolyte and solvent adjustments follow the matched short-run screens. Intervals are deliberately broad because both test potentials are unmeasured, long-time data exist only at +0.5 V/E2, and low-yield assay noise strongly affects short runs and the score’s yield gate.

**Optimization Q rationale (verbatim).**

> Predictions use the observed S0/E0 batch as the main local anchor, scale product formation with electrolysis duration and configured current, and impose the campaign’s strong positive-potential window. The S0/E1, S0/E3, and S2/E0 combinations are assigned low activity because cross-pair controls showed severe nonadditive solvent–electrolyte incompatibility. Higher current raises expected yield but lowers transport and charge efficiency. Intervals include final-assay noise plus substantial extrapolation uncertainty, especially for negative polarity and untested material pairs.

## E.8 Complete optimization forecasts

All twelve forecasts use 0.012 mol in 0.025 L. Predictions and nominal 80% intervals were sealed before reference feedback. References below are the original seeded observations. The four bold query identifiers share +0.8 V, 100 mA and 7,200 s, while changing the material pair.

**Table E7. Query settings, sealed forecasts and reference scores.**

| Q | Pair | V | mA | s | Forecast | 80% interval | Reference |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | S0/E0 | -0.8 | 100 | 600 | 0.050 | 0.000-0.180 | 0.032659 |
| 02 | S0/E0 | 0.8 | 100 | 600 | 0.230 | 0.040-0.480 | 0.349491 |
| 03 | S0/E0 | -0.8 | 100 | 7200 | 0.250 | 0.080-0.440 | 0.358985 |
| **04** | S0/E0 | 0.8 | 100 | 7200 | 0.570 | 0.430-0.680 | 0.572012 |
| 05 | S0/E1 | -0.8 | 100 | 7200 | 0.080 | 0.000-0.250 | 0.362359 |
| **06** | S0/E1 | 0.8 | 100 | 7200 | 0.100 | 0.000-0.290 | 0.627599 |
| 07 | S0/E3 | -0.8 | 100 | 7200 | 0.070 | 0.000-0.230 | 0.347853 |
| **08** | S0/E3 | 0.8 | 100 | 7200 | 0.090 | 0.000-0.280 | 0.542955 |
| 09 | S2/E0 | -0.8 | 100 | 7200 | 0.060 | 0.000-0.210 | 0.288226 |
| **10** | S2/E0 | 0.8 | 100 | 7200 | 0.070 | 0.000-0.240 | 0.494376 |
| 11 | S0/E0 | -0.8 | 500 | 7200 | 0.170 | 0.040-0.360 | 0.276451 |
| 12 | S0/E0 | 0.8 | 500 | 7200 | 0.550 | 0.390-0.680 | 0.344881 |

Score MAE is 0.229397; interval coverage is 5/12. The accurate Q04 prediction is retained alongside the large underestimates at Q06, Q08 and Q10. Source-to-query changes involve amount, volume and electrical settings, so these contrasts do not isolate one changed variable. Twelve query outcomes do not establish population calibration. No intermediate sealed prediction checkpoints were collected, so final prediction errors cannot be plotted as a within-session learning curve.

# Appendix F. Equilibrium predictions and model comparisons

## F.1 Original intervals and campaign-specific observations

The Sol equilibrium comparisons show point predictions for the lowest-concentration recipe (Fig. 5c and Supplementary Fig. S8c). Table F1 retains all fifteen original 80% prediction intervals and each campaign's source-response range. These are prediction intervals issued by the agent, not confidence intervals on an estimated mean. Each source range covers twelve final assays; the reference is the mean of the original five evaluator observations and was unavailable during prediction or retrospective reflection.

**Table F1. Dissociation predictions at the most dilute recipe, with all values in percent.**

| World / arm | Source range | Point prediction | 80% interval | Reference mean |
| :--- | ---: | ---: | ---: | ---: |
| 1 / Opaque | 6.18-8.34 | 69.90 | [25.00, 90.00] | 71.60 |
| 1 / Aligned | 6.20-9.23 | 10.40 | [4.40, 22.50] | 71.60 |
| 1 / MisIndexed | 6.11-9.25 | 10.92 | [7.72, 14.12] | 71.60 |
| 2 / Opaque | 6.17-8.57 | 62.90 | [45.00, 80.00] | 65.46 |
| 2 / Aligned | 6.12-8.06 | 8.04 | [5.30, 10.80] | 65.46 |
| 2 / MisIndexed | 6.23-7.98 | 8.06 | [5.56, 10.56] | 65.46 |
| 3 / Opaque | 5.94-8.22 | 56.30 | [43.00, 70.00] | 57.97 |
| 3 / Aligned | 6.34-8.02 | 11.00 | [4.50, 19.00] | 57.97 |
| 3 / MisIndexed | 6.16-7.94 | 46.00 | [10.00, 75.00] | 57.97 |
| 4 / Opaque | 6.19-7.91 | 52.00 | [15.00, 88.00] | 51.73 |
| 4 / Aligned | 5.82-8.14 | 7.24 | [4.00, 10.50] | 51.73 |
| 4 / MisIndexed | 5.81-8.22 | 9.62 | [4.00, 45.00] | 51.73 |
| 5 / Opaque | 5.49-7.48 | 41.30 | [20.00, 70.00] | 44.80 |
| 5 / Aligned | 6.44-7.99 | 7.90 | [3.50, 13.00] | 44.80 |
| 5 / MisIndexed | 6.58-7.79 | 6.81 | [4.00, 9.60] | 44.80 |

The recipe contains 1 micromole in 75 mL (nominal concentration 13.3 μM). The source-observation band in Supplementary Figure S8 pools the minimum and maximum across all 180 assays, whereas Figure 5c uses only the five Opaque campaigns; the ranges above are specific to each campaign. World 3 MisIndexed retains its mixed-explanation departure from the plateau. Public explanation categories and K1/Q chronology are in section C.4.

## F.2 Sol interval and regime comparisons

**Supplementary Table F2. GPT-5.6 Sol equilibrium predictions across test regions.**

| Arm | Remaining nine: MAE | Lowest three: MAE | Remaining nine: coverage | Lowest three: coverage |
| --- | --- | --- | --- | --- |
| Opaque | 0.01008 | 0.01833 | 90.7% | 93.3% |
| Aligned | 0.00465 | 0.15862 | 91.3% | 2.2% |
| MisIndexed | 0.00439 | 0.14397 | 89.6% | 13.8% |

Values average five worlds and three response targets per group: normalized pH, dissociation fraction and precipitation signal. Coverage uses original 80% prediction intervals, with 675 reference-containment judgments per arm for the remaining nine conditions and 225 for the three lowest-concentration conditions; these judgments are not independent world replicates. The concentration grouping is post hoc and exploratory; the remaining nine conditions also include boundaries. Figure 4b shows the same macro-error comparison, whereas Supplementary Fig. S8c shows one response and one query separately.

## F.3 Complete five-model comparison

**Supplementary Table F3. Equilibrium predictions from five medium model configurations.**

| Model | Arm | Remaining nine: MAE | Lowest three: MAE | Lowest three: coverage |
| --- | --- | --- | --- | --- |
| GPT-5.5 | Opaque | 0.00647 | 0.16325 | 6.7% |
| GPT-5.5 | Aligned | 0.00638 | 0.16146 | 2.7% |
| GPT-5.5 | MisIndexed | 0.00461 | 0.13604 | 13.3% |
| GPT-5.6 Luna | Opaque | 0.09867 | 0.15240 | 48.4% |
| GPT-5.6 Luna | Aligned | 0.04997 | 0.13319 | 31.1% |
| GPT-5.6 Luna | MisIndexed | 0.05494 | 0.12556 | 44.4% |
| GPT-5.6 Terra | Opaque | 0.03268 | 0.14611 | 67.1% |
| GPT-5.6 Terra | Aligned | 0.01545 | 0.11466 | 26.2% |
| GPT-5.6 Terra | MisIndexed | 0.01369 | 0.12130 | 41.8% |
| GPT-5.6 Sol | Opaque | 0.01008 | 0.01833 | 93.3% |
| GPT-5.6 Sol | Aligned | 0.00465 | 0.15862 | 2.2% |
| GPT-5.6 Sol | MisIndexed | 0.00439 | 0.14397 | 13.8% |
| GPT-6 Astra | Opaque | 0.00244 | 0.04040 | 82.7% |
| GPT-6 Astra | Aligned | 0.00384 | 0.03853 | 82.7% |
| GPT-6 Astra | MisIndexed | 0.00234 | 0.01857 | 92.4% |

Each row contains five independent source campaigns, equally weighting the five worlds; worlds recur across information conditions and models. Each campaign predicts pH/14, dissociation fraction and precipitation signal for twelve queries. The three lowest-concentration conditions are the same fixed query group; the remaining nine also include boundary and unexplored conditions. Coverage concerns original 80% intervals and five reference observations, not confidence intervals or independent model replications. All three arms are retained; lower MisIndexed error does not itself establish a causal benefit of incorrect knowledge.

The number of worlds in which Aligned improves on the remaining nine conditions but worsens on the three lowest-concentration conditions relative to Opaque is 5/5 for Sol, 2/5 for Luna, 0/5 for Terra, 1/5 for GPT-5.5 and 0/5 for Astra. Excluding the known pilot World 1, mean MAE differences (Aligned minus Opaque) on the remaining nine/lowest-concentration three conditions are −0.04105/−0.00306 for Luna, −0.02061/−0.03544 for Terra, +0.00054/+0.00119 for GPT-5.5 and +0.00122/−0.01140 for Astra.

For the four targeted configurations, mean interval scores on the three lowest-concentration conditions, in Opaque/Aligned/MisIndexed order, are 0.76286/0.95830/0.76799 for Luna, 0.63495/0.76843/0.71607 for Terra, 1.38838/1.31276/1.19913 for GPT-5.5 and 0.29182/0.22233/0.16108 for Astra. Lower Aligned point errors in Luna and Terra are not accompanied by improved interval scores.

Median campaign minimum source concentrations are 0.125 M for Luna, 0.125 M for Terra, 0.0185 M for GPT-5.5 and 0.001 M for Astra; campaigns with positively loaded assays at or below 1 mM number 0/15, 0/15, 0/15 and 11/15, respectively. All 180 Sol assays exceed 0.018 M. The threshold describes acquired evidence coverage rather than a physical response boundary.

## F.4 Detailed Sol equilibrium figure

![Supplementary Figure S8. GPT-5.6 Sol experimental evidence, regime reversal and original equilibrium forecasts. a, All 180 source assays at their nominal concentrations (0.0185–2 M), representing autonomously selected recipes and histories. Twelve diamonds show each query's reference mean across five worlds, with world-level sample standard deviation (SD); each world reference is a mean of five evaluator observations. The source-response band spans the sampled concentration range, and vertical shading marks three dilute conditions with no source assays. b, Macro MAE for the remaining nine and three lowest-concentration conditions. Bars and error bars show five-world means ± sample SD; open points retain every world and ratios compare Aligned with Opaque within a test region. c, Original dissociation predictions and reference means for the lowest-concentration recipe (13.3 μM) in five worlds. Horizontal shading spans source observations of 5.5–9.2%, retaining the World 3 MisIndexed counterexample. Supplementary Tables F1, F2 and F3 give original 80% prediction intervals, group metrics and cross-model comparisons, respectively.](../../figures/narrative-final/figureS8.pdf)

# Appendix G. Response contributions and purity-error diagnosis

## G.1 Equilibrium reversal by response

This exploratory decomposition retains all fifteen parameter-prior campaigns and all 540 response predictions. It uses the existing three-lowest-concentration grouping. MAE first averages queries within a campaign and response, then the five worlds. Averaging the three response MAEs exactly recovers Supplementary Table F2. The same worlds recur across arms; queries and responses are not independent replicates.

**Table G1. Original prediction MAE by response and concentration group.**

| Response | Group | Opaque | Aligned | MisIndexed | Lower / higher |
| :--- | :--- | ---: | ---: | ---: | :--- |
| pH / 14 | Other nine | 0.00261 | 0.00269 | 0.00254 | 2 / 3 of 5 |
| pH / 14 | Dilute three | 0.00448 | 0.05576 | 0.05230 | 0 / 5 of 5 |
| Dissociation fraction | Other nine | 0.00839 | 0.00709 | 0.00660 | 3 / 2 of 5 |
| Dissociation fraction | Dilute three | 0.02640 | 0.28229 | 0.23861 | 0 / 5 of 5 |
| Precipitation signal | Other nine | 0.01923 | 0.00417 | 0.00403 | 5 / 0 of 5 |
| Precipitation signal | Dilute three | 0.02411 | 0.13783 | 0.14099 | 0 / 5 of 5 |

The final column counts worlds with lower/higher Aligned MAE than Opaque. Signed response differences divided by three sum to the macro-error difference. They quantify the contribution on the declared normalized scales; they do not establish a shared failure mechanism or physical comparability of targets.

## G.2 Separating purity offset from variation error

For each of thirty campaigns, let $p_i$ and $y_i$ be its original prediction and retained noiseless reference for the twelve queries. Define $b=\overline{p-y}$ and $c_i=(p_i-\bar p)-(y_i-\bar y)$. Then

$$\operatorname{MSE}=b^2+\frac{1}{12}\sum_{i=1}^{12}c_i^2.$$

The first term measures the common offset; the second measures mismatched variation across conditions. Centred RMSE is the square root of the second term. Reference and prediction standard deviations use denominator twelve. All calculations retain the source-assay shortfall. Demeaning uses withheld references only for diagnosis; it is not an available predictor or a corrected performance result. MAE has no analogous additive decomposition.

**Table G2. Purity offset and variation diagnostics.**

| Batches | Arm | N | Bias | cRMSE | Ref. SD | Pred. SD | Offset share |
| ---: | :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Both | All | 30 | -4.289 | 1.889 | 0.598 | 1.968 | 87.6% |
| 12 | Opaque | 5 | -0.806 | 0.970 | 0.598 | 1.031 | 45.3% |
| 12 | Aligned | 5 | -4.920 | 1.837 | 0.598 | 1.791 | 89.8% |
| 12 | MisIndexed | 5 | -9.166 | 2.843 | 0.598 | 2.977 | 91.3% |
| 24 | Opaque | 5 | -1.816 | 1.682 | 0.598 | 1.649 | 57.4% |
| 24 | Aligned | 5 | -3.948 | 1.797 | 0.598 | 1.983 | 85.6% |
| 24 | MisIndexed | 5 | -5.080 | 2.206 | 0.598 | 2.376 | 85.3% |

N is the campaign count; cRMSE denotes centred RMSE. Bias, cRMSE and both standard deviations are campaign means in percentage points. Offset share is the ratio of summed squared campaign biases to summed campaign MSEs, with equal query counts; it is not the mean campaign fraction. The median campaign fraction is 77.6%. Mean bias is negative in 30 of 30 campaigns. Centred RMSE exceeds reference SD in 29 of 30. These comparisons describe forecast outputs and do not identify an internal revision process. No new agent or simulator calls were made.

## G.3 Information conditions and resources

Information conditions further delimit this interpretation. At twelve batches, Aligned and MisIndexed improve recovery MAE but worsen purity MAE relative to Opaque in every world; at 24 batches, this joint direction appears in only two and three of five worlds, respectively (Fig. 6c). Prediction intervals also fail to reliably accommodate purity errors (Fig. 6d). At both budgets, Aligned and MisIndexed have wider mean intervals than Opaque, so poorer coverage cannot simply be attributed to narrower stated uncertainty. Conversely, high Opaque coverage alone does not establish calibration or sharpness. These effects depend jointly on response and research resources.

# Appendix H. Executed process models and information conditions

## H.1 Equilibrium response model

The parameter-prior study uses a bounded monoprotic acid-base model followed by a precipitation calculation. These are the process relations used for the retained campaigns and references. They are distinct from explanations proposed by the agents. In particular, an agent's proposed active-pool cap is not the implemented source of the dissociation plateau.

Let $n$ be the current ledger amount of the initial reactant, $V$ the current sample volume and $C=n/V$. The background-ion amounts are $n_+=\min(0.020,0.15n)$ and $n_-=\min(0.020,0.08n)$, in moles. With $H=[\mathrm{H}^+]$, $K_a=10^{-\mathrm{p}K_a}$ and activity-ratio factor $g$, the solver obtains

$$[\mathrm{A}^-]=\frac{CK_a}{K_a+gH},\qquad [\mathrm{OH}^-]=\frac{K_w(T)}{H},$$

subject to charge balance,

$$H+\frac{n_+}{V}-\frac{K_w(T)}{H}-[\mathrm{A}^-]-\frac{n_-}{V}=0.$$

The reported responses are $\mathrm{pH}/14=-\log_{10}(H)/14$ and dissociation fraction $\alpha=[\mathrm{A}^-]/C$, clipped to the public unit interval. In the uncapped background-ion range, charge balance implies $\alpha=0.07+H/C-K_w/(HC)$. At sufficiently high concentration the last two terms are small, giving a local plateau near 7%; dilution makes their contribution appreciable. The plateau and departure therefore arise under the same fixed equations. The five effective pKa values span 4.6594 to 5.3794 in increments of 0.18; the default activity-ratio factor is one.

Precipitation is calculated sequentially from effective ion inventories $a=n_++0.10n_{\mathrm{A}^-}$ and $b=n_-+0.08n_{\mathrm{HA}}$. When supersaturated, a 1:1 removal $x$, bounded by the limiting inventory, satisfies $(a-x)(b-x)/V^2=K_{sp}$, with default $K_{sp}=1.8\times10^{-10}$. The public signal is $x/n$, clipped to $[0,1]$. This hook does not feed precipitation back into the acid-base solution. Thus the three public responses are related but should not be interpreted as three independent measurements of one failure mechanism.

The concentration in Figure 4a and Supplementary Figure S8a is a recipe descriptor: total nominal reagent additions divided by total solvent additions. The solver instead uses the ledger state at measurement, after any sample consumption and other operations. The scatterplot combines distinct recipes and histories; it is not a controlled one-dimensional titration curve. The three most dilute test recipes have nominal concentrations of approximately $1.33\times10^{-4}$, $1.33\times10^{-5}$ and $1.67\times10^{-4}$ M. No source assay in these fifteen Sol campaigns reaches those concentrations.

## H.2 A concrete three-arm information example

Table H1 reproduces the numerical content of the first equilibrium world's public prior from the frozen configuration and input serializer. It is a formatted input excerpt, not a reconstruction of agent dialogue. All three arms retain the same public operations, general task background, resource contract and physical world. Opaque receives no instance-specific initial world model. The other two arms receive the same schema and wording; MisIndexed substitutes the configured fifth world's claim.

**Table H1. Public prior content in one matched physical world.**

| Supplied field | Opaque | Aligned | MisIndexed |
| :--- | :--- | :--- | :--- |
| Effective pKa interval (80%) | Absent | [4.6094, 4.7094] | [5.3294, 5.4294] |
| Dilution change in pH/14 | Absent | +0.003494987 | +0.000875889 |
| Dilution change in dissociation | Absent | +0.008187416 | +0.001884676 |
| Nominal confidence | Absent | 0.8 | 0.8 |

The common dilution anchor is 0.001 mol acid at 298.15 K, with volume increasing from 0.018 to 0.054 L. Both supplied records identify the source as an “independent bounded archival fit” and qualify the claim as a “local effective relationship; not a universal aqueous-chemistry law”. The pKa intervals above are rounded for display; the input contains their full precision. Aligned therefore supplies correct partial local information, not the evaluator's complete process equations, query answers or an instruction to enter the most dilute test region. The experiment contrasts the resulting complete research processes, including possible changes to evidence acquisition and interpretation.

## H.3 Crystallization response model

The retained crystallization block composes upstream reaction, thermal operations, seeding, crystal nucleation and growth, filtration and measurement. It uses the latent-material process family and its linear supersaturation-dependent impurity transfer. Solid product, solid impurity and the particle population persist across operations; dissolved and solid inventories are accounted for separately.

The temperature-dependent solubility follows

$$c^*(T)=c^*_{\mathrm{ref}}\exp\!\left[-\frac{\Delta H}{R}\left(\frac{1}{T}-\frac{1}{T_{\mathrm{ref}}}\right)\right],$$

with $T_{\mathrm{ref}}=298.15$ K, $\Delta H=20{,}000$ $\mathrm{J\,mol^{-1}}$ and a declared temperature domain of 250-430 K. World and solvent properties scale the reference solubility and kinetics. For relative supersaturation $s=\max(C/c^*-1,0)$, primary nucleation scales as $B=k_b s^2$ and linear growth as $G=k_g s$. Before world and solvent multipliers, the coefficients are $2\times10^7$ $\mathrm{L^{-1}\,s^{-1}}$ for nucleation and $2\times10^{-8}$ $\mathrm{m\,s^{-1}}$ for growth. Nucleation and growth consume available dissolved target and update the population distribution; they are not independent score adjustments.

Each crystallized target increment transfers impurity according to

$$\Delta n_{I,s}=\min\!\left(n_{I,l},\;\Delta n_{P,s}\,k_{\mathrm{occ}}(1+0.5s)\right),$$

where $k_{\mathrm{occ}}=0.02$ times the solvent's occlusion multiplier. The four nominal solvent multipliers are 1.20, 0.80, 0.65 and 1.05; world-fixed material residuals further modulate these properties. Filtration retains 96% of target solids and 92% of impurity solids. The final-assay purity is the solid-target mole fraction $n_{P,s}/(n_{P,s}+n_{I,s})$. Seed contributes to target purity but is subtracted in the full-process recovery numerator; final-assay recovery is normalized by the initial reagent charge.

These relations allow thermal and seeding histories to alter the amount and size distribution of crystals while impurity incorporation remains modest. They explain how recovery and particle responses can vary without requiring a comparable purity change. The approximately 98.5% purity level is an empirical property of the retained source and query conditions, not a hard-coded value or a universal invariant of the model. The present analysis does not isolate individual process contributions to that stability. Appendix G separately tests whether the forecasts preserve the level and variation of the retained purity references.

## H.4 Scope of this reconstruction

The equations and input excerpt were checked against the execution-version source and retained configuration bindings. Later equilibrium adapters and alternative crystallization impurity laws are not used to explain these observations. This documentation and the error decompositions use existing source records, predictions and references only; they add no agent or simulator calls. Internal source identities are retained with the analysis records for the archival package.
