# W2-47 feature-only terminal packet 诊断收束

状态：**历史 development protocol diagnostic；不作为 action-quality 或 Paper 2 证据。**

## 保留结果

- 一个 partition world，三臂各一个 persistent session；`36/36` participant experiments、`15/15`
  checkpoints、`3/3` same-thread terminal readouts 均完成。
- Provider-free checkpoint/candidate truth 与 exact replay 为 `24/24 + 24/24`；provider error、resource
  rejection、candidate overlap 均为 0。
- `aligned_nominal / opaque / misindexed_nominal` 分别选择真实第 `3 / 4 / 8` 名；normalized regret
  分别为 `0.0497 / 0.0653 / 1.0000`。
- 三臂 final-law normalized MAE 分别为 `0.3801 / 0.2101 / 0.2649`，均高于 `0.05` adequacy gate。

## 终止原因

Terminal prompt 声称揭示 fixed unseen candidate operations，但公共 packet 只包含材料、体积、混合等
feature values。Evaluator 在 host 侧补齐了未公开的完整操作序列，包括 reagent 是否存在、HPLC 位置和
次数、phase separation 与 final-assay 路径。三臂自主实验的操作拓扑又各不相同，因此 agent 并未在知晓
完整候选动作的条件下完成排序。

该缺陷不是“开放式三臂 workflow 不同”；开放式 workflow 是保留的研究对象。缺陷是 outcome-blind 被
错误实现为部分 action-semantics-blind。旧 result 只能说明流程可运行、模型会形成不同探索与解释轨迹，
不能干净衡量综合决策质量。

## 保留与后继

- 原始 records、provider receipts、truth、replay 和 machine summary 原样保留在 ignored development run
  root：`runs/development/work-ii-as-longitudinal-decision-single-world-seed153150025-v0.1/`。
- 旧 note、config、launcher、materializer 和专属 tests 已移入本归档，不得恢复为当前入口。
- 后继 W2-48 保持 participant open-action exploration；final checkpoint 后公开每个候选的完整 executable
  ActionPlan，只隐藏 outcome、rank、truth 和其他 arm evidence，并要求 public/truth/executed plan hash
  完全一致。
