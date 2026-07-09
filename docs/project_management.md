# 双人开发规则

本页给出小团队协作规则。目标是避免多人同时重构时互相覆盖，也避免文档、代码和 TODO
之间失去同步。

## 共享事实源

根目录 `TODO.md` 是唯一活跃任务板。每个任务必须有 owner、状态和可验收结果。
站点中的“统一任务板”只是摘要，不作为第二份工作板维护。

## 开始工作协议

开始前先同步主分支、查看当前 diff，并确认自己要改的文件范围。认领任务时必须更新
根目录 `TODO.md` 并推送，避免两个人同时做同一项。

## 工作中

- 小步提交。
- 运行与修改范围匹配的测试。
- 文档和代码一起更新。
- 如果发现他人未提交改动，先读懂再继续，不要回滚。

## 完成协议

完成后更新 `TODO.md`、运行检查、写清楚变更摘要和剩余风险，然后立即推送。

## 状态值

- `todo`
- `in_progress`
- `blocked`
- `review`
- `done`

仓库根目录 `TODO.md` 使用的正式状态为 `Open`、`Claimed`、`Active`、`Review`、`Done`、
`Blocked`。本页的小写状态只用于口头交接时快速描述。

## 交接说明

交接时写明：已完成什么、未完成什么、验证命令、下一步文件入口和已知风险。

## 检查

```bash
python -m ruff check .
python -m mypy src/chemworld
python -m pytest
python -m mkdocs build --strict
```

## 不要做

- 不要重置他人的未提交改动。
- 不要把大规模搬迁和功能修改混在一个提交。
- 不要在没有 maturity 标注时发布 benchmark claim。
