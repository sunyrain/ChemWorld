# 发布说明

## World Law v0.2

当前发布使用 `chemworld-physical-chemistry-v0.2` 和
`chemworld-task-contract-0.4`。世界律版本提升表示运行时物理语义发生了可观察变化；旧轨迹
不会被静默解释为新合同。

### 专业模块接入

- 冷却结晶运行时改用 van't Hoff 溶解度曲线、显式晶种质量和紧凑粒度群体平衡，输出
  D10/D50/D90、过饱和度、纯度、回收率和物料残差；
- 连续流运行时改用几何解析 PFR，记录体积、管径、轴向温度边界、Reynolds 数、压降、
  求解器诊断和能量账；
- 相接触和洗涤改用活度修正萃取 train，记录逐级收敛、夹带、TPD-style 稳定性诊断和
  组分物料守恒；
- 上述任务模块标为 `professional_candidate`，不再标为 proxy。

### 保留的降级边界

干燥、浓缩和转移仍使用有界、可解释的 benchmark 降级模型，因为当前没有覆盖同一运行时
语义的专业模块。包含这些动作的任务继续公开 `proxy_allowed=true`。合成仪器信号和部分安全/
压力关系也保持其声明的轻量边界。

### 合同与复现

- 所有任务合同 hash 和冻结 scripted trajectories 已按 v0.2 重建；
- replay verifier 会拒绝 world law、mechanism、runtime profile 或 scoring contract 不匹配；
- 任务的 `kernel_maturity`、`physics_maturity` 与 `proxy_allowed` 随 reset 信息、trajectory、
  dataset card 和 submission manifest 一同发布。

迁移旧结果时，请在旧环境版本完成复现，或在新版本重新运行；不要跨版本直接比较未经重新
生成的 trajectory score。

## Task Contract v0.4

- 通用 `core` / `serious` preset 替代投稿专用命名；
- 新增机器可读 serious-task readiness contract 和 `chemworld tasks readiness`；
- 严肃候选套件排除所有 proxy task，并区分 `contract_ready` 与 `benchmark_ready`；
- task JSON schema 从四个必填字段扩展为完整可执行合同；
- 删除完成后只做重导出的 runtime kernel facade，运行时直接依赖 contracts、registry 与 profile。
