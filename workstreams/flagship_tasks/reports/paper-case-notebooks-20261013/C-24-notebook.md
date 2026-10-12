# C-24 — model-authored source notebook

Development replication. Each version is the model's scientific account, not verified environment truth. Posttest answers are separate in the JSON record.

## Revision 1

Recorded: 2026-10-12T17:59:13.622534+00:00; public operations available: 0; reviewed through: not specified.

# Hypothesis notebook

## H1 [tentative]
Solvent S2 should favor crystal recovery and growth with fewer fines/less occlusion than S0, while catalyst C1 or C3 may give strong upstream target formation. Prediction: a concentrated charge in S2, adequate hot reaction time, modest seeding, slow cooling and a cold hold will meet purity/fines constraints and exceed 0.10 crystal recovery. Faster cooling or excessive seed should increase fines; insufficient cold hold should reduce recovery.

## Initial design decision
Screen catalyst/solvent combinations and thermal histories first, then replicate/refine the best feasible region. Evidence from final assays is authoritative; particle-size checks will diagnose selected batches. I will revise if observed rankings contradict the dossier.

---

## Revision 2

Recorded: 2026-10-12T18:01:00.691697+00:00; public operations available: 90; reviewed through: runner-operation-0090.

# Hypothesis notebook

## H1 [supported in screened scope]
Solvent S2 is the only screened neat solvent that simultaneously gives high purity and fines below 0.50 under slow cooling to 250 K. Final assays: batches 2–4 (events runner-operation-0024, -0035, -0046) gave crystal recovery about 0.42–0.47 with fines about 0.35–0.40 and purity about 0.98–1.00. S0/S1 had numerically higher recovery in some cases but failed the fines constraint (events -0057, -0079); S3 also failed (-0068). This supports the dossier's growth/nucleation ordering for the tested recipe, though solvent and catalyst are confounded across some comparisons.

## H2 [tentative]
Within S2 at 390 K reaction conditions, catalyst C0 is currently best among the four catalysts for constrained recovery (batch 2, event runner-operation-0024), but single measurements and process noise leave the size of the catalyst effect unresolved.

## H3 [tentative]
Colder and longer cooling improved recovery and reduced fines relative to the 275 K baseline (batch 1 event runner-operation-0013 versus batch 2), but catalyst changed simultaneously. Prediction: in S2/C0, longer cold aging, low seed dose, and seeding nearer the supersaturation region will raise recovery or reduce fines. I will test seed dose/timing, cold hold, concentration, cooling rate, and one redissolution/recooling history; a failure to reproduce batch 2 would weaken H2/H3.

---

## Revision 3

Recorded: 2026-10-12T18:02:18.991254+00:00; public operations available: 181; reviewed through: runner-operation-0181.

# Hypothesis notebook

## H1 [supported in screened scope]
S2 robustly satisfies purity and fines constraints under a 14,400 s cool to 250 K. Across batches 2, 9–13, and 15, final recovery is roughly 0.47–0.49 with fines roughly 0.34–0.40 and purity above 0.97 (events runner-operation-0024, -0100, -0111, -0122, -0134, -0146, -0168). S0/S1/S3 neat-solvent screens had higher fines; this is not a claim outside tested histories.

## H2 [unresolved]
C0 remains the best screened S2 catalyst recipe, but seed-dose effects from zero to 0.05 g are smaller than run-to-run/instrument variation in batches 9–11 (events -0100, -0111, -0122). Do not claim a seed optimum.

## H3 [supported for rate; unresolved for hold]
Fast cooling causes excessive fines: batch 14 (event -0157) had fines about 0.84 versus about 0.35 for slow-cool neighbors. A single 14,400 s cold hold in batch 12 gave larger measured size but essentially unchanged recovery/fines versus nearby slow-cool runs (event -0134); one comparison is insufficient for a hold effect. Redissolution/recooling worsened fines (batch 16, event -0181) under the tested history.

## H4 [testable boundary hypothesis]
S1 offers somewhat higher recovery but narrowly misses the fines constraint in the initial screen. Prediction before batches 17–23: long cold aging or blending S1 with S2 may move fines below 0.50 while retaining recovery above the S2 plateau. Replicate S2/no-seed to assess robustness. The final batch will confirm the best feasible recipe.

---

## Revision 4

Recorded: 2026-10-12T18:03:10.728116+00:00; public operations available: 264; reviewed through: runner-operation-0264.

# Hypothesis notebook

## H1 [revised; supported in tested scope]
S2 is a robust low-fines baseline, but S1 can meet the fines constraint when slow cooling is followed by cold aging. Batch 17 (event runner-operation-0192: one 14,400 s hold) achieved recovery about 0.56, purity about 1.00, fines about 0.45. Batch 23 (event -0264: three holds) also met constraints with recovery about 0.55 and fines about 0.45. The earlier unaged S1 batch 5 failed on fines (event -0057). This numerical pattern supports an aging benefit for S1, although batch-to-batch variation and changed seed protocol are confounds.

## H2 [unresolved]
Seed dose has no resolved recovery benefit. In aged S1, no-seed batch 17 numerically exceeded 0.05 g seed batch 18 (event runner-operation-0204), while both were near the fines boundary. Prefer no purchased seed because seed-excluded recovery is the objective and the simpler protocol performed best.

## H3 [supported]
Slow cooling is essential in this tested family; fast cooling and redissolution/recooling produced excessive fines (events runner-operation-0157 and -0181). S1/S2 blends interpolate behavior but did not beat aged neat S1 (events -0216, -0228).

## Final pre-confirmation prediction
An exact no-seed S1/C0 replicate with 390 K reaction, slow cool to 250 K, and one 14,400 s cold hold should again satisfy purity >=0.80 and fines <=0.50, with crystal recovery near the observed 0.55 region. If it fails the fines constraint, recommend completed batch 17 rather than extrapolating.

---

## Revision 5

Recorded: 2026-10-12T18:03:31.085184+00:00; public operations available: 274; reviewed through: runner-operation-0274.

# Hypothesis notebook

## H1 [supported, boundary-sensitive]
Aged S1 can improve constrained crystal recovery beyond the robust S2 baseline, but fines sit near the 0.50 specification. Batch 17 (event runner-operation-0192) remains the best observed feasible result: crystal yield 0.563, purity 0.997, fines 0.454. Batch 18 also narrowly met the constraint (event -0204: yield 0.552, fines 0.497), and batch 23 met it (event -0264: yield 0.548, fines 0.448). Exact-process confirmation batch 24 had yield 0.542 and purity 1.00 but fines 0.514 (event -0274), so reproducibility at the fines boundary is unresolved and the numerical yield differences should not be overstated.

## H2 [supported baseline]
S2/C0, no or low seed, 14,400 s cooling to 250 K is a more robust low-fines region (multiple events including runner-operation-0100, -0111, -0238), with lower recovery near 0.49. It is the fallback when fines robustness matters more than maximum observed recovery.

## H3 [decision]
Recommend completed batch 17 because it has the highest observed crystal recovery among batches satisfying both explicit quality constraints. Its process used S1 (0.08 L), reagent 0.04 mol, C0 0.005 mol, 390 K for 3600 s at 500 rpm, quench, no seed, cooling to 250 K over 14,400 s, a 14,400 s hold at 300 rpm, then filtration. Condition that would change this choice: if repeatability/guard-band assurance were required, prefer the lower-yield S2 baseline because batch 24 shows aged S1 may cross the fines limit.

---
