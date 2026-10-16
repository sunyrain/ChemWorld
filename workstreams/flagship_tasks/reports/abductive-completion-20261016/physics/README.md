# Matched-world physical qualification

This is provider-free development evidence for W2-263, separate from the subsequent 30 autonomous research sessions. The [experiment note](../../../WORK_II_ABDUCTIVE_COMPLETION_20261016.md) fixes every executed block and retains the unsuccessful first candidate.

## Scientific construction

Five matched parameter pairs share effective acidity, solubility product, cation loading, activity coefficient, public operation interface and initial-condition seed. In each pair, one closed equilibrium network permits direct free-ion precipitation; the other additionally permits neutral aqueous ion-pair association. Both enforce acid and cation balances, electroneutrality, mass action and solid complementarity. The implementation uses the existing runtime interventions and solver without modifying their physics.

The two reference assays contain 6e-7 mol reagent in 0.08 and 0.075 L solvent. Their paired noise-free differences are below one instrument standard deviation on all three channels. Reference observations are actual, separately realized world-specific assays with shared keyed noise, not fabricated identical observations. They are a supplied scaffold, outside the 12 batches chosen by each participant. The accessible diagnostic grid spans 0.001--1 M. The prediction questions are withheld from participants until the scientific account is sealed; qualification itself necessarily evaluates these conditions.

## Retained blocks

| Block | Coverage and outcome |
|---|---|
| Candidate 1 | 210/210 kernel states; all closure checks and reference-overlap checks passed. P05 failed the requirement for at least two diagnostic conditions separated in two channels. All 30 runtime campaigns retained: 190/210 assays completed; 20 reference assays failed the existing material precondition. Every campaign replayed exactly. |
| Fixed calibration | 210/210 states, no numerical failures. Enumerated all 12 legal reference candidates across 10 worlds and the nine-point diagnostic grid. The fixed minimum-worst-gap selection rule selected the two reference recipes above. No physical parameter or threshold was changed. |
| Candidate 2 | 230/230 kernel states; 30/30 runtime campaigns, 230/230 assays and 960/960 committed operations. All 30 campaigns replayed at zero tolerance. No failures. |
| Nuisance refit | Five pre-specified direct-network fits to the ion-pair worlds, all optimizer-success flags true. Reported independently from qualification and participant performance. |

The maximum normalized physical closure residual in candidate 2 is **3.63e-11**. All 60 noise-free scale/path comparisons agree within 1e-9. All five pairs have at least one response channel separated by three assay standard deviations at all nine diagnostic conditions; the numbers separated in at least two channels are **7, 6, 5, 5 and 3**.

The paired runtime readback checks 115 condition pairs against the kernel predictions. Common keyed noise cancels between corresponding unclipped observations; the largest remaining contrast discrepancy is **4.57e-8**, consistent with the public observation float conversion. Ninety clipped channel pairs are explicitly excluded from this subtraction check. Submitted actions, committed operation status, volume deltas, observed results and exact replay are retained in `attempt-02/runtime.json`; this validates a change in actual chemical outputs, rather than interpreting renamed commands as different chemistry.

An additional readback replays the retained twelve heldout action sequences for every world and captures actual premeasurement physical means from the runtime. **120/120 means across all ten worlds agree with the standalone kernel within 1e-10**, including all five ion-pair worlds. All ten readback trajectories replay exactly. This reuses existing conditions; it is not a new mechanism-selection or participant block. See `attempt-02/runtime-physical-means.json`.

## Nuisance-refit limitation

The direct-family null was permitted to vary pKa, solubility product, cation fraction and activity coefficient, with fixed bounds and optimizer settings in the note. Its noise-scaled mean-square fitting errors were **36.77, 31.67, 26.54, 21.74 and 17.58**. On the twelve prediction queries, at least two channels exceeded three assay standard deviations for **12, 12, 12, 12 and 10** queries, respectively. Queries sharing a final concentration are controls, not independent mechanism tests.

These are best numerical refits under a bounded, specified family. They provide evidence against simple parameter refitting as an adequate account of this response grid; they do not prove global identifiability among all possible mechanisms. Agents need not recover simulator labels, and an explanation may remain unresolved on the particular evidence an agent chooses to obtain.

## Files and reproduction

- `attempt-01/`: full unsuccessful first candidate; never replaced.
- `calibration-02.json`: all calibration states and the fixed reference selection.
- `attempt-02/`: successful restarted qualification, actual public reference observations and paired runtime/kernel readback.
- `nuisance-refit.json`: all five fitted parameter vectors, optimizer status, heldout errors and any failed objective evaluations.
- Raw simulator trajectories remain outside Git at `D:/Projects/ChemWorld-local-research/20261016-abductive-completion/physics-attempt-01/` and `physics-attempt-02/`.

Entry points use the locked environment: `uv run --no-sync python -m scripts.qualify_abductive_worlds`, `scripts.calibrate_abductive_references`, `scripts.refit_abductive_null`, and `scripts.check_abductive_physical_means`, each with a fresh output path. All six Python files pass Ruff; six focused scientific-contract tests pass. No participant/provider call was made by this physical qualification executor.
