# 通用环境与虚实配对契约

本应用先定义通用场景环境，不绑定某一种实验。实验本身由 ChemWorld Core 执行；此处的 Environment
负责场景对象、机器人物流、教育演示设备与只读反馈。启动方法见 [README](README.md)。

## 环境定义

| 对象 | 定义与行为 |
| --- | --- |
| 空间 | `environment.json`：米制、右手 `lab_world` 坐标系，边界、障碍、停靠点与交接台面 |
| 资产 | `catalog.py`：36 个可寻址设备、容器、样品与机器人，含能力、尺寸和支撑关系 |
| 样品 | `sample_tube_01`：密封状态、体积/质量/内容物、台面或机器人持有关系；搬运不改变库存 |
| 动作 | 导航、抓取、放置、设备参数与动作、转移；前置条件、资源占用和稳定命令 ID |
| 任务 | 1–50 步顺序计划；单步失败停止后续步骤 |
| 生命周期 | accepted/running → succeeded/failed/cancelled/interrupted；服务重启中断未完成动作 |
| 反馈 | binding ID、物理标识、来源与接收时间、序列、单位、质量、标定版本 |
| 监督 | 目标、演示模拟值和观测值分开；识别偏差、陈旧及低质量数据 |
| 记录 | 本地状态、命令、任务、样品交接事件和追加事件日志；全部运行输出忽略于 Git |

`asset.action` 成功表示底层接口动作已应用，例如开始加热，不表示温度已达标。导航和抓放则在完整虚拟
运动结束后成功。具体实验还需要显式等待条件和结果判据。超时后查询原 ID，不要生成新 ID 重复执行。
急停取消当前虚拟动作和任务；解除后不自动重放，夹持中的样品保持夹持。

## SDK 与 HTTP

本地默认地址 `http://127.0.0.1:8877`，完整路由由 `GET /openapi.json` 提供。

```python
from apps.blender_lab.environment_client import EnvironmentClient

env = EnvironmentClient()
state = env.observe()
job = env.step("robot.navigate", {"station": "preparation"},
               command_id="run001-go-preparation",
               expected_revision=state["simulation"]["revision"])
result = env.wait(job["id"])
assert result["status"] == "succeeded", result
# 重试使用相同 command_id 和完全相同的参数。
```

以下路径都以前缀 `/api/v1/environment` 开始：

| 路径 | 用途 |
| --- | --- |
| `GET /`（允许省略末尾斜杠） | 环境定义和能力 |
| `GET /state` | 演示模拟状态、持有关系、命令、任务和监督 |
| `POST /commands`；`GET /commands/{id}` | 提交、查询动作 |
| `POST /tasks`；`GET /tasks/{id}` | 通用顺序计划 |
| `POST /demo/transport`，请求体 `{}` | 前往样品 → 抓取 → 前往另一交接位 → 放置 → 返回 |
| `POST /bindings`；`GET /bindings` | 声明虚实对象配对 |
| `POST /observations` | 标准化观测 |
| `GET /supervision` | 比较场景模拟值与观测值，输出只读建议 |
| `GET /events` | 最近 500 条环境事件 |

命令 `mode` 仅支持 `simulation`，真实硬件输出被拒绝。`expected_revision` 是模拟状态版本。
Core 的公开展示另用 `/api/v1/chemworld/frame`；这两类数据不会相互覆盖。

## 验证反馈管线

```python
from apps.blender_lab.adapters import MockTemperatureAdapter

mock = MockTemperatureAdapter(env, offset=8)
mock.bind()
mock.publish_once()
print(env.supervision())
```

该适配器明确标记为合成源。8°C 偏差超过默认 2°C 容差，停止发布超过 15 秒后变为陈旧。
监督比较的是 **ChemLab 场景演示值**，不读取 Core 隐藏状态，也不把反馈自动注入 Core 测量。

## 与真实实验室配对的后续步骤

1. **资产身份**：为虚拟资产匹配现场序列号或资产标签，建立不可变 `binding_id`。当前来源由调用者声明，
   还没有设备身份认证；改变标定配置应建立新的配对记录。
2. **空间与测量标定**：测量基准点、台面、机器人基座和工具中心，建立真实坐标到 `lab_world` 的变换，
   同时校准传感器。当前只有名义模型坐标，`calibration_id` 是 `declared_not_verified` 版本标签，
   没有空间变换求解、实际位姿观测或相机标定。
3. **只读观测**：设备驱动转换为统一 envelope。支持温度 `degC`、转速 `rpm`、体积 `ml`、质量 `g`；
   携带 UTC 时间、单调序列、质量与标定版本。错单位、乱序和标定不匹配会被拒绝。缺少观测不代表一致。
4. **影子运行**：比较实际状态与模型进度，保留目标、回执和测量。当前监督只给建议，不会自动更新模型、
   暂停真实设备或调节控制器。绑定 Core 前还需明确样本身份、量纲转换和公开测量合同。
5. **受限控制**：在驱动、控制权、独立急停与联锁、运动标定和现场验证完成后，再开放具体设备的有限控制。
   每次决策关联任务、命令、实际回执、观测与标定版本。

`adapters.py` 的 `DeviceAdapter` 是扩展边界，mock 可以运行。SiLA 2、OPC UA、ROS 2 是明确抛出
未实现错误的占位，没有真实硬件驱动。

导航采用平面障碍膨胀和 A*，行进时复查障碍。机械臂是几何运动与距离检查，没有接触动力学、完整六轴
碰撞或真实抓取控制。当前搬运仅开放有明确抓取轮廓的密封样品管，其身份尚未对应 Core 的取样记录。

本机接口没有远程鉴权，长期部署还需要事件归档和容量管理。开发测试覆盖与运行命令见 [README](README.md)；
软件测试和动画演示不构成真实实验室控制或迁移有效性的验证。
