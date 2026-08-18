# Work II A-S：12 轮纵向机制到动作排序 canary

## 1. 本次实际测试的问题

本 block 测试的不是旧 B4 两轮固定证据接口，而是以下完整纵向流程：

1. 同一个持久 agent session 自主完成 12 个物理实验；
2. 在 `0/3/6/9/12` 个实验后提交机制 checkpoint；
3. 第 12 轮 final checkpoint 提交前，8 个候选动作不可见；
4. final checkpoint 提交后才揭示候选；
5. agent 不填写 `8 × 4` 数值预测表，只完整排序 8 个候选并选择第一名。

三个 initial-model arms 各运行一次：

- `opaque`：不给目标机制先验；
- `aligned_nominal`：给出正确的非线性 power-response 机制族及指数 1.75；
- `misindexed_nominal`：给出错误的 linear-response 先验。

这是一个已暴露世界上的 development canary，只用于检查真实纵向流程和观察行为，不支持 arm-level 或论文级统计结论。W2-41/W2-42 的固定上下文、零物理实验结果不能替代本 block。

## 2. 执行与恢复说明

- 计划并保留：`3/3` sessions、`36/36` participant experiments。
- 每个 session：`12/12` 实验、`5/5` checkpoints、单一持久 thread。
- terminal：`3/3` 调用 `terminal_action_readout`，`3/3` 提交 final recommendation。
- 候选碰撞：`0/8` per session；没有候选曾在前 12 轮被精确执行。
- ranking-only 数值预测项：`0`。
- provider/platform failure：`0`。
- 修复后的合格结果：`3/3` completed and uncontaminated。

初次派生结果曾错误显示 `0/3` 合格。原因不是实验失败，而是旧 qualification 分支仍要求 `candidate_predictions` 非空；ranking-only contract 明确禁止该字段。现已按 contract 修复并只重算已有记录，没有重新调用 provider，也没有替换任何轨迹。

## 3. 八个候选到底是什么关系

候选同时改变 solvent、extractant、两个体积变量以及混合/静置条件。它们不是只沿一个机制轴变化的 matched pair，因此不能只凭“知道指数 1.75”直接得到排序。

| 真实名次 | query ID | solvent / extractant | aqueous / extractant volume (L) | mix / settle / rpm | true score |
|---:|---|---|---|---|---:|
| 1 | `b3-s3-e2-v2-m0` | toluene / acetonitrile | 0.028 / 0.014 | 180 / 600 / 450 | 0.728352 |
| 2 | `b3-s0-e1-v2-m1` | water / ethanol | 0.028 / 0.014 | 480 / 1500 / 950 | 0.714167 |
| 3 | `b3-s2-e2-v2-m0` | acetonitrile / acetonitrile | 0.028 / 0.014 | 180 / 600 / 450 | 0.709732 |
| 4 | `b3-s2-e0-v3-m1` | acetonitrile / water | 0.016 / 0.030 | 480 / 1500 / 950 | 0.706067 |
| 5 | `b3-s0-e3-v0-m0` | water / toluene | 0.012 / 0.018 | 180 / 600 / 450 | 0.700480 |
| 6 | `b3-s0-e3-v0-m1` | water / toluene | 0.012 / 0.018 | 480 / 1500 / 950 | 0.697201 |
| 7 | `b3-s1-e0-v1-m0` | ethanol / water | 0.020 / 0.020 | 180 / 600 / 450 | 0.690975 |
| 8 | `b3-s2-e3-v3-m1` | acetonitrile / toluene | 0.016 / 0.030 | 480 / 1500 / 950 | 0.676912 |

真实第一与第三只改变 solvent：`toluene/acetonitrile` 高于 `acetonitrile/acetonitrile`。真实第八虽然具有较大的 extractant volume 和较长处理时间，却是最低分。这两个对照直接检验 agent 是否把前 12 轮的局部经验错误外推为“matched pair 一定最好”或“extractant volume 越大一定越好”。

## 4. 三条完整排序

表中数字为 agent 排名位置；越小越靠前。

| true rank | query ID | opaque position | aligned position | misindexed position |
|---:|---|---:|---:|---:|
| 1 | `b3-s3-e2-v2-m0` | 7 | 7 | 1 |
| 2 | `b3-s0-e1-v2-m1` | 5 | 8 | 6 |
| 3 | `b3-s2-e2-v2-m0` | 8 | 1 | 2 |
| 4 | `b3-s2-e0-v3-m1` | 3 | 2 | 7 |
| 5 | `b3-s0-e3-v0-m0` | 4 | 5 | 4 |
| 6 | `b3-s0-e3-v0-m1` | 2 | 6 | 5 |
| 7 | `b3-s1-e0-v1-m0` | 6 | 4 | 8 |
| 8 | `b3-s2-e3-v3-m1` | 1 | 3 | 3 |

按 agent 输出顺序表示：

- `misindexed_nominal`：真实名次 `[1, 3, 8, 5, 6, 2, 4, 7]`；选择真实第 1 名。
- `aligned_nominal`：真实名次 `[3, 4, 8, 7, 5, 6, 1, 2]`；选择真实第 3 名。
- `opaque`：真实名次 `[8, 6, 4, 5, 2, 7, 1, 3]`；选择真实第 8 名。

| arm | selected true rank | selected score | normalized regret | selected − random-candidate mean | final-law normalized MAE |
|---|---:|---:|---:|---:|---:|
| `misindexed_nominal` | 1 | 0.728352 | 0.000000 | +0.025366 | 0.144066 |
| `aligned_nominal` | 3 | 0.709732 | 0.361971 | +0.006746 | 0.086371 |
| `opaque` | 8 | 0.676912 | 1.000000 | −0.026074 | 0.270836 |

三条 final law 的 normalized MAE 都高于预设 adequate threshold `0.05`。因此本次唯一 Top-1 成功属于 `inadequate_law__correct_action`，不能解释为“agent 已准确恢复完整 executable law”。

## 5. 每条 12 轮实验轨迹

缩写：W = water，EtOH = ethanol，ACN = acetonitrile，Tol = toluene；`Porg` 为 `product_in_organic`。

### 5.1 `aligned_nominal`

该 agent 先做 solvent 小扫描，随后迅速集中到 ACN/ACN，并优化 phase balance，最后重复局部最优点。

| round | solvent / extractant | phase setting | extractant vol. | process | Porg | score |
|---:|---|---|---:|---|---:|---:|
| 1 | ACN / Tol | aqueous 0.020 | 0.020 | 120 s, 500 rpm, settle 300 s | 0.550 | 0.369 |
| 2 | Tol / Tol | aqueous 0.020 | 0.020 | 同上 | 0.544 | 0.363 |
| 3 | W / Tol | aqueous 0.020 | 0.020 | 同上 | 0.528 | 0.349 |
| 4 | EtOH / Tol | aqueous 0.020 | 0.020 | 同上 | 0.536 | 0.355 |
| 5 | ACN / ACN | aqueous 0.020 | 0.020 | 同上 | 0.707 | 0.500 |
| 6 | EtOH / EtOH | aqueous 0.020 | 0.020 | 同上 | 0.427 | 0.263 |
| 7 | ACN / ACN | aqueous 0.010 | 0.030 | 同上 | 0.900 | 0.666 |
| 8 | ACN / ACN | aqueous 0.005 | 0.040 | 同上 | 0.955 | 0.711 |
| 9 | ACN / ACN | aqueous 0.003 | 0.050 | 同上 | 1.000 | 0.751 |
| 10 | ACN / ACN | aqueous 0.003 | 0.050 | 240 s, 900 rpm, settle 300 s | 0.998 | 0.750 |
| 11 | ACN / ACN | aqueous 0.003 | 0.050 | 120 s, 500 rpm, settle 300 s | 1.000 | 0.752 |
| 12 | ACN / ACN | aqueous 0.003 | 0.050 | 同上 | 0.986 | 0.738 |

机制 checkpoint 演化：

- 0 轮：接受 power-response / exponent 1.75 先验。
- 3 轮：认为 solvent 只有小效应。
- 6 轮：发现 ACN/ACN 特异交互，放弃“所有 matched pair 都好”。
- 9 轮：把 ACN/ACN 与极端 organic-favored volume balance 认定为两个主导杠杆。
- 12 轮：形成高度局部化的 ACN/ACN 最优定律，并准备选择最接近该局部最优的候选。

失败点不是没有学习，而是学习得过于局部：它把 ACN/ACN 的极端体积优化结果外推到候选区，最终把 ACN/ACN 排第一；但候选都不具备其 0.003/0.050 L 的局部最优体积，真实世界在共同候选条件下反而由 Tol/ACN 更优。

### 5.2 `misindexed_nominal`

该 agent 没有追随错误 linear prior 做单点优化，而是近似完成 solvent × extractant 的广覆盖扫描。

| round | solvent / extractant | phase setting | process | Porg | score |
|---:|---|---|---|---:|---:|
| 1 | Tol / EtOH | aqueous+organic 0.014/0.014, ext 0.010 | 120 s, 600 rpm, settle 300 s | 0.543 | 0.363 |
| 2 | Tol / ACN | aqueous+organic 0.013/0.013, ext 0.010 | 150 s, 700 rpm, settle 240 s | 0.823 | 0.600 |
| 3 | Tol / Tol | 同体积 | 180 s, 800 rpm, settle 360 s | 0.661 | 0.462 |
| 4 | Tol / W | 同体积 | 120 s, 600 rpm, settle 300 s | 0.245 | 0.107 |
| 5 | ACN / ACN | 同体积 | 150 s, 700 rpm, settle 240 s | 0.815 | 0.592 |
| 6 | ACN / Tol | 同体积 | 180 s, 800 rpm, settle 300 s | 0.664 | 0.464 |
| 7 | EtOH / ACN | 同体积 | 120 s, 600 rpm, settle 300 s | 0.803 | 0.583 |
| 8 | EtOH / Tol | 同体积 | 150 s, 700 rpm, settle 240 s | 0.631 | 0.436 |
| 9 | W / ACN | 同体积 | 120 s, 600 rpm, settle 300 s | 0.802 | 0.582 |
| 10 | W / Tol | 同体积 | 150 s, 700 rpm, settle 240 s | 0.649 | 0.453 |
| 11 | ACN / EtOH | 同体积 | 180 s, 800 rpm, settle 300 s | 0.560 | 0.378 |
| 12 | EtOH / EtOH | 同体积 | 120 s, 600 rpm, settle 300 s | 0.511 | 0.334 |

机制 checkpoint 演化：

- 0 轮：持有错误 linear-response 先验。
- 3 轮：发现固定 Tol solvent 下 extractant identity 强烈改变 Porg。
- 6 轮：在 Tol 与 ACN 两种 solvent 上确认 ACN extractant 最高、Tol 次之、EtOH 和 W 更低。
- 9 轮：形成“extractant 主导、solvent 小修正”的加性经验定律。
- 12 轮：完成较宽的离散组合覆盖，并直接用该经验排序候选。

它正确选择 Tol/ACN，不是因为恢复了指数 1.75，而是因为第 2 轮已经在接近候选结构的区域直接观察到 Tol/ACN 高于 ACN/ACN，并用广覆盖离散比较保留了这个次序。

### 5.3 `opaque`

该 agent 从零探索后发现“加入 organic phase + Tol extractant”在自己的轨迹中表现很好，并围绕该区域做 volume、solvent、reagent-load 与 phase-volume 检查。

| round | solvent / extractant | phase setting | extractant vol. | extra change | Porg | score |
|---:|---|---|---:|---|---:|---:|
| 1 | Tol / EtOH | aqueous 0.020 | 0.002 | — | 0.097 | 0.000 |
| 2 | ACN / Tol | organic 0.020 | 0.004 | longer mix | 0.734 | 0.525 |
| 3 | ACN / Tol | aqueous 0.020 | 0.004 | — | 0.208 | 0.076 |
| 4 | ACN / EtOH | organic 0.020 | 0.004 | — | 0.582 | 0.393 |
| 5 | ACN / Tol | organic 0.020 | 0.002 | — | 0.674 | 0.472 |
| 6 | ACN / Tol | organic 0.020 | 0.008 | — | 0.746 | 0.534 |
| 7 | EtOH / Tol | organic 0.020 | 0.004 | — | 0.710 | 0.505 |
| 8 | W / Tol | organic 0.020 | 0.004 | — | 0.682 | 0.479 |
| 9 | Tol / Tol | organic 0.020 | 0.004 | — | 0.710 | 0.504 |
| 10 | ACN / Tol | organic 0.020 | 0.008 | reagent 0.020 mol | 0.373 | 0.219 |
| 11 | ACN / Tol | organic 0.010 | 0.008 | — | 0.612 | 0.422 |
| 12 | ACN / Tol | organic 0.020 | 0.012 | — | 0.777 | 0.560 |

机制 checkpoint 演化：

- 0 轮：无名义机制。
- 3 轮：认为 ACN solvent、organic phase 与 Tol extractant 共同有利。
- 6 轮：确认 phase type 是巨大杠杆，Tol extractant volume 上升有利。
- 9 轮：认为 solvent 次要，organic phase + Tol extractant 是主要规律。
- 12 轮：继续外推“ACN/Tol + 大 extractant volume”并选择对应候选。

它选择真实第 8 名的核心原因是 transfer mismatch：前 12 轮最强信号来自 `organic` phase addition，而 terminal candidate 特征并没有让它复用这一离散操作；它随后用 ACN/Tol、较大 extractant volume 和较长处理时间做代理，正好把真实最低候选排到了第一。

## 6. 当前能得到的结论

1. 真正的 12 轮纵向接口已经可运行；候选隐藏、final checkpoint gate、same-thread 和 ranking-only 提交均成功。
2. 12 轮实验确实改变了 agent 的动作判断，但“形成某种机制叙述”不等于“能在新候选上正确排序”。
3. 本 world 中，广覆盖的离散比较比围绕正确机制先验做局部最优化更有利于 terminal ranking。
4. 正确 Top-1 与准确 executable law 在本样本中分离：唯一 Top-1 arm 的 final-law MAE 仍不合格。
5. 当前候选 packet 同时改变太多维度，并包含前 12 轮可能学到但 terminal 中不可复用的操作轴。它适合做困难的总体 action-selection canary，但不适合单独归因“机制认识是否导致正确动作”。

下一步不应继续回到 W2-41/W2-42 的固定上下文重复。若要扩大样本，应先决定主问题：

- 若测总体科研决策能力：保留多维候选，但增加多个世界和 session，只评价排序/选择；
- 若测机制到动作的因果链：重做 matched candidates，让候选主要沿目标机制轴变化，并把 phase-type 等不可转移轴固定；
- 两者可以并列，但必须作为两个 estimand 分开报告。
