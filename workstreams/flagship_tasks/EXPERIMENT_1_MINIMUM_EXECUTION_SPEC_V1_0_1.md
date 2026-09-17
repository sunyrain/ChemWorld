# ChemWorld Experiment 1 最小执行规范 v1.0.1

状态：**冻结用于 development qualification；尚不是 benchmark release。**
冻结日期：2026-09-17。执行入口由
[`WORK_II_TODOLIST.md`](WORK_II_TODOLIST.md) 管理，机器合同为
[`experiment_1_ec_qualification_v1.0.1.json`](../../configs/benchmark/experiment_1_ec_qualification_v1.0.1.json)。

## 1. 本版本冻结什么

本规范冻结 Experiment 1 的最小可执行语义：

- 七体系：`EC / RX / PA / FL / P / C / D`；
- 每体系五个候选 private Worlds，目标共 35 Worlds；
- 三个先验 locus：`entity / parametric / structural`；
- 三个机器 Arm ID：`opaque / aligned / misspecified`；
- qualification 的判定层级、共同硬门、状态词和失败语义；
- 首个垂直切片 `EC-W00` 与 `EC-W01..EC-W05` 的候选 seed、预算和阈值；
- qualification、Participant 和 evaluator 的可见性边界；
- manifest、truth/prior/evidence hash 与 exact replay 要求。

本版本不冻结 Participant 模型、正式样本量、七体系全部 private truth 数值，也不宣称任一格已经通过。
`v1.0.1` 是执行规范版本；正式可发布 benchmark 必须另有 release manifest，并且只能包含已经资格化的单元。

## 2. 对象、计数与状态

World 是 simulator 编译出的完整隐藏物理实例，seed 只是生成钥匙。O/A/M 不得改变 World、公共操作、仪器、
资源、噪声政策或任务目标。

- `EC-W00`：开发 canary，只验证合同、运行、记录和 replay；永不进入科学分母。
- `EC-W01..EC-W05`：EC 的五个候选正式 Worlds。
- 一个资格化原子单元是 `system × world × prior_locus`。
- EC 首轮共有 `5 × 3 = 15` 个原子单元；全目标空间共有 `35 × 3 = 105` 个原子单元，允许科学上合理的
  `N/A`。
- 一个 `system × locus` 只有在预注册五个 Worlds 全部通过后才是 `five_world_qualified`。
- 全 benchmark 只有在所有非 `N/A` 单元通过、执行面冻结且 release audit 通过后才可称 ready。

实现成熟度和科学结果不得混写：

| 字段 | 允许值 | 含义 |
| --- | --- | --- |
| `implementation_readiness` | `A / B / C` | 已有资产 / 可直接开发 / 需新增 private physics |
| `qualification_status` | `pending / qualified / failed / N/A` | 本协议的实际资格化结果 |

`A` 不等于 `qualified`，历史 PASS 也不能自动升级为本协议 PASS。

## 3. Arm 与可见性

| Arm ID | Participant 可见内容 |
| --- | --- |
| `opaque` | 公共科学背景和实验合同；没有目标 locus 的实例级 claim |
| `aligned` | 与 private World 一致但有限、非 oracle 的目标 claim |
| `misspecified` | schema、字段、精度、语气、置信度和长度匹配，但目标 claim 错误 |

Participant 不得看到 Arm 名称、world seed、private truth、hidden mechanism、qualification 结果或 evidence bundle。
Qualification runner 可以读取 private truth，但不得调用 Participant provider，也不得使用 Participant 结果选择 World、
阈值或错误先验。Evaluator 在 Participant 冻结提交之后才可读取 private truth。

## 4. 每个原子单元的八个共同硬门

| Gate | 必须满足的条件 |
| --- | --- |
| Q1 world integrity | 质量/电荷/状态与资源 ledger 自洽；全部执行完成分类；exact replay 通过 |
| Q2 task accessibility | 公共合法操作域与预算中存在可执行、能产生任务相关信息的路径 |
| Q3 public-contract invariance | O/A/M 的操作、仪器、资源、噪声和目标一致；不泄漏 Arm/private 身份 |
| Q4 prior symmetry | A/M schema、上下文、置信度和近似长度一致，只改变注册科学 claim |
| Q5 identifiability | A/M hypotheses 在公开实验空间产生超过冻结阈值的可测差异 |
| Q6 budgeted falsifiability | Participant 预算内至少存在一个合法反证设计，不要求穷举 qualification 网格 |
| Q7 behavioral relevance | 错误 claim 会在至少一个预注册合理策略或决策区改变实验、预测或行动 |
| Q8 noise robustness | 结论在冻结的独立噪声重复下成立，不依赖单一幸运 seed |

任一必需 Gate 失败，则原子单元为 `failed`，不得用平均分抵消。平台缺陷允许修复，但受影响块必须从第一个单位重跑；
科学失败保留且不降低阈值。正式 Participant 开始后禁止按其表现替换 World 或 prior。

## 5. EC 垂直切片

五个候选 Worlds 共享 `electrochemical-conversion`、`public-test` split、
`nominal-prior-latent-v2` material family 和 `electrochemical-s0-balanced-efficiency-v2` scoring contract。
候选 runtime seeds 固定为 `0..4`，映射为 `EC-W01..EC-W05`。角色是覆盖目标，不是预写结论：

| World | seed | authoring role |
| --- | ---: | --- |
| EC-W01 | 0 | central reference |
| EC-W02 | 1 | quantitative shift |
| EC-W03 | 2 | alternate response regime candidate |
| EC-W04 | 3 | strong coupling candidate |
| EC-W05 | 4 | boundary robustness candidate |

qualification 必须报告 realized private-truth digest 与响应覆盖；如果 role 未被实际物理支持，Q1/Q5/Q8 之一失败，
不能只改标签。`EC-W00` 使用独立 seed `900000`，仅作 canary。

### 5.1 EC-E：电解液 dossier 映射

- target：`electrolyte_profile` 的四行匿名 nominal dossier；solvent 信息状态保持一致；
- frozen transposition：`E0 ↔ E2`，整行交换，不逐字段篡改；
- qualification design：两个 outcome-blind complementary anchors，四种 electrolyte 全扫，每点三次独立 keyed-noise 重复；
- 主要 endpoint：`transport_efficiency`；支持 endpoint：`ohmic_efficiency`；
- 被交换两种材料在两个 anchors 均须满足绝对 separation `>= 0.05` 且 SNR `>= 2.0`；
- 正确 nominal mapping 不得被 realized residual 系统性反转；
- Participant 可反证预算：至多四个独特完整 recipes（两材料 × 两 anchors）。

### 5.2 EC-P：电位—电流局部关系

- provider-free `11 × 11` surface；36 个 fit 点，其余 held-out；
- aligned normalized MAE `<= 0.20`；
- A/M held-out disagreement fraction `>= 0.25`；
- misspecified 相对 aligned 的 blind normalized-error margin `>= 0.05`；
- 低侧与高侧各至少三个 counterexamples；代表点网格距离 `>= 4`；
- A/M 在中央 `3 × 3` 邻域匹配，基线 utility gap `<= 0.05`；
- Participant 可反证预算：四点，覆盖 potential/current 的两侧。

### 5.3 EC-S：高电流 transport limitation

- qualification grid：potential 低/中/高 × current 低/中/高；关键点三次独立噪声重复；
- 关键 effect `>= max(0.03, 6 × observed_sigma)`；
- held-out disagreement fraction `>= 0.40`；
- 低/高 current 区都存在 counterexample；
- aligned blind error 小于 misspecified blind error；
- 至少一个与 transport limitation 一致的 efficiency-loss 或 diminishing-gain signature；
- Participant 可反证预算：同一 potential 下的中/高 current 对比可在四个独特实验内完成。

## 6. 运行顺序、产物与停止规则

```text
freeze spec + config
        ↓
EC-W00 canary
        ↓ 仅在工程链通过时
EC-W01..W05 × entity/parametric/structural provider-free qualification
        ↓
15-row registry + five-world locus decisions + evidence hashes
        ↓ 仅在 EC 三格均通过且执行面冻结时
Participant development run（另写 note；不由本规范自动授权）
```

每次 qualification 必须输出：冻结输入 manifest、原子单元 registry、准确分母、所有失败、资源计数、
truth/prior/report hashes、可读 Markdown 摘要和 exact replay 绑定。不得覆盖既有 attempt。

W00 失败时停止 W1–W5；任一平台失败时停止并修复后整块重跑；科学 Gate 失败时完成预注册分母并报告 `failed`，
不得启动对应 Participant 单元。EC 通过只证明 21 个 `system × locus` 中的三格，不代表全 benchmark 通过。
