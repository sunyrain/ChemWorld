# 仓库开发与证据维护

本页说明如何区分 ChemWorld 的当前入口、历史实现、派生文件和实验证据。核心原则是：代码可以整合，
证据不能因为不再“当前”而被回写或删除。

## 当前入口

`configs/current.json` 是仓库唯一的人工维护当前面清单。它指向当前 backend、正式评测协议、机制适应
协议、方法冻结状态和仍可引用的开发证据。不要根据文件名中的 `vnext`、最大版本号或最近修改时间猜测
当前版本；历史配置会为精确回放继续留在仓库中。

项目的责任边界是提供物理化学 world-model 环境、反馈、预算和评测合同。它允许外部训练 Agent，
但评测 campaign 本身不更新 hosted model 的权重；campaign 内的适应指上下文、记忆、信念与行动更新。

## 内容分级

| 内容 | 处理规则 |
| --- | --- |
| `src/`、当前 `configs/` | 可在新版本中整合；行为或语义变化必须增加协议版本并补测试 |
| 冻结协议、报告、负结果 | 不回写、不就地“修好”；由新版本通过 `supersedes` 或当前面清单降级 |
| `runs/`、checkpoint、provider receipt | 默认视为原始证据；只有存在清单、摘要和保留决策时才能迁移或删除 |
| `workstreams/**/reports/archive/` | 非当前、但仍有审计价值的诊断；不会被默认入口或论文主张读取 |
| cache、`__pycache__`、文档 `site/`、LaTeX `build/` | 可再生派生物，可以安全清理 |
| `paper/figures/*.pdf` | 论文引用的确定性构建产物；PNG 预览不再生成或跟踪 |

当前没有活动论文稿。2026-07-21 的 NCS 工作稿已经归档到
`paper/archive/ncs-working-draft-2026-07-21/`；仓库根部的 `paper/main.*` 是更早的历史快照。历史稿件
并非可直接去重的副本，删除前必须先完成引用和证据账本迁移。

## 开发流程

1. 运行 `python scripts/manage_claims.py check`，再按 `claims/README.md` 建立互不重叠的 owned paths。
2. 从 `configs/current.json` 解析当前协议，不要在 runner 中硬编码“最新”文件名。
3. 修改 runtime 或协议时增加定向测试；修改冻结语义时创建新版本，保留旧入口供回放。
4. 运行 `ruff`、相关 `pytest`、配置与证据审计，再关闭 claim。
5. 提交前用 `git status --short` 检查未跟踪文件，尤其避免提交密钥、私有 seed 或 provider 原始响应。

### Source 与 evidence 的两提交证明模式

需要绑定 source commit 的生成证据采用两个连续提交：第一个提交只包含源码、协议与测试；随后在这个
干净 source commit 上按 evidence DAG 生成报告和 `configs/current.json`，第二个提交只物化这些证据视图。
因此 evidence-only 提交的 HEAD 比报告中的 `source_commit` 前进一个提交是预期状态，不是 stale evidence。
一旦第二个提交混入新的源码或协议变化，原证明立即失效，必须重新从新的干净 source commit 生成。

新增或迁移证据脚本必须复用 `chemworld.eval.provenance` 中的 canonical JSON hash、文件 hash、
原子 JSON 写入与 Git provenance 工具；不要在脚本内复制私有 `_write_json`、`_file_sha256` 或
tracked-tree 判定。生成节点、不可变输入和正式结果的角色与顺序只在
`scripts/evidence_pipeline.py` 的 evidence DAG 中声明。

常用检查：

```bash
python scripts/manage_claims.py check
python -m pytest tests/test_repository_current_registry.py -q
python -m ruff check src tests
python -m mkdocs build --strict
```

## 重复代码与版本化实现

协议 runner 中相似的 hash、Git 状态和 PPO/SAC preflight 逻辑目前有一部分是冻结源的一部分。直接抽取
公共函数会改变 source hash 和可复现边界，因此本轮不把它们当作死代码删除。后续应在新的协议版本中
引入共享工具，再让旧 runner 只承担历史回放。

同理，`MechanismDiagnosticLiveLLMAgent` 保留用于 v0.1 轨迹回放；新工作应从
`chemworld.agents.mechanism_adaptation_live_llm` 使用 `MechanismAdaptationLiveLLMAgent`。它不在包级
`chemworld.agents` 中重新导出，因为该入口受既有 LLM affordance source digest 约束。exact duplicate
文件若受 release manifest 或 replay digest 绑定，也应保留并在报告中解释，而不是按字节相同直接删除。
