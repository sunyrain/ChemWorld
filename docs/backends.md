# Backend 后端

Backend 层用于把同一套任务语义连接到不同物理实现：轻量 proxy、参考校准模块、外部
模拟器或未来真实设备 adapter。当前默认 backend 仍以可控虚拟环境为主。

## 为什么需要 Backend

没有 backend 抽象时，任务逻辑、物理近似和运行时工程会混在一起，导致 maturity 难以
声明、测试难以隔离、未来替换参考实现也困难。

Backend 应回答：

- 使用哪套物性/动力学/相平衡模型；
- 是否带噪声、近似或隐藏参数；
- 可复现性边界在哪里；
- 与 task maturity 的关系是什么。

## 参考校准

RMG-Py、IDAES、teqp、thermopack 等只适合作为独立校准层，不是 benchmark 的强制依赖。
新增 backend 必须保持公共语义，并公开依赖、适用域和 maturity。

## 当前边界

当前 ChemWorld 仍是 agent 化学交互环境，不是真实流程模拟器。Backend 抽象是为了给
未来升级留接口，而不是暗示当前所有结果已经达到工程级物性精度。
