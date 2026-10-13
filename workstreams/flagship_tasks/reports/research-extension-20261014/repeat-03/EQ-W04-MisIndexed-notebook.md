# repeat-03 / EQ-W04-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T18:10:46.553413+00:00; available public operations: 0; reviewed through: None.

# Source-stage hypothesis notebook

## H1 [tentative]
Within this bounded aqueous weak-acid slice, pH and acid dissociation should be governed primarily by total loading divided by liquid volume. At fixed loading, dilution should slightly increase both pH and dissociation fraction; the archival local prediction at 0.001 mol from 0.018 to 0.054 L is Δ(pH/14)=+0.00256 and Δdissociation=+0.00581 (80% effective pKa interval 4.789–4.889).

## H2 [tentative]
The precipitation proxy may exhibit a bounded concentration/loading threshold rather than the smooth weak-acid dilution relation. A 4×3 water-only grid (0.001, 0.004, 0.012, 0.030 mol; 0.018, 0.036, 0.054 L) will separate loading from volume through repeated concentrations and span 0.0185–1.67 mol/L. Each batch will have a pre-termination pH-meter observation and a final assay at the same composition, allowing instrument/readout agreement to be assessed without claiming that the pair is independent replication.

Predictions made before experiments: pH_normalized and dissociation will be higher at lower concentration; equal concentration made from different loading/volume combinations should be similar if concentration alone is sufficient. A precipitation threshold would appear as a nonlinear rise at high concentration; systematic differences at equal concentration would reject a concentration-only account.

## Revision 2

Recorded: 2026-10-13T18:12:05.432097+00:00; available public operations: 30; reviewed through: runner-operation-0030.

# Source-stage hypothesis notebook

## H1 [rejected at the archival anchor]
The supplied local dilution direction is not reproduced by the lower-noise final assays. At 0.001 mol, changing 0.018→0.054 L gave pH_normalized 0.29252→0.29182 and dissociation 0.07944→0.07440 (events runner-operation-0005 and -0015), whereas the archival fit predicted increases of +0.00256 and +0.00581. These observed changes are opposite in sign, though small; therefore the specific archival local relationship is rejected for this campaign rather than generalized. The pH-meter readings disagree variably with final assays, so they are secondary evidence rather than interchangeable replicates.

## H2 [unresolved; revised]
Across final assays through 0.004 mol, pH and dissociation vary only modestly and not monotonically with dilution (events runner-operation-0005 through -0030). This weakens a simple concentration-only weak-acid description. The remaining higher-load grid will test whether total loading independently shifts responses and whether equal-concentration pairs agree.

## H3 [tentative]
The precipitation proxy is approximately flat near 0.15 over the measured low-loading domain rather than showing an evident threshold. A threshold remains possible only at higher loading/concentration. Final-assay precipitation values span roughly 0.150–0.163 through six batches; pH-meter differences are compatible with its larger stated noise and do not establish an effect.

Decision: retain the preregistered 4×3 grid. A sharp rise at 0.012 or 0.030 mol would revive the threshold hypothesis; otherwise report a flat bounded proxy over the tested water-only scope.

## Revision 3

Recorded: 2026-10-13T18:13:49.611442+00:00; available public operations: 60; reviewed through: runner-operation-0060.

# Source-stage hypothesis notebook

## H1 [partly supported only as an effective trend; archival anchor not reproduced]
The exact archival 0.001 mol dilution claim was not reproduced by final assays: 0.018→0.054 L changed pH_normalized 0.29252→0.29182 and dissociation 0.07944→0.07440 (runner-operation-0005, -0015), opposite the predicted +0.00256 and +0.00581. However, dissociation increased across the same dilution at each higher loading: +0.00513 (0.004 mol; -0020 to -0030), +0.00737 (0.012 mol; -0035 to -0045), and +0.00905 (0.030 mol; -0050 to -0060). Thus dilution-enhanced dissociation is supported qualitatively in the 0.004–0.030 mol scope, but the supplied local magnitude and effective-pKa interval are not validated at their stated anchor.

A descriptive final-assay fit y = a + b_n ln(n/mol) + b_V ln(V/L) gave dissociation b_n=-0.00259 and b_V=+0.00386. Opposite signs are broadly compatible with a concentration effect, but unequal magnitudes leave total-loading/volume effects, model misspecification, and measurement scatter equivalent explanations. The one exact equal-concentration comparison (0.004/0.018 vs 0.012/0.054 = 0.222 mol/L; runner-operation-0020 vs -0045) differs by 0.00348 in pH_normalized and 0.00882 in dissociation; without independent repeats this numerical difference is not firm evidence of a separate loading effect.

## H2 [unresolved for pH]
Final pH_normalized occupied a narrow 0.28713–0.29451 band across 0.0185–1.67 mol/L. Dilution directions were mixed across loadings. A descriptive two-factor log fit gave b_n≈-0.000022 and b_V≈-0.000895, too small and structurally inconsistent with a simple concentration-only law to treat as identified. Since final-assay noise is stated as 0.002 per observation and batches lack independent condition replicates, the data support only a weak/flat pH response over this grid, not a precise law.

## H3 [supported in tested scope]
The final-assay precipitation proxy stayed in 0.14828–0.16277 across all 12 water-only conditions, with no high-loading threshold (runner-operation-0005 through -0060). Its descriptive log coefficients are small (b_n=-0.000326, b_V=+0.00163). A genuinely flat response, a proxy baseline/floor, and a threshold outside the tested domain remain equivalent explanations; only the absence of a resolved transition inside this domain is supported.

## Measurement qualification
Pre-termination pH-meter and final-assay observations were at nominally the same composition but are not independent batch replicates. Mean meter-minus-final differences were +0.00199 for pH_normalized and +0.00670 for dissociation, with variable signs/magnitudes across conditions (e.g. runner-operation-0003 vs -0005). Interpret final assays as primary because their declared channel noise is lower. Equilibrium residual/confidence are environment diagnostics and were not optimized or used as scientific confidence.

## Scope and next test
Claims apply only to anonymous reagent in water near 298 K, 0.001–0.030 mol total loading and 0.018–0.054 L. Independent repeated batches at the archival anchor and at matched concentrations would distinguish noise from total-loading effects. Extending concentration beyond 1.67 mol/L, if legal in a future campaign, would test whether precipitation is truly flat or merely below threshold.
