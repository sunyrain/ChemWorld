# 研究发现

!!! warning "Pre-v0.5 诊断结果"
    早期 classical、Safe-GP 与 SAC 数字早于 v0.5 candidate backend，只用于说明协议和失败模式，
    不能作为当前 15 个任务上的方法排名。

> **ChemWorld 已经形成有价值的环境控制、失败案例和诊断证据，但尚未完成正式 benchmark release。**

## 证据等级

| 等级 | 含义 |
| --- | --- |
| 已实现 | 存在可执行代码路径和公开接口 |
| 控制验证 | 可执行对照证明环境行为符合合同 |
| Agent 演示 | Agent 在开发实验中表现出可解释行为 |
| 确证结果 | 冻结方法在未触碰 cohort 上完成评估 |
| 外部桥接 | 独立 backend、真实数据或物理证据提供支持 |

## 发现一：目标提升可能掩盖风险退化

早期无约束 structured GP 在部分任务上提高目标值，同时增加操作风险超限。因此，最终 outcome 不能替代
风险、成本和协议有效性的独立报告。

## 发现二：严格判据应保留有信息量的失败

早期 Safe-GP 确证在四个任务上改善目标并满足安全/成本规则，但 flow effect 低于预注册实用阈值，
所以整体主张仍然失败。ChemWorld 将这种边界失败保留为结果，而不是事后放宽阈值。

## 发现三：受控可识别性通过，在线 material family 仍失败

当前 material、mechanism 与 constitutive-law counterfactual 均由隐藏世界执行。RC20 在预算 4 下的
controlled matched certificate 为 235/240（97.92%）并通过；独立 online-policy-feasible certificate
总体为 227/240（94.58%），但反应催化剂映射反事实仅识别 22/30，未满足逐 family Wilson 规则，
因此 Gate A 总状态为 false。`rate_law_family` 在受控与在线证书中均为 29/30，不是当前阻断项。
RC20 将该 family 绑定为上游目标生成路径的 pivot-normalized catalyst-activity-order stress，并验证
结晶构成参数不变。该结果只支持受控条件下的可识别性，不证明被评 Agent 已具备机制发现能力，
也不代表发现了结晶动力学或精确速率参数。以上数字是冻结的 RC20 历史结果；诊断设计合同版本化后，
当前源码绑定已失效，等待 RC21 重新认证。非正式开发曲线显示 material family 在 4–12 步之间仍会
平台，下一 decoder 需要显式使用跨动作关系证据。

## 发现四：当前 RL 证据诊断的是合同，不是排名

早期 100,000-step SAC 管线能够端到端运行，但行为覆盖和核心 flow operation 仍不足。当前结果用于发现
action、reward、checkpoint 和资源计量问题，不构成正式多 seed 排名。

## 发现五：LLM 的反馈利用需要因果消融

operation-level 交互、跨实验记忆、光谱披露和资源计量已经实现，但解释文本本身不能证明反馈改变了决策。
正式证据仍需要局部配对反馈反应测试和完整 campaign 因果消融。

**当前状态：benchmark candidate。** 尚不支持 SOTA、完整 RL/LLM 排名、Agent 机制适应或真实世界迁移主张。
机器可读状态以 [`configs/current.json`](https://github.com/sunyrain/ChemWorld/blob/main/configs/current.json)
和[证据与当前状态](benchmark_release.md)为准。
