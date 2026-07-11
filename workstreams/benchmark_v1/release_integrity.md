# Benchmark release integrity

`check_frozen_benchmark.py` 必须从公开 bundle 重新验证事实，不能把
`benchmark_ready_count` 或 `validated=true` 当成事实来源。

当前存在两种明确模式：

- 默认 strict frozen：校验结构、内嵌 SHA-256、当前 task contract、source commit、clean tree、
  `release_status=frozen` 和完整 trajectory index/archive；任一失配即失败；
- `--allow-candidate`：只允许 task/commit/trajectory freshness 暂未完成，且输出
  `release_claim_allowed=false`；任何文件篡改、矩阵缺失或摘要失配仍然失败。

本地开发门禁在 WF-110 重冻结前使用 candidate 模式，并在 summary 中写入
`benchmark_mode=candidate`、`release_claim_ready=false`。论文、tag 或正式发布必须使用：

```powershell
.\.venv\Scripts\python.exe scripts\run_release_gate.py --require-frozen-benchmark
```

严格模式未通过时，不能通过改名、忽略返回码或手工改 JSON 生成正式声明。
