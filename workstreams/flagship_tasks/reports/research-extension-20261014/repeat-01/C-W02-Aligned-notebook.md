# repeat-01 / C-W02-Aligned — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T16:51:12.049014+00:00; available public operations: 0; reviewed through: None.

# Hypothesis notebook

## H1 [tentative]
Within the nominal dossier, solvent S2 should favor high recovery and larger/cleaner crystals because it combines low relative solubility, high growth, low nucleation, and low occlusion. S1 is the main alternative if S2 gives inadequate conversion or unexpected residual behavior.

## H2 [tentative]
Catalyst C1 or C3 should outperform C0, but fixed-world residuals may reverse this. A moderate-temperature reaction with the full per-batch nominal charge, followed by seeded slow cooling and a growth hold, is expected to meet purity >=0.80 and fines <=0.50. Particle-size measurements will test whether slower cooling and/or more seed reduces fines; final assays determine recovery.

Decision rule: first establish a feasible S2/C1 baseline, then vary catalyst/solvent and crystallization history. Prefer the highest observed crystal_yield among batches satisfying both constraints; reverse these priors if direct assays disagree.

## Revision 2

Recorded: 2026-10-13T16:55:24.715809+00:00; available public operations: 220; reviewed through: runner-operation-0220.

# Hypothesis notebook

## H1 [rejected in tested scope]
The dossier-based expectation that S2 would give the best particle distribution was contradicted. Across S2 processes, final fines remained about 0.995–1.000 despite seed-dose, extended hold, delayed seeding, and thermal-cycle variants (final assays runner-operation-0014, -0030, -0055, -0070, -0090). These interventions were confounded across batches, so individual kinetic effects remain unresolved, but none made S2 feasible.

## H2 [supported qualitatively, not to specification]
Solvent identity dominated the observed crystallization response. The S3 baseline reduced final fines to 0.647 while retaining high purity (runner-operation-0132), materially better than the tested S0/S1/S2 endpoints. Deeper staged cooling to 250 K further reduced fines to 0.513 and gave recovery 0.451 (runner-operation-0196). Repeating nominal growth calls at 250 K gave a numerically similar, not clearly improved result: fines 0.518 and recovery 0.454 (runner-operation-0220). With single noisy assays and no exact replicate, the small difference is not evidence of a duration effect.

## H3 [unresolved]
For S3, larger seed dosing did not clearly improve fines: the 1 g cumulative-dose process still assayed at 0.669 fines (runner-operation-0181), while 0.05 g with deeper cooling reached 0.513 (runner-operation-0196). Temperature endpoint/history is the more plausible driver in this tested region; the seed comparison is confounded by cooling history.

## Final decision
No completed batch met both required constraints because every final fines estimate exceeded 0.50; purity was comfortably above 0.80 throughout the leading S3 runs. Batch 11 is the closest-to-feasible recommendation (purity 0.993, fines 0.513, recovery 0.451; runner-operation-0196). Batch 12 had slightly higher recovery (0.454) but a slightly larger fines violation (0.518; runner-operation-0220). Further work should extend or modify S3 thermal processing near/below the available 250 K limit and replicate the boundary region; a result convincingly below 0.50 would change the feasibility conclusion.
