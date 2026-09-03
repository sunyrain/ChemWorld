# Work II W2-63 B3 双模型 failure-aware 收束

DeepSeek 与 Codex 均使用冻结的 30-cell B3 scientific surface。所有 participant 失败保留；缺失动作固定计为 regret=1、Top-1=0。模型差值方向为 Codex − DeepSeek，仅作配对描述。

| 模型 | scheduled | completed | failures | regret | Top-1 | joint law | post MAE |
|---|---:|---:|---:|---:|---:|---:|---:|
| deepseek | 30 | 17 | 13 | 0.9579 | 0/30 | 0/30 | 0.0928 |
| codex | 30 | 30 | 0 | 0.7594 | 2/30 | 5/30 | 0.0320 |

## 配对描述

- failure-aware regret 差值: `-0.1985`; task-world cluster bootstrap 95% interval `[-0.4372, -0.0170]`。
- Top-1 rate 差值: `0.0667`。
- joint family+exponent recovery rate 差值: `0.1667`。

不执行模型优劣检验，也不将 provider 差异解释为因果效应。
