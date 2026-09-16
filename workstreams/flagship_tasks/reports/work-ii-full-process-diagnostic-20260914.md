# 完整流程可达性与接口诊断

2026-09-14；开发诊断；无新模型调用。

固定15个完整批次，各一次；所有分支从首动作执行并支付前缀成本。
不改W2-103质量阈值，不替换历史失败。

计数：`{"planned": 15, "attempted": 15, "completed": 13, "final_assays": 13, "operations": 255, "replay_verified": 15, "prefix_reproduced": 15, "transaction_failures": 2, "execution_exceptions": 2, "model_calls": 0}`。

下表为实际终检读数；JSON另保留终检观察定律的无噪声真值及局部过程摘要，三者分列。
局部过程摘要的组分/分母与终检不同，不能把它当成终检真值。
局部见证要求合法完成、终检观察值与同口径真值均达标、重放和资源核对通过。

| 条件 | 纯度 | 回收（结晶排除晶种） | 细粉 | 过程秒 | 费用 | 完成终检 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| P1 | 0.1914 | 0.0612 | — | 21388.8 | 1.4039 | True |
| P2 | 0.1522 | 0.0464 | — | 21388.8 | 1.4259 | True |
| P3 | 0.1172 | 0.0357 | — | 21388.8 | 1.4289 | True |
| P4 | 0.3932 | 0.0571 | — | 10589.0 | 1.2557 | True |
| P5 | 0.7596 | 0.0487 | — | 3973.9 | 0.9137 | True |
| D1 | 0.3587 | 0.9641 | — | 27028.9 | 1.8087 | True |
| D2 | 缺失 | 缺失 | — | 34228.9 | 2.0037 | False |
| D3 | 0.2442 | 0.9705 | — | 34228.9 | 2.2417 | True |
| D4 | 0.5108 | 0.8132 | — | 24628.9 | 1.6494 | True |
| C1 | 0.9795 | 0.3897 | 1.0000 | 4701.0 | 0.7929 | True |
| C2 | 0.9811 | 0.4594 | 0.9105 | 17301.0 | 0.8837 | True |
| C3 | 0.9871 | 0.4566 | 0.9549 | 17301.0 | 0.8925 | True |
| C4 | 0.9821 | 0.2483 | 1.0000 | 17301.0 | 0.8552 | True |
| C5 | 缺失 | 缺失 | 缺失 | 2421.0 | 0.4849 | False |
| C6 | 0.9796 | 0.4622 | 1.0000 | 19401.0 | 0.9489 | True |

可达见证：`{"reaction-to-purification": [], "reaction-to-crystallization": [], "reaction-to-distillation": []}`。
未出现见证只表示本块覆盖未证明可达，不表示全域无解。

失败：
- D2: {'message': "stop at failed transaction: {'operation': 'collect_fraction', 'transfer_fraction': 0.0}", 'type': 'RuntimeError'}; [{'action': {'operation': 'collect_fraction', 'transfer_fraction': 0.0}, 'failed_preconditions': {'payload_bounds:transfer_fraction': False}, 'reason': 'validation_failed', 'status': 'validation_failed', 'step': 15}]
- C5: {'message': "stop at failed transaction: {'operation': 'cool_crystallize', 'target_temperature_K': 305.0, 'duration_s': 7200}", 'type': 'RuntimeError'}; [{'action': {'duration_s': 7200, 'operation': 'cool_crystallize', 'target_temperature_K': 305.0}, 'failed_preconditions': {'payload_bounds:target_temperature_K': False}, 'reason': 'validation_failed', 'status': 'validation_failed', 'step': 10}]

## 解释与实际调整

1. 纯化P1→P2→P3增加洗涤，终检纯度约19.1%→15.2%→11.7%，回收同步下降。局部过程摘要却显示纯度提高：它只汇总可分配副产物家族，终检还计入残留的其他杂质；局部回收相对分离前产物，终检回收使用初始反应物。本报告初版误把局部摘要当作同口径真值，现由原轨迹重放提取真正终检真值；没有新条件、改动作或替换结果。这个分析错误不能归因于Agent。
2. 蒸馏首段停止D1与追加并混合D3的终检纯度35.9%→24.4%，回收96.4%→97.1%；这是两个完整预定流程的描述性比较。预设的D2零收集隔离对照失败，不能把D1/D3比较冒充已完成的等过程成本隔离实验。缩短首段D4纯度51.1%、回收81.3%，仍未合格。
3. 结晶延长冷却C1→C2，细粉终检100%→91.0%、净回收38.97%→45.94%；50 mg晶种未进一步改善细粉。当前HPLC只能测晶体纯度，粒径/细粉直到终检才可见，尚不支持声称已设计粒径反馈闭环。
4. 两个失败属于本轮脚本设计：collect_fraction下限0.0001，零收集不是重选容器；C5试图从约301.78 K冷却到305 K，超过动态上界。保留失败，不补跑，不计为Agent错误。
5. 已新增完整任务公开操作状态：实际温度/体积、相身份、选中对象、当前测量或旧读数标记；模型压缩状态包保留这些字段。组分真实含量、私有参数及免费粒径信息未公开。新增理想传感读数属于下一版合同，旧Agent并未看到；本轮未做新provider验证。
6. 还确认采样按比例扣除全部库存，包括保存的相；不能将当前多容器解释为取样互相隔离。后续先处理测量对象/扣样范围及付费粒径仪器，再验证全组分终检质量的可达性。不降低80%纯度或50%细粉要求来制造成功。

后续新Astra条件仍仅GPT-6 Astra / medium，各一次；先完成上述任务资格，再做同证据交付和同前缀决策对照。当前数据不能支持系统性信息损失或跨世界结论。
