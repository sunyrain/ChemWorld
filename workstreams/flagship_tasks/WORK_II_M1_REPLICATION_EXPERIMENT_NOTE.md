# M1 independent-world replication

Status: design fixed before execution on 2026-09-05. The user's continuation authorizes this
planned M1 block; M2–M4 are separate. Freeze the stable source once after focused acceptance,
before the first execution. The retained release manifest records the exact source commit.

## Question and fixed coverage

Does a public-data quadratic fit reduce decision regret relative to a model-generated quadratic
under the same deterministic maximizer? Cross representation (L: model law; F: public ridge fit)
with decision rule (A: fresh same-model recipient; X: shared deterministic maximizer). L-A and F-A
receive identical evidence and candidates except for the supplied coefficients. The replacement
includes computation and does not identify an internal psychological mediation effect.

Two tasks (electrochemical conversion; reaction to crystallization), five new public-test worlds
per task, DeepSeek-v4-flash/high and GPT-5.6-sol/medium, two fresh source repeats per model/world:
10 independent world clusters, 40 source states, 120 provider-session opportunities (40 source,
80 decision), 160 factorial slots. Each world has 12 public evidence and eight hidden candidates:
200 physical executions and 200 exact replays. Evidence, candidates and fitted laws are shared
across models/repeats within world; their copies are not independent observations.

World identities are determined without outcomes: for task and index 1–5, take the first four
SHA256 bytes of `chemworld-m1-replication-v1/{task}/{index}` as a big-endian integer modulo 2^31.
These are public-test identities, distinct from exposed seeds 0–4, not private held-out seeds.
Same normalized 12-point/8-point LHS and complete controls as the
[development note](WORK_II_M0_M1_DEVELOPMENT_EXPERIMENT_NOTE.md), fixed in the concrete protocol.
No control-range, point, world or task selection depends on this block's outcomes. This tests
unseen parameters within two fixed local response-surface tasks, not unseen mechanism topology.

Both representations use `[1,x,y,x*x,x*y,y*y]`, linear normalized coordinates, unclipped utility,
ridge 1e-6 with unpenalized intercept for F, original candidate order for exact ties. No tuning or
hidden outcomes enter fitting or choices. Source sessions never see terminal candidates. All
40 source states are permuted with NumPy seed 20260905. Within each state, source precedes the
two decision sessions; L/F order alternates on world index + task index + model index + repeat
index parity, giving one order of each kind per world/model. Every session is fresh and tool-free.

The physical constructor, score and exact replay are shared by evidence and hidden candidates.
Keyed observation seed is 90500 + design index; noise namespace adds the world cluster to the
block namespace. Candidate utility is one measured outcome per plan, not noiseless latent truth.
The prior development intervention positive control is retained; no extra intervention pair is
added to this independent-world denominator.

## Readouts and decision rules

Primary: mean paired failure-aware regret difference F-X minus L-X, averaged over the four
model/repeat states within each world, then equally across worlds within task and across tasks.
Raw utility regret uses fixed scale 1. Missing/invalid choices have regret 1; completed-only regret
is secondary. Near-optimality is regret <= 0.01. Primary material benefit is supported only if the
upper end of the two-sided 95% interval is below -0.01. Negative, null and opposite effects are
retained; no additional seeds, retries, favorable replacement, or significance-based stopping.

Resample five worlds with replacement separately within each task, preserving all nested states;
20,000 percentile-bootstrap replicates, seed 20260906. Four secondary contrasts are L-X minus L-A,
F-A minus L-A, F-X minus F-A, and the representation-by-rule interaction; report 98.75% marginal
intervals (Bonferroni adjustment for four comparisons). All intervals are approximate with only
five worlds per task. Show every world's effect and each task mean, availability, near-optimality,
Top-1, candidate prediction MAE, and A/X agreement. Nonfinite prediction error is reported as
unavailable, not silently clipped. Completed-only contrasts retain their eligible denominators.

Nearest public observation in normalized Euclidean distance predicts each candidate; maximize
those predictions with original row-order ties. Also report exact expected uniform-random regret.
Both baselines use the same public evidence/hidden evaluation and count once per world. Fit plus
argmax is a strong classical baseline, not itself a novel algorithm.

## Failures, resources and outputs

No paid slot retries or repair turns. Resume reads completed receipts; an already started session
without a receipt becomes an interrupted failure and is not relaunched. Missing source blocks
L-A/L-X while independent F-A/F-X continue. Unknown IDs, extra fields and nonfinite coefficients
fail local validation. Preserve the source artifact once. Seal all 160 choices before analysis
loads hidden scores. Physical failure, semantic mismatch or replay failure stops dependent
provider work; forbidden tools, missing/reused session identity or hidden-data leakage stop the
remaining block. Keep all failed and unstarted opportunities. Such platform/protocol failure
invalidates formal inference; a repair requires a separately documented full affected block.

Each provider session has a 600-second timeout; 2,048 requested output tokens is a prompt request,
not a hard cap on reasoning. Sequential maximum provider envelope is 20 hours; development rates
suggest roughly 2.3 provider hours plus 30 minutes for physics/replay, subject to provider latency.
Report actual tokens (input/cache/output/reasoning), wall time by model/stage, physical CPU/wall,
operations, measurements, recipe durations and reagent use. Replay CPU/wall is included;
recipe resources count primary executions once. No invented currency estimate.

Runner: `scripts/run_work_ii_factorial_replication.py`; concrete protocol:
`configs/benchmark/work_ii_m1_replication_20260905.json`. Ignored output root:
`runs/work-ii-m1-replication-20260905`. Stages are prepare, run, analyze. One release manifest binds
the clean source commit and execution-relevant files. Raw provider data and trajectories stay
ignored. Export one sanitized JSON/Markdown report with every slot, exact denominators, failures,
cluster contrasts, costs and source binding; update the existing TODO/results/matrix. Figures
use world-level paired effects and clearly separate missing outputs from measured loss. Formal
manuscript integration is conditional on successful execution validity, never on a positive effect.
