# 虚拟光谱

虚拟光谱为 agent 提供有限、带噪、可计费的观测通道。它服务 benchmark 和教学，不追求
数据库级真实谱图预测。

## 信号类型

当前可表达的信号包括：

- UV-vis absorbance；
- HPLC/GC retention summary；
- IR/NMR-like feature peaks；
- final assay；
- phase or impurity probe。

## 信号位置

光谱信号由 instrument service 生成，进入 observation 或 `info` 中的 instrument record。
隐藏 species amount 不应直接暴露给 agent，而应通过信号、噪声和校准关系间接反映。

## 设计边界

虚拟光谱的目标是让 agent 学会：

- 选择何时测量；
- 选择哪种仪器；
- 权衡成本、噪声和信息增益；
- 用读数改进后续操作。

它不是真实谱图数据库、量化计算工具或实验仪器控制层。
