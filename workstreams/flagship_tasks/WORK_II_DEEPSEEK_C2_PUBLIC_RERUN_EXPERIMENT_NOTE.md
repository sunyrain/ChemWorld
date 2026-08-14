# Work II DeepSeek C2 corrected-semantics public rerun experiment note

## Question

在同一 DeepSeek `deepseek-v4-flash` participant 下，修正模型可见动作边界、quench 语义以及
partition、crystallization、distillation 的连续物理转移后，opaque、aligned-nominal 和
misindexed-nominal 三种初始世界模型是否改变规律恢复、实验决策、失败方式和最终推荐？

旧 public v0.1 的全部终态作为历史结果保留；本轮不续跑、不补齐、不与旧结果拼接，从首个
scheduled cell 建立独立 cohort。

## Fixed coverage

- A-E public：5 tasks × 5 fresh worlds × 3 arms = 75 sessions；每 session 8 个完整实验，共 600。
- A-P：2 tasks × 5 fresh worlds × 3 arms = 30 sessions；每 session 10 个完整实验，共 300。
- A-S：2 tasks × 5 fresh worlds × 3 arms = 30 sessions；每 session 12 个完整实验，共 360。
- public 合计：45 task/world triplets、135 sessions、1,260 complete experiments。
- 三臂在同一 task/world 内共享世界和 keyed observation noise；每个 cell 是一个持久 provider
  session，participant 自主选择合法实验操作。

## Frozen execution semantics

- 动作 schema 的 duration 和资源参数边界来自当前 batch、apparatus 和操作状态；host 仅做合法性、
  安全性和资源记账，不替 participant 选择动作。
- partition、crystallization 和 distillation 保持跨操作的物料、相态和设备连续性；合法的救援、
  重处理或后续 assay/filter 路径由当前物理状态决定。
- quench 是改变反应与热状态的化学操作，不被解释为通用 closeout，也不凭空销毁物料。
- provider token 逐回执计数一次；cache hit、cache miss 和 output 分开记录。资源上限为 report-only，
  不作为在线停止条件。

## Measurements and analysis boundary

- 所有 locus：belief snapshots、held-out prediction error、证据引用、完整实验数、最终推荐、
  blind validation、operation/tool/provider 使用量、全部失败、right-censoring 和 exact replay。
- A-E 主分析为 task-stratified dossier-assignment ITT；仅 partition-extractant 作为预先限定的
  identifiable-locus strong-signal analysis，其余任务保留为 weak-identifiability boundary/stress
  evidence。不得因 outcome 删除 task、world 或 arm。
- A-P 另外报告 optimum-ridge distance、turnover detection、局部梯度与交互误差。
- A-S 另外报告机制模块识别、干预后果预测与结构恢复误差。

## Terminal, failure, and stop rules

- 每个 scheduled cell 保留 completed、right-censored 或 failed 终态；科学/participant 失败不替换。
- 只有同一 triplet 三臂均在首个 committed operation 前遇到同一基础设施故障，才暂停后续 triplet；
  修复后只恢复缺失基础设施 cell，不覆盖已存在轨迹。
- 物理安全、固定轮数、checkpoint、样品/库存和 closeout 规则保持不变；运行中不按结果修改设计。
- 至少每 30 秒记录进度；终态 summary 给出精确分母、全部终态、失败和资源账本。

## Expected outputs

- 独立输出根目录中的 execution plan、逐 cell trajectory/summary、terminal store、progress 和 public
  汇总；原始 provider payload 保持在 ignored run directory，不进入 Git。
- public 终态后生成不含 crystallization 的即时汇报图，同时保留完整机器分析；A-E private 继续延期，
  除非用户另行授权。
- 本说明和 `configs/benchmark/work_ii_deepseek_c2_prospective_v0.2.json` 固定本轮设计；不创建额外
  readiness、SHA inventory 或 release-audit 包。
