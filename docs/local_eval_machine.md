# 运行本地评测机

本地评测机让教师或维护者在一台机器上走完“接收提交—运行私有环境—回放验证—发布汇总”的流程，
不依赖托管服务。它适合课程和可信代码，也是未来 hosted leaderboard 的最小原型。

当前实现位于 `local_eval_server/`，核心入口是：

```bash
python local_eval_server/teacher_side/eval_machine.py
```

## 教师端与学生端怎样分工

```text
local_eval_server/
├── teacher_side/
│   ├── eval_machine.py
│   └── eval_config.demo.json
└── student_side/
    ├── student_agent_runtime.py
    └── team_alpha_submission/
        ├── agent.py
        ├── manifest.json
        ├── requirements.txt
        └── README.md
```

教师端拥有 ChemWorld 环境、private salt、seeds、trajectory、verify、evaluate、leaderboard
和发布目录。学生端只暴露一个 JSONL agent runtime：教师端发送 sanitized task info 和
history，学生端返回下一步 action。

学生端不创建 `gym.make("ChemWorld", ...)`，也不直接调用 `env.step()`。

## 一条命令跑完整演示

```bash
python local_eval_server/teacher_side/eval_machine.py \
  --workspace runs/local_eval_machine \
  demo \
  --tasks reaction-to-assay \
  --seeds 0
```

这个命令会初始化 demo workspace、接收一个模拟学生提交、运行教师端环境、保存轨迹、
重放验证、计算指标并发布 leaderboard 与 summary。

## 在课程或内部评测中分步运行

推荐在正式课程或内部评测中使用分步命令：

```bash
python local_eval_server/teacher_side/eval_machine.py \
  --workspace runs/local_eval_machine \
  init-demo

python local_eval_server/teacher_side/eval_machine.py \
  --workspace runs/local_eval_machine \
  validate

python local_eval_server/teacher_side/eval_machine.py \
  --workspace runs/local_eval_machine \
  run \
  --tasks reaction-to-assay \
  --seeds 0

python local_eval_server/teacher_side/eval_machine.py \
  --workspace runs/local_eval_machine \
  summarize \
  --run-id demo_eval
```

对应含义：

| 步骤 | 命令 | 产物 |
| --- | --- | --- |
| 初始化 | `init-demo` | `teacher_private/eval_config.json` 和 `submissions/incoming/team_alpha_submission/` |
| 接收提交 | `validate` | 校验 manifest、entrypoint、依赖声明；合法提交移动到 `submissions/accepted/` |
| 教师端运行 | `run` | `runs/<run_id>/<team>/trajectories/`、`results/`、`verify/`、`logs/` |
| 汇总发布 | `summarize` | `published/<run_id>_leaderboard.json`、`.csv`、`<run_id>_summary.json` |

`run` 阶段会调用正式的 `chemworld.eval.verify_records`，不是本地简化 verifier。因此
本地评测机与 benchmark replay gate 使用同一套重放检查。

## 去哪里找结果

```text
runs/local_eval_machine/
├── teacher_private/
│   └── eval_config.json
├── submissions/
│   ├── incoming/
│   ├── accepted/team_alpha/
│   └── rejected/
├── runs/demo_eval/team_alpha/
│   ├── trajectories/reaction-to-assay_seed0.jsonl
│   ├── results/reaction-to-assay_seed0.json
│   ├── verify/reaction-to-assay_seed0.json
│   └── logs/
└── published/
    ├── demo_eval_leaderboard.csv
    ├── demo_eval_leaderboard.json
    └── demo_eval_summary.json
```

`summary.json` 至少包含：

```json
{
  "result_count": 1,
  "verification_count": 1,
  "verified_count": 1,
  "failed_verifications": [],
  "leaderboard_json": ".../demo_eval_leaderboard.json"
}
```

## 先理解它的安全边界

当前实现是 `trusted-local-subprocess`，只允许运行教师信任的代码；它是本机模拟
Docker，而不是强隔离沙箱：

- 教师端负责 `env.reset/env.step`；
- 学生端只通过 stdin/stdout JSONL 协议收发消息；
- 教师端使用环境变量白名单，不向学生进程继承任意宿主变量；
- manifest 的 `team_id`、entrypoint 和依赖路径会经过字符集与目录边界校验；
- 学生端收到的 `task_info` 和 `info` 会被清理，避免直接暴露 private world 信息；
- 每次学生响应都有 timeout。

不得使用该模式直接运行不可信第三方提交。真实第三方评测必须使用独立容器或沙箱，
并配置只读挂载、网络禁用、环境白名单、CPU/内存/PID 限制和低权限用户。仅在 manifest
中声明 `allowed_network=false` 不构成网络隔离。

## 当前有哪些自动测试

测试 `tests/test_local_eval_machine.py` 覆盖：

- 一条命令 demo；
- 分步 `init-demo -> validate -> run -> summarize`；
- trajectory、result、verify、leaderboard 和 summary 产物存在；
- verify JSON 中 `verified == true`。
