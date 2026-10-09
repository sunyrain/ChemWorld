# ChemWorld 第一篇工作区

## 唯一当前入口

新协作者只需要先阅读：

1. [`../../AGENTS.md`](../../AGENTS.md)
2. [`FIRST_PAPER_TODOLIST.md`](FIRST_PAPER_TODOLIST.md)

第一篇原任务已冻结完成。用户新增的社区发布改良按
[TODO 第 9 节](FIRST_PAPER_TODOLIST.md#community-release-todo)分为 **Ours / LYJ** 两组，
按文件独占并行，协调者在 `main` 顺序集成；该节提供“完成 / 认领 / 暂未开始”状态格。
必要性评估见 [44 项改良清单](experiments/COMMUNITY_RELEASE_IMPROVEMENT_PLAN.md)。
不要认领旧 Work I task，不要恢复 claim、租约、integration queue 或逐任务 review 流程。

## 目录分类

- `FIRST_PAPER_TODOLIST.md`：唯一活跃执行清单。
- 退役计划、协调快照和旧审稿材料由Git历史保存，不再保留重复archive入口。
- `claims/`：仅保留 policy-validity 历史读取边界所需的 `W1-V06` 与 `W1-V08`；其余旧 claim 已移回
  Git历史。旧integration/review队列已删除；`story/`仅保留冻结图件输入所需的历史architecture，
  不分配工作或约束当前论文结构。
- `reports/`：历史和当前证据输出。只有当前 TODO 明确引用的结果才进入新稿件。
- 根目录中的旧 readiness、incident、related-work 和 master-plan 文档：为避免破坏冻结结果的路径
  绑定而原位保留，统一视为legacy evidence，不是当前计划；无路径依赖的旧provenance说明由Git历史保存。

若任何历史文档与当前 TODO 冲突，以当前 TODO 和用户最新指令为准。
