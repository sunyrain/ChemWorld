# Work II electrochemical matched-prior qualification

Date: 2026-08-11  
Status: v0.1/v0.2 development smokes rejected; v0.3 frozen before qualification execution

## Question and units

Can each preregistered electrochemical world support matched, participant-visible aligned and
misspecified local models of controlled potential/current that are initially comparable yet
falsifiable from held-out experiments?

- Worlds: the complete `world_seed=0,1,2,3,4` cohort; one task × world is the qualification unit.
- Provider calls: zero. No participant trajectory is read or generated.
- Source: the completed electrochemical mechanism-oracle v0.2 summary and its five hash-bound world
  reports. A failed source binding stops the block.

## Coverage and measurements

For each world, select the first separated high-quality validation context under the frozen
`score_gap <= 0.05` and non-target distance `>= 0.05` rule. Round only the fixed non-target controls.
At that context, execute an `11 × 11` deterministic grid over the two public signed control
coordinates for controlled potential and current (`0.25--0.75` in steps of `0.05`). The even/even
checkerboard is the 36-query fit set; the remaining 85 queries are held out. Select 16 held-out
queries by deterministic space-filling distance for later evaluator use.

Measure exact classified/completed/physical/platform denominators; fitted score-model error;
baseline utility gap; held-out disagreement; blind identification margin; low/high falsification
support; prior word/schema matching; participant-visible leakage; and generated package/config
bindings. Safety risk is still recorded, but it is not included in the matched-law error because the
source qualification found no electrochemical safety frontier.

## Pass and failure rules

Every world must independently pass:

- `121/121` surface queries classified, zero platform failures, at least 24 safe fit and 40 safe
  held-out queries;
- aligned held-out score normalized MAE `<= 0.20`;
- one frozen baseline-preserving reflection candidate in the order potential, then current. The
  candidate agrees exactly inside the central `3 × 3` reference neighborhood and reflects the
  fitted law outside it; it must have baseline score gap `<= 0.05`,
  disagreement fraction `>= 0.25`, blind normalized-error margin `>= 0.05`, at least three
  falsification queries on each side, and representative grid distance `>= 4`;
- exactly 16 balanced held-out queries;
- aligned and misspecified public priors have identical schema, context, confidence and word count,
  and differ only in `model.claim.expected_relation`;
- no oracle, world, arm, run path or hidden-mechanism leakage.

A schema-valid dynamic physical failure is retained as a task outcome and is not retried. A payload,
compiler/runtime, missing-result, observation or binding failure is a platform failure and rejects
the complete block without changing worlds, coverage or thresholds. Any scientific gate failure is
also retained and stops electrochemical provider expansion.

## Expected outputs

The block may write ignored raw world reports plus one tracked machine summary, one five-world prior
package and one development D1 config. The D1 config is generated only if all five worlds pass and
must retain `formal_r5_authorized=false`. This Q2 block authorizes no provider execution by itself.

## Development-smoke record and v0.2 amendment

Before the five-world qualification, a world-0 implementation smoke executed `121/121` queries with
zero physical/platform failures and aligned normalized MAE `0.139583`. The originally proposed full
axis reflections were rejected before qualification: potential reflection failed baseline matching
(`0.067799 > 0.05`), while current reflection failed blind margin (`0.034653 < 0.05`). This smoke is
development evidence and is not replaced or counted in the qualification denominator.

The v0.3 construction keeps every coverage unit and pass/failure threshold unchanged. It freezes a
finite reflection strength `1.0` for each axis, selected in the order stated above. Preserving the
central neighborhood makes the two incomplete priors initially comparable while retaining an
outside-region directional error; it does not change observed outcomes, fit data or public
confidence. No further candidate, axis, construction rule or threshold may be added after the
five-world qualification starts.

The intermediate v0.2 strength smoke is also retained as development evidence: world 0 remained
operationally clean, but potential strength `0.70` had blind margin `0.043444` and the full/current
candidate had `0.034653`, both below the unchanged `0.05` gate. It is not part of the formal
denominator.

The final v0.3 world-0 smoke again completed `121/121` queries with zero physical/platform failures.
The baseline-preserving potential reflection passed every gate: baseline gap `0`, disagreement
`73/85`, blind margin `0.094693`, low/high support `21/15`, representative distance `10`, and all
prior matching/leakage checks. This verifies implementation viability only; the five-world
qualification still starts from world 0 on a clean committed source.

