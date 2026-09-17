# Experiment 1 EC-W00/W01–W05 qualification v1.0.1

状态：**在任何新数据产生前冻结；development-only；provider-free。**

## 问题

在同一组五个真实电化学 Worlds 上，实体、参数和结构三类先验干预是否分别满足
[`Experiment 1 最小执行规范 v1.0.1`](EXPERIMENT_1_MINIMUM_EXECUTION_SPEC_V1_0_1.md) 的八个共同硬门，
从而允许 EC-E、EC-P、EC-S 进入后续 Participant development？

## 单位、覆盖与顺序

- `EC-W00`，seed `900000`：只验证配置、公共合同、一次物理执行、记录、hash 和 tolerance-zero replay；不计科学分母。
- `EC-W01..EC-W05`，seeds `0..4`：每个 World 分别运行 `entity / parametric / structural`。
- 科学分母固定为 15 个 `world × locus` 原子单元。一个 locus 需要 5/5 Worlds 全部通过才是
  `five_world_qualified`。
- W00 工程失败立即停止。W1–W5 开始后不得改变 seed、交换规则、查询网格、阈值、预算或噪声重复。
- 不调用模型 provider，不读取历史 Participant 表现，不启动正式 Participant。

## 测量与冻结判定

- 共同 Q1–Q8、EC-E/EC-P/EC-S 的具体阈值和 Participant 反证预算全部以 v1.0.1 规范及机器合同为准。
- qualification 网格与噪声重复不计入 Participant 的实验预算；Q6 单独证明预算内存在合法反证路径。
- 每个物理执行必须被分类并 tolerance-zero exact replay；平台错误与物理/科学失败分开记账。
- prior schema/leakage audit 在不读取 Participant 结果的情况下完成。
- behavioral relevance 使用预注册、provider-free 的有限决策对照；不得以“看起来会影响 Agent”代替机器判定。

## 失败与修复

- 平台缺陷：保留失败 attempt，修复后从受影响 qualification block 的第一个单位重跑。
- 科学 Gate 失败：完成固定分母并登记 `failed`；可以进入下一轮 world/prior redesign，但不能降低阈值或覆盖原结果。
- 某一 World 失败会使对应 `system × locus` 不能称为 five-world qualified；其他 locus 的结果仍独立报告。
- 不允许把历史 qualification PASS 拼接成 v1.0.1 PASS；历史资产只用于实现复用和差异核对。

## 预期输出

- 一个不可覆盖的 development attempt 目录，含 W00、三类 qualification 的 raw receipts/trajectories；
- 一个 15-row machine registry、一个机器摘要和一个可读 Markdown 摘要；
- 每个 World 的 realized truth digest、prior digest、evidence bundle hash、精确分母与全部失败；
- 最终决定只能是各 locus 的 `five_world_qualified / failed / pending` 以及 EC 是否可进入 Participant development。
