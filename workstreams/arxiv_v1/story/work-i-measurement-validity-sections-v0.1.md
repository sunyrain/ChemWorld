# Work I known-policy measurement-validity sections v0.1

> **SUPERSEDED 2026-08-04.** Historical drafting handoff; use
> [`../FIRST_PAPER_TODOLIST.md`](../FIRST_PAPER_TODOLIST.md) for current work.

Historical status: **integration-ready for the retired Work I draft**

Task: `W1-S05`

Accountable owner: `Yijun`

This package supplies the known-policy measurement-validity text owned by W1-S05. It
does not edit the manuscript, recompute a frozen result, or alter the Figure 2 asset.
The source-defined factorial is **5 formal world seeds × 2 information arms × 3 known
policies = 30 primary campaign profiles**. It must not be restated as “5 profiles × 2
arms × 3 seeds”: the five levels are worlds, the three levels are policies, and each
scheduled cell produces one campaign profile. Each campaign contains six started
vessels closed by one committed final assay or discard, giving **30 × 6 = 180 primary
closed lifecycles**.

## Results — Known policies validate the experimental-agency profile

Before interpreting complete agent systems, we tested whether the frozen
experimental-agency profile could recover behavioral structures fixed by construction.
The profile keeps five observable axes separate—terminal commitment, evidence
acquisition, evidence-conditioned action, resource deployment, and outcome-trajectory
organization—and reports endpoint context beside, rather than inside, those axes. We
therefore treated the campaign profile, not a lifecycle or primitive operation, as the
primary unit and formed no composite intelligence score.

We crossed five simulated electrochemical worlds (formal world seeds 0--4), two
information arms (`opaque_codes` and `anonymous_nominal_properties`), and three
deterministic known policies. The resulting 30 original campaigns contained 180/180
closed lifecycles and made zero provider calls (Fig. 2). `assay_all` terminated and
assayed every vessel; `start_then_discard` discarded each vessel immediately after
starting it; and `measure_then_threshold` acquired one UV--vis conversion signal,
discarded values below the independently qualified threshold, and otherwise performed
one additional electrolysis before termination and final assay. The threshold policy
produced 28 assays and 32 discards among its 60 primary lifecycles, satisfying the
preregistered requirement that both branches occur.

The recovered campaign-equal summaries followed the frozen signatures. For
`assay_all`, the mean assay-fraction, discard-fraction, measured-lifecycle,
continued-investment, and non-final-instrument fractions were 1.000, 0.000, 0.000,
0.000, and 0.000, with 6.000
attempted operations per closed lifecycle. The corresponding values for
`start_then_discard` were 0.000, 1.000, 0.000, 0.000, and 0.000, with 2.000 attempted
operations. For `measure_then_threshold`, they were 0.467, 0.533, 1.000, 0.467, and
1.000, with 6.933 attempted operations. Thus all six preregistered partial orderings
held: assay commitment decreased from `assay_all` through the threshold policy to
`start_then_discard`; discard commitment had the reverse ordering; only the threshold
policy measured; only the threshold policy performed a further committed process
operation after its measurement; only the threshold policy used a non-final
instrument; and attempted
operations ordered as threshold > assay-all > immediate-discard.

The registered conditional-null pattern also held. First-measurement timing was null
for the two policies that never acquired non-final evidence and finite for the threshold
policy. Because `start_then_discard` performed no final assay, both endpoint-context
values and all five outcome-trajectory metrics were null. `assay_all` had finite
endpoint context, while its recovery rate remained denominator-dependent and was null
exactly when no loss episode existed. The threshold policy's outcome-trajectory
quantities followed the same frozen denominator rules using its observed assay count;
undefined quantities were retained as null rather than coerced to zero. Evidence-to-
terminal concordance was 1.000 for the threshold-eligible policy and null for the two
ineligible policies.

Resource checks agreed with the action grammar. In every world-arm pair,
`start_then_discard` used fewer committed operations and no reagent relative to the two
full-prefix policies. `assay_all` and `measure_then_threshold` used the same solvent and
reagent prefix schedule, and every campaign ledger reconciled to its committed path.
No ordering was registered for endpoint score, outcome-trajectory metrics, or cost and
risk between `assay_all` and `measure_then_threshold`; none is inferred from these
controls.

All 12 frozen gates passed, including profile reconstruction, resource-ledger replay,
exact replay and deterministic retest, conditional nulls, signatures, orderings,
matched-arm invariance, and the zero-provider gate. The policies never read the
material dossier, so equality between the matched information arms is an interface,
pairing, and identity check—not an estimate of a causal material-information null
effect. A second same-identity execution reproduced the registered controller,
trajectory identity, profile, and component hashes for all 30 campaign pairs. These 30
retest campaigns and their 180 closed lifecycles are reliability evidence only and do
not double the primary sample.

Together, these results establish a bounded construct/discriminant-validity positive
control: within this simulated apparatus, the multidimensional readout distinguished
three policies whose evidence and terminal-decision structures were known in advance.
They do not establish chemical intelligence, stochastic-agent or complete-system
competence, a unified model ranking, endpoint superiority, physical-chemistry validity,
or transfer to a real laboratory.

## Methods — Frozen known-policy validation

### Construct and analysis unit

Experimental agency was operationalized as the observable organization of
resource-constrained choices over typed operations, active evidence acquisition,
post-evidence action, and lifecycle termination in a hidden stateful chemical world.
The frozen record contains 19 metrics across five construct axes. Mean and best assayed
scores are two separate endpoint-context fields and never enter a composite profile.
One primary observation is the profile from one original campaign in one fixed world,
information arm, and policy cell. Profiles were constructed within campaigns before
aggregation; each of the ten world-arm campaigns for a policy received equal weight.
Lifecycle rows were not pooled before profile construction, and primitive operations
were not treated as independent samples.

### Factorial, inclusion, and counting rules

The formal schedule was fixed as five world seeds (0--4) × two information arms ×
three policies, with six lifecycles per campaign. A primary lifecycle was a started
vessel closed by exactly one committed terminal action (`final_assay` or
`discard_batch`). Only original executions have the primary role. Failed or incomplete
cells would have been retained outside the primary count and could not be silently
coerced to complete; in the frozen execution all 30 cells and all 180 primary
lifecycles completed. Same-identity retests have a separate reliability role and are
excluded from the primary estimand. Provider calls were required to remain zero in
both original and retest executions.

Within each world-policy pair, the two arms shared physics, probe order, keyed-noise
namespace, policy code, and resource card; only the supplied material dossier changed.
The deterministic policies did not consume that dossier. Arm equality was therefore a
preregistered invariance check, not a causal contrast in information utility.

### Frozen policies and threshold firewall

All policies received the same six probe cards in the same order. `assay_all` used six
committed operations per lifecycle: add solvent, add reagent, set potential,
electrolyze, terminate, and final assay. `start_then_discard` used two: add solvent and
discard. `measure_then_threshold` first executed the shared four-operation physical
prefix, measured public UV--vis conversion, and compared the finite scalar signal with
the frozen threshold **0.007984561379998922** using `>=`. Values below threshold were
discarded after six operations; values at or above threshold received one additional
electrolysis, termination, and final assay for eight operations.

The threshold was selected before formal execution from qualification world seeds
1000--1004 only. Formal seeds 0--4 were excluded. Candidate midpoints had to produce
both branches in every qualification arm; the admissible candidate closest to the
pooled qualification median was selected, with ties resolved toward the lower value.
The threshold, source-manifest identity, and formal-world exclusion were frozen before
the policies were released. Had the formal threshold policy been degenerate, the full
result would still have been reported as an unestablished positive control; formal-data
retuning, result replacement, and seed substitution were forbidden.

### Resource and operation contract

Every campaign used resource card `work-i-known-policy-formal-k6-v1`. Hard limits were
48 operation attempts, six vessel starts, six final assays, six non-final instrument
uses, six UV--vis uses, 0.09 mol reagent, and 0.15 L solvent. The six probe cards used
0.025 L solvent each, reagent amounts 0.010--0.020 mol, potentials 0.72--1.24 V,
currents 25--90 mA, and matched 300--900 s probe/post-measure durations. An admitted
environment step counted as an attempted operation, including a validation failure or
transaction rollback; a committed operation required `transaction_status=committed`.
Only committed non-final measurements counted as evidence acquisition. Cost and risk
were campaign-ledger deltas: charged attempt penalties remained included, whereas
rejected candidate-state changes remained excluded.

These are bounded state-coupled synthetic-instrument and executable simulator
semantics. The UV--vis signal and final assay are not claims of empirical calibration
against physical devices, and resource accounting is not a certificate of real-world
material use, safety, or elapsed laboratory time.

### Frozen signatures, nulls, and aggregation

Signature recovery was evaluated only after the execution-validity gate required all
planned lifecycles to close, every submitted action to commit, no validation or
resource rejection, and exact event/state/resource replay. For the threshold policy,
letting \(p\) denote its assayed fraction, the frozen algebra was assay fraction
\(p\), discard fraction \(1-p\), continued-investment fraction \(p\),
post-measure process operations per lifecycle \(p\), first-measurement timing
\(2/3-p/6\), and attempted and committed operations per lifecycle \(6+2p\).
Strict policy orderings were evaluated only after the pooled formal non-degeneracy gate
established \(0<p<1\).

Undefined conditional metrics followed their declared denominators. In particular,
first-measurement timing was null when no closed lifecycle contained a committed
non-final measurement; threshold concordance was null when no lifecycle had a finite
registered diagnostic; endpoint context and all outcome-trajectory metrics were null
without a final assay; retention and drawdown required at least two assays; recovery
was null without a loss episode; and terminal-to-best retention was null without a
positive assayed score. Nulls were never replaced by zeros. Endpoint and trajectory
values were descriptive extensions, not construct-recovery orderings.

The read-only V06/V09 analysis independently rebuilt profiles from immutable event and
resource evidence, replayed every campaign ledger, and verified bundle file hashes,
byte counts, dependency identities, and report self-hashes. Policy summaries were
arithmetic means of ten equally weighted campaign profiles. No world, controller,
provider, threshold, inclusion rule, or estimand was executed or modified by the
reporter.

### Replay and deterministic reliability

For each original campaign, exact replay required event, simulator-state, resource,
terminal, endpoint, profile, and trajectory-manifest hashes to match. The reliability
execution then reran the same deterministic policy from the same world identity,
keyed-noise namespace, arm, threshold, and resource card. All 30 original/retest pairs
matched the controller, trajectory identity, profile, and component hashes. Because
this is same-identity deterministic reproducibility, it does not measure variability
of stochastic agents or external systems.

### Figure 2 contract and interpretation boundary

Figure 2's sole narrative job is to show that the frozen multidimensional profile
recovers the three known-policy signatures and that the same-identity deterministic
retest is exact. It may display: (A) the five profile axes with endpoint context kept
separate; (B) campaign-equal policy summaries and registered nulls; (C) the threshold
split, six orderings, and resource checks; and (D) 30/30 deterministic retest matches.
The caption must state **30 primary campaigns / 180 primary closed lifecycles** and
identify the additional 30 campaigns / 180 lifecycles as excluded reliability
retests.

Figure 2 does not rank endpoints, agents, language models, or complete systems; treat
lifecycles or operations as inferential replicates; estimate a causal information
effect; validate physical instruments or real chemistry; or support laboratory
transfer. It establishes permission to interpret later profile differences only at
the level of a bounded positive control for this simulated measurement apparatus.

## Evidence bindings

File SHA-256 values below are byte hashes independently recomputed for this handoff.
Embedded semantic identities, where applicable, remain distinct: profile contract
`01e3cb3ff5c7b2455fd998fb5eebdd1932931c6fef2d5125632b103d79a34262`,
known-policy contract
`79681abfa92af758af8326db1727b865376ad0da192ea13552b68fd94a66dd45`,
threshold binding
`8a55b713ca900a644a301ecd8e83a0a686f9a28b3f60a18a85a4e57b66288c6a`,
formal matrix manifest
`d15c7af5084a96d579fa87de55e0177d3eb2026dc5cb651042c516251751cdcc`,
formal audit
`661d42ec74993200750f040bb4d12f4403fbc9c2c4b78aed5a9e6cc2b0c6be95`,
and V09 report
`ebb56a052929944330acdf594e4a341c8c8fdb2b4ea2e276556384e7ce6b2064`.

| Source commit | Path | File SHA-256 | Supports |
| --- | --- | --- | --- |
| `523f08fd3e67dc7d9cd0c94ca32027f7371e1811` | `configs/benchmark/work_i_policy_profile_contract_v0.1.json` | `f9d71ba31e8885b2150ef8457dfed6e91d33f986de924ba314ae46d33af8eab6` | Five-axis construct, 19 profile metrics, two separate endpoint fields, denominators, nulls, campaign-first aggregation, and no composite score. |
| `345f1d13dc2338680228a5f3f5058962eaacabf6` | `configs/benchmark/work_i_known_policy_contract_v0.1.json` | `a3ec08634309e947bb0491a4b406585e8ae0a46894368f2c6dcdf516aae379d2` | Three policy grammars, 5 × 2 × 3 × 6 design, exact signatures, six orderings, resource expectations, non-orderings, and claim ceiling. |
| `bb2031c0e77aacb428996e239e4da484e51cac26` | `configs/benchmark/work_i_known_policy_threshold_v0.1.json` | `97665fc6fb5bbc613fb20be270a77f562849257a8ceb89dcc5d2677523c03be5` | Frozen threshold, comparator, qualification/formal seed separation, both-arm branch balance, and no formal retuning. |
| `260eb0966222a855faf98e6b42be718d3b33f55d` | `configs/benchmark/work_i_policy_control_matrix_v0.1.json` | `8b3446ec22e54703096c0c74b2f9a0879bf9d034985913ec61d2fc9535cd9c15` | Formal factorial, six lifecycles per campaign, resource card, primary/retest roles, failed-cell rule, and zero-provider requirement. |
| `bb2031c0e77aacb428996e239e4da484e51cac26` | `workstreams/arxiv_v1/reports/work-i-known-policy-threshold-qualification-v0.1.json` | `4ab26d299c4cf75f4ca589ab3614592c63a4d7dbff8d11757caa31f82300c929` | Outcome-independent threshold selection from seeds 1000--1004 and exclusion of formal seeds 0--4. |
| `55b7b3c1908a6bec8ee3dbc4b5e3efcbd3599ab6` | `workstreams/arxiv_v1/reports/work-i-policy-control-formal-v0.1/matrix_manifest.json` | `0c627f679835299d657938a28899413b596ff01aaf344290658a057252e3433e` | Immutable 30-cell formal schedule, 180 primary and 180 retest lifecycles, bundle identities, and retest exclusion. |
| `7e3337b7cbcb83248a88dceef31bcb635468d680` | `workstreams/arxiv_v1/reports/work-i-policy-control-formal-audit-v0.1.json` | `d4c539048dd4463b5e281fe7bec014fd11e87809057b32c34a3d99b08f900b55` | Independent profile/ledger reconstruction, 12 gates, 28/32 threshold split, null/order/resource checks, and exact retests. |
| `fc120816f9e04ca34f2a78bdaebab8dda1351799` | `workstreams/arxiv_v1/reports/work-i-known-policy-validity-report-v0.1.json` | `58458670f1db62a1f048a778539e054131a125941ff04fa38d5892d27c382dee` | Frozen campaign-equal results, complete cell profiles, evidence bindings, reliability result, and bounded interpretation. |
| `fc120816f9e04ca34f2a78bdaebab8dda1351799` | `workstreams/arxiv_v1/reports/work-i-known-policy-validity-report-v0.1.md` | `41c272af762f228fa75abb955bc338cd574de0e6de2f40bb0244b8b4942f43f2` | Human-readable frozen design, policy summaries, gate disposition, reliability result, and interpretation boundary. |
| `477538003c7d39b1efdcf67e081642be922e69bc` | `src/chemworld/eval/policy_validity_audit.py` | `8ea2c4f47a3414a2ad3ad2f3490ed533f6691a2294c56d975650687b7e56041d` | Independent profile construction, denominator-aware null handling, policy algebra, arm invariance, resource checks, and frozen gate evaluation. |
| `477538003c7d39b1efdcf67e081642be922e69bc` | `tests/test_policy_validity_audit.py` | `1017dfc6b0d4a435f6aa6c76ae765b68cf9a6be917e2d14fb276847da7142838` | Provider-free positive, tamper, degenerate-threshold, retest-identity, arm-drift, and endpoint-nonordering tests. |
| `9ac541dcf1b4a083ca465b556362c40480a4cde7` | `src/chemworld/eval/policy_validity_report.py` | `d510346506f7312fc10f82e75266348366103f93ef4cc3a51c518a996d90cd5e` | Read-only campaign-equal V09 analysis, frozen count enforcement, failure-preserving reporting, and claim-boundary rendering. |
| `9ac541dcf1b4a083ca465b556362c40480a4cde7` | `tests/test_policy_validity_report.py` | `4b1cf45b37e3dcc6096ff49b2f2cd992a1b9c4b7a372ac414213bb73958a68e1` | Deterministic checks for counts, weighting, retest exclusion, self-hashes, tamper rejection, and no retuning after gate failure. |
| `ed63799a9e88a98d03842f013fd244c2ebfb5230` | `workstreams/arxiv_v1/story/work-i-story-architecture-v0.1.md` | `de686d923df53c3754694eb2dca9550b1fc9fb6877848654760b73507dda4f9b` | Figure 2's unique narrative job, evidence ceiling, primary/retest separation, and section ownership. |
| `96f35a70888cce2b24a26b8f8f2434b403be3463` | `workstreams/arxiv_v1/reports/work-i-platform-surface-v0.1.json` | `f9ad46d399bfde37389d8e93a2846a92b98e2ee405a11b04db0beef53485ba59` | F09 apparatus boundary: registered executable platform scope is not formal agent performance or physical-laboratory validation. |
| `ffa507e68813600155e5291afaa63711350d88d0` on reviewed branch head `4a71667cd56a71abb6003478205b3bf8b5719f31` | `workstreams/arxiv_v1/reviews/W1-Q04-chemistry-review--Yijun.md` | `d236cea8e44f53b4e65ba7dc73749b8b83b889ce316af3c4e88405fc4fd517cb` | Independent approval of V only as bounded simulated construct/discriminant evidence and rejection of chemistry, competence, or physical-transfer promotion. |
| `fd12304c5592694e17a98b6ba230f213d101ba24` | `workstreams/arxiv_v1/story/work-i-claim-evidence-figure-map-v0.1.md` | `661e2bd05c23da524629cc420b23ff33ec4a88a29df0d8b3363be4da3980da8b` | Claim routing for VALID-01--05, analysis units, Figure 2 panels, and forbidden interpretations; referenced from the isolated W1-S01 review branch. |

## Integration locks

- Preserve “5 worlds × 2 information arms × 3 policies,” “30 primary campaign
  profiles,” and “180 primary closed lifecycles” as three different counting units.
- Keep the 30 deterministic retest campaigns / 180 retest lifecycles outside the
  primary estimand everywhere, including captions and derived-data labels.
- Describe the controls as policies, never agents, systems, models, or chemistry
  baselines.
- Keep endpoint values and all registered non-orderings descriptive; do not derive a
  unified ranking or scalar from Figure 2.
- Describe matched-arm equality as an interface/pairing check, not a causal
  information-null result.
- Use “simulated apparatus,” “executable simulator,” or “state-coupled synthetic
  instrument”; do not use “calibrated instrument,” “physical replay,” “chemical
  intelligence,” “agent competence,” or “laboratory transfer” as established results.
- Do not rerun, recompute, reselect, retune, or overwrite the frozen fresh-session
  results. This section neither consumes nor changes those results.
