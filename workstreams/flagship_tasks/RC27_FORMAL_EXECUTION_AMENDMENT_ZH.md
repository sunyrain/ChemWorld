# ChemWorld RC27 正式执行修正说明

状态：`pre-execution requalification required`

RC26 完成 A3 后，A2 在任何 A2 job 或 seed 被消费前被
`unsupported paired Gate A public contrast encoding` fail-closed 拦截。原因是正式计划自
RC24 起冻结为
`post_minus_pre_same_recipe_or_declared_same_background_relation`，而 runner 的入口检查
仍只接受旧的 `post_minus_pre_same_recipe` 字面值。下游 A2 实现已经支持并要求 declared
same-background relation；错误只位于入口允许列表。

RC27：

- 接受旧 same-recipe 编码及其已冻结的 relation-aware 扩展；
- 增加零 seed、零 job 的 production-entry validator；
- 保留 RC26 的正确结构收据计数：A3=2,016，A2=3,456；
- 不改变世界、family、干预、动作、预算、seed namespace、changepoint、reference
  policy、阈值、scorer、bootstrap、聚合、exclusion 或 stopping rule。

RC26 A3 报告作为 superseded formal attempt 原样保留，不在 RC27 中复用、比较或解释。
RC27 必须重新运行完整 A3 和 A2。
