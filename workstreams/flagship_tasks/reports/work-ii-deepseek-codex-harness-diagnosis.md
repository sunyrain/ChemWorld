# Work II DeepSeek--Codex harness diagnosis

Date: 2026-08-09. Status: provider qualification; not scientific evidence.

## Finding

The original failure was not endpoint connectivity, authentication, Responses transport or MCP
startup. It was a model-catalog/tool-routing mismatch in Codex CLI 0.145.0. Before repair, the
DeepSeek catalog advertised `supports_search_tool=true` while leaving `tool_mode=null` (direct).
ChemWorld's MCP server publishes tools but no resources. Under this combination its domain tools
are routed through Codex's deferred/search path rather than exposed directly to the model.

The two retained control attempts are consistent with that mechanism:

| Attempt | Provider turn | Provider errors | Domain MCP calls | Physical operations | Observed behavior |
|---|---:|---:|---:|---:|---|
| `...seed0-opaque-real` | completed | 0 | 0 | 0 | resource discovery followed by shell/file exploration |
| `...seed0-opaque-real2` | completed | 0 | 0 | 0 | repeated resource-list/read calls |

Codex's provider defaults enable namespaced tools, its tool planner activates search when the model
catalog says search is supported, and MCP tools are deferred by default. The relevant upstream
source is the Codex 0.145.0 provider default and configured-provider implementation, the MCP
exposure policy, and the tool-spec planner:

- <https://github.com/openai/codex/blob/rust-v0.145.0/codex-rs/model-provider/src/provider.rs#L40-L47>
- <https://github.com/openai/codex/blob/rust-v0.145.0/codex-rs/core/src/mcp_tool_exposure.rs#L35-L38>
- <https://github.com/openai/codex/blob/rust-v0.145.0/codex-rs/core/src/tools/spec_plan.rs#L316-L318>

The empty catalog `base_instructions` field is not the primary cause: the ChemWorld launcher passes
an explicit `model_instructions_file`. The MCP server's tools-only contract and the launcher binding
are in `src/chemworld/agents/experiment_codex_mcp.py` and
`src/chemworld/agents/interactive_codex_experiment.py`.

## Single-variable canary

The diagnostic catalog changed only `supports_search_tool` from true to false. The model, endpoint,
reasoning effort, prompt, seed, prior arm, tools and scientific/resource limits remained unchanged.
The canary immediately called `material_information`, then completed all four experiment lifecycles.

| Measurement | Result |
|---|---:|
| Complete experiments | 4 / 4 |
| Valid belief checkpoints | 4 / 4 |
| Operation attempts | 25 |
| Committed operations | 25 |
| Resource rejections | 0 |
| Exact replay | 25 / 25 steps |
| MCP calls | 37 total, including 25 `step` calls |
| Provider result | return code 0, status completed, 0 provider errors |
| Wall time | 351.8 s |

This passes the frozen direct-tool-exposure criterion and causally confirms the first root cause.
The ignored canary artifact is
`runs/development/work-ii-deepseek-direct-mcp-canary-seed0-opaque/report.json`.

## Qualification-v1 failures

The canary is not a fully passing campaign cell. It failed two end-of-session checks:

1. Provider input was 2,490,494 tokens against a 2,400,000 cap; output was 43,647 tokens against a
   24,000 cap. Uncached input was only 87,038 tokens and cache reuse was 96.5%, but the frozen limits
   still apply.
2. The provider turn completed, but the final agent message did not validate against the required
   campaign-complete JSON payload. Consequently `provider_session_completed` was false even though
   all four experiments, checkpoints, terminal resources and exact replay passed.

At this point the DeepSeek/Codex connection was operational at the domain-tool layer but not yet
fully qualified. `code_mode_only` was no longer needed to explain or repair tool visibility. The
subsequent v2 qualification below resolves the remaining context/output and JSON-finalization
checks. No failed qualification run enters the scientific denominator.

## Qualification-v2 local repair

The production DeepSeek catalog now sets `supports_search_tool=false`. The campaign system prompt
and MCP 0.5 final-checkpoint response both require one JSON object with no prose. The event monitor
continues to accept exact JSON and additionally normalizes only one bounded equivalent: a whole
message consisting of a single JSON code fence. It records the encoding and still rejects JSON
embedded in prose, so this does not convert an arbitrary natural-language answer into a pass.

The new qualification-only config preserves one public seed-0 opaque cell, one model call, one
persistent session and the original physical/checkpoint envelope. Its frozen limits are 2,750,000
cumulative input, 320,000 uncached input and 50,000 output tokens, with zero finalization retries.
These are qualification limits derived with at least 10% headroom over the retained v1 overrun;
they are not formal scientific budgets. The local implementation passes 29 focused tests.

## Qualification-v2 result

The single frozen seed-0 opaque v2 cell passed every qualification check on 2026-08-09. It used the
production model catalog and one local credential file that remained ignored and untracked. The
run is retained at
`runs/development/work-ii-deepseek-qualification-v2-seed0-opaque/report.json` and remains outside
the scientific denominator.

| Measurement | Result |
|---|---:|
| Complete experiments | 4 / 4 |
| Valid belief checkpoints | 4 / 4 |
| Operation attempts | 26 |
| Committed operations | 25 |
| Validation failures | 1 |
| Resource rejections | 0 |
| Exact replay | 26 / 26 steps; maximum absolute error 0 |
| MCP calls | 32 |
| Provider result | return code 0, status completed, 0 provider errors |
| Final payload | valid `campaign_complete`, exact JSON encoding |
| Input | 2,031,397 total; 1,944,704 cached; 86,693 uncached |
| Output | 38,993 |
| Wall time | 332.2 s |

One validation-failed `add_reagent` attempt was retained and did not commit a physical operation.
All physical, session, checkpoint, token, tool-integrity and replay checks passed. At the official
rates recorded for the execution date, the externally calculated provider cost is USD 0.0285002;
the runner correctly leaves monetary accounting incomplete rather than writing an unverifiable
zero-cost claim. DeepSeek is now qualified for this campaign harness and envelope, not for an
unbounded task/model/scaffold matrix.

## Current V4 catalog and bounded-cost audit

Rechecked against the official DeepSeek API documentation on 2026-08-10. The supported API model
IDs are `deepseek-v4-flash` and `deepseek-v4-pro`; the legacy `deepseek-chat` and
`deepseek-reasoner` names were scheduled for retirement on 2026-07-24. The repository already uses
`deepseek-v4-flash`, so a retired legacy alias is not part of the observed Codex harness failure.
DeepSeek also states that the same `deepseek-v4-flash` slug now serves the 2026-07-31 model update
and natively supports the Responses API with Codex adaptation. This provider-managed moving alias
would need explicit version/provenance treatment in any formal provider amendment.

Official sources:

- <https://api-docs.deepseek.com/quick_start/pricing?article_id=article_1779470751466_8>
- <https://api-docs.deepseek.com/updates/>
- <https://api-docs.deepseek.com/api/list-models>

At the rates displayed on 2026-08-10, V4 Flash costs USD 0.0028 per million cache-hit input tokens,
USD 0.14 per million cache-miss input tokens, and USD 0.28 per million output tokens. If the current
three-arm qualification token envelopes were transferred unchanged to V4 Flash, the accepted
three-session schedule caps 7.2M cumulative input, 0.96M uncached input and 0.072M output. Its
cache-accounted cap is therefore
`0.96*0.14 + 6.24*0.0028 + 0.072*0.28 = USD 0.172032`. The qualification provider-process hard cap
also permits one infrastructure-only resume per arm, so reserving all six process attempts doubles
the enforceable qualification cap to USD 0.344064.

Treating every accepted-schedule input token as a cache miss gives USD 1.02816, but that deliberately
ignores the separately frozen uncached-input cap. It is a pricing stress counterfactual, not the
approved qualification contract hard cap. Under the current five-task, five-world, three-arm formal
design, transferring the same V4 Flash rates to the task-specific token envelopes yields 75 initial
provider attempts with 324M input, 43.2M uncached input and 3.24M output for USD 7.74144. Reserving
the full 150-attempt infrastructure-resume ceiling yields 648M input, 86.4M uncached input and 6.48M
output for USD 15.48288. The final formal ceiling must cover that 150-attempt amount and is enforced
by reserving each cell's complete token-envelope cost before provider-process launch.

These figures exclude taxes, account-specific charges and future price changes. They neither price
the frozen WellAU contract nor authorize a DeepSeek amendment or provider call. The current formal
method remains WellAU `gpt-5.6-sol` medium until an outcome-blind user-approved provider amendment
rebuilds all affected method, preflight, qualification, pricing and preregistration bindings.
