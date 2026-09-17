# RX-S v1.1.0 qualification platform recovery 1

状态：**传输加固重启记录；不是科学 qualification 结果。**

日期：2026-09-18。

RX-S v1.1.0 primary attempt 1 写入
`runs/development/experiment-1-rx-s-v1.1.0-primary-4b7ca63`。该进程通过依附 SSH 的
长连接启动；同一 campaign 的 C-S 与 FL 长进程已出现 SSH 传输结束后远端子进程被终止、
控制会话返回 255 且无完整尾部摘要的现象。为避免在 270-unit denominator 中途发生同类
平台中断，operator 在 attempt 1 完成 RX-W01 和 RX-W02 的部分 receipts 后主动终止该
transport-bound 进程。

attempt 1 的全部 receipts 和 RX-W01 world report 原样保留，不进入 composite registry，
不据此修改候选、World、阈值或 protocol。恢复在新的 write-once `primary-attempt2` 目录
从 execution 0 完整重跑冻结的 270 units；代码与 contract commit 仍为 `4b7ca63`，只是
进程改为服务器持久执行并将 stdout/stderr 写入独立日志。

只有 attempt 2 形成完整五 World summary 后，才允许登记 RX-S v1.1.0 primary 结果。
