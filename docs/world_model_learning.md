# 学习 World Model

World model 让 Agent 不只记住“哪个配方分高”，而是从交互历史中学习：执行一个操作后会看到什么，
哪些测量值得做，以及当前局部规律能否迁移到新场景。

## 可以使用的数据

学习器可以读取 trajectory 中的公开信息：

- Action、observation 与 reward；
- constraint flags 和 instrument readings；
- 公开的任务、场景与预算元数据；
- Agent 自己的历史决策和测量结果。

隐藏 state、oracle 机理参数和 private-eval 场景不属于训练输入。

## 一个模型可以帮助什么

| 能力 | 典型用途 |
| --- | --- |
| 下一步观测预测 | 判断某个操作会带来什么可见变化 |
| 最终结果估计 | 在真实执行前筛掉明显较差的 recipe |
| 不确定性估计 | 选择最有信息量的测量或实验 |
| 局部响应面 | 支持 BO、主动学习和 campaign 规划 |
| 状态表示学习 | 把长轨迹压缩成可用于决策的实验记忆 |

## 如何评价

prediction loss 只是起点。更有用的问题是：

1. 模型能否在未见 scenario 上保持校准？
2. 不确定性是否真的帮助 Agent 选择实验？
3. 使用该模型后，固定预算下的最终决策是否更好？
4. 模型失败时，Agent 是否能识别并恢复？

因此，world model 应同时报告预测质量、决策收益、资源成本和跨世界稳定性，而不是只给一张训练
loss 曲线。数据导出方法见[导出与使用数据集](dataset_layer.md)。
