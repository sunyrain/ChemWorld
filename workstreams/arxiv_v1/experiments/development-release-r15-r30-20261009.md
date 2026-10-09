# R15 / R30：当前语义标识与风险含义

开发块，Codex /root。main 不解释旧物理轨迹；论文复现独立使用 current.publication.frozen_release 指向的公开 v0.2.0 固定源码及 uv.lock，开发历史轨迹使用实际执行提交。新增 runtime_semantics_id 只用于拒绝误读，不选择后端、不保留旧执行器；新 API/时钟/采样数值不回填论文证据。

风险问题：safety_risk 累积了过程代理量与 invalid/rollback 的程序罚分；unsafe 只是任务阈值判定。先把这一事实公开于 task_info、task_prompt、step info 和 trajectory，不重写评分，也不把程序惩罚说成物理事故概率。

固定验证：离线文档例子的 seed 0 六步路径（1 次预期拒绝）验证新标识与 exact replay；另 seed 0 空釜 13 次 HPLC 拒绝，物料、体积、温度保持不变，sample_consumed=0，罚分累加到任务阈值。对同一六步日志删除/篡改 runtime 标识、混合一行旧标识三种情形均须在 0 步时返回原冻结 runtime 指引，不能启动新运行时假装兼容。相关风险/回放/接口测试只作功能验证。输出 `D:/Projects/ChemWorld-local-research/20261009-r15-r30/`，保留失败，不作正式资格或真实实验室安全声明。

结果：2/2 开发块通过，6+13=19 次真实操作、两条轨迹零容差 replay；3/3 历史/混合标识在 0 步拒绝且测试确认 gym.make 不被调用。13/13 预期拒绝完整保留，物料/温度/体积不变，实际样品消耗 0，程序罚分达到 1.0。机器摘要 `attempt-01/summary.json`，失败列表为空。

首次功能测试 60 passed / 1 failed：测试错误地期待 masked 拒绝观测也设置 unsafe=true；修正该断言并公开缺失语义后，风险/接口相关 25 项重跑通过，其余已通过项未重复。保留首次拒绝轨迹与测试错误说明。Ruff 通过；5 个修改模块 mypy 通过，agent_interface 的两处既有未标注装饰器签名错误与 HEAD 一致，本项不顺带重写。

LYJ R37/R38 交接：

- 当前 task_info 与 JSONL 的 `runtime_semantics_id=chemworld-current-20261009` 覆盖本轮热控、负结果、瞬时时钟及逐相采样合同；独立热控标识仍可供读者查明该项语义。它不是版本选择参数。当前包版本字符串仍待 R07 最终发行时与 __init__/打包一次对齐，不能拿 0.2.0 字符串代替执行语义标识。
- 论文复现入口为 [固定 v0.2.0 源码](https://github.com/sunyrain/ChemWorld-Public/tree/03e8026301c185fd6ba5bdbda7460765d9b3e724) 和该树的 uv.lock。该绑定来自 `configs/current.json` 的 publication.frozen_release；不要使用当前 main 的 uv.lock、仪器时钟或物理实现复现旧数值。旧开发轨迹则使用其真实执行提交，不统统归入论文 release。既有 JSONL 可以作为历史数据读取；读取文件不等于在 main 复现旧物理。
- `risk_signal_contract` 已进入 task_info、task_prompt、step info 与轨迹。safety_risk 是混合过程代理/程序惩罚；unsafe 是**已观测**数值的任务阈值，cost_components 也混有程序失败与成本。拒绝观测保持 null/mask=false，此时 unsafe=false 不是安全结论。未校准实验室事故概率，不更改现有评分权重或恢复任何旧评分执行器。
- 研究能力差异是明确的当前模式：默认分析观测归一化、v5 原始投料回收；不为历史错扣采样、旧时钟或旧热控添加执行分支。原论文、旧轨迹和正式证据保持不变。
