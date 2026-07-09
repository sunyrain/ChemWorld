# 路线图

本路线图按发布优先级组织，而不是按理想研究愿景展开。

## P0：当前预发布收束

- 中文化 `site/` 发布站点。
- 固定首页、导航、任务卡和 release checklist。
- 确保 `python -m mkdocs build --strict` 通过。
- 确保环境自洽性审计通过。
- 对 `reward=0`、precondition 和 phase workflow 的常见问题补文档。

## P1：Benchmark 合同加固

- 冻结 action schema、observation schema 和 task cards。
- 补全 baseline table 和 trajectory manifest。
- 明确每个任务的 maturity、budget、metrics 和 failure flags。
- 建立最小 submission bundle。

## P2：数据与 Agent 研究层

- 接近 Minari 风格的数据集打包。
- 增加 rule baseline、optimizer baseline 和 tool-agent baseline。
- 增加 world-model learning 接口。
- 建立本地 leaderboard prototype。

## P3：专业物理深化

- 逐步强化物性、相平衡、反应网络、单元操作和仪器模型。
- 引入参考 backend 校准，但保持默认环境轻量。
- 所有专业模块必须携带 maturity metadata。

## P4：托管评测

- 隔离执行第三方提交。
- 隐藏 evaluation split。
- 自动生成 score report、failure report 和公开榜单。
