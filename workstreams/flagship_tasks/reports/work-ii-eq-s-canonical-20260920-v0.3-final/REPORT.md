# EQ-S v0.3 canonical mechanism-characterization block — final report

## Completion and execution integrity

Completed 15/15 independent source sessions, 180/180 autonomous source batches, 45/45 sealed K1/Q/K2 posttests, and 300/300 reference executions. All 15 source trajectories replay exactly and all 15 effective posttest chains are valid.

The zero-provider gate passed before launch. W01 ran as a three-arm canary, followed by the remaining matrix with at most eight isolated workers. Retained provider failures were recovered only from the latest legal same-thread boundary: original records remain preserved, physical source experiments were not rerun, and the questions, model, worlds, and scoring contract were unchanged.

## Quantitative prediction performance by information arm

Each row macro-averages the three scored public metrics within each cell and then the five physical worlds. These adaptive development results are descriptive, not a powered causal estimate of arm effects.

| Arm | Cells | Mean MAE | Mean 80% coverage | Mean width | Mean interval score |
|---|---:|---:|---:|---:|---:|
| Opaque | 5 | 0.0140815 | 0.914444 | 0.0331222 | 0.099516 |
| Aligned | 5 | 0.0158966 | 0.825556 | 0.0365444 | 0.0999331 |
| MisIndexed | 5 | 0.0134496 | 0.842222 | 0.0331167 | 0.0800547 |

## World-by-world quantitative result

| World | Opaque MAE / coverage | Aligned MAE / coverage | MisIndexed MAE / coverage |
|---|---:|---:|---:|
| EQ-S-W01 | 0.00264636 / 0.994444 | 0.00309443 / 0.988889 | 0.0224358 / 0.716667 |
| EQ-S-W02 | 0.00891616 / 0.955556 | 0.00726175 / 0.972222 | 0.00819065 / 0.972222 |
| EQ-S-W03 | 0.0522224 / 0.727778 | 0.0183786 / 0.861111 | 0.0134359 / 0.855556 |
| EQ-S-W04 | 0.00456377 / 0.916667 | 0.0360295 / 0.483333 | 0.00594249 / 0.922222 |
| EQ-S-W05 | 0.00205904 / 0.977778 | 0.0147189 / 0.822222 | 0.017243 / 0.744444 |

## Mechanism-report interpretation

K1 is the primary mechanism artifact and remains open-form. It must be read or externally audited on the preregistered descriptive dimensions: proposed species/processes, proposed reaction edges or equations, evidence-versus-conjecture separation, true common-backbone coverage, treatment of an aqueous intermediate or competing networks, and calibration to identifiability limits. The protocol deliberately provides no closed-set family-accuracy headline and no single composite mechanism score.

## Scope and evidence boundary

This is an S-locus mechanism-characterization block, not a process-optimization block. Opaque received no instance dossier. Aligned and MisIndexed received field-matched opposite topology claims without numerical constants or Q coordinates. Every participant received the same canonical K1 and K2; only the preregistered EQ-S Q payload is system-specific.

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
