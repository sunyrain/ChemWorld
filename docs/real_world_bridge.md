# 从虚拟世界到真实实验

> **ChemWorld 与现实的关系，不应只由“模拟得够不够像”一个问题决定。**

Core 研究的是受控世界中的实验决策与机制适应。Bridge 要进一步回答：虚拟训练是否能减少 Agent
适应独立模型、真实数据和物理实验所需的实验次数、风险与成本。

!!! info "当前状态"
    ChemWorld Bridge 是一条验证路线，不是已经交付的真实实验控制产品。当前网站描述的是分层目标、
    所需证据和首批候选，不声称已经完成物理迁移。

## 现实有效性的阶梯

| 层级 | 问题 | 当前主要承担者 |
| --- | --- | --- |
| 合同有效性 | 状态、操作、守恒和回放是否正确 | Core |
| 决策有效性 | 世界是否产生合理的实验权衡 | Core + Bench |
| 因果有效性 | 干预是否改变规律与有效策略 | Core + Bench |
| 行为有效性 | Agent 排名是否跨独立 backend 保持 | Bridge 待验证 |
| 迁移有效性 | 虚拟训练是否减少现实适应实验数 | Bridge 待验证 |
| 数值预测有效性 | 是否准确预测具体真实体系 | 仅限独立窄域模型，不是通用目标 |

Core 主要承担前三层。Bridge 逐步检验第四和第五层；任意真实化学体系的通用数值预测不属于当前
主张。

## 什么可能迁移

- 选择有信息价值的测量；
- 安排探索顺序；
- 表达和更新不确定性；
- 识别模型失效与世界变化；
- 从失败中恢复；
- 在安全和预算下进行少样本适应。

这些是实验策略层能力，不依赖某个匿名催化剂在虚拟世界中的具体最优用量。

## 什么不能直接照搬

- 匿名 Catalyst A–D 的具体身份和最佳用量；
- 未校准材料的绝对产率、谱图或分配系数；
- 虚拟风险分数对应的现实安全限值；
- 虚拟设备参数直接映射成现实控制设定；
- 在一个模拟器中的方法排名自动成为现实排名。

## Bridge Backend 架构

<div class="cw-bridge-flow">
  <div class="cw-bridge-step"><strong>Dataset Oracle</strong><span class="cw-muted">历史真实实验，只读查询</span></div>
  <div class="cw-bridge-step"><strong>Calibrated Simulator</strong><span class="cw-muted">用开发数据校准</span></div>
  <div class="cw-bridge-step"><strong>Independent Backend</strong><span class="cw-muted">独立实现与测试数据</span></div>
  <div class="cw-bridge-step"><strong>Physical Lab</strong><span class="cw-muted">审批后的窄域设备</span></div>
</div>

所有 Backend 共享公开 Action 与 observation 合同，但应明确声明无法映射的操作、单位转换、设备边界
和不确定性。Bridge 不允许用隐式 fallback 掩盖缺少现实实现。

## 一个 Bridge Pack 需要什么

1. 物料身份、批次与 provenance；
2. 虚拟 Action 到现实操作的映射；
3. 单位、设备能力与安全边界；
4. 仪器 observation 的校准和缺失策略；
5. 校准数据与完全独立的测试数据；
6. 预测与测量不确定性；
7. 人类审批、权限和停止规则；
8. 从建议到执行再到结果的 replay provenance。

## 第一批候选

| 候选 | 为什么适合 | 主要障碍 |
| --- | --- | --- |
| Partition | 条件温和、成本较低、测量和物料映射清晰 | 真实混合物身份、相平衡校准与仪器误差 |
| Flow | 连续反馈、系统辨识与工业意义强 | 设备时延、联锁、安全与高频数据 |
| Crystallization | 动态过程和多目标适应价值高 | 成核随机性、粒度测量与设备差异 |
| Distillation | 多阶段规划与能耗问题重要 | 设备规模、安全和运行成本，不宜作为首个硬件闭环 |

建议顺序是：Partition 数据/低风险实验 → Flow shadow mode → Crystallization 窄域验证 → 更复杂流程。

## 正确的迁移指标

零样本复制虚拟最优配方不是主要终点。更关键的是在相同现实预算 `k` 下比较：

```text
Transfer advantage(k)
  = J(pretrained → target, k experiments)
  - J(from scratch, k experiments)
```

还应报告：

- 达到同一目标减少了多少次现实实验；
- 适应期间的风险、失败与样品成本；
- 预训练先验是否造成负迁移；
- 与只使用现实开发数据的方法相比是否仍有收益。

## 从 Shadow Mode 开始

第一阶段 Agent 只提出建议，不控制设备。人类执行经过审批的操作，再把结果回写为 observation。
只有建议质量、权限、安全限幅、停止条件和 replay 链经过独立验证后，才讨论窄域闭环。

```text
Agent proposal
  → deterministic validator
  → safety envelope
  → human approval
  → device adapter
  → measured result
  → provenance and replay
```

设备执行永远不能只依赖模型自然语言。任何现实实验都需要相应机构、人员资质和本地安全流程。

下一步：[材料名称代表什么](material_identity.md) · [模型成熟度](model_maturity.md) ·
[了解适用范围](limitations.md)
