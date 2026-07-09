# 提交包

提交包定义 agent 如何参加本地评测或未来 hosted leaderboard。

## 最小结构

```text
submission/
├── README.md
├── agent.py
├── requirements.txt
├── config.json
└── manifest.json
```

## Agent 入口

Agent 应暴露一个清晰入口：接收 observation，返回 action。评测端负责创建环境、设置
seed、执行 step、保存轨迹和评分。

## Manifest

`manifest.json` 应包含：

- 提交名称；
- 版本；
- 依赖；
- 允许资源；
- 随机性说明；
- 作者声明；
- 适用任务。

## 运行限制

托管评测应限制时间、内存、网络和文件系统访问。第三方 agent 不应接触 hidden scenario
或评测答案。
