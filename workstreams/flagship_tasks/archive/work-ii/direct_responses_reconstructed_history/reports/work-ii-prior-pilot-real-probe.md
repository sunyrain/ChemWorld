# Work II prior pilot — real-provider probe

Status: **PASSED**  
Scope: development interface qualification only; no scientific or benchmark claim.

The smallest real-provider probe completed **3/3 cells with 0 failures** on
`electrochemical-conversion`, world seed 0. The three cells were `opaque`, `aligned_nominal` and
`misindexed_nominal`; each executed one complete experiment from one direct WellAU Responses
decision. The model was exactly `gpt-5.6-sol` at medium reasoning. Tools and MCP were disabled.

| Arm | Calls / attempts | Input / cache / output | Prompt estimate / cap | Completion |
| --- | ---: | ---: | ---: | ---: |
| opaque | 1 / 1 | 1,706 / 0 / 721 | 1,647 / 18,000 | PASS |
| aligned nominal | 1 / 1 | 2,875 / 0 / 1,992 | 2,706 / 18,000 | PASS |
| misindexed nominal | 1 / 1 | 2,873 / 0 / 2,463 | 2,706 / 18,000 | PASS |

Totals were 3 provider calls, 3 attempts, 0 retries, 7,454 input tokens, 0 cache-hit tokens,
5,176 output tokens and 12,630 total tokens. Provider pricing remains unavailable, so monetary
accounting is explicitly incomplete rather than recorded as zero cost. The progress wrapper emitted
30-second liveness updates and the run finished in approximately 150.5 s.

The one-experiment terminal scores are retained only in the JSON evidence summary. They are not a
prior-effect estimate and cannot be used to choose tasks, mappings, horizons or hypotheses. This
probe authorizes implementation of the one-seed breadth protocol, not scientific interpretation or
multi-seed execution.
