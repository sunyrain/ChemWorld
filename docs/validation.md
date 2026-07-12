# 验证安装与结果

验证分成三个尺度：快速检查单条轨迹、运行开发测试、执行完整发布门禁。日常开发不必每次都跑最重
的一组，但准备发布时不能只依赖局部测试。

## 我刚跑完一条轨迹

```bash
chemworld verify --constitution --submission runs/<trajectory>.jsonl
chemworld evaluate --submission runs/<trajectory>.jsonl
```

这会检查 schema、合同、状态守恒与 replay，并从轨迹重算指标。

## 我修改了代码或文档

```bash
python -m ruff check .
python -m mypy src/chemworld
python -m pytest
python -m mkdocs build --strict
```

当前 release gate 执行 Ruff lint，但**没有自动执行 `ruff format --check`**。准备合并或发布时建议额外
运行：

```bash
python -m ruff format --check .
```

## 我要准备一个发布候选

```bash
python -m pip install -e ".[dev,docs,physchem-ref]"
python scripts/run_release_gate.py
```

完整入口串联核心 typing、pytest、严格文档构建、wheel smoke、参考验证、runtime/model 审计、环境
一致性、baseline smoke 与 benchmark bundle integrity。任一阶段失败，发布候选都不应被标为全绿。

## 物理与数值证据如何分层

1. 用解析解和守恒式检查简单极限。
2. 用单元测试固定模型行为和错误边界。
3. 用可选专业参考后端对照局部性质、动力学或传递切片。
4. 用 runtime integration 确认模型真的进入 Gym 状态转移。
5. 用冻结 trajectory 检查版本化世界律的端到端行为。

参考依赖缺失时，对应验证应显示为 skipped 或 unavailable，而不是被当作通过。

## 结果为什么能够复现

Trajectory、submission manifest 与 dataset card 会记录任务、场景、机理、世界律、runtime profile、
observation/scoring contract、依赖环境和源码摘要。`chemworld verify` 使用这些字段发现合同漂移或
轨迹修改。

发布 artifact 的完整要求见[验证结果可信度](release_integrity.md)。
