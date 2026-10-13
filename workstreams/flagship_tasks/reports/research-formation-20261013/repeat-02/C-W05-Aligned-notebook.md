# repeat-02 / C-W05-Aligned — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T11:56:17.166044+00:00; available public operations: 0; reviewed through: None.

# Hypothesis notebook

## H1 [tentative]
Within the anonymous-material prior, S2 should favor crystal growth, purity, and recovery because it has low relative solubility and impurity occlusion, while slow cooling plus moderate seeding should suppress fines. C1 or C3 may give strong reaction performance. This is only a prior; world-specific residuals may reverse rankings.

**Pre-experiment prediction:** a concentrated reaction using C1, followed by S2 crystallization with 0.5–1 g seed, slow cooling, and a growth hold will meet purity ≥0.80 and fines ≤0.50, and outperform unseeded/fast-cooled controls in recovery or size. If early assays contradict this, screen material identities before thermal fine-tuning.

## Revision 2

Recorded: 2026-10-13T11:58:22.581742+00:00; available public operations: 56; reviewed through: runner-operation-0056.

# Hypothesis notebook

## H1 [revised: supported only for growth/fines, rejected for recovery ranking]
The nominal S2 prior correctly anticipated acceptable morphology and purity, but not maximal recovery. Under C1, 370 K/3600 s and 280 K/14400 s, S1 gave the highest observed recovery (0.456) while satisfying purity and fines; S2 gave about 0.383–0.385. S0 and S3 produced excessive fines (~0.87–0.88), so they are unsuitable in this thermal regime. Evidence: final assays runner-operation-0013, -0023, -0034, -0045, -0056. Differences exceed single-instrument noise scale, but the S1 comparison is not replicated and solvent changes both reaction and crystallization.

## H2 [tentative]
Use S1 for optimization. Screen catalysts under fixed S1 conditions, then test lower final temperature and reaction severity. Prediction: cooler endpoints should increase recovery, but may increase nucleation/fines; longer/slower cooling or seeding may keep fines ≤0.50. A catalyst that improves upstream selectivity may indirectly improve crystal purity/recovery.

## Revision 3

Recorded: 2026-10-13T11:59:27.084408+00:00; available public operations: 133; reviewed through: runner-operation-0133.

# Hypothesis notebook

## H1 [supported in tested scope]
Solvent identity strongly controls crystallization morphology and recovery. Under the common 370 K reaction / 280 K slow-cooling regime, S1 was the best compliant solvent observed; S0 and S3 produced fines well above 0.50, whereas S1 and S2 were compliant. The result reverses the dossier-based expectation that S2 would maximize recovery. Evidence: final assays runner-operation-0013, -0023, -0034, -0045, -0056.

## H2 [supported in tested scope]
With S1, C0 gave higher observed crystal recovery (0.508) than C1, C2, or C3 at the shared thermal conditions while maintaining high purity and compliant fines (runner-operation-0067 versus -0034, -0078, -0089). Material and reaction effects remain partially confounded because only one batch per catalyst was run.

## H3 [supported directionally; optimum unresolved within noise]
For C0/S1 at 370 K for 3600 s, lowering the crystallization endpoint from 280 K to 260 K and 250 K increased observed recovery from 0.508 to 0.547 and 0.560 without violating the fines constraint (runner-operation-0067, -0100, -0111). The 250 K endpoint is the legal lower bound, so further endpoint optimization was not possible. A 380 K reaction followed by the same 250 K crystallization gave recovery 0.5595 (runner-operation-0133), numerically indistinguishable from the 370 K result relative to assay noise; reaction-temperature superiority is unresolved. The 350 K/7200 s variant was worse (runner-operation-0122), but temperature and duration were confounded.

## Decision
Recommend batch 10 because it has the highest observed seed-excluded crystal recovery (0.5600) among compliant batches, with purity 0.976 and fines 0.435. Batch 12 is a near-tie (0.5595 recovery, 0.993 purity, 0.466 fines) and provides no convincing recovery gain. A future replication of batches 10 and 12 would be needed to resolve the tiny difference.
