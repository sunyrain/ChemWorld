# G2 v0.6 前瞻确证执行日志

## `monitor-001`：中期监控输出越界

- 发生时间：2026-08-02 14:31（Asia/Shanghai）
- 发现方式：首个 time block 完成后定位一个右删失 cell 的基础设施错误。
- 原因：监控命令对 cell 目录执行了过宽的文本检索；由于 trajectory JSONL
  的单行记录包含大量字段，输出意外包含该右删失单臂 campaign 的局部公开历史分数。
- 暴露范围：`cell-001`；一个未完成、已永久右删失的 nominal 单臂 campaign。
  没有查看任何完整 pair 的 nominal-minus-opaque 差异，没有查看其他 cell 的结果，
  该 cell 按冻结规则不会进入 complete-pair 主分析。
- 决策影响：无。样本量、停止规则、world、schedule、arm、资源卡、主指标、
  实质阈值、覆盖门槛、分析代码和正式运行均未改变；该局部信息不用于任何分析、
  实验扩展或论文结论。
- 修正：停止对运行目录做通配文本搜索；新增
  `paper/tools/monitor_g2_confirmatory_status.py`，后续只通过字段 allowlist 输出状态、
  基础设施失败类别和接受操作数，禁止读取 trajectory、score、outcome 和 arm contrast。
- 推断边界：执行本身仍完全遵循冻结方案，主推断仍只在全部 cell 终态后对完整 pair
  运行预注册分析；最终工件不再表述为“分析者全程未见任何单臂局部分数”，而准确记录
  此次不改变决策的监控偏差。

## `owner-stop-001`：按第一版概念论文范围停止扩展矩阵

- 停止时间：2026-08-02 14:37（Asia/Shanghai）。
- 决策：第一版论文以既有五 world 自主实验作为主要 G2 能力与现象证据，不再为
  16-world 总体确证矩阵继续消耗 provider 资源。
- 决策依据：论文范围与资源配置；停止前没有查看任何完整 pair 的分数或 arm contrast。
- 停止时正式 manifest：7 completed cells、1 right-censored cell、3 complete pair audits、
  152 pending cells。第二个 time block 的 `cell-009/011/013/015` 在运行中被终止，
  其目录原样保留，不覆盖、不补跑、不纳入正式推断。
- 数据定位：该矩阵只作为扩展性和执行记录，不表述为完成的 prospective confirmation。
  运行根目录写入 `OWNER_STOP.json`；除非先做专门的 partial-cell 审计，否则禁止 resume。
