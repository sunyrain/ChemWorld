# Reproduction

Use the EQ-E v0.2 freeze manifest. Maintain the configured persistent SSH proxy tunnel for background provider access. Run the zero-provider gate, freeze, W01 three-arm canary, and the remaining matrix with at most eight isolated workers. Generate truth only after all 15 K2 responses are sealed, then run this exporter. The ignored run namespace retains trajectories, preflight failures, reference repeats, process material, and provider-private files; this public package excludes authentication, raw model streams, session identifiers, private entity parameters, and usage accounting.

## Public agent-visible source trajectories

The public EQ-E package contains one sanitized `trajectory.jsonl` for each effective source campaign. Every attempted operation remains in order with the public decision context, selected action and audit, complete agent-visible environment response, and transaction result. Export requires exact operation-count and twelve-batch-summary equality between the effective source trajectory, effective result, and existing public result. Authentication material, raw provider events, provider session identifiers, usage accounting, evaluator-only state, and private world parameters remain excluded. No source campaign, posttest, prediction, truth value, or score is rerun or changed.
