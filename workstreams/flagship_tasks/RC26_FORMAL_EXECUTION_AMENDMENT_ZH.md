# ChemWorld RC26 正式执行修正说明

状态：`pre-execution correction; no formal cohort consumed`

RC26 只修正 RC25 A3 metric-embargo 结构收据的期望计数。RC25 将
`world_seeds_per_family=180` 在已经展开 task × candidate × world 的基础上再次相乘，
导致期望值被错误写成 362,880。冻结矩阵的正确计数为：

- A3 predictive fit：2 tasks × 4 candidates × 6 actions × 12 samples = 576；
- A3 online certificate：2 tasks × 4 truth states × 180 world clusters = 1,440；
- A3 terminal receipts：576 + 1,440 = 2,016；
- A2 terminal receipts：576 predictive-fit + 2,880 controlled certificate = 3,456。

该修正发生在任何 A2、A3 或 private seed 被消费之前。RC26 不改变物理世界、候选
family、干预、动作、预算、seed namespace、changepoint、reference policy、阈值、
scorer、bootstrap、聚合规则、exclusion 或 stopping rule。RC25 不用于正式执行，
保留在 Git 历史中作为被 RC26 supersede 的预执行候选。

RC26 继承 `RC25_EXPERIMENT_PLAN_AND_TODO_ZH.md` 中除版本化路径外的全部执行顺序、
go/no-go 规则和报告要求。正式命令使用 runner 的 RC26 默认值：

```powershell
.\.venv\Scripts\python.exe scripts\run_mechanism_adaptation.py `
  --stage online-attainability-certificate

.\.venv\Scripts\python.exe scripts\run_mechanism_adaptation.py `
  --stage gate-a `
  --online-attainability-certificate `
  workstreams/flagship_tasks/reports/mechanism-adaptation-online-attainability-certificate-v0.9-rc26.json

.\.venv\Scripts\python.exe scripts\run_mechanism_adaptation.py `
  --stage public-decision
```

正式 trial store 为 `runs/mechanism-adaptation-v0.3.0-rc26/confirmatory-trials/`；
所有重启只能加 `--resume`，不得删除 terminal receipt 后重跑。
