# Work I platform and controlled-programmability sections v0.1

Status: **integration-ready isolated handoff; manuscript integration pending**

Task: `W1-S04`

Owner: `Yijun`

Scope: Results and Methods prose for the apparatus, F10 semantics, and frozen
world-fork certificate. This file does not change a protocol, result, figure, or
manuscript.

## Results text

### An executable apparatus separates experimental choices from endpoint scores

ChemWorld represents an experiment as a stateful sequence of typed operations and
measurements, rather than as a direct value query. The registered surface contains 15
live task contracts spanning 28 registered typed operation kinds and five public
instrument contracts. Qualification executed 415 complete-experiment boundary recipes
and resolved 62 ordered task-by-metric bindings to executable evaluators. These are
different counting units: the 62 bindings contain 43 unique metric identifiers, and the
415 executions are boundary-recipe qualifications, not tasks, agent trials,
independent samples, or physical experiments. The campaign-only terminal decision
`discard_batch` is outside the 28-member `OPERATION_TYPES` registry and therefore does
not add a twenty-ninth registered operation kind.

The apparatus records typed state, public observations, resource receipts, transaction
outcomes, terminal decisions, and evaluator inputs while retaining audit-only world
identity and hidden simulator state. **Figure 1a–d** first establishes this interaction
loop and its identity, authority, resource, and replay controls, then shows the bounded
world-fork qualification. Figure 1 is responsible for establishing the executable
measurement surface and controlled programmability. It is not an agent-performance
comparison and does not show that agents were evaluated on all 15 registered tasks.

### Transaction outcomes keep state change distinct from failed attempts

All 28 registered operation kinds committed in at least one valid context. In a paired
invalid probe for each kind, the pre-action simulator-state projection was preserved.
Only the `committed` transaction status installs a candidate simulator-state
transition. The other qualified statuses—`validation_failed`, `rolled_back`, and
`campaign_resource_rejected`—leave that pre-action simulator state in place, while the
audit record may still retain the reserved operation attempt or an explicitly declared
process penalty appropriate to the failure stage. A failed operation is therefore not
silently converted into a successful state transition, but neither is it assumed to
have zero accounting consequence.

Campaign limits are enforced by a two-phase, event-hashed resource ledger. An operation
attempt is reserved at preflight; material-stock and vessel-start debits, non-final
instrument-use counts, and final-assay or discard counts are applied only to committed
outcomes. The qualified ledger rejected an over-limit action before execution and
round-tripped exactly from its hashed snapshot. This is an executable-world accounting
invariant, not a certificate of real material custody.

All five public instrument contracts matched their declared cost, sample consumption,
and terminal precondition in executable probes. Instrument latency is a declared
scheduling quantity, not elapsed simulator-process time or physical-device time. The
instrument outputs are bounded, state-coupled synthetic signals with explicit
calibration, detection, saturation, missingness, and maturity metadata. A
`reference_validated` model-card label records reference closures and tests within the
declared runtime slice; it does not mean that HPLC, GC, UV–visible, pH, or final-assay
outputs have been empirically calibrated against laboratory devices or real samples.
The serious-benchmark task subset rejects proxy-allowed kernels, but that policy does
not upgrade synthetic/reference-tested modules into physical validation.

### Single-component forks demonstrate controlled programmability

The frozen qualification tested two registered intervention classes across three seeds
per class. One case changed `private_physics.constitutive_laws` under the registered
`mechanism_or_constitutive_law` class; the other changed
`private_physics.material_laws` under `material_law_counterfactual`. Each of the six
parent–child pairs changed exactly one declared private component while preserving all
nine declared public-contract components: actions, constitution and safety, failures,
instruments, material catalog, observations, resources, scoring, and task.

Within each pair, the parent and child executed the same deterministic midpoint action
sequence under a fixed policy. Both variants were then repeated for exact executable-
trajectory replay, giving 6 pairs × 2 variants × 2 executions = 24 traces and zero
model-provider calls. All six pairs passed single-target lineage, public-contract
invariance, same-sequence executability, preregistered simulator-state and public-
observation divergence, exact replay, and zero-provider gates. These results establish
controlled programmability of the executable apparatus for the two tested
single-private-component interventions.

The claim ends at that boundary. The certificate does not establish untested
multi-component recombination, a general third-party world-authoring language, agent
adaptation or law learning, model ranking, or transfer to a physical laboratory. The
observed response differences are changes in hidden simulator-state variables and
synthetic public observations; the replay is exact environment/trajectory replay, not
reproduction of a physical material batch, apparatus, or model-generated decision.

## Methods text

### Registered-surface enumeration and counting units

We rebuilt the platform inventory from the live registries rather than transcribing
display counts. A task was one entry in `TASK_REGISTRY`, excluding aliases. An operation
kind was one globally unique entry in `OPERATION_TYPES`, counted once irrespective of
how many tasks exposed it; `discard_batch` was separately declared as a campaign-control
operation. An instrument was one entry in the five-member public `INSTRUMENTS` contract.
An evaluator binding was one ordered `(task_id, success_metric_id)` entry produced by the
task-metric contract builder; reuse of a metric identifier across tasks produced
separate bindings. The boundary-recipe count was the executed
`boundary_recipe_case_count` in the frozen task-design matrix. The deterministic audit
also required that all live task identifiers matched the matrix, every registered
operation and instrument was reachable, all bindings were executable and unique at the
task-metric level, and every task had executable midpoint and boundary recipes.

### Transaction, failure, resource, and instrument qualification

For each of the 28 registered operation kinds, we identified a registered task and
executed a valid action through its runtime kernel and domain service. We then submitted
an invalid action from a fresh deterministic environment and compared a hidden
simulator-state projection before and after the attempt. A probe passed only if the
valid action was `committed` and the invalid action returned either
`validation_failed` or `rolled_back` without changing that projection. A separate
constitution probe attempted an invalid negative-volume candidate and required atomic
rollback to the original state. Together with a hard resource-envelope rejection,
these probes exercised the four public transaction statuses.

Resource semantics were qualified with a campaign card that capped operation attempts,
vessel starts, final assays, non-final instrument uses, per-instrument uses, and material
stocks. Preflight derived and reserved the proposed resource delta. Outcome recording
then applied committed-only quantities, bound the normalized action and outcome to the
same deterministic event identifier, recomputed ledger state from ordered events, and
verified the canonical snapshot hash after restoration. Attempts remained a preflight
quantity, so a rejected or rolled-back attempt could consume attempt budget without
creating a stock, vessel, instrument, assay, or discard debit.

For each of HPLC, GC, UV–visible, pH meter, and final assay, the executable probe checked
the declared cost delta, destructive sample-volume delta, and whether termination was
required. The first four instruments were permitted before termination; final assay
required a terminated state. Latencies were read as scheduling-contract fields and
were not added to the process-state clock by this qualification. Instrument maturity
and calibration fields were interpreted only within each model card's synthetic
boundary.

### Frozen world-fork protocol and analysis units

The formal world-fork protocol fixed seeds 0, 1, and 2; a keyed-noise namespace; a
public midpoint policy generated from a unit vector of 0.5; the two intervention cases;
their private target components; simulator-state and public-observation divergence
oracles; and the all-gates pass rule before formal execution. For each case and seed, a
content-addressed parent and child were derived from the frozen component inventory.
Hashes were compared for every component, and a pair was rejected unless exactly its
declared private target changed and all nine public-contract hashes remained equal.

The same typed sequence was executed on the parent and child, and each execution was
repeated from the same bound identity and keyed-noise contract. Exact replay,
same-sequence executability, identity leakage, expected divergence, provider-call, and
lineage checks were evaluated for every pair. The scientific analysis unit was one of
the six parent–child pairs. The 24 traces were execution and replay accounting, not 24
independent experiments or agent trials. No policy, component target, seed, threshold,
oracle, gate, or display-entry rule was changed in response to the formal outcomes.

## Figure 1 integration contract and warning

- First reference is the Results sentence beginning “**Figure 1a–d** first establishes”.
- Panels A–B own the agent/world interaction loop and explicit identity, authority,
  evidence, resource, transaction, and replay controls.
- Panels C–D own the two single-private-component examples and the six-pair/24-trace
  gate summary.
- The figure must not carry agent competence, agent adaptation, general world-language,
  or physical-transfer conclusions.
- **Integration warning:** the current W1-P02 render labels panel B `physical identity`
  and `world + material`. Before final integration, W1-S07/W1-P09 and the Figure 1
  caption must define this as **hidden simulator-world/material identity**, or the label
  must be changed by the figure owner. It must not imply a reproduced physical batch,
  instrument, or laboratory apparatus.

## Evidence bindings

File SHA-256 values were recomputed in the isolated worktree. “Source commit” is the
commit that last changed the cited file on the reviewed history; embedded artifact
identities are listed separately where the format defines one.

| Evidence | Source commit | Path | File SHA-256 | Supports |
| --- | --- | --- | --- | --- |
| Frozen story architecture | `ed63799a9e88a98d03842f013fd244c2ebfb5230` | `workstreams/arxiv_v1/story/work-i-story-architecture-v0.1.md` | `de686d923df53c3754694eb2dca9550b1fc9fb6877848654760b73507dda4f9b` | Figure 1 owns apparatus plus controlled programmability, has no agent-performance role, and is first in narrative order. |
| F09 platform-surface audit | `96f35a70888cce2b24a26b8f8f2434b403be3463` | `workstreams/arxiv_v1/reports/work-i-platform-surface-v0.1.json` | `f9ad46d399bfde37389d8e93a2846a92b98e2ee405a11b04db0beef53485ba59` | 15 tasks, 28 registered operation kinds, five instruments, 62 task-metric bindings, 43 unique metric identifiers, 415 executed boundary recipes, and their counting rules. Embedded audit: `941278c0c5d3419989d5d93e187fc73494e05be5bb8c622c8f776978c6106b77`. |
| Operation registry | `1c9bfc5cd9d2a57b6ecc9b870a913b54c37a6514` | `src/chemworld/world/operations.py` | `023753613046d98a5f3045e078f307e8761d630dd8c392ea3a7f27eb531f4920` | `OPERATION_TYPES` has 28 members, while `discard_batch` is in the separate campaign-control tuple. |
| F10 semantics qualification | `af6a21651ed7808ffce96c302ce93852d564eb42` | `workstreams/arxiv_v1/reports/work-i-experiment-semantics-v0.1.json` | `cce0455d11d8081a57007fc5ec47e5988bfe3c8cf9dfb1f67da583c82c7350cc` | 28/28 valid commits, 28/28 invalid state-preservation probes, 5/5 instrument probes, four statuses, hard resource limits, and exact snapshot restoration. Embedded qualification: `91f7d5d5c49b98606825eee05832de60057a3e09677f1839443a33f0885013b3`. |
| Campaign ledger implementation | `1c9bfc5cd9d2a57b6ecc9b870a913b54c37a6514` | `src/chemworld/campaign_resources.py` | `bbf1a2def3f58053d32c4815182943ccba66fa72f4c1747053f2ab3790173d7b` | Preflight attempt charging, committed-only outcome deltas, action/outcome hashes, event-order reconstruction, and canonical snapshot replay. |
| Instrument contracts | `998315efadbf15f4d29aab94c18db7989ed2e61a` | `src/chemworld/world/instruments.py` | `7fce183ef3799bbb551561ddfdd2b481264804e93155499bf3afaa0f2bf8dd4e` | Five state-coupled synthetic instrument contracts, scheduling latency, model-card fields, and the explicit non-physical synthetic boundary. |
| Serious-task design policy | `03c6eb91eb26235a88cf4037cd1deefe0f274b34` | `src/chemworld/task_design.py` | `1f3ccc6b4f7262249f0f7d20d7aafa71f983ce411544d695b6e0520f130c857a` | Serious-task contract review rejects proxy-allowed kernels and keeps task status candidate rather than physically validated. |
| Frozen world-fork formal report | `af6a21651ed7808ffce96c302ce93852d564eb42` | `workstreams/arxiv_v1/reports/work-i-world-fork-qualification-v0.1.json` | `d16981dd3937d661ae65a972bcaacd22c793f086403410f78d103078d25288b8` | Two cases, seeds 0–2, six pairs, 24 traces, nine public components per pair, six gate families, and zero providers. Embedded formal report: `62684d414e9f9037b70d170abc6b29b442a928cf76df900a6bb53a3d60f2ee02`; protocol: `52e8846f0fdf28492ea2141fc008efe56d1b269f869678fdf017e65da9cbb7f8`. |
| Frozen world-fork certificate | `af6a21651ed7808ffce96c302ce93852d564eb42` | `workstreams/arxiv_v1/reports/work-i-world-fork-certificate-v0.1.json` | `8a0299b6957a700e720f46401a62b30a1da4ac2f8d71d57f00071805abcf9ad9` | Pair-level lineage, targets, public invariance, divergence, replay, and bounded interpretation. Embedded certificate: `5b09842469956d749370ace16d2b0698ec55eb69f46a13044810f6b2ca63ef78`. |
| Figure 1 handoff | `e0344545cc8fcae2e5663c31927be3bc1f8d13e2` | `paper/figures/experimental-intelligence-v1/publication/figure-1-apparatus-world-forks.manifest.json` | `1b01c22afe09483117e216fa739a48dba16f3c0322cb6e8c399eb9da8951df98` | Panel roles, evidence census, exclusion of performance/adaptation/physical-transfer claims, and the panel-B integration warning. W1-P02 remains independently reviewable. |
| Independent chemistry review | `4a71667cd56a71abb6003478205b3bf8b5719f31` | `workstreams/arxiv_v1/reviews/W1-Q04-chemistry-review--Yijun.md` on `work1/w1-q04-chemistry-review-yijun` | `d236cea8e44f53b4e65ba7dc73749b8b83b889ce316af3c4e88405fc4fd517cb` | Independent approval of the F evidence within the simulated-apparatus boundary and the required wording ceilings applied here. This review is a guardrail, not a replacement evidence source. |

The W1-S01 evidence map at remote branch commit
`dd6f01d66ab36278516f7037ce8f058641f0559a` was used as a secondary cross-check only;
all numeric statements and file hashes above were independently reconstructed from the
listed primary sources.

## Claim-language guardrails

Allowed short form:

> ChemWorld exposes a registered, executable experimental surface and qualified two
> controlled single-private-component world-fork classes under fixed-policy,
> provider-free probes.

Do not shorten the evidence into any of the following claims:

- 15 formal agent tasks, 62 unique metrics, or 415 physical/agent experiments;
- calibrated laboratory instruments, real-world safety, or empirical device/material
  validation;
- exact physical replay or reproduction of model-generated decisions;
- validated recombination of mechanisms, observation channels, instruments, resources,
  or failure laws beyond the two tested private targets;
- agent adaptation, law learning, chemical intelligence, or model superiority from the
  deterministic fork probe; or
- direct physical-laboratory transfer or a general third-party authoring language.

## Validation record

- `uv run python scripts/audit_work_i_platform_surface.py --check` — passed; rebuilt
  `15 / 28 / 5 / 62 / 415` and audit
  `941278c0c5d3419989d5d93e187fc73494e05be5bb8c622c8f776978c6106b77`.
- `uv run python scripts/qualify_work_i_experiment_semantics.py --check` — passed;
  rebuilt `28 / 28 / 5 / 4` semantic counts and qualification
  `91f7d5d5c49b98606825eee05832de60057a3e09677f1839443a33f0885013b3`.
- `uv run python scripts/summarize_work_i_world_fork.py --check` — passed; rebuilt six
  pairs, 24 traces, and certificate
  `5b09842469956d749370ace16d2b0698ec55eb69f46a13044810f6b2ca63ef78`.
- `uv run --extra dev pytest -q tests/test_work_i_platform_surface.py tests/test_work_i_experiment_semantics.py tests/test_world_fork_report.py tests/test_world_fork_public_contract.py tests/test_world_fork_divergence.py tests/test_task_design.py tests/test_state_transition_invariants.py`
  — **35 passed in 202.90 s**; provider/formal/agent executions: `0`.
- Wording scan, declared-write-set audit, `git diff --check`, and final file-hash audit
  are run again at handoff and recorded in the W1-S04 claim.
