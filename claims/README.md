# 任务认领制度

本仓库采用“先 claim，后实现”。任何代码、文档、实验或发布任务在开始前，都必须先创建并推送
一个 active claim；未完成 claim 的工作不得开始，也不得要求集成负责人预留文件。

## 强制流程

1. 同步 `main` 并查看现有认领：

   ```powershell
   git pull --ff-only origin main
   .\.venv\Scripts\python.exe scripts\manage_claims.py list
   ```

2. 检查任务和 owned paths 与现有 claim 不重叠。
3. 创建 claim：

   ```powershell
   .\.venv\Scripts\python.exe scripts\manage_claims.py claim `
     --task-id wf-20-instruments `
     --owner your-name `
     --branch team/wf-20-instruments `
     --scope "Instrument and spectrum reference models" `
     --paths src/chemworld/physchem/spectroscopy.py tests/test_spectroscopy.py
   ```

4. claim 必须作为独立的小提交先推送。只有远端能看到 `claims/active/<task-id>.json` 后，任务才算
   已认领，随后才能修改 owned paths。
5. 实现期间只能编辑 claim 的 owned paths。需要扩大范围时，先更新并推送 claim。
6. 完成并验证后关闭 claim：

   ```powershell
   .\.venv\Scripts\python.exe scripts\manage_claims.py complete `
     --task-id wf-20-instruments `
     --owner your-name `
     --summary "Reference cases and adapter proposal completed"
   ```

7. completed claim 保留在 `claims/completed/`，不得删除历史记录。

## 冲突与时效

- 一个 `task_id` 同时只能有一个 active claim。
- 两个 active claim 的 owned paths 不得相同、互为父目录或存在前缀覆盖。
- 默认有效期为 7 天。到期前仍未完成时必须更新 claim；过期 claim 会令本地门禁失败。
- 阻塞超过 24 小时应在 claim 的 notes 中说明；需要交接时先关闭原 claim，再由接手者认领。
- `src/chemworld/tasks.py`、World Law、runtime registry/dispatch、正式 golden、发布文档和 benchmark
  evidence 属于集成共享面，只能由明确认领 WF-00/WF-110 或 release integration 的负责人修改。
- 紧急修复也必须 claim；可以缩短流程，但不能跳过。

## 检查

```powershell
.\.venv\Scripts\python.exe scripts\manage_claims.py check
```

机器检查覆盖 schema、文件名、唯一 task、owned path 重叠和过期状态。认领只解决协作所有权，
不会替代测试、代码审查或 benchmark 冻结规则。
