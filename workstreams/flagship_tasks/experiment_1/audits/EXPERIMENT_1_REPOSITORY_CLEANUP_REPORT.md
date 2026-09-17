# Experiment 1 Authority / Navigation Cleanup Report

日期：2026-09-17。范围：**小范围 authority audit 与 navigation cleanup。**

本报告不产生科学样本，不运行 Participant，不修改 simulator physics、World、prior、Gate、预算或 qualification 结果。

## A. Before

清理前，Experiment 1 的有效信息分布在：

- `WORK_II_TODOLIST.md` 和 `WORK_II_EXPERIMENT_MATRIX.md`；
- 顶层的 v1.0.1 minimum execution spec 与 EC qualification note；
- `configs/benchmark/` 的机器合同；
- `scripts/`、`src/chemworld/eval/` 和历史 `work_ii_*` 依赖；
- tracked 人类可读报告与服务器 ignored `runs/` evidence；
- `experiment_1/guidance/` 的五份非 normative 设计文档。

主要风险不是文件缺失，而是未来开发者可能把旧 Work II 设计、guidance、机器合同和结果报告视为同一层权威；同时，按文件名清理 `work_ii_*` 会破坏当前 EC 运行链。

## B. After

```text
workstreams/flagship_tasks/experiment_1/
├── README.md
├── AUTHORITY.md
├── LEGACY_INDEX.md
├── audits/
│   └── EXPERIMENT_1_REPOSITORY_CLEANUP_REPORT.md
└── guidance/
    ├── README.md
    └── five versioned design documents
```

本轮只增加导航、权威图和依赖分类；所有冻结规范、配置、代码、历史文档和 evidence 保持原路径。

## C. Authority

- 唯一导航入口：`workstreams/flagship_tasks/experiment_1/README.md`；
- 当前 qualification 科学执行语义：`EXPERIMENT_1_MINIMUM_EXECUTION_SPEC_V1_0_1.md`；
- 当前 EC 精确机器合同：`configs/benchmark/experiment_1_ec_qualification_v1.0.1.json`；
- 当前 EC 实验 note：`EXPERIMENT_1_EC_QUALIFICATION_V1_0_1_NOTE.md`；
- 当前 EC machine result：服务器 final registry；
- 当前 EC readable result：`reports/experiment-1-ec-qualification-v1.0.1-20260917.md`；
- 五份七体系设计文件：guidance，不是 normative specification。

七体系完整 benchmark 仍未冻结；本轮没有创建 `DESIGN_SPEC_V1.md`。

## D. Migration Table

| old path / class | action | reason |
| --- | --- | --- |
| v1.0.1 minimum spec | retained in place | 机器合同绑定路径与 SHA-256 |
| EC qualification note | retained in place | 机器合同绑定路径与 SHA-256 |
| EC machine contract | retained in place | 冻结执行输入与 evidence binding |
| EC report | retained in place | 已完成结果的可读记录 |
| five design documents | retained under `guidance/` | 保留版本和 provenance，明确非 normative |
| current `work_ii_*` code/assets | retained and indexed | EC runner/contract 仍直接依赖 |
| other historical Work II assets | retained in place | 未完成 replay/link/dependency 审计 |
| new Experiment 1 namespace | navigation files added | 建立单一入口，不复制第二份权威 |

## E. Legacy Dependency Audit

### Current direct dependency

机器合同直接绑定：

- `configs/benchmark/work_ii_campaign_pilot.json`；
- `reports/work-ii-electrochemical-matched-prior-qualification-20260811.json`；
- `reports/work-ii-mechanism-oracle-electrochemical-classified-v0.2-20260811.json`。

当前 runner 直接 import：

- `work_ii_ae_prior_qualification_v02`；
- `work_ii_electrochemical_matched_prior_qualification`；
- `work_ii_structural_candidate_qualification`；
- 三个对应历史 runner/helper script。

### Historical only

未被上述合同或当前 runner 直接引用的旧 notes/configs/reports，本轮只保留为 historical reproduction/provenance；没有逐文件改变其状态。

### Dead/unreferenced candidate

无。本轮证据不足以安全宣布任何文件可删除。

## F. Audit Findings

- 本地基线分支：`codex/experiment1-v1.0.1-ec-qualification`；
- 清理前本地提交：`6ef09ca4d237bfef9b456f7cedaf1072da850a44`；
- 清理前相对 `origin/main`：0 behind / 8 ahead；
- 机器合同绑定的 specification、note、campaign config 和两份 source reports 均存在，实际 SHA-256 与合同一致；
- 服务器 evidence 根目录存在，共 248 个文件；
- final registry 文件 SHA-256：`f320b54836bd018e7940df98c5e906a755baf940ce5080a7cc7c2f4700df1ff1`；
- final registry self-hash：`ad3b0a7c7f2561375bdd99372f277d0d678014c32d2bdc86fc88b3ea84675b26`；
- final summary 文件 SHA-256：`ccc29884d24e3a3622d05c7f108d5c9b4de7123f35924ba436fb5f0b66b90c06`；
- 结果为 15/15 单元完成、11/15 qualified、4/15 failed；0 provider calls；
- 当前 EC 仍未获 Participant development 或 formal benchmark authorization。

## G. Verification

验证已在 Materials 服务器的项目锁定 `.venv` 中完成（主机和服务器均没有可调用的 `uv` CLI，因此没有使用系统 Python）：

- 新导航文档 Markdown 相对链接：7 条已检查，0 条缺失；
- EC contract load：通过，全部绑定路径和 hash 有效；
- execution authorization：`participant_execution_authorized = false`；
- `tests/test_experiment_1_ec_qualification.py`：7 passed；
- `git diff --check`：通过；
- final registry/summary 文件 hash 与清理前一致；
- 没有执行 qualification runner，没有调用 provider，没有产生或覆盖科学 evidence。

## H. Remaining Debt / Stop Point

1. 人工审阅本报告和 authority map；
2. 审阅通过后，为 `EC-W01/W04 × entity/structural` 编写独立 repair note；
3. 冻结新 repair manifest 后，仅重跑受影响 block；
4. EC 全部通过前，不启动 Participant；
5. EC 全部通过后，再决定是否进行全面 legacy migration；
6. RX、PA、FL、P、C、D 的 system-specific normative specs、private truth 和机器合同仍需未来独立冻结。

本任务在人工审阅门停止，不自动进入 repair。
