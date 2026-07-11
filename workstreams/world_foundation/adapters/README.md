# Model adapter provenance

本目录保存 World Law v0.4 集成时使用的 adapter 交付快照，仅用于来源追踪。运行时和发布门禁不再
读取这些 proposal；当前事实以 provider registry 与 model reachability audit 为准。

每份 proposal 必须：

1. 使用与对应 claim 相同的 `owner_workstream`；
2. 只列出 claim 已拥有的实现、测试、model card 和参考证据路径；
3. 使用新的 provider `model_id`，通过 `replaces_model_ids` 指明要移除的旧实现；
4. 指向 `chemworld-physical-chemistry-vnext`；
这些文件不得作为当前成熟度、readiness 或 benchmark 结论；下一版 adapter 不追加到本目录。
