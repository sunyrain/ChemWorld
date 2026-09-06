# Blender 实验室与自动化助手

Blender 实验室已经作为可选本地应用接入 ChemWorld。现有设备模型、移动机械臂、样品搬运和通用环境接口
位于 `apps/blender_lab/`；公开状态适配器位于 `chemworld.interfaces.blender`。

## 整个流程接在哪里

| 层 | 职责与入口 |
| --- | --- |
| ChemWorld Core | 执行 `reset/step`，计算测量、预算、奖励，保留精确回放 |
| Task Lab / Python | Student、LLM、经典 Agent 共用可选 `BlenderObserver`；自定义工作流也可直接包装环境 |
| Blender 接口 | 通过公开 `observation_view` 获取状态，只把已经观测的值显示在三维场景中 |
| 场景 Environment | 定义坐标、资产能力、样品持有关系、导航和抓放任务；由显式物流指令驱动 |
| 反馈适配器 | 接收带来源、时间、单位、质量和标定版本的观测，进行只读偏差监督 |

```text
人 / Agent → ChemWorld 动作 → 公开观测 → Blender 三维展示
                      └→ 原始轨迹 → 精确回放与评测
工作流 → 显式搬运任务 → 场景 Environment → 移动助手
设备适配器 → 标准化观测 → 只读监督 → 工作流决策
```

原场景 **ChemLab** 面板里的教育演示库存与合成测量独立于 Core。当前密封样品管尚未绑定到 Core 的具体
样本身份；运行示例会在取样后显式等待搬运完成，再继续检测。Task Lab 的一般动作仅同步公开展示。
UV–Vis、FTIR、pH 有对应设备模型，其余仪器显示文字报告。

## 本地启动

在仓库根目录执行，Blender 路径改成自己的安装位置：

```powershell
uv sync --extra dev --python 3.12
uv run --no-sync python -m apps.blender_lab --blender "C:\path\to\blender.exe"
$env:CHEMWORLD_BLENDER_URL = "http://127.0.0.1:8877"
uv run --no-sync python -m apps.task_lab.server --port 8876
```

Blender 服务默认端口 **8877**，Task Lab 使用 **8876**。场景与应用需要源代码仓库；Python 观察器可随
`chemworld` 包安装。启动器负责打开模型和连接服务，直接双击模型不一定会启动接口。

在 Blender 的 3D 视图按 **N**，**ChemWorld** 页显示任务、步骤、剩余预算和已测量结果，**自动化** 页
可以运行样品搬运、跟随机器人或急停。搬运由实时服务驱动，不需要按时间轴播放。

运行含搬运的完整示例，并核验原生 ChemWorld 轨迹：

```powershell
uv run --no-sync python examples/demo_blender_workflow.py --output runs/blender_lab/my-demo/trajectory.jsonl
uv run --no-sync chemworld verify --constitution --submission runs/blender_lab/my-demo/trajectory.jsonl
```

每次运行使用新输出路径。示例保留失败轨迹，拒绝覆盖已有文件。一个 Blender 服务同时接收一个 Core
会话；多会话请使用独立端口。关闭会话会释放占用，并保留最后画面。

## 接口边界和真实实验室配对

观察器不读取隐藏状态，未测量值保持 `null`。Blender 断线不会重放已执行动作，也不会改变返回值和预算；
失败记录在观察器的 `projection_error`。原有评测默认不启用 Blender。

后续配对按“资产身份 → 空间和传感器标定 → 只读观测 → 影子运行 → 经验证的受限控制”推进。
当前已有配对和观测格式、命令生命周期、样品交接记录、偏差/陈旧/低质量判别；监督比较的是场景演示值，
不会把真实或合成观测自动注入 Core。需要进一步明确实验类型、实际样本身份与公开测量合同。

当前没有真实硬件驱动、真实运动标定、完整机械臂碰撞或动力学。标定标签属于声明，SiLA 2、OPC UA、
ROS 2 仍为占位适配器。这次接入验证的是软件接口和回放一致性，不构成物理迁移证据。

启动、SDK、HTTP 接口和开发验证详见
[应用说明](https://github.com/sunyrain/ChemWorld/tree/main/apps/blender_lab)及
[Environment 契约](https://github.com/sunyrain/ChemWorld/blob/main/apps/blender_lab/ENVIRONMENT.md)。
真实有效性的验证路线见[从虚拟世界到真实实验](real_world_bridge.md)。
