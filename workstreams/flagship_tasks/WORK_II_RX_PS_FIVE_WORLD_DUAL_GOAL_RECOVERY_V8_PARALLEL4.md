# Work II RX-P/S five-world block — recovery v8 parallel-four execution

Date: 2026-09-19. Status: retained old-account provider failure; truth remained embargoed.

Launch outcome: the CLI-path preflight passed, but the remote host still held the previously synchronized Codex account. Task 26 Q returned a provider failure with no payload, and the other three admitted cells stopped at zero operations and zero batches after provider errors. The bounded queue admitted no further tasks. The user then identified the stale account and explicitly authorized synchronization of the newly logged-in Mac credential cache. V9 retains every v8 directory and retries only these zero-action/provider-failed units under the newly verified remote login.

Recovery v7 stopped because the detached worker environment could not locate the Codex CLI. No worker called the model or performed a physical action. Task 26 retains its incomplete `posttest-repair-v7/` manifest; tasks 27–35 retain only their original `attempt.json` and public-prior binding. Those records are not deleted or overwritten.

V8 keeps the frozen 60-session scientific contract and the four-worker design from v7. It adds an explicit CLI-path preflight and records the resolved executable in the manifest. Task 26 writes a fresh `posttest-repair-v8/` and reruns only Q→K2 on the original source thread. Each v7 zero-action source writes under its own `source-repair-v8/` using the same frozen cell and deterministic seeds. Never-started cells continue to use their original source directories.

Only four cells may be admitted at once. A succeeding cell admits one replacement; the first failure cancels every not-yet-running item and preserves at most the other three in-flight outcomes. The coordinator remains the sole writer of the recovery summary and may release the 600 provider-free truth executions only after all 60 effective K1/Q/K2 chains validate.

The ETA basis remains the observed 703.3-second median per completed task: about 1 hour 45 minutes for nine four-worker waves, with a 2–3 hour operational range including provider contention, the slow tail, truth generation, evaluation, and recommendation retests.
