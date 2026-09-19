# Work II RX-P/S five-world block — recovery v10 continue-on-cell-failure

Date: 2026-09-19. Status: user-authorized operational-policy correction; scientific design unchanged.

V9 stopped the whole queue when one completed source lacked a valid Q payload. The user explicitly requested that an isolated cell failure must not automatically stop unrelated workers. V10 therefore keeps four mutually exclusive workers active: a successful completion or a retained cell failure both admit the next unstarted cell. Failures are recorded in the live summary with their cell IDs and are never overwritten.

At launch, 33/60 chains are effective. `RX-W03--S--mechanism_discovery--Opaque` has twelve valid source experiments, K1, and K2; v10 resumes its original source thread and reruns only Q→K2 in `posttest-repair-v10/`. The remaining 26 cells are either retained zero-action repairs or never-started frozen cells. Prompts, prior arms, model, reasoning effort, cell definitions, deterministic seeds, budgets, twelve-experiment limit, and K1/Q/K2 content remain unchanged.

Continue-on-failure does not weaken truth isolation. The queue may finish with an isolated-failure list, but reference truth, prediction evaluation, and recommendation retests remain forbidden until all 60 effective chains are complete and sealed. V10 attempts every remaining cell before exiting; it never retries indefinitely and never deletes or replaces a retained failure.

With 27 work items and four workers, the initial estimate is seven waves. Using the observed 703.3-second historical median gives about 82 minutes for sources and posttests, plus final truth/evaluation/retest time after 60/60 sealing.
