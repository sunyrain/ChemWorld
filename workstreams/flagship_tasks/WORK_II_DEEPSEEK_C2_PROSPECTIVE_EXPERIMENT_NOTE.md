# Work II DeepSeek C2 prospective experiment note

## Question

在同一 DeepSeek `deepseek-v4-flash` participant 与 ChemWorld MCP 执行语义下，比较 opaque、
aligned-nominal、misindexed-nominal 三种初始世界模型，检验实体层（A-E）、局部规律层（A-P）和
结构机制层（A-S）的先验是否改变规律恢复、实验决策和最终推荐。

## Fixed coverage

- A-E public：5 tasks × 5 fresh worlds × 3 arms = 75 sessions；每 session 8 个完整实验，共 600。
- A-P public：2 tasks × 5 fresh worlds × 3 arms = 30 sessions；每 session 10 个完整实验，共 300。
- A-S public：2 tasks × 5 fresh worlds × 3 arms = 30 sessions；每 session 12 个完整实验，共 360。
- A-E private：5 tasks × 5 sealed worlds × 3 arms = 75 sessions；每 session 8 个完整实验，共 600。
- 完整 C2：210 sessions，1,860 complete experiments。public C2 的 135 sessions / 1,260 experiments
  终态后，才解封并执行 private A-E。

三臂在同一 task/world 内共享世界和 keyed observation noise。每个 cell 是一个持久 provider session；
participant 自主选择实验操作，host 只负责类型校验、执行、资源记账和隐藏世界计算。

## Measurements and analysis boundary

- 所有 locus：belief snapshot、held-out prediction error、证据引用、完整实验数、最终推荐、blind validation、
  provider/session/tool/operation 使用量和全部失败。
- A-E：主要比较 misindexed 与 aligned 的 pre-to-final prediction-error change，同时报告 opaque 对照。
- A-P：另外报告 optimum-ridge distance、turnover detection、局部梯度和交互误差。
- A-S：另外报告机制模块识别、干预后果预测与结构恢复误差。
- v0.3 A-E classifier fit 与 untouched validation 各完成 `14,400/14,400` primary 及 exact replay；10 个
  candidate loci 只有 `partition-extractant` 在 60/60 worlds 上通过，整体结论为 scientifically rejected。
  因此完整五任务 A-E 的正式 estimand 预先改为 dossier assignment 对搜索、预测、belief、action 和失败的
  task-stratified ITT 效应；不得把它解释成五任务 universal selective correction。只有 partition-extractant
  可单列为 identifiable-locus strong-signal analysis，其余任务预注册为 weak-identifiability boundary/stress
  evidence。不得在看到 participant outcome 后删除任务、世界或臂。

## Terminal, failure, and stop rules

- 每个 scheduled cell 保留 completed、right-censored 或 failed 终态；科学失败和已有 trajectory 的失败不替换。
- provider token、调用、费用和 wall time 仅记录，不作为在线停止条件；物理安全、实验轮数、checkpoint、
  样品/库存和 closeout 规则保持固定。
- 只有三臂均在首个 committed operation 前遇到同一基础设施故障时，才暂停新的 world triplet；修复后只补
  缺失的基础设施 cell，不覆盖已有科学轨迹。
- 进度至少每 30 秒写入一次；机器摘要必须给出 exact denominators、全部终态和失败原因。

## Expected outputs

- 忽略目录下的原始 provider transcripts、逐 cell summaries、terminal store、public C2 progress 与终态汇总。
- public 完成后生成 task/locus-stratified analysis；随后才读取已在 public outcome 前迁移并重新承诺的
  DeepSeek C2 private seal，启动 A-E private。
- 本说明和 `configs/benchmark/work_ii_deepseek_c2_prospective_v0.1.json` 共同固定本轮设计；不再生成额外的
  readiness、SHA inventory 或 release-audit 包来阻止执行。
