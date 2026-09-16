# Astra完整流程单轮开发结果

2026-09-14；GPT-6 Astra / medium；开发证据，非正式实验。

本轮每任务一个自主单批，Agent选择全部操作、材料和测量。尚未进行多批发现、机制组合迁移或信息损失因果实验。

预定Agent条件3个，实际启动3个、合法终检2个、质量达标0个；无Agent补跑。
参考尝试4个，包含1次干燥时间记账失败及其独立修正验证；3个完成终检。

质量目标：纯化/蒸馏纯度≥80%、回收≥10%；结晶纯度≥80%、排除晶种回收≥10%、细粉≤50%。
参考均未满足全部目标，因而未建立质量联合可达性的参考见证；阴性结果不能直接判为Agent能力缺陷。

## 终检结果

| 流程 | 条件 | 动作提交/记录 | 纯度 | 回收 | 细粉 | 原生分数 | 质量达标 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 反应—萃取—纯化 | 原参考 | 16/15 | — | — | — | — | 未评估 |
| 反应—路径依赖结晶 | 原参考 | 16/16 | 97.95% | 43.40% | 100.00% | 0.3579 | 否 |
| 反应—分段蒸馏 | 原参考 | 17/17 | 8.09% | 88.32% | — | 0.2447 | 否 |
| 反应—萃取—纯化 | 修正参考 | 21/21 | 79.84% | 3.73% | — | 0.2886 | 否 |
| 反应—萃取—纯化 | Astra自主 | 22/22 | 28.40% | 10.65% | — | 0.1259 | 否 |
| 反应—路径依赖结晶 | Astra自主 | 1/1 | — | — | — | — | 未评估 |
| 反应—分段蒸馏 | Astra自主 | 17/17 | 24.42% | 97.05% | — | 0.4297 | 否 |

回收使用各原生任务的分母；结晶是排除晶种的下游回收率，不等于原料到产品的总收率。原生分数为次指标。

## 本轮观察与下一步假说

纯化Agent进行了三段加热及六次HPLC；后段反应的转化读数继续上升，产率与选择性读数下降。后处理先加有机相、洗涤，后来才加萃取剂并混合，整条轨迹没有显式settle/separate_phase。这提示需要检验实验阶段组织和选相前信息使用，但没有同前缀对照，尚不能归因具体损失来源。

蒸馏Agent完成三段加热、两段蒸馏与一次全部收集。高回收伴随低纯度；原生加权分数也未保证质量达标。应在后续独立块比较同一前缀的继续蒸馏、停止及收集策略，并核对采样对象；不能把不同阶段的GC读数变化直接归因于某个控制参数。

结晶仅完成第一次加料便出现provider错误，原始回执只保留未分类错误摘要，具体服务原因未确证。本轮不补跑，不将此条件计作科学失败；完整自主结晶表现仍未知。

下一块优先证明质量目标在公开操作和预算内可达，再做有信息对照的过程决策实验。本轮在3个预定Agent条件终态后停止，没有继续扩大样本或搜索失败案例。

## 自主执行轨迹

### 反应—萃取—纯化

状态：completed；已记录22次动作，22次提交成功。

| 步 | 操作及参数 | 事务状态 |
| --- | --- | --- |
| 1 | `{"amount_mol":0.04,"operation":"add_reagent"}` | committed |
| 2 | `{"operation":"add_solvent","solvent":2,"volume_L":0.04}` | committed |
| 3 | `{"catalyst":0,"catalyst_amount_mol":0.001,"operation":"add_catalyst"}` | committed |
| 4 | `{"duration_s":1800,"operation":"heat","stirring_speed_rpm":600,"target_temperature_K":345}` | committed |
| 5 | `{"instrument":"hplc","operation":"measure"}` | committed |
| 6 | `{"duration_s":7200,"operation":"heat","stirring_speed_rpm":800,"target_temperature_K":365}` | committed |
| 7 | `{"instrument":"hplc","operation":"measure"}` | committed |
| 8 | `{"duration_s":10800,"operation":"heat","stirring_speed_rpm":800,"target_temperature_K":345}` | committed |
| 9 | `{"instrument":"hplc","operation":"measure"}` | committed |
| 10 | `{"operation":"quench"}` | committed |
| 11 | `{"operation":"add_phase","phase":"organic","volume_L":0.04}` | committed |
| 12 | `{"operation":"wash","wash_volume_L":0.02}` | committed |
| 13 | `{"instrument":"hplc","operation":"measure"}` | committed |
| 14 | `{"extractant":3,"operation":"add_extractant","volume_L":0.02}` | committed |
| 15 | `{"duration_s":600,"operation":"mix","stirring_speed_rpm":600}` | committed |
| 16 | `{"instrument":"hplc","operation":"measure"}` | committed |
| 17 | `{"operation":"wash","wash_volume_L":0.02}` | committed |
| 18 | `{"operation":"dry"}` | committed |
| 19 | `{"instrument":"hplc","operation":"measure"}` | committed |
| 20 | `{"duration_s":1800,"operation":"concentrate"}` | committed |
| 21 | `{"operation":"terminate"}` | committed |
| 22 | `{"instrument":"final_assay","operation":"measure"}` | committed |

模型终答（保留其自述，解释须结合实际轨迹）：

Completed one vessel through termination and final assay; the batch was not discarded. Used 0.040 mol reagent, 40 mL acetonitrile and 0.001 mol Catalyst A. HPLC-guided heating increased conversion, but extended heating reduced product yield and purity. Quenched, added organic phase and toluene extractant, mixed, washed, dried and concentrated. Final assay: purity 0.2840 (FAIL: target ≥0.80), recovery 0.1065 (nominal PASS: target ≥0.10), yield 0.1008, conversion 0.8342 and process mass-balance error 0.00166. Overall quality objective was not achieved. Native leaderboard score: 0.12586. Used 22 of 90 operations, six HPLC measurements and one final assay; peak reported safety risk was 0.2496, below 0.65. Total reported physical cost was 1.5227 benchmark units. Recovery is close to its threshold relative to assay noise; this single synthetic trajectory does not establish causal effects or an optimal process.

### 反应—路径依赖结晶

状态：failed；已记录1次动作，1次提交成功。

| 步 | 操作及参数 | 事务状态 |
| --- | --- | --- |
| 1 | `{"amount_mol":0.04,"operation":"add_reagent"}` | committed |

模型终答（保留其自述，解释须结合实际轨迹）：

未取得有效终答

失败：`{"message": "Codex session crossed a frozen operational limit before the next executable operation; no fallback action was emitted: max_provider_error_events", "type": "InteractiveCodexExperimentError"}`

### 反应—分段蒸馏

状态：completed；已记录17次动作，17次提交成功。

| 步 | 操作及参数 | 事务状态 |
| --- | --- | --- |
| 1 | `{"amount_mol":0.04,"operation":"add_reagent"}` | committed |
| 2 | `{"operation":"add_solvent","solvent":2,"volume_L":0.04}` | committed |
| 3 | `{"catalyst":0,"catalyst_amount_mol":0.002,"operation":"add_catalyst"}` | committed |
| 4 | `{"duration_s":1800,"operation":"heat","stirring_speed_rpm":700,"target_temperature_K":350}` | committed |
| 5 | `{"instrument":"hplc","operation":"measure"}` | committed |
| 6 | `{"duration_s":7200,"operation":"heat","stirring_speed_rpm":800,"target_temperature_K":370}` | committed |
| 7 | `{"instrument":"hplc","operation":"measure"}` | committed |
| 8 | `{"duration_s":14400,"operation":"heat","stirring_speed_rpm":800,"target_temperature_K":370}` | committed |
| 9 | `{"instrument":"hplc","operation":"measure"}` | committed |
| 10 | `{"operation":"quench"}` | committed |
| 11 | `{"duration_s":3600,"operation":"distill","reflux_ratio":8,"target_temperature_K":365}` | committed |
| 12 | `{"instrument":"gc","operation":"measure"}` | committed |
| 13 | `{"duration_s":7200,"operation":"distill","reflux_ratio":10,"target_temperature_K":350}` | committed |
| 14 | `{"operation":"collect_fraction","transfer_fraction":1}` | committed |
| 15 | `{"instrument":"gc","operation":"measure"}` | committed |
| 16 | `{"operation":"terminate"}` | committed |
| 17 | `{"instrument":"final_assay","operation":"measure"}` | committed |

模型终答（保留其自述，解释须结合实际轨迹）：

Completed one vessel with explicit termination and final assay; no batch was discarded. Used 0.040 mol reagent, 40 mL acetonitrile and 0.002 mol Catalyst A. Extended heating from a 350 K setpoint to 370 K as HPLC yield estimates rose from 0.101 to 0.524, then quenched. Distilled at 365 K/reflux 8, followed by 350 K/reflux 10, and collected the available fraction. Final assay: distillate purity 0.2442 (FAIL: target ≥0.80), recovery 0.9705 (PASS: target ≥0.10), yield 0.5253, conversion 0.5188 and solvent loss 0. Native leaderboard score: 0.429684. Thus, the overall quality goal was not met despite high recovery. Used 17/72 operations and five nonfinal measurements; reported physical cost totaled 2.2237 benchmark units, with peak risk 0.3412 below the 0.65 limit. Purity remained the principal limitation; this single adaptive trajectory does not establish causal effects or an optimal recipe.

## 资源与完整性

| 流程/条件 | 过程秒 | 物理费用 | 采样升 | 非终检测量 | 模型输入/缓存/输出tokens | 精确重放 |
| --- | --- | --- | --- | --- | --- | --- |
| 反应—萃取—纯化/reference | 3073.85 | 0.6619 | 0.000600 | 3 | 0/0/0 | 15步/True |
| 反应—路径依赖结晶/reference | 6800.98 | 0.8550 | 0.000900 | 3 | 0/0/0 | 16步/True |
| 反应—分段蒸馏/reference | 5719.36 | 0.9535 | 0.001000 | 4 | 0/0/0 | 17步/True |
| 反应—萃取—纯化/reference-corrected | 3973.85 | 0.9357 | 0.001100 | 4 | 0/0/0 | 21步/True |
| 反应—萃取—纯化/agent | 22528.84 | 1.5227 | 0.001500 | 6 | 853824/789120/1326 | 22步/True |
| 反应—路径依赖结晶/agent | 0.00 | 0.1200 | 0.000000 | 0 | 未回传/未回传/未回传 | 1步/True |
| 反应—分段蒸馏/agent | 34228.93 | 2.2237 | 0.001200 | 5 | 547365/498176/1132 | 17步/True |

原纯化失败只对15条持久化前缀做重放与记账；后续dry已触发运行但发生资源预留异常，不能声称全失败轨迹已精确重放。

| 问题 | 类别/影响 | 处理与验证 |
| --- | --- | --- |
| dry固定耗时300秒未进入资源卡 | K1，执行记账缺陷；仅纯化受影响 | 原失败保留，补上时间预留后从头验证同一参考一次；保留资源强制扣账，B/C不重跑 |

逐动作时间、费用、采样与物料求和已与资源账交叉核对；具体检查及全部失败见JSON。
结晶provider中断未回传token用量，记为缺失，不按零成本处理。后端模型响应次数未完整观测，会话/进程与MCP工具次数分别报告；订阅用量无法归属到每次运行的美元金额。

## 解释边界

测量后调整、重复控制和不可逆操作可用于提出后续假说；仅凭这一轮不能归因科学信息损失或系统性失效。
新程序未改变模拟器物理定律；这是自由操作的单批试跑，完整实验矩阵仍待开发。

[实验说明](../WORK_II_ASTRA_FULL_PROCESS_TRIAL_NOTE.md) · [机器结果](work-ii-astra-full-process-20260914.json)
