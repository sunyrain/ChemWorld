# Experiment 1 P benchmark asset authoring note v1.1.0

Status: **ASSET BUILD PREREGISTERED; FORMAL QUALIFICATION NOT AUTHORIZED**

## Purpose

This block builds the prerequisites that the v1.0.1 readiness audit found absent. It does not
promote smoke seeds, run P-W01--W05 qualification, or change Q1--Q8. Asset authoring must finish,
pass focused tests and be frozen in a later execution contract before any formal denominator is
opened.

## Five private Worlds

All Worlds use the public `reaction-to-purification` contract and seeds `0..4`, but they also carry
preregistered downstream interventions so they are not merely five noise seeds:

| World | Role | Private downstream intervention |
| --- | --- | --- |
| P-W01 | central | none |
| P-W02 | stronger partition | partition-strength extrapolation `+0.50` |
| P-W03 | weaker partition | partition-strength extrapolation `-0.50` |
| P-W04 | aqueous-favored phase ratio | phase-volume extrapolation `-0.50` |
| P-W05 | coupled boundary | partition-strength `+0.25`, phase-volume `+0.50` |

The runtime must derive private truth and hashes from these parameters. Observable labels are not
authored by hand.

## Entity asset

P-E uses four anonymous extractants `X0..X3` under the purification workflow's historical
extractant-index contract. The task-specific dossier is computed at two feed-composition anchors
using one common contact protocol. Aligned and misspecified priors have identical schema and
precision. The frozen derangement is `[X2, X0, X3, X1]`; it has no fixed point and is not selected
from formal outcomes.

## Parametric asset

P-P targets

`S* = K_product / K_impurity`

at the reference extractant/contact context. The oracle is executable, not prompt-authored.
Aligned and misspecified bands are symmetric in log space with the same half-width. The false
center is displaced by a preregistered signed log shift; band width, units and rendering remain
identical. Low/high phase-ratio and product-rich/impurity-rich anchors are reserved for later
qualification.

## Structural private family

P-S compares:

- parent: composition-independent intrinsic `K_product` and `K_impurity`;
- child: `partition_composition_response_stress_v1`, where product and impurity coefficients respond
  oppositely to the actual feed fractions under the same public action contract.

The child remains positive and mass conserving. It must change the separation-factor response
between at least two feed anchors and cannot be represented by one refitted constant K. A prompt
description alone is not an asset.

## Stop and execution rules

This stage may run focused unit/runtime tests and provider-free calibration only. Before any
data-producing calibration block, write a separate concise experiment note fixing anchors,
denominators and pass/fail rules. Do not run formal qualification until all assets are hash-bound
in a new contract. Failures are retained; no gate is weakened and Participant/provider calls remain
zero.
