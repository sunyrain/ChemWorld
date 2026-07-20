# ChemWorld 研究任务 Demo

这组 notebook 一一覆盖六个 serious research tasks。它们展示的是环境提供的隐藏世界、干预和公开反馈，
不包含也不假设任何特定 Agent 训练算法。

| Notebook | Task | 主要展示 |
| --- | --- | --- |
| `01_partition_discovery.ipynb` | `partition-discovery` | 分配构成律、相条件干预和跨世界响应 |
| `02_reaction_crystallization.ipynb` | `reaction-to-crystallization` | 反应动力学如何传播到结晶产率、纯度和粒度 |
| `03_reaction_distillation.ipynb` | `reaction-to-distillation` | 反应网络与蒸馏切割的耦合反馈 |
| `04_flow_reaction.ipynb` | `flow-reaction-optimization` | 流量、停留时间、温度与隐藏速率律 |
| `05_electrochemical_conversion.ipynb` | `electrochemical-conversion` | 诊断反馈、设定值调整与电化学构成律 |
| `06_equilibrium_characterization.ipynb` | `equilibrium-characterization` | 浓度探针、pH/UV-vis 反馈与非理想平衡 |

每份 notebook 都包含：

1. 公开任务合同；
2. 由公开 recipe adapter 生成的候选干预；
3. 三组条件的反馈比较；
4. 一次完整运行的测量轨迹；
5. 同一干预在两个 opaque worlds 下的配对比较；
6. 留给 Agent/world-model 方法回答的预测与下一实验问题。

运行前安装项目及 notebook 依赖：

```bash
python -m pip install -e ".[notebooks]"
```

这些 Demo 使用的 `mechanism_family` 配对是教学控制，不是正式 benchmark 结果。代码不会读取 hidden
state、隐藏参数或机制真值；`World A`/`World B` 只是 notebook 展示标签。
