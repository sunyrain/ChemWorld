# ChemWorld 五年全面强化 TODO

本清单面向 2026-2031 年，把 ChemWorld 从可运行 benchmark 推进为专业级物理化学世界与自驱实验评测生态。

## Year 1：Benchmark 底座冻结

- 完成 `core/batch_reactor.py` 拆分，把 ODE、热量、相分配、分离、观测、评分逐步迁入 `chemworld.world`。
- 冻结 `WorldLawSpec`、`ScenarioSpec`、`TaskSpec`、trajectory schema、submission bundle schema。
- 为每个 task 生成 task card、scenario card、instrument card、baseline card。
- 已建立 official baseline report 生成器：`chemworld baselines report` 可按 task/agent/seed 输出 results、leaderboard 和 report metadata；正式发布前需用全量矩阵冻结结果。
- 已建立 signed private-eval artifact：`chemworld private-eval sign` 使用 hidden salt 生成 salt hash、运行日志、commit hash 和 HMAC 结果签名。
- 完成本机教师端/学生端评测机：submission inbox、verify、evaluate、leaderboard export。
- 已建立 v0.2 preprint artifact 生成器：`chemworld artifact create` 输出 task cards、schema snapshots、baseline tables、dataset examples 和复现实验脚本。

## Year 2：同一世界下扩展物理过程

- 已完成 crystallization module 基础版：晶种、冷却结晶、过滤、晶体纯度/收率/粒径 proxy；后续增强成核/生长/溶解模型。
- 已完成 evaporation/distillation module 基础版：蒸发、蒸馏、收馏分、馏分纯度/回收/能耗 proxy；后续增强挥发度与分离效率模型。
- 已完成 continuous-flow module 基础版：流速、停留时间、流动反应投影、flow conversion；后续增强停留时间分布与堵塞风险。
- 已完成 electrochemistry module 基础版：电位、电流、电解、选择性和能效 proxy；后续增强传质与副反应。
- 所有新过程必须共享 ontology、constitution、operation registry、instrument registry。
- 已新增 cross-process tasks：`reaction-to-crystallization`、`reaction-to-distillation`、`flow-reaction-optimization`、`electrochemical-conversion`；后续继续增加 reaction → purification → crystallization 复合任务。
- 引入 property-based tests，检查守恒、非负性、边界条件、seed reproducibility。

## Year 3：数据与 Agent 生态

- 引入 Minari 风格 dataset registry：dataset card、版本、license、privacy、provenance。
- 支持 Parquet/HDF5/Zarr sensor trace 数据。
- 发布官方 trajectory datasets：baseline、human pilot、LLM replay、BO campaigns。
- 建立 agent SDK：validator tool、recipe compiler、surrogate API、instrument planner、offline replay cache。
- 接入真实工具型 LLM baseline：搜索、文档、代码、validator、surrogate、实验语言规划。
- 建立 explanation rubric：机制假设、证据链、失败分析、下一实验理由。
- 形成外部 submission benchmark protocol 和公开 leaderboard review policy。

## Year 4：真实 grounding 与混合评测

- 用公开化学/化工数据校准部分 virtual worlds 的参数分布。
- 引入 expert review：机制解释、策略合理性、安全意识。
- 与真实 self-driving lab 或教学实验数据建立小规模对照，不宣称通用真实预测。
- 开发 hybrid backend：semi-mechanistic + empirical surrogate + optional external simulator adapter。
- 建立 public/private/generalization 三层评测：public-dev、public-test、private-eval。
- 支持 containerized student/agent sandbox，限制网络、时间、文件系统和外部 API。

## Year 5：国际 benchmark 生态

- 发布稳定 1.0：多物理过程、多 task family、多 baseline、多数据集。
- 建立年度 ChemWorld Challenge：固定任务、隐藏评测、报告模板、结果签名。
- 提供课程版 ChemWorld-Edu：12-15 天 notebook、教师端、评分 rubric、匿名化流程。
- 提供研究版 ChemWorld-Bench：SDK、CLI、dataset registry、private eval protocol。
- 与 DiscoveryWorld、ChemGymRL、Safety-Gymnasium、Minari 风格生态对齐接口。
- 形成可引用 benchmark paper、dataset paper、education paper、agent competition report。

## Cross-Cutting TODO

- **物理宪法**：持续增强 material balance、energy balance、phase balance、safety boundary。
- **状态账本**：让 species、phase、vessel、instrument、cost、risk、time、sample 全部可回放。
- **Schema 单源**：所有 JSON schema 由 Python 常量生成或被测试锁定，避免漂移。
- **私有评测**：private parameters 不入库，只发布签名结果和可复现实验摘要。
- **安全伦理**：学生数据知情同意、匿名化、教学评分与科研使用分离。
- **工程质量**：ruff、mypy、pytest、docs build、notebook smoke、baseline smoke 全进 CI。
- **文档治理**：每次 API/task/schema 变化必须同步 architecture、task cards、release checklist。
