# Confirmatory Benchmark Tasks: Design, Preregistration, and Status

> **Showcase Worlds demonstrate platform breadth; Confirmatory Benchmark Tasks carry confirmatory claims. They are no longer described by the same “flagship” label.**

## Two orthogonal sets

The homepage presents four **Showcase Worlds**: partition discovery,
reaction-to-crystallization, reaction-to-distillation, and flow-reaction
optimization. They demonstrate the experimental-reasoning and physical-chemistry
feedback supported by ChemWorld.

The mechanism-adaptation protocol currently has two **Confirmatory Benchmark
Tasks**:

| Confirmatory task | Hidden change families | Intervenable diagnostic coordinates | Main observations |
| --- | --- | --- | --- |
| Reaction to Crystallization | rate law, reaction topology, catalyst mapping | catalyst dose, temperature/time, catalyst choice | HPLC, final assay, task score |
| Electrochemical Conversion | constitutive law, solvent mapping, electrolyte-profile mapping | potential, current, time, solvent, electrolyte profile | UV-Vis, final assay, task score |

A showcase card is not confirmatory evidence, and a confirmatory task need not be
one of the four homepage cards. Some internal `flagship` identifiers remain for
API compatibility; they no longer define the scientific taxonomy.

## Current state machine

| State | Current value |
| --- | --- |
| Environment design candidate | passed |
| Semantic protocol audit | passed, RC24 25/25 |
| A1 physical validity | passed, RC24 81/81 design checks |
| A2 controlled identifiability | pending |
| A3 online attainability | pending |
| Participant-Agent Gates B–E | pending |
| Private confirmation | sealed |
| Publication ready | `false` |

The 25 semantic checks and 81 design checks are audit checks, not 106 independent
pieces of scientific evidence. The protocol is executable and preregistrable,
but no new A2/A3 confirmatory result exists yet.

## What A1, A2, and A3 certify

| Level | Certification subject | Purpose |
| --- | --- | --- |
| A1 | physical world and hidden intervention | Is the change real, single-axis, reachable, and visible in public observations? |
| A2 | controlled oracle/decoder | Are candidate families distinguishable under controlled, budget-matched experiments? |
| A3 | frozen reference diagnostic policy | Can one compliant online policy build a reference, detect a hidden change, and identify its family without receiving change time or truth? |
| Gates B–E | evaluated participant Agent | Detection, feedback use, adaptation/recovery, and procedural autonomy |

A DeepSeek, Claude, or other participant failure therefore cannot redefine A3
or make the environment automatically “unidentifiable.” A3 is formally the
**Online attainability certificate**. Participant Agents begin at Gate B.

## Calibrated online-change semantics

```text
truth change time ∈ {never, 6, 8, 10}
total experiment horizon = 18
relative checkpoints k ∈ {1, 2, 4, 8}
```

`τ=6` means exactly that the first six complete experiments use the old world;
experiment 7 is the first eligible changed-world experiment. The policy sees
only the total horizon and that the world may remain stable or change at an
unspecified time. The minimum stable prefix, candidate change times, truth,
reference certificate, pseudo-checkpoint, and relative checkpoint are hidden.

`never` is a first-class truth state. Its evaluator pseudo-checkpoint creates no
runtime event and changes no instance identifier, metadata, reset rule, or
random-number stream.

## A3 reference sufficiency is not a six-ID checklist

The frozen six-action recipe is a reproducible **canonical witness set**, not
the only valid answer. The certificate is based on **relation closure**:

- varied fields and controlled backgrounds satisfy the declared relation;
- rate-law or constitutive-law low/pivot/high levels are formed;
- topology and material-map same-background contrasts are closed;
- observable signatures have non-saturated fit information; and
- reference age remains inside the frozen limit.

A future policy may use different continuous doses or scan points. It does not
fail merely because it did not call `design-00` through `design-05`, provided
that it closes the same relations and passes predictive adequacy.

## Predictive adequacy avoids circular certification

Development data freeze only the feature encoding, predictive family, action
selection rule, and thresholds. Each A3 campaign estimates nuisance reference
parameters from its own pre-change observations using leave-one-experiment-out
cross-fitting. A held-out old-world observation cannot fit its own parameters;
post-change observations and the realized family label are prohibited.
Standardized error, predictive log score, and 95% prediction-interval coverage
are retained.

## Changed and never use different denominators

Let `R` denote reference sufficiency, `D_change` a change alarm, and `A` correct
family attribution.

Changed campaigns report:

```text
P(R | changed)
P(D_change | R, changed)
P(A | D_change, R, changed)
P(R ∧ D_change ∧ A | changed)
```

No-change campaigns report:

```text
P(R | never)
P(no false alarm | R, never)
FPR_horizon = P(ever alarms within the eight-experiment window | never)
```

Attribution is undefined for `never`, so no never row enters an attribution
denominator. Reference failures leave only the conditional attribution
denominator and remain failures in the changed end-to-end rate.

## Time-resolved detection

Recall(k), AUROC(k), Brier(k), and matched no-change FPR(k) are reported at
`k={1,2,4,8}`. The primary Brier score first weights changed and never equally,
then averages the four checkpoints equally.

```text
T_D = min{k : p(change) >= 0.5}
```

A changed campaign not detected by `k=8` is right-censored. It is not assigned
8 or infinity and is not deleted. Horizon FPR records whether a threshold was
ever crossed, so a later posterior decline cannot erase an earlier false alarm.

## Sample size and independence

RC24 freezes:

- 180 independent world-seed clusters per task/family in A2, A3, and private confirmation;
- exactly 60 clusters per `τ∈{6,8,10}` for each changed family;
- 180 `never` clusters per task;
- five provider repeats per paired cell as nested technical repeats, not independent samples; and
- `task_id + world_seed` as the cluster-bootstrap unit.

With 30 clusters and true reference success 0.90, the probability of satisfying
the Wilson lower-bound rule is only about 0.18. At 180 clusters it is about
0.964. Under true recall 0.90 and FPR 0.05, the frozen cluster-bootstrap pass
probabilities are about 0.978 and 0.808. Power remains limited if true reference
success is only 0.85; the audit states that limitation explicitly.

## Strictly paired no-change controls

Each changed/never twin shares initial state, world seed, pre/post session
boundary, reset rule, action schedule, observation-noise key (common random
numbers), and checkpoint-adjacent metadata. The only permitted difference is
whether the hidden physical-law intervention is applied. The pseudo-checkpoint
has no runtime side effect, and no reset or instance signal reaches the policy.

## Stratified gate rule

A3 uses an intersection:

1. overall pass;
2. Reaction to Crystallization pass;
3. Electrochemical Conversion pass;
4. every changed family pass; and
5. macro-average pass.

The pooled micro-average is supplemental. An easy task or family cannot conceal
a locally unattainable one.

## Evidence boundary for Gates B–E

The current design audit found no Gate C–E prerequisite confusion analogous to
the old A3 error, but their **empirical validity remains untested**:

- Gate B evaluates participant-Agent temporal detection and calibration;
- Gate C must still validate identical-prefix feedback pairs and provider noise;
- Gate D must still validate frozen, adaptive, and oracle policy definitions; and
- Gate E must still establish that assisted history does not contaminate later autonomous runs.

A semantic-audit pass is not an empirical Gate C–E pass.

## Single preregistration entry point

Before A2/A3, the sole controlling file is:

`configs/benchmark/mechanism-adaptation-preregistration-v0.3.0-rc24.json`

It binds source commit, protocol/plan/relation/scorer hashes, cohort namespaces,
sample size, reference-policy version, thresholds, checkpoints, bootstrap,
stratification, failure handling, exclusions, stopping, and private-unseal
conditions. Any bound change creates a new RC and cannot reinterpret existing
results.

## Audit entry points

- Protocol: `configs/benchmark/mechanism_adaptation_v0.3.0.json`
- Gate A plan: `configs/benchmark/mechanism_adaptation_gate_a_v0.3.0.json`
- Preregistration: `configs/benchmark/mechanism-adaptation-preregistration-v0.3.0-rc24.json`
- Sample-size audit: `mechanism-adaptation-sample-size-audit-v0.3.0-rc24.json`
- Relation graph: `mechanism-adaptation-diagnostic-relation-graph-v0.3.0-rc24.json`
- Semantic audit: `confirmatory-task-semantics-audit-rc24.json`
- Current-state source: `configs/current.json`
