# Work I Platform Surface Audit

Audit: `chemworld-work-i-platform-surface-941278c0c5d34199`  
SHA-256: `941278c0c5d3419989d5d93e187fc73494e05be5bb8c622c8f776978c6106b77`

## Approved display statement

ChemWorld exposes 15 registered task contracts spanning all 28 typed operation kinds and five instrument contracts; qualification executed 415 complete-experiment boundary recipes and bound all 62 task-specific metric endpoints to executable evaluators.

## Exact count meanings

| Display number | Meaning | Qualification |
| ---: | --- | --- |
| 15 | live registered task contracts | all have executable midpoint and boundary recipes |
| 28 | globally unique typed operation kinds | every kind is reachable from at least one registered task |
| 5 | globally unique public instrument contracts | every instrument is reachable from at least one task |
| 62 | ordered task-metric evaluator bindings | all bindings resolve to executable evaluators |
| 415 | executed boundary recipes | qualification executions, not tasks or agent trials |

The 62 endpoint count is deliberately task-specific. The same metric name in two task contracts contributes two evaluator bindings; it does not imply 62 unique metric definitions (the live registry contains 43 unique metric identifiers).

## Publication boundary

These numbers describe the registered and executable platform surface. They do not claim that autonomous agents were empirically compared on all 15 tasks, and they do not constitute physical-laboratory validation.
