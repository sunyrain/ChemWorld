# 虚拟光谱如何生成

虚拟光谱把隐藏状态转换成 Agent 可以付费获取的部分观测。它的目标不是复刻真实谱图库，而是提供
一个足以研究测量选择、信息增益和证据使用的信号通道。

## 当前信号类型

以下是**信号概念**，不是 `measure.instrument` 可直接接收的 ID 列表。
基础 ID 是 `hplc`、`gc`、`uvvis`、`ph_meter`、`final_assay`，以及部分任务的
`particle_size`。新增 `nmr`、`ir`、`ms` 需要 composition 和任务显式开放，
以当前任务的 `env.unwrapped.action_schema("measure")` 为准。
旧谱包中的 IR/NMR/MS-like 特征与新独立仪器不同，不能仅凭视图标签判断允许的动作。

新仪器先用 `configure_instrument(instrument, scan_count, resolution_factor, dilution_factor)`
配置，再用 `measure` 采集。它们提供有限匿名校准通道、原始信号和基于信号拟合的估计，
不从分子结构预测真实谱图。未检出/饱和/不可辨识保留 null 和原因；分析秒数与反应器物理时钟分开。

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

Agent Observatory 的公开选择是 raw、unassigned、assigned，便于做谱图信息消融。具体交互见
[打开可视化实验室](interactive_task_lab.md)。

!!! warning "解释边界"
    这些曲线是状态耦合的合成观测，不是现实样品谱图、量化计算结果或仪器控制信号。
