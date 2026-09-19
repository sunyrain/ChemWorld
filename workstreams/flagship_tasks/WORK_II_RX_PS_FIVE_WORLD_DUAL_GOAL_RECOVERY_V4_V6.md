# Work II RX-P/S five-world block — recovery v4–v6 record

Date: 2026-09-19. Status: development recovery record; the 60-task block remains incomplete and truth-embargoed.

## Purpose and unchanged scientific contract

This record continues the write-once recovery described in
`WORK_II_RX_PS_FIVE_WORLD_DUAL_GOAL_RECOVERY_V3.md`. It does not change the frozen
60-task coverage, twelve-experiment source budget, K1/Q/K2 questions, query rows,
model, reasoning effort, public information, scoring contract, or truth-release rule.
Every failed receipt and partial recovery directory remains preserved. No reference
truth, prediction score, or recommendation-retest result was available to a resumed
agent.

The immediate target was `RX-W03--P--mechanism_discovery--Opaque`. Its twelve source
experiments and K1 were already valid; Q had no payload after a provider connection
failure, and K2 had timed out while repeatedly reconnecting. Recovery therefore reused
the archived original source thread and reran only Q and K2.

## Platform diagnosis and retained attempts

- **Recovery v4:** the first background launch did not inherit the login-shell path to
  `uv`; it exited before any model or experiment work. A corrected launch reached Q but
  had no usable outbound model connection. The partial Q attempt was retained.
- **Recovery v5:** HTTP/HTTPS proxy variables reached the Codex process, but the SSH
  reverse-forward listener on `127.0.0.1:7897` disappeared when the launching SSH
  connection ended. Direct server access to the OpenAI endpoint timed out. The Q attempt
  was terminated rather than waiting for the full turn deadline, and its logs were
  retained separately.
- **Recovery v6:** a persistent SSH tunnel was established before launch, and endpoint
  reachability was checked through the remote listener. The original thread then
  completed Q in 65.6 seconds and K2 in 109.9 seconds, with exit code zero, no provider
  errors, valid payloads, and unchanged prompts. This sealed task 25/60.

These events are platform recovery evidence, not additional scientific replicates.
They add no source experiment and do not replace the original nonconforming result.

## Effective status after v6

- W01: 12/12 tasks complete; 144/144 source experiments; 36/36 K1/Q/K2 posttests sealed.
- W02: 12/12 tasks complete; 144/144 source experiments; 36/36 K1/Q/K2 posttests sealed.
- W03 P mechanism-discovery Opaque: complete after the Q/K2 recovery above.
- Total effective sealed tasks: 25/60, representing 300/720 source experiments and
  75/180 sealed posttests.

The next task, `RX-W03--P--mechanism_discovery--Aligned`, completed all twelve source
experiments, K1, and K2. Its Q call ended with a provider failure and no payload. The
runner retained the task as nonconforming and stopped before task 27. Consequently:

- 312/720 source experiments have physically completed;
- 25/60 tasks are fully sealed;
- task 26 has a complete source but an incomplete posttest chain;
- tasks 27–60 (34 tasks) have not started;
- reference truth, prediction evaluation, and recommendation retests remain embargoed
  and ungenerated.

## Published interim results

The Git-tracked interim report directory
`reports/work-ii-rx-ps-five-world-dual-goal-20260919-w01-w02/` contains the complete
readable pre-truth reports for W01 and W02: 24 tasks, 288 source experiments, and 72
sealed posttests. Raw provider streams, credentials, thread identifiers, ignored run
directories, and machine payload JSON remain outside Git.
