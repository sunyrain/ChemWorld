# M0/M1 development experiment

Status: completed development; design fixed before data production on 2026-09-05. This block implements the user's
request to organize/optimize experiments and figures. It is not formal publication evidence.

## Question and coverage

Can one shared world/ActionPlan executor provide consistent public evidence and hidden decision
scores, and can a minimal representation-by-decision protocol run without the old redundant
checkpoint/status submissions? Development tasks are electrochemical conversion and reaction to
crystallization, public-test world seed 0 for each. This is two development world clusters, not a
new multi-world confirmation. No historical participant output or candidate score is reused.

For each task, preselect two continuous controls and hold all other controls fixed. Choose 12
public evidence points with a seeded two-dimensional Latin hypercube and eight disjoint terminal
points with an independently seeded Latin hypercube; seeds are 90512 and 90508. Select points
without outcomes, using the same normalized design in both tasks. Electrochemistry varies controlled
potential 0.65–1.65 V and controlled current 20–120 mA, excluding the contract's minimum changes
from the fixed probe (1.18 V, 70 mA) before any execution. Crystallization varies reaction
temperature 350–405 K and crystallization temperature 275–295 K. Complete ActionPlans disclose
all controls; this tests local response surfaces, not general mechanism identification.

The shared score is the task's balanced leaderboard utility. Both artifact sources use the same
six-term quadratic in normalized coordinates: 1, x, y, x², xy, y². The reference fits only the 12
public observations using ridge 1e-6 with an unpenalized intercept. No hidden scores, world
parameters, target outcomes, or data-dependent hyperparameter selection enter fitting or decisions.

Each source model produces one coefficient vector without terminal candidates. Fresh sessions then
receive the same public evidence and candidates plus either its artifact (L-A) or the fitted artifact
(F-A). The shared deterministic maximizer evaluates those artifacts for L-X/F-X. Agent output is only
the six coefficients or one candidate ID; runner-owned status is never submitted by the participant.
Use the existing DeepSeek-v4-flash/high and GPT-5.6-sol/medium configurations, one repeat per task:
four source sessions and eight fresh decision sessions, at most 12 provider calls. No tool use,
session reuse, slot retries, or additional evidence are allowed. Each call is limited to 600 seconds
and a requested output budget of 2,048 tokens; report actual provider usage rather than claiming the
prompt is a hard token cap. Total provider wall-time envelope is two hours, sequential execution.

## Measurements and success/failure rules

M0 checks all 40 physical executions (24 evidence + 16 hidden candidates), their exact replays,
compiled/public/executed plan equality, resource receipts and one actual world-intervention
positive-control pair. The latter adds two executions and two replays using the same first public
electrochemical plan with a registered electrolyte-profile intervention; its measured divergence is
a diagnostic, and semantic preservation is checked against the trajectory's recorded intervention.
The 42-execution denominator is fixed. No fit or participant performance threshold controls entry.

M1 reports all 16 factorial condition slots, the 12 provider-call opportunities, and two simple
baselines per world (nearest-neighbor public evidence and exact expected uniform-random utility).
Primary readout is raw decision regret; normalized regret uses the fixed score scale 1, avoiding
candidate-range inflation. Near-optimality is regret <=0.01. Report artifact prediction MAE,
execution availability, failures, paired contrasts and provider/physical costs. Two development
worlds support a functional demonstration and cost calibration only; no significance test or
generalization claim is made. L-X/F-X are calculated before any score is read by the analyzer.

All submitted laws and selections are retained once. Missing/invalid artifacts block their
dependent L slots while the independent F slots continue; missing decisions remain failures.
Failure-aware regret is 1 with completed-only values secondary. Invalid numeric values, extra
scientific fields and unknown candidate IDs fail local validation. No repair turn is granted.
Provider/schema failures are outcomes and do not trigger replacements. A physical execution,
replay, public/truth semantic mismatch, forbidden tool call, reused thread or hidden-data leak
halts dependent provider work. Preserve the whole affected block if platform repair is needed,
then document a new block before re-execution; never repair unfavorable science by rerunning it.

## Outputs

One ignored development root contains the protocol, immutable physical trajectories/receipts,
public evidence/candidate packets, private scores, source artifacts, provider attempts/receipts,
all condition results, progress events and a readable JSON/Markdown summary. Public/truth projection
uses explicit allowlists. A sanitized report is linked from the existing TODO/results index.
Figure redesign reuses current bound publication data and does not add observations or inference.
The larger M1 matrix and M2/M3/M4 remain separately planned and are not silently executed by this note.

## Concrete implementation fixed before execution

Runner: `scripts/run_work_ii_factorial.py`; shared public fit/decision primitives:
`src/chemworld/eval/work_ii_factorial.py`. Output: ignored
`runs/development/work-ii-m0-m1-20260905`. Use `prepare`, then `run`; `analyze` is read-only
with respect to executions. A started unit is never automatically retried on resume.

Normalized designs use NumPy `default_rng(seed)`, one permutation plus independent uniform jitter
per axis. Reject the entire LHS if any electrochemical point violates the two minimum-change
bands; choose the first valid design (maximum 10,000 outcome-blind attempts). Both tasks share
the accepted coordinates. Coordinates are linear in the stated ranges, in [0,1]. Exact ties
use original candidate-ID order; predictions are not clipped. Nearest-neighbor baseline assigns
each candidate the utility of its nearest evidence point in normalized Euclidean distance and
maximizes those predictions; all ties use original row order.

Electrochemical fixed controls: electrolyte profile 2, solvent 1, reagent 0.004 mol;
probe 1.18 V, 70 mA, 630 s; controlled duration 3540 s; autonomous-open workflow and balanced
efficiency-v2 score. Crystallization fixed controls: catalyst 0 at 0.000315 mol, solvent 1,
reagent 0.015 mol, stirring 675 rpm, reaction 3600 s, seed 0.008 g, crystallization 7200 s.
Noise is keyed, with the protocol's task-specific namespace and observation seed 90500 plus
design index (evidence first, candidates second). The intervention pair both use index 0.
Its registered public-to-baseline electrolyte mapping is [2,1,0,3].

Calls proceed task order electrochemistry, crystallization; model order DeepSeek, GPT;
source, L-A, F-A. Fitted artifacts and executor choices use the same code for both models.
Candidate scores are first loaded by analysis after all selections have been sealed.
The minimal source/decision output contract is locally validated even when a provider claims
schema conformance. Raw trajectories stay private; public packets allowlist controls, plans,
coordinates and public evidence scores. Physical costs distinguish simulator measurement units,
scheduled recipe durations and reagent amounts from actual CPU/wall time; no currency estimate
is invented. Quadratic identification and provider arithmetic remain scientific limitations.

Execution completed once with 42/42 physical executions and replays, 12/12 provider sessions,
and 16/16 condition slots. No execution or participant output was replaced. The post-execution
report exporter adds no execution or scoring changes. Reproduce the sanitized summary with:

```powershell
uv run --no-sync python scripts/run_work_ii_factorial.py analyze --report <new-report-path.json>
```

The retained [JSON](reports/work-ii-m0-m1-development-20260905.json) and
[readable summary](reports/work-ii-m0-m1-development-20260905.md) remain development evidence.
