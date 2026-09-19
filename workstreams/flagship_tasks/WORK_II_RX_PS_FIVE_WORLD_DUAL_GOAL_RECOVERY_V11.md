# Work II RX P/S five-world dual-goal recovery v11

## Scope

Recovery v10 attempted every remaining scheduled cell and retained seven nonconforming outcomes after the remote Codex provider connection entered a reconnecting state. The frozen scientific design, prompts, seeds, 12-batch budget, K1/Q/K2 order, scoring contract, and truth embargo remain unchanged.

## Diagnosed platform fault

The remote runner depends on `HTTP_PROXY`, `HTTPS_PROXY`, and `ALL_PROXY` at `127.0.0.1:7897`, supplied by the Mac SSH reverse forward. The durable reverse-forward session was absent when the reconnect storm occurred. Account login remains valid and the account is not quota-limited. Before v11, a persistent SSH control-master tunnel was established with `ExitOnForwardFailure`, 30-second keepalives, and three missed-keepalive tolerance. The remote listener and an HTTPS request through the proxy were verified.

## Authorized repairs

- Preserve all original v10 directories, results, receipts, and provider failures as write-once evidence.
- Re-run K1, Q, and K2 in order, on the archived original source thread and without new experiments, for the two cells whose 12-batch source completed:
  - `RX-W04--S--safety_constrained_optimization--MisIndexed`
  - `RX-W05--S--mechanism_discovery--Opaque`
- Re-run the entire frozen source cell from batch 1 in a nested `source-repair-v11` directory for the five cells whose source was interrupted by the same provider transport fault:
  - `RX-W05--S--mechanism_discovery--Aligned`
  - `RX-W05--S--mechanism_discovery--MisIndexed`
  - `RX-W05--S--safety_constrained_optimization--Opaque`
  - `RX-W05--S--safety_constrained_optimization--Aligned`
  - `RX-W05--S--safety_constrained_optimization--MisIndexed`
- Use four isolated workers, matching the active block's frozen recovery concurrency. Continue attempting the queue after an individual cell failure.
- Do not create or expose reference truth until all 60 effective cells have sealed 12-batch sources and valid K1/Q/K2 chains.

## Acceptance criteria

Recovery is complete only when the effective matrix is 60/60 cells, 720/720 source batches, and 60/60 sealed K1/Q/K2 chains. Any further provider failure remains preserved and keeps truth embargoed.
