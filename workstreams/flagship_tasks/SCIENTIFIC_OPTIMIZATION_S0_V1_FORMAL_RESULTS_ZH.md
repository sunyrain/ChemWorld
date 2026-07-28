# Scientific Optimization S0 v1.0 正式结果

状态：两个旗舰任务均完成 10 个独立世界、每世界 20 轮探索，参与者与全部经典基线均已精确重放审计。

所有算法比较均为描述性结果：本轮没有预注册 superiority 阈值或多重比较方案；特权基线只作校准。

## electrochemical

Codex 盲测主分均值 0.7150，世界 bootstrap 95% 区间 [0.6283, 0.7861]。

| 基线 | 角色 | 基线均值 | Codex−基线 | 配对95%区间 | 胜/平/负 |
|---|---:|---:|---:|---:|---:|
| descriptor_rf_ei | privileged_calibration | 0.6441 | +0.0708 | [-0.0072, +0.1354] | 7/0/3 |
| transport_prior_rf_ei | privileged_calibration | 0.6403 | +0.0747 | [-0.0104, +0.1478] | 7/0/3 |
| descriptor_telemetry_rf_ei | privileged_calibration | 0.6168 | +0.0982 | [+0.0139, +0.1711] | 7/0/3 |
| structured_rf_ei | information_matched | 0.6159 | +0.0991 | [+0.0103, +0.1748] | 9/0/1 |
| shuffled_descriptor_rf_ei | negative_control | 0.6147 | +0.1002 | [+0.0117, +0.1727] | 8/0/2 |
| greedy | information_matched | 0.6132 | +0.1018 | [+0.0025, +0.1866] | 8/0/2 |
| lhs | information_matched | 0.6128 | +0.1021 | [+0.0077, +0.1849] | 8/0/2 |
| descriptor_gp_ei | privileged_calibration | 0.6109 | +0.1041 | [+0.0183, +0.1780] | 8/0/2 |
| structured_gp_ei | information_matched | 0.6095 | +0.1054 | [+0.0072, +0.1948] | 8/0/2 |
| structured_safe_gp_ei | information_matched | 0.6095 | +0.1054 | [+0.0074, +0.1949] | 8/0/2 |
| telemetry_rf_ei | information_matched | 0.6092 | +0.1057 | [+0.0130, +0.1910] | 7/0/3 |
| transport_prior_gp_ei | privileged_calibration | 0.6033 | +0.1117 | [+0.0181, +0.1932] | 8/0/2 |
| random | information_matched | 0.6013 | +0.1137 | [+0.0187, +0.1953] | 9/0/1 |
| shuffled_descriptor_gp_ei | negative_control | 0.6006 | +0.1144 | [+0.0454, +0.1784] | 8/0/2 |

二级预测诊断：方向准确率 0.744，Brier 0.186。

## crystallization

Codex 盲测主分均值 0.5355，世界 bootstrap 95% 区间 [0.5045, 0.5644]。

| 基线 | 角色 | 基线均值 | Codex−基线 | 配对95%区间 | 胜/平/负 |
|---|---:|---:|---:|---:|---:|
| lhs | information_matched | 0.5708 | -0.0353 | [-0.0650, -0.0085] | 4/0/6 |
| structured_gp_ei | information_matched | 0.5648 | -0.0293 | [-0.0626, +0.0012] | 4/0/6 |
| structured_safe_gp_ei | information_matched | 0.5648 | -0.0293 | [-0.0627, +0.0011] | 4/0/6 |
| telemetry_rf_ei | information_matched | 0.5620 | -0.0265 | [-0.0578, +0.0009] | 4/0/6 |
| structured_rf_ei | information_matched | 0.5555 | -0.0200 | [-0.0505, +0.0072] | 4/0/6 |
| random | information_matched | 0.5526 | -0.0171 | [-0.0466, +0.0095] | 5/0/5 |
| greedy | information_matched | 0.5441 | -0.0087 | [-0.0385, +0.0189] | 6/0/4 |

二级预测诊断：方向准确率 0.478，Brier 0.298。

## 证据边界

- 实际物理实验总数：28060。
- 参与者最终推荐全部为已测试条件，相对已验证 incumbent 增益均为 0。
- 不允许从本轮推断 provider 因果效应或超出采样世界的广泛泛化。
- 旧 0.3902/0.4829 结果已撤回，不属于本正式证据。
