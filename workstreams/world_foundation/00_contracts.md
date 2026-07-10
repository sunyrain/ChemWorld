# WF-00 合同与集成边界

目标：冻结所有并行团队共同使用的最小 protocol，不实现具体物理模型。

独占范围：maturity/evidence schema、provider protocol、adapter manifest schema、模块可达性审计。

禁止范围：不得改变 v0.3 状态转移、task score 或正式轨迹。

交付：

- model input/output、units、domain check、diagnostics、failure 和 provenance protocol；
- operation → service → kernel → model 可达性报告格式；
- 每个模块的独立 fixture/stub；
- shared-file ownership 检查；
- 给 `110` 的 adapter manifest schema。

验收：`10`–`100` 团队只依赖这里的 protocol 就能运行模块测试；protocol 冻结后兼容性修改才可
进入当前开发周期。
