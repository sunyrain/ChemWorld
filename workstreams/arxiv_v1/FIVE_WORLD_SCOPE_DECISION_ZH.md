# ChemWorld arXiv v1：五 world 证据范围与故事决策

## 决策

第一版论文不再以 16-world 总体方差确证为门槛。G2 主证据使用已有五个 matched
physical worlds；fresh-session replication 用于显示同一 physical world 内行为轨迹的
变化。已停止的 v0.6 扩展矩阵只作为补充执行记录，不表述为完成的 confirmatory study。

这不是削弱主张，而是把主张改回证据最强的逻辑类型：

> **终点是实验轨迹的多对一投影，因此不是 experimental agency 的充分统计量。**

这个测量结论由 raw-terminal 反向实例、完整匹配轨迹和重复会话直接建立，不依赖对任意
world population 的平均效应估计。

## 已有证据矩阵

| 层级 | 规模 | 主要职责 |
|---|---:|---|
| Environment qualification | 15 tasks、28 operations、5 instruments、415 complete boundary cases、62 bound endpoints | 证明 apparatus 的广度、可执行性和 evaluator binding |
| G0 compiled controls | 29,580 simulator executions；2 tasks；每任务 10 worlds | 分离 endpoint、held-out prediction、calibration、claims 与 prior response |
| G2 five-world primitive control | 2 complete agent systems；各 5 worlds × 2 arms × 6 vessels；共 120 closed lifecycles、1,704 accepted operations | 证明不同 agent system 可在同一 apparatus 中逐操作实验，并解析 assay、discard 与资源政策 |
| G2 fresh-session replication | 2 fixed worlds × 5 pairs；8 complete pairs、2 right-censored | 证明 trajectory 是随机且需要单独测量的对象 |
| v0.6 stopped extension | 3 complete pairs；1 right-censored pair；其余停止 | 仅作为三个新 world 的补充描述和扩展运行记录 |

## 关键实证结果

### 五-world primitive control

- 60/60 vessels 完成，所有完成 cell 的 physical-pair、resource-ledger 和 exact-replay
  审计通过；两个信息臂的无效操作均值均为 0。
- nominal 与 opaque 的平均 best score 分别为 0.709 和 0.631，差值 +0.078。
- nominal 相对 opaque：online retention +0.20、maximum drawdown -0.241、pooled
  recovery +0.30、terminal-to-best +0.270。
- DeepSeek 同样完成 60/60 batch closeout，但只申请 24 次 final assay，并显式 discard
  36 个 batch；Codex 为 60 assays、0 discard。两者 non-final instrument use 几乎相同
  （164 与 163），说明 completion flag 会掩盖不同的实验承诺政策。
- 五个 development worlds 同时产生 best discovery、retention、drawdown、recovery 与
  relative terminal retention；这些是 endpoint 单独不记录的独立过程读数。

### Fresh sessions

- 8 个完整 fresh pairs 中，best-score 与 algebraically independent raw-terminal contrast
  在 2/8 中符号相反；描述性 Pearson correlation 为 +0.826。
- world 3/r01 是清晰实例：best-score -0.167，raw terminal +0.240。
- terminal-to-best 是有效的 relative-retention 读数，但因分母复用了 best，它与
  best-score contrast 的 4/8 反向只作为 sensitivity，不再承担独立主轴论证。
- 四个 lifecycle readouts 的 8 个 world-by-metric 分类中 6 个为 mixed；对两个缺失
  pair 的任意正/负/零符号赋值后仍至少 6 个 mixed。该阈值分类是支持性摘要，主图使用
  全部十个计划 pair 的连续 signed contrasts。

### 三个额外 outcome-blind world pairs

- world 13：best-score -0.100，relative retention +0.624；支持过程读数分离。
- world 26：best-score +0.184，terminal-to-best +0.022；明显 endpoint 改善对应近零
  terminal-retention 改变。
- world 49：best-score -0.163，terminal-to-best -0.128；方向一致。
- 它们重复了 qualitative separation，但因父矩阵由 owner 按范围停止，只放补充材料。

## arXiv v1 的主故事

1. **新的科学仪器**：ChemWorld 不是参数 oracle，也不是实验室机器人；它把可交互、
   可干预、可复现的化学实验过程本身变成研究 apparatus。
2. **新的测量对象**：agent 可以选择 primitive operations、表征、资源分配、终止和
   final assay；因此 discovery、retention、loss、recovery 与 evidence use 可被直接测量。
3. **新的实证发现**：endpoint、prediction、claims 和 lifecycle 不等价；best score
   不能恢复 raw terminal 或完整 experimental policy，两个 complete systems 的
   assay/discard 策略也可在相同 completion 下显著不同。
4. **新的评价原则**：scientific agent 的能力必须用可干预 profile 表示，不能被一个
   optimization score 压缩。

标题采用：

> **Executable Chemical Worlds Make Experimental Agency Measurable**

主文不使用“LLM 胜过 BO”“world law 来自一个分布”或“等待大规模 population
confirmation”作为中心比赛项目。
