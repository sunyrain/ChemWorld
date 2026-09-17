# Experiment 1 RX-S structural repair manifest v1.1.0

状态：**冻结用于 provider-free development qualification；不授权 Participant 或正式 benchmark。**

日期：2026-09-18。本文件在任何 RX-W01--W05 v1.1.0 结果生成前冻结。

## 1. 被取代的问题

RX-S v1.0.1 的 `deactivating_baseline` vs `stable_catalyst` fork 可执行且可 replay，
但五个正式 Worlds 的公开效应均明显低于已冻结门槛。旧结果保留，不降低阈值，也不通过
放大失活常数来追求 PASS。

## 2. 校准选择证据

预注册 authoring note 为 `STRUCTURAL_REDESIGN_AUTHORING_NOTE_V1_1_0.md`。选择只使用
非 benchmark seeds 201、202、203；243/243 次执行 exact replay。

- `stable_catalyst`：0/3 calibration Worlds 通过；
- `reversible_target_pathway`：3/3 calibration Worlds 通过；
- 每个 calibration World 均有 3 个 resolving public metrics；
- 跨 Worlds 的最小 maximum public effect 为 `0.19999206269047642`；
- calibration summary SHA-256：
  `b404f7416218f3a20b592c2e16eb411a346fc96de18d706d0b14222a8689bf63`。

因此 v1.1.0 按预注册选择规则唯一冻结 `reversible_target_pathway`，不再比较或挑选
RX-W01--W05 的候选。

## 3. 正式 development qualification 设计

- parent：`deactivating_baseline`；
- child：`reversible_target_pathway`；
- child 只增加显式 `P -> A` reverse channel；severity `0.8`；full-severity reverse
  rate constant `0.000625 s^-1`；
- 五个 Worlds、3 x 3 x 3 public grid、温度/时长/催化剂剂量、公开 endpoints、
  effect gates、最小 safe/completed pairs、空间分离规则和 Participant 最小预算均保持
  v1.0.1 不变；
- paired laws 共用 action plan 和 keyed-noise coordinate；
- v1.1.0 使用新的 observation-noise namespace；
- 每 World 54 次，共 270 次；随后在独立 write-once 目录完整 replay 同一冻结 denominator。

## 4. Gate 解释

Q1--Q8 名称不变。Q7 的 private-physics binding 从“删除一个失活反应”更新为：child
恰好增加一个 `family_reverse_channel`，方向为 `P -> A`，mechanism hash 改变、绑定确定且
与执行 receipt 一致。Q5 仍要求至少两个 public metrics 分辨并出现 duration-accumulation
signature；Q6 仍要求分离支持点覆盖至少两个 catalyst doses；所有阈值保持不变。

科学失败会如实冻结并继续 campaign。任何结果均不代表 Participant 表现；provider calls
固定为 0。
