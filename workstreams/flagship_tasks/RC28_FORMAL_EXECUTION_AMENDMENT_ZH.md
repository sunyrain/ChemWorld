# ChemWorld RC28 正式执行修正说明

状态：`formal A2/A3 complete; joint Gate A decision passed`

RC27 A3 完整生成 2,016/2,016 个 terminal receipts。A2 在完整生成
2,736 个 receipts 后、首个电化学 budget-4 trial 被调度前 fail-closed：

```text
electrochemical-conversion controlled primary budget cannot cover every
declared relational intervention
```

静态关系并集证明表明：

- 反应–结晶的全部声明关系最少需要 4 个不同动作；
- 电化学的 constitutive low/pivot/high 需要 3 个同材料动作；
- solvent 与 electrolyte_profile 反事实各需要一个与共同 pivot 配对的单变量动作；
- 因而电化学的最小关系闭合并集是 5 个不同动作，4 个动作不可能完整覆盖。

RC28 以通用关系并集最小覆盖证书修复设计审计与正式入口：

- 在任何 A2 scheduler 前验证 primary budget 能闭合每个声明关系；
- 保留 A2 的 k=2、k=4 诊断曲线，新增最小可行 k=5 作为 primary certificate；
- A3 的 k={1,2,4,8} 时序检查点、online horizon=8 和 reference policy 不变；
- 世界、family、干预、六动作库、seed namespace、changepoint、阈值、scorer、
  bootstrap、聚合、exclusion 与 stopping rule 不变。

RC27 的 A3 与部分 A2 作为 superseded formal attempt 原样保留，不在 RC28
中复用、比较或解释。RC28 必须重新运行完整 A3 与 A2。

正式启动前，冻结提交 `6573c62d777a51305c66f58e9b27f5fefb9e060d`
已在 clean detached worktree 中通过 qualification check、A2/A3 零作业入口验证及
61 项 mechanism release/execution 集成测试。可复核环境与测试哈希见
`reports/mechanism-adaptation-clean-detached-attestation-v0.1-rc28.json`。

## 正式执行结果

RC28 从头重新运行并完成：

- A3：2,016/2,016 terminal receipts，4 个 trial manifests；
- A2：4,896/4,896 terminal receipts，8 个 trial manifests；
- A2/A3 的 protocol SHA-256 与 Gate A plan SHA-256 完全一致；
- A3 指标在 A2 完成前保持 embargo，随后只通过联合 public-decision 解封；
- 正式进程均正常退出，stderr 为 0。

联合决策为：

```text
a1_pass=true
a2_pass=true
a3_pass=true
gate_a_pass=true
benchmark_ready=true
go_no_go=a2_a3_passed
```

A2 主预算 `k=5` 下 active oracle 与 fixed decoder top-1 均为 98.26%；
A3 `k=8` 端到端 reference–detection–attribution 成功率为 96.57%。正式结果见
`reports/mechanism-adaptation-public-decision-v0.1-rc28.json`，结构完整性分别见
`reports/mechanism-adaptation-a2-structural-receipt-v0.1-rc28.json` 和
`reports/mechanism-adaptation-a3-structural-receipt-v0.1-rc28.json`。

该结果只解除环境 benchmark prerequisites。Participant-Agent Gates B–E 仍需要独立冻结
method roster、prompt/scaffold、runner、样本量、统计/排除规则和 provider 成本契约；当前不允许把
Gate A 通过解释为 DeepSeek 或其他 Agent 已通过，也不允许设置 `evidence_complete=true` 或
`publication_ready=true`。
