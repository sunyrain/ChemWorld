# ChemWorld first-paper numeric display items

Status: complete for the current first-paper evidence programme.

Every number below is rendered from the current-bound reader-facing figure data.
Counts retain their exact qualification denominators and are not statistical samples.

## Main tables

### Table 1 | Public construction surface and evidence scope

| Quantity | Count | Interpretation |
| --- | --- | --- |
| reusable component types | 9 | declared component vocabulary |
| frozen component patterns | 8 | coverage design |
| registered reference tasks | 15 | reference landmarks |
| typed operation kinds | 28 | public action surface |
| synthetic instrument contracts | 5 | public measurement surface |
| task-metric bindings | 62 | evaluation bindings |
| coverage-generated compositions | 52 | full generated census |
| unseen reaction-distillation compositions | 8 | absent from reference identities |
| controlled fork pairs | 6 | single private target |
| provider-free fork traces | 24 | parent and child executions |

Reference tasks, operations, instruments, metrics, generated compositions and fork
traces count different objects. The 15 reference tasks do not bound the world space.

### Table 2 | Full-census qualification

| Qualification unit | Passed | Denominator | Gate role |
| --- | --- | --- | --- |
| reference units | 64 | 64 | complete execution |
| reference recipes | 1,786 | 1,786 | complete execution |
| generated | 52 | 52 | complete execution |
| unseen distillation | 8 | 8 | complete execution |
| module probes | 32 | 32 | qualified probe |
| interface paths | 7 | 7 | qualified probe |
| invalid declarations | 7 | 7 | expected rejection |
| invalid actions | 192 | 192 | expected rejection |

Zero findings: 0 registered failure classes, 0 missing receipts and 0 public/private leakage findings.

### Table 3 | Deterministic instrument-use cases

| Case | Scientific use | Submitted | Committed | Rollback | Final assay | Resources | Replay |
| --- | --- | --- | --- | --- | --- | --- | --- |
| U01 | rxn to crystal | 12 | 12 | 0 | 1 | PASS | PASS |
| U02 | resource eq. | 5 | 5 | 0 | 1 | PASS | PASS |
| U03/E01 | failure + recovery | 19 | 18 | 1 | 1 | PASS | PASS |
| U06-flow | flow | 8 | 8 | 0 | 1 | PASS | PASS |
| U06-electro | electrochem. | 11 | 11 | 0 | 1 | PASS | PASS |
| U06-distillation | distillation | 12 | 12 | 0 | 1 | PASS | PASS |
| U06-partition | partition | 10 | 10 | 0 | 1 | PASS | PASS |
| U06-crystallization | crystallization | 12 | 12 | 0 | 1 | PASS | PASS |

The planned rollback occurred at step 1; physical state, observation random-number state and ghost state were preserved, the declared penalty
reconciled, and the following 18 actions committed.

### Table 4 | Controlled single-private-component forks

| Intervention | Pairs | Seeds | Invariant public fields | All gates passed |
| --- | --- | --- | --- | --- |
| constitutive-law family | 3 | 0, 1, 2 | 9 | 3 |
| material-law counterfactual | 3 | 0, 1, 2 | 9 | 3 |

The full census contains 6 pairs and 24 provider-free traces. Every pair passed lineage,
public invariance, same-sequence executability, expected divergence, replay and
zero-provider gates.

### Table 5 | Complete-agent environment and provider ledgers

| Ledger item | Observed | Reference or limit | Meaning |
| --- | --- | --- | --- |
| submitted actions | 15 | 16 | environment action ceiling |
| committed actions | 15 | 15 | all submitted actions |
| rollbacks | 0 | 0 | required zero |
| explicit termination | 1 | 1 | required lifecycle closure |
| final assay | 1 | 1 | required exactly once |
| environment process time (s) | 8158.454 | 10440.000 | simulated process ledger |
| instrument uses | 4 | 4 | environment resource ledger |
| sample consumed (mL) | 0.850 | 1.000 | environment resource ledger |
| provider sessions | 1 | 1 | provider ledger |
| logical agent turns | 1 | 1 | provider ledger |
| instrument-interface calls | 17 | 17 | provider ledger |
| cumulative input tokens | 493,092 | 640,000 | provider ledger |
| cached input tokens | 440,832 | 493,092 | reused context |
| uncached input tokens | 52,260 | 192,000 | independent hard limit |
| output tokens | 2,973 | 64,000 | provider ledger |

Cached input is reused context, not repeated model output. Environment process time
and provider resources are independent ledgers.

#### Worked endpoint-near process record

| Process coordinate | Matched-pair contrast |
| --- | --- |
| raw terminal score | 0.003 |
| normalized best-discovery position | 0.400 |
| online incumbent retention | 0.400 |
| maximum drawdown | -0.306 |
| terminal-to-best ratio | 0.173 |

The archived world-1, replicate-3 pair is descriptive only. Its near-zero raw terminal
contrast does not erase its process-coordinate differences and supports no model ranking.

## Figure legends

**Figure 1 | ChemWorld from composable components to replayable controlled worlds.**
**A,** Reusable process and instrument modules expose shared declarations.
**B,** The compiler either produces a public contract with evaluator-owned private
mechanisms or returns structured diagnostics before construction. **C,** Typed actions pass
preflight, runtime-precondition and post-execution gates before commit; failed branches retain
declared attempt consequences without installing candidate state. **D,** Deterministic replay
requires exact reconstruction, whereas controlled forks retain the public contract and action
sequence while changing one private law.

**Figure 2 | Programmable construction and frozen coverage design.**
**A,** Topology novelty and exact task--world identity novelty are represented separately
across the eight component patterns. **B,** Pairwise discrete coverage, seeded continuous
strata and ordered workflow interactions determine the 52 generated rows. Qualification
outcomes remain in the results text and census table rather than being redrawn as pass bars.

**Figure 3 | Workflow diversity and planned rollback recovery.**
**A,** Eight cases span single-process, multistage and reference-library workflows.
**B,** The protocol-frozen rollback remains in the 89-action census and is followed by 18
commits from the last committed state. State-restoration and replay outcomes remain in the
results text rather than being repeated as PASS cards.

**Figure 4 | Controlled private-law interventions under an invariant public contract.**
**A,** Parent and child share the public world structure, contract and fixed action sequence
while one private mechanism changes. **B,** All six fork pairs diverge in their registered
physical and public-observation channels under exact replay. The complete-agent integration
case remains a bounded textual result rather than a separate schematic panel.
