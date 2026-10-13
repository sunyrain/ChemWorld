# repeat-01 / EQ-W05-Aligned — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T11:32:46.855958+00:00; available public operations: 0; reviewed through: None.

# Hypothesis notebook

## H1 [tentative; prediction before experiments]
Within the bounded aqueous slice, increasing total acid concentration (loading/volume) should lower pH and may increase the precipitation proxy; dilution at fixed acid moles should slightly increase both pH and dissociation fraction. At the archival anchor (0.001 mol, 0.018→0.054 L, near 298 K), predicted changes are ΔpH_normalized ≈ +0.000876 and Δdissociation ≈ +0.001885; these are small relative to single-measurement noise, so paired final assays and broader concentration contrasts will be more informative than treating one pair as decisive.

## H2 [unresolved; prediction before experiments]
A monoprotic weak-acid effective model with pKa near 5.33–5.43 may describe pH/dissociation locally, but precipitation could create loading-dependent departures. I will span concentration and use some equal-concentration pairs to separate total-mole from concentration/volume effects. Evidence inconsistent with concentration collapse will favor an independent total-loading or precipitation coupling.

## Revision 2

Recorded: 2026-10-13T11:33:29.777458+00:00; available public operations: 30; reviewed through: runner-operation-0030.

# Hypothesis notebook

## H1 [tentative; archival dilution effect not yet resolved]
The anchor pair (0.001 mol, nominal 0.018 vs 0.054 L) moved final-assay pH_normalized from 0.30261 to 0.30574 and dissociation from 0.06987 to 0.08214 (runner-operation-0005, runner-operation-0010), directions consistent with the archival prediction but magnitudes are only modest relative to assay noise and the pH difference exceeds the archival local estimate. Treat as suggestive, not confirmation; repeatability is absent.

## H2 [unresolved; simple concentration-only model under strain]
Across the first six final assays, pH stays near 0.30 and dissociation near 0.06–0.08 despite concentration changes. Equal nominal concentration 0.1667 mol/L at 0.005/0.03 and 0.01/0.06 gives numerical differences in dissociation and precipitation (runner-operation-0015, runner-operation-0030), but neither is replicated enough to establish a total-loading effect. Remaining batches will include three nominal 0.5 mol/L conditions at different total moles/volumes, providing a stronger collapse test.

## H3 [tentative]
Precipitation_signal is roughly 0.14–0.16 in final assays so far, without an obvious monotone dependence on concentration. A high-loading series can distinguish a threshold/upturn from a near-constant baseline; lack of a systematic trend would shelve the monotone precipitation claim within this design.

## Revision 3

Recorded: 2026-10-13T11:34:58.803915+00:00; available public operations: 60; reviewed through: runner-operation-0060.

# Hypothesis notebook

## H1 [supported only as a weak local tendency]
At 0.001 mol, dilution from nominal 0.018 to 0.054 L increased final pH_normalized by 0.00313 and dissociation fraction by 0.01227 (runner-operation-0005, runner-operation-0010), matching the archival directions. With final-assay standard deviations 0.002 and 0.006 per measurement, this single pair is not decisive and does not precisely validate the much smaller archival deltas. The archival local relationship remains plausible but should not be treated as calibrated by this campaign.

## H2 [supported in scope: approximately constant effective acidity; detailed loading law unresolved]
Across 12 water batches spanning 0.001–0.04 mol and nominal 0.018–0.08 L, final pH_normalized remained about 0.301–0.307 and dissociation about 0.064–0.082 (runner-operation-0005 through runner-operation-0060). A descriptive fit using intercept, ln(total concentration), and total moles gave small coefficients for pH_normalized (−0.00055 per ln concentration; +0.063 per mol) and dissociation (−0.0071 per ln concentration; +0.40 per mol), but the design is correlated and unreplicated, so these are summaries rather than identified causal terms. Three nominal 0.5 mol/L batches at 0.02/0.04, 0.03/0.06, and 0.04/0.08 produced similar endpoints (runner-operation-0035, -0045, -0060), supporting approximate concentration collapse and arguing against a large independent total-mole effect in this slice.

Using pKa_eff = pH − log10(alpha/(1−alpha)) as an effective representation, the 12 final assays average about 5.36 with individual values about 5.28–5.45. This is consistent with the archival 5.329–5.429 interval at the aggregate level, while individual spread and sensor noise preclude a universal constant claim. An equivalent explanation is a buffered/regulated response that merely mimics a monoprotic Henderson–Hasselbalch relation; composition channels cannot distinguish these mechanisms.

## H3 [shelved: monotone precipitation dependence]
Final precipitation_signal stayed roughly 0.139–0.158 with no systematic upturn across the loading range (runner-operation-0005 through runner-operation-0060). A descriptive linear fit versus concentration and total moles had small, opposing coefficients (−0.0147 per mol/L; +0.202 per mol), not an identified law. Thus a monotone concentration or total-loading effect is unsupported here; a near-constant baseline, weak competing effects, or a threshold outside the tested domain remain equivalent explanations.

## Scope and uncertainty
Claims apply only to anonymous reagent in water near 298 K, immediate equilibration, and the tested loading/volume bounds. Each recipe has one final assay; paired ph-meter readings add a noisier contemporaneous check but not true batch replication. The strongest future discriminators are replicate anchor dilutions and orthogonal designs varying volume and moles independently near fixed concentration. Equilibrium diagnostics were recorded but were not used as confidence in these scientific claims.
