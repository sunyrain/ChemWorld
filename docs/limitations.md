# 适用范围与限制

ChemWorld-Bench 是评估 agent 在部分可观测、实验有成本、存在约束的虚拟环境中进行多轮探索、
调度和证据更新的研究平台。它不是现实产率预测器、分子模拟器、商业流程模拟器、实验机器人
控制软件或安全决策系统。

## 可以声明

- task、scenario、mechanism、provider、scoring 与 trajectory 有版本化合同和 hash；
- agent 通过公开 observation、instrument result、cost/risk 与历史轨迹作决策；
- v0.4 runtime 已接入显式的 LLE、干燥、浓缩、转移、结晶、蒸馏、流动和电化学窄域模型；
- WF-110 机器审计证明旧正式 proxy/fallback route 已移除，且实际事务执行与声明 provider 一致；
- 当前 v0.4 产物是 backend candidate，可用于后续有效性和方法实验。

## 不可声明

- 输出能够预测或指导真实反应、分离、谱图、装置设计或危险实验；
- `reference_validated` 或 `professional_candidate` 等于工业、法规或实验室验证；
- 历史 v1 结果可直接代表 v0.4；
- 当前 v0.4 已有论文级方法排名、统计功效、私评泛化或 SOTA 结论；
- leaderboard 分数代表现实实验成功概率。

## 仍然有限的表面

- reaction kinetics 是局部机制和速率律，不是数据库级真实反应预测；
- 分配系数、设备参数和物性切片为 benchmark 校准值，真实物料名不改变这一事实；
- 合成 HPLC、GC、UV–vis、IR、NMR、MS 与 final assay 是状态耦合观测模型，不是真实谱图预测；
- 水相平衡、电化学、结晶、流动和蒸馏均只覆盖模型卡声明的窄域；
- cost/risk 是任务约束信号，不是采购报价或安全合规结论；
- private-eval 无 maintainer salt 时仍是 placeholder，不能用于正式泛化声明。

## 发布状态

`benchmark/releases/chemworld-serious-vnext` 明确写入
`release_status=candidate_backend_only`、`benchmark_claim_allowed=false`。它没有包含新的 baseline
结果。必须先完成任务有效性/功效、泛化/反作弊、统一资源协议和多类方法实验，才能创建新的
冻结 benchmark release。历史 `chemworld-serious-v1` 不会被 v0.4 产物覆盖。

本地验证：

```powershell
python scripts/audit_vnext_runtime_integration.py
python scripts/build_vnext_backend_candidate.py
python scripts/run_release_gate.py
```
