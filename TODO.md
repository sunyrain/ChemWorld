# ChemWorld 统一 TODO

最后更新：2026-07-09

本文件是 ChemWorld 唯一活跃任务板。此前的发布、专业化、模型深化和站点任务板已经收束到这里。站点中的 `docs/todo.md` 只保留摘要，不作为第二份工作板维护。

## 0. 当前结论

当前 ChemWorld 已经不是“缺少功能入口”的阶段，而是进入 **benchmark trust hardening** 阶段：需要继续把任务合同、评分、回放、提交包、agent 交互、文档和成熟度边界做实。

当前剩余工作：

- 总任务 58 项。
- 已完成 17 项。
- 进行中 1 项。
- 已认领 3 项。
- 待开始 37 项。
- 剩余 41 项。

三个 cutline：

| Cutline | 剩余 | 含义 |
| --- | ---: | --- |
| 最小可信 benchmark | 3 | 完成全部 P0/P1 后，三项冻结任务的 replay、scoring、ledger、observation、runtime 边界才算基本可信 |
| 可公开预发布包 | 14 | 完成 P0/P1/P2/P4 后，外部用户可安装、运行、提交、阅读文档和复现实验 |
| 全部可见路线图 | 41 | 包含长期专业物化深化，不应阻塞第一版公开预发布 |

当前应优先完成：

1. `P1-CONSIST-06`：ledger single-source-of-truth audit。
2. `P1-CONSIST-07`：public observation leakage audit。
3. `P1-CONSIST-08`：runtime boundary scan。

## 1. 进度统计

| 范围 | 总数 | 已完成 | 进行中 | 已认领 | 待开始 | 剩余 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| P0 预发布 benchmark hardening | 12 | 12 | 0 | 0 | 0 | 0 |
| P1 runtime 与环境自洽性 | 8 | 5 | 1 | 0 | 2 | 3 |
| P2 agent-facing 交互与数据集 | 6 | 0 | 0 | 0 | 6 | 6 |
| P3 专业物理化学深化 | 27 | 0 | 0 | 3 | 24 | 27 |
| P4 文档、notebook、站点与发布包装 | 5 | 0 | 0 | 0 | 5 | 5 |
| Total | 58 | 17 | 1 | 3 | 37 | 41 |

## 2. 当前系统状态

已经完成并可作为当前基线的部分：

- 正式 Gymnasium 入口统一为 `gym.make("ChemWorld", task_id=...)`。
- 所有正式 task 指向同一个 `world_law_id`。
- 已建立 task registry、scenario/profile/mechanism/scoring hash、submission bundle、paper artifact、local release gate。
- Runtime v2 的主要概念已经进入代码：typed ledger、transaction record、operation kernel、domain service、compiled mechanism、observation/scoring contract、replay verifier。
- Agent-facing API 已具备基础入口：task prompt、available actions、action schema、validation、RL/tool JSON/lab report observation view、campaign state。
- 已有本地教师端/学生端评测机模拟。
- MkDocs 站点已发布，但 P4 仍需继续压缩结构、增强教程和补齐端到端 notebook。

仍需明确的边界：

- 当前不是真实反应预测软件。
- 当前不是完整流程模拟器。
- 当前不是通用化学世界模型。
- 当前是机制驱动、可交互、可回放、可评测的虚拟物理化学 benchmark 底座。
- P3 的 professional physchem deepening 是长期工作，不阻塞第一版公开预发布，除非某个冻结 task 明确依赖该模型。

## 3. 协作规则

- 从 `main` 开发。
- 开始非平凡任务前先拉取远端。
- 每次只把一个任务标记为 `Active`。
- 任务完成后立即更新本文件、提交并推送。
- 已由他人 `Claimed` 的任务不要重复实现，除非显式重新分配。
- 不维护第二份活跃 TODO。
- 不把 `proxy`、`lite` 或 `professional-candidate` 模型写成 `professional`。
- 每个 `Done` 项必须有代码、测试、文档，或明确的 no-test rationale。

状态定义：

| 状态 | 含义 |
| --- | --- |
| Open | 可以开始 |
| Claimed | 已由 owner 预留，但尚未实现 |
| Active | 正在实现 |
| Review | 已推送，等待审查 |
| Done | 已实现、已验证、已更新 TODO、已推送 |
| Blocked | 有明确阻塞条件 |

## 4. 下一轮执行顺序

最短路径是先完成 P1，然后进入 P2/P4：

1. `P1-CONSIST-06`：补齐 ledger single-source-of-truth audit，确认 material/equipment/process/vessel 主状态不落回 metadata。
2. `P1-CONSIST-07`：审计 public observation、tool JSON、lab report、spectra label、trajectory 是否泄露 hidden species id 或 rate constants。
3. `P1-CONSIST-08`：扫描 runtime 边界，确认 `ChemWorldEnv` 保持薄层，不再出现 operation-specific dispatch 或 legacy core runtime 回流。
4. `P2-AGENT-*`：让 RL/BO/LLM/student agent 不需要读源码也能规划、验证、执行、恢复和复现。
5. `P4-DOCS-*`：收束站点和教程，只展示已测试能力，不让文档超过代码。

## P0：预发布 Benchmark Hardening

目标：第一版公开 benchmark 小而可信，可复现、可提交、可引用。

冻结核心任务：

- `reaction-to-assay`
- `reaction-to-purification`
- `partition-discovery`

| ID | Owner | Status | Task | Exit Criteria |
| --- | --- | --- | --- | --- |
| P0-BENCH-01 | Codex | Done | Freeze the three-task pre-release contract | Task cards specify objective, budget, allowed operations, instruments, seeds, score metrics, safety limits, maturity tags, and expected qualitative behavior |
| P0-BENCH-02 | Codex | Done | Build official seed suite | `chemworld seeds show` exposes the pre-release seed suite, public-dev/public-test seeds, private-eval salt policy, and suite/baseline CLI paths load the official plan unless explicit smoke seeds are provided |
| P0-BENCH-03 | Codex | Done | Generate official baseline table | `chemworld baselines report` runs random, scripted, BO, safe BO, ToolUsingLLMStub, and LLMReplay across frozen task seeds; `baseline_summary_table.json` and docs report mean, stderr, invalid rate, final-assay count, and AUC |
| P0-BENCH-04 | Codex | Done | Calibrate BO budgets and initial samples | BO acquisition diagnostics are recorded in agent traces, metrics, baseline summaries, tests, and docs; GP-BO/safe GP-BO enter acquisition under default budgets and outperform random without saturating score |
| P0-BENCH-05 | Codex | Done | Lock golden trajectories | `tests/fixtures/golden/pre_release_scripted_trajectories.json` locks scripted trajectories for the three pre-release tasks; tests regenerate summaries and compare actions, observations, rewards, transaction metadata, final assay output, and final metrics |
| P0-BENCH-06 | Codex | Done | Audit scoring contracts | `audit_scoring_contract` recomputes observation score, reward, observed reward, final-assay leaderboard score, processed metric alignment, scoring contract hash, and evaluate-record final best score |
| P0-BENCH-07 | Codex | Done | Harden replay verifier | `verify_records` catches tampered mechanism hash, scoring hash, profile hash, reward, observation, operation metadata, runtime transaction status, world events, state patch summaries, and early-termination replay drift |
| P0-BENCH-08 | Codex | Done | Build one valid submission bundle example | `chemworld submission example` and `examples/demo_submission_bundle.py` generate a complete bundle with manifest, trajectories, results, explanations, dependencies, README, validation, summary, and replay verification |
| P0-BENCH-09 | Codex | Done | Build local teacher/student evaluation smoke | Local teacher-side evaluator supports init-demo, validate, run, aggregate, summarize, and demo over a simulated student sandbox |
| P0-BENCH-10 | Codex | Done | Produce benchmark paper artifact skeleton | `chemworld artifact create` generates task cards, contracts, scenario/world-law snapshots, schemas, baseline report, example trajectory, dataset card, replay manifest, release manifest, checklist, environment summary, and reproduction script |
| P0-BENCH-11 | Codex | Done | Add CI-like local release command | `scripts/run_release_gate.py` runs lint, type check, tests, docs build, full environment audit, and baseline smoke |
| P0-BENCH-12 | Codex | Done | Write pre-release limitations statement | Docs and paper artifacts include a clear virtual semi-mechanistic scope, maturity boundary, non-real-predictor statement, proxy/lite surface, and release-gate requirement |

## P1：Runtime 与环境自洽性

目标：actions、ledgers、observations、spectra、scoring、logs、replay、docs 讲同一个故事。

| ID | Owner | Status | Task | Exit Criteria |
| --- | --- | --- | --- | --- |
| P1-CONSIST-01 | Codex | Done | Run and document environment self-consistency audit | Full audit covers 14 formal tasks over seeds 0/1/2 with task/profile/mechanism/scoring/observation hash coverage, replay verification, and documented warnings |
| P1-CONSIST-02 | Codex | Done | Spectra-metric semantic alignment | Downstream final assay spectra use selected-phase public species calibration; full audit reports zero spectra failures and zero spectra warnings |
| P1-CONSIST-03 | Codex | Done | Action affordance consistency | `available_actions`, ActionMaskWrapper, OperationValidator affordance, task policy, operation registry, and action masks are covered by cross-task tests |
| P1-CONSIST-04 | Codex | Done | Invalid action atomicity | Schema, task-policy, payload-bound, and state-precondition failures are covered by material-ledger atomicity tests; invalid actions only mutate process/cost/risk ledgers and emit explicit validation or rollback metadata |
| P1-CONSIST-05 | Codex | Done | Campaign vs single-experiment semantics audit | Tests cover all task termination policies; single-experiment final assay terminates and campaign final assay records experiment summaries while keeping the Gym episode alive when budget remains |
| P1-CONSIST-06 | Codex | Active | Ledger single-source-of-truth audit | Material amounts come from typed phase ledgers; equipment/process/vessel state does not fall back to metadata |
| P1-CONSIST-07 |  | Open | Public observation leakage audit | Agent-visible observations, tool JSON, lab reports, spectra labels, and trajectories do not expose hidden species ids or rate constants |
| P1-CONSIST-08 |  | Open | Runtime boundary scan | `ChemWorldEnv` remains thin, no operation-specific if/elif dispatch returns, and runtime does not import legacy core modules |

## P2：Agent-Facing 交互与数据集

目标：RL、BO、LLM 和学生 agent 不需要读内部源码，也能规划、验证、执行、恢复、复现。

| ID | Owner | Status | Task | Exit Criteria |
| --- | --- | --- | --- | --- |
| P2-AGENT-01 |  | Open | Polish `task_prompt()` for the three pre-release tasks | Prompts include objective, constraints, hidden-info policy, success criteria, and allowed tools in concise human-readable form |
| P2-AGENT-02 |  | Open | Improve lab-report summaries | Failed actions, spectra packets, final assay, campaign progress, and recovery suggestions are deterministic and public-observation-only |
| P2-AGENT-03 |  | Open | Stabilize RL observation view | Vector, mask, cost channel, bounds, and NaN-safe behavior are documented and covered by tests |
| P2-AGENT-04 |  | Open | Add agent trace to dataset export examples | Prompt summary, selected action, validation result, observation summary, and memory note are exported in JSONL/Parquet |
| P2-AGENT-05 |  | Open | Multi-round ToolUsingLLMStub probe | At least one task runs 12+ decision rounds over seeds 0/1/2 with best-score AUC and invalid-action recovery metrics |
| P2-AGENT-06 |  | Open | LLMReplay benchmark fixture | A fixed reasoning/action trace replays deterministically and is usable as a public baseline artifact |

## P3：专业物理化学深化

目标：把仍然是 proxy/lite 的物化模块逐步替换成窄范围、可审计、可验证的专业模型切片。

说明：

- P3 不阻塞第一版公开预发布。
- `liyijun` 已认领的三项不得重复实现，除非重新分配。
- 每个 P3 项都必须带 maturity 声明、适用范围、验证算例和失败边界。

| ID | Owner | Status | Task | Exit Criteria |
| --- | --- | --- | --- | --- |
| DEEP-D1A | liyijun | Claimed | Component identity registry | Aliases, CAS/InChI-like placeholders, formula, charge, molecular weight, provenance, duplicate checks, JSON round-trip |
| DEEP-D1B | liyijun | Claimed | Unit-dimension checker | Canonical dimensions for amount, mass, volume, temperature, pressure, energy, transport properties, and instrument response |
| DEEP-D1C | liyijun | Claimed | Data conflict policy | Deterministic source priority, uncertainty fields, warning vs hard-fail reports, dataset-card provenance |
| DEEP-D4B |  | Open | LLE phase-split solver | TPD-style heuristic, initialization policy, mass-balance checks, extraction-task integration |
| DEEP-D4C |  | Open | Aqueous acid-base equilibrium | Charge balance, activity simplifications, pH observation kernel, precipitation hooks |
| DEEP-D4D |  | Open | Gibbs-minimization toy solver hardening | Small stoichiometric examples with convexity and constraint diagnostics |
| DEEP-D5A |  | Open | Thermochemistry-coupled reversibility | Equilibrium constants from standard-state Gibbs energy, detailed balance, reactor ODE integration |
| DEEP-D5B |  | Open | Pressure-dependent and falloff kinetics | Troe/Lindemann-style compact slice, third-body efficiencies, validation cases |
| DEEP-D6B |  | Open | CSTR dynamics | Dynamic mass/energy balance, residence time, stability, startup/shutdown, multiple steady states |
| DEEP-D6C |  | Open | PFR/plug-flow slice | Axial integration, pressure-drop coupling, heat-transfer boundary, validation cases |
| DEEP-D6D |  | Open | Solver backend interface | Deterministic tolerances, event handling, failure diagnostics, replay verification |
| DEEP-D7A |  | Open | Rigorous flash unit | Material and energy balance, vapor-liquid split, enthalpy duty, nonideal hooks |
| DEEP-D7C |  | Open | Extraction unit | Distribution coefficients from activity/partition model, entrainment, wash sequence, recovery/purity metrics |
| DEEP-D7D |  | Open | Crystallization unit | Solubility curve, supersaturation, nucleation/growth compact model, impurity occlusion, CSD metadata |
| DEEP-D8A |  | Open | Phase-change and equipment heat transfer | Boiling/condensation warnings, jacket/coil/shell corrections, fouling evolution, energy-ledger validation |
| DEEP-D8B |  | Open | Two-phase pressure drop | Documented correlation slice with validity limits replacing homogeneous proxy |
| DEEP-D8C |  | Open | Relief and safety envelope | Pressure/temperature hazard envelopes, runaway indicators, safety-cost integration |
| DEEP-D8D |  | Open | Equipment cards | Vessel, pump, mixer, condenser, heat exchanger, and column specs with constraints |
| DEEP-D9A |  | Open | Empirical HPLC/GC method sensitivity | Retention-index examples, temperature/mobile-phase sensitivity, detector response calibration, asymmetric peak flags |
| DEEP-D9C |  | Open | NMR slice | Chemical shift anchors, multiplicity/coupling metadata, integration, solvent reference, failure modes |
| DEEP-D9D |  | Open | MS slice | Simple fragmentation metadata, isotope envelopes for small formulas, detector response uncertainty |
| DEEP-D10C |  | Open | Reference-baseline reports | Task-specific official tables, seed confidence intervals, public/private generalization gaps |
| DEEP-D10D |  | Open | Solver/provenance manifest | Commit hash, dependency lock, optional backend versions, tolerances, hidden-scenario salt policy |
| DEEP-D11B |  | Open | Mass-transfer limiting-current slice | Diffusion-layer approximation, limiting current, depletion, current-efficiency loss, analytical plateau checks |
| DEEP-D11C |  | Open | Potentiostatic and galvanostatic controllers | Controller semantics, clipping, ramp/hold recipes, operation logs, replay contracts |
| DEEP-D11D |  | Open | Double-layer and capacitive-current slice | RC transient, non-Faradaic current, startup artifacts, current-trace observations |
| DEEP-D11E |  | Open | Electrochemical scenario cards | Redox metadata, electrode area, electrolyte window, side-reaction thresholds, hidden-parameter generation |

## P4：文档、Notebook、站点与发布包装

目标：让外部用户能快速理解当前稳定能力，并能完成端到端复现实验。

| ID | Owner | Status | Task | Exit Criteria |
| --- | --- | --- | --- | --- |
| P4-DOCS-01 |  | Open | Reorganize docs around pre-release benchmark | Site first explains what is stable, what is experimental, and where to start |
| P4-DOCS-02 |  | Open | Build a concise architecture report from current code | High-level document describes Runtime v2, task contracts, ledgers, mechanisms, agent interface, and limitations |
| P4-DOCS-03 |  | Open | Harden 12-day tutorial workload | Each day requires a nontrivial artifact: experiment log, plot, model, decision rationale, or report |
| P4-DOCS-04 |  | Open | Add three end-to-end notebooks | Reaction-to-assay, reaction-to-purification, and partition-discovery each show planning, execution, spectra, metrics, and reflection |
| P4-DOCS-05 |  | Open | Finalize release checklist page | Includes gates, artifacts, known limitations, private-eval policy, and citation instructions |

## 5. 已合并并废弃的旧任务板

以下任务板已合并到本文件，不再单独维护：

- `TODO_PROFESSIONAL.md`
- `TODO_PROFESSIONAL_DEEPENING.md`

如果任何文档页面与本文件冲突，以本文件为准。
