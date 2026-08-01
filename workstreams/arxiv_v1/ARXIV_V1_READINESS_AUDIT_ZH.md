# ChemWorld 第一版 arXiv 完成度与剩余实验终态审计

审计日期：2026-08-02（Asia/Shanghai）

机器权威：`reports/g2-v0.5-remaining-experiment-audit-live-v0.1.json`

实验量审计 SHA-256：`c609cd34867331d6df41e7b72a1c01429fd48c42b3400f9e9a331956b49a5563`

G2 v0.5 科学审计 SHA-256：`7bb4045fa1ca041de047d967a31ed3d89d5f8ad83851aa7b469144b4da37f28d`

## 结论

第一版所需的新科学实验已经全部终态化并通过 fail-closed 审计。必需新增实验数为 **0**，待终态 cell 为 **0**，待解析 vessel opportunity 为 **0**。现在剩余的是发布、归档、格式和独立复现工作，不是补做科学矩阵。

论文应同时报告三种不能互换的总量：

| 计数口径 | G2 v0.5 | 项目总计 |
| --- | ---: | ---: |
| 预设实验机会 | 120 | 29,760 |
| 已启动/执行的物理实验 | 114 | 29,754 |
| 完成实验或 final assay | 112 | 29,752 |

29,760 只是固定设计分母，不能称为实际执行或完成实验数。

## 1. 第一版证据矩阵

| 层级 | 终态 | 第一版作用 |
| --- | --- | --- |
| 环境资格 | 15 tasks、28 operations、5 instruments、415 deterministic cases、62/62 evaluator-bound endpoints | 证明声明能力与可达性，不外推为全部任务上的 Agent 性能 |
| G0 compiled control | 29,580 个去重物理实验 | 任务依赖优化、先验干预、优化与认知端点解耦 |
| G2 v0.4 autonomous development | 10 cells、60/60 vessels、815 个自主 primitive operations | 建立逐操作生命周期与 discovery/retention/drawdown/recovery 指标，选择复制世界 |
| G2 v0.5 fresh trajectories | 20/20 cells 终态；18 completed、2 right-censored | 检验固定物理世界内行为结构能否跨新 Agent 轨迹重复 |
| 主文稿 | 摘要、Results 3--7、Discussion、Methods 9.1--9.6 均已写入终态结果 | 只剩引用格式、统计措辞和最终 claim audit |
| 显示项 | Tables 1--4、Figures 1--6 | 均由 frozen derived JSON 生成 |
| 数据链 | self-hashed derived JSON、6 CSV、figure manifest、G2 终态索引、compact replay subset | 禁止手工复制主表数字 |

## 2. G2 v0.5 终态实验量

### 2.1 Cell、vessel 与配对

| 对象 | 固定总量 | 完成 | 右删失 | 未决 |
| --- | ---: | ---: | ---: | ---: |
| cells | 20 | 18 | 2 | 0 |
| vessel opportunities | 120 | 112 个 final assays | 2 个已启动未完成；6 个未启动 | 0 |
| trajectory pairs | 10 | 8 | 2 | 0 |

每个世界均有 4 个完整 pair 和 1 个 right-censored pair，超过冻结策略要求的每世界至少 3 个完整 pair。不存在补抽、替换或结果依赖停止。

### 2.2 两个右删失 cell

- `cell-001`：world 1、r01、nominal；50 个 accepted operations；3 个 vessel starts；2 个 final assays。
- `cell-019`：world 3、r05、opaque；56 个 accepted operations；3 个 vessel starts；2 个 final assays。

两者均为动作后的 `provider_infrastructure_failure`：各有一个已启动但未完成 vessel，并各失去三个未启动机会。每个 cell 只有一个正式 attempt。内部 `codex.exe` session 轮换不构成 attempt-level retry。全部终态 cell 的 attempt-selection、物理配对、资源重放和 exact replay 门禁均通过。

### 2.3 为什么三个总数不同

```text
29,640 已有完成/审计实验
+ 114 G2 v0.5 已执行 vessels
= 29,754 已执行物理实验

29,640 已有完成/审计实验
+ 112 G2 v0.5 final assays
= 29,752 完成实验

29,640 + 120 预设机会 = 29,760 设计分母
```

差额不是数据缺失：两个已启动 vessel 因基础设施失败没有 final assay，六个机会因 cell 永久右删失从未启动。

## 3. 终态科学结果

冻结解释映射机械选择 `frequent_within_world_reversal`：8 个 world × core-lifecycle 分类中有 6 个为 mixed，没有任何 core lifecycle metric 在两个世界中呈现各自稳定而方向相反的模式。

- world 1：best-score 中位差 `+0.228`、mean-score 中位差 `+0.224`，均为 3 正 1 负；discovery 和 retention 为 mixed；drawdown 为 3 负 1 正（nominal 回撤通常更小）；terminal/best 为 3 正 1 负。
- world 3：mean-score 中位差 `-0.065`，3 负 1 正；best-score 为 2 正 2 负；discovery、retention、drawdown、terminal/best 全部 mixed。

第一版最有力且证据匹配的结论不是“先验有益/有害”，而是：**端点方向性不保证产生它的实验生命周期可重复。** 固定物理身份以后，新 Agent 轨迹仍频繁翻转 discovery、retention、drawdown 和 terminal behavior；prior response 不能被压缩成模型或世界的单一标量属性。

该结论只适用于两个经开发结果选择的世界。不得合并总体 p 值，不得估计一般世界中的先验效应频率，也不得把未受控的 provider sampling 写成已识别的因果来源。

## 4. 还差多少实验

| 类别 | 第一版必需剩余量 |
| --- | ---: |
| G0 新实验 | 0 |
| G2 v0.5 新实验 | 0 |
| G2 待终态 cells | 0 |
| G2 待解析 opportunities | 0 |
| 可选 post-arXiv 实验 | 0（对第一版） |

以下矩阵具有后续研究价值，但不是第一版的隐藏门槛：matched compiled-vs-agent-directed control（约 240 次）、G2 misindexed-prior 三臂扩展（约 180 次）、counterfactual feedback branching、多任务/多模型/多 provider 复制和现实实验 bridge。

## 5. 非实验发布门禁

已经完成：

1. G2 v0.5 terminal audit；
2. frozen derived JSON、六个 CSV、Table 4 和 Figure 5；
3. 677-file G2 终态 SHA-256 索引（279,923,501 bytes）；
4. 四 cell compact replay subset：一个完整 pair 与两个 right-censored cells；
5. 摘要与 Section 7 终态结果写入。

仍需完成：

1. 在最终 source commit 上刷新 evidence graph；
2. full tests、clean-wheel 安装和 terminal replay；
3. 从独立 checkout 重建 derived data、图表和审计；
4. 给约 17.7 GB G0 原始根目录取得持久外部 archive identifier；
5. 参考文献目标格式、统计语言与最终主张审计。

依赖关系为：

```text
terminal G2 audit（完成）
        |
        v
frozen derived data + Figures/Tables（完成）
        |
        v
final evidence + wheel + replay + independent checkout（待完成）
        |
        v
arXiv package

external G0 archive identifier ------------------------^
```

因此，当前不应暂停来修改科学设计或追加矩阵；应继续完成证据与发布闭环。
