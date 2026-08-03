# W1-Q01 independent protocol review

- Reviewer: `Yijun`
- Reviewed baseline: `b4c643dbd65af934b40678e5c82f63fdcdefeef8`
- Review date: `2026-08-03`
- Overall verdict: **CHANGES_REQUESTED**
- Outcome boundary: read-only protocol and source review; no formal shadow terminal was executed, no latent discard score was read, and no agent/provider was called.

The world-fork protocol, known-policy measurement-validity protocol, and corrected latent-terminal contract are approved within their stated boundaries. The L02 reconstructability audit is not approved for the frozen `36/36 exact pre-discard prefix reconstructions` evidence-entry rule because its implementation admits numeric drift and does not independently exact-bind a historical keyed-noise receipt. L03 replay implementation and L04 synthetic analysis qualification may continue, but L05 formal shadow execution and any latent-dependent main-text claim remain gated on the bounded L02 remediation below.

## Reviewed evidence bindings

| Surface | Artifact | File SHA-256 | Verdict |
| --- | --- | --- | --- |
| Apparatus inventory | `workstreams/arxiv_v1/reports/work-i-platform-surface-v0.1.json` | `f9ad46d399bfde37389d8e93a2846a92b98e2ee405a11b04db0beef53485ba59` | supporting evidence |
| Experiment semantics | `workstreams/arxiv_v1/reports/work-i-experiment-semantics-v0.1.json` | `cce0455d11d8081a57007fc5ec47e5988bfe3c8cf9dfb1f67da583c82c7350cc` | supporting evidence |
| World fork | `workstreams/arxiv_v1/reports/work-i-world-fork-certificate-v0.1.json` | `8a0299b6957a700e720f46401a62b30a1da4ac2f8d71d57f00071805abcf9ad9` | **APPROVE** |
| Known-policy validity | `workstreams/arxiv_v1/reports/work-i-known-policy-validity-report-v0.1.json` | `58458670f1db62a1f048a778539e054131a125941ff04fa38d5892d27c382dee` | **APPROVE** |
| L01 corrected contract | `configs/benchmark/work_i_latent_terminal_contract_v0.1.json` | `e69db432f7018a3cc41287fa02335337c624caf5ba7f0b487a0695809e052ce5` | **APPROVE** |
| L02 reconstructability report | `workstreams/arxiv_v1/reports/work-i-latent-terminal-reconstructability-v0.1.json` | `ec18b041543f44b9c2d2f16ee56a08da727efbe0128622778a8ae6d688afcba3` | **CHANGES_REQUESTED** |
| L02 validator source | `src/chemworld/eval/latent_terminal_reconstructability.py` | `80466f9a778f1c497ac3ac4871830b39dc429521361fa62e311c4aa965f4ca5a` | reviewed |
| L02 tests | `tests/test_latent_terminal_reconstructability.py` | `1c343e4383d9f3e5afb602320a31fb14bcd9a47f51dab8b912965111f8aae096` | reviewed |

The L01 machine contract is additionally self-bound by `contract_sha256=55a0d6a7cb983ce4099dbea24586ea63ccc9433e106d36011d349472809efe30`; the L02 report is self-bound by `report_sha256=995f16032de09044ecf11a54b7d6fef9f0b3463eab2dad331adc52f7c4533857`.

## Requirement-by-requirement verdicts

### World-fork protocol — APPROVE

| Requirement | Verdict | Review finding |
| --- | --- | --- |
| Pre-outcome freeze | PASS | The intervention families, parent-child bindings, public-contract preservation surface, deterministic probe, divergence criteria, and replay checks were frozen before qualification results. |
| Single-component identity | PASS | The certificate binds a parent and child differing in one registered private component while preserving the nine declared public-contract components. |
| Replay and provider boundary | PASS | Qualification reports six parent-child pairs and 24 original/replay traces with exact replay and zero provider calls. |
| Estimand/analysis unit | PASS | The unit is the registered parent-child pair under a fixed deterministic policy; trace count is execution accounting, not independent agent evidence. |
| Claim boundary | PASS | The admissible claim is controlled programmability of the executable apparatus. It does not establish agent adaptation, law learning, physical transfer, or arbitrary world authoring. |

### Known-policy measurement-validity protocol — APPROVE

| Requirement | Verdict | Review finding |
| --- | --- | --- |
| Pre-outcome policy freeze | PASS | Three deterministic policy signatures, expected nulls/orderings, resources, matched-arm invariance, and entry gates were registered before the formal matrix. |
| Construct before aggregation | PASS | Terminal commitment, evidence acquisition, evidence-conditioned action, resource deployment, and outcome trajectory remain separate profile coordinates before aggregation. |
| Analysis unit and reliability | PASS | The primary unit is an equally weighted campaign profile; same-identity retests are reliability checks and are excluded from the primary estimand. |
| Discriminant and claim boundary | PASS | The protocol is a bounded construct/discriminant-validity positive control, not an endpoint leaderboard, scalar intelligence score, provider capability test, or causal information-effect study. |
| Resource, identity, and replay gates | PASS | The frozen report binds the schedule, runner qualification, resources, world/noise identities, profile recovery, matched-arm invariance, and same-identity retests with zero providers. |

### Latent-terminal L01 contract — APPROVE

| Requirement | Verdict | Review finding |
| --- | --- | --- |
| Outcome-blind population freeze | PASS | The finite population is frozen as 60 DeepSeek lifecycles: 24 observed assays plus all 36 discards. The contract records zero latent-outcome and hidden-pre-discard-state reads during freeze. |
| Estimands and denominators | PASS | All eight estimands are defined. The discard denominator is 36, lifecycle selection denominator is 60, campaign-oracle regret uses the nine discard-opportunity cells, and `cell-02` remains an explicit no-opportunity null rather than zero. |
| Thresholds and decision timing | PASS | Primary quality is inclusive `score >= 0.90 B_c`; `0.80 B_c`, `1.00 B_c`, and absolute `0.58` are registered sensitivity rows. Decision-time regret uses only the incumbent available before the discard and retains a null when none exists. |
| Missingness/censoring | PASS | Unresolved shadows fail closed; complete-case substitution, favorable reruns, clamping, and semantic repair are forbidden. All estimands retain registered bounds and all-zero/all-one sensitivity endpoints. |
| Evidence entry and claim boundary | PASS | Main-text latent quantities require 36/36 exact prefix reconstructions, 36/36 valid scores, 36/36 exact same-identity shadow replays, zero providers, and no original trajectory/ledger mutation. No result-direction or significance gate exists. |

### Latent-terminal L02 reconstructability — CHANGES_REQUESTED

The committed audit is valuable and outcome-blind: it exact-hashes all 53 indexed raw files and 127,883,533 bytes, covers all 36 discard units, reconstructs campaign-resource prefixes, performs two deterministic checkpoint captures per cell, emits only hashes, executes zero shadow terminals, reads zero latent scores, and calls zero providers. Those facts are approved as reconstructability evidence. They do not yet prove the stronger L01 exact-prefix entry rule for these reasons:

1. `src/chemworld/eval/latent_terminal_reconstructability.py:485` fixes trajectory tolerance at `1.0e-5`; reward and public-observation differences pass when they are at or below that tolerance (`:540-575`), and structured numeric audit fields use the same tolerance (`:615-620`). The committed report happens to record `max_abs_error=0.0`, but the validator's acceptance condition is not exact and therefore permits a future or tampered report generated with nonzero drift.
2. The checkpoint hashes `last_observation_noise_sha256`, but the current gate only compares two newly reconstructed checkpoints through `checkpoint == repeat` (`:783`). Historical identity checks bind noise mode, namespace, and seed (`:642-658`); they do not independently derive an expected keyed-noise receipt from the frozen public coordinate and exact-compare it with the replay receipt. The public compact record does not itself persist the full receipt, so the report must not describe this as a direct comparison with a previously stored historical receipt.
3. `tests/test_latent_terminal_reconstructability.py` rejects aggregate gate and outcome-boundary tampering, but it has no negative case for a sub-`1e-5` observation/reward drift or for a keyed-noise coordinate/receipt mismatch.

## Bounded remediation required for L02 approval

1. Replace tolerant trajectory acceptance with exact canonical equality (or exact canonical hashes) for every recorded reward, public observation, and numeric structured prefix field covered by the L01 identity rule. Retain diagnostic absolute errors if useful, but no nonzero error may pass the exact gate.
2. Independently derive the expected keyed-noise provenance from the frozen recorded coordinate inputs—at minimum namespace, observation seed, operation/lifecycle coordinate, and occurrence ordinal—and exact-bind that expected receipt to the replayed receipt at every prefix observation. Publish only the receipt/provenance hashes needed for audit. State explicitly that this is deterministic reconstruction from persisted coordinates, not comparison to an unavailable historical receipt payload.
3. Add fail-closed unit/report gates and negative tests for: a nonzero numeric drift smaller than `1e-5`; namespace, seed, operation coordinate, and occurrence-ordinal tampering; replay receipt hash tampering; and removal or falsification of the new exact gates.
4. Regenerate the machine and human L02 reports, update their self/source hashes, rerun the focused tests, Ruff, Mypy, deterministic report check, and `git diff --check`, then request independent re-review.

Until those items pass, report L02 as “deterministic state/resource reconstruction with zero observed replay error under the current audit,” not as final proof of the frozen 36/36 exact prefix-and-keyed-receipt entry gate. This finding does not authorize reading latent outcomes or executing formal shadow assays.

## Review disposition

- World fork: **APPROVE**
- Known-policy measurement validity: **APPROVE**
- L01 corrected latent-terminal contract: **APPROVE**
- L02 reconstructability audit: **CHANGES_REQUESTED**
- W1-Q01 overall: **CHANGES_REQUESTED** because one reviewed protocol surface remains below its own pre-registered entry rule.

