# Work I Task Claim

```yaml
task_id: W1-V07
title: "Qualify the known-policy matrix runner and freeze the formal protocol"
status: DONE

owner: codex-1
collaborators:
  - "agent:/root/w1_v07"
claimed_at_utc: 2026-08-03T08:24:08Z
lease_expires_at_utc: 2026-08-05T08:24:08Z
heartbeat_at_utc: 2026-08-03T09:56:14Z

base_commit: "82051ba99fe82fb432e5459c2dc372839d8db5a4"
branch: work1/w1-v07-byte-rebuild-correction
worktree: ../ChemWorld-W1-V07
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-V07--codex-1.md
  - src/chemworld/eval/policy_validity_qualification.py
  - src/chemworld/eval/policy_validity_matrix.py
  - src/chemworld/eval/policy_validity_audit.py
  - scripts/qualify_work_i_policy_controls.py
  - configs/benchmark/work_i_policy_control_matrix_v0.1.json
  - configs/benchmark/work_i_policy_control_qualification_v0.1.json
  - configs/benchmark/work_i_policy_control_formal_qualification_receipt_v0.1.json
  - tests/test_policy_validity_qualification.py
  - tests/test_policy_validity_matrix.py
  - tests/test_policy_validity_audit.py
  - workstreams/arxiv_v1/reports/work-i-policy-control-matrix-runner-preflight-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-policy-control-runner-qualification-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-policy-control-runner-qualification-v0.1.md
  - workstreams/arxiv_v1/reports/work-i-policy-control-runner-qualification-v0.1/**
shared_hot_file_requests:
  - "GRANTED by coordinator at 2026-08-03T08:42:54Z: src/chemworld/eval/policy_validity_matrix.py and its task-local test/preflight, solely to correct the qualification-discovered native material-information identity binding before protocol freeze."
  - "GRANTED by coordinator at 2026-08-03T08:47:00Z: src/chemworld/eval/policy_validity_audit.py and its task-local tests, solely to make the independent native adapter bind that corrected digest to the frozen bundle cell descriptor before its SHA is frozen in the V07 receipt."
  - "GRANTED by coordinator at 2026-08-03T09:28:53Z: configs/benchmark/work_i_policy_control_matrix_v0.1.json, solely to freeze and bind the exact CPython, NumPy, SciPy, platform/wheel, and uv.lock identity required for byte-exact V07 qualification and subsequent V08 formal execution; no scientific protocol field may change."

deliverables:
  - Outcome-free qualification of the exact V05 runner through an injected synthetic 5 x 2 x 3 matrix with identities explicitly distinct from formal chemical worlds.
  - V06 audit PASS over the native immutable V05 qualification manifest, including construct, resource, replay/retest, arm-invariance, null, ordering, and non-degeneracy gates.
  - Live controller/interface smoke on fixed nonformal seed 20000 for both arms and all three policies, with original/retest identity and zero-provider verification.
  - Immutable qualification manifests, hashes, byte counts, source bindings, and explicit exclusion from the 30-campaign/180-lifecycle formal estimand.
  - Self-hashed V05-compatible W1-V07 receipt freezing formal protocol, preflight, source, controller, auditor, and qualification-evidence bindings.
  - Fail-closed W1-V08 entry gates with no seed, threshold, estimand, stopping-rule, or acceptance-rule retuning after qualification.
validation:
  - uv run --isolated --frozen --python 3.11.15 python scripts/run_work_i_policy_controls.py --config configs/benchmark/work_i_policy_control_matrix_v0.1.json --preflight --check
  - uv run --isolated --frozen --python 3.11.15 python scripts/qualify_work_i_policy_controls.py --config configs/benchmark/work_i_policy_control_qualification_v0.1.json
  - uv run --isolated --frozen --python 3.11.15 python scripts/qualify_work_i_policy_controls.py --config configs/benchmark/work_i_policy_control_qualification_v0.1.json --check
  - uv run --isolated --frozen --python 3.11.15 pytest -q tests/test_policy_validity_contract.py tests/test_known_policy_contract.py tests/test_known_policy_threshold.py tests/test_known_policy_agents.py tests/test_policy_validity_matrix.py tests/test_policy_validity_audit.py tests/test_policy_validity_qualification.py
  - uv run --isolated --frozen --python 3.11.15 ruff check src/chemworld/eval/policy_validity_qualification.py scripts/qualify_work_i_policy_controls.py tests/test_policy_validity_qualification.py
  - uv run --isolated --frozen --python 3.11.15 mypy src/chemworld/eval/policy_validity_qualification.py scripts/qualify_work_i_policy_controls.py
  - Verify native live executions bind material_information_sha256 to the frozen canonical arm descriptor and reject a null, stale, or cross-arm digest.
  - Verify the independent V06 native adapter rejects null, stale, and cross-arm-swapped material-information digests even after all producer self-hashes are recomputed.
  - git diff --check
  - git diff --check 82051ba99fe82fb432e5459c2dc372839d8db5a4...HEAD

completed_since_last_heartbeat:
  - "Qualification discovery fail-closed exposed and corrected the pre-freeze V05 producer/V06 adapter material-information identity binding under coordinator reservations; null, stale, and cross-arm-swapped rehashed evidence is rejected."
  - "Pushed implementation hardening 9a65b0c8, deterministic preflight 5361cf7b, immutable artifacts/delivery manifest 1e09cb48, report/Markdown bfb16215, and formal receipt 7021e407."
  - "Complete injected synthetic V05 matrix passed every V06 gate: 30 campaigns, 180 closed lifecycles, 30 threshold assays, 30 threshold discards, and zero provider calls."
  - "Fixed seed-20000 nonformal smoke passed all gates: 6 original plus 6 exact retest campaigns, 36 plus 36 closed lifecycles, matched-arm invariance, and zero provider calls."
  - "Exact preflight and qualification byte rebuilds passed; full V01-V07 task-local suite passed 79 tests in 134.51s; ruff, mypy, both diff checks, and clean/upstream parity passed."
  - "Independent reviewer /root/w1_v07_review returned APPROVE: qualification --check passed in 27.4s; seven tamper negatives, ruff, mypy, preflight check, and diff checks passed; source/auditor/controller/preflight bindings agreed; formal environment/outcome counts were 0/0."
  - "Coordinator integration reproduced a byte-exact rebuild failure on main: semantic values differed only in non-frozen floating tails, but 19 generated artifact files changed bytes. No formal world or outcome was accessed."
  - "Correction froze the original CPython 3.11.15/NumPy 2.2.6/SciPy 1.17.1 apparatus, rebuilt the complete evidence chain, and proved byte equality across four fresh-process hash seeds without changing scientific payloads."
  - "Final validation passed 84 tests, preflight and qualification byte checks, ruff, mypy, diff checks, and main integration gates; formal environment execution and outcome reads remained 0/0."
current_validation: "DONE: main rejects the default CPython 3.12 apparatus before output/world/executor construction and passes exact preflight plus qualification byte rebuild under the frozen CPython 3.11.15 apparatus. Report SHA256 a8fe852d71dee311fc50211de7610d86855a64018ed29586bc5efa628b14ec9a; receipt SHA256 bb3b6170e654cd74122ff719ac9a01d55bc163e8f2ca57046245139d9d3c60fa; apparatus SHA256 e56f897906bfc2a345ba5d667ae08d87b07b3e886cf42a6cfbfb8383dbedb8d0."
files_touched:
  - src/chemworld/eval/policy_validity_qualification.py
  - src/chemworld/eval/policy_validity_matrix.py
  - src/chemworld/eval/policy_validity_audit.py
  - scripts/qualify_work_i_policy_controls.py
  - configs/benchmark/work_i_policy_control_qualification_v0.1.json
  - tests/test_policy_validity_qualification.py
  - tests/test_policy_validity_matrix.py
  - tests/test_policy_validity_audit.py
  - workstreams/arxiv_v1/reports/work-i-policy-control-matrix-runner-preflight-v0.1.json
  - configs/benchmark/work_i_policy_control_matrix_v0.1.json
  - configs/benchmark/work_i_policy_control_formal_qualification_receipt_v0.1.json
  - workstreams/arxiv_v1/reports/work-i-policy-control-runner-qualification-v0.1.json
  - workstreams/arxiv_v1/reports/work-i-policy-control-runner-qualification-v0.1.md
  - workstreams/arxiv_v1/reports/work-i-policy-control-runner-qualification-v0.1/**
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: null
next_24h: "Handoff complete; V08 may activate only from the pushed V07 DONE baseline and must consume the frozen apparatus and receipt."
handoff_eta: 2026-08-03T09:56:14Z

final_commit: "7f24e26bb19224717fc2df77a45482b0a9e3fb35"
reviewer: "/root/w1_v07_review"
review_result: "APPROVE: one concentrated blocking review covered c033abdb..7f24e26b; all 36 bundle scientific payloads match the original 3.11 lineage after removing apparatus-only fields, and every apparatus, resume, source, preflight, report, receipt, and delivery binding closes without a blocker."
notes: "The original work1/w1-v07-runner-qualification-freeze branch and rejected receipt remain preserved. Formal seeds 0-4 appear only as frozen schedule coordinates in injected synthetic artifacts; no formal environment, controller execution, or outcome was accessed. Synthetic identities remain explicitly qualification-only, and noise identity stays paired across information arms. The native producer and independent auditor bind material_information_sha256 to semantic_sha256(cell.material_information); null, stale, or swapped values remain invalid after rehashing. The original apparatus is frozen as CPython 3.11.15, cpython-311/cp311, NumPy 2.2.6 wheel SHA256 e8213002e427c69c45a52bbd94163084025f533a55a59d6f9c5b820774ef3303, SciPy 1.17.1 wheel SHA256 d30e57c72013c2a4fe441c2fcb8e77b14e152ad48b5464858e07e2ad9fbfceff, Windows win-amd64, and uv.lock SHA256 e79dbec48a50730499e96806b0ae7ccd989eaf67693009143b55901b6e2fc9b7. Four distinct PYTHONHASHSEED subprocesses produced byte-identical bundles/manifests, so hash seed is tested but not frozen. Hostname, paths, timestamps, CPU model, Windows patch, locale, uv version, and unrelated packages remain excluded."
```
