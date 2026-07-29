# Flagship experiments

Two ChemWorld tasks currently have formal multi-world Participant campaigns:
Electrochemical Conversion and Reaction to Crystallization. Three additional tasks
now have a five-world development-only comparison, bringing complete comparative
execution to five tasks. This page records the design and results; see the
[authoritative current-status page](https://sunyrain.github.io/ChemWorld/benchmark_release/)
for release readiness.

## 1. Questions

The experiments separate two questions:

1. **S0 v1.0, no dossier:** how does the Participant compare with classical
   optimizers under anonymous materials and a fixed 20-experiment budget?
2. **S0 v1.2, three arms:** does correct material information help, does a targeted
   error mislead, and can experimental feedback support recovery?

The nominal dossier contains correct but limited attributes for anonymous
materials. It does not reveal the answer; performance still has to be learned
through experiments.

## 2. Frozen common contract

| Item | Frozen value |
| --- | --- |
| Tasks | Electrochemical Conversion; Reaction to Crystallization |
| Independent worlds | seeds 0–9 |
| Autonomous exploration | 20 complete experiments per task × world × arm |
| Participant | Codex subscription, `gpt-5.6-sol`, medium reasoning |
| Primary endpoint | paired blind-validated final-recommendation score |
| Replay | exact for every formal unit |
| Inference unit | independent world, not provider call or algorithm seed |

| Arm | Visible information | Causal role |
| --- | --- | --- |
| `opaque` | anonymous IDs, no dossier | no-information reference |
| `nominal` | correct attributes attached to each ID | correct information |
| `misindexed` | one target field has a fixed two-row swap | targeted wrong prior |

Within each task and world, the arms share the semantic world, keyed observation
noise, budget, model, scaffold, and blind endpoint. The paired contrast therefore
targets the dossier condition rather than world difficulty.

## 3. S0 v1.0: Participant and classical baselines

| Task | Codex | 95% world interval | Best information-matched | Best privileged calibration |
| --- | ---: | ---: | ---: | ---: |
| Electrochemical Conversion | **0.7150** | [0.6283, 0.7861] | Structured RF-EI 0.6159 | Descriptor RF-EI 0.6441 |
| Reaction to Crystallization | **0.5355** | [0.5045, 0.5644] | LHS 0.5708 | n/a |

Electrochemistry has a descriptive +0.0991 difference from the best
information-matched baseline, but is not stable against the best privileged
calibration baseline. Crystallization is below LHS. No superiority threshold or
multiplicity plan was preregistered, so these are formal descriptive results—not
broad SOTA or provider-effect claims.

## 4. S0 v1.2: three-arm results

### Value of correct information

| Task | Opaque | Nominal | Paired difference | Familywise 97.5% interval | Decision |
| --- | ---: | ---: | ---: | ---: | --- |
| Electrochemical Conversion | 0.7150 | **0.7874** | +0.0724 | [+0.0074, +0.1546] | positive information value |
| Reaction to Crystallization | 0.5355 | **0.5615** | +0.0260 | [−0.0130, +0.0630] | inconclusive |

### Wrong prior and recovery

| Task | Misindexed | Misindexed − Nominal | Manipulation | Action correction | Recovery to Opaque | Overall |
| --- | ---: | ---: | --- | --- | --- | --- |
| Electrochemical Conversion | 0.6853 | −0.1020; [−0.2101, −0.0078] | pass | pass | fail | **fail** |
| Reaction to Crystallization | 0.5845 | +0.0229; [+0.0046, +0.0419] | pass | fail | pass | **fail** |

The joint recovery rule requires a material early behavioral effect, later
correction away from the misleading action, and practical performance recovery
to the opaque arm. Passing only one component is not evidence that the model
identified and corrected the wrong dossier.

The higher misindexed crystallization score is only a benefit of this fixed swap
in the sampled worlds. Because action correction failed, it is not evidence of
error discovery.

## 5. Accounting and audit

| Item | S0 v1.0 | S0 v1.2 three-arm |
| --- | ---: | ---: |
| Formal units | 20 | 60 |
| Participant provider calls | 420 | 1,260 |
| Participant physical experiments | 760 | 2,280 |
| Physical experiments including baselines | 28,060 | baselines not counted again |
| Automatic retries | — | 5 |
| Method failures | 0 | 0 |
| Exact replay | all passed | all passed |

The three-arm campaign reuses the v1.0 opaque results; those observations are not
independent duplicates.

## 6. Evidence

- [v1.0 formal summary](https://github.com/sunyrain/ChemWorld/blob/main/workstreams/flagship_tasks/reports/static-s0-v1.0-formal-campaign-summary.json)
- [v1.2 three-arm summary](https://github.com/sunyrain/ChemWorld/blob/main/workstreams/flagship_tasks/reports/static-s0-v1.2-three-arm-information-campaign-summary.json)
- [v1.2 result audit](https://github.com/sunyrain/ChemWorld/blob/main/workstreams/flagship_tasks/STATIC_S0_V1_2_THREE_ARM_INFORMATION_RESULTS_ZH.md)
- [v1.2 preregistration](https://github.com/sunyrain/ChemWorld/blob/main/workstreams/flagship_tasks/STATIC_S0_V1_2_MISINDEXED_INFORMATION_PREREGISTRATION_ZH.md)

## 7. Boundary with mechanism adaptation

The three-arm study asks how prior information changes search in a static world.
Mechanism adaptation asks whether an Agent detects, attributes, and recovers from
a law change during a campaign. They share the evidence-correction narrative but
are not interchangeable experiments.

RC28 Gate A certified environment identifiability and online attainability only
on its historical frozen source. Its current-source binding is stale, and
Participant Gates B–E remain pending.

## 8. Five-task post-qualification extension

On source `74cfcdaa0d9780de2d21424ef8c329079554f8b5`, five tasks used the same
task-neutral Codex prompt, world seeds 0–4, 20 exploration experiments, and
3+3 blind validations. Five classical methods used the same public task
information. This is audited development evidence, not a preregistered
superiority study.

| Task | Codex | Best classical method | Difference | Wins/ties/losses against each world's best |
| --- | ---: | ---: | ---: | ---: |
| Electrochemical Conversion | **0.7454 ± 0.0522** | RF-EI 0.6622 | +0.0832 | 3 / 0 / 2 |
| Reaction to Crystallization | 0.5206 ± 0.0681 | **RF-EI 0.6071** | −0.0866 | 1 / 0 / 4 |
| Reaction to Distillation | **0.4795 ± 0.0264** | GP-EI 0.4192 | +0.0603 | 4 / 0 / 1 |
| Partition Discovery | 0.5426 ± 0.0870 | **GP-EI 0.5511** | −0.0085 | 1 / 0 / 4 |
| Flow Reaction Optimization | 0.1627 ± 0.0131 | **GP-EI 0.2145** | −0.0518 | 0 / 0 / 5 |

All 150 method-by-world cells and 3,900 physical experiments completed exact
replay. The new 13-dimensional reaction–distillation task reached its task
threshold in every world. No method reached Partition Discovery's frozen 0.58
cross-world threshold. Absolute scores are not comparable across tasks.

- [Machine-readable five-task summary](https://github.com/sunyrain/ChemWorld/blob/main/workstreams/flagship_tasks/reports/static-s0-five-task-postqualification-campaign-summary.json)
- [Detailed Chinese audit](https://github.com/sunyrain/ChemWorld/blob/main/workstreams/flagship_tasks/STATIC_S0_FIVE_TASK_POSTQUALIFICATION_RESULTS_ZH.md)
