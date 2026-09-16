# Astra medium：修正合同后的单次开发实验

状态：development_stopped；仅一个反应—结晶四格组，每条件一次。

模型 0/20 完成；物理 0/164 完成；失败 1，未启动 163；重放通过 1。

评分为基于公开测量的质量加权回收估计/过程小时，扣除晶种回收；旧score只作诊断。
不是精确摩尔产率。学习/留出各6个查询；无独立复现，不作系统性失效推断。

| 条件 | 留出反应MAE | 留出回收MAE | 留出纯度MAE | R1C2效用/小时 | R2C1效用/小时 |
| --- | --- | --- | --- | --- | --- |

## 支持域与失败

近支持使用事前固定的公开5维凸包距离≤0.05；不等于完整隐状态支持。
- 停止原因：ContractError: qualification/R1C1/0: {'type': 'ContractError', 'message': 'declared and actual quench temperatures differ'}
- qualification/R1C1/0：{'message': 'declared and actual quench temperatures differ', 'type': 'ContractError'}

逐批资源、预测真值/误差、部署参数及参考结果见同名JSON；原始provider及私有初始化留在ignored运行目录。

报告token用量：`{}`。美元费用未估算。
