# Work II A-P independent terminal D1 development results

Status: terminal development evidence; platform requalification complete; not formal/R5/C2 evidence.

## Coverage and outcome

The four frozen provider-by-task blocks reached `4/4` block terminal state and `12/12` immutable cell terminal state. Only `4/12` cells passed the complete qualification contract. Terminal therefore does not mean passed.

Across the planned `120` experiments, `94` completed and `9/12` cells reached 10/10. All `11/11` cells with committed physical operations passed exact replay. There were `0` provider error events, `0` missing cells and `0` invalid store receipts.

## Cell-level results

| Provider | Task | Arm | Disposition | Experiments | Ops committed/attempted | Replay | MCP recovered/max consecutive | Checkpoints | Final | Failure or failed gates |
|---|---|---|---|---:|---:|---|---:|---:|---|---|
| deepseek | reaction-safety-constrained | aligned_nominal | right_censored_retained | 10/10 | 79/79 | pass | 11/2 | 4/5 | no | typed_belief_checkpoints_complete, provider_session_completed, final_recommendation_committed, provider_operational_limits_reconciled |
| deepseek | reaction-safety-constrained | misindexed_nominal | qualification_completed | 10/10 | 70/70 | pass | 0/0 | 5/5 | yes | none |
| deepseek | reaction-safety-constrained | opaque | qualification_completed | 10/10 | 71/71 | pass | 1/1 | 5/5 | yes | none |
| deepseek | electrochemical-conversion | aligned_nominal | qualification_completed | 10/10 | 62/62 | pass | 0/0 | 5/5 | yes | none |
| deepseek | electrochemical-conversion | misindexed_nominal | right_censored_retained | 10/10 | 83/83 | pass | 7/3 | 4/5 | no | typed_belief_checkpoints_complete, provider_session_completed, final_recommendation_committed, provider_operational_limits_reconciled |
| deepseek | electrochemical-conversion | opaque | right_censored_retained | 10/10 | 81/81 | pass | 11/3 | 4/5 | no | typed_belief_checkpoints_complete, provider_session_completed, final_recommendation_committed, provider_operational_limits_reconciled |
| wellau | reaction-safety-constrained | aligned_nominal | right_censored_retained | 10/10 | 60/61 | pass | 3/3 | 5/5 | yes | provider_operational_limits_reconciled |
| wellau | reaction-safety-constrained | misindexed_nominal | qualification_completed | 10/10 | 61/61 | pass | 0/0 | 5/5 | yes | none |
| wellau | reaction-safety-constrained | opaque | right_censored_retained | 2/10 | 12/12 | pass | 48/48 | 2/5 | no | InteractiveCodexExperimentError: Codex session crossed a frozen operational limit before action acceptance; no fallback action was emitted: max_recovered_mcp_tool_failures; planned_complete_experiments, typed_belief_checkpoints_complete, provider_session_completed, final_recommendation_committed, campaign_terminal, provider_usage_reconciled, provider_operational_limits_reconciled |
| wellau | electrochemical-conversion | aligned_nominal | right_censored_retained | 10/10 | 80/81 | pass | 8/3 | 4/5 | no | typed_belief_checkpoints_complete, provider_session_completed, final_recommendation_committed, provider_operational_limits_reconciled |
| wellau | electrochemical-conversion | misindexed_nominal | right_censored_retained | 2/10 | 12/12 | pass | 49/48 | 2/5 | no | InteractiveCodexExperimentError: Codex session crossed a frozen operational limit before action acceptance; no fallback action was emitted: max_recovered_mcp_tool_failures; planned_complete_experiments, typed_belief_checkpoints_complete, provider_session_completed, final_recommendation_committed, campaign_terminal, provider_usage_reconciled, provider_operational_limits_reconciled |
| wellau | electrochemical-conversion | opaque | infrastructure_failure_retained | 0/10 | 0/0 | not available | 5/5 | 1/5 | no | InteractiveCodexExperimentError: Codex session crossed a frozen operational limit before action acceptance; no fallback action was emitted: max_recovered_mcp_tool_failures; planned_complete_experiments, typed_belief_checkpoints_complete, provider_session_completed, final_recommendation_committed, campaign_terminal, process_time_reconciled, exact_replay, execution_audit, provider_usage_reconciled, provider_operational_limits_reconciled |

## Platform requalification

Typed MCP failure accounting is complete for `12/12` cells: provider/network `0`, transport/IPC/OS `1`, agent-invalid `142`, and unclassified `0`.

Frozen platform gates: pass.

## Interpretation boundary

This block supports execution and failure-mode diagnosis only. Missingness and censoring depend on provider, task and arm, so the retained trajectories do not support a scientific provider/model/arm comparison or formal admission.

The frozen scientific gates remain unchanged: three arms, ten experiments, checkpoints at 0/2/4/7/10, participant-authored final recommendation, exact replay, resource accounting, all-failure retention, immutable terminals and missing-infrastructure-only retry.

Use the complete development result to decide qualification readiness. Any platform change still requires its affected qualification block to restart from the first cell; retained scientific failures are not retryable.
