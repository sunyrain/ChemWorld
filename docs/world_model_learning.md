# World Model 学习

World-model learning 任务关注 agent 是否能从交互数据中学习环境动态、观测模型和评分
结构。它是 ChemWorld 从 recipe benchmark 走向 agentic science environment 的关键。

## 学习者可用数据

可提供的数据包括：

- trajectory；
- action；
- observation；
- reward；
- constraint flags；
- instrument readings；
- task metadata；
- public scenario metadata。

隐藏 state、oracle mechanism 参数和 private eval scenario 不应直接提供。

## Surrogate 接口

学习到的 surrogate model 可以用于：

- 预测下一个 observation；
- 估计最终得分；
- 选择信息增益最高的 measurement；
- 规划下一批 experiment；
- 在低成本模拟中预筛 recipe。

## 评测重点

不要只看 prediction loss。还应评估 surrogate 是否能帮助 agent 在新 scenario 中获得更好
的交互决策。
