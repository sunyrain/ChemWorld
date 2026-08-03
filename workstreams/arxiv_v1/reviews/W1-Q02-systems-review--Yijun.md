# W1-Q02 independent systems review

- Reviewer: `Yijun`
- Reviewed merged baseline: `9548e0afb32e4b01064e0c6e7c8dffa8c54389fe`
- L03 implementation commit: `e785329e3b9adc005d75971a0a3f409c64c68db3`
- D01 contract commit: `59845a6fc5bea277a6f641919d42859715ab7bc6`
- Review date: `2026-08-03`
- Overall verdict: **CHANGES_REQUESTED**
- Outcome boundary: read-only source/report review and synthetic/focused checks only. No formal checkpoint payload or latent discard score was read, no formal shadow terminal was executed, and no agent/provider was called.

The L03 evaluator-only branch is usefully isolated and its committed synthetic mechanism qualification is deterministic. The D01 schema/counting contract is self-hashed and deterministically rebuilt. Neither surface is ready for downstream consumption, however: L03 does not exact-bind the runtime full resource-ledger history or the prefix keyed-noise receipt chain, while D01 declares the affected review-pending L02/L03 artifacts immutable and frozen for D03. The findings below are bounded to those system gates.

## Reviewed evidence bindings

| Surface | Path | File SHA-256 | Verdict |
| --- | --- | --- | --- |
| L01 frozen contract | `configs/benchmark/work_i_latent_terminal_contract_v0.1.json` | `e69db432f7018a3cc41287fa02335337c624caf5ba7f0b487a0695809e052ce5` | approved upstream contract |
| L02 reconstructability report | `workstreams/arxiv_v1/reports/work-i-latent-terminal-reconstructability-v0.1.json` | `ec18b041543f44b9c2d2f16ee56a08da727efbe0128622778a8ae6d688afcba3` | upstream **CHANGES_REQUESTED** |
| L03 replay implementation | `src/chemworld/eval/latent_terminal_replay.py` | `cfb5e0fee22d021e8c503f570af7252de9c7ccee02cb87b4f30a428b0d8e0927` | **CHANGES_REQUESTED** |
| L03 qualification builder | `scripts/qualify_work_i_latent_terminal_replay.py` | `2d14ff5b65e04bcf904858f69961d6a0426bf4896377a62dec69edf4e292f267` | **CHANGES_REQUESTED** |
| L03 tests | `tests/test_latent_terminal_replay.py` | `1ebf754a35c2fcb40487af9cff128a275cee663312d32204f2b1224e817bc92f` | reviewed |
| L03 qualification report | `workstreams/arxiv_v1/reports/work-i-latent-terminal-replay-qualification-v0.1.json` | `ac3023715ab027221887b5a0b3404a655064939444c63241e9459a88c2cbcde5` | synthetic mechanism evidence only |
| D01 contract implementation | `src/chemworld/eval/work_i_data_contract.py` | `7ebf77d4c5a8368eb94593264ee13ec34bd1afa28111bfb0c77f3f71a2a94efd` | **CHANGES_REQUESTED** |
| D01 builder | `scripts/build_work_i_data_contract.py` | `8f466ed0d3049562eb37dd16cc028d3c795db91cd73e2eddc61e37a6f8daf607` | reviewed |
| D01 tests | `tests/test_work_i_data_contract.py` | `7c330e9ce8db1bd34b7377c1a8dd7d5d51c357f8dfe9c6e4102f677c962ad978` | reviewed |
| D01 machine contract | `configs/benchmark/work_i_incremental_data_contract_v0.1.json` | `9ba95bb0d64d188d381f95184c21257cc677cab0e609b0a74cb7c1b326f219f8` | **CHANGES_REQUESTED** |
| D01 human report | `workstreams/arxiv_v1/reports/work-i-incremental-data-contract-v0.1.md` | `7d3d38b4e936bb3d9e3714a7b9ba1e999ae203abf1f5877746ab81017fcae1ff` | **CHANGES_REQUESTED** |

The independent Q01 review at commit `662159f008ba663e473ddb532274498474add61f` (review file SHA-256 `9efc13a9fa919f7d0751073df2a23c47eaa9e45558d6018a649a3aa6c48d6881`) requests changes to L02 because tolerant numeric comparison and the absence of an independently exact-bound historical keyed-noise receipt do not satisfy L01's exact-prefix entry rule. This is an upstream gate; it is not substituted for the separate L03 findings below.

## W1-L03 — CHANGES_REQUESTED

### Mechanism facts that pass

- The replacement path calls the isolated observation kernel directly rather than `env.step`, permits only `measure_final_requires_terminated`, checks final-assay resource preflight, and requires a finite score in `[0,1]` (`src/chemworld/eval/latent_terminal_replay.py:306-405`).
- The branch deep-copies the observation kernel and hidden state, hashes a broad before/after mutation surface, and reports zero agent/provider calls (`src/chemworld/eval/latent_terminal_replay.py:126-161`, `:352-460`).
- The committed report is self-hashed, contains two identical synthetic terminal identities, reports zero formal checkpoint/outcome access, and keeps L05 as formal owner. The existing focused tests and qualification checks pass on the reviewed baseline.
- Constant contract paths are repository-relative and resolved from the supplied repository root; no caller-controlled filesystem path is accepted by the L03 evaluator.

These are valid synthetic mechanism checks. They do not close the following exact-identity gaps.

### Finding L03-1 — runtime full ledger/event history is not exact-bound

`capture_prefix_identity` validates that the supplied authoritative snapshot is internally replayable, reads its `ledger_sha256`, and compares only `canonical_json_sha256(resources["state"])` between the runtime and authoritative snapshots (`src/chemworld/eval/latent_terminal_replay.py:187-205`). It then assigns the authoritative hash directly to `campaign_resource_snapshot_sha256` (`:214-236`). It never computes or compares the runtime snapshot's full `ledger_sha256`, whose canonical payload includes the card, state, ordered events, and `last_event_id` (`src/chemworld/campaign_resources.py:666-675`). Therefore a runtime ledger with the same aggregate state but a different valid event history can inherit the authoritative full-ledger identity and pass this gate.

The current negative probe changes the expected identity field while using the same runtime snapshot as the authoritative snapshot (`scripts/qualify_work_i_latent_terminal_replay.py:250-294`); it does not exercise same-state/different-history input.

Minimum remediation:

1. Recompute the runtime full snapshot hash and require exact equality with the independently reconstructed authoritative `ledger_sha256` before scoring. Bind the runtime hash, event count, and last-event identity in the prefix receipt rather than copying an unverified authoritative value.
2. Add a fail-closed negative test using two canonically valid ledgers with equal aggregate `state` but different ordered event history/card/last-event identity; terminal evaluation must be rejected before observation.

Gate impact: this is an L03 identity defect. Even after L02 is repaired, W1-L05 must not execute formal shadow terminals until this negative test and regenerated L03 qualification pass.

### Finding L03-2 — prefix keyed-noise/checkpoint receipt chain is absent from identity

`PREFIX_IDENTITY_FIELDS` binds only observation seed, mode, and namespace for prefix noise (`src/chemworld/eval/latent_terminal_replay.py:48-72`). It does not bind the L02 `checkpoint_identity_sha256`, raw/source trajectory identity, occurrence ordinals, or an exact aggregate/hash chain of every prefix keyed-noise receipt. `assert_exact_prefix_identity` consequently cannot reject a receipt-chain mismatch (`:258-279`). The qualification's `terminal_noise_key_reused_exactly` gate compares only the newly generated shadow final-assay key across two synthetic evaluations (`scripts/qualify_work_i_latent_terminal_replay.py:320-325`); it does not establish exact identity of historical prefix-noise receipts.

Minimum remediation:

1. After the bounded L02 correction, require and verify the accepted L02 report/source hash, the unit's `checkpoint_identity_sha256`, exact prefix keyed-noise receipt-chain digest (including operation/lifecycle coordinate and occurrence ordinal), and frozen L01 unit membership before scoring.
2. Require the expected prefix self-hash rather than treating it as optional, recompute it from the accepted fields, and reject missing/stale receipt bindings.
3. Add negative tests for noise namespace, seed, operation coordinate, occurrence ordinal, receipt-chain digest, checkpoint identity, and removal of a mandatory self/source binding.

Gate impact: this is distinct from Q01's L02 defect. L02 must first publish an independently reconstructed exact receipt chain; L03 must then consume and fail-closed bind it. Until both reviews close, the 36/36 exact-prefix entry rule and W1-L05 remain blocked.

## W1-D01 — CHANGES_REQUESTED for final freeze; schema/counting mechanics approved

### Contract facts that pass

- The machine contract self-hashes to `e3a941c5a4d958b8284a244947a4c3e1b4ae3639576d12e27a005dbb9baa363c` and binds seven inputs by embedded and file hashes.
- F/V/L primary units are kept distinct; exact replay, deterministic retest, synthetic qualification, and evaluator shadows do not inflate primary denominators. The L census remains 60 terminal lifecycles, 36 discards, 24 observed assays, and nine oracle-opportunity cells with `cell-02` null.
- JSON-null/nonfinite rules, source-row hashes, duplicate-key fatality, provider-zero accounting, immutable-manifest requirements, and the prohibition on raw hidden/provider payloads are explicit.
- `validate_work_i_data_contract(..., root=...)` deterministically rebuilds the contract and rejects source/hash/schema/counting changes (`src/chemworld/eval/work_i_data_contract.py:782-850`). The focused tests and deterministic builder check pass on the reviewed baseline.

The schema/counting freeze is therefore sound as a pre-outcome interface draft. The disposition fails only because the same artifact presents review-pending L bindings as a final immutable freeze.

### Finding D01-1 — review-pending L02/L03 inputs are prematurely immutable/frozen for D03

The source registry labels L02 and L03 as `immutable_outcome_blind_audit` and `immutable_synthetic_qualification` (`src/chemworld/eval/work_i_data_contract.py:60-83`). The builder requires only their internal status/count/outcome-boundary gates, not independent review acceptance (`:179-286`), then emits `status: frozen`, `mutable_after_freeze: false` (`:651-678`) and requires D03 to bind this contract hash (`:756-768`). At this reviewed baseline, L02 is already **CHANGES_REQUESTED**, and L03 is **CHANGES_REQUESTED** above. Their necessary remediation will change the source/report hashes and deterministically stale the current D01 contract.

Minimum remediation:

1. Preserve the approved schema, units, counting, nullability, and D03 boundary, but mark the current L source snapshot as review-pending/provisional and explicitly forbid D03 from treating hash `e3a941c5...` as its final frozen L input.
2. Once corrected L02 and L03 have independent approval, generate a versioned refreeze with updated source/file hashes and an explicit review-acceptance gate. Because the current artifact declares itself immutable, do not silently rewrite its identity; retain it as a superseded pre-outcome snapshot or version the replacement.
3. Regenerate the human report and add a test that a source with unresolved review disposition cannot be emitted as the D03-consumable final freeze.

Gate impact: D01's present contract may guide schema implementation, but W1-D03 must not consume its hash as final. L02/L03 fixes proceed under their own claims; after approval, D01 must refreeze before D03 assembly. This D01 disposition does not itself authorize or execute W1-L05.

## Validation disposition

- L03 focused tests, deterministic qualification check, and Ruff: PASS on the reviewed merged baseline (coordinator rerun).
- D01 focused tests, deterministic contract check, and Ruff: PASS on the reviewed merged baseline (coordinator rerun).
- Source/report file hashes: verified above.
- Reviewed implementation commits are present in the merged baseline.
- Formal checkpoint payloads loaded: `0`.
- Formal shadow terminal evaluations executed: `0`.
- Formal latent discard scores accessed: `0`.
- Agent/provider calls: `0`.
- Review write set: only this report and `workstreams/arxiv_v1/claims/W1-Q02--Yijun.md`.

## Final disposition

- W1-L03: **CHANGES_REQUESTED**.
- W1-D01 schema/counting mechanics: **APPROVE**.
- W1-D01 final immutable source freeze: **CHANGES_REQUESTED**.
- W1-Q02 overall: **CHANGES_REQUESTED**.

No L05 formal shadow execution or latent-dependent main-text entry is permitted until L02 and L03 are independently approved. No D03 final derived-data layer may bind the current D01 hash until the corrected, approved L inputs are version-refrozen.
