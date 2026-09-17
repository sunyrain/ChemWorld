# ChemWorld 实验 1 设计指导文件

## 目录定位

本目录保存实验 1 的科学设计、World authoring 和 qualification 讨论稿，作为后续实现、审查和扩展七体系 benchmark 的设计依据。

这些文件是**设计指导与版本历史**，不是当前运行器直接读取的机器执行合同。把文件收入仓库不等于其中所有候选 World、阈值或 Gate 已经 qualification 通过，也不会自动改变任何实验结果。

## 当前执行权威

对于当前已经启动的 EC W00 + W1–W5 qualification，发生冲突时按以下优先级解释：

1. `configs/benchmark/experiment_1_ec_qualification_v1.0.1.json`：机器可读配置与实际运行参数；
2. `workstreams/flagship_tasks/EXPERIMENT_1_MINIMUM_EXECUTION_SPEC_V1_0_1.md`：冻结的最小执行规范；
3. `workstreams/flagship_tasks/EXPERIMENT_1_EC_QUALIFICATION_V1_0_1_NOTE.md`：本轮 qualification 的实验记录与解释；
4. 本目录五份文件：设计依据、科学语义和未来扩展参考。

七体系 35 Worlds / 21 格正式 benchmark 不应仅依据本目录直接开跑；还需要在机器可读配置、private truth、prior generator、qualification threshold 和 freeze manifest 中完成对应冻结。

## 推荐阅读顺序

1. `ChemWorld_实验1_七大任务体系科学定义_v0.1.md`：理解七个体系分别研究什么；
2. `ChemWorld_实验1_七任务三层先验扰动矩阵_v0.1.md`：理解实体、参数、结构三层先验与 21 格；
3. `ChemWorld_实验1_35底层World_PrivateTruth设计_v0.3.md`：理解 35 个 World 的底层规律候选；
4. `ChemWorld_实验1_21格_Qualification_Specification_v0.5.md`：理解每格的 qualification 科学条件；
5. `ChemWorld_实验1_七体系35Worlds_21格Qualification_设计规范_v1.0.md`：作为前述设计的综合版本阅读。

## 文件来源与完整性

以下文件于 2026-09-17 从项目负责人提供的本地文档原样收入仓库；除第一份文件名从 URL 编码规范化为可读中文外，正文未修改。

| 文件 | SHA-256 |
| --- | --- |
| `ChemWorld_实验1_21格_Qualification_Specification_v0.5.md` | `f32a91769480fd3b8a2746e4b6256b90d3398c249ae52251421b876277a447d5` |
| `ChemWorld_实验1_七体系35Worlds_21格Qualification_设计规范_v1.0.md` | `fedfa7a57541461e6df1692072da974cf43e90f2bce5073678f28b74335f6aae` |
| `ChemWorld_实验1_35底层World_PrivateTruth设计_v0.3.md` | `949170ce6779c3072d8a441e89c730ae47bbf376894051fdaeb31bad392b8837` |
| `ChemWorld_实验1_七大任务体系科学定义_v0.1.md` | `6e17b9e563f026d95fd3f34c8cb96e4c1bc25d365534d9af9cff5b44cdc7c181` |
| `ChemWorld_实验1_七任务三层先验扰动矩阵_v0.1.md` | `5cb3502980b01c60144d7fec181dad1aba2b8c64e2342dbd58bcba2b1066cb79` |

## 维护规则

- 保留文件名中的版本号，不用新内容覆盖旧版本；
- 新版本以新文件加入，并在本索引中注明替代关系；
- 设计稿中的变更只有同步进入执行规范、机器配置和 freeze manifest 后，才算进入 benchmark；
- 正式实验开始后，禁止静默修改已冻结的 World、先验生成规则、预算或 Gate 阈值。
