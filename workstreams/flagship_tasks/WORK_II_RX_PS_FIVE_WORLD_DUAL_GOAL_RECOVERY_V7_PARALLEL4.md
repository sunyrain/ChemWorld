# Work II RX-P/S five-world block — recovery v7 parallel-four execution

Date: 2026-09-19. Status: authorized development recovery; the scientific contract remains frozen.

## Question and unchanged coverage

This recovery asks whether the unfinished portion of the already authorized RX-P/S block can be completed with four isolated worker processes without changing its scientific meaning. The denominator remains 60 independent source sessions (`2 loci × 5 worlds × 3 arms × 2 goals`), twelve experiments per source, and the sealed K1→Q→K2 chain per source. Model, reasoning effort, prior payloads, query rows, budgets, seeds, measurements, scoring, and the truth embargo are unchanged.

At launch, 25/60 chains are complete. Task 26, `RX-W03--P--mechanism_discovery--Aligned`, has a valid twelve-experiment source and K1/K2 but no valid Q payload. It will resume the original source thread and rerun only Q followed by K2, without rerunning physical experiments. Tasks 27–60 are unstarted and retain their original schedule entries.

## Four-worker isolation and measurements

Exactly four spawned worker processes consume mutually exclusive cell IDs. Each new task writes only its own previously absent `sources/<cell_id>/` directory. The task-26 repair writes a new `posttest-repair-v7/` directory and never overwrites the retained original. The coordinator alone writes the v7 manifest/summary and, only after all 60 chains validate, the shared reference truth, evaluations, and recommendation retests.

Progress records completed work items, effective task count, elapsed time, per-cell worker time, and ETA. The pre-launch estimate uses the observed 25-task median of 703.3 seconds: 35 work items require nine four-worker waves, about 1 hour 45 minutes for sources and posttests. The operational ETA is 2–3 hours after allowing for provider contention, the slow tail, 600 provider-free reference executions, evaluations, and retests.

## Failure and release rules

Any invalid payload, provider failure, nonzero worker exception, unexpected pre-existing cell directory, or nonconforming result stops queue admission and retains all in-flight outcomes. No truth is generated unless every one of the 60 effective results is complete and its K1/Q/K2 chain is sealed. A failure never causes an experiment or posttest to be silently overwritten or replaced.

Expected outputs are the new source/result directories, task-26 `posttest-repair-v7`, `recovery-v7-parallel4/manifest.json`, a live write-once summary, and—only after complete sealing—the 600 reference executions, 60 prediction evaluations, and valid recommendation retests.
