# Work II evidence-to-action large-grid v1.0 平台缺陷收口

状态：**PLATFORM-DEFECTIVE PARTIAL / 无科学结果**
日期：2026-08-24

首次 `320-grid` construction screen 的第一个单元完成 `320/320` grid truth/replay 与
`16/16` registered truth/replay。拟合与蒸馏本身成功，candidate design rank 为 `8`，蒸馏最大
绝对误差为 `3.20e-14`；但 typed-law validator 要求 `evidence_ids` 最多 `128` 项，而旧 artifact
builder 将全部 `320` 个 fit IDs 同时写入 reader-facing law summary，导致 law 被判无效。评分器
随后报告的 `rho=0` 是无效 law 的保护值，不是八候选排序的科学测量。

发现缺陷时第二个单元已有 `160/320` grid truth/replay 完成，未运行 registered truth、未生成
oracle artifact。该次运行合计保留 `496/496` truth/replay，provider calls 为 `0`；五个后续单元
未启动，prospective qualification seeds 和 formal reserved seeds 均未触碰。

修复后，artifact 顶层 `fit_query_ids` 继续保存全部拟合 provenance，typed law 的 `evidence_ids`
则从完整拟合集合中确定性均匀选择 schema 允许的 `128` 项。该变化不读取或引入候选 outcome。
缺陷 partial 原样保留且不复用；修复后的 construction screen 必须在新 run root 从第一个单元
完整重启。

机器收口：`work-ii-evidence-to-action-large-grid-v1.0-platform-defect-closeout.json`。
