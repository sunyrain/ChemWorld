# 专业化深化 TODO 归档

本页不再作为活跃任务板使用。

当前唯一活跃任务板是仓库根目录的 `TODO.md`。专业化深化任务已经并入其中的
`P3 Professional PhysChem Deepening`。

## 当前使用规则

- 计划、认领、完成状态和剩余工作量只更新根目录 `TODO.md`。
- 本页仅保留归档说明，避免站点读者看到过期乱码或过期路线。
- 专业化深化任务不阻塞第一个 public benchmark pre-release，除非它直接影响冻结任务的可信度。

## 深化工作的边界

专业化深化的目标不是一次性实现完整化工流程模拟器，而是逐一替换当前明确声明的 proxy/lite surface。每个深化任务都应满足：

- 范围小且可审计；
- 有物理假设、适用边界和 maturity 标记；
- 有测试或参考案例；
- 不破坏 Gym API、trajectory replay、task cards 和 benchmark 复现。

详细任务以根目录 `TODO.md` 为准。
