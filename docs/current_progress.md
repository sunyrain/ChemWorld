# 当前进展

ChemWorld 已从单一任务原型推进到统一世界律下的多任务 benchmark 雏形。当前核心问题不再是
“能否创建环境”，而是如何持续提高物理化学底座、agent 交互合同、任务成熟度和发布可信度。

## 阶段总结

- 正式 Gymnasium 入口为 `ChemWorld`；
- 任务通过 `task_id` 选择，共享 `world_law_id`；
- Runtime V2、typed ledger、transaction record 和 instrument observation 已形成主线；
- Agent-facing API 已支持 task prompt、available actions、validation、RL/tool-json/lab-report observation view 和 campaign state；
- 公开预发布包的 P0/P1/P2/P4 已完成；
- P3 专业物理化学深化已经开始，D4 组已完成。

## 已实现能力

- 反应、分离、表征、安全、机理解释、连续流、电化学和 tool-agent planning 任务切片；
- action schema、recipe 执行和 operation validator；
- safety/cost/constraint flags；
- 虚拟仪器和虚拟光谱；
- replay verifier、golden trajectories、baseline report 和 release gate；
- 本地教师端/学生端评测机模拟；
- LLE phase split 的 TPD-style diagnostic；
- aqueous acid-base pH observation 与 Ksp precipitation hooks；
- Gibbs minimization 的 constraint/KKT-style diagnostics。

## 当前验证状态

推荐门禁：

```bash
python -m ruff check .
python -m mypy src/chemworld
python -m pytest
python -m mkdocs build --strict
python scripts/audit_environment_consistency.py --tasks all --seeds 0 1 2
```

D4 相关专项测试当前通过：

```bash
python -m pytest tests/test_equilibrium_chemistry.py
```

## 成熟度边界

当前系统应被称为 research benchmark / virtual chemical world model gym，而不是：

- 真实反应预测软件；
- DFT wrapper；
- 完整流程模拟器；
- 机器人控制器；
- 通用 chemical world model。

所有公开 claim 都必须携带 maturity label 和适用范围。

## 已知风险

- 仍有多个 P3 专业模块未完成；
- 部分物理模块仍是 proxy/lite；
- 英文镜像尚未逐页维护；
- 历史文档仍可能存在需要继续清理的旧审计文本；
- 当前 D4 的 pH 和 Gibbs 能力是 benchmark slice，不是数据库驱动的严谨 speciation 或 multiphase equilibrium solver。

## 下一步

按照当前用户要求：D4 完成后暂停，先讨论后续路线。若继续 P3，优先从未被 `liyijun`
认领的开放项中选择，并保持每个专业切片都同步代码、测试、model card、文档和 TODO。
