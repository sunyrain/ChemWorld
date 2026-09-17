# Experiment 1 Participant readiness after continuous qualification

状态：**CANDIDATE SCOPE ONLY — Participant execution 未授权**

机器事实来源：`EXPERIMENT_1_QUALIFICATION_REGISTRY.json`。

## 1. Current decision

105 个 atomic units 已全部有状态：`41 qualified / 64 failed / 0 pending / 0 N/A`。
只有 EC 达到体系级 15/15；它是唯一完整的 Participant-ready candidate，但仍需独立冻结
Participant/release manifest 后才能启动。

如果项目需要尽快开始 Agent 实验，可以另行预注册一个 **qualified-subset benchmark**，最多只
纳入当前 41 个 qualified units。不得把 failed unit 淆入主分析，也不得在看到 Agent 表现后改变
纳入规则。

## 2. Five-world-qualified loci

- EC：entity、parametric、structural；
- RX：parametric；
- PA：entity、structural；
- C：entity。

FL 没有通过的 locus。P/D 当前是 readiness failure：公开任务 5/5 smoke 可运行，但缺少正式
five-World/prior/private-family 前置资产，因此不能进入 Participant denominator。

## 3. Repair order

建议按“局部失败优先、整块设计其次、缺失 private physics 最后”推进：

1. RX entity（2 个失败）、C parametric（3 个失败）、PA parametric（4 个失败）；
2. RX structural 与 C structural（各 5 个失败）；
3. FL 三个 locus（15 个科学失败，需要重新检查 discriminator、后果门和 noise gate）；
4. P/D world authoring 与 prior generator；
5. P constant-K fork 与 D composition-dependent VLE fork。

每项 repair 必须使用新版本，保留本轮失败，不降低 Gate，并在新 evidence 产生前提交冻结合同。

## 4. Authorization boundary

本文件不选择 Participant 模型、不冻结正式样本量、不授权 provider call，也不发布 benchmark。
正式运行至少还需要：纳入单元清单、模型与 Arm 随机化、预算、重复数、停止规则、盲化边界、
统计分析计划和 release manifest。
