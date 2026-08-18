# Work II A-S open-action single-world three-arm development pilot

Status: user-authorized development run; not formal evidence and not part of the W2-48 denominator.

## Question

With one persistent agent session per arm, after twelve open-ended partition experiments, can the
agent rank and select one of eight newly revealed complete ActionPlans when candidate outcomes,
hidden ranks, checkpoint truth, and other arms' evidence remain hidden? The three arms are
`opaque`, `aligned_nominal`, and `misindexed_nominal`.

## Frozen pilot units and coverage

- One world seed: `153150025`.
- Candidate packet seed: `400`.
- Three persistent sessions, one per arm; twelve participant experiments per session.
- Five belief checkpoints: `0/3/6/9/12`.
- Eight candidates, selected before truth execution from the 128-query pool by deterministic
  packet-hash permutation with eight distinct material pairs, two candidates per volume regime,
  and four candidates per mixing regime.
- Participant workflow remains open: operation order, intermediate measurements, phase separation,
  reagent use, and parameters are chosen by the agent within the host feasibility/resource contract.

## Measurements and binding gates

- Terminal task is ranking-only: rank all eight candidates exactly once and select the first.
- Each public candidate contains the complete ordered operation list, every parameter, initial-state
  contract, measurement positions, terminal assay, workflow family, omitted optional operations,
  objective, and metric IDs; no candidate outcomes, ranks, truth, or other-arm evidence are public.
- The exact public `action_plan` is passed to evaluator truth and replay. Public, compiled-truth, and
  executed trajectory action-plan hashes must agree.
- Provider-free checkpoint and candidate truth/replay are completed before provider sessions.

## Pass/failure and retention

- All three cells, all failures, exact replay, resource usage, provider receipts, and final
  recommendations are retained.
- A failed cell is not replaced or rerun because its outcome is unfavorable.
- The pilot is diagnostic only; it cannot authorize or populate the five-world formal denominator.

## Expected outputs

One input manifest, deterministic public candidate packet, provider-free truth/replay receipts,
three cell records, a machine-readable summary, progress log, and Chinese report.
