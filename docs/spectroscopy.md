# 虚拟光谱如何生成

虚拟光谱把隐藏状态转换成 Agent 可以付费获取的部分观测。它的目标不是复刻真实谱图库，而是提供
一个足以研究测量选择、信息增益和证据使用的信号通道。

## 当前信号类型

- HPLC / GC retention curve 与峰摘要；
- UV–Vis absorbance；
- IR / NMR-like feature peaks；
- MS-like 特征；
- phase、impurity 与 final-assay 读数。

信号由 instrument service 根据当前状态生成，并带有公开的噪声、成本、样品消耗与披露级别。隐藏
物种量不会直接进入 Agent 输入，而是通过曲线、峰和处理后估计间接体现。

## Agent 可以研究什么

1. 什么时候值得测量；
2. 选择哪一种仪器；
3. 如何在成本、噪声和信息增益间取舍；
4. 新读数是否真的改变后续操作。

Agent Observatory 支持 raw、unassigned、assigned 与 masked 条件，便于做谱图信息消融。具体交互见
[打开可视化实验室](interactive_task_lab.md)。

!!! warning "解释边界"
    这些曲线是状态耦合的合成观测，不是现实样品谱图、量化计算结果或仪器控制信号。
