# Work II A-S：纵向机制到动作 matched-candidate 支线收束

## 1. 结论先行

严格的 partition exponent → action 支线在 provider 前终止。三次冻结资格尝试都完整保留，分别完成
`640/640`、`80/80`、`80/80` 条 provider-free truth；全部 exact replay，最大误差为 0，且始终没有
provider 调用。最强的修正版仍只有 `2/20` 个 contrast×world 单元通过，5 个 construction worlds 的整套
roster 均失败。

因此，当前 partition 任务无法提供一套跨 world 稳定、主要由指数 `1.0` 对 `1.75` 决定排序的 8 动作候选。
继续建立第四版近似 crossover 只会形成候选微调—资格失败—再微调的循环，不会增加可解释的科学证据。

W2-43 仍然有效：它证明了“同一 agent 自主做完 12 轮实验后，再对新动作排序”的真实纵向流程能够运行；
但它测的是多维总体科研决策，不是“准确机制认识是否因果地导出正确动作”。

## 2. 三次资格尝试分别回答了什么

| Work package | 冻结问题 | Provider-free 结果 | 处置 |
|---|---|---|---|
| W2-44 | 旧固定过程 64-action 网格中，能否找到 4 组跨 5 worlds 稳定的指数反转对 | `640/640` truth 与 replay；仅 1 组合格 contrast，要求为 4 组 | 科学拒绝；不放宽门槛 |
| W2-45 | 用解析 crossover 公式直接构造 4 组反转对 | `80/80` truth 与 replay；4 组均未跨 5 worlds 稳定通过 | 设计否定；发现公式遗漏固定 solvent volume |
| W2-46 | 修正总 organic volume，并用 common random numbers 去掉 query-specific 噪声 | `80/80` truth 与 replay；仅 `2/20` contrast×world 通过，`0/5` world rosters 通过 | 终态科学负结果；停止同类构造 |

W2-45 的问题不是 runtime 执行了错误物理。runtime truth 是正确的；错误发生在候选设计者用来“预平衡”
动作的简化公式。因此 W2-45 可以否定该解析 roster，却不能单独否定更广义的 matched-action 可行性。
W2-46 修正了这个前提，因而是对当前 partition 支线最有判别力的结果。

## 3. 为什么修正后仍然失败

解析构造隐含地把动作效用近似成单一项 `K^p × V`，希望在中间指数处配平体积，让 `p=1.0` 与
`p=1.75` 分别偏好 contrast 的不同一侧。实际 runtime 排序不是这个单项函数：

- product 与 impurity 各有 pair-specific partition coefficient，二者都进入 exponent transform；
- coefficient 还与温度、混合效率和 world-specific multipliers 共同进入非线性 extraction；
- 有限相体积、相稳定性、stage efficiency 与 entrainment 会改变最终 organic/aqueous allocation；
- composite score 同时奖励 `product_in_organic`，惩罚 `product_in_aqueous` 和 `phase_ratio`，并非只读
  product partition term；
- 饱和与 world nuisance 会把理想公式中的微小 crossover gap 压缩、翻转或改由其他评分项主导。

W2-46 的 common-random-number truth 已经消除了候选 ID 带来的独立观测噪声，但结构性不稳定仍然存在。
这说明失败源不是“随机噪声太大”，而是当前效用函数本身不允许一个统一指数跨 5 worlds 稳定控制候选排序。

## 4. 控制与事故处置

| 控制或事件 | Class / impact | 证据 | 决定 |
|---|---|---|---|
| W2-44 资格失败 | S：真实设计负结果 | 仅 1/4 所需 contrasts | 保留，不重跑 |
| W2-45 解析前提错误 | S：候选设计否定；无 participant 污染 | truth 正确执行，provider 0 | 保留并由 W2-46 做最小修正检验 |
| W2-46 修正版失败 | S：真实科学/设计负结果 | `2/20` contrast×world、`0/5` rosters | 终态，不再造同类 W2-47 |
| tolerance-zero exact replay | K1：执行与解释完整性 | `800/800` receipts verified | 保留在 truth 边界 |
| provider-before-gate stop | K0/K1：资源与科学边界 | 三块 provider calls 均为 0 | 保留 |
| 继续增加近似 crossover gates | K4 风险 | 三次连续失败已定位结构原因 | 拒绝同类新增 |

最小受影响单元只是这条“严格 exponent-sensitive partition roster”设计支线。W2-43 的三条纵向 participant
轨迹、排序和结论未被这些资格失败污染；没有 downstream provider decision 消费失败 roster。

Launch decision：`terminal_outcome`。

## 5. 当前证据边界与真正有价值的下一步

当前可以保留三层结论：

1. W2-43：真实 12 轮纵向 action-ranking canary 可运行，且暴露出学习策略、局部外推与 transfer mismatch；
2. W2-44–46：在当前 partition runtime 与 composite score 下，无法构造跨 world 稳定的单指数 matched roster；
3. 因而不能把 W2-43 的排序差异归因于 exponent recovery，也不应把 W2-44–46 包装成 agent 能力失败。

后续只有两个科学上不同的方向：

- **总体科研决策**：沿 W2-43 扩大多个世界，保留真实多维动作，只评估排序、regret 与选择理由；
- **机制到动作因果链**：更换或新建一个 action utility 由目标机制直接控制的任务/评分函数，重新从 Q0/Q1
  资格化，而不是继续微调当前 partition 候选。

两者必须作为不同 estimand。前者回答“实验后能否做出更好决策”，后者回答“机制认识是否导致正确动作”。
