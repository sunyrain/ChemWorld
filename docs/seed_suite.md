# Seed 与数据划分

Seed 决定可复现的世界实例，但 seed 变化不等同于机理族或真实分布变化。ChemWorld 将软件回归
seed、研究 cohort 和私有世界分开管理。

## 查看内置 seed plan

```bash
chemworld seeds show
chemworld seeds show --all-tasks
chemworld seeds show --tasks reaction-to-assay partition-discovery
```

输出包含 suite、task、split、公开 seed 和 private-eval policy。内置 plan 用于示例、回归和本地
一致性，不自动授权方法排名。

## 软件回归 seeds

| Task | Split | Seeds | 用途 |
| --- | --- | --- | --- |
| `reaction-to-assay` | `public-dev` | `0` | 最小合法闭环 |
| `reaction-to-purification` | `public-test` | `0–4` | 下游与 replay 回归 |
| `partition-discovery` | `public-test` | `0–4` | campaign 回归 |

六个 serious 候选任务的历史 v1 plan 也使用 `0–4`。这些 seeds 已被广泛查看和调试，应视为开发
数据，不再充当未触碰的最终确认 cohort。

## 协议特异 cohort

正式方法协议必须单独冻结 paired seeds，并记录它们是否已用于调参。2026-07 的四任务经典诊断
使用公开 seeds `20–39`；运行后发现安全/成本规则缺失，因此这组 seeds 已被消费为诊断数据。加入
新决策规则后必须换用未触碰的 cohort，不能对同一数据追补门槛再称为确认实验。

## 三类泛化证据

| 变化 | 能证明什么 | 不能证明什么 |
| --- | --- | --- |
| 同任务换 seed | 对实例随机性的稳定性 | 机理外推 |
| 换 world/mechanism family | 对预注册机制轴的适应 | 现实化学迁移 |
| salted private cells | 对隐藏虚拟世界的泛化 | 实验室有效性 |

Train、Dev 和 Bench 的 mechanism cells 必须不重叠。Dev 可用于选择超参数；Bench 和 Private 不得
继续训练或调 prompt。

## Private-eval policy

维护者通过进程环境提供高熵 secret，例如：

```bash
CHEMWORLD_PRIVATE_EVAL_SALT=<secret>
```

- raw salt、隐藏 seeds 和可逆世界参数不发布；
- 没有 secret 时，`private-eval` 只是本地占位，不代表正式私有榜单；
- Agent 进程不接收世界 seed 或 salt，只接收独立 public agent seed；
- 对外只发布签名聚合 envelope、协议摘要和允许公开的统计；
- 私有数据不能用于事后选择方法、模型或 prompt。

显式 `--seeds` 适合 smoke 和研究运行；报告必须同时给出 seed 来源、是否预注册以及是否用于开发。
