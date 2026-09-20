# EQ-S five-world mechanism-characterization block — final report

## Completion and execution integrity

Completed 15/15 independent source sessions, 180/180 autonomous source batches, 60/60 sealed K1/Q/K2/EQS posttests, and 300/300 reference executions. All 15 source trajectories replay exactly and all 15 effective posttest chains are valid.

The provider-free gate passed all 12 registered checks on 15 campaigns and 180 batches with zero model calls. The first W01 canary retained a provider-schema failure affecting EQS only: the API rejected `uniqueItems` before inference. Version v0.2.1 removed that unsupported provider-schema keyword while retaining explicit local uniqueness validation. The three original nonconforming results remain preserved; recovery reused their threads and reran no source experiment, K1, Q, or K2.

## Quantitative prediction performance by information arm

Each row macro-averages the three scored public metrics within each cell and then the five physical worlds. These adaptive development results are descriptive and are not a powered causal estimate of prior-arm effects.

| Arm | Cells | Mean MAE | Mean 80% coverage | Mean width | Mean interval score | Family correct | Abstentions |
|---|---:|---:|---:|---:|---:|---:|---:|
| Opaque | 5 | 0.00994378 | 0.93 | 0.0362389 | 0.0531115 | 0/5 | 5/5 |
| Aligned | 5 | 0.0129193 | 0.931111 | 0.0465333 | 0.0672989 | 0/5 | 5/5 |
| MisIndexed | 5 | 0.0112024 | 0.891111 | 0.0376222 | 0.0713981 | 0/5 | 5/5 |

Opaque had the lowest aggregate MAE and interval score in this single five-world block; Aligned had the highest mean coverage but also the widest intervals. MisIndexed was intermediate on MAE and had the lowest mean coverage. These rankings vary by world and should not be generalized without replication.

## World-by-world result

| World | Truth family | Opaque MAE / coverage | Aligned MAE / coverage | MisIndexed MAE / coverage | EQS outcome in all arms |
|---|---|---:|---:|---:|---|
| EQ-S-W01 | direct_free_ion_precipitation | 0.017131 / 0.883333 | 0.00291575 / 0.994444 | 0.0130304 / 0.911111 | indeterminate |
| EQ-S-W02 | aqueous_ion_pair_intermediate | 0.00702545 / 0.961111 | 0.0420611 / 0.766667 | 0.0123695 / 0.972222 | indeterminate |
| EQ-S-W03 | direct_free_ion_precipitation | 0.0167711 / 0.844444 | 0.01315 / 0.922222 | 0.0125727 / 0.816667 | indeterminate |
| EQ-S-W04 | aqueous_ion_pair_intermediate | 0.00508632 / 0.977778 | 0.00371196 / 0.977778 | 0.00411713 / 0.933333 | indeterminate |
| EQ-S-W05 | direct_free_ion_precipitation | 0.00370499 / 0.983333 | 0.00275782 / 0.994444 | 0.0139221 / 0.822222 | indeterminate |

## Structural identification result

All 15/15 EQS payloads were schema-valid, but every cell selected `indeterminate`. Therefore network-family accuracy is 0/15 and the abstention rate is 15/15. This applies to all 9 direct-network cells and all 6 ion-pair cells.

The result is scientifically informative: the preregistered simulator-level non-collapse gate shows that the two topology families cannot be absorbed by the registered four-parameter direct null on held-out conditions, yet the autonomous agents did not convert their 12 adaptive observations into a categorical topology claim. The likely bottleneck is agent experimental design and inference, not a failed physical contrast. This interpretation is an inference from the gate and agent outputs, not a new experiment.

## Scope and evidence boundary

This is an S-locus mechanism-characterization block, not a process-optimization block. Opaque received no instance dossier. Aligned and MisIndexed received field-matched opposite topology claims without numerical constants or Q coordinates. K1 preceded Q; Q preceded K2; K2 preceded EQS; all 15 EQS responses preceded truth generation. The reports preserve unfavorable results and the v0.2 schema incident. No model call was repeated because of a scientific answer or score.

## Contents

- [EQ-S-W01--Aligned](sources/EQ-S-W01--Aligned/EXPERIMENT_REPORT.md)
- [EQ-S-W01--MisIndexed](sources/EQ-S-W01--MisIndexed/EXPERIMENT_REPORT.md)
- [EQ-S-W01--Opaque](sources/EQ-S-W01--Opaque/EXPERIMENT_REPORT.md)
- [EQ-S-W02--Aligned](sources/EQ-S-W02--Aligned/EXPERIMENT_REPORT.md)
- [EQ-S-W02--MisIndexed](sources/EQ-S-W02--MisIndexed/EXPERIMENT_REPORT.md)
- [EQ-S-W02--Opaque](sources/EQ-S-W02--Opaque/EXPERIMENT_REPORT.md)
- [EQ-S-W03--Aligned](sources/EQ-S-W03--Aligned/EXPERIMENT_REPORT.md)
- [EQ-S-W03--MisIndexed](sources/EQ-S-W03--MisIndexed/EXPERIMENT_REPORT.md)
- [EQ-S-W03--Opaque](sources/EQ-S-W03--Opaque/EXPERIMENT_REPORT.md)
- [EQ-S-W04--Aligned](sources/EQ-S-W04--Aligned/EXPERIMENT_REPORT.md)
- [EQ-S-W04--MisIndexed](sources/EQ-S-W04--MisIndexed/EXPERIMENT_REPORT.md)
- [EQ-S-W04--Opaque](sources/EQ-S-W04--Opaque/EXPERIMENT_REPORT.md)
- [EQ-S-W05--Aligned](sources/EQ-S-W05--Aligned/EXPERIMENT_REPORT.md)
- [EQ-S-W05--MisIndexed](sources/EQ-S-W05--MisIndexed/EXPERIMENT_REPORT.md)
- [EQ-S-W05--Opaque](sources/EQ-S-W05--Opaque/EXPERIMENT_REPORT.md)
