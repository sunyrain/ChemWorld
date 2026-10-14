# 统一回收定义后的45场结晶研究

固定45场全部到达终态；失败保留，未按结果替换或追加会话。

终态 45/45；完整链 41/45；源批次 510/540；后测 125/135；有效预测 42/45；推荐复测 42/45。

回收率统一为扣除晶种后的固体目标物摩尔数除以初始试剂投料摩尔数，截断到[0,1]。源指令、任务契约、操作说明和预测问题均已对齐；数值动力学、噪声、评分与阈值未改。
60个参考批次全部精确重放，数值与原参考一致。旧45场结晶独立保留；前后不是同期随机提示对照，不能把差异直接归因于定义修正。

源重放核验 45/45；复测重放 42/42；笔记 145 版；源操作 7214 次。
完整token账 41/45；已观测输入+输出token下限 54,968,797。中断且未返回usage的会话不按零消耗解释。
结构窗口 58 个，来自35/45 场。这不是认识修订数，不并入旧105窗口编码。

## 各信息条件的完成度

| 信息条件 | 终态 | 完整链 | 源批次 | 后测 | 有效Q |
| --- | ---: | ---: | ---: | ---: | ---: |
| Opaque | 15/15 | 14/15 | 180/180 | 44/45 | 15/15 |
| Aligned | 15/15 | 14/15 | 168/180 | 42/45 | 14/15 |
| MisIndexed | 15/15 | 13/15 | 162/180 | 39/45 | 13/15 |

## 描述性结果

每个世界先平均该臂可用会话，再对五世界等权平均。表中±为世界均值的样本标准差；括号为有观测世界数/5。逐世界表另给三场会话的均值、样本标准差及实测分母。
质量合格只要求存在颗粒、纯度≥0.80和细粉≤0.50；联合合格另要求回收≥0.10。缺失预测/复测不计零，不以未完成代替预测错误。
四个响应均使用公开的0–1尺度；粒径为min(数目加权d50/250微米,1)指数，其MAE不是以微米计的直径误差。

| 指标 | Opaque | Aligned | MisIndexed |
| --- | ---: | ---: | ---: |
| 回收率 MAE | 0.11273 ± 0.039061 (5/5) | 0.10267 ± 0.018908 (5/5) | 0.088987 ± 0.024932 (5/5) |
| 纯度 MAE | 0.016242 ± 0.0052974 (5/5) | 0.051329 ± 0.014489 (5/5) | 0.052614 ± 0.020667 (5/5) |
| 粒径 MAE | 0.06251 ± 0.02609 (5/5) | 0.094661 ± 0.042266 (5/5) | 0.073908 ± 0.026883 (5/5) |
| 细粉比例 MAE | 0.32266 ± 0.05823 (5/5) | 0.30955 ± 0.038081 (5/5) | 0.32777 ± 0.017564 (5/5) |
| 纯度有符号误差（预测减参考） | -0.014256 ± 0.0064943 (5/5) | -0.051056 ± 0.01463 (5/5) | -0.051958 ± 0.02103 (5/5) |
| 质量分类正确数 /12 | 7.0667 ± 2.6916 (5/5) | 7.0667 ± 1.2561 (5/5) | 7.1667 ± 1.5 (5/5) |
| 推荐复测真实回收率 | 0.53555 ± 0.051763 (5/5) | 0.50228 ± 0.11881 (5/5) | 0.5171 ± 0.045436 (5/5) |
| 推荐复测满足质量条件（比例） | 0.86667 ± 0.18257 (5/5) | 0.8 ± 0.44721 (5/5) | 0.76667 ± 0.22361 (5/5) |
| 推荐同时满足质量及回收率 ≥0.10（比例） | 0.86667 ± 0.18257 (5/5) | 0.73333 ± 0.43461 (5/5) | 0.76667 ± 0.22361 (5/5) |
| 热历史细粉方向正确（比例） | 0.53333 ± 0.29814 (5/5) | 0.4 ± 0.27889 (5/5) | 0.46667 ± 0.36132 (5/5) |
| 热历史细粉差值绝对误差 | 0.46281 ± 0.17675 (5/5) | 0.47861 ± 0.16212 (5/5) | 0.48348 ± 0.269 (5/5) |
| 质量分类 balanced accuracy | 0.6262 ± 0.26793 (5/5) | 0.61994 ± 0.083074 (5/5) | 0.71429 ± 0.060873 (5/5) |
| crystal_yield_coverage80 | 0.48889 ± 0.2075 (5/5) | 0.54722 ± 0.23315 (5/5) | 0.61111 ± 0.12227 (5/5) |
| crystal_purity_coverage80 | 0.96111 ± 0.031672 (5/5) | 0.65 ± 0.09542 (5/5) | 0.55278 ± 0.25276 (5/5) |
| crystal_size_coverage80 | 0.63333 ± 0.13665 (5/5) | 0.54444 ± 0.18488 (5/5) | 0.54722 ± 0.1883 (5/5) |
| crystal_fines_fraction_coverage80 | 0.31667 ± 0.17743 (5/5) | 0.32222 ± 0.082402 (5/5) | 0.28333 ± 0.067042 (5/5) |
| crystal_yield_mean_width80 | 0.21561 ± 0.020184 (5/5) | 0.19325 ± 0.040353 (5/5) | 0.20749 ± 0.019783 (5/5) |
| crystal_purity_mean_width80 | 0.087894 ± 0.0080577 (5/5) | 0.13196 ± 0.020646 (5/5) | 0.12668 ± 0.018019 (5/5) |
| crystal_size_mean_width80 | 0.14496 ± 0.034435 (5/5) | 0.16439 ± 0.044695 (5/5) | 0.15797 ± 0.034942 (5/5) |
| crystal_fines_fraction_mean_width80 | 0.34022 ± 0.02506 (5/5) | 0.31733 ± 0.014424 (5/5) | 0.31392 ± 0.023411 (5/5) |

### 查询质量类别构成

这是对既有12题的描述，不改变评分或问题。高分类正确数可能来自多数类别；同时报告原评估器的balanced accuracy，不能仅凭正确数推定理解了条件差异。

| 世界 | 合格题 /12 | 不合格题 /12 | 恒预测合格正确数 | 恒预测不合格正确数 |
| --- | ---: | ---: | ---: | ---: |
| W01 | 1 | 11 | 1 | 11 |
| W02 | 1 | 11 | 1 | 11 |
| W03 | 6 | 6 | 6 | 6 |
| W04 | 4 | 8 | 4 | 8 |
| W05 | 5 | 7 | 5 | 7 |

## 同条件三次会话的稳定性

下表按repeat-01/02/03列出推荐复测是否同时满足质量与回收≥0.10。只有三次都有复测，才归为三次均达标、均未达标或混合；缺失不按失败填充。三次会话描述本次路径波动，不提供受控模型seed或总体稳定概率。

| 条件 | 三次联合达标 | 复测覆盖 | 状态 | 回收MAE范围 | 细粉MAE范围 |
| --- | --- | ---: | --- | ---: | ---: |
| C-W01-Aligned | 缺失 / 达标 / 达标 | 2/3 | 复测不全 | 0.11534–0.13333 | 0.29519–0.32441 |
| C-W01-MisIndexed | 达标 / 达标 / 未达标 | 3/3 | 有成有败 | 0.040496–0.12458 | 0.28102–0.41564 |
| C-W01-Opaque | 达标 / 达标 / 达标 | 3/3 | 三次达标 | 0.022292–0.077293 | 0.26309–0.47392 |
| C-W02-Aligned | 未达标 / 未达标 / 未达标 | 3/3 | 三次未达标 | 0.076759–0.12975 | 0.16988–0.3154 |
| C-W02-MisIndexed | 达标 / 达标 / 达标 | 3/3 | 三次达标 | 0.080208–0.14975 | 0.32453–0.37953 |
| C-W02-Opaque | 达标 / 未达标 / 达标 | 3/3 | 有成有败 | 0.045769–0.19641 | 0.37274–0.39524 |
| C-W03-Aligned | 未达标 / 达标 / 达标 | 3/3 | 有成有败 | 0.034869–0.13447 | 0.32907–0.39782 |
| C-W03-MisIndexed | 未达标 / 达标 / 达标 | 3/3 | 有成有败 | 0.065694–0.12636 | 0.30782–0.34282 |
| C-W03-Opaque | 达标 / 达标 / 未达标 | 3/3 | 有成有败 | 0.10886–0.19553 | 0.30587–0.3803 |
| C-W04-Aligned | 达标 / 达标 / 达标 | 3/3 | 三次达标 | 0.034721–0.1083 | 0.29128–0.34639 |
| C-W04-MisIndexed | 达标 / 达标 / 缺失 | 2/3 | 复测不全 | 0.032967–0.073123 | 0.22795–0.37961 |
| C-W04-Opaque | 达标 / 达标 / 达标 | 3/3 | 三次达标 | 0.11455–0.14497 | 0.23961–0.27997 |
| C-W05-Aligned | 达标 / 达标 / 达标 | 3/3 | 三次达标 | 0.040578–0.15634 | 0.26823–0.34906 |
| C-W05-MisIndexed | 未达标 / 缺失 / 达标 | 2/3 | 复测不全 | 0.049862–0.1816 | 0.3199–0.34073 |
| C-W05-Opaque | 达标 / 达标 / 达标 | 3/3 | 三次达标 | 0.094099–0.1641 | 0.20906–0.2924 |

## 逐世界的三次会话

### 回收率 MAE

| 世界 | Opaque | Aligned | MisIndexed |
| --- | ---: | ---: | ---: |
| W01 | 0.047482 ± 0.02779 (3/3) | 0.12433 ± 0.012722 (2/3) | 0.078146 ± 0.042725 (3/3) |
| W02 | 0.11134 ± 0.077193 (3/3) | 0.10609 ± 0.026945 (3/3) | 0.10798 ± 0.036819 (3/3) |
| W03 | 0.14984 ± 0.043526 (3/3) | 0.097497 ± 0.054531 (3/3) | 0.09003 ± 0.032066 (3/3) |
| W04 | 0.13144 ± 0.015485 (3/3) | 0.073685 ± 0.03698 (3/3) | 0.053045 ± 0.028395 (2/3) |
| W05 | 0.12354 ± 0.036299 (3/3) | 0.11173 ± 0.062278 (3/3) | 0.11573 ± 0.093152 (2/3) |

### 纯度 MAE

| 世界 | Opaque | Aligned | MisIndexed |
| --- | ---: | ---: | ---: |
| W01 | 0.011372 ± 0.0045145 (3/3) | 0.072533 ± 0.024159 (2/3) | 0.063229 ± 0.044386 (3/3) |
| W02 | 0.01876 ± 0.0034807 (3/3) | 0.03896 ± 0.022127 (3/3) | 0.032837 ± 0.021952 (3/3) |
| W03 | 0.013776 ± 0.0068074 (3/3) | 0.047435 ± 0.038064 (3/3) | 0.043112 ± 0.033053 (3/3) |
| W04 | 0.012973 ± 0.0035123 (3/3) | 0.059099 ± 0.052541 (3/3) | 0.083627 ± 0.0070711 (2/3) |
| W05 | 0.024331 ± 0.01102 (3/3) | 0.038616 ± 0.019221 (3/3) | 0.040263 ± 0.034204 (2/3) |

### 粒径 MAE

| 世界 | Opaque | Aligned | MisIndexed |
| --- | ---: | ---: | ---: |
| W01 | 0.055965 ± 0.024941 (3/3) | 0.050173 ± 0.013142 (2/3) | 0.051771 ± 0.036325 (3/3) |
| W02 | 0.091272 ± 0.079189 (3/3) | 0.066029 ± 0.049018 (3/3) | 0.10917 ± 0.066633 (3/3) |
| W03 | 0.08841 ± 0.03952 (3/3) | 0.12845 ± 0.10292 (3/3) | 0.042553 ± 0.031018 (3/3) |
| W04 | 0.04193 ± 0.015196 (3/3) | 0.1492 ± 0.082423 (3/3) | 0.081027 ± 0.071005 (2/3) |
| W05 | 0.034972 ± 0.020114 (3/3) | 0.079457 ± 0.091364 (3/3) | 0.085014 ± 0.014645 (2/3) |

### 细粉比例 MAE

| 世界 | Opaque | Aligned | MisIndexed |
| --- | ---: | ---: | ---: |
| W01 | 0.37061 ± 0.10548 (3/3) | 0.3098 ± 0.02066 (2/3) | 0.32631 ± 0.077368 (3/3) |
| W02 | 0.38613 ± 0.011843 (3/3) | 0.24962 ± 0.073754 (3/3) | 0.35314 ± 0.027567 (3/3) |
| W03 | 0.33095 ± 0.04274 (3/3) | 0.35545 ± 0.037057 (3/3) | 0.32531 ± 0.0175 (3/3) |
| W04 | 0.26435 ± 0.021665 (3/3) | 0.31826 ± 0.027571 (3/3) | 0.30378 ± 0.10724 (2/3) |
| W05 | 0.26128 ± 0.045499 (3/3) | 0.31462 ± 0.041719 (3/3) | 0.33031 ± 0.014731 (2/3) |

### 纯度有符号误差（预测减参考）

| 世界 | Opaque | Aligned | MisIndexed |
| --- | ---: | ---: | ---: |
| W01 | -0.0080611 ± 0.0077573 (3/3) | -0.072533 ± 0.024159 (2/3) | -0.062589 ± 0.045492 (3/3) |
| W02 | -0.017177 ± 0.0043368 (3/3) | -0.038677 ± 0.022546 (3/3) | -0.031927 ± 0.023497 (3/3) |
| W03 | -0.0096312 ± 0.0094595 (3/3) | -0.046353 ± 0.039405 (3/3) | -0.042242 ± 0.034147 (3/3) |
| W04 | -0.012321 ± 0.0039232 (3/3) | -0.059099 ± 0.052541 (3/3) | -0.083627 ± 0.0070711 (2/3) |
| W05 | -0.024088 ± 0.011281 (3/3) | -0.038616 ± 0.019221 (3/3) | -0.039407 ± 0.035414 (2/3) |

### 质量分类正确数 /12

| 世界 | Opaque | Aligned | MisIndexed |
| --- | ---: | ---: | ---: |
| W01 | 4.6667 ± 2.0817 (3/3) | 5 ± 0 (2/3) | 5 ± 1 (3/3) |
| W02 | 4 ± 0 (3/3) | 7.6667 ± 3.0551 (3/3) | 6.6667 ± 0.57735 (3/3) |
| W03 | 7.3333 ± 1.1547 (3/3) | 7 ± 1 (3/3) | 8.6667 ± 1.1547 (3/3) |
| W04 | 9.3333 ± 1.5275 (3/3) | 7.3333 ± 3.7859 (3/3) | 8.5 ± 2.1213 (2/3) |
| W05 | 10 ± 0 (3/3) | 8.3333 ± 1.1547 (3/3) | 7 ± 0 (2/3) |

### 推荐复测真实回收率

| 世界 | Opaque | Aligned | MisIndexed |
| --- | ---: | ---: | ---: |
| W01 | 0.56748 ± 0.11626 (3/3) | 0.52379 ± 0.015944 (2/3) | 0.51126 ± 0.17475 (3/3) |
| W02 | 0.57936 ± 0.058825 (3/3) | 0.59534 ± 0.025862 (3/3) | 0.56954 ± 0.13829 (3/3) |
| W03 | 0.57 ± 0.10746 (3/3) | 0.29593 ± 0.25743 (3/3) | 0.54555 ± 0.12935 (3/3) |
| W04 | 0.49657 ± 0.090178 (3/3) | 0.56468 ± 0.097065 (3/3) | 0.44917 ± 0.0025711 (2/3) |
| W05 | 0.46433 ± 0.11802 (3/3) | 0.53165 ± 0.085436 (3/3) | 0.50997 ± 0.15763 (2/3) |

### 推荐复测满足质量条件（比例）

| 世界 | Opaque | Aligned | MisIndexed |
| --- | ---: | ---: | ---: |
| W01 | 1 ± 0 (3/3) | 1 ± 0 (2/3) | 0.66667 ± 0.57735 (3/3) |
| W02 | 0.66667 ± 0.57735 (3/3) | 0 ± 0 (3/3) | 1 ± 0 (3/3) |
| W03 | 0.66667 ± 0.57735 (3/3) | 1 ± 0 (3/3) | 0.66667 ± 0.57735 (3/3) |
| W04 | 1 ± 0 (3/3) | 1 ± 0 (3/3) | 1 ± 0 (2/3) |
| W05 | 1 ± 0 (3/3) | 1 ± 0 (3/3) | 0.5 ± 0.70711 (2/3) |

### 推荐同时满足质量及回收率 ≥0.10（比例）

| 世界 | Opaque | Aligned | MisIndexed |
| --- | ---: | ---: | ---: |
| W01 | 1 ± 0 (3/3) | 1 ± 0 (2/3) | 0.66667 ± 0.57735 (3/3) |
| W02 | 0.66667 ± 0.57735 (3/3) | 0 ± 0 (3/3) | 1 ± 0 (3/3) |
| W03 | 0.66667 ± 0.57735 (3/3) | 0.66667 ± 0.57735 (3/3) | 0.66667 ± 0.57735 (3/3) |
| W04 | 1 ± 0 (3/3) | 1 ± 0 (3/3) | 1 ± 0 (2/3) |
| W05 | 1 ± 0 (3/3) | 1 ± 0 (3/3) | 0.5 ± 0.70711 (2/3) |

### 热历史细粉方向正确（比例）

| 世界 | Opaque | Aligned | MisIndexed |
| --- | ---: | ---: | ---: |
| W01 | 0.33333 ± 0.57735 (3/3) | 0 ± 0 (2/3) | 0 ± 0 (3/3) |
| W02 | 0.33333 ± 0.57735 (3/3) | 0.33333 ± 0.57735 (3/3) | 1 ± 0 (3/3) |
| W03 | 0.33333 ± 0.57735 (3/3) | 0.33333 ± 0.57735 (3/3) | 0.33333 ± 0.57735 (3/3) |
| W04 | 0.66667 ± 0.57735 (3/3) | 0.66667 ± 0.57735 (3/3) | 0.5 ± 0.70711 (2/3) |
| W05 | 1 ± 0 (3/3) | 0.66667 ± 0.57735 (3/3) | 0.5 ± 0.70711 (2/3) |

### 热历史细粉差值绝对误差

| 世界 | Opaque | Aligned | MisIndexed |
| --- | ---: | ---: | ---: |
| W01 | 0.39425 ± 0.20648 (3/3) | 0.40258 ± 0.091924 (2/3) | 0.51425 ± 0.025166 (3/3) |
| W02 | 0.29576 ± 0.23903 (3/3) | 0.28309 ± 0.14901 (3/3) | 0.055759 ± 0.046202 (3/3) |
| W03 | 0.74901 ± 0.18009 (3/3) | 0.65234 ± 0.43278 (3/3) | 0.76901 ± 0.1893 (3/3) |
| W04 | 0.36982 ± 0.24576 (3/3) | 0.41315 ± 0.29687 (3/3) | 0.44482 ± 0.28991 (2/3) |
| W05 | 0.50521 ± 0.073711 (3/3) | 0.64188 ± 0.21825 (3/3) | 0.63355 ± 0.24749 (2/3) |

## 全部会话与科学记录

| 会话 | 状态 | 批次 | 后测 | 回收MAE | 纯度偏差 | 笔记/报告/执行 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| repeat-01/C-W01-Opaque | completed | 12/12 | 3/3 | 0.022292 | -0.012117 | [笔记](repeat-01/C-W01-Opaque-notebook.md) / [报告](repeat-01/C-W01-Opaque-reports.md) / [时序](sessions/repeat-01/C-W01-Opaque.json) |
| repeat-01/C-W01-Aligned | failed | 0/12 | 0/3 | — | — | [笔记](repeat-01/C-W01-Aligned-notebook.md) / [报告](repeat-01/C-W01-Aligned-reports.md) / [时序](sessions/repeat-01/C-W01-Aligned.json) |
| repeat-01/C-W01-MisIndexed | completed | 12/12 | 3/3 | 0.12458 | -0.0102 | [笔记](repeat-01/C-W01-MisIndexed-notebook.md) / [报告](repeat-01/C-W01-MisIndexed-reports.md) / [时序](sessions/repeat-01/C-W01-MisIndexed.json) |
| repeat-01/C-W02-Opaque | failed | 12/12 | 2/3 | 0.045769 | -0.020649 | [笔记](repeat-01/C-W02-Opaque-notebook.md) / [报告](repeat-01/C-W02-Opaque-reports.md) / [时序](sessions/repeat-01/C-W02-Opaque.json) |
| repeat-01/C-W02-Aligned | completed | 12/12 | 3/3 | 0.11176 | -0.016399 | [笔记](repeat-01/C-W02-Aligned-notebook.md) / [报告](repeat-01/C-W02-Aligned-reports.md) / [时序](sessions/repeat-01/C-W02-Aligned.json) |
| repeat-01/C-W02-MisIndexed | completed | 12/12 | 3/3 | 0.14975 | -0.0053154 | [笔记](repeat-01/C-W02-MisIndexed-notebook.md) / [报告](repeat-01/C-W02-MisIndexed-reports.md) / [时序](sessions/repeat-01/C-W02-MisIndexed.json) |
| repeat-01/C-W03-Opaque | completed | 12/12 | 3/3 | 0.19553 | -0.0078534 | [笔记](repeat-01/C-W03-Opaque-notebook.md) / [报告](repeat-01/C-W03-Opaque-reports.md) / [时序](sessions/repeat-01/C-W03-Opaque.json) |
| repeat-01/C-W03-Aligned | completed | 12/12 | 3/3 | 0.12315 | -0.08277 | [笔记](repeat-01/C-W03-Aligned-notebook.md) / [报告](repeat-01/C-W03-Aligned-reports.md) / [时序](sessions/repeat-01/C-W03-Aligned.json) |
| repeat-01/C-W03-MisIndexed | completed | 12/12 | 3/3 | 0.065694 | -0.033687 | [笔记](repeat-01/C-W03-MisIndexed-notebook.md) / [报告](repeat-01/C-W03-MisIndexed-reports.md) / [时序](sessions/repeat-01/C-W03-MisIndexed.json) |
| repeat-01/C-W04-Opaque | completed | 12/12 | 3/3 | 0.14497 | -0.01471 | [笔记](repeat-01/C-W04-Opaque-notebook.md) / [报告](repeat-01/C-W04-Opaque-reports.md) / [时序](sessions/repeat-01/C-W04-Opaque.json) |
| repeat-01/C-W04-Aligned | completed | 12/12 | 3/3 | 0.078039 | -0.03421 | [笔记](repeat-01/C-W04-Aligned-notebook.md) / [报告](repeat-01/C-W04-Aligned-reports.md) / [时序](sessions/repeat-01/C-W04-Aligned.json) |
| repeat-01/C-W04-MisIndexed | completed | 12/12 | 3/3 | 0.032967 | -0.078627 | [笔记](repeat-01/C-W04-MisIndexed-notebook.md) / [报告](repeat-01/C-W04-MisIndexed-reports.md) / [时序](sessions/repeat-01/C-W04-MisIndexed.json) |
| repeat-01/C-W05-Opaque | completed | 12/12 | 3/3 | 0.094099 | -0.036949 | [笔记](repeat-01/C-W05-Opaque-notebook.md) / [报告](repeat-01/C-W05-Opaque-reports.md) / [时序](sessions/repeat-01/C-W05-Opaque.json) |
| repeat-01/C-W05-Aligned | completed | 12/12 | 3/3 | 0.040578 | -0.056949 | [笔记](repeat-01/C-W05-Aligned-notebook.md) / [报告](repeat-01/C-W05-Aligned-reports.md) / [时序](sessions/repeat-01/C-W05-Aligned.json) |
| repeat-01/C-W05-MisIndexed | completed | 12/12 | 3/3 | 0.049862 | -0.064449 | [笔记](repeat-01/C-W05-MisIndexed-notebook.md) / [报告](repeat-01/C-W05-MisIndexed-reports.md) / [时序](sessions/repeat-01/C-W05-MisIndexed.json) |
| repeat-02/C-W03-MisIndexed | completed | 12/12 | 3/3 | 0.078031 | -0.013187 | [笔记](repeat-02/C-W03-MisIndexed-notebook.md) / [报告](repeat-02/C-W03-MisIndexed-reports.md) / [时序](sessions/repeat-02/C-W03-MisIndexed.json) |
| repeat-02/C-W03-Aligned | completed | 12/12 | 3/3 | 0.13447 | -0.05177 | [笔记](repeat-02/C-W03-Aligned-notebook.md) / [报告](repeat-02/C-W03-Aligned-reports.md) / [时序](sessions/repeat-02/C-W03-Aligned.json) |
| repeat-02/C-W03-Opaque | completed | 12/12 | 3/3 | 0.10886 | -0.019853 | [笔记](repeat-02/C-W03-Opaque-notebook.md) / [报告](repeat-02/C-W03-Opaque-reports.md) / [时序](sessions/repeat-02/C-W03-Opaque.json) |
| repeat-02/C-W04-MisIndexed | completed | 12/12 | 3/3 | 0.073123 | -0.088627 | [笔记](repeat-02/C-W04-MisIndexed-notebook.md) / [报告](repeat-02/C-W04-MisIndexed-reports.md) / [时序](sessions/repeat-02/C-W04-MisIndexed.json) |
| repeat-02/C-W04-Aligned | completed | 12/12 | 3/3 | 0.1083 | -0.11946 | [笔记](repeat-02/C-W04-Aligned-notebook.md) / [报告](repeat-02/C-W04-Aligned-reports.md) / [时序](sessions/repeat-02/C-W04-Aligned.json) |
| repeat-02/C-W04-Opaque | completed | 12/12 | 3/3 | 0.13481 | -0.01446 | [笔记](repeat-02/C-W04-Opaque-notebook.md) / [报告](repeat-02/C-W04-Opaque-reports.md) / [时序](sessions/repeat-02/C-W04-Opaque.json) |
| repeat-02/C-W05-MisIndexed | failed | 6/12 | 0/3 | — | — | [笔记](repeat-02/C-W05-MisIndexed-notebook.md) / [报告](repeat-02/C-W05-MisIndexed-reports.md) / [时序](sessions/repeat-02/C-W05-MisIndexed.json) |
| repeat-02/C-W05-Aligned | completed | 12/12 | 3/3 | 0.13827 | -0.018616 | [笔记](repeat-02/C-W05-Aligned-notebook.md) / [报告](repeat-02/C-W05-Aligned-reports.md) / [时序](sessions/repeat-02/C-W05-Aligned.json) |
| repeat-02/C-W05-Opaque | completed | 12/12 | 3/3 | 0.11243 | -0.015866 | [笔记](repeat-02/C-W05-Opaque-notebook.md) / [报告](repeat-02/C-W05-Opaque-reports.md) / [时序](sessions/repeat-02/C-W05-Opaque.json) |
| repeat-02/C-W01-MisIndexed | completed | 12/12 | 3/3 | 0.069362 | -0.08545 | [笔记](repeat-02/C-W01-MisIndexed-notebook.md) / [报告](repeat-02/C-W01-MisIndexed-reports.md) / [时序](sessions/repeat-02/C-W01-MisIndexed.json) |
| repeat-02/C-W01-Aligned | completed | 12/12 | 3/3 | 0.11534 | -0.05545 | [笔记](repeat-02/C-W01-Aligned-notebook.md) / [报告](repeat-02/C-W01-Aligned-reports.md) / [时序](sessions/repeat-02/C-W01-Aligned.json) |
| repeat-02/C-W01-Opaque | completed | 12/12 | 3/3 | 0.042862 | 0.00088338 | [笔记](repeat-02/C-W01-Opaque-notebook.md) / [报告](repeat-02/C-W01-Opaque-reports.md) / [时序](sessions/repeat-02/C-W01-Opaque.json) |
| repeat-02/C-W02-MisIndexed | completed | 12/12 | 3/3 | 0.093995 | -0.049815 | [笔记](repeat-02/C-W02-MisIndexed-notebook.md) / [报告](repeat-02/C-W02-MisIndexed-reports.md) / [时序](sessions/repeat-02/C-W02-MisIndexed.json) |
| repeat-02/C-W02-Aligned | completed | 12/12 | 3/3 | 0.076759 | -0.061482 | [笔记](repeat-02/C-W02-Aligned-notebook.md) / [报告](repeat-02/C-W02-Aligned-reports.md) / [时序](sessions/repeat-02/C-W02-Aligned.json) |
| repeat-02/C-W02-Opaque | completed | 12/12 | 3/3 | 0.091829 | -0.018565 | [笔记](repeat-02/C-W02-Opaque-notebook.md) / [报告](repeat-02/C-W02-Opaque-reports.md) / [时序](sessions/repeat-02/C-W02-Opaque.json) |
| repeat-03/C-W05-Aligned | completed | 12/12 | 3/3 | 0.15634 | -0.040282 | [笔记](repeat-03/C-W05-Aligned-notebook.md) / [报告](repeat-03/C-W05-Aligned-reports.md) / [时序](sessions/repeat-03/C-W05-Aligned.json) |
| repeat-03/C-W05-Opaque | completed | 12/12 | 3/3 | 0.1641 | -0.019449 | [笔记](repeat-03/C-W05-Opaque-notebook.md) / [报告](repeat-03/C-W05-Opaque-reports.md) / [时序](sessions/repeat-03/C-W05-Opaque.json) |
| repeat-03/C-W05-MisIndexed | completed | 12/12 | 3/3 | 0.1816 | -0.014366 | [笔记](repeat-03/C-W05-MisIndexed-notebook.md) / [报告](repeat-03/C-W05-MisIndexed-reports.md) / [时序](sessions/repeat-03/C-W05-MisIndexed.json) |
| repeat-03/C-W01-Aligned | completed | 12/12 | 3/3 | 0.13333 | -0.089617 | [笔记](repeat-03/C-W01-Aligned-notebook.md) / [报告](repeat-03/C-W01-Aligned-reports.md) / [时序](sessions/repeat-03/C-W01-Aligned.json) |
| repeat-03/C-W01-Opaque | completed | 12/12 | 3/3 | 0.077293 | -0.01295 | [笔记](repeat-03/C-W01-Opaque-notebook.md) / [报告](repeat-03/C-W01-Opaque-reports.md) / [时序](sessions/repeat-03/C-W01-Opaque.json) |
| repeat-03/C-W01-MisIndexed | completed | 12/12 | 3/3 | 0.040496 | -0.092117 | [笔记](repeat-03/C-W01-MisIndexed-notebook.md) / [报告](repeat-03/C-W01-MisIndexed-reports.md) / [时序](sessions/repeat-03/C-W01-MisIndexed.json) |
| repeat-03/C-W02-Aligned | completed | 12/12 | 3/3 | 0.12975 | -0.038149 | [笔记](repeat-03/C-W02-Aligned-notebook.md) / [报告](repeat-03/C-W02-Aligned-reports.md) / [时序](sessions/repeat-03/C-W02-Aligned.json) |
| repeat-03/C-W02-Opaque | completed | 12/12 | 3/3 | 0.19641 | -0.012315 | [笔记](repeat-03/C-W02-Opaque-notebook.md) / [报告](repeat-03/C-W02-Opaque-reports.md) / [时序](sessions/repeat-03/C-W02-Opaque.json) |
| repeat-03/C-W02-MisIndexed | completed | 12/12 | 3/3 | 0.080208 | -0.040649 | [笔记](repeat-03/C-W02-MisIndexed-notebook.md) / [报告](repeat-03/C-W02-MisIndexed-reports.md) / [时序](sessions/repeat-03/C-W02-MisIndexed.json) |
| repeat-03/C-W03-Aligned | completed | 12/12 | 3/3 | 0.034869 | -0.0045201 | [笔记](repeat-03/C-W03-Aligned-notebook.md) / [报告](repeat-03/C-W03-Aligned-reports.md) / [时序](sessions/repeat-03/C-W03-Aligned.json) |
| repeat-03/C-W03-Opaque | completed | 12/12 | 3/3 | 0.14512 | -0.0011868 | [笔记](repeat-03/C-W03-Opaque-notebook.md) / [报告](repeat-03/C-W03-Opaque-reports.md) / [时序](sessions/repeat-03/C-W03-Opaque.json) |
| repeat-03/C-W03-MisIndexed | completed | 12/12 | 3/3 | 0.12636 | -0.079853 | [笔记](repeat-03/C-W03-MisIndexed-notebook.md) / [报告](repeat-03/C-W03-MisIndexed-reports.md) / [时序](sessions/repeat-03/C-W03-MisIndexed.json) |
| repeat-03/C-W04-Aligned | completed | 12/12 | 3/3 | 0.034721 | -0.023627 | [笔记](repeat-03/C-W04-Aligned-notebook.md) / [报告](repeat-03/C-W04-Aligned-reports.md) / [时序](sessions/repeat-03/C-W04-Aligned.json) |
| repeat-03/C-W04-Opaque | completed | 12/12 | 3/3 | 0.11455 | -0.0077935 | [笔记](repeat-03/C-W04-Opaque-notebook.md) / [报告](repeat-03/C-W04-Opaque-reports.md) / [时序](sessions/repeat-03/C-W04-Opaque.json) |
| repeat-03/C-W04-MisIndexed | failed | 0/12 | 0/3 | — | — | [笔记](repeat-03/C-W04-MisIndexed-notebook.md) / [报告](repeat-03/C-W04-MisIndexed-reports.md) / [时序](sessions/repeat-03/C-W04-MisIndexed.json) |

## 保留失败

- repeat-01/C-W01-Aligned: failed; 缺失=['K1', 'Q', 'K2']; {'stage': 'source', 'type': 'InteractiveCodexExperimentError', 'message': 'Codex session crossed a frozen operational limit before the next executable operation; no fallback action was emitted: max_provider_error_events'}
- repeat-01/C-W02-Opaque: failed; 缺失=['K2']; {'stage': 'K2', 'message': 'provider_failure'}
- repeat-02/C-W05-MisIndexed: failed; 缺失=['K1', 'Q', 'K2']; {'stage': 'source', 'type': 'InteractiveCodexExperimentError', 'message': 'Codex session crossed a frozen operational limit before the next executable operation; no fallback action was emitted: max_provider_error_events'}
- repeat-03/C-W04-MisIndexed: failed; 缺失=['K1', 'Q', 'K2']; {'stage': 'source', 'type': 'InteractiveCodexExperimentError', 'message': 'Codex session crossed a frozen operational limit before the next executable operation; no fallback action was emitted: max_provider_error_events'}

## 解释边界

- Fresh model sessions; model sampling RNG cannot be fixed.
- Corrected protocol, not a randomized prompt-correction effect estimate.
- Source batches, queries and windows are nested within sessions/worlds.
- Old 90-session results and failures remain; no replacement or denominator pooling.
- Timelines establish public evidence and execution, not private cognition or causality.
- Independent researcher review remains unfinished.
