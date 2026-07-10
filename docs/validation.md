# 验证与质量保证

ChemWorld 的发布质量由可执行门禁保证，而不是由文档中的人工状态声明保证。

## 完整发布门禁

安装完整依赖后运行：

```bash
python -m pip install -e ".[dev,docs,physchem-ref]"
python scripts/run_release_gate.py
```

该入口依次检查：

- Ruff lint 与源码格式；
- `src/chemworld` 全量 mypy 类型检查；
- pytest 单元、集成、冻结轨迹和参考后端测试；
- MkDocs strict build 与站内链接；
- 所有注册任务的环境自洽性、replay、谱图、操作合法性和 constitution；
- baseline 与发布 artifact smoke tests。

任一阶段失败都会令发布门禁失败。

## 物理与数值证据

验证采用分层方法：

1. 解析解和守恒式检查简单极限；
2. 单元级回归固定模型行为和异常边界；
3. 可选专业参考后端对照局部性质、动力学或传递切片；
4. 运行时适配测试确认专业模型的诊断和 ledger 真正进入 Gym 环境；
5. 冻结 trajectory 确认版本化世界律的端到端行为。

参考后端测试要求独立依赖真实可导入；缺失依赖不会被当作通过。

## 可复现性字段

trajectory、submission manifest 和 dataset card 会记录任务、场景、机制、世界律、runtime
profile、observation/scoring contract、依赖环境和源码 digest。`chemworld verify` 会重新执行并检查
这些字段，从而检测合同漂移或轨迹修改。

## 用户侧最小检查

准备引用或提交结果前，至少执行：

```bash
python -m pytest
python -m mkdocs build --strict
chemworld verify --constitution --submission runs/<trajectory>.jsonl
```

正式发布应使用完整门禁。详细产物要求见[发布检查表](release_checklist.md)和
[结果完整性](release_integrity.md)。
