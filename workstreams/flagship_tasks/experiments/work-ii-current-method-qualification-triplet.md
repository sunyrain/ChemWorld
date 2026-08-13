# Work II current-method qualification triplet

Status: completed and passed on 2026-08-14; development qualification only.

## Question

Can the frozen formal participant method complete one matched three-arm discovery triplet with
the required persistent-session, operation-level, shared-resource, checkpoint, final-summary and
replay semantics before any formal participant outcome is collected?

## Tested units and coverage

- Task: electrochemical conversion.
- Development/qualification world seed: 0; excluded from every formal denominator.
- Prior arms: opaque, aligned nominal and misindexed nominal.
- One persistent Codex process/session per arm.
- Eight complete experiments and five typed belief checkpoints at experiments `0/2/4/6/8` per arm.
- Initial provider-process count: 3; hard cap: 6, allowing at most one infrastructure-only resume
  per arm.
- Operation-attempt hard cap: 168 across the triplet.

## Measurements

- Schema-valid and committed operation counts.
- Complete experiments, checkpoint coverage and lifecycle closure.
- Same-session identity across operations, checkpoints, final law summary and recommendation.
- Campaign-resource accounting, process-time use and closeout reserve.
- Provider attempts, tokens, reconstructed cost, wall time and failure classification.
- Exact physical replay, resource-ledger replay and hidden-boundary audit.

## Pass and failure rules

- All three arms must reach a valid qualification terminal state and satisfy the frozen method
  receipt; scientific outcomes are never used for selection.
- Any scientific or participant-method failure is retained and forbids replacement.
- A missing arm may resume only after a pure infrastructure failure with no persisted trajectory,
  and at most once.
- Any provider call without a pre-call authorization and cost reservation is forbidden.
- A failed triplet does not authorize the formal matrix; an implementation defect may be repaired,
  but a replacement qualification block must restart from all three arms under a new run root.

## Expected outputs

- Immutable three-arm development report and per-cell terminal receipts.
- Append-only provider-attempt and cost-reservation journal.
- Machine-readable qualification receipt binding the provider contract, pricing, token use,
  resource/replay audits and observed ETA.
- A concise human-readable qualification summary; raw provider responses remain outside Git.

## Result

The frozen triplet completed without replacement or retry. All three arms reached `8/8` complete
experiments and all five registered checkpoints (`24/24` experiments and `15/15` checkpoints in
total). Each arm used one provider attempt, with zero provider or infrastructure failures. Exact
replay passed for all three arms (`48` validated steps per arm, zero mismatches), and the terminal
qualification receipt passed with zero validation errors.

This closes only the current-method harness/lifecycle/replay gate. The run is excluded from every
scientific denominator and does not authorize formal participant execution. The incomplete W2-26
nine-task resource-calibration block and the release authorization remain separate gates.
