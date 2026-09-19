# Work II RX-P/S five-world block — recovery v8 parallel-four execution

Date: 2026-09-19. Status: authorized continuation after a retained pre-action platform failure.

Recovery v7 stopped because the detached worker environment could not locate the Codex CLI. No worker called the model or performed a physical action. Task 26 retains its incomplete `posttest-repair-v7/` manifest; tasks 27–35 retain only their original `attempt.json` and public-prior binding. Those records are not deleted or overwritten.

V8 keeps the frozen 60-session scientific contract and the four-worker design from v7. It adds an explicit CLI-path preflight and records the resolved executable in the manifest. Task 26 writes a fresh `posttest-repair-v8/` and reruns only Q→K2 on the original source thread. Each v7 zero-action source writes under its own `source-repair-v8/` using the same frozen cell and deterministic seeds. Never-started cells continue to use their original source directories.

Only four cells may be admitted at once. A succeeding cell admits one replacement; the first failure cancels every not-yet-running item and preserves at most the other three in-flight outcomes. The coordinator remains the sole writer of the recovery summary and may release the 600 provider-free truth executions only after all 60 effective K1/Q/K2 chains validate.

The ETA basis remains the observed 703.3-second median per completed task: about 1 hour 45 minutes for nine four-worker waves, with a 2–3 hour operational range including provider contention, the slow tail, truth generation, evaluation, and recommendation retests.
