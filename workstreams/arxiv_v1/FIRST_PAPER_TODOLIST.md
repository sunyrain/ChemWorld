# ChemWorld 第一篇精简 TODO —— 世界仪器发布

状态：**DONE**
负责人：**codex-1**  
执行方式：**单 agent、main 分支、完成一段即提交并推送**  
写作方式：**venue-neutral；Nature 系列 skill 停用，除非用户以后明确重新启用**

本文件是第一篇当前唯一执行清单。新协作者先读本文件和同目录 `README.md`；`archive/`、
claims、integration、story、reviews 以及旧审计材料均为历史记录，不得据此恢复任务或 owner。

## 0A. 协作认领与稿件源规则

- **Claim 规则**：认领时在当前 TODO 的进度快照或对应任务行写明执行者身份、任务 ID 和状态，格式为
  `Claim: Codex /root — A02 — DOING`；不新建 claim 文件、租约、review queue 或 per-task worktree。
- **完成规则**：完成标准和定向验证通过后，将任务标记为 `DONE`，在同一段提交中说明实际改动，随后推送到
  `main`；若未完成，不得提前标记 `DONE`。
- **规范稿件源**：`paper/experimental_intelligence_v1_manuscript.md` 是论文 Markdown 规范源，正文和
  frontmatter 只在这里修改。
- **生成链**：运行 `paper/tools/build_arxiv_release.py`，由规范源生成 `paper/arxiv/main.tex`，再编译
  `paper/exports/experimental-intelligence-v1-arxiv/` 下的 PDF、source bundle 和 build manifest；不得手改
  `paper/arxiv/main.tex` 或生成的 PDF 来绕过源稿。
- **文件位置**：`paper/arxiv/` 保存生成后的投稿 TeX、参考文献和临时编译目录，不是正文编辑入口；可交付
  PDF 的固定路径是 `paper/exports/experimental-intelligence-v1-arxiv/chemworld-experimental-agency-arxiv.pdf`，
  同目录的 `build-manifest.json`、source ZIP/TAR 和 `source/` 必须来自同一次构建。
- **同步要求**：论文正文改动完成后，若影响标题、摘要、正文或图表，必须在同一发布段重建并检查 arXiv
  TeX/PDF、source bundle 和 build manifest；生成物未同步或 PDF 未做视觉检查时，该稿件段不算完成。

## 0. 当前进度快照

- **DONE**：15 个参考任务、既有边界用例、typed operations/instruments、资源账本、精确重放、
  单组件 world forks、known-policy controls 和已有完整 agent 生命周期均可复用。
- **DONE（实现）/ 未执行（新故事）**：已有一个面向 15 个参考任务的跨世界资格 runner；它可作为
  C01、C04--C06 的参考集基线，但不能替代生成组合 C02 或未见组合 C03，也不证明世界空间只有 15 项。
- **DONE**：A01，统一世界底座/仪器主张和边界；源稿的标题、摘要、引言和讨论已切换到新故事，且
  arXiv TeX/PDF 已由规范源重建同步。
- **DONE**：A02，Codex `/root` 完成 v1 世界组合语法与公开构造契约；规范见
  `docs/world-composition-contract.md`。
- **DONE**：A03，Codex `/root` 完成当前能力表；规范见 `docs/world-capability-map.md`。
- **DONE**：A04，Codex `/root` 已将论文 Results 重排为构造、组合覆盖、接口/物理/事务资格、受控分叉、agent 使用和过程记录；arXiv TeX/PDF 已同步并通过视觉顺序检查。
- **DONE**：B01，Codex `/root` 已实现统一声明式世界构造入口；合法的 v1 组件组合可编译为运行时任务与场景，并公开操作、仪器、资源、终止和评价表面。
- **DONE**：B02，Codex `/root` 已实现执行前兼容性检查；缺失依赖、冲突状态所有者、单位不匹配、无效参数、资源不可能性和生命周期空洞会以结构化诊断 fail closed，声明范围会收窄运行时操作验证，结晶/电化学组合保留模板工作流门控。
- **DONE**：B03，Codex `/root` 已实现覆盖引导的组合生成；离散轴使用 pairwise covering rows，连续轴使用 seeded Latin hypercube，工作流覆盖关键有序操作交互，并报告精确分母、成功数和全部失败。
- **DONE**：B04，Codex `/root` 已补齐并统一说明单一过程模块、跨模块、多阶段和受控分叉 authoring 示例；三份组合请求通过统一编译器验证，15 个参考任务已按八个组件模式及同一 TaskSpec 覆盖层映射。
- **DONE**：U00，Codex `/root` 已锁定 U01--U06 案例矩阵；六项分别承担多阶段传播、资源受限测量、失败恢复、受控分叉、未见组合/完整 agent 和案例广度证据，U05 与 C03 共用预先冻结的反应--蒸馏覆盖批次。
- **DONE**：C00，Codex `/root` 已冻结 C01--C08 与 D01--D04 的单份组合资格实验说明；正式分母、覆盖 seeds、U05/C03 共同未见批次、测量、pass/failure 规则和输出均在数据生成前锁定。
- **DONE / 平台预算修复 design v3**：v2 在第 16 步 final assay 暴露的 `measure` repeat-limit 合同矛盾已修复；旧失败完整保留。Design v3 未改变 coverage、seed、workflow、process-time 秒数或其他重复上限，全量组合资格从首个 case 重跑并通过 64/64 reference units、1,786/1,786 recipes、192/192 negatives、52/52 generated、8/8 unseen、32/32 modules、7/7 interfaces 和 7/7 mutants；受影响的 8 个确定性案例也从头重跑并通过。
- **DONE**：`Claim: Codex /root — U00/B04-AMEND — DONE`；U02/U03 authoring example 已改用 runtime
  支持的 `balanced` objective，冻结并执行验证 5-step 表征路径和 19-step 失败--恢复路径；规范源、arXiv
  TeX、19 页 PDF、source bundle 和 build manifest 已由同一次确定性构建同步，PDF 第 3--4 页视觉检查通过。
- **DONE / Claim**：`Claim: Codex /root — U01-U03/U06/E01-DET — DONE`；按
  `experiments/first-paper-deterministic-use-cases.md` 完成 8 个冻结确定性案例。正式结果为 89/89 submitted
  actions 均有完整回执、88 commits、1 个预注册 rollback、8 个 final assays；89/89 逐步资源对账、8/8
  exact replay、U03 ghost-state 对账和 U04/U05 current evidence binding 全部通过，provider、leakage、
  missing receipts 和 failure classes 均为零。规范论文源、arXiv TeX、19 页 PDF、source bundle 与 build
  manifest 已同步；PDF 第 1、4、11 页视觉检查及重复构建零 diff 通过。
- **DONE / Claim**：`Claim: Codex /root — U04/U05/E02-INSTRUMENT-USE — DONE`；U04 通过
  `configs/current.json` 复用既有 single-private-component fork 正式证据，没有重跑。U05/E02 的 design-v3
  真实 provider 单元在冻结 C03 首个未见反应--蒸馏组合上闭合一个完整生命周期：15/15 actions committed、
  1 terminate、1 final assay、0 rollback、0 leakage、exact replay 零误差；process time 为
  8,158.454/10,440 s。Provider accounting 为 1 session、1 logical Codex turn、17 MCP calls；累计 input
  493,092（cache hit 440,832、uncached 52,260），output 2,973，均在冻结上限内。v1/v2 失败继续保留，
  成功结果见 `reports/first-paper-agent-instrument-use-v3.{json,md}`。
- **DONE**：E03/E04 与 F01、F02、F04--F06 已收束。正文保留 endpoint 与 19 维过程记录的区别，删除偏离主线的
  archived pair；Related Work、能力边界、reference registry、coverage 映射、逐组件 model card、exact replay
  定义和 agent provenance 已补齐。六图压缩为四图，14 页 arXiv PDF、source bundle 与 manifest 已集中验收。
- **DONE / 优势导向收束**：标题、摘要、引言、Related Work、Results、Discussion、Conclusion 与 model cards
  已围绕可组合世界、事务化生命周期、私有定律受控分叉、全面观测和精确重放重写；ChemGymRL、SDL、优化/
  控制套件、交互式科学世界、覆盖设计与计算 provenance 的 Related Work 已恢复并定位，补入互补能力比较表。
  生成块已严格拆分 topology novelty 与 exact task--world identity novelty，覆盖分母统一为 60/60、180/180、
  212/212 和 84/84；删除开发历史句和主图中的 token/cache accounting。14 页 PDF 完成逐页视觉检查；发布测试
  6 passed，图、作者与读者边界测试 11 passed，Ruff 与 diff 检查通过。
- **DONE / 作者元数据**：补入 Xiaonan Wang 为第三作者及通讯作者，共用 Tsinghua affiliation 1，公开通讯邮箱为
  `wangxiaonan@tsinghua.edu.cn`；规范源、arXiv TeX、PDF 与 source bundle 同步生成。
- **DONE / 审稿意见择要采纳**：删除读者可见的 `v1` 表述，压缩摘要数字，补入 executable/qualitative 语义边界、
  coverage 非穷尽说明、状态转移与 public/private projection 形式化、environment/action-trace replay taxonomy，
  并加入两个 agent-facing 交互例子；未新增 agent benchmark、多模型比较或三阶覆盖实验。
- **DONE / 最终清稿**：修正 Figure 4B 相对差异指标与方向判定说明，收紧软件实验底座资格表述，将具体
  provider/model 信息下沉到 Methods，补齐 runtime 事件/账本对象、Qualification scope 与 protocol 术语；
  规范源、四张可编辑 SVG、15 页 arXiv PDF、source bundle 和 manifest 已同步，18 项定向测试、Ruff、diff
  检查和关键页视觉检查通过。
- **DONE / 结果层次重构与全局清稿**：`Claim: Codex /root — A04-RESULTS-REFRAME — DONE`；将原第 4--7 节按
  “世界资格验证—过程完整与受控干预—Agent 契约接入”重组，消除 failure、replay 和非参考世界证据的跨节重复，
  同步统一摘要、贡献列表、Discussion、Methods、Conclusion 与测试断言；三张结果图已固定在对应证据章节，
  16 页 arXiv PDF、source bundle 和 manifest 已同次重建，12 项定向测试、Ruff、diff 检查及第 5--12 页视觉检查通过。
- **DONE / 最终 minor revision**：`Claim: Codex /root — FINAL-MINOR-POLISH — DONE`；收紧摘要中的 software-condition
  与 safety 表述，统一 substrate / executable world / public instrument contract 术语，补齐 Section 3.2 接受/拒绝事件
  形式化，压缩 ChemGymRL 比较，删除 Section 5.3 重复并将 Figure 4 后置到 Section 6.3；证据、结果结构与实验分母
  未改变。16 页 arXiv PDF、source bundle 与 manifest 已重建，12 项定向测试、Ruff、diff 检查及关键页视觉检查通过。
- **DONE / 发布前形式闭合与图件收口**：`Claim: Codex /root — FINAL-FORMAL-CLOSURE — DONE`；闭合
  public world / private mechanism、preflight rejection / post-execution rollback 和直接私有字段暴露的定义，新增
  controlled-fork 规格表与 19 个过程坐标表，并重做 Figure 1、修正 Figure 3/4 的原生可编辑矢量表达；未新增实验或改变
  分母。18 页 arXiv PDF、source bundle 与 manifest 已同次重建，14 项定向测试、Ruff、diff 检查及第 1、3--5、8--10、
  16 页视觉检查通过。
- **DONE / 最终 replay 与验证边界闭合**：`Claim: Codex /root — FINAL-REPLAY-BOUNDARY — DONE`；确认 exact replay
  重放完整 submitted action/transaction trace（失败案例 19/19 steps，含 1 个 rollback），从既有 192-probe 报告真实拆出
  128 个 `P=0` admission rejects 与 64 个 `P=1,C=0` runtime-precondition rollbacks，并明确 solver/observation fault 未有独立
  分母；同步统一 world/scenario/task--world identity、observation-RNG、fork 规律、过程坐标、Figure 1/2/4 和术语。19 页 arXiv
  PDF、source bundle 与 manifest 已同次重建；20 项定向测试、Ruff、diff 检查及关键页视觉检查通过。未新增实验、未改冻结
  分母、未虚构发布标识。
- **DONE / 最终 PDF 版面微调**：`Claim: Codex /root — FINAL-PDF-LAYOUT — DONE`；第五页 commit 公式改为双行，
  第十页 Figure 4 浮动顺序调整后消除空白右栏，Figure 4D 长标签重新断行；19 页规范 PDF、source bundle 与 manifest
  已同次重建，逐页缩略图及第 5、10、11 页高分辨率检查通过，19 项定向测试、Ruff 与 diff 检查通过。
- **DONE / 全面排版修复**：`Claim: Codex /root — FINAL-LAYOUT-COMPREHENSIVE — DONE`；统一双栏浮动参数、表格
  ragged-right 列型、标题间距和附录全宽块，消除 Figure 2/3 浮动页、第 7 页空白右栏、附录孤页/孤行及参考文献前后
  错序；规范 PDF 压缩为 18 页，且无 overfull 或未解析引用。PDF、source ZIP/TAR 与 manifest 已同次确定性重建，
  逐页缩略图及第 7、8、15--18 页高分辨率检查、14 项定向测试、diff 检查和重复构建哈希一致性均通过；未新增实验或改动冻结分母。
- **DEFERRED / 可选 Image 2 参考图**：WellAU Responses wire 的 bounded 生成探针未获得图像结果。Figure 1--3 现均按
  用户指示直接采用给定 PNG；Image 2 生成及三张主图的矢量重建不再阻塞发布。
- **当前 owner**：全部新工作由 `codex-1` 推进。旧文档或旧协议里的其他 owner 只表示历史提交者。
- **DONE / Claim**：`Claim: Codex /root — CENTRAL-QUESTION-LAYOUT-REFRAME — DONE`；在不改变冻结证据、
  实验分母或能力边界的前提下，将论文主轴提升为“世界构造本身成为受控实验变量”，同步重写标题、摘要、
  引言、贡献、章节标题、Discussion 与 Conclusion；合并读者能力图谱和使用案例以消除附录整栏空白，统一
  `Programmable Chemical Worlds` 页眉，并重建为 18 页 PDF。17 项论文/图件/发布测试、Ruff、无 overfull/
  未解析引用检查、关键页高分辨率视觉验收及连续两次构建的 PDF/source bundle/manifest 哈希一致性均通过。
- **DONE / Claim**：`Claim: Codex /root — FIGURE-INFORMATION-SWEEP — DONE`；按“每个面板必须提供不可由
  一句话或表格更清楚替代的独立信息”清扫主图，删除 Figure 2C/D、Figure 3C/D 和 Figure 4C/D 的重复通过率、
  PASS 卡片、资源占比与低信息时间线，将三张结果图收缩为横向双面板，并同步图注、正文、显示项和发布检查。
  规范 PDF 由 18 页压缩为 17 页，Figure 2/3 在第 7 页形成紧凑证据组，Figure 4 在第 9 页贴近 fork 结果；
  17 项论文/图件/发布测试、Ruff、diff 检查、无 overfull/未解析引用检查、逐页视觉验收和双构建哈希一致性均通过。
- **DONE / Figure 1 直接替换**：按用户指定的 `ChemWorld_Figure1_editable_16x9_01.png` 直接替换 Figure 1，
  不重做渲染器或矢量重建；同步更新图注、显示项、Figure manifest、17 页 PDF 和 source bundle。20 项定向测试、
  Ruff、diff 检查及第 3 页高分辨率视觉检查通过。
- **DONE / Figure 2 直接替换**：按用户指定的 `ChemWorld_Figure2_editable_16x9_01.png` 直接替换 Figure 2，
  不重做渲染器或矢量重建；同步更新四面板图注、显示项、Figure manifest、arXiv PDF 和 source bundle，并完成定向测试与视觉检查。
- **DONE / 主图精简与 Figure 3 直接替换**：删除信息已被正文、资格 census 和 Figure 1 覆盖的旧 Figure 3；
  新 Figure 3 按用户指定的 4:3 PNG 直接插入，以 A--C 三个面板展示冻结执行案例、失败回滚后的继续提交，以及受控私有定律分叉与独立 agent 生命周期。
- **DONE / Figure 2--3 原像素版面修复**：Figure 2（9599×5400）和 Figure 3（7200×5400）改用零边框、无插值的
  lossless PDF 包装，修复手工 page box 引起的偏移、裁切和图注覆盖；17 页 PDF 与 source bundle 同次重建，最终 PDF
  保留两张原始像素图，第 6、8 页高分辨率视觉检查确认边界完整且无文字覆盖；Figure manifest 工具只校验并绑定
  三张直接插入资产，不再运行旧绘图路径覆盖用户给定图件。
- **DONE / 统一附录结构**：将原 Appendix A--D 合并为一个 `Appendix` 主节，并保留 A--D 四个功能小节；移除
  表格 caption 中误用的 `Appendix D.` 前缀，使组件 model-card 表显示为正常的 `Table 10.` 标题。规范源、arXiv
  TeX/PDF、source bundle 与 build manifest 已同次重建并完成附录页视觉检查。
- **READY / 待独立公开仓库首推**：`Claim: Codex /root — PUBLIC-REPOSITORY-RELEASE — READY`；第一篇冻结代码、
  协议、机器报告、图件和 arXiv 包已整理到本地独立仓库 `sunyrain/ChemWorld-Public`，后续 benchmark/Work II
  配置、实验专用模块、运行结果和 provider payload 均未纳入；正文 Data and Code Availability 已改指该仓库。
  本地公开提交 `dc3dc30` 通过 87 项定向/集成测试、382 文件 release manifest、离线 denominator verifier
  与凭据扫描；arXiv PDF/source bundle 已同次重建。远端首推仍按约定等待用户明确确认。

## 1. 论文只讲什么

核心命题：

> ChemWorld 是一个可组合的可执行化学世界底座，也是可编程虚拟实验仪器。
> 它允许自主 agent 在世界中连续操作，并让过程、观测、资源、失败和终止决定
> 被结构化记录与精确重放。

第一篇需要建立四件事：

1. 世界由有限、声明清楚的 v1 组件词表与兼容规则构造，而不是由 15 个固定任务定义。
2. 组合空间是开放且可扩展的；15 个任务只是人工挑选的参考样例，不代表规模上限，
   也不构成对“无限任务”的穷举验证。
3. 组件、接口和运行时在覆盖引导的已见与未见组合中保持守恒、事务、观测、资源和重放语义。
4. 完整 agent 可以把这些世界当作实验仪器自主运行；本文展示仪器能记录什么，不解释 agent
   为什么这样行动，也不宣称通用智能、机制发现或物理实验室迁移。

推荐的一句话表述：

> We validate reusable process-model and transactional components, their declared interfaces,
> and coverage-guided compositions—not every possible task.

## 2. 必须统一的对象层级

- **组件**：反应、热、相、分离、结晶、蒸馏、连续流、电化学、观测等可复用模块。
- **完整世界**：`𝒲 = (W_pub, θ)`；`W_pub` 是公开组件拓扑、公开参数域和接口，`θ` 是评价器持有的私有定律、隐藏参数与私有初始化。
- **任务契约**：`T = (W_pub, S0_pub, A, I, O, R, τ, E)`，即公开世界描述、公开初态投影、操作、仪器、观测、
  资源、终止和评价的组合；完整私有世界身份不进入 Agent 契约。
- **场景**：一个任务契约下的具体参数、初态和随机实例。
- **轨迹**：agent 与该场景交互产生的操作—观测序列。
- **参考任务集**：15 个经过人工检查的示例，用来展示结构跨度和使用方式，不是 benchmark 全集。
- **世界分叉**：为了归因而只改变一个私有组件的受控实验；它不等于一般的多组件世界构造。

对外使用“在 v1 已声明组件词表和兼容域内的开放式构造”，不用“通用”“任意”或“已经验证无限任务”。

## 3. 执行清单

状态只用 `TODO / DOING / DONE / DEFERRED`。新实验块各写一份短说明即可，不建立 claim、租约、
逐任务审稿或手工哈希清单。

### A. 先锁定故事与构造契约

| ID | 状态 | 工作 | 完成标准 |
| --- | --- | --- | --- |
| A01 | DONE | 重写论文主张、术语和边界 | 摘要、引言、讨论使用同一套“世界底座 + 仪器”表述；15 个任务不再作为规模边界 |
| A02 | DONE | 写出 v1 世界组合语法 | 明确组件、参数、接口、兼容/排斥规则及任务契约；读者能区分世界、任务、场景、轨迹和分叉 |
| A03 | DONE | 建立当前能力表 | 一张读者可读表列出组件、可组合接口、连续参数、操作和仪器；不出现仓库文件名、SHA 或内部 ID |
| A04 | DONE | 重排论文结果结构 | 主结果按“构造—组合覆盖—接口/物理资格—受控分叉—agent 使用”组织，不按内部 Work I 流程组织 |

### B. 把“可组合世界”做成真实能力

| ID | 状态 | 工作 | 完成标准 |
| --- | --- | --- | --- |
| B01 | DONE | 统一世界构造入口 | 可从声明式契约构造合法世界并得到明确的公开操作、仪器、资源、终止和评价表面 |
| B02 | DONE | 实现兼容性检查 | 合法组合可编译；缺失依赖、冲突模块、单位不匹配和无效参数在执行前被清楚拒绝 |
| B03 | DONE | 实现覆盖引导的组合生成 | 离散轴采用 covering array，连续轴采用空间填充采样，操作流程覆盖关键有序交互；生成规模由覆盖目标决定而非声称穷举 |
| B04 | DONE | 补充公开 authoring 示例 | 单模块、跨模块、多阶段和受控分叉示例均由同一契约体系解释；U02/U03 的公开请求与冻结确定性路径均可执行闭环 |

### C. 世界与仪器资格实验（第一篇新增证据的核心）

先提交一份简短的组合资格实验说明，冻结覆盖规则、测试单位、检查项和失败处理；随后只运行一次正式资格批次。

| ID | 状态 | 工作 | 主要读出 |
| --- | --- | --- | --- |
| C00 | DONE | 冻结组合资格实验说明 | 在任何新数据生成前固定问题、测试单位、覆盖、测量、pass/failure 规则和机器可读输出；见 `experiments/first-paper-composition-qualification.md` |
| C01 | DONE | 参考任务结构覆盖 | 将 15 个任务重画为组件/接口/观测/资源/终止轴上的参考基，不再画成 15 行 benchmark 成绩表 |
| C02 | DONE | 覆盖引导的生成组合 | 报告有效组合数、覆盖到的轴与交互、成功编译/执行数及全部失败类别 |
| C03 | DONE | 冻结后的未见组合 | 在构造器与规则冻结后生成一批未出现在 15 个样例中的组合；不改核心运行时完成构造、执行和闭环 |
| C04 | DONE | 组合接口闭合 | 跨模块检查物质、单位、非负性、适用时的电荷/能量/相平衡、状态身份和事件传递 |
| C05 | DONE | 事务与资源语义 | 检查原子提交、失败不产生幽灵状态、耗材/时间/样品对账、终止后不可继续操作 |
| C06 | DONE | 观测边界与精确重放 | 公共观测不泄漏私有状态；同一已提交轨迹可重建相同世界转换和公开记录 |
| C07 | DONE | 无效组合与变异测试 | 系统性破坏依赖、单位、前置条件或资源约束，确认平台拒绝错误而不是静默运行 |
| C08 | DONE | 组合深度与运行开销 | 随组件数、阶段数和轨迹长度报告构造成功率、执行时间与记录体积，界定 v1 实际工作范围 |

这些检查以世界/组合为计数单位。确定性资格报告分子、分母和失败，不为通过率制造显著性检验，
也不为每个小步骤生成独立审计包。

### D. 化学合理性按“模块 + 接口”验证

| ID | 状态 | 工作 | 完成标准 |
| --- | --- | --- | --- |
| D01 | DONE | 模块级极限与单调性测试 | 对各物理模块检查零输入、极端输入、已知方向性、守恒和不变量 |
| D02 | DONE | 参考解或参考数据对照 | 对有成熟参考的模块给出数值误差/趋势对照；没有参考的模块明确标成合成或概念模型 |
| D03 | DONE | 跨模块传递验证 | 上游输出作为下游输入时单位、身份、数量和状态语义不漂移 |
| D04 | DONE | 划清物理效度边界 | 声明这是虚拟仪器资格，不把模块自洽性写成真实实验室预测效度 |

不需要对无限任务逐一做物理验证，也不为凑样例加入象征性的湿实验。验证可复用模块及接口即可。

### E. Agent 只作为仪器使用示例

| ID | 状态 | 工作 | 完成标准 |
| --- | --- | --- | --- |
| E01 | DONE | 保留一个确定性控制 | 展示世界、资源、失败、观测和终止如何被仪器记录 |
| E02 | DONE | 在未见生成世界上运行完整 agent | 证明 agent 可使用同一公开契约进入新组合世界并闭合生命周期；只作可用性展示 |
| E03 | DONE | 保留 endpoint 与过程可分辨性的论证 | 说明过程记录提供 endpoint 之外的信息；19 个维度保持分立，不合成“智能分数”；删除偏离主线的 archived pair |
| E04 | DONE | 压缩旧 agent 结果 | 多模型排名、行为机制、规则学习、跨模型归因和大规模 agent 统计全部移到第二篇 |

除非 C/E 暴露真实缺口，不再扩张广泛模型对比、16-world 行为研究或交互界面因果研究。

### U. 新增使用案例：展示仪器价值，不扩成 benchmark

每个案例只需说明科学问题、所用组件、agent 可见契约、可用操作/仪器、资源限制和产生的过程记录。
每个案例先有一条确定性参考轨迹；完整 agent 只需覆盖其中 1--2 个未见组合。

| ID | 状态 | 使用案例 | 论文价值与放置 |
| --- | --- | --- | --- |
| U00 | DONE | 锁定并修订 U01--U06 案例矩阵 | 六个案例的契约、证据角色和共用关系无歧义；U02/U03 路径已完成 pre-launch amendment，U05 与 C03 绑定同一冻结未见组合批次 |
| U01 | DONE | 多阶段反应到分离/结晶 | 展示反应、相态和下游纯化组成一个连续世界；主文候选 |
| U02 | DONE | 资源受限的结构/平衡表征 | 展示仪器选择、信息获取、样品消耗和停止决定；主文候选 |
| U03 | DONE | 失败、约束与恢复 | 展示前置条件、安全边界、失败回执、资源后果和后续恢复；主文或扩展图 |
| U04 | DONE | 同一公开仪器下的受控世界分叉 | 展示只改变私有定律而保持操作与观测合同；复用既有 fork 证据 |
| U05 | DONE | 覆盖生成的未见组合世界 | 展示不改核心运行时即可构造、执行、重放，并由完整 agent 闭合生命周期；主文必选 |
| U06 | DONE | 参考案例库 | 连续流、电化学、蒸馏、分配、结晶等更多样例放附录/公开文档，不逐个写成性能实验 |

#### U00 冻结案例矩阵

这一步只锁定案例设计，不产生新实验数据。每个案例先运行一条确定性参考轨迹；只有 U05 再运行一个
冻结的完整 agent 系统，且不设置比较组或模型排名。

| ID | 科学问题与世界 | Agent 可见契约 | 资源与确定性参考轨迹 |
| --- | --- | --- | --- |
| U01 | 上游反应质量如何传播到结晶、过滤和终检？使用 `reaction + thermal + crystallization + observation`，锚定 `reaction-to-crystallization`。 | 公开加料、加热、取样、HPLC、加晶种、冷却结晶、过滤、终止和 final assay；不公开私有动力学、材料身份或结晶定律。 | 使用任务合同的预算、时间、样品和仪器账本；参考轨迹由公开 task-recipe 中点向量确定，完整经过反应、两次过程测量、结晶、过滤和终检。 |
| U02 | 在极小操作与样品预算下，哪些测量足以表征一个有界平衡状态？使用 B04 的单一过程模块示例 `phase + observation`，objective 修订为 runtime 支持的 `balanced`。 | 公开建立可测样品所需的 `add_solvent`、`add_reagent`，以及 `measure` 与 `terminate`；仪器为 pH meter、UV--Vis 和 final assay，无反应或热操作表面。 | 冻结为 5 次操作、0.001 L 样品上限、3 次仪器使用和 1 次终检；参考路径为加溶剂、加试剂、pH 测量、显式终止、final assay，UV--Vis 保留为未选替代仪器。 |
| U03 | 无效前置条件或资源约束触发后，事务是否保持原子性，并允许从已提交状态继续恢复？使用 B04 的 `reaction + thermal + phase + separation + observation` 多阶段世界，objective 修订为 runtime 支持的 `balanced`。 | 公开反应、分相、洗涤、干燥、浓缩、转移、过程测量、终止和终检；失败返回结构化原因，不自动改写动作。 | 20 次操作、0.001 L 样品、3600 s、2 次仪器使用和 1 次终检；冻结 19 个 submitted actions：首步故意过早 `separate_phase` 必须回滚且保持物理状态，随后 18 步完成合法反应--分离--终检恢复路径。 |
| U04 | 只改变一个私有定律时，公开仪器契约是否保持不变而预注册状态/观测产生受控分歧？复用既有 single-private-component world forks。 | 父子世界公开同一操作、仪器、观测、资源、失败、终止和评分合同；agent 不见私有目标、世界身份或谱系。 | 父子双方使用同一冻结 typed-operation 序列、相同公共资源合同和精确 replay；记录单目标变化、公开不变性、预注册分歧与两侧重放，不新增模型调用。 |
| U05 | 一个在构造器冻结后生成、且不属于 15 个固定参考任务身份的世界，能否无核心补丁完成构造、确定性执行、完整 agent 生命周期与精确重放？使用 `reaction + thermal + distillation + observation`。 | 新 composition ID 下公开反应、蒸发、蒸馏、馏分收集、HPLC/GC/final assay、资源、终止和评价；完整 agent 只读取同一公开 task contract。 | 与 C03 共用一个 seeded 覆盖批次：离散轴冻结为 reaction family、fraction count、instrument profile 和 authored temperature/reflux ranges；连续 LHS 轴覆盖反应、蒸发、蒸馏的温度/时间、reflux ratio 与 transfer fraction；两条有序流程均闭合。全部 case 先跑确定性参考轨迹，完整 agent 主案例固定为生成顺序第一项，不按结果改选。 |
| U06 | 读者如何复用更多仪器形态而不把示例库误读成性能 benchmark？覆盖连续流、电化学、蒸馏、分配和结晶五类公开任务配方。 | 每个条目只给科学问题、组件、task card、公开操作/仪器、资源和观测边界；不提供跨任务总分或模型排序。 | 每类使用公开 task-recipe 中点向量生成一条确定性参考轨迹，并给出精确 replay 与资源摘要；详细样例进入附录/文档，主文只引用结构覆盖。 |

过程记录口径同时冻结：每个案例保存动作与 schema 判定、事务状态、公开观测、资源借贷、终止/评价、
轨迹重放结论和全部失败。U01 负责多阶段传播，U02 负责测量选择与资源约束，U03 负责失败和恢复，
U04 负责单私有组件归因，U05 负责未见组合与完整 agent，U06 负责可复用案例广度；不得用一个案例的
结果替代另一个证据角色。

U05/C03 的正式生成前必须在同一份资格实验说明中写出确切离散 levels、连续 bounds、seed、两条工作流、
case 数、资源上限与 pass/failure 规则。说明一旦冻结，不得因结果改变覆盖选择；若修复平台缺陷，整个
U05/C03 批次从头重跑并保留全部失败。

使用案例不是任务规模证明。主文选择 3 个互补案例，附录列更多案例；不要求把所有可能组合都展示出来。

### F. 稿件、图和发布收束

| ID | 状态 | 工作 | 完成标准 |
| --- | --- | --- | --- |
| F01 | DONE | 重写标题、摘要、引言和贡献 | 开头直接说明“开放组合但有限资格”的逻辑，避免读者追问为何只有 15 个任务 |
| F02 | DONE | 重写 Results/Methods/Discussion | 新资格实验成为主证据；agent profile 降为仪器应用案例；第二篇边界明确 |
| F03 | DONE | 重做主图 | Figure 1--3 按用户指定 PNG 直接插入；三张主图分别承担系统契约、组合空间，以及执行/干预/agent 接入证据，Image 2 参考图转为非阻塞的可选后续工作 |
| F04 | DONE | 整理附录 | 放完整组件表、兼容规则、覆盖矩阵、模块参考验证、失败类别和更多参考任务样例 |
| F05 | DONE | 清理读者无关内容 | 正文和图中不出现文件名、路径、SHA、commit、run ID、manifest、内部 task/release 名称 |
| F06 | DONE | 一次集中验收并导出 | 只做一次完整测试、一次图/PDF 视觉检查和一次内容边界检查，然后生成第一版发布包 |

## 4. 已有证据如何处理

以下内容继续复用，不重复跑：15 个参考任务、现有边界用例、typed operations 与 instruments、
资源账本、精确重放、单组件 world forks、known-policy controls、完整 agent 生命周期和已有过程差异示例。
它们是新故事中的基础材料，不再主导论文结构。

历史 discarded-state 缺陷如仍被正文使用，只需修复后做一次针对性资格验证；若从主叙事删除，
则保留为限制，不为它单独扩张整套实验。

## 5. 第一版的停止条件

以下条件满足即停止扩实验，进入集中收稿：

1. v1 组合语法和兼容域可公开说明，并有统一构造入口；
2. 覆盖引导组合与冻结后的未见组合完成，失败均有可解释归类；
3. 核心物理/事务/资源/观测/重放接口在测试组合中闭合；
4. 至少一个完整 agent 在未见生成世界中闭合生命周期；
5. 15 个任务已被明确重定位为参考样例；
6. 稿件与图完成一次集中验收，读者看不到内部工程元数据。

## 6. 暂不做

- 不验证“无限任务”，只验证构造语法、组件、接口和覆盖引导的组合；
- 不做通用 agent 排名、机制解释、belief revision 或 law learning；
- 不把模拟器自洽性写成真实化学实验室外部效度；
- 不做逐任务 claim、租约、重复 reviewer、重复全量测试、手工 SHA 清单或多套 manifest；
- 不再调用 Nature-specific skills；论文按内容选择期刊，不反向套用 Nature 叙事模板。

## 7. 立即执行顺序

1. 完成 A01--A04：先改论文契约和结构。
2. 完成 B01--B04：让“可组合世界”成为清楚、可用的发布能力。
3. 锁定 U01--U06 的案例矩阵，并让 U05 与 C03 共用同一批未见组合。
4. 写一份短实验说明并一次完成 C01--C08 与 D01--D04。
5. 完成 E01--E04：补一个未见世界 agent 使用例，压缩旧行为结果。
6. 完成 F01--F06：统一改稿、重画图、一次验收、发布即停。
