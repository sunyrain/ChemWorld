# ChemWorld-Bench

<p class="cw-site-version">当前站点版本：中文发布版 · 2026-07-09</p>

ChemWorld-Bench 是面向闭环虚拟化学实验的研究级 benchmark。正式的
Gymnasium 入口是 `ChemWorld`：所有任务都来自同一个物理化学世界律的切片，
而不是彼此独立的小游戏。

当前范围：

- 一个共享的 `world_law_id`：`chemworld-physical-chemistry`；
- 14 个已注册任务切片，覆盖反应优化、安全、机理解释、表征、纯化、分配发现、
  结晶、蒸馏、连续流、电化学和 tool-agent 规划；
- 机制驱动的运行时服务、typed ledger、transaction record、带噪仪器观测、
  虚拟光谱、replay verification 和任务级评测指标；
- 显式成熟度元数据，避免把 proxy、lite、reference-validated 和
  professional-candidate 组件混在一起声明。

## 快速入口

| 目标 | 入口 |
| --- | --- |
| 先理解 ChemWorld 是什么 | [项目总览](chemworld_overview_zh.md) 与 [当前进展](current_progress.md) |
| 直接运行环境和任务 | [环境卡](env_cards.md)、[任务列表](tasks.md)、[任务卡](task_cards.md) |
| 给 agent / optimizer 接入 | [Agent 交互接口](agent_interface.md)、[操作协议](operations.md)、[Action Schema](action_schema.md)、[Wrappers](wrappers.md) |
| 做正式 benchmark 评测 | [评测协议](benchmark_protocol.md)、[Baseline 参考](baseline_reference.md)、[提交包](submission.md) |
| 导出数据和论文产物 | [数据集层](dataset_layer.md)、[论文产物](paper_artifact.md)、[伦理与数据](ethics_and_data.md) |
| 理解世界模型底座 | [架构设计](architecture.md)、[世界律](world_law.md)、[物理化学核心设计](physchem_core_design.md) |
| 检查环境是否自洽 | [环境自一致性审计](environment_self_consistency_audit_zh.md)、[物化成熟度审计](physchem_maturity_audit.md) |
| 使用课程和示例材料 | [教程课程图](tutorial_curriculum_zh.md)、[演示](demos.md)、[Agent 交互示例](agent_interaction_examples.md) |
| 准备 release | [路线图](roadmap.md)、[发布检查表](release_checklist.md)、[项目管理](project_management.md) |

## 当前闸门

当前文档和实现预期通过：

```bash
python -m ruff check .
python -m mypy src/chemworld
python -m pytest
python -m mkdocs build --strict
python scripts/audit_environment_consistency.py --tasks all --seeds 0 1 2
```

最近一次本地 self-consistency audit 对已注册任务集报告：零 replay failure、零
spectra failure、零 invalid smoke step、零 constitution failure。

## 边界说明

ChemWorld 不是现实反应预测器、DFT wrapper、流程模拟器或机器人控制器。它是一个
面向 agent、学生和 optimizer 的可控虚拟交互环境。物理模块只应在声明的成熟度边界
内使用，benchmark 声明必须携带 registry 产出的 task maturity metadata。
