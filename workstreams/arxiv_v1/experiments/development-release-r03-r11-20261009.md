# R03 / R11：测量时钟与 CLI

开发验证，Codex /root；不产生正式论文证据。问题：声明、实际采样、返回和资源时间是否一致；常见 CLI 输入错误是否给出可操作的短诊断？

当前世界没有排队或测量期间的反应演化模型。采用统一的瞬时虚拟快照：全部六种仪器的 latency_s=0，采样时刻=返回时刻=当前 ledger.time_s，不推进反应、温度或能量，只扣既有仪器成本及样品。色谱横轴是信号的保留时间，不是世界经过的时间。不伪称真实仪器耗时，也不引入两套时钟或兼容开关。

执行前固定覆盖：6 种仪器（HPLC/GC/UV–Vis/pH/final assay/particle size），final assay 先合法终止，particle size 使用 R02 固定 320 K 真零配方。比较仪器声明、acquisition 回执、前后世界时间/温度/三项能量、成本与样品；被拒的测量不能记仪器消耗。用记录与 zero-tolerance replay 验证实际路径。前后物理时钟/温度/能量要求逐值相等，资源差与声明误差 ≤ 1e-12。CLI 通过真实子进程检查未知 task/scenario/env、缺文件、坏 JSON、JSONL 非对象及坏 action 形状，退出码 2 且无 traceback；有效命令继续成功，合法但未通过的业务校验保留退出码 1。

输出在 `D:/Projects/ChemWorld-local-research/20261009-r03-r11/`，失败完整保存；首次执行后不改覆盖/容差。修复受影响实现后重跑该块并保存旧尝试。定向单元测试补充当前边界；不运行 provider 或全仓审计。

结果：开发修复完成。`attempt-01/summary.json` 保存 6/6 仪器路径与零容差回放、7/7 真实 CLI 错误子进程，全部通过。15 项新增定向测试通过；相关整合测试 65 passed、1 failed，唯一失败为本轮之前已发现的 R08：readiness 声明 4/6 而旧测试要求 6/6。本次未伪造 readiness、未刷新历史资格；R08 继续按支持范围决定。Ruff 和 6 个修改源码文件的 mypy 通过。首次整合命令误用了不存在的测试文件名，未运行任何测试；随后使用实际测试文件重跑，以上为真实结果。

给 LYJ 的接口交接：

- `task_info()['instruments'][id]` 的 `clock_semantics='instantaneous_snapshot'`、`latency_s=0`。全部测量 `raw_signal.acquisition` 给出 clock_semantics、sample_time_s、result_time_s，后两者相等。物理时间冻结不是免费测量：成本、取样和 campaign 仪器使用上限继续生效。该简化不支持真实仪器耗时、排队或测量期间的反应演化；色谱信号横轴不等于经过的世界时间。
- CLI 对 OSError、输入 ValueError 和未知 Gym 环境给 `chemworld: error: ...` 及退出码 2；未知 scenario 在对应入口转换为输入错误，不兜底吞掉程序内部的任意异常。坏 JSONL/非对象记录包含路径与行号。原有业务校验失败仍为退出码 1，正常输出格式不变。
- 旧论文及旧开发轨迹仍使用原冻结代码；没有保留非零延迟兼容分支。R01/R02 报告中的 120 s 粒径时间属于当时版本的结果，不回填。
