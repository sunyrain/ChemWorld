# DeepSeek parametric pilot evaluator attempt 1 — invalidated

Date: 2026-08-11

The first zero-provider evaluator attempt completed 4/4 held-out truth queries and 18/18 blind
replays with exact replay. Its numeric machine report had SHA-256
`7c401ef8f46f9a3ca232d903b9821bba8345661635354fae5672245740c94418`.

The generated Markdown contained a hard-coded WellAU interpretation claiming that the misspecified
arm remained below the opaque endpoint. The DeepSeek data showed the opposite: best observed scores
were `0.8307` for misspecified and `0.5876` for opaque. The numeric evaluator outputs were not used to
change any intervention, participant trajectory, threshold or denominator, but the report package is
invalid because prose and data disagree.

The complete attempt-1 evaluator root remains ignored at
`runs/development/work-ii-deepseek-parametric-initial-model-pilot-evaluation-20260811-run1/`.
After fixing the renderer to derive every directional statement from the machine report, the entire
zero-provider evaluator block must restart from the first truth query under a new output identity.
The three retained participant sessions are not rerun.
