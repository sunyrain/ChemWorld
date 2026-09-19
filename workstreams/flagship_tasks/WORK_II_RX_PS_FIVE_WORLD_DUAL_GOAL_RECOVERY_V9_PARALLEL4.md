# Work II RX-P/S five-world block — recovery v9 after credential refresh

Date: 2026-09-19. Status: retained single-cell posttest failure after reaching 33/60 effective chains.

Launch outcome: the credential refresh succeeded. Task 26 and seven additional cells sealed, bringing the effective block to 33/60. `RX-W03--S--mechanism_discovery--Opaque` completed twelve source experiments plus valid K1 and K2, but Q returned a provider failure with no payload. The v9 coordinator then applied its preregistered fail-closed queue rule. Three other in-flight cells completed and were retained, no truth was generated, and no result was overwritten. At the user's request, v10 replaces whole-queue fail-close with per-cell isolation while keeping the truth embargo.

The user explicitly requested replacing the stale remote Codex login cache with the newly authenticated cache from the Mac. The transfer was atomic, the remote file mode is `600`, local and remote SHA-256 values matched immediately after transfer, and `codex login status` reported ChatGPT authentication. No credential content or digest is stored in this experiment record.

V9 preserves the frozen 60-session scientific design. Task 26 writes `posttest-repair-v9/` and reruns only Q→K2 on its original source thread. Tasks 27–29 retain their v8 zero-action provider failures and write new `source-repair-v9/` results; tasks 30–35 retain their v7 pre-action directories and also write under `source-repair-v9/`. Never-started tasks use their original cell directories. The cell definitions, deterministic seeds, model, reasoning effort, prompts, prior arms, twelve experiments, measurements, K1/Q/K2 questions, and truth embargo do not change.

Before creating the v9 manifest, the coordinator requires both an absolute Codex CLI path and a successful `codex login status`. Exactly four cells are admitted initially; thereafter each successful completion admits one replacement. The first failure cancels every queued item and retains at most three other in-flight outcomes. Reference truth remains forbidden until all 60 effective chains are complete and sealed.

The ETA remains approximately 1 hour 45 minutes for sources and posttests from the historical 703.3-second median and nine four-worker waves, or 2–3 hours operationally including provider contention, truth generation, evaluations, and recommendation retests.
