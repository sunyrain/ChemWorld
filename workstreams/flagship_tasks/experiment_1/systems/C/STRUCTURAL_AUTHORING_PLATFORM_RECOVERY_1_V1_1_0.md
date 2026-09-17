# C-S v1.1.0 structural authoring platform recovery 1

状态：**平台中断记录；不是科学 qualification 结果。**

日期：2026-09-18。

冻结设计 `STRUCTURAL_REDESIGN_AUTHORING_NOTE_V1_1_0.md` 的 corrected run 写入
`runs/development/experiment-1-c-s-authoring-v1.1.0-0a64545-attempt2`。远端执行进程在
完成 24/48 receipts 后消失，SSH 控制会话最终返回 255；目录中只有 CAL01 的完整
analysis 和 CAL02 的前 8 个 receipts，没有 campaign `summary.json`。因此该 attempt
不具备固定 denominator，不得用于 candidate selection 或 benchmark registry。

已完成 receipts 与轨迹原样保留，不覆盖、不删除。恢复动作不修改代码、World seeds、
public grid、private fork、effect gate、选择规则或 observation-noise namespace；在新的
write-once `attempt3` 目录从 execution 0 完整重跑 48 个 frozen calibration units。长任务
改由服务器持久进程执行，stdout/stderr 写入独立日志，避免 SSH transport 中断向子进程
传播 SIGHUP。

只有 attempt3 产生完整 48/48、exact replay 计数和最终 summary 后，才允许按预注册规则
选择或拒绝候选。
