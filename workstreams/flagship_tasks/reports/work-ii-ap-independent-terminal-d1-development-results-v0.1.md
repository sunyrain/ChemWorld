# Work II A-P independent terminal D1 development results

Status: terminal development evidence; platform requalification required; not formal/R5/C2 evidence.

## Coverage and outcome

The four frozen provider-by-task blocks reached `4/4` block terminal state and `12/12` immutable cell terminal state. Only `4/12` cells passed the complete qualification contract. Terminal therefore does not mean passed.

Across the planned `120` experiments, `99` completed and `9/12` cells reached 10/10. All `10/10` cells with committed physical operations passed exact replay. There were `0` provider error events, `0` missing cells and `0` invalid store receipts.

## Cell-level results

| Provider | Task | Arm | Disposition | Experiments | Ops committed/attempted | Replay | MCP recovered/max consecutive | Checkpoints | Final | Failure or failed gates |
|---|---|---|---|---:|---:|---|---:|---:|---|---|
| deepseek | reaction-safety-constrained | aligned_nominal | qualification_completed | 10/10 | 60/60 | pass | 0/0 | 5/5 | yes | none |
| deepseek | reaction-safety-constrained | misindexed_nominal | right_censored_retained | 10/10 | 90/90 | pass | 9/2 | 4/5 | no | MethodResourceLimitError: method resource limit exceeded: input_token_count, output_token_count; typed_belief_checkpoints_complete, provider_session_completed, final_recommendation_committed, provider_usage_reconciled, provider_operational_limits_reconciled |
| deepseek | reaction-safety-constrained | opaque | right_censored_retained | 10/10 | 70/70 | pass | 1/1 | 5/5 | yes | MethodResourceLimitError: method resource limit exceeded: input_token_count; provider_usage_reconciled |
| deepseek | electrochemical-conversion | aligned_nominal | infrastructure_failure_retained | 0/10 | 0/0 | not available | 0/0 | 0/5 | no | InteractiveCodexExperimentError: Codex failed before the next executable operation; no fallback action was emitted; planned_complete_experiments, typed_belief_checkpoints_complete, provider_session_completed, final_recommendation_committed, campaign_terminal, process_time_reconciled, exact_replay, execution_audit, provider_usage_reconciled |
| deepseek | electrochemical-conversion | misindexed_nominal | qualification_completed | 10/10 | 63/63 | pass | 2/1 | 5/5 | yes | none |
| deepseek | electrochemical-conversion | opaque | right_censored_retained | 9/10 | 61/62 | pass | 2/1 | 5/5 | yes | MethodResourceLimitError: method resource limit exceeded: input_token_count; planned_complete_experiments, campaign_terminal, provider_usage_reconciled |
| wellau | reaction-safety-constrained | aligned_nominal | qualification_completed | 10/10 | 70/70 | pass | 0/0 | 5/5 | yes | none |
| wellau | reaction-safety-constrained | misindexed_nominal | infrastructure_failure_retained | 0/10 | 0/0 | not available | 0/0 | 0/5 | no | OSError: [WinError 1450] 系统资源不足，无法完成请求的服务。; planned_complete_experiments, typed_belief_checkpoints_complete, provider_session_completed, final_recommendation_committed, campaign_terminal, process_time_reconciled, exact_replay, execution_audit, provider_usage_reconciled |
| wellau | reaction-safety-constrained | opaque | qualification_completed | 10/10 | 69/70 | pass | 1/1 | 5/5 | yes | none |
| wellau | electrochemical-conversion | aligned_nominal | right_censored_retained | 10/10 | 80/80 | pass | 10/4 | 4/5 | no | typed_belief_checkpoints_complete, provider_session_completed, final_recommendation_committed, provider_operational_limits_reconciled |
| wellau | electrochemical-conversion | misindexed_nominal | right_censored_retained | 10/10 | 80/80 | pass | 5/2 | 4/5 | no | typed_belief_checkpoints_complete, provider_session_completed, final_recommendation_committed, provider_operational_limits_reconciled |
| wellau | electrochemical-conversion | opaque | right_censored_retained | 10/10 | 80/80 | pass | 4/2 | 4/5 | no | typed_belief_checkpoints_complete, provider_session_completed, final_recommendation_committed, provider_operational_limits_reconciled |

## Interpretation boundary

This block supports execution and failure-mode diagnosis only. Missingness and censoring depend on provider, task and arm, so the retained trajectories do not support a scientific provider/model/arm comparison or formal admission.

The frozen scientific gates remain unchanged: three arms, ten experiments, checkpoints at 0/2/4/7/10, participant-authored final recommendation, exact replay, resource accounting, all-failure retention, immutable terminals and missing-infrastructure-only retry.

Before requalification, the platform must separate provider/network, transport/IPC/OS and agent-invalid schema/timing failures; expose an actionable checkpoint/final closeout state without authoring participant content; classify zero-operation infrastructure failures before permanent terminal disposition; parse reports as UTF-8 from terminal store receipts; and prospectively freeze provider-specific cached/uncached/output/cost envelopes. All four affected blocks must then restart from their first cell in new output roots.
