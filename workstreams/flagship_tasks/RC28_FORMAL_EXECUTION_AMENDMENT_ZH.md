# ChemWorld RC28 正式执行修正说明

状态：`pre-execution qualified; formal cohorts not yet consumed`

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
