# repeat-03 / EQ-W01-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T12:22:57.114042+00:00; available public operations: 0; reviewed through: None.

# Source-stage hypothesis notebook

## H1 [tentative; pre-experiment]
Within this bounded aqueous slice, pH and acid dissociation should primarily track total concentration (reagent loading/liquid volume), while the precipitation proxy may introduce a threshold or saturation-like departure at higher concentration. Equal-concentration pairs made with different absolute loading and volume should be similar if concentration alone is sufficient; systematic differences would support an additional extensive/loading or volume effect.

## Planned discriminations
Use a concentration ladder with repeated concentration values obtained by different loading/volume pairs. Purchase one pH-meter observation before termination and the required final assay afterward in every independent batch; agreement will indicate repeatability at the instrument scale. This is a prediction, not yet evidence. Water-only solvent scope is intentional; no claim will be made about other solvents.

## Revision 2

Recorded: 2026-10-13T12:24:11.575869+00:00; available public operations: 60; reviewed through: runner-operation-0060.

# Source-stage hypothesis notebook

## H1 [not supported as a simple concentration law in tested scope]
Prediction before experimentation: pH and dissociation would primarily track concentration, with precipitation becoming threshold-like at high concentration. Across water batches spanning nominal 0.0625–2 mol/L, the final-assay pH-normalized values remained in a narrow, non-monotone band (about 0.250–0.256), dissociation about 0.063–0.079, and precipitation proxy about 0.144–0.162 (final assays: runner-operation-0005 through runner-operation-0060 at five-event intervals). Given stated final-assay standard deviations (0.002, 0.006, 0.006 respectively), extrema alone are not persuasive evidence of a smooth loading/concentration response, and multiplicity plus lack of monotonicity further weakens that interpretation.

## H2 [supported in this scope: broad invariance; unresolved fine structure]
Equal-concentration comparisons are broadly compatible with concentration-only invariance but do not uniquely establish it. At nominal 0.5 mol/L, different loading/volume pairs (events runner-operation-0020, -0035, -0050) gave nearly equal dissociation (~0.0673–0.0692) and overlapping pH/precipitation ranges. At 0.25 mol/L (events -0015, -0030, -0045), the pH span was larger (~0.006 normalized) and dissociation differed by ~0.012; these are numerical differences but, without independent same-condition final-assay replication, remain unresolved possible volume/loading effects versus noise/batch variation. At 1 mol/L (events -0040, -0055), dissociation also differed by ~0.009.

## H3 [instrument-repeatability qualification]
Pre-termination pH-meter and final-assay estimates are not interchangeable precision replicates: their declared noise differs. Some pairs agree closely (especially batch 3: runner-operation-0013 vs -0015), while several dissociation/precipitation pairs differ materially relative to the final-assay noise alone (e.g. batches 7 and 9). This supports using final assays for cross-batch comparisons and treating meter/final discrepancies as measurement-method variation, not time evolution (both are instantaneous and termination itself does not advance chemistry).

## Effective scope and alternatives
Supported claim is deliberately narrow: room-temperature, immediate, water-only mixtures with 0.005–0.04 mol reagent and 0.02–0.08 L starting liquid. No supplied task-specific local relationship was available to validate. Within this design, a nearly constant response plus bounded measurement noise is observationally adequate. Equivalent alternatives include a weak nonlinear concentration response, separate small loading/volume terms, or a precipitation threshold outside/too subtle within the tested range. Precipitation proxy showed no convincing high-concentration rise.

A decisive follow-up would replicate identical recipes with final assays and use staged dilution within the same batch; a reproducible shift exceeding method variation at fixed loading would favor a volume/concentration effect. Batch 3 is the preferred evidentiary anchor because it is a central repeated-concentration condition and its two instruments agreed unusually closely across all three scientific channels.
