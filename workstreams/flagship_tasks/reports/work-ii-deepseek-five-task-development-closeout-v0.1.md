# Work II DeepSeek five-task development closeout

Date: 2026-08-10. Status: terminal development evidence; not formal or held-out evidence.

Machine analysis:
`workstreams/flagship_tasks/reports/work-ii-deepseek-five-task-development-closeout-v0.1.json`.
Source manifest:
`configs/benchmark/work_ii_deepseek_five_task_development_analysis_sources_v0.1.json`.

## Result

The existing recovery-amended five-seed matrices for electrochemical conversion,
reaction-to-crystallization and reaction-to-distillation were preserved without rerun. The two
remaining tasks in the frozen five-task development scope were each run first as a seed-0,
three-prior-arm gate triplet. Neither triplet passed its frozen expansion gate, so no additional
world seeds were launched.

| Task | Coverage reached | Terminal cells | Runner-qualified | Complete experiments | Attempts / committed | MCP failures | Provider errors | Resource rejects | Exact replay |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Electrochemical conversion | 5 seeds | 15/15 | 15/15 | 60/60 | 373 / 372 | 13 | 0 | 0 | 15/15 |
| Reaction to crystallization | 5 seeds | 15/15 | 13/15 | 54/60 | 606 / 605 | 18 | 0 | 0 | 15/15 |
| Reaction to distillation | 5 seeds | 15/15 | 15/15 | 60/60 | 637 / 637 | 7 | 0 | 0 | 15/15 |
| Partition discovery | seed-0 gate only | 3/3 | 2/3 | 12/12 | 106 / 92 | 2 | 0 | 2 | 3/3 |
| Safety-constrained reaction | seed-0 gate only | 3/3 | 2/3 | 10/12 | 100 / 78 | 8 | 0 | 0 | 3/3 |
| **Combined observed** | **45 full-matrix + 6 pilot cells** | **51/51** | **47/51** | **196/204** | **1,822 / 1,784** | **48** | **0** | **2** | **51/51** |

The combined cells used 189,139,364 input tokens, including 183,646,080 cached and 5,493,284
uncached tokens, plus 2,044,739 output tokens. The 97.10% cache-hit fraction represents reused
input context, not repeated model output. Provider usage is complete for 49/51 cells; the two
crystallization cells that were forcibly stopped before a provider terminal event retain usage as
unavailable rather than zero.

## Retained gate failures

The two historical crystallization failures remain unchanged. The new gate failures are:

- `partition-discovery / misindexed_nominal / seed 0` completed all four experiments and exact
  replay with zero provider errors, but produced 54,295 output tokens against the frozen 48,000
  limit. It also recorded one resource-rejected proposal. It is retained as a method-resource
  failure and does not authorize seeds 1--4.
- `reaction-safety-constrained / aligned_nominal / seed 0` completed only two experiments. After
  exhausting solvent and catalyst it repeatedly proposed an inapplicable `wait`, consumed the
  40-attempt campaign budget, recorded six recovered MCP failures and used 5,293,657 input and
  64,595 output tokens. It is an agent resource-allocation/tool-contract failure, not a provider,
  network or chemical-platform failure.

Both new triplets had zero provider error events and every terminal trajectory, including failed
prefixes, passed exact physical/resource replay.

## Strict experiment-note audit

The experiment note required zero resource rejection in a passing seed-0 pilot. The reused config
generator inherited the later recovery-amended allowance of at most one rejection per cell. This
was a pre-execution contract mismatch. It does not change the stop decision: both task triplets
already failed independent hard gates and neither expanded. For fail-honest reporting, the
machine analyzer's 47/51 runner-qualified denominator is supplemented by a stricter note-level
denominator of **46/51 protocol-qualified cells**: partition opaque is also non-passing because it
recorded one resource rejection. The config generator and the two current task configs are corrected
to zero rejection only after terminal closeout, preventing future recurrence. No observed threshold
is retroactively amended and no pilot is rerun.

## Scientific interpretation

The three five-seed recovery-amended tasks retain their prior-arm descriptive conclusion: explicit
priors reshape endpoints, but endpoint improvement and verbal warning do not selectively identify
the misindexed prior. The two new seed-0 triplets add operational evidence only. Partition shows
that one task-pattern output tail can cross a task-specific cap despite complete physical work;
safety shows that nominally helpful information can coexist with catastrophic campaign resource
allocation and failure to close the planned experiment count. Because these tasks did not reach
five seeds, their endpoint differences are not promoted to task-level scientific contrasts.

This closes the requested DeepSeek development series under the frozen pilot-expansion rule. It
does not execute the 75-cell public formal matrix, private sealed confirmation, evaluator-truth
prediction scoring or blind transfer, and it does not support a DeepSeek-versus-WellAU capability
ranking.
