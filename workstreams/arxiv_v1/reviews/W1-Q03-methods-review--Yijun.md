# W1-Q03 independent methods and statistics review

- Reviewer: `Yijun`
- Reviewed supporting `origin/main`: `ff20fab5f912596077e449546965b9a65a520bd7`
- Reviewed L04 remote head: `e91300ad9f16d95d131894b7009814bbaaa1103e`
- L04 implementation/qualification commit: `9044f8b61ccdce0d1f9e04c63d018326bf798f9a`
- Review date: `2026-08-03` UTC
- Statistical estimand implementation: **APPROVE within synthetic/mechanical qualification**
- Formal evidence-ingestion and scientific-entry implementation: **CHANGES_REQUESTED**
- Overall W1-Q03 verdict: **CHANGES_REQUESTED**
- Outcome boundary: read-only source/report review, deterministic synthetic checks, and provider-free focused tests. No formal checkpoint payload or latent discard outcome was read, no formal shadow terminal was executed, and no agent/provider was called.

L04 correctly implements the frozen finite-population analysis mechanics: all eight estimands, the 36/24/60 denominators, the nine opportunity-cell campaign oracle with `cell-02` retained as null, registered thresholds, strictly prior decision-time incumbents, and unresolved-outcome bounds. The synthetic qualification is reproducible and appropriately says that it is not a formal result.

The formal public entry path is not yet evidence-authentic, however. It accepts score rows that contain none of the L02 checkpoint or L03 terminal-replay identities, treats six caller-supplied aggregate values as execution gates, and can mark arbitrary constructed scores as main-text eligible. In addition, failed formal execution gates do not make latent-dependent point estimates unavailable, and the exported structural validator cannot authenticate a rehashed analysis artifact. These are formal-readiness defects, not failures of the underlying estimand formulas.

## Reviewed evidence bindings

| Surface | Commit/path | File SHA-256 or embedded identity | Disposition |
| --- | --- | --- | --- |
| Frozen L01 contract | `configs/benchmark/work_i_latent_terminal_contract_v0.1.json` | file `e69db432f7018a3cc41287fa02335337c624caf5ba7f0b487a0695809e052ce5`; contract `55a0d6a7cb983ce4099dbea24586ea63ccc9433e106d36011d349472809efe30` | **APPROVE** |
| L02 reconstructability report | `workstreams/arxiv_v1/reports/work-i-latent-terminal-reconstructability-v0.1.json` | file `ec18b041543f44b9c2d2f16ee56a08da727efbe0128622778a8ae6d688afcba3`; report `995f16032de09044ecf11a54b7d6fef9f0b3463eab2dad331adc52f7c4533857` | prerequisite remains review-pending / **CHANGES_REQUESTED** upstream |
| L03 replay implementation | `src/chemworld/eval/latent_terminal_replay.py` | `cfb5e0fee22d021e8c503f570af7252de9c7ccee02cb87b4f30a428b0d8e0927` | prerequisite remains **CHANGES_REQUESTED** upstream |
| L03 synthetic replay qualification | `workstreams/arxiv_v1/reports/work-i-latent-terminal-replay-qualification-v0.1.json` | file `ac3023715ab027221887b5a0b3404a655064939444c63241e9459a88c2cbcde5`; report `14d0e3358fe4ae00b13e2705519e64f3b8a8644f987dd878b6814fc61247b10f` | mechanism qualification only |
| L04 analyzer | `e91300ad...:src/chemworld/eval/latent_terminal_analysis.py` | `3cd94f7609916877b33007dd7671c957acfcd96520f367a6ec95e2002f03f297` | **CHANGES_REQUESTED** for formal entry |
| L04 qualifier | `e91300ad...:scripts/qualify_work_i_latent_terminal_analysis.py` | `672f64682530bfac87e4d729f9abace79b769f1bb744ec549e38def8f85cdaa2` | synthetic mechanics **APPROVE** |
| L04 focused tests | `e91300ad...:tests/test_latent_terminal_analysis.py` | `cf522eee2a1bec1406a87641dd14bd7f70228c09b83df751ed5fa70a6ce73956` | 20/20 pass; formal negative surface incomplete |
| L04 machine qualification | `e91300ad...:workstreams/arxiv_v1/reports/work-i-latent-terminal-analysis-qualification-v0.1.json` | file `52ea78e38e2d71a2929c64bc6202c0c07fbf8be833ee1c5a44d8cfd390178d53`; report `f2113e77d8b3bca66f80ddd1e88d48c87bc25443ab52c29129f4aca4271747be` | synthetic mechanics **APPROVE** |
| V known-policy validity report | `workstreams/arxiv_v1/reports/work-i-known-policy-validity-report-v0.1.json` | file `58458670f1db62a1f048a778539e054131a125941ff04fa38d5892d27c382dee`; report `ebb56a052929944330acdf594e4a341c8c8fdb2b4ea2e276556384e7ce6b2064` | **APPROVE** within bounded construct validity |

The L04 remote head equals the fetched remote identity above and is clean. Relative to its ACTIVE-claim parent, its implementation history modifies only the six declared L04 paths. The only change after the claimed final implementation commit `9044f8b...` is the L04 handoff claim.

The independent prerequisite reviews are also material to formal readiness. Q01 report commit `662159f008ba663e473ddb532274498474add61f` (file SHA-256 `9efc13a9fa919f7d0751073df2a23c47eaa9e45558d6018a649a3aa6c48d6881`) requests exact L02 numeric and keyed-noise receipt remediation. Q02 report commit `ed35beb2dbe11d1172fa2ad218d261c94b692847` (file SHA-256 `6ddbffb065563551012898e9b83dca449c9b717caf3256c1d43df4330f747f77`) requests L03 full-ledger and prefix checkpoint/noise-chain binding. Neither prerequisite has a later implementation commit on its task branch, so there is not yet an independently accepted L02/L03 identity for L04 or L05 to consume.

## Requirement-level methods verdict

| Requirement | Verdict | Evidence and interpretation |
| --- | --- | --- |
| Eight frozen estimands | PASS | The exact L01 set is emitted: three discard-level continuous quantities, nine-cell campaign oracle regret, three classification quantities, and decision-time discard regret. |
| Frozen census and denominators | PASS | The analyzer enforces 10 cells, 60 closed lifecycles, 24 assays, and 36 discards; discard metrics retain denominator 36 and selection uses all 60 lifecycles. |
| Campaign oracle opportunity rule | PASS | Exactly nine cells contribute; `cell-02` remains in the ten-cell census with null point/bounds and is never assigned zero regret. |
| Threshold registration | PASS | Relative `0.80`, primary inclusive `0.90`, relative `1.00`, and absolute `0.58` rows are emitted; threshold equality is classified near-best. |
| Decision-time temporal rule | PASS | Only assays with `terminal_step < discard terminal_step` define the incumbent. Two pre-assay discards remain null; no future assay is imputed; denominator is 34. |
| Analysis unit and aggregation | PASS | Finite-population lifecycle micro summaries remain primary, cell macro summaries do not replace them, and world-paired arm contrasts remain descriptive. Campaign-oracle units are cells, not pooled lifecycle rows. |
| Missingness and censoring | PASS | Missing, non-finite, out-of-range, identity-mismatched, and explicitly unresolved inputs retain their frozen units, withhold affected primary points, expose reason strata, and produce all-zero/all-one and sharp support bounds. Complete-case substitution is not used. |
| Synthetic qualification boundary | PASS | Seven deterministic cases rebuild exactly; formal evaluations/outcomes and provider calls remain zero. This qualifies formulas only. |
| Formal receipt identity and provenance | **FAIL — Critical/blocking** | Formal rows need not contain or validate L02 checkpoint, hidden-state/resource, L03 replay, terminal-noise, scoring-contract, observation, or terminal-evaluation identities. Arbitrary scores can be accepted as formal. |
| Formal gate semantics | **FAIL — High/blocking** | Gate eligibility derives from six caller-supplied aggregate values rather than verified per-receipt facts. A failed gate correctly sets `main_text_eligible=false`, but does not make latent point estimates scientifically unavailable as required by L01. |
| Standalone analysis-artifact validation | **FAIL — Medium/blocking for downstream artifact-only consumption** | The exported function is explicitly structural and catches an unchanged self-hash, but after rehash it does not recompute unit/estimand/gate consistency. Qualification CLI regeneration remains sound; an L05/L06 consumer that relies only on this validator would not be sound. |

## Finding Q03-1 — formal receipts and gates are not source-bound

**Severity: Critical / blocks L05.**

`analyze_latent_terminal_population` is an exported public entry point. In formal mode, `_parse_unit` validates only contract/population identity, a string `fixture_kind`, discard/cell/world/arm/lifecycle/step, public-prefix hash, and original terminal-action hash. The accepted row uses a free `score` field. It does not require:

- the accepted L02 report identity or the unit's `checkpoint_identity_sha256`, `hidden_state_sha256`, resource snapshot/state/full-ledger identity, raw/source prefix identity, or exact prefix-noise receipt chain;
- the accepted L03 implementation/qualification identity, `prefix_identity_sha256`, `terminal_evaluation_identity_sha256`, replacement-action identity, `shadow_observation_sha256`, `noise_key_sha256`/provenance, scoring and observation contract hashes, or replay receipt schema/version;
- receipt-local proof that the original environment, prefix, trajectory, and resource ledger were unmodified, exactly one isolated evaluator observation occurred, and provider calls were zero.

The formal `execution_gates` parameter is a caller-supplied mapping. Six aggregate equality checks are enough to set `main_text_eligible=true`; none is derived from or linked to a receipt. The native L03 output also calls the scalar `leaderboard_score` and binds it inside `terminal_evaluation_identity_sha256`, whereas L04 accepts a separate unbound `score`. There is currently no formal L04 CLI or versioned adapter that proves these are the same value.

Reproduction through the exported entry point:

1. Build the committed 36 synthetic rows, change only `fixture_kind` to `formal_shadow_receipt`, and assign every free `score` to `0.999`.
2. Call `analyze_latent_terminal_population(..., mode="formal_shadow_analysis", execution_gates={the six required values})`.
3. Observed result: `resolved_shadow_receipts=36`, `main_text_eligible=true`, and `validate_latent_terminal_analysis(...) == []`, even though the input rows contain no L02 checkpoint field and no L03 replay/noise/score identity field.

Minimum remediation:

1. Define a versioned formal receipt schema that directly consumes the native L03 terminal receipt, or carries an immutable hash/reference to it. Derive the analyzed scalar from its identity-bound `leaderboard_score`; do not accept an independent free score.
2. Bind and validate the approved L01 contract, approved L02 report and exact unit checkpoint/receipt-chain identity, approved L03 implementation/qualification, formal execution manifest, source manifest, scoring/observation contracts, and every per-unit replay/noise/mutation/provider/resource gate before a score is resolved.
3. Derive aggregate gate counts from the 36 validated receipts. Remove caller-supplied truth values, or replace them with a self-hashed L05 manifest whose content and per-receipt references L04 independently verifies.
4. Add negative formal-mode tests for missing/stale/cross-unit/swapped/rehashed checkpoint, prefix, ledger, noise, replay, observation, score, receipt, dependency, and source identities. Each must fail before a latent point estimate can become available.

## Finding Q03-2 — failed formal execution gates leave latent point estimates available

**Severity: High / blocks scientific entry.**

L04 distinguishes `entry_gate.main_text_eligible`, which is correctly false on a failed gate, from analysis availability. However, `all_resolved` alone drives top-level `status` and every latent-dependent `point_estimate_status`. With 36 numeric rows and `original_trajectory_mutated=true`, the exported analyzer produced:

```text
status=complete
main_text_eligible=False
latent point_estimate_status=available
latent mean=0.48444444444444446
validator errors=[]
```

“Complete” can reasonably describe artifact generation, but L01's frozen failure rule additionally requires the terminal-quality result to be marked unresolved and forbids publication of a latent-dependent point estimate when any entry gate fails. Keeping the numbers in an artifact while only one Boolean forbids promotion creates an avoidable downstream misuse path.

Minimum remediation:

1. Separate `artifact_generation_status` from `scientific_result_status`.
2. Define scientific resolution as all 36 receipt-local scores resolved **and** every independently derived execution/identity gate passing.
3. When any formal gate fails, set every affected latent-dependent point estimate/status to unavailable/withheld and publish only the complete frozen failure audit and registered bounds. The observed-only assay precision may remain computed but must retain its existing non-promotable flag.
4. Add formal negative tests for every gate individually and assert status, point availability, bounds, and main-text eligibility together.

## Finding Q03-3 — a rehashed analysis artifact passes the structural validator

**Severity: Medium / blocks validator-only L06 consumption, but does not invalidate the synthetic qualification CLI.**

`validate_latent_terminal_analysis` describes itself as structural. It checks schema/version, the self-hash, frozen contract identifier, aggregate receipt counts, the set of eight estimand keys, one complete-case Boolean, 36 row count, and four threshold-row count. It does not recompute output from receipts or validate nested scientific consistency.

After changing a unit score/classification, the reported latent mean, a supplied provider-call gate, `main_text_eligible`, and the formal-outcome boundary, then recomputing `analysis_sha256`, the validator returned `[]`. This does **not** compromise `scripts/qualify_work_i_latent_terminal_analysis.py --check`, which deterministically rebuilds the synthetic report and compares exact bytes. It does mean the exported validator cannot serve as the authenticity gate for a formal artifact received by L06 or the paper layer.

Minimum remediation, choosing and documenting one ownership model:

- Preferred: validate a formal artifact together with its frozen contract, 36 source receipts, and accepted dependency manifest, deterministically rebuild the analysis, and require exact canonical equality.
- Acceptable split: rename/document this function as checksum/shape validation only and make every L05/L06 consumer invoke a separate source-bound semantic validator/rebuilder. No downstream code may treat `errors == []` from the structural validator as evidence validity.

In either model, add rehashed tamper tests covering unit identities/scores, thresholds, estimand summaries, bounds, null rules, gate fields, statuses, evidence bindings, and scientific-boundary fields.

## Frozen V construct/discriminant-validity check — APPROVE within bounds

The current V report establishes a bounded positive control for three deterministic known policies over five simulated worlds and two information arms. All 12 frozen gates pass, including exact signatures, conditional nulls, six partial orderings, resource expectations, matched-arm invariance, exact replay/retest identity, and threshold non-degeneracy (`28` assays, `32` discards for the threshold policy).

The primary estimand is one equally weighted original campaign profile: 30 campaigns and 180 closed lifecycles. The 30 same-identity retest campaigns and 180 retest lifecycles are reliability evidence only and are explicitly excluded from the primary estimand; lifecycle rows are not pooled before profile construction. The focused contract/replay/V-report run in this review passed 26 tests.

This supports construct/discriminant validity of the experimental-agency profile in the frozen simulator. It does not establish agent competence, endpoint superiority, a causal material-information effect, stochastic reliability, a scalar intelligence score, physical chemistry validity, or real-laboratory transfer.

## Downstream gates: implementation, formal execution, and paper use

### Implementation gate

- L04's synthetic statistical mechanics are approved and may be retained.
- L04 is not approved as a formal evidence-ingestion or artifact-authentication layer until Q03-1 through Q03-3 are remediated and independently re-reviewed.
- Q01's L02 and Q02's L03 changes remain separate upstream prerequisites; this report does not reopen or substitute for those reviews.

### Formal gate

- W1-L05 must not load formal checkpoint payloads, execute the 36 formal shadow assays, or freeze their receipts until corrected L02, corrected L03, and corrected L04 each have an accepted immutable identity and the L05 preflight binds all three.
- W1-L06 remains downstream of an accepted L05 receipt set and must use source-bound semantic reconstruction, not the current structural validator alone.

### Paper gate

- W1-S05 may proceed from the approved V evidence only, using campaign-profile units, bounded construct/discriminant language, and explicit retest exclusion. It may not import a latent-terminal result.
- W1-S06 may draft the preregistered latent-audit structure and failure/bounds language, but it must not publish latent-dependent point estimates, threshold conclusions, or `main_text_eligible` claims until L02-L06 close and Q03 findings are approved.
- A synthetic L04 qualification result is never a paper result.

## Commands and reproducible validation

```text
git fetch origin --prune
git ls-remote origin refs/heads/work1/w1-l04-latent-terminal-analysis
git rev-parse HEAD origin/work1/w1-l04-latent-terminal-analysis
sha256sum <reviewed L01-L04 and V paths>

PYTHONPATH=src /mnt/afs/home/liyijun/ChemWorld/.venv/bin/python \
  scripts/qualify_work_i_latent_terminal_analysis.py --check
# PASS; 7 cases; report_sha256=f2113e77...; formal executions/outcomes=0/false

PYTHONPATH=src /mnt/afs/home/liyijun/ChemWorld/.venv/bin/pytest -q \
  tests/test_latent_terminal_analysis.py
# 20 passed

PYTHONPATH=src /mnt/afs/home/liyijun/ChemWorld/.venv/bin/pytest -q \
  tests/test_latent_terminal_contract.py \
  tests/test_latent_terminal_replay.py \
  tests/test_policy_validity_report.py
# 26 passed

/mnt/afs/home/liyijun/ChemWorld/.venv/bin/ruff check \
  src/chemworld/eval/latent_terminal_analysis.py \
  scripts/qualify_work_i_latent_terminal_analysis.py \
  tests/test_latent_terminal_analysis.py
# All checks passed

# Exported-entry formal forgery probe
# observed: validator_errors=[]; main_text_eligible=true; resolved=36;
# no L02 checkpoint fields; no L03 replay/noise/score identity fields

# Failed-execution-gate probe
# observed: status=complete; main_text_eligible=false;
# latent point status=available; validator_errors=[]

# Rehashed nested-artifact tamper probe
# observed: validate_latent_terminal_analysis(rehashed_tamper) == []

git diff --check
```

The three probes used only synthetic rows and in-memory copies. They wrote no reviewed artifact, executed no world or shadow terminal, and accessed no formal outcome.

## Final disposition

- W1-V frozen construct/discriminant validity and retest exclusion: **APPROVE within the stated simulated positive-control boundary**.
- W1-L01 frozen estimands and entry rules: **APPROVE**.
- W1-L04 estimand, aggregation, null, threshold, and censoring mechanics: **APPROVE for synthetic implementation qualification**.
- W1-L04 formal receipt/gate binding, scientific availability semantics, and downstream artifact authentication: **CHANGES_REQUESTED**.
- W1-Q03 overall: **CHANGES_REQUESTED**.

No formal latent-terminal execution or latent-dependent paper entry is authorized by this review.
