# LLM Agent Harness

ChemWorld 当前默认不依赖在线 LLM API。首版 harness 采用可复现的离线协议：

```text
Planner -> Action Validator -> Env Step -> Observation Summarizer -> Memory -> Next Action
```

这样可以先把 tool-use、validator-use、observation-use 和 replay 评测打牢，再接入在线模型。

## ToolUsingLLMStubAgent

`ToolUsingLLMStubAgent` 是确定性的 tool-using LLM stub。它不调用模型，但会模拟一个 LLM/tool agent 应该留下的行为记录：

- prompt input 摘要；
- selected action；
- reasoning summary；
- hypothesis note；
- validator result；
- observation summary；
- memory note。

运行示例：

```bash
python examples/demo_llm_replay_harness.py
```

## LLMReplayAgent

`LLMReplayAgent` 从 JSONL 读取固定 action trace，用于复现实验、教学展示和之后对真实 LLM trace 的离线评测。

```json
{"action": {"operation": "add_solvent", "volume_L": 0.028, "solvent": 2}}
{"action": {"operation": "add_reagent", "amount_mol": 0.010}}
{"action": {"operation": "terminate"}}
{"action": {"operation": "measure", "instrument": "final_assay"}}
```

公开 fixture：

```text
examples/fixtures/llm_replay/reaction_to_assay_public_trace.jsonl
```

## Codex Subagent Baseline

可复现评测定义两层 Codex baseline：

- `codex_subagent_online`：在线运行协议。它使用 `task_prompt()`、`available_actions()`、`validate_action()`、`lab_report` 和 `campaign_state()`，每一步先验证 action，再执行环境 step。在线结果应记录模型名、日期、配置、prompt 摘要、动作、验证结果、观测摘要和假设更新。
- `codex_subagent_replay`：可复现 replay agent。它读取或生成固定 action trace，用于 artifact、CI 和本地复现。

仓库内默认不直接调用在线 Codex API 或外部子 agent。在线运行结果应先落盘为 replay trace，再进入论文 artifact。

Trace 规范：

```json
{
  "prompt_summary": "public task and observation summary",
  "selected_action": {"operation": "measure", "instrument": "ph_meter"},
  "validation_result": {"valid": true, "reasons": []},
  "observation_summary": "public lab-report summary",
  "hypothesis_note": "short mechanism or next-step note",
  "model_metadata": {
    "model_name": "codex-5.5-medium",
    "run_date": "YYYY-MM-DD",
    "mode": "online_or_replay"
  }
}
```

不要保存完整 chain-of-thought；只保存可审计的 reasoning summary 和 decision evidence。

## Trace Policy

`agent_trace` 只保存行为摘要，建议记录：

- prompt/task 摘要；
- validator 结果；
- selected action；
- observation-use 摘要；
- hypothesis or next-step rationale；
- memory note。
