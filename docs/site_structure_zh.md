# 站点层级规划

当前站点采用“导航先稳定、文件后迁移”的策略。也就是说，先在
`mkdocs.yml` 中固定读者看到的信息架构，暂时不批量移动 `docs/` 下的文件路径。
这样可以避免大量断链，同时让公开站点先变得更像专业 Gym / benchmark 文档。

## 参考原则

专业交互环境文档通常不是按内部开发历史组织，而是按使用路径组织：

- 先给新用户快速入口；
- 再解释环境、任务和 action/observation 合同；
- 然后给 agent、baseline、dataset、benchmark protocol；
- 最后放内部架构、审计、开发路线图。

ChemWorld 当前导航因此不再把“项目状态、核心概念、Benchmark 合同、审计”平铺在同一层，
而是收束为：

```text
首页
快速开始
环境与任务
Agent 交互
Benchmark 与评测
数据与产物
世界模型底座
审计与状态
开发与发布
```

## 当前展示结构

```text
首页
├── 快速开始
│   ├── 项目总览
│   ├── 当前进展
│   ├── 演示
│   ├── 教程课程图
│   └── API 参考
├── 环境与任务
│   ├── 环境卡
│   ├── 世界律
│   ├── 任务分类
│   ├── 任务列表
│   ├── 任务卡
│   ├── 场景生成
│   ├── Campaign 模型
│   └── 反应与分离任务
├── Agent 交互
│   ├── Agent 交互接口
│   ├── 操作协议
│   ├── Action 协议
│   ├── Wrapper 与合法性
│   ├── LLM Agent Harness
│   └── Agent 交互示例
├── Benchmark 与评测
│   ├── 评测协议
│   ├── Baseline 参考
│   ├── 提交包
│   ├── 安全与成本
│   ├── 本地评测机
│   └── 榜单蓝图
├── 数据与产物
│   ├── 数据集层
│   ├── 论文产物
│   └── 伦理与数据
├── 世界模型底座
│   ├── 架构设计
│   ├── 技术架构
│   ├── 物理化学核心设计
│   ├── Mechanism 协议
│   ├── 仪器合同
│   ├── 虚拟光谱
│   ├── Backend 后端
│   └── World Model 学习
├── 审计与状态
│   ├── 环境自一致性审计
│   ├── 物化成熟度审计
│   ├── SOTA Agent 环境差距审计
│   ├── 代码审计
│   ├── 站点审计
│   ├── 站点层级规划
│   └── Codex 5.5 Medium 行为报告
└── 开发与发布
    ├── 路线图
    ├── 发布检查表
    ├── 项目管理
    ├── 本地参考仓库
    └── 统一任务板
```

## 未来文件目录结构

```text
docs/
├── index.md
├── en/
│   └── index.md
├── getting-started/
│   ├── chemworld_overview_zh.md
│   ├── current_progress.md
│   ├── demos.md
│   ├── tutorial_curriculum_zh.md
│   └── api_reference.md
├── environments/
│   ├── env_cards.md
│   ├── world_law.md
│   ├── task_taxonomy.md
│   ├── tasks.md
│   ├── task_cards.md
│   ├── scenario_generation.md
│   ├── campaign_model.md
│   └── reaction_separation_tasks.md
├── agent-interface/
│   ├── agent_interface.md
│   ├── operations.md
│   ├── action_schema.md
│   ├── wrappers.md
│   ├── llm_agent_harness.md
│   └── agent_interaction_examples.md
├── benchmark/
│   ├── benchmark_protocol.md
│   ├── baseline_reference.md
│   ├── submission.md
│   ├── safety_cost.md
│   ├── local_eval_machine.md
│   └── leaderboard_project_blueprint.md
├── datasets/
│   ├── dataset_layer.md
│   ├── paper_artifact.md
│   └── ethics_and_data.md
├── foundation/
│   ├── architecture.md
│   ├── technical_architecture_zh.md
│   ├── physchem_core_design.md
│   ├── mechanism_schema.md
│   ├── instrument_contracts.md
│   ├── spectroscopy.md
│   ├── backends.md
│   └── world_model_learning.md
├── audits/
│   ├── environment_self_consistency_audit_zh.md
│   ├── physchem_maturity_audit.md
│   ├── sota_agent_environment_gap_audit.md
│   ├── code_review_audit.md
│   ├── site_audit_zh.md
│   ├── site_structure_zh.md
│   └── codex55_medium_behavior_report.md
└── development/
    ├── roadmap.md
    ├── release_checklist.md
    ├── project_management.md
    ├── reference_repos.md
    └── todo.md
```

## 迁移顺序

1. 先保持现有文件路径，用 `mkdocs.yml` 固定展示层级。
2. 稳定一周后，优先移动 `getting-started/`、`development/`、`audits/` 三组低耦合文档。
3. 再移动 `environments/`、`agent-interface/`、`benchmark/`、`datasets/`、`foundation/`。
4. 每一批迁移后运行 `python -m mkdocs build --strict`，确保没有断链。
5. 如果站点已经被外部引用，再引入静态跳转页或 `mkdocs-redirects` 保留旧 URL。

## 命名规则

- 中文页面文件名继续使用英文 slug，保证 URL 稳定且便于引用。
- 一级目录按读者任务划分，而不是按作者或历史来源划分。
- `en/` 先保留英文首页，后续若要完整双语化，可逐页扩展为镜像结构。
- 评测合同、任务卡、schema 和提交协议属于稳定 public contract，应优先避免频繁改 URL。
