# repeat-01 / EQ-W05-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T17:09:27.254200+00:00; available public operations: 0; reviewed through: None.

# Source-stage hypothesis notebook

## H1 [tentative; pre-experiment]
Within the archival scope, treating `add_reagent` loading divided by aqueous volume as an effective monoprotic-acid concentration should predict lower pH at higher concentration and a modest rise in dissociation on dilution. For 0.001 mol at 298 K, dilution from 0.018 to 0.054 L is predicted *before testing* to increase acid_dissociation_fraction by about 0.0082 and pH_normalized by about 0.0035; the effective pKa prior is 4.61–4.71.

## H2 [unresolved; pre-experiment]
The bounded precipitation proxy may depend on concentration/loading beyond the acid equilibrium alone. A concentration series plus matched-loading dilution pairs should distinguish a mostly concentration-controlled response from a total-moles effect, but anonymous formulation and proxy saturation may leave equivalent explanations.

Decision rule: use paired staged dilution and replicated concentration points; revise H1 if observed direction or magnitude is inconsistent beyond visible instrument variation. Do not treat equilibrium_confidence as scientific confidence.

## Revision 2

Recorded: 2026-10-13T17:10:51.451358+00:00; available public operations: 54; reviewed through: runner-operation-0054.

# Source-stage hypothesis notebook

## H1 [rejected as mapped to `add_reagent`]
Pre-experiment I mapped anonymous limiting reagent loading/volume to the archival effective acid. Across final assays spanning 0.001–0.018 mol and 0.018–0.054 L, pH_normalized (~0.300–0.309), dissociation (~0.066–0.076), and precipitation proxy (~0.143–0.161) remained nearly flat, including nominal concentration changes up to roughly 1 mol/L (events runner-operation-0006, -0012, -0018, -0024, -0030, -0036, -0042, -0048, -0054). Numerical scatter is present, but the predicted systematic acid-concentration response is absent. Thus the archival acid coordinate is probably not `add_reagent`, or the response is strongly buffered/clipped in this slice.

## H2 [unresolved]
The `add_component` control may be the effective acid-total coordinate despite the anonymous label. Remaining batches will test component 0 at the archival paired volumes and a higher loading. If it yields the predicted dilution direction, this supports a control-index mapping rather than a universal chemistry identity claim.

## H3 [supported only for reagent-only scope]
For water plus `add_reagent` over tested endpoints, precipitation_signal is approximately a baseline near 0.15 without an obvious monotone loading or concentration dependence. Final-assay noise is declared ~0.006, so some point differences are numerical but do not establish a loading effect without repeatable structure. Equivalent explanations include a spectator reagent, hidden buffer domination, or output clipping.

Do not interpret equilibrium_confidence as evidentiary confidence.

## Revision 3

Recorded: 2026-10-13T17:11:43.423756+00:00; available public operations: 72; reviewed through: runner-operation-0072.

# Source-stage hypothesis notebook

## H1 [partly supported locally; rejected as a broad loading law]
At the archival 0.001 mol endpoints, independent final assays at 0.054 L gave pH_normalized 0.3036 and 0.3093 and dissociation 0.0666 and 0.0755 (runner-operation-0006, -0012); the 0.018 L endpoint gave 0.3042 and 0.0669 (-0018). Averaging the two dilute endpoints gives an apparent dilution change of about +0.0022 in pH_normalized and +0.0042 in dissociation relative to 0.018 L: correct archival direction, but smaller than the prior (+0.0035, +0.0082) and poorly resolved with only one concentrated replicate and declared assay noise.

Across reagent endpoints spanning nominal 0.0185–1 mol/L, mean final pH_normalized was 0.3047, mean dissociation 0.0716, and mean precipitation proxy 0.1535 (events -0006 through -0054). A simple least-squares pH slope versus ln(n/V) was only -0.00056 normalized units per ln-unit, much weaker than extrapolating the local archival relation. Therefore the prior is at most local and cannot be used as a broad concentration law here.

## H2 [unresolved total-moles effect]
Matched nominal concentrations do not cleanly separate total loading from volume: at ~0.0556 mol/L, 0.001/0.018 versus 0.003/0.054 L differed by +0.00137 pH_normalized and +0.00863 dissociation (-0018, -0024), while the ~0.1667 mol/L pair showed differences in another direction (-0030, -0036). With single observations and assay noise, these are numerical differences, not a repeatable total-moles effect.

## H3 [supported as a bounded null/near-null response]
For water plus anonymous reagent in the tested range, precipitation_signal stayed near a baseline (~0.15) with no repeatable monotone dependence on nominal loading or concentration. Component-0 substitution at 0.001 mol/0.018 L, 0.001/0.054 L, and 0.009/0.018 L likewise produced final pH, dissociation, and precipitation values in the same band (runner-operation-0060, -0066, -0072), opposing the proposed control-index remapping.

## Scope and alternatives
Identifiable evidence supports a buffered/saturated near-constant response with, at most, a small local dilution effect around 0.001 mol. Equivalent explanations remain: hidden background buffer, an effective acid inventory not controlled one-for-one by either public loading operation, or bounded proxy compression/mis-indexing. The data do not identify a unique pKa from broad loading response, so the archival 4.61–4.71 interval is not independently established. Temperature was ambient water throughout; no solvent-identity or temperature generalization is warranted. Equilibrium_confidence was treated only as an environment diagnostic.

A decisive follow-up would replicate both 0.001 mol endpoints with the same high-precision assay and include blank-water controls; a repeatable dilute-minus-concentrated change near the archival values would strengthen the local relation, while a change near zero would reject it.
