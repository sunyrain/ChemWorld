# Pre-v0.4.8 SAC diagnostic weights

This directory publishes four small, representative SAC model archives from the
interrupted pre-v0.4.8 Train/Dev run so collaborators can inspect the old result.
Replay buffers are intentionally excluded.

These weights are **diagnostic only**. They were written before the current
task-specific observation contract and checkpoint writer contract landed on
`main`. They use checkpoint sidecar schema
`chemworld-rl-checkpoint-contract-sidecar-0.1`; current runtime loading requires
manifest schema `chemworld-rl-checkpoint-0.3` and sidecar schema
`chemworld-rl-checkpoint-contract-sidecar-0.2` with an exact observation-contract
hash. Therefore they are not formal v0.4.8 evidence, must not be resumed in the
current runtime, and must not be entered into the formal checkpoint index.

Selection is one representative checkpoint per task. Three are the best
legacy-eligible candidates under the preregistered Dev ranking. The
crystallization checkpoint is only the best observed candidate because that
task produced no legacy-eligible checkpoint.

See `manifest.json` for digests, source commits, and selection labels. See
`result-summary.json` for the interrupted matrix coverage and resource totals.
