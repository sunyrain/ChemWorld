# 仪器合同

仪器合同定义 agent 能从世界中观测到什么。ChemWorld 的观测不应直接泄露 hidden state，
而应通过带噪、有限预算、任务相关的 instrument channel 暴露。

## 典型仪器

- `final_assay`：终点评测读数。
- `quick_assay`：低成本但噪声较高的过程读数。
- `spectroscopy`：虚拟光谱或特征峰。
- `phase_probe`：相组成或分配相关观测。
- `safety_monitor`：安全风险摘要。

## 合同字段

仪器读数应说明：

- instrument name；
- measured quantity；
- unit；
- noise model；
- cost；
- time/budget impact；
- visibility boundary。

## 设计边界

虚拟仪器服务 benchmark 和教学，不等同真实仪器控制。若未来接入真实设备，应把设备
adapter、校准、权限和安全审查与当前虚拟 instrument contract 分开处理。
