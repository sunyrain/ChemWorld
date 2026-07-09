# ChemWorld 端到端 Notebook

这组 notebook 面向外部读者，展示从 task prompt 到执行、谱图、指标和反思的完整闭环。

| Notebook | 任务 | 覆盖内容 |
| --- | --- | --- |
| `reaction_to_assay_end_to_end.ipynb` | `reaction-to-assay` | 任务规划、HPLC 中间测量、final assay、谱图和下一轮实验 |
| `reaction_to_purification_end_to_end.ipynb` | `reaction-to-purification` | 反应、相系统、萃取、分相、洗涤、干燥、浓缩、final assay |
| `partition_discovery_end_to_end.ipynb` | `partition-discovery` | campaign 多轮实验、分配趋势、final assay packet 和局部 world model |

这些 notebooks 不是最高分策略，而是可验证流程模板。运行前请安装：

```bash
python -m pip install -e ".[dev,notebooks]"
python -m ipykernel install --user --name chemworld --display-name "Python (ChemWorld)"
```
