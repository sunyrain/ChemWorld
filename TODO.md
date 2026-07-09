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

ChemWorld 已完成公开预发布与 AAAI 实验准备所需的 P0/P1/P2/P4。当前主线进入 P3：专业物理化学模块深化。AAAI 6 任务 preset、`equilibrium-characterization`、reference-baseline reports、solver/provenance manifest 和 artifact smoke 已完成。

## 当前统计

| 阶段 | 目标 | 总数 | Done | Claimed | Open | Blocked | 剩余 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| P0 | 预发布 benchmark hardening | 12 | 12 | 0 | 0 | 0 | 0 |
| P1 | runtime 与环境自洽性 | 8 | 8 | 0 | 0 | 0 | 0 |
| P2 | agent-facing 交互与数据集 | 6 | 6 | 0 | 0 | 0 | 0 |
| P3 | 专业物理化学深化 | 27 | 6 | 3 | 18 | 0 | 21 |
| P4 | 文档、notebook、站点与发布包装 | 5 | 5 | 0 | 0 | 0 | 0 |
| **合计** |  | **58** | **37** | **3** | **18** | **0** | **21** |

还需完成 **21 项**，全部属于 P3 长期专业化深化。其中 3 项已由 `liyijun` 认领，Codex 暂不处理。

## Cutline

| Cutline | 还差 | 判定标准 |
| --- | ---: | --- |
| 最小可信 benchmark | 0 | P0/P1 全部完成。任务、runtime、ledger、observation、scoring、replay 和公开边界通过审计。 |
| 可公开预发布包 | 0 | P2/P4 完成。外部用户能安装、运行、提交、阅读文档、复现实验并理解限制。 |
| AAAI 投稿实验包 | 0 | 6 任务 preset、`equilibrium-characterization`、baseline report、solver/provenance manifest 和 artifact smoke 已完成。 |
| 全部可见路线图 | 21 | 完成 P3 专业物理化学深化。 |

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
- `liyijun` 已认领的三项不得重复实现，除非重新分配。
- 每个 P3 任务必须包含 maturity label、适用范围、验证算例和失败边界。

| ID | Owner | Status | Task | Exit Criteria |
| --- | --- | --- | --- | --- |
| DEEP-D1A | liyijun | Claimed | Component identity registry | Aliases, CAS/InChI-like placeholders, formula, charge, molecular weight, provenance, duplicate checks, JSON round-trip. |
| DEEP-D1B | liyijun | Claimed | Unit-dimension checker | Canonical dimensions for amount, mass, volume, temperature, pressure, energy, transport properties, and instrument response. |
| DEEP-D1C | liyijun | Claimed | Data conflict policy | Deterministic source priority, uncertainty fields, warning vs hard-fail reports, dataset-card provenance. |
| DEEP-D4B | Codex | Done | LLE phase-split solver | Added TPD-style diagnostic, runtime partition split, initialization policy, phase-stability metadata, and mass-balance tests. |
| DEEP-D4C | Codex | Done | Aqueous acid-base equilibrium | Added public pH-meter observation, charge-balance-compatible acid/base result, precipitation hooks, model-card evidence, and tests. |
| DEEP-D4D | Codex | Done | Gibbs-minimization toy solver hardening | Added diagnostics, KKT-style residual, rank/DOF checks, reference cases, model-card evidence, and documentation. |
| DEEP-D5A | Codex | Done | Thermochemistry-coupled reversibility | NASA7 species Gibbs energy now drives K_eq, concentration standard-state conversion, reverse Arrhenius detailed balance, reversible batch ODE equilibrium tests, and model-card evidence. |
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
| DEEP-D10C | Codex | Done | Reference-baseline reports | Added AAAI preset baseline reporting, task-level summary rows, equilibrium metrics, Codex replay baseline, and smoke tests. |
| DEEP-D10D | Codex | Done | Solver/provenance manifest | Added solver/provenance manifest with commit hash, dependency versions, solver tolerances, maturity labels, salt policy, and artifact integration. |
| DEEP-D11B |  | Open | Mass-transfer limiting-current slice | Diffusion-layer approximation, limiting current, depletion, current-efficiency loss, analytical plateau checks. |
| DEEP-D11C |  | Open | Potentiostatic and galvanostatic controllers | Controller semantics, clipping, ramp/hold recipes, operation logs, replay contracts. |
| DEEP-D11D |  | Open | Double-layer and capacitive-current slice | RC transient, non-Faradaic current, startup artifacts, current-trace observations. |
| DEEP-D11E |  | Open | Electrochemical scenario cards | Redox metadata, electrode area, electrolyte window, side-reaction thresholds, hidden-parameter generation. |

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
