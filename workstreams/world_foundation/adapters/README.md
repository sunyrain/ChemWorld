# Model adapter proposals

本目录存放物理模块交给 WF-110 的机器可验收 proposal。不要手写或复制 hash；应通过
`ModelAdapterManifest.to_dict()` 生成完整 JSON。

每份 proposal 必须：

1. 使用与对应 claim 相同的 `owner_workstream`；
2. 只列出 claim 已拥有的实现、测试、model card 和参考证据路径；
3. 使用新的 provider `model_id`，通过 `replaces_model_ids` 指明要移除的旧实现；
4. 指向 `chemworld-physical-chemistry-vnext`；
5. 在本模块分支运行以下命令并保存通过报告：

```powershell
.\.venv\Scripts\python.exe scripts\validate_model_adapters.py `
  workstreams/world_foundation/adapters/<proposal>.json `
  --require-manifests
```

通过 intake 仅表示 proposal 可以进入共享 runtime 的集成审查，不表示成熟度已经提升，也不允许
模块团队自行修改 task contract、World Law、runtime dispatch、golden 或 benchmark evidence。
