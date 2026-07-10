# ChemWorld Unified TODO

最后更新：2026-07-10

本文档是 ChemWorld 唯一活跃任务板。所有开发、发布、专业物理模型深化、notebook、站点和本地评测机任务都收束到这里。`docs/todo.md` 只保留公开摘要，不作为第二份任务板维护。

## 协作规则

- 默认在 `main` 开发。
- 开始非平凡任务前先执行 `git pull --ff-only origin main`。
- 已由 `liyijun` 标记为 `Claimed` 的任务不重复实现，除非重新分配。
- 开始任务时写清楚 owner；完成一个任务后立即更新本文档、运行对应门禁、提交并推送。
- 远端 TODO 改变后，本地开发者必须先拉取并合并最新任务板。
- `Done` 必须有代码、测试、文档，或明确 no-test rationale。
- 不把 `proxy`、`lite`、`reference_validated` 或 `professional-candidate` 混写成 `professional`。

## 当前结论

ChemWorld 已完成公开预发布、AAAI 实验准备和 P3 专业物理化学深化任务。AAAI 6 任务 preset、`equilibrium-characterization`、reference-baseline reports、solver/provenance manifest、artifact smoke 与三项数据基础设施均已完成。

## 当前统计

| 阶段 | 目标 | 总数 | Done | Claimed | Open | Blocked | 剩余 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| P0 | 预发布 benchmark hardening | 12 | 12 | 0 | 0 | 0 | 0 |
| P1 | runtime 与环境自洽性 | 8 | 8 | 0 | 0 | 0 | 0 |
| P2 | agent-facing 交互与数据集 | 6 | 6 | 0 | 0 | 0 | 0 |
| P3 | 专业物理化学深化 | 27 | 27 | 0 | 0 | 0 | 0 |
| P4 | 文档、notebook、站点与发布包装 | 5 | 5 | 0 | 0 | 0 | 0 |
| **合计** |  | **58** | **58** | **0** | **0** | **0** | **0** |

当前任务板 **58 项已全部完成**。后续新增工作必须作为新任务登记，不回写或模糊既有完成标准。

## Cutline

| Cutline | 还差 | 判定标准 |
| --- | ---: | --- |
| 最小可信 benchmark | 0 | P0/P1 全部完成。任务、runtime、ledger、observation、scoring、replay 和公开边界通过审计。 |
| 可公开预发布包 | 0 | P2/P4 完成。外部用户能安装、运行、提交、阅读文档、复现实验并理解限制。 |
| AAAI 投稿实验包 | 0 | 6 任务 preset、`equilibrium-characterization`、baseline report、solver/provenance manifest 和 artifact smoke 已完成。 |
| 全部可见路线图 | 0 | P3 专业物理化学深化的既定 27 项已全部完成。 |

## P0 - 预发布 Benchmark Hardening

| ID | Owner | Status | Task |
| --- | --- | --- | --- |
| P0-BENCH-01 | Codex | Done | Freeze the three-task pre-release contract |
| P0-BENCH-02 | Codex | Done | Build official seed suite |
| P0-BENCH-03 | Codex | Done | Generate official baseline table |
| P0-BENCH-04 | Codex | Done | Calibrate BO budgets and initial samples |
| P0-BENCH-05 | Codex | Done | Lock golden trajectories |
| P0-BENCH-06 | Codex | Done | Audit scoring contracts |
| P0-BENCH-07 | Codex | Done | Harden replay verifier |
| P0-BENCH-08 | Codex | Done | Build one valid submission bundle example |
| P0-BENCH-09 | Codex | Done | Build local teacher/student evaluation smoke |
| P0-BENCH-10 | Codex | Done | Produce benchmark paper artifact skeleton |
| P0-BENCH-11 | Codex | Done | Add CI-like local release command |
| P0-BENCH-12 | Codex | Done | Write pre-release limitations statement |

## P1 - Runtime 与环境自洽性

| ID | Owner | Status | Task |
| --- | --- | --- | --- |
| P1-CONSIST-01 | Codex | Done | Run and document environment self-consistency audit |
| P1-CONSIST-02 | Codex | Done | Spectra-metric semantic alignment |
| P1-CONSIST-03 | Codex | Done | Action affordance consistency |
| P1-CONSIST-04 | Codex | Done | Invalid action atomicity |
| P1-CONSIST-05 | Codex | Done | Campaign vs single-experiment semantics audit |
| P1-CONSIST-06 | Codex | Done | Ledger single-source-of-truth audit |
| P1-CONSIST-07 | Codex | Done | Public observation leakage audit |
| P1-CONSIST-08 | Codex | Done | Runtime boundary scan |

## P2 - Agent-Facing 交互与数据集

| ID | Owner | Status | Task |
| --- | --- | --- | --- |
| P2-AGENT-01 | Codex | Done | Polish `task_prompt()` for the three pre-release tasks |
| P2-AGENT-02 | Codex | Done | Improve lab-report summaries |
| P2-AGENT-03 | Codex | Done | Stabilize RL observation view |
| P2-AGENT-04 | Codex | Done | Add agent trace to dataset export examples |
| P2-AGENT-05 | Codex | Done | Multi-round ToolUsingLLMStub probe |
| P2-AGENT-06 | Codex | Done | LLMReplay benchmark fixture |

## P3 - 专业物理化学深化

规则：

- P3 不阻塞第一版公开预发布。
- 原由 `liyijun` 认领的 D1A/D1B/D1C 已在其退出协作后由用户重新分配给 Codex。
- 每个 P3 任务必须包含 maturity label、适用范围、验证算例和失败边界。

| ID | Owner | Status | Task | Exit Criteria |
| --- | --- | --- | --- | --- |
| DEEP-D1A | Codex | Done | Component identity registry | Added versioned immutable registry, aliases, checksum-validated CAS, InChI/InChIKey, formula/charge/formula-checked molecular weight, provenance, collision checks, canonical SHA-256, curated identities, exact JSON round-trip, tests, and a professional-candidate model card. |
| DEEP-D1B | Codex | Done | Unit-dimension checker | Added canonical exponent vectors and semantic dimensions for amount/mass/volume/temperature/pressure/energy, thermodynamic and transport properties, electrochemistry and instrument responses; added field contracts, strict mismatch reports, complete unit-catalog closure tests, and a professional-candidate model card. |
| DEEP-D1C | Codex | Done | Data conflict policy | Added deterministic source-ranked multi-field audits, scalar tolerances, required uncertainty policy, warning versus hard-fail findings, source provenance, canonical report/card digests, dataset-card provenance schema 0.3, round-trip/tamper tests, and a professional-candidate model card. |
| DEEP-D4B | Codex | Done | LLE phase-split solver | Added TPD-style diagnostic, runtime partition split, initialization policy, phase-stability metadata, and mass-balance tests. |
| DEEP-D4C | Codex | Done | Aqueous acid-base equilibrium | Added public pH-meter observation, charge-balance-compatible acid/base result, precipitation hooks, model-card evidence, and tests. |
| DEEP-D4D | Codex | Done | Gibbs-minimization toy solver hardening | Added diagnostics, KKT-style residual, rank/DOF checks, reference cases, model-card evidence, and documentation. |
| DEEP-D5A | Codex | Done | Thermochemistry-coupled reversibility | NASA7 species Gibbs energy now drives K_eq, concentration standard-state conversion, reverse Arrhenius detailed balance, reversible batch ODE equilibrium tests, and model-card evidence. |
| DEEP-D5B | Codex | Done | Pressure-dependent and falloff kinetics | Added third-body collision efficiencies, Lindemann low/high-pressure limits, Troe broadening, bath-gas-sensitive ODE validation, mechanism schema support, and model-card evidence. |
| DEEP-D6B | Codex | Done | CSTR dynamics | Added dynamic material/energy balances, residence-time metadata, linear/step startup and shutdown flow programs, analytical transient tests, multiple steady states, stability classification, and model-card evidence. |
| DEEP-D6C | Codex | Done | PFR/plug-flow slice | Added axial position mapping, geometry contract, Darcy pressure-drop profile, distributed heat-transfer boundary, analytical validation cases, solver diagnostics, and model-card evidence. |
| DEEP-D6D | Codex | Done | Solver backend interface | Added versioned policies, deterministic tolerances, named event contracts, failure diagnostics, policy hashes, provenance integration, cross-reactor adoption, and dedicated tests. |
| DEEP-D7A | Codex | Done | Rigorous flash unit | Added iterative fixed-TP gamma-phi flash, per-component material split, enthalpy-duty ledger, nonideal fugacity/Poynting hooks, convergence diagnostics, professional-candidate model card, and analytical/reference-backed tests. |
| DEEP-D7C | Codex | Done | Extraction unit | Added activity-corrected distribution coefficients, fresh-solvent extraction stages, explicit entrainment, aqueous wash sequences, stage convergence reports, recovery/purity/rejection metrics, analytical tests, and a professional-candidate model card. |
| DEEP-D7D | Codex | Done | Crystallization unit | Added provenance-tagged van't Hoff solubility curves, cooling-ramp supersaturation, capped primary-nucleation/growth cohort integration, explicit seed mass, impurity occlusion, D10/D50/D90/CV/fines metadata, analytical tests, and a professional-candidate model card. |
| DEEP-D8A | Codex | Done | Phase-change and equipment heat transfer | Added explicit jacket/coil/shell corrections, asymptotic fouling resistance, lumped sensible heating/cooling, boiling/condensation plateaus, phase-crossing warnings, signed phase inventory, exact sensible/latent energy ledgers, tests, and a professional-candidate model card. |
| DEEP-D8B | Codex | Done | Two-phase pressure drop | Added a horizontal smooth-pipe Lockhart-Martinelli/Chisholm separated-flow model with phase Reynolds/friction anchors, regime-specific multipliers, explicit validity failures/warnings, exact `fluids` reference comparison, tests, and a reference-validated model card; retained the homogeneous rollout model as an explicit proxy. |
| DEEP-D8C | Codex | Done | Relief and safety envelope | Added ordered pressure/temperature/relief/MAWP envelopes, Arrhenius/Semenov runaway indicators, MTSR and time-to-limit projections, relief capacity ratios, emergency flags, auditable risk/cost composition, Gym constraint adapters, tests, and a professional-candidate model card. |
| DEEP-D8D | Codex | Done | Equipment cards | Added versioned JSON equipment cards for vessel/pump/mixer/condenser/heat-exchanger/column types, provenance-tagged rated parameters, shared unit-bearing min/max constraints, margin/utilization reports, warning vs hard feasibility, round-trip tests, and a professional-candidate model card. |
| DEEP-D9A | Codex | Done | Empirical HPLC/GC method sensitivity | Added HPLC mobile-phase/temperature log-k sensitivity, GC van't Hoff retention, logarithmic n-alkane retention-index interpolation, detector slope/intercept/R²/LOD/LOQ calibration, fronting/tailing severity flags, tests, and a professional-candidate model card. |
| DEEP-D9C | Codex | Done | NMR slice | Added provenance-tagged 1H shift anchors, first-order s/d/t/q/quint/dd/m splitting, J-coupling stick lines, amount/proton/response integration, solvent/reference correction, overlap/second-order/exchange warnings, tests, and a professional-candidate model card. |
| DEEP-D9D | Codex | Done | MS slice | Added natural-abundance isotope convolution for common small-formula elements, nominal/exact-mass/m-z envelopes, curated fragment/neutral-loss metadata, detector mean/RSD uncertainty, Cl/Br/C analytical patterns, failure warnings, tests, and a professional-candidate model card. |
| DEEP-D10C | Codex | Done | Reference-baseline reports | Added AAAI preset baseline reporting, task-level summary rows, equilibrium metrics, Codex replay baseline, and smoke tests. |
| DEEP-D10D | Codex | Done | Solver/provenance manifest | Added solver/provenance manifest with commit hash, dependency versions, solver tolerances, maturity labels, salt policy, and artifact integration. |
| DEEP-D11B | Codex | Done | Mass-transfer limiting-current slice | Added planar diffusion-layer i_lim, surface depletion, finite-reservoir piecewise linear/exponential bulk depletion, kinetic/transport caps, signed useful current, useful/side charge and efficiency ledgers, analytical plateau tests, and a professional-candidate model card. |
| DEEP-D11C | Codex | Done | Potentiostatic and galvanostatic controllers | Added versioned potentiostatic/galvanostatic ramp/hold recipes, range/slew clipping, mode-state semantics, sampled traces, operation logs, canonical recipe/execution SHA-256, exact replay verification, tests, and a professional-candidate model card. |
| DEEP-D11D | Codex | Done | Double-layer and capacitive-current slice | Added Randles Rs-(Rct||Cdl) potential/current step analytics, capacitive/Faradaic/total current traces, interfacial/terminal potential, exact charge ledgers, 5τ/startup-artifact warnings, observation arrays, tests, and a professional-candidate model card. |
| DEEP-D11E | Codex | Done | Electrochemical scenario cards | Added versioned public redox/geometry/window/onset cards, private range policies, salted split-aware deterministic hidden generation, hidden digests, side-reaction severity, direct reaction/ohmic/diffusion/double-layer model bundles, tests, and a professional-candidate model card. |

## P4 - 文档、Notebook、站点与发布包装

| ID | Owner | Status | Task |
| --- | --- | --- | --- |
| P4-DOCS-01 | Codex | Done | Reorganize docs around pre-release benchmark |
| P4-DOCS-02 | Codex | Done | Build a concise architecture report from current code |
| P4-DOCS-03 | Codex | Done | Harden 12-day tutorial workload |
| P4-DOCS-04 | Codex | Done | Add three end-to-end notebooks |
| P4-DOCS-05 | Codex | Done | Finalize release checklist page |

## 任务门禁

| 任务类型 | 必跑检查 |
| --- | --- |
| Python/runtime | `python -m ruff check .`; `python -m mypy src/chemworld`; `python -m pytest` |
| Env/benchmark/replay | 上述检查 + `python scripts/audit_environment_consistency.py --tasks all --seeds 0 1 2` |
| Docs/site | `python -m mkdocs build --strict` |
| Release-level | `python scripts/run_release_gate.py` |

## 已合并并废弃的旧任务板

- `TODO_PROFESSIONAL.md`
- `TODO_PROFESSIONAL_DEEPENING.md`

如果任何文档页面与本文档冲突，以本文档为准。
