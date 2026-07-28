# S0 电化学不透明材料 20×5：结果分析与 Codex 订阅迁移

## 1. 结论

WellAU `gpt-5.6-sol` medium 的 5-seed development 矩阵已经完整结束：

- seeds `0–4`；
- `100/100` 次探索实验；
- `5/5` 次最终综合；
- `20/20` 次配对盲验证；
- `120` 次物理实验；
- 五份独立回放全部 `all_verified=true`；
- 5-seed 聚合审计 `all_runs_completed=true`、`all_audits_passed=true`。

主要结果不是“模型已经学会充分探索材料”，而是：

1. 在已知总 horizon 为 20 的轨迹中，所有 seed 的最好分都出现在第 9–20 轮；
2. 后 12 轮相对前 8 轮 best 的平均增益为 `0.066449`；
3. 但模型高度偏向 exploitation：`80/100` 次实验落在最终推荐材料 pair 上；
4. 每个世界平均只覆盖 `3.2/16` 个材料 pair；
5. seed 2 完全没有切换材料，seed 3 到第 11 轮才首次切换；
6. 只有 seeds 1 和 3 做了能部分拆分 electrolyte 与 solvent 效应的单因素材料对照；
7. 最终综合没有稳定超越已观察 incumbent，平均盲验证增益仅
   `+0.000022`。

因此，20 轮改善了连续参数优化和部分迟发材料发现，但没有稳定解决不透明材料代码下的
类别探索问题。

## 2. 单 seed 结果

| Seed | 探索 best | 1–8 轮 best | 9–20 轮 best | best 轮次 | 盲验证推荐分 | 推荐相对 incumbent | pair 数 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0.834835 | 0.778826 | 0.834835 | 18 | 0.826999 | 0 | 2 |
| 1 | 0.777480 | 0.774326 | 0.777480 | 12 | 0.770732 | +0.000269 | 5 |
| 2 | 0.769242 | 0.661187 | 0.769242 | 20 | 0.764377 | 0 | 1 |
| 3 | 0.827198 | 0.692693 | 0.827198 | 11 | 0.826195 | 0 | 4 |
| 4 | 0.684988 | 0.654467 | 0.684988 | 17 | 0.679937 | −0.000158 | 4 |

跨 seed 描述统计：

- 盲验证推荐分均值：`0.773648`；
- 跨 seed 样本标准差：`0.060174`；
- 标准误：`0.026911`；
- 描述性 t 区间：`[0.698932, 0.848364]`；
- 探索 best 均值：`0.778749`；
- best-so-far AUC 均值：`0.703895`；
- 盲验证分范围：`0.679937–0.826999`。

该区间只描述 5 个 development worlds 的离散程度，不是正式 benchmark 推断。

## 3. Horizon 行为

五个 seed 的全局 best 均发生在第 9–20 轮：

| Seed | 前 8 轮 best | 最终 best | 后续增益 |
|---:|---:|---:|---:|
| 0 | 0.778826 | 0.834835 | +0.056009 |
| 1 | 0.774326 | 0.777480 | +0.003155 |
| 2 | 0.661187 | 0.769242 | +0.108054 |
| 3 | 0.692693 | 0.827198 | +0.134505 |
| 4 | 0.654467 | 0.684988 | +0.030521 |

平均增益为 `0.066449`，中位数为 `0.056009`。其中：

- seed 1 在第 8 轮已经基本收敛，后 12 轮只增加 `0.003155`；
- seed 2 的材料类别没有变化，但连续参数优化直到第 20 轮仍明显改善；
- seed 3 的主要增益来自第 11 轮材料切换，而不是在旧材料 pair 内继续微调。

这证明“这五条已知 20 轮轨迹在第 8 轮尚未全部完成优化”，但不能证明独立的 20-round
protocol 因果优于 8-round protocol。模型从一开始就知道总预算为 20，探索节奏会受终点影响；
若要回答 horizon 因果问题，需要冻结方法后比较 `8/12/16/20` 或在统一最大预算下读取固定
checkpoints。

## 4. 材料 pair 搜索

### Seed 0

- 轨迹：`E0-S0` 1 次，随后 `E1-S1` 连续 19 次；
- 相邻材料切换：1 次；
- 推荐 pair：`E1-S1`；
- 推荐配方首次出现且取得 best：第 18 轮。

模型很快找到高分 pair，但 `E0-S0 → E1-S1` 同时改变两种材料，无法区分收益来自
electrolyte、solvent 还是交互效应。后续没有类别证伪。

### Seed 1

- `E1-S1` 使用 16 次；
- 另测 `E0-S0`、`E2-S2`、`E3-S1`、`E1-S3`；
- 相邻材料切换：6 次；
- 推荐 pair：`E1-S1`。

该 seed 的材料证据最完整。`E3-S1` 和 `E1-S3` 分别提供 electrolyte-only 和
solvent-only 的局部反事实，且分数明显低于 `E1-S1`。最终综合没有选择一次性最高分的第 12
轮配方，而选择了在第 8、17 轮重复测试过的配方；盲验证相对 incumbent 为
`+0.000269`，体现了轻微的稳健性收益。

### Seed 2

- 20 轮全部为 `E1-S1`；
- 相邻材料切换：0；
- 推荐 pair：`E1-S1`；
- best 出现在第 20 轮。

这是最明确的类别探索失败。较高的最终分只能说明连续控制优化有效，不能说明 agent 识别了
材料类别；它没有收集任何材料对照证据。

### Seed 3

- 前 10 轮全部为 `E1-S1`，该 pair best 为 `0.7279`；
- 第 11 轮切到 `E2-S1`，立即达到 `0.827198`；
- 后续测试 `E2-S2` 与 `E3-S1`；
- 推荐 pair：`E2-S1`。

这是延长 horizon 最有价值的 seed。若只读前 8 轮，会错过约 `0.1345` 的最终 best 增益。
后续的 `E2-S2` 和 `E3-S1` 还提供了局部单因素材料证据。

### Seed 4

- 前四轮依次为 `E0-S0`、`E1-S1`、`E2-S2`、`E3-S3`；
- 随后 16 轮中的 16 轮均回到 `E2-S2`；
- 推荐 pair：`E2-S2`。

它覆盖了四个 pair，但全部沿对角线同时改变 electrolyte 和 solvent，不能识别单个类别变量
或交互项。类别覆盖数高于 seed 0/2，但科学可解释性仍弱。

### 汇总

- 16 个允许 pair 中，每个 seed 平均覆盖 `3.2` 个；
- 100 次探索中有 80 次位于最终推荐 pair；
- 95 个相邻轮次转移中仅 15 次改变材料 pair；
- 4/5 seeds 至少切换一次，1/5 完全不切换；
- 只有 2/5 seeds 形成了部分正交材料对照。

当前 scaffold 更像“快速选一个 pair 后做连续局部优化”，而不是显式预算化的
categorical-then-continuous 搜索。

## 5. 连续控制与推荐

五个最终推荐均为实际测试过的配方：

| Seed | Pair | V | mA | 时间 s | 物料 mol | 推荐配方出现轮次 |
|---:|---|---:|---:|---:|---:|---|
| 0 | E1-S1 | 1.45 | 185 | 3600 | 0.004625 | 18 |
| 1 | E1-S1 | 1.30 | 100 | 3600 | 0.003000 | 8、17 |
| 2 | E1-S1 | 1.30 | 150 | 3600 | 0.006000 | 16、20 |
| 3 | E2-S1 | 1.30 | 155 | 3600 | 0.003900 | 11、19、20 |
| 4 | E2-S2 | 1.50 | 220 | 3600 | 0.006000 | 12、16 |

共同模式：

- 五个推荐全部使用上界 `3600 s`；
- 100 次探索中有 79 次使用 `3600 s`；
- 推荐电位范围 `1.30–1.50 V`；
- 推荐电流范围 `100–220 mA`；
- 推荐物料量范围 `0.003–0.006 mol`。

这说明 agent 很快把时间推到上界，再针对材料世界调整电流、物料量与电位。由于 primary
reward 没有直接惩罚实验时长，不能把 `3600 s` 的集中解释为已证明的通用电化学机制；它也
可能是目标合同诱导出的边界解。

## 6. 最终综合与盲验证

探索 best 与盲验证推荐分的差值分别为：

- seed 0：`0.007836`；
- seed 1：`0.006749`；
- seed 2：`0.004865`；
- seed 3：`0.001003`；
- seed 4：`0.005050`。

平均乐观偏差仅 `0.005101`，说明最终提交配方在独立观测噪声下总体稳定。另一方面：

- 3 个 seeds 的 recommendation 与 incumbent 完全相同；
- seed 1 只提高 `0.000269`；
- seed 4 只降低 `0.000158`；
- 跨 seed 平均增益为 `+0.000022`。

因此 final synthesis 的价值主要是选择和提交一个可复现的 tested recipe，而不是从 20 轮历史
中构造出显著优于 incumbent 的新配方。当前结果不支持“最终综合本身提高优化分数”的结论。

## 7. 测量、安全与资源

测量行为：

- 100/100 次探索均请求 `pH meter + UV-vis` 两个诊断槽；
- 当前协议没有 measurement hard cap，因此未观察到测量资源取舍；
- 若未来要评价 active measurement selection，需要单独冻结成本或槽位预算。

安全：

- 五个 seeds 的最高 `peak_safety_risk` 为 `0.137057`；
- 协议阈值为 `0.65`；
- 所有实验都处在较宽安全余量内。

WellAU 资源：

- 106 个逻辑 provider calls；
- 132 个 provider attempts；
- `1,002,667` prompt tokens；
- `90,635` completion tokens；
- 合计 `1,093,302` tokens；
- seed 0 的首次运行在最终综合处遇到 provider `502`，随后通过新目录 continuation 完成；
- WellAU 没有冻结可核实定价，因此美元成本保持未知。

## 8. 机制声明边界

每个 seed 的最终综合都提交了 structured claims，但当前协议明确：

- declared claim scoring 关闭；
- predictive validation 关闭；
- 没有针对 seeds 0–4 的冻结 material-family reference。

因此这些机制声明只能作为可审计的 working hypotheses，不能与优化分数一起解释为机制正确性
证据。尤其 seeds 0、2、4 的材料设计不足以支持对 electrolyte 与 solvent 的独立因果归因。

## 9. 切换到 Codex 订阅

已新增独立 provider：`codex_subscription`。

运行合同：

- 通过本机 `codex exec` 使用缓存的 ChatGPT 登录；
- 强制验证 `codex login status` 为 `Logged in using ChatGPT`；
- 模型 `gpt-5.6-sol`；
- reasoning effort `medium`；
- `ephemeral` session；
- 忽略用户 config 与仓库 rules；
- 禁用 shell、apps、multi-agent 和 plugins；
- system prompt 写入临时 `model_instructions_file`，替换 Codex 编码代理默认指令；
- 从 `required_json_shape` 生成严格 JSON Schema；
- 解析 JSONL `turn.completed` usage；
- ChatGPT 订阅无法按单次请求归因美元价格，因此 `accounting_complete=false`。

本机状态：

- Codex CLI 已从 `0.142.4` 升级到 `0.145.0`；
- ChatGPT 订阅登录有效；
- 模型目录识别 `gpt-5.6-sol`；
- 外部结构化 smoke call 成功；
- 当前网络会先发生 WebSocket timeout，再回退 HTTPS，单次 smoke 增加约 90 秒延迟；
- v0.7.1 最终方法哈希已完成 5-seed local mock 和聚合回放：
  `100` 次探索、`20` 次验证、所有审计通过。

历史 WellAU v0.7 协议与方法配置保持不变，用于重放已有结果。新的后续入口是：

- `configs/benchmark/scientific_optimization_s0_v0.7.1_material_opaque_codex_subscription_20x5_dev.json`
- `configs/methods/llm_v0.4/participant_methods_s0_codex_subscription_sol_material_opaque_20x5_v071.json`

尚未启动新的 Codex subscription 真实 5-seed 矩阵；目前只完成迁移、结构化 smoke 和本地
5-seed 资格验证。

## 10. 下一步建议

按证据优先级排序：

1. 先做 1 个 Codex subscription seed 的真实端到端 pilot，并审计 CLI JSONL usage、
   timeout 和 resume；
2. 在同一 seed、同一 observation namespace 下，把 Codex subscription 与 WellAU 结果视为
   两个独立 transport/method cells，不假设相同 model slug 等于相同服务实现；
3. 若继续研究材料发现，在 scaffold 中冻结最小类别探索合同，例如前 6–8 轮覆盖若干正交
   electrolyte/solvent 对照；
4. 再比较 constrained categorical exploration 与自由 LLM 策略，而不是直接修改本轮历史；
5. 若研究 horizon，使用统一最大预算并在 8/12/16/20 checkpoints 读取 incumbent。
