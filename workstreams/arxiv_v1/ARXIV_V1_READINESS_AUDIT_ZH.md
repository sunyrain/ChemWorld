# ChemWorld 第一版 arXiv 完成度与剩余实验审计

审计快照：2026-08-02 02:14（Asia/Shanghai）。

机器权威：
`reports/g2-v0.5-remaining-experiment-audit-live-v0.1.json`，审计 SHA-256 为
`74aad2fb0a7a7637890b928f1c248da11bee8db73d3ef6e1bc6a95fb5a2cb203`。

本文件区分三件事：已经完成的科学证据、仍需终态化的预定实验，以及不需要新增实验但
仍须完成的发布工件。所有 pending-cell 字节只用于运行监控，不进入论文结果。

## 1. 第一版已经具备什么

| 层级 | 当前状态 | 第一版中的作用 |
| --- | --- | --- |
| 环境资格 | 15 个任务、28 类操作、5 类仪器、415 个确定性完整实验用例、62 个显式绑定端点 | 证明 apparatus 的声明能力与可达性，不外推为 15 个任务上的 Agent 性能 |
| G0 compiled control | 29,580 个去重物理实验，双任务、三信息臂及经典方法均已有正式汇总 | 任务依赖优化、先验干预、优化与认知端点分离 |
| G2 v0.4 autonomous development | 10 个 cell、60/60 个完整实验、815 个自主 primitive operations | 建立逐操作生命周期、发现、保留、回撤和恢复指标，并选择复制世界 |
| G2 v0.5 fresh trajectories | 20-cell 固定矩阵正在执行 | 判断选定世界内的实验行为是否能跨新轨迹重复 |
| 主文稿 | Introduction、Related work、Results 3--6、Discussion、Methods 9.1--9.6 已写实 | Section 7 和摘要中的 v0.5 结果句保持占位 |
| 显示项 | Figures 1--4、6；Tables 1--3；六份完整图注 | Figure 5 与 Table 4 的数值内容由终态 v0.5 自动解锁 |
| 数据链 | self-hashed derived JSON、五个 CSV、figure manifest、display-item renderer | 禁止手工复制主表数值，所有显示项绑定一个数据源 |
| 证据门禁 | 55/55 evidence nodes 通过 | 最终 commit、clean wheel 和独立 checkout 后仍须再验证 |

## 2. 还差多少科学实验

第一版不再需要任何新的 G0 实验，也不要求额外 G1、misindexed-G2、feedback branching、
多任务自主矩阵或现实实验室 bridge。唯一必须完成的新科学矩阵是 G2 v0.5。

### 2.1 固定设计与当前终态量

| 计数对象 | 固定总量 | 当前正式终态 | 尚待解析 |
| --- | ---: | ---: | ---: |
| G2 v0.5 cells | 20 | 8 completed + 1 right-censored | 11 cells |
| vessel opportunity slots | 120 | 54 slots 已由终态 cell 解析 | 66 slots |
| 已执行 vessel，仅计终态 cell | 最终值未知 | 51 | 不用 120 减 51 解释“剩余实验” |
| completed final assays，仅计终态 cell | 最终值未知 | 50 | 终态审计后冻结 |
| trajectory pairs | 10 | 3 completed + 1 right-censored | 6 unresolved pairs |

因此，最清晰的答案是：**还差 11 个 cell 终态化，对应 66 个尚未解析的预定实验机会位**。
“66”是剩余设计机会，不保证最终会形成 66 个已执行且完成终测的实验；方法失败可产生
新的右删失。

### 2.2 为什么 120、117、116 不能混用

已右删失的 `cell-001` 启动了 3 个 vessel，但只完成 2 次 final assay。该 cell 的另外 3 个
机会位因 cell 终态而永远不会启动。由此即使所有尚未解析机会都完成：

- G2 v0.5 的最大已执行 vessel 数是 117；
- G2 v0.5 的最大 completed final-assay 数是 116；
- 加上既有 G0 和 G2 v0.4，最大已执行物理实验总数是 29,757；
- 最大完成实验总数是 29,756；
- 29,760 只是不因删失而改变的 planned-opportunity denominator。

论文最终必须同时报告 planned opportunities、executed vessels 和 completed final assays，
不能把三者写成一个“实验数量”。

### 2.3 当前可见但未晋升的运行字节

在本快照时，全部目录中可读到 54 次 vessel start、52 次 final assay 和 738 次 primitive
operation。其中 pending cells 比正式终态量多 3 次 start、2 次 final assay；这些值只证明
运行仍在推进，不得进入摘要、Figure 5、Table 4 或结果解释。

### 2.4 配对分析容量

| 选定物理世界 | 计划 pairs | 完整 pairs | 右删失 pairs | 未解析 pairs | 最终最多完整 pairs |
| --- | ---: | ---: | ---: | ---: | ---: |
| world 1 | 5 | 1 | 1 | 3 | 4 |
| world 3 | 5 | 2 | 0 | 3 | 5 |
| 合计 | 10 | 3 | 1 | 6 | 9 |

右删失 pair 保留在设计分母中，但不制造 nominal-minus-opaque 差值。两个选定世界分别报告
五个 replicate 的状态和可用差值，不合并成一般世界分布上的 p-value。

## 3. 实验结束后仍要完成什么

这些工作不增加科学实验数量，但都是 arXiv 发布门禁：

1. 对 20/20 cells 运行 attempt-selection、identity pairing、resource、provider、trajectory、
   exact-replay 和 censoring 的 fail-closed 终态审计。
2. 生成终态 G2 文件哈希索引与 compact replay subset。
3. 把通过审计的 v0.5 数据一次性写入 derived JSON，冻结新 hash，并重生成全部 CSV、
   Tables 1--4、Figures 1--6 和 figure manifest。
4. 根据冻结 audit 在 Section 7 的三个预注册解释分支中选择一个，并补摘要结果句；不得依据
   叙事偏好选分支。
5. 完成统计语言、claim boundary、参考文献格式和逐数字一致性审计。
6. 运行完整测试、clean-wheel 安装、终态 replay 和独立 checkout 重建。
7. 为约 17.7 GB 的 G0 原始根目录取得持久外部 archive identifier。仓库已有 1,441 文件、
   17,725,724,603 bytes 的逐文件 SHA-256 索引，但不能伪造外部归档标识。

## 4. 当前真正的阻塞关系

```text
11 cells terminalize
        |
        v
terminal G2 audit -> frozen derived data -> Figure 5 / Table 4 -> Section 7 / Abstract
        |                    |                         |
        +--------------------+-------------------------+
                             v
              final evidence + replay + release checks
                             |
                             v
                         arXiv package

external G0 archive identifier ------------------------^
```

截至本快照，没有理由新增实验矩阵或暂停修改科学设计。第一版的内部关键路径只剩既定 G2
终态化和随后的冻结流水线；外部关键路径只剩 G0 原始数据的持久归档标识。
