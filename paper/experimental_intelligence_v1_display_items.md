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

**Figure 1 | Object hierarchy and public instrument contract.**
**A,** Reusable physical and transactional components compile into a world.
**B,** A task contract attaches the initial state, actions, instruments, observations,
resources, termination and evaluation surface while private laws remain hidden.
**C,** Scenarios instantiate a task, trajectories record interaction, and a controlled
fork is a separate single-private-component intervention. **D,** Reference tasks, typed
operations, instruments and task-metric bindings retain distinct denominators.

**Figure 2 | Coverage-guided construction beyond the reference task identities.**
**A,** Eight component patterns define the frozen construction blocks; the highlighted
reaction-distillation pattern is absent from the reference identities. **B,** Pairwise
discrete coverage, seeded space filling and ordered workflow interactions determine the
rows. **C,** Fifteen reference tasks and 52 generated compositions count different
objects. **D,** All eight unseen rows and all 52 generated rows completed; unseen does
not mean unbounded or arbitrary.

**Figure 3 | Full-census qualification of the software experimental substrate.**
**A,** All reference and generated execution units passed. **B,** Module, interface,
compile-mutant and invalid-action censuses retain their exact denominators. **C,** invalid
declarations fail before construction, while invalid actions preserve physical state.
**D,** Failure classes, missing receipts and public/private leakage findings were zero.

**Figure 4 | Deterministic cases exercise lifecycle and failure semantics.**
**A,** Eight cases cover multistage, resource-limited and reference-library workflows.
**B,** The single planned precondition failure remains in the 89-action census and
is followed by 18 commits. **C,** Rollback preserves non-accounting state while charging
the declared attempt consequences. **D,** All eight lifecycles, final assays, resource
ledgers and exact replays passed.

**Figure 5 | Controlled forks change one private component under an invariant public contract.**
**A,** Parent and child share nine public fields and the same action sequence.
**B,** Three constitutive-law and three material-law pairs change one private target each.
**C,** All six pairs pass every registered gate. **D,** Physical-state and public-
observation divergence occurs in the protocol-specified channels. The traces contain no
provider calls and support no agent-adaptation claim.

**Figure 6 | Instrument records distinguish endpoint, process and execution status.**
**A,** The 12-action deterministic reference and 15-action complete-agent trajectory are
independent execution units on the same frozen unseen world. **B,** All 15 agent actions
committed, with one termination, one final assay and exact replay. **C,** Environment
resources and provider context use separate ledgers. **D,** An archived matched pair has
a near-zero terminal contrast but marked discovery, retention, drawdown and terminal-
retention differences; the example is descriptive and supports no model ranking.
