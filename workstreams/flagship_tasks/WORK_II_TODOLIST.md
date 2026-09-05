# Work II TODO — Experimental knowledge and scientific decisions

最后更新：2026-09-05。执行者：Codex /root；单 executor，main 分支。

## 1. 当前任务与唯一入口

M1独立世界正式块已完成：10 worlds、120/120 sessions、160/160条件、200/200物理执行与重放，
零失败和替换；图文与发布验证已完成。主效应−0.00538，95%区间[−0.01630,+0.00061]，
未支持预设实质改善。M0/M1开发结果独立保留；M2–M4未执行。

| 入口 | 唯一职责 |
| --- | --- |
| 本文件 | 当前任务、执行约束与下一步 |
| [实验矩阵](WORK_II_EXPERIMENT_MATRIX.md) | 证据处置、新实验对照/分母/读出与优先级 |
| [论文故事](../../paper/prior_discovery_story_zh.md) | 中心问题、贡献边界与 spotlight 路径 |
| [结果索引](WORK_II_PAPER_RESULTS_ZH.md) | 当前结果与不可替换的失败、删失和来源 |
| [当前绑定](../../configs/current.json) | 已有机器证据的解析入口 |
| [投稿清单](../../paper/ICLR_2027_SUBMISSION_CHECKLIST.md) | ICLR 格式、时间与匿名交付 |

旧任务卡、逐日恢复日志、旧 Q0–R5 扩展漏斗和累计 claim ladder 的文本由 Git 历史保存。
原 experiment notes、冻结配置、机器报告、原始轨迹和科学失败继续原位保留。它们解释已执行块，
不自动成为新设计门禁；不得按版本外观挑选结果或将旧未启动分母重新解释成待补样本。

## 2. 研究问题与当前结论

> 实验形成的预测和显式规律，在什么条件下能够支持未见科学决策？
> 干预知识表示与决策规则，可以定位并减少哪些决策损失？

Work I 保持已发布的世界/仪器贡献；材料信息三臂及 A-E/A-P/A-S/B/C/D 属于 Work II。
当前论文包含描述性证据、受限信息策略比较及已完成的M1正式干预。
M1未支持实质拟合收益，F-A/F-X 40/40一致；新条件迁移与普遍修复方法仍未验证。

当前核心证据：
- C2各135 scheduled cells：DeepSeek/GPT laws为135/129，注册selective-correction gates均未通过，
  预测有平均改善，规律压缩误差不同，incumbent replay增益均接近零。
- DeepSeek W2-50/64：45 scheduled cells、42 terminal rankings；law-implied Top-1 0/45，
  participant Top-1 11/45，follow-law12/42。这是显式artifact与行为的描述性差异。
- W2-61各180 slots：autonomy-minus-none regret -0.0913/+0.1102，两区间均跨零。
  donor和yoked failures进入主分母，不能隔离纯取证效应。
- B3各30 scheduled：DeepSeek17完成/13 schema失败、GPT30完成；joint recovery0/30与5/30。
- B2、reasoning-budget、schema capacity和rank/action mismatch承担测量或评价诊断，
  不共同充当Agent内部“能力链断裂”的因果证据。

## 3. 当前任务

| ID | 状态 | 工作与完成标准 |
| --- | --- | --- |
| W2-65 | DONE | 收束故事、当前入口、两份稿件及发布状态语义；实验矩阵与spotlight判别标准已整理；定向验证和PDF检查通过，未产生新实验数据 |
| W2-66 | DONE | M0：新M1公开/私有评分共用ActionPlan执行器；最小提交；42/42主执行与精确重放，包含干预对照 |
| W2-67 | DONE (development) | M1 runner及canary：2 task-worlds，12/12 sessions、16/16 slots；失败感知读出、简单基线和成本汇总；独立正式复核见W2-72 |
| W2-68 | DEFERRED | M2：同预算取证对照；仅当论文保留acquisition因果主张时进入必做集合 |
| W2-69 | NEXT (design only) | M3：先区分none/raw evidence/L-only/F-only；来源与目标机制映射、候选覆盖、主对比和成本须在执行前固定；信息剥离与新条件迁移分别命名，未执行 |
| W2-70 | DEFERRED | M4：独立模型/参考数据复核；加强外部效度，不作为近期全面数字孪生任务 |
| W2-71 | DONE | 六张图重构、配对分母与缺失值呈现修正；长稿17页，ICLR正文9页/总19页，PDF视觉及28项定向检查通过 |
| W2-72 | DONE | M1正式完成：10 worlds、120/120会话、160/160条件、200/200物理/replay，零失败；冻结面核验通过，主实质改善未获支持；七图、两份PDF及匿名数值复现验证完成；17项定向检查、Ruff及41页视觉验收通过。见[实验说明](WORK_II_M1_REPLICATION_EXPERIMENT_NOTE.md)和[结果](reports/work-ii-m1-replication-20260905.md) |

W2-01–W2-64继续使用各自终态结果，不为完成率重跑。W2-51/52的oracle排序路线关闭；
W2-57/58/59/60失败或未启动部分不续跑补齐；W2-61/62/63独立后继不能回填旧分母。
新科学设计在实验矩阵展开，本表保留唯一执行状态。

本轮来源：[开发note](WORK_II_M0_M1_DEVELOPMENT_EXPERIMENT_NOTE.md)、
[机器摘要](reports/work-ii-m0-m1-development-20260905.json)及
[可读摘要](reports/work-ii-m0-m1-development-20260905.md)。物理执行及重放约6.2分钟，
provider约13.9分钟；输入153,016、输出95,411 tokens（其中95,149 reasoning）。
开发结果不进入当前正式Results；历史provider/轨迹记录及失败未替换。

## 4. 开发优先，最后冻结一次

- 默认development mode。实现、定向测试和开发设计不依赖clean worktree、全树SHA、
  旧Gate A、preregistration readiness或release certificate。
- 旧证据因开发不匹配HEAD时，保留为其冻结版本证据，不反复修补整条旧证据链。
- 每个数据生产块开始前写一份短experiment note，固定问题、单位、coverage、测量、分母、
  pass/failure与stop rules、输出。规划矩阵不能代替执行前note。
- 开始后不按结果换任务、world、阈值、重复次数或停止规则；保留所有失败和不可评分单位。
- 平台缺陷影响正式执行语义时，受影响qualification block从首单元重跑，旧结果原样保留。
  状态文字或历史hash变化不等于物理执行失效。
- 功能与矩阵稳定且用户授权正式生产后，再绑定最小执行/evaluator表面、冻结一次、执行一次，
  最终源码提交后集中验收。不将测试、稿件或无关历史材料纳入运行时hash。

## 5. 保留的科学执行语义

原note对已执行块的规则保持有效；以下为跨块边界。
- 既有cell = task × world seed × initial-model arm × participant method。
- cell内为长驻session；新batch重置物理状态，已耗资源和可见历史不重置。
- 完整experiment由新batch开始，至committed final assay或允许的discard关闭；
  terminate本身不等于完成assay。
- 独立单位是task × world；arms、模型、重复sessions、queries、checkpoints、operations、
  replays按匹配/嵌套结构处理。重复模型采样不增加独立世界数。
- 三臂opaque/aligned/misspecified干预的是提供给参与者的描述，不直接等同不可观察的内部模型；
  初始预测用于manipulation check。
- 世界内规律固定；真实预算、安全、操作和评分契约不作为错误先验。
- 原failure-aware主分析保留；完成者结果仅作敏感性。
- H3衡量pre–final误差改善差，受初始headroom影响；不通过不等于证明不能纠错。
- best-minus-first描述搜索，不单独识别feedback learning；incumbent replay不替代未见决策。
- 每个正式task block默认最多5个world seeds，增加世界数须另行取得用户审核。
  M1的模型重复用于描述采样变异，不被当作增加统计独立性。

## 6. 参与者、资源与运行约束

- 主证据涉及DeepSeek-v4-flash/high与GPT-5.6-sol/medium，Codex为共用harness。
  它们是完整agent systems，不是模型排行榜；旧提供方/预算设置不自动授权新campaign。
- 保留task-pattern-owned stock、时间、测量、样品、终检、token与wall-clock账本。
  新实验先做本协议的成本校准，不沿用旧并发和39–93h等过时ETA。
- 当前单executor；不根据旧文档恢复三臂并发。超过60秒的命令每分钟至少报告stage、
  完成/总量、吞吐与ETA，或明确liveness counter。
- Python、pytest、Ruff和实验入口均使用 `uv run --no-sync ...`。
- 原始provider payload、credentials、private seeds和ignored runs不进Git。
- 不新建claim文件、review queue、readiness package或重复manifest。

## 7. 投稿与作者

2026-09-05核实ICLR2027官方页面：摘要2026-09-18 23:59 AoE、全文2026-09-25 23:59 AoE；
北京时间分别为9月19日与26日19:59。review正文上限9页。作者确认与实际投稿由用户处理。

作者顺序保持Jiangjie Qiu, Yijun Li, Yaotian Yang, Honghao Chen, Wentao Li, Xiaonan Wang；
前三位共同第一作者，Xiaonan Wang为通讯作者。稿件front matter是唯一作者元数据入口。
第一篇保持venue-neutral；本次ICLR/spotlight规划只适用于Work II。

本轮停止条件：当前入口不再给出冲突执行指令；已有证据、未来设计与来源清楚分开；
稿件只表达已完成结果；矩阵给出可审核对照和成本分母；定向检查通过且PDF与源稿同步。
M0/M1开发结果与M1正式复核分别计数；M2–M4未执行，不得因投稿期限降低科学门槛。

2026-09-05最终收束记录：M1完整分母、未支持的主结果、任务差异、基线和资源已接入。
七张图提供PDF/SVG及高分辨率位图；匿名稿9页正文/21页总长，长稿20页，41页完成视觉检查。
17项出版定向检查、Ruff、diff检查及独立补充包验证通过；NumPy入口重算拟合、选择与五个区间。
冻结执行面在运行前通过48项验收，运行后核验一致。原始provider/轨迹、历史失败与Work I未改。
公开报告允许同一封存结果的说明重建，禁止覆盖不同的科学结果；Git文本使用规范LF以保留跨平台绑定。
M2–M4未执行，M3先按信息剥离与目标机制映射组织；本次未支持的门槛不会触发追加M1样本。
控制处置：公开/私有边界、资源账本、exact replay和固定覆盖保留在科学执行层；freeze只做一次；
重复队列和历史状态不再支配新设计。新工作继续由本TODO与实验矩阵管理。
