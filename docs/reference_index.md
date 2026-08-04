# 技术参考索引

主导航只保留理解、体验、构建和评测 ChemWorld 所需的核心路径。全部低层规范仍在这里可查，
也可以使用站内搜索按类、字段或命令定位。

## 世界与运行时

- [规范系统模型](architecture.md)
- [Campaign 与状态模型](campaign_model.md)
- [世界律与版本](world_law.md)
- [场景生成](scenario_generation.md)
- [隐藏机理与世界族](mechanism_schema.md)
- [计算后端与物理 Provider](backends.md)
- [虚拟世界的有效性](world_validity.md)

## 物理、仪器与材料

- [物理化学模型总览](physchem_core_design.md)
- [模型成熟度](model_maturity.md)
- [反应与分离流程](reaction_separation_tasks.md)
- [安全与成本](safety_cost.md)
- [仪器合同](instrument_contracts.md)
- [虚拟光谱](spectroscopy.md)
- [材料身份](material_identity.md)

## Agent 与操作

- [Agent API](agent_interface.md)
- [World authoring contract](world-authoring-contract.md)
- [World composition contract](world-composition-contract.md)
- [Public world-authoring examples](world-composition-examples.md)
- [Coverage-guided composition generation](world-composition-coverage.md)
- [World capability map](world-capability-map.md)
- [认识操作语言](operations.md)
- [编写 Action 与 Recipe](action_schema.md)
- [使用 Wrapper](wrappers.md)
- [交互示例](agent_interaction_examples.md)
- [LLM 实验智能体](llm_agent_harness.md)
- [RL 与 World Model](world_model_learning.md)

## 任务、数据与评测

- [完整任务目录](tasks.md)
- [任务卡](task_cards.md)
- [环境卡](env_cards.md)
- [任务分类](task_taxonomy.md)
- [数据集层](dataset_layer.md)
- [Baseline 与资源](baseline_reference.md)
- [Seed 与数据划分](seed_suite.md)
- [验证安装与结果](validation.md)
- [本地评测机](local_eval_machine.md)
- [API Reference](api_reference.md)
- [示例与 Notebook](demos.md)

## 教学、发布与治理

- [教学路线](tutorial_curriculum_zh.md)
- [提交、回放与私有评测](submission.md)
- [结果可信链](release_integrity.md)
- [伦理与数据](ethics_and_data.md)

状态类问题不要从技术页拼接推断，请直接查
[证据与当前状态](benchmark_release.md)和机器可读的
[`configs/current.json`](https://github.com/sunyrain/ChemWorld/blob/main/configs/current.json)。
