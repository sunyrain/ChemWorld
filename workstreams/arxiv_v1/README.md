# ChemWorld 第一篇工作区

## 唯一当前入口

新协作者只需要先阅读：

1. [`../../AGENTS.md`](../../AGENTS.md)
2. [`FIRST_PAPER_TODOLIST.md`](FIRST_PAPER_TODOLIST.md)

第一篇当前由 `codex-1` 在 `main` 上单 agent 推进。不要认领旧 Work I task，不要恢复
claim、租约、integration queue 或逐任务 review 流程。

## 目录分类

- `FIRST_PAPER_TODOLIST.md`：唯一活跃执行清单。
- `archive/`：已退役的计划、协调快照和旧审稿材料，只用于历史追溯。
- `claims/`：仅保留 policy-validity 历史读取边界所需的 `W1-V06` 与 `W1-V08`；其余旧 claim 已移回
  Git 历史。旧 integration queue 已删除；`story/`、`reviews/` 中仍有少量 legacy consumer，均不分配
  工作或约束当前论文结构。
- `reports/`：历史和当前证据输出。只有当前 TODO 明确引用的结果才进入新稿件。
- 根目录中的旧 readiness、incident、related-work 和 master-plan 文档：为避免破坏冻结结果的路径
  绑定而原位保留，统一视为 legacy evidence，不是当前计划；无路径依赖的旧 provenance 说明已移入
  `archive/evidence/`。

若任何历史文档与当前 TODO 冲突，以当前 TODO 和用户最新指令为准。
