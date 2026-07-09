# 代码审计

本页记录当前工程结构的主要审计结论。原始逐条历史记录较长，发布站点中保留中文收束版；
更细的过程信息应放入开发日志或 archive。

## 主要发现

### 高优先级：PhysChem 大模块仍需继续拆分

部分物理化学模块已经完成 facade 化，但仍有一些文件同时承担 public spec、数值 kernel、
验证 helper 和导出列表。后续应继续按职责拆分，避免单个文件成为审查和测试瓶颈。

建议方向：

- public dataclass / spec 放在 `*_specs.py` 或 model card 模块；
- 数值 kernel 放在独立实现模块；
- validation helper 与测试 fixture 分开；
- facade 只保留稳定导入面。

### 中优先级：Model card 应继续模块化

model card 是 maturity、参考来源、适用边界和验证证据的承载层。它们不应散落在 runtime
或数值 kernel 中。推荐为 properties、reactors、separations、spectroscopy、transport
等模块分别维护轻量 metadata。

### 中优先级：Runtime V2 边界已建立

当前 runtime 已经具备 `ChemWorldRuntime`、mechanism-aware state、typed ledgers 和
domain services。下一步不是重写 runtime，而是继续收紧边界：

- generic runtime 不直接读取固定 species 名；
- task-specific scoring 进入 world/scoring 或 task evaluator；
- process operation 不在 runtime 主循环里写大量 inline branch；
- action catalog 属于 world-law 层。

### 中优先级：黄金表征测试值得保留

golden characterization tests 能保护 agent-facing 行为不被重构破坏。建议继续覆盖：

- reset info；
- action validity；
- reward timing；
- constraint flags；
- spectra/instrument readout；
- replay verification。

### 低优先级：Facade 较大但目前可接受

一些 facade 导出较多，但它们为外部用户提供稳定导入路径。短期不必为了“看起来更小”
破坏 API；优先拆内部职责。

## 已完成清理

- property 模块已从大型数值文件收缩为更薄的 facade。
- reactor 模块已完成初步职责拆分。
- mechanism compiler、runtime kernel/profile、domain-service composition、constitution、
  foundation state 等边界已有测试保护。
- action catalog 已向 world-law 层迁移。
- duplicated scoring island 已收束到统一 scoring 路线。

## 验证

推荐检查：

```bash
python -m ruff check .
python -m mypy src/chemworld
python -m pytest
python -m mkdocs build --strict
```

架构类测试应持续防止 runtime、world law、task registry 和 physchem kernel 再次互相侵入。

## 下一轮清理顺序

1. 先处理仍然超过合理长度的 physchem 模块。
2. 再整理 model card 和 maturity metadata。
3. 最后处理 facade 命名和 public exports。

整体判断：当前工程已经从“功能堆叠”进入“边界可维护”的阶段，但距离科研级长期维护还
需要继续压缩大文件、冻结 public contract，并把 maturity metadata 做成发布硬门槛。
