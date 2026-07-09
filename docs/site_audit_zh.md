# 文档站审计与收束报告

本文档记录当前 ChemWorld 文档站的结构审计结果。目标不是继续堆页面，
而是让外部研究者、课程使用者和开发者都能快速找到正确入口。

## 当前判断

当前文档站已经覆盖主要内容，但此前存在三个问题：

1. 一级导航过长，读者很难判断哪些页面是主线文档，哪些是审计记录或开发工作板。
2. 部分页面仍保留快速迭代阶段的语气，例如历史迁移、占位 baseline、过时测试数量。
3. 任务、runtime、maturity、self-consistency audit 已经成为当前阶段主线，但首页没有把这些放在首屏。

本轮已把站点收束为七个分区：

| 分区 | 作用 |
| --- | --- |
| 项目状态 | 当前进度、站点审计、发布检查、路线图 |
| 核心概念 | 项目定位、世界规律、核心架构、物理化学底座 |
| Benchmark 合同 | 环境、任务、动作、机制、仪器、提交和评测协议 |
| 评测与数据 | baseline、dataset、本地评测机、leaderboard、paper artifact |
| 教程与示例 | 12 天教程、示例、API |
| 审计 | 自洽性、成熟度、SOTA 对比、agent 行为、代码审计 |
| 开发与发布 | 双人协作、参考仓库、专业 TODO |

## 当前主线

当前文档站应围绕这条主线组织：

```text
ChemWorld overview
  -> world law and runtime architecture
  -> task registry and task cards
  -> action/instrument/observation contracts
  -> benchmark protocol and submission bundle
  -> baseline and dataset outputs
  -> self-consistency and maturity audits
```

这条路径避免把 ChemWorld 描述成一组松散示例。任务是同一物理化学世界规律下的不同切片。

## 已完成收束

- 首页改为读者路径入口，而不是链接堆叠页。
- MkDocs 导航改为分区导航。
- `current_progress.md` 改为当前 `main` 分支状态摘要。
- `task_cards.md` 增加当前任务矩阵，并明确 task card 是 registry 生成的发布合同。
- `campaign_model.md` 扩展为 campaign / experiment / operation 的正式语义页。
- `env_cards.md` 扩展为环境能力、`task_info()` 字段和 audit 入口说明。
- `roadmap.md` 改为当前阶段的 P0/P1/P2/P3 收束路线。
- `release_checklist.md` 增加 environment audit、site audit、baseline artifact 和 maturity gate。

## 仍需跟踪

### 任务 profile 需要继续收紧

自洽性审计能跑通所有任务，但也标记了一个真实设计风险：
部分 broad process task 仍允许过多跨模块操作。未来冻结 release task 时，应让每个 task profile 只暴露该任务需要的 operation capability。

### Baseline 表需要冻结

`chemworld baselines report` 已经是正式工具，但公开论文/榜单版本还需要固定：

- release task set；
- seeds；
- agent versions；
- baseline commands；
- generated result table；
- maturity metadata；
- platform commit。

### 部分历史审计页较长

`code_review_audit.md`、`physchem_core_design.md`、`professional_todo.md`
记录了大量过程信息。它们保留在“审计 / 开发与发布”分区，但不再作为首页入口。
后续如果准备公开文档站，可以再拆成 archive 或 developer notes。

## 文档站验收

每次收束后至少运行：

```bash
python -m mkdocs build --strict
python -m pytest tests/test_environment_self_consistency.py
python scripts/audit_environment_consistency.py --tasks all --seeds 0 1 2
```

发布前再运行完整门禁：

```bash
python -m ruff check .
python -m mypy src/chemworld
python -m pytest
python -m mkdocs build --strict
```

## 当前结论

站点现在应被视为“科研预发布文档站”，而不是教学 demo 页面集合。它的中心是：

- `ChemWorld` 单一环境；
- 共享 world law；
- task registry；
- runtime v2；
- instrument observation；
- benchmark protocol；
- self-consistency audit；
- maturity boundary。

下一阶段文档优化应围绕 baseline 冻结、task profile 收紧和 release artifact 生成，而不是继续增加横向页面数量。
