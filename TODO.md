# ChemWorld Unified TODO

最后更新：2026-07-09

本文件是 ChemWorld 唯一活跃任务板。所有开发、发布、专业物理模型深化、notebook、站点和本地评测机任务都收束到这里。`docs/todo.md` 只保留公开摘要，不作为第二份工作板维护。

## 1. 当前结论

ChemWorld 当前已经完成 **最小可信 benchmark** 的 P0/P1 收束：核心任务、baseline、submission、replay、release gate、runtime boundary audit、ledger audit、public leakage audit 和环境自洽性审计已经闭环。

下一步不应继续扩散新概念，而是完成两个方向：

1. **公开预发布包**：先完成 P2 agent-facing 交互与数据集，再直接完成 P4 文档/notebook/站点。
2. **长期专业化路线**：P3 专业物理化学模块深化暂缓，不阻塞当前公开预发布。

## 2. 当前统计

| 阶段 | 目标 | 总数 | Done | Claimed | Open | Blocked | 剩余 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| P0 | 预发布 benchmark hardening | 12 | 12 | 0 | 0 | 0 | 0 |
| P1 | runtime 与环境自洽性 | 8 | 8 | 0 | 0 | 0 | 0 |
| P2 | agent-facing 交互与数据集 | 6 | 6 | 0 | 0 | 0 | 0 |
| P3 | 专业物理化学深化 | 27 | 0 | 3 | 24 | 0 | 27 |
| P4 | 文档、notebook、站点与发布包装 | 5 | 5 | 0 | 0 | 0 | 0 |
| **合计** |  | **58** | **31** | **3** | **24** | **0** | **27** |

还需要完成 **27 项**：

- **0 项**用于公开预发布：P2/P4 已完成。
- **27 项**用于长期专业化深化：P3 全部 27 项，其中 3 项已由 `liyijun` 认领。
- 当前没有 `Active` 或 `Blocked` 项。

## 3. Cutline

| Cutline | 还差 | 判定标准 |
| --- | ---: | --- |
| 最小可信 benchmark | 0 | P0/P1 全部完成。任务、runtime、ledger、observation、scoring、replay 和公开边界通过审计。 |
| 可公开预发布包 | 0 | P2/P4 已完成。外部用户能安装、运行、提交、阅读文档、复现实验、理解限制。 |
| 全部可见路线图 | 27 | 完成 P3。包含长期专业物理化学模块深化。 |

## 4. 推荐执行顺序

公开预发布包装已经完成。P3 不阻塞公开预发布，当前按用户要求暂缓。

## 5. 协作规则

- 默认在 `main` 开发。
- 开始非平凡任务前先 `git pull --ff-only origin main`。
- 一次只把一个任务标为 `Active`。
- 已由别人标为 `Claimed` 的任务不要重复实现，除非明确重新分配。
- 完成一个任务后立即更新本文件、运行相关门禁、提交并推送。
- `docs/todo.md` 只同步摘要，不作为第二份任务板。
- 不把 `proxy`、`lite`、`reference_validated` 或 `professional-candidate` 混写成 `professional`。
- 每个 `Done` 项必须有代码、测试、文档，或明确的 no-test rationale。

状态定义：

| 状态 | 含义 |
| --- | --- |
| Open | 可开始 |
| Claimed | 已由 owner 预留，但尚未实现 |
| Active | 正在实现 |
| Review | 已推送，等待审查 |
| Done | 已实现、已验证、已更新 TODO、已推送 |
| Blocked | 有明确阻塞条件 |

## 6. 当前系统基线

已具备能力：

- 正式 Gymnasium 入口是 `gym.make("ChemWorld", task_id=...)`。
- 所有正式 task 指向同一个 `world_law_id`。
- 已有 task registry、scenario/profile/mechanism/scoring hash、submission bundle、paper artifact 和 local release gate。
- Runtime v2 概念已进入代码：typed ledger、transaction record、operation kernel、domain service、compiled mechanism、observation/scoring contract、replay verifier。
- Ledger single-source audit 已进入 constitution check 和环境审计。Phase ledger 是物料主来源；process ledger 是时间、成本、风险和样品消耗主来源；metadata 不允许保存 primary structured state。
- Agent-facing API 已具备基础入口：task prompt、available actions、action schema、validation、RL/tool-JSON/lab-report observation view、campaign state。
- 已有本地教师端/学生端评测机模拟。
- MkDocs 站点已发布，但 P4 仍需围绕预发布 benchmark 重组结构、增强教程和补齐端到端 notebook。

边界声明：

- ChemWorld 不是实际反应预测软件。
- ChemWorld 不是完整流程模拟器。
- ChemWorld 当前还不是通用化学 world model。
- ChemWorld 当前是机制驱动、可交互、可回放、可评测的虚拟物理化学 benchmark 环境。
- P3 professional deepening 是长期工作，必须带明确 maturity label、验证算例和失败边界。

## 7. P0 - 预发布 Benchmark Hardening

目标：让第一版公开 benchmark 小而可信，可复现、可提交、可引用。

冻结核心任务：

- `reaction-to-assay`
- `reaction-to-purification`
- `partition-discovery`

| ID | Owner | Status | Task | Exit Criteria |
| --- | --- | --- | --- | --- |
| P0-BENCH-01 | Codex | Done | Freeze the three-task pre-release contract | Task cards specify objective, budget, allowed operations, instruments, seeds, score metrics, safety limits, maturity tags, and expected qualitative behavior. |
| P0-BENCH-02 | Codex | Done | Build official seed suite | `chemworld seeds show` exposes the pre-release seed suite, public-dev/public-test seeds, private-eval salt policy, and suite/baseline CLI paths load the official plan unless explicit smoke seeds are provided. |
| P0-BENCH-03 | Codex | Done | Generate official baseline table | `chemworld baselines report` runs random, scripted, BO, safe BO, ToolUsingLLMStub, and LLMReplay across frozen task seeds; baseline docs report mean, stderr, invalid rate, final-assay count, and AUC. |
| P0-BENCH-04 | Codex | Done | Calibrate BO budgets and initial samples | BO acquisition diagnostics are recorded in traces, metrics, baseline summaries, tests, and docs; GP-BO/safe GP-BO enter acquisition under default budgets and outperform random without saturating score. |
| P0-BENCH-05 | Codex | Done | Lock golden trajectories | Golden scripted trajectories for the three pre-release tasks compare actions, observations, rewards, transaction metadata, final assay output, and final metrics. |
| P0-BENCH-06 | Codex | Done | Audit scoring contracts | `audit_scoring_contract` recomputes observation score, reward, observed reward, final-assay leaderboard score, processed metric alignment, scoring contract hash, and evaluate-record final best score. |
| P0-BENCH-07 | Codex | Done | Harden replay verifier | `verify_records` catches tampered mechanism hash, scoring hash, profile hash, reward, observation, operation metadata, runtime transaction status, world events, state patch summaries, and early-termination replay drift. |
| P0-BENCH-08 | Codex | Done | Build one valid submission bundle example | `chemworld submission example` and `examples/demo_submission_bundle.py` generate a complete bundle with manifest, trajectories, results, explanations, dependencies, README, validation, summary, and replay verification. |
| P0-BENCH-09 | Codex | Done | Build local teacher/student evaluation smoke | Local teacher-side evaluator supports init-demo, validate, run, aggregate, summarize, and demo over a simulated student sandbox. |
| P0-BENCH-10 | Codex | Done | Produce benchmark paper artifact skeleton | `chemworld artifact create` generates task cards, contracts, scenario/world-law snapshots, schemas, baseline report, example trajectory, dataset card, replay manifest, release manifest, checklist, environment summary, and reproduction script. |
| P0-BENCH-11 | Codex | Done | Add CI-like local release command | `scripts/run_release_gate.py` runs lint, type check, tests, docs build, full environment audit, and baseline smoke. |
| P0-BENCH-12 | Codex | Done | Write pre-release limitations statement | Docs and paper artifacts include a virtual semi-mechanistic scope, maturity boundary, non-real-predictor statement, proxy/lite surface, and release-gate requirement. |

## 8. P1 - Runtime 与环境自洽性

目标：actions、ledgers、observations、spectra、scoring、logs、replay 和 docs 必须互相一致。

| ID | Owner | Status | Task | Exit Criteria |
| --- | --- | --- | --- | --- |
| P1-CONSIST-01 | Codex | Done | Run and document environment self-consistency audit | Full audit covers 14 formal tasks over seeds 0/1/2 with task/profile/mechanism/scoring/observation hash coverage, replay verification, and documented warnings. |
| P1-CONSIST-02 | Codex | Done | Spectra-metric semantic alignment | Downstream final assay spectra use selected-phase public species calibration; full audit reports zero spectra failures and zero spectra warnings. |
| P1-CONSIST-03 | Codex | Done | Action affordance consistency | `available_actions`, ActionMaskWrapper, OperationValidator affordance, task policy, operation registry, and action masks are covered by cross-task tests. |
| P1-CONSIST-04 | Codex | Done | Invalid action atomicity | Schema, task-policy, payload-bound, and state-precondition failures are covered by material-ledger atomicity tests; invalid actions only mutate process/cost/risk ledgers and emit explicit validation or rollback metadata. |
| P1-CONSIST-05 | Codex | Done | Campaign vs single-experiment semantics audit | Tests cover all task termination policies; single-experiment final assay terminates and campaign final assay records experiment summaries while keeping the Gym episode alive when budget remains. |
| P1-CONSIST-06 | Codex | Done | Ledger single-source-of-truth audit | `audit_ledger_single_source_of_truth()` is part of constitution state checks and release audit; tests cover material totals, process compatibility, metadata rejection, reference closure, and all formal task smoke trajectories. |
| P1-CONSIST-07 | Codex | Done | Public observation leakage audit | `audit_public_payload()` scans reset info, task info, observations, step info, tool JSON, lab reports, agent views, spectra labels, and JSONL trajectories; public task info no longer exposes mechanism manifest, reactions, compiled mechanism, mechanism observable mapping, hidden scenario seeds, hidden species ids, or rate constants unless `debug_truth=True`; full environment audit reports `public_leakage_failures=0`. |
| P1-CONSIST-08 | Codex | Done | Runtime boundary scan | `scripts/audit_runtime_boundary.py` and `audit_runtime_boundaries()` verify that `ChemWorldEnv` delegates valid and invalid actions to runtime transactions, does not access `runtime.domain_services`, does not branch on specific operation names inside `step()`, and runtime-facing source does not import legacy `chemworld.core` modules. |

## 9. P2 - Agent-Facing 交互与数据集

目标：RL、BO、LLM 和学生 agent 不需要读内部源码，也能规划、验证、执行、恢复和复现。

| ID | Owner | Status | Task | Exit Criteria |
| --- | --- | --- | --- | --- |
| P2-AGENT-01 | Codex | Done | Polish `task_prompt()` for the three pre-release tasks | Prompts include objective, constraints, hidden-info policy, success criteria, and allowed tools in concise human-readable form; three pre-release prompts now expose structured task_goal, constraints, success_criteria, allowed_tools, measurement_policy, recommended_strategy, failure_modes, and public-leakage tests. |
| P2-AGENT-02 | Codex | Done | Improve lab-report summaries | Failed actions, spectra packets, final assay, campaign progress, and recovery suggestions are deterministic and derived only from public observations; lab reports now expose visible_metrics, instrument_summary, spectra_summary, final_assay_summary, campaign_progress, failure_summary, next_action_hints, and recovery_suggestion. |
| P2-AGENT-03 | Codex | Done | Stabilize RL observation view | Vector, mask, cost channel, bounds, and NaN-safe behavior are documented and covered by tests; RL view now exposes schema_version, stable keys, missing-value sentinel, finite value/mask bounds, cost channel, and wrapper Box space built from the same spec. |
| P2-AGENT-04 | Codex | Done | Add agent trace to dataset export examples | Prompt summary, selected action, validation result, observation summary, reasoning summary, hypothesis note, and memory note are exported through trajectory JSONL and flattened dataset records; `examples/demo_dataset_agent_trace_export.py` runs a deterministic tool-agent export and handles optional Parquet backends. |
| P2-AGENT-05 | Codex | Done | Multi-round ToolUsingLLMStub probe | `scripts/probe_tool_agent_rounds.py` and `chemworld.eval.agent_probe.run_tool_agent_probe()` run `ToolUsingLLMStubAgent` for 12+ rounds over seeds 0/1/2, emit JSON/CSV reports, record best-score AUC, invalid action rate, precondition recovery, final assay count, observation-use summary, and trajectory paths. |
| P2-AGENT-06 | Codex | Done | LLMReplay benchmark fixture | `examples/fixtures/llm_replay/reaction_to_assay_public_trace.jsonl` is a fixed public reasoning/action trace; tests verify deterministic action sequence, final assay scores, evaluation metrics, validator result, observation summary, hypothesis note, and memory note under the same seed. |

## 10. P3 - 专业物理化学深化

目标：把 proxy/lite 物理化学模块逐步替换为范围明确、可审计、可验证的专业模型切片。

规则：

- P3 不阻塞第一版公开预发布。
- `liyijun` 已认领的三项不得重复实现，除非重新分配。
- 每个 P3 任务必须包含 maturity label、适用范围、验证算例和失败边界。

| ID | Owner | Status | Task | Exit Criteria |
| --- | --- | --- | --- | --- |
| DEEP-D1A | liyijun | Claimed | Component identity registry | Aliases, CAS/InChI-like placeholders, formula, charge, molecular weight, provenance, duplicate checks, JSON round-trip. |
| DEEP-D1B | liyijun | Claimed | Unit-dimension checker | Canonical dimensions for amount, mass, volume, temperature, pressure, energy, transport properties, and instrument response. |
| DEEP-D1C | liyijun | Claimed | Data conflict policy | Deterministic source priority, uncertainty fields, warning vs hard-fail reports, dataset-card provenance. |
| DEEP-D4B |  | Open | LLE phase-split solver | TPD-style heuristic, initialization policy, mass-balance checks, extraction-task integration. |
| DEEP-D4C |  | Open | Aqueous acid-base equilibrium | Charge balance, activity simplifications, pH observation kernel, precipitation hooks. |
| DEEP-D4D |  | Open | Gibbs-minimization toy solver hardening | Small stoichiometric examples with convexity and constraint diagnostics. |
| DEEP-D5A |  | Open | Thermochemistry-coupled reversibility | Equilibrium constants from standard-state Gibbs energy, detailed balance, reactor ODE integration. |
| DEEP-D5B |  | Open | Pressure-dependent and falloff kinetics | Troe/Lindemann-style compact slice, third-body efficiencies, validation cases. |
| DEEP-D6B |  | Open | CSTR dynamics | Dynamic mass/energy balance, residence time, stability, startup/shutdown, multiple steady states. |
| DEEP-D6C |  | Open | PFR/plug-flow slice | Axial integration, pressure-drop coupling, heat-transfer boundary, validation cases. |
| DEEP-D6D |  | Open | Solver backend interface | Deterministic tolerances, event handling, failure diagnostics, replay verification. |
| DEEP-D7A |  | Open | Rigorous flash unit | Material and energy balance, vapor-liquid split, enthalpy duty, nonideal hooks. |
| DEEP-D7C |  | Open | Extraction unit | Distribution coefficients from activity/partition model, entrainment, wash sequence, recovery/purity metrics. |
| DEEP-D7D |  | Open | Crystallization unit | Solubility curve, supersaturation, nucleation/growth compact model, impurity occlusion, CSD metadata. |
| DEEP-D8A |  | Open | Phase-change and equipment heat transfer | Boiling/condensation warnings, jacket/coil/shell corrections, fouling evolution, energy-ledger validation. |
| DEEP-D8B |  | Open | Two-phase pressure drop | Documented correlation slice with validity limits replacing homogeneous proxy. |
| DEEP-D8C |  | Open | Relief and safety envelope | Pressure/temperature hazard envelopes, runaway indicators, safety-cost integration. |
| DEEP-D8D |  | Open | Equipment cards | Vessel, pump, mixer, condenser, heat exchanger, and column specs with constraints. |
| DEEP-D9A |  | Open | Empirical HPLC/GC method sensitivity | Retention-index examples, temperature/mobile-phase sensitivity, detector response calibration, asymmetric peak flags. |
| DEEP-D9C |  | Open | NMR slice | Chemical shift anchors, multiplicity/coupling metadata, integration, solvent reference, failure modes. |
| DEEP-D9D |  | Open | MS slice | Simple fragmentation metadata, isotope envelopes for small formulas, detector response uncertainty. |
| DEEP-D10C |  | Open | Reference-baseline reports | Task-specific official tables, seed confidence intervals, public/private generalization gaps. |
| DEEP-D10D |  | Open | Solver/provenance manifest | Commit hash, dependency lock, optional backend versions, tolerances, hidden-scenario salt policy. |
| DEEP-D11B |  | Open | Mass-transfer limiting-current slice | Diffusion-layer approximation, limiting current, depletion, current-efficiency loss, analytical plateau checks. |
| DEEP-D11C |  | Open | Potentiostatic and galvanostatic controllers | Controller semantics, clipping, ramp/hold recipes, operation logs, replay contracts. |
| DEEP-D11D |  | Open | Double-layer and capacitive-current slice | RC transient, non-Faradaic current, startup artifacts, current-trace observations. |
| DEEP-D11E |  | Open | Electrochemical scenario cards | Redox metadata, electrode area, electrolyte window, side-reaction thresholds, hidden-parameter generation. |

## 11. P4 - 文档、Notebook、站点与发布包装

目标：让外部用户能快速理解稳定能力，并能完成端到端实验复现。

| ID | Owner | Status | Task | Exit Criteria |
| --- | --- | --- | --- | --- |
| P4-DOCS-01 | Codex | Done | Reorganize docs around pre-release benchmark | Site first explains stable entry points, benchmark contract, agent access, data/artifacts, world foundation, audits, and release boundaries; center language buttons are removed in favor of the top language switch, and the left navigation/right outline roles are documented. |
| P4-DOCS-02 | Codex | Done | Build a concise architecture report from current code | `docs/architecture_report.md` summarizes the current main-branch architecture: package layers, Gym step path, Runtime v2, mechanism compiler, typed ledgers, agent-facing API, evaluation/data outputs, and explicit limitations. |
| P4-DOCS-03 | Codex | Done | Harden 12-day tutorial workload | `scripts/audit_tutorial_workload.py` and `tests/test_tutorial_notebooks.py` enforce Day 1-12 half-hour timeboxes, three-hour work orders, student workspaces, minimum experiment/submission thresholds, evidence markers, and no garbled or helper-based checkpoints. |
| P4-DOCS-04 | Codex | Done | Add three end-to-end notebooks | `notebooks/end_to_end/` contains reaction-to-assay, reaction-to-purification, and partition-discovery notebooks with planning, validation, execution, spectra, metrics, and reflection. They are generated by a UTF-8 builder, structure-tested, mojibake-scanned, and executed with nbconvert. |
| P4-DOCS-05 | Codex | Done | Finalize release checklist page | `docs/release_checklist.md` now defines release gates, benchmark contracts, artifacts, known limitations, private-eval policy, citation guidance, and stop-release conditions. |

## 12. 任务门禁

按任务类型运行对应检查：

| 任务类型 | 必跑检查 |
| --- | --- |
| Python/runtime | `python -m ruff check .`; `python -m mypy src/chemworld`; `python -m pytest` |
| Env/benchmark/replay | 上述检查 + `python scripts/audit_environment_consistency.py --tasks all --seeds 0 1 2` |
| Docs/site | `python -m mkdocs build --strict` |
| Release-level | `python scripts/run_release_gate.py` |

## 13. 已合并并废弃的旧任务板

以下任务板已合并到本文件，不再单独维护：

- `TODO_PROFESSIONAL.md`
- `TODO_PROFESSIONAL_DEEPENING.md`

如果任何文档页面与本文件冲突，以本文件为准。
