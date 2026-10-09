# R08 / R31 / R14：适用域、当前能力与新增轴声明

开发块，Codex /root。5 个现有 authoring 轴已进入执行注册表，但 task_design 漏了科学注解，导致合同检查 4/6。只同步当前声明，并把开发 authoring 与已验证 benchmark 区分，不更新冻结 readiness/evidence 或声称新泛化结果。

固定覆盖：seed 0 的 reaction-to-crystallization、equilibrium-characterization 各一条默认参考路径；另结晶 population-regime / impurity-occlusion-law / impurity-occlusion-capacity 各 +1 extrapolation，平衡 mechanism-benchmark +1 extrapolation 与该 substrate 加 aqueous-ion-pair-network +0.7 interpolation，共 7 条路径。全部使用公开 task recipe 的固定 0.5 向量，终检、所有失败、物料/时钟/采样账与零容差 replay 保存。轴必须改变声明目标并实际进入完整路径；scalar-null 允许在当前样品上没有可观测响应，不按结果改配方。结果是功能/域验证，不是结构识别或泛化性能证明。

R31 复用 R01–R04 的切分/守恒/时钟/负结果与采样证据，不为同一修复再跑全模块校准；源模型卡补当前夹套与仪器 snapshot 的适用范围。现有原始结果按实际执行提交解释，不用当前 HEAD 重写旧数据。固定输出 `D:/Projects/ChemWorld-local-research/20261009-r08-r31/`。

结果：7/7 路径、72/72 操作提交、7/7 终检与零容差 replay；5 个轴均改变声明目标后进入实路径。首次报告因 runner 忘记向 verify_records 传 world_interventions 而只有 2/7 replay 通过；原始七条执行轨迹均完整，随后仅补齐原设计的上下文重验，不重复执行或覆盖数据。初始 5 个调用失败保留于 attempt-01/summary.json，最终逐路径结论在 attempt-01/replay-with-context.json。与现有 verifier 的私有干预上下文要求一致，不把这次工具调用错误写成平台非确定性。

20 项合同/模型卡/CLI 测试、Ruff 与 3 个模块 mypy 通过。实时合同检查 6/6，benchmark_ready 仍为 0；本项既不改冻结 readiness 文件，也不把 development_authoring 轴认证成正式泛化 benchmark。离子对网络需 coupled-equilibrium substrate，已在合同声明 required_context；capacity 轴只是 authoring 的 scalar null。

R31 给 LYJ 的科学适用域：

| 表面 | 当前声明与限制 | 本轮证据及实际边界 |
| --- | --- | --- |
| 反应/热 | 充分混合液相、常热容；当前未淬灭夹套 clip(4×温差, −70, 90) W；气相、变 Cp、多容器/连续 feed 不在事件合同 | R01 的 seeds 0/1/2，升温/降温/起始设点各 1×1200 与 6×200 s；最大末温差 7.16e−8 K，小于预定 0.002 K；物料 2e−7 mol、能量 0.05 J/2e−5 相对容差。不是所有相变/反馈策略的等价证明 |
| 测量 | 合成仪器，瞬时 snapshot，无排队/测量中并行演化；色谱轴不是世界时钟 | R03 6/6 时钟、消耗、成本与 replay；未做真实设备误差校准 |
| 采样 | selected receiver 或代表性浆料，未选中库存不变；默认分析归一化与 v5 原始投料回收分母不同 | R04 默认/v5 ×3 seeds ×GC/sample 共 12 路径；最大总体积误差 2.86e−18 L，对应 1e−12 L/mol 容差；不承诺任意瓶子/分样/合并 |
| 结晶 | 有界 van't Hoff 溶解度、幂律成核/生长与 cohort 粒群；无团聚/破碎；温度必须在曲线域内 | R02 负结果终检/null 与回放；粒径为合成 summary，低于回收阈值不能伪造粒径/纯度；不等于真实晶体预测 |
| 平衡/其他过程 | 仅注册的有界酸碱/沉淀、蒸馏、PFR、电化学等求解域；具体 assumptions/validity_limits 在现有模型卡 | 本项 7 条 authoring 功能路径；已有 ModelCard 的 reference_validated 描述所列数值/合成参考，不自动覆盖当前整个 runtime，也不表示工业准确性 |
| 风险 | 混合过程代理/程序惩罚，masked 时不能作安全结论 | R30 物理状态不变也能累积程序罚分；无真实实验室事故概率校准 |

底层模型卡已补当前夹套/采样/时钟的说明：`chemworld.physchem.reactor_cards.reactor_model_cards()`、`chemworld.physchem.crystallization_cards.crystallization_unit_model_cards()`、`chemworld.physchem.spectroscopy_adapter_manifest.instrument_runtime_model_card()`；其余模型同模块已有 ModelCard 返回 assumptions、validity_limits、model_limit_notes、validation_evidence。模型卡中的低层 semibatch/NMR 等可用性不能直接翻译成 ChemWorld Agent 操作支持。

R14 给 LYJ 的最小接口交接（复用现有接口，不新增能力 manifest）：

| 用户需要 | 权威入口与解释 |
| --- | --- |
| 该任务支持什么 | `env.unwrapped.task_info()` 的 allowed_operations、allowed_instruments、instruments、operation_contracts、kernel_maturity 与 runtime_semantics_id；registry 总词表不等于每个任务都允许 |
| 现在可做什么 | `chemworld.agent_interface.available_actions(env)` 与 `action_schema(env, operation)`；支持的动作在当前阶段仍可能不满足物料/资源/终态前置条件 |
| 输入范围 | 以 action_schema/operation validator 为准；共享 Gym Box 是上界包络，如温度 250–520 K，不代表每个过程在全区间有效；结晶冷却公开 250–330 K 仍须满足曲线域与状态条件 |
| 自由研究全流程 | 3 个 reaction-to-purification/crystallization/distillation 任务可显式设 full_process_contract_id="phase-resolved-process-v5"；其他任务不能直接套该模式；自动闭环不是通用多容器控制 |
| 电化学开放控制 | 用既有 electrochemical_workflow_mode 合同与 task_info 值；不能从一般任务表推断所有模式都能无限重复 setpoint |
| 仪器名称 | hplc、gc、uvvis、ph_meter、final_assay；full-process 再有 particle_size，最终允许项仍读 allowed_instruments；不可把底层光谱库函数名当 measure instrument ID |
| Gym/Agent/记忆 | R09 的 RLObservationWrapper/连续动作 wrapper；研究宿主 R17 notebook/事实 ledger；R18 history offset/next_offset；MCP step 只接收动作，文件自由度由宿主授权 |
| 当前与论文版本 | R15 的执行标识和独立 v0.2.0 论文快照；新版结果另列，正式包版本由 LYJ R07 与核心 __version__ 最终一次对齐 |

R19 与 R33 本次不触发：只确认脚本/文件恢复，不承诺真实 LLM 压缩恢复；只共享环境，不做排行榜或跨 provider 方法比较。R21 未设需满足的长程性能预算，本次 80 事件可读性不是规模性能证明，因此不推测性优化账本。R23–R29、R36 的 8 项新科学能力继续后置。
