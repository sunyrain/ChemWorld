# C-S structural redesign result v1.1.0

状态：**failed-development；未进入正式 W01--W05 qualification。**

## 冻结设计与平台恢复

候选比较在非 benchmark seeds 301--303 上执行 `seed_growth_parent` 与
`primary_nucleation_dominated`。第一次 corrected run（attempt2）因 SSH transport 在
24/48 时中断，未生成 summary；其原始 receipts 保留但不参与选择。按照 recovery note，
attempt3 在新 write-once 目录从 execution 0 完整重跑。

## 完整结果

- planned/completed/exact replay：48/48/48；
- provider calls：0；
- private fork 在三个 Worlds 均确定、改变 world hash，且 nucleation 与 growth 反向移动；
- public effect、分离支持点与非标量 interaction 在三个 Worlds 均通过；
- CAL01、CAL02 未改变预注册的 yield-optimal task decision；CAL03 改变 seed 与 duration；
- 全门禁通过 Worlds：1/3；
- `selected_candidate = null`；
- summary SHA-256：
  `13e07aac027b7a1a2135bde286694b949ae97930d28dd0795377d88adec2b401`。

选择规则要求候选在 3/3 calibration Worlds 全部通过，因此不能只凭公开 endpoint 可辨识
就进入正式 benchmark。未降低 `0.03` effect/interaction gate，未删除
`task_decision_changes`，未更换 calibration seeds，也未运行 C-W01--W05 的结构修复版本。

C-S 维持 `failed-development`。本 campaign 不启动事后第二轮调参；若未来提出第二个
科学问题，必须另写预注册 authoring note，并继续受每 locus 最多两次 redesign 的限制。

Participant execution was not started.
