# Work II W2-62 C2 双模型 current-composite 收束

两个模型均使用同一 135-cell、45-world-cluster、9-task C2 evaluator surface。差值方向固定为 Codex − DeepSeek，仅作 matched descriptive analysis。

| 模型 | completed | prediction Δ | final error | law MAE | compression loss | blind gain |
|---|---:|---:|---:|---:|---:|---:|
| deepseek | 121/135 | 0.1198 | 0.1685 | 0.2371 | 0.0686 | -0.0010 |
| codex | 126/135 | 0.1329 | 0.1614 | 0.1753 | 0.0142 | -0.0001 |

## 配对差值

- prediction_improvement: n=`135`, Δ=`0.0131`, 95% cluster interval=`[-0.0081, 0.0328]`。
- effective_final_error: n=`135`, Δ=`-0.0071`, 95% cluster interval=`[-0.0182, 0.0036]`。
- law_mae: n=`129`, Δ=`-0.0648`, 95% cluster interval=`[-0.0921, -0.0382]`。
- law_compression_loss: n=`129`, Δ=`-0.0579`, 95% cluster interval=`[-0.0837, -0.0333]`。
- blind_gain: n=`114`, Δ=`0.0009`。

不执行模型优劣检验，也不解释为 provider 因果效应。
