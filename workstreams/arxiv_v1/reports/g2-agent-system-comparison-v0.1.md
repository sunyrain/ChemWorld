# G2 matched agent-system demonstration

Both complete agent systems passed resource-ledger, exact-replay, provider qualification, and within-world physical-pair audits in all ten cells. The comparison is a platform and behavior-profile demonstration, not a model leaderboard or an isolated backend experiment.

| Complete agent system | Closed batches | Final assays | Discards | Operations | Non-final instruments | Assay commitment |
|---|---:|---:|---:|---:|---:|---:|
| gpt-5.6-sol / native Codex MCP session per vessel | 60 | 60 | 0 | 815 | 164 | 100% |
| deepseek-v4-flash / direct JSON decision per primitive operation with local dynamic schema validation | 60 | 24 | 36 | 889 | 163 | 40% |

## Within-system nominal-minus-opaque profiles

| System | Worlds nominal higher in best | Mean Δ best | Mean Δ operation-AUC | Δ operations | Δ assays | Δ discards |
|---|---:|---:|---:|---:|---:|---:|
| gpt-5.6-sol | 4/5 | +0.0778 | -0.0190 | -11 | +0 | +0 |
| deepseek-v4-flash | 4/5 | +0.1238 | +0.0361 | +67 | +8 | -8 |

Physical identity matched in 10/10 cells across world, mechanism, material instance, scoring, noise, workflow and resource-card identities.

Interpretation boundary: The design does not isolate a causal model-backend effect because the complete systems also differ in decision transport and scaffold.

Comparison hash: `5d534615aa0eb070b1a8ddf7cf123c2548bc8e4c948a98ffe2eafb0b545ef93e`
