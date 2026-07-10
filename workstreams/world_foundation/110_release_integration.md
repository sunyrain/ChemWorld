# WF-110 Runtime 接入与下一版冻结

本模块是共享文件的唯一所有者；在物理模块开发期间不与其它团队并行修改 shared files。

独占 paths：`tasks.py`、World Law、runtime registry/profile/domain services、world kernels、顶层 exports、
正式 docs、golden、benchmark validation 和 release artifacts。

集成顺序：

1. 验证模块 card、reference evidence 和 WF-00 protocol；
2. 接入一个模块并删除对应正式 fallback；
3. 运行 operation → model 可达性和守恒审计；
4. 每次接入保持测试可运行，所有模块完成后提升 World Law；
5. 重建任务 hash、golden、15-task consistency、serious baseline、response surface 和 replay；
6. 发布新 benchmark contract，不覆盖 v1。

验收：共享文件无跨团队冲突，正式 runtime 不存在隐式双路由，wheel 可复现新 World Law，所有
成熟度声明均由实际调用与证据自动生成。

## Adapter intake 门禁

专业模块在请求修改共享 runtime 前，将 `ModelAdapterManifest.to_dict()` 生成的 JSON 放入
`workstreams/world_foundation/adapters/`。intake 只接受满足以下条件的 proposal：

- `manifest_hash` 与全部字段一致；
- `owner_workstream` 存在对应的 active 或 completed claim；
- manifest 的 `owned_paths` 完全落在该 claim 范围内，普通模块不占用共享 integration path；
- provider symbol 已可导入，model id 不覆盖现有 provider；
- integration operation 已注册且属于 provider contract；
- replacement model id 已存在或由同批 proposal 提供；
- 目标是 `chemworld-physical-chemistry-vnext`，而不是冻结的 v0.3。

运行：

```powershell
.\.venv\Scripts\python.exe scripts\validate_model_adapters.py --require-manifests
```

本地发布门禁也会自动扫描该目录。目录为空时门禁通过；集成负责人开始模块接入前使用
`--require-manifests`，防止在没有交付物时误报完成。

## vNext staging plan

通过 intake 仍不等于可以修改 runtime。核心集成负责人使用 staging plan 区分三类交付：

- `diagnostic_addition`：只增加校验或诊断证据，不替代 runtime model，也不传播成熟度；
- `runtime_addition`：新增 runtime 能力，需要 World Law、路由和任务边界审查；
- `runtime_replacement`：使用新 model id 明确替代旧 model，仍需完成 runtime/reference evidence 后
  才能删除旧实现或修改成熟度。

只有 claim 已完成、intake 通过且不存在分类冲突的 proposal 才标记为 `integration_ready`。active
claim 对应的 proposal 会保持 `readiness_blockers`，但不会令默认结构门禁失败；这样模块团队可以先
运行完整 release gate，再按纪律关闭 claim。`--require-integration-ready` 仍会拒绝尚未完成的交付。
staging 自身永远不修改 v0.3、不删除旧模型，也不允许直接提升 task maturity。

```powershell
.\.venv\Scripts\python.exe scripts\build_vnext_integration_plan.py `
  --require-integration-ready
```

正式开始 runtime 替换前再增加 `--require-runtime-replacement`。该开关能防止把纯诊断模块误当成
物理底座替换已经完成。
