# Benchmark Protocol

## Splits

- `public-dev`: open development and teaching split.
- `public-test`: open local benchmark split.
- `private-eval`: hidden production leaderboard split.

The public repository deterministically generates all splits so the package is
self-testable. A production leaderboard should replace `private-eval` with a
server-side registry while preserving the same public API. In local open-source
runs, `private-eval` is marked as `public-placeholder-private`. Maintainers can
set `CHEMWORLD_PRIVATE_EVAL_SALT` for hidden production parameters without
changing the public environment interface.

## Submission

A valid submission contains:

- trajectory JSONL;
- agent manifest;
- environment version;
- world family version;
- seed and budget;
- reproducible command.

`chemworld run` writes a `*.manifest.json` sidecar containing dependency
versions, platform information, source digest, agent metadata, and the exact
command used for the local run. If git metadata are available, it also records
the current commit hash.

Every trajectory is validated before scoring. A single JSONL file must contain
exactly one task, contiguous step numbers, required action keys, required
observation keys, and observations in valid benchmark ranges.

Maintainers can additionally run `chemworld verify` to replay submitted
operations in the declared environment and confirm that observations and rewards
match the deterministic benchmark implementation. Use
`chemworld verify --constitution` to require the recorded physical constitution
checks to be present and reproducible.

## Foundation Records

Each trajectory records event-level world-model fields:

- `operation_type`;
- `preconditions`;
- `state_delta_summary`;
- `constitution_checks`;
- `instrument`;
- `instrument_source`;
- `observed_keys`;
- `observed_mask`;
- `raw_signal`;
- `processed_estimate`;
- `uncertainty`;
- `measurement_cost`;
- `sample_consumed`;
- `observed_reward`;
- `leaderboard_score`;
- `reward_source`.

Observation records are partial-observation records, not truth dumps. Fields that
were not measured by the current or carried-forward instrument are stored as
`null` in JSON and have `observed_mask[field] == false`. Gym observations use
`NaN` for the same missing values. Public ledger fields such as cost and safety
risk remain observable.

Instrument records distinguish signal and estimate layers. `raw_signal` stores
the instrument-like signal packet, `processed_estimate` stores the derived
public estimates, and `uncertainty` stores measurement-noise metadata. This
keeps the benchmark usable by simple Gym agents while preserving a richer
scientific audit trail.

Failed action preconditions return a non-informative observation: all observation
fields are `null`/`NaN`, `observed_keys` is empty, `observed_reward` is zero, and
`error_message` records the failed precondition names. Failed measurement actions
do not consume instrument cost or sample volume.

`observed_reward` is the online feedback available to the agent from measured
quantities and public ledger state. `leaderboard_score` is only populated for
official final-assay scoring events and is the value used for benchmark
performance metrics.

`final_assay` is terminal for the Gym episode. It requires a terminated reaction
state and can only be scored once; repeated final assays are rejected by the
physical constitution and cannot create additional leaderboard scores.

Use `chemworld inspect-constitution --env BatchReactorWorld` to inspect the
declared rules for the environment.

## Metrics

ChemWorld-Bench reports official metrics from `leaderboard_score`, so
intermediate HPLC, GC, or UV-vis measurements cannot directly become formal
leaderboard performance. It reports:

- final best score;
- best valid score after excluding unsafe and high-cost experiments;
- best valid yield;
- area under the best-score curve;
- threshold sample efficiency;
- safety violations;
- mean cost and mean risk;
- safety-aware score;
- weighted total score.

The default total score is:

```text
0.40 * performance
+ 0.25 * sample efficiency
+ 0.20 * safety-aware score
+ 0.15 * best valid score
```

Explanation quality is collected through structured fields but is not included
in the automatic total score.

For research comparisons, run the same agent over multiple seeds and at least
`public-test` plus `private-eval`. The local leaderboard reports a
`public_private_gap` when both splits are available for an agent. It also
reports standard deviation, standard error, and a 95% confidence interval for
mean total score.
