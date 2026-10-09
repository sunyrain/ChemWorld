# R04 / R09：当前采样合同与 Gym 适配

开发块，Codex /root。现有默认 Python/Gym 入口仍接受新实验，RLObservationWrapper 与连续动作 wrapper 已公开；因此 R04/R09 的条件已触发。修正当前实现，不为了旧轨迹保留旧采样分支。历史数据只由原执行快照解释。

问题：选中接收器采样是否只扣除该库存、体积/物料/消耗字段能否对账；标准 Gym checker 的差异来自科学状态还是会话元数据？先定位 root cause，再复用现有 wrapper 给出受支持入口。保持 missing mask、科学确定性、唯一 campaign 标识及原始可审计记录。

固定覆盖：reaction-to-distillation 的默认模式/v5，各 seeds 0/1/2；公开 task recipe 0.5 向量执行到蒸馏接收器建立，再分别 GC 0.00015 L 和 sample 0.0001 L，共 12 条路径。逐相、总量、原始投料分母、采样消耗、失败和零容差重放全部记录。容差 1e-12 L/mol，未选中库存不变，sample/measure 顶层字段等于账本增量。若前缀不能建立接收器，保留失败并报告，不按结果选路径。

Gym：reaction-to-assay、reaction-to-distillation、reaction-to-crystallization、partition-discovery 四类任务，RLObservationWrapper 与再包 ContinuousEventActionWrapper 两种入口，共 8 个标准 checker；另两个向量环境固定 seed 42、20 次公开动作抽样，检查有限向量与 mask。raw NaN 语义保留并说明其与标准 checker 不兼容，受支持 checker 入口明确使用 wrapper；不关闭检查。输出在 `D:/Projects/ChemWorld-local-research/20261009-r04-r09/`，记录完整失败，不作训练效果或正式证据声明。

首轮诊断：12 条采样路径与 8 个 checker 通过，但相关集成 104 passed / 3 failed，其中两项证明把默认分析模式的归一化分母也改成原始投料会使纯取样被计入 conversion；另一项仍期待 R03 已删除的 120 s 粒径延时。该设计不接受，首轮仅作开发失败记录，不据此结项。

后续修正块在执行前声明：保留以上全部路径/seed/操作/容差与覆盖；逐相采样只有一个实现。分母按测量用途区分：默认分析模式保持取样归一化，full-process 模式保持原始投料回收分母，均不提供旧结果解释引擎。这替代首轮把两种测量分母统一的错误设计；新增两条已有单釜 HPLC 组成不变测试为接受条件。重新执行完整 12 条采样、8 个 checker 与向量块，结果另存 attempt-02，不覆盖首轮诊断。

最终结果：21/21 单元通过，12/12 采样路径、144 次操作、12/12 零容差回放；GC/sample 只扣除 selected domain，未选中相逐值不变，顶层 sample_consumed 来自实际 ledger 增量。8/8 官方 Gym checker 通过，双环境 20 步向量循环通过；保留 checker 关于 wrapper 和 Box 范围的建议 warning。相关集成 129 passed，Ruff 与 5 个修改模块 mypy 通过。首轮轨迹/3 项失败记录保存在 attempt-01，最终机器摘要为 attempt-02/summary.json。

LYJ 交接：标准训练入口使用 `RLObservationWrapper(gym.make("ChemWorld", task_id=...))`，Box 动作再包 `ContinuousEventActionWrapper`。raw 环境保留 NaN/mask 的研究接口，因此不宣称 raw 可通过默认 equal_nan=False 的 checker。wrapper 的 `last_audit_metadata["campaign_id"]` 保留真实独立标识；同 seed 的训练 info 不包含该随机标识，核心 env 与轨迹日志仍保留。此验证针对默认资源配置，不声称资源卡或所有 wrapper 组合均已穷尽检查。

当前默认分析模式的归一化量与 full-process 模式的原始投料回收率须在文档中区分；研究者要逐相库存/原始投料回收语义时使用 v5。没有保留旧版错扣采样实现；新旧结果不可直接混用，旧轨迹交给原冻结执行环境。
