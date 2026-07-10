# Official Seed Suite

ChemWorld 的正式评测不应临时挑 seed。core 和 serious 套件使用公开、冻结的 seed plan，所有
baseline、submission 示例和本地教师端评测都应引用同一份计划。

## 查看 seed suite

```bash
chemworld seeds show
```

查看全部已注册任务：

```bash
chemworld seeds show --all-tasks
```

查看指定任务：

```bash
chemworld seeds show --tasks reaction-to-assay reaction-to-purification
```

输出字段：

| 字段 | 含义 |
| --- | --- |
| `schema_version` | 当前为 `chemworld-seed-suite-0.1` |
| `suite_id` | 当前 suite 标识 |
| `task_seed_plan` | runner 实际使用的 seed 列表 |
| `published_seed_plan` | 可公开声明的 seed 列表 |
| `entries` | 每个 task 的 split、role、seed 和 hidden-eval policy |
| `private_eval_salt_policy` | private-eval salt 和隐藏 seed 的公开政策 |

## Core 任务

| Task | Split | Public seeds |
| --- | --- | --- |
| `reaction-to-assay` | `public-dev` | `0` |
| `reaction-to-purification` | `public-test` | `0, 1, 2, 3, 4` |
| `partition-discovery` | `public-test` | `0, 1, 2` |

## Split 语义

| Split | 用途 | Seed 政策 |
| --- | --- | --- |
| `public-dev` | 开发、教学、smoke test | seed 公开，可用于调试 |
| `public-test` | 正式公开 benchmark 报告 | seed 公开且固定 |
| `private-eval` | 维护者侧 leaderboard | hidden seeds 由维护者控制 |

## Private-Eval Salt Policy

private eval 使用环境变量：

```bash
CHEMWORLD_PRIVATE_EVAL_SALT=<secret>
```

规则：

- raw salt 永不发布；
- public repo 只暴露本地 placeholder seeds；
- 没有 `CHEMWORLD_PRIVATE_EVAL_SALT` 时，`private-eval` 只是 public placeholder，不代表正式榜单；
- 维护者发布 signed result artifact，包含 salt hash、commit、task、seed policy 和聚合结果；
- 第三方提交包不能直接访问 hidden salt 或 hidden scenario 参数。

## CLI 加载

以下命令在指定 `--task` 时会读取 official seed suite：

```bash
chemworld suite --task reaction-to-purification --agent tool_using_llm_stub
chemworld baselines report --tasks reaction-to-purification --agents tool_using_llm_stub
```

如果显式传入 `--seeds`，则进入 smoke/debug override；正式报告应说明这一点。
