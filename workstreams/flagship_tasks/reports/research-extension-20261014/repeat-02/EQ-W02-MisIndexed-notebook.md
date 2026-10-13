# repeat-02 / EQ-W02-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T17:34:09.300258+00:00; available public operations: 0; reviewed through: None.

# Hypothesis notebook

## H1 [tentative; pre-experiment]
Within aqueous batches near 298 K, pH and acid dissociation should primarily track analytical loading concentration (reagent mol / liquid L), with dilution increasing both pH and dissociation fraction slightly. The archival local prediction at 0.001 mol, 0.018→0.054 L is ΔpH_normalized ≈ +0.001275 and Δdissociation ≈ +0.002776 (effective pKa 5.15–5.25).

## H2 [tentative; pre-experiment]
The precipitation proxy may increase with concentration and show a threshold or saturation, so equal concentration produced by different amount/volume pairs should help distinguish concentration control from independent total-amount or volume effects.

## Design commitments
Use water only, near ambient conditions, and span a factorial-like set of loadings and volumes with repeats. One pre-terminal pH-meter reading per batch will compare lower-precision intermediate values with the final assay; final interpretation will emphasize final assays and repeatability. A direct archival-anchor dilution pair and exact repeats will test the local claim and noise scale.

## Revision 2

Recorded: 2026-10-13T17:35:29.411128+00:00; available public operations: 30; reviewed through: runner-operation-0030.

# Hypothesis notebook

## H1 [not supported for anonymous reagent loading; scope narrowed]
For water-only ambient batches, varying anonymous reagent concentration from 0.0185 to 0.556 mol/L produced final pH_normalized, dissociation, and precipitation values that remained in overlapping narrow bands rather than showing a clear monotonic loading response (events runner-operation-0005 through -0030). The archival 0.001 mol, 0.018→0.054 L dilution direction was not reproducible across the two pairs: final pH differences changed sign and were comparable to between-repeat variation (events -0005/-0010 and -0015/-0020). Thus the supplied local relationship is not supported when “acid_total” is mapped to add_reagent.

## H2 [unresolved]
Equal-concentration but different amount/volume batches (0.001/0.018 versus 0.003/0.054; events -0005/-0015 versus -0025) do not show a resolved systematic difference. This is consistent with either a nearly flat response or measurements dominated by run variation; it does not establish concentration control.

## H3 [pre-experiment pivot]
A plausible mis-indexing alternative is that add_component index 0, rather than add_reagent, controls the acid/precipitation slice. Remaining batches will use a crossed component-loading × volume series (0.001, 0.010, 0.020 mol at 0.018 and 0.054 L). A monotonic response with component concentration would support this mapping; continued flatness would favor a bounded response insensitive to both accessible loadings in this scope.

## Measurement caveat
Single pH-meter values sometimes differ materially from the corresponding final assay, while final-assay repeats also vary. Conclusions therefore require trends larger than these observed run-to-run differences; no post-hoc numerical significance threshold is imposed.

## Revision 3

Recorded: 2026-10-13T17:36:26.348740+00:00; available public operations: 60; reviewed through: runner-operation-0060.

# Hypothesis notebook

## H1 [weakly supported only as a local average; not established globally]
At the archival anchor (0.001 mol anonymous reagent), averaging duplicate final assays gives the 0.018→0.054 L changes ΔpH_normalized = +0.000724 and Δdissociation = +0.003979 (events runner-operation-0005/-0010/-0015/-0020). These have the archival directions and the dissociation magnitude is similar to the prior (+0.002776), but individual paired differences reverse sign and the pH mean change is smaller than the prior (+0.001275). Treat this as consistency, not a precise validation.

Across the broader reagent-loading series (0.0185–0.556 mol/L; events -0005 through -0030), an exploratory linear fit of pH_normalized versus ln(concentration) has slope about -0.00075 per natural-log unit. This is small relative to replicate scatter and does not support extrapolating the local archival relation.

## H2 [unresolved / effectively flat over studied scope]
Final precipitation stayed near 0.15–0.17 throughout reagent-loading experiments and did not show a resolved threshold. At the duplicated archival dilution anchor, mean precipitation changed by -0.0126, but duplicate variability and the absence of a monotonic broader trend prevent attributing this to dilution.

## H3 [mis-indexing alternative not supported]
The crossed add_component index-0 series spanning 0.0185–1.11 mol/L (events runner-operation-0035 through -0060) also remained nearly flat: final pH_normalized 0.2651–0.2699, dissociation 0.0639–0.0833, precipitation 0.1462–0.1593. Its exploratory pH slope versus ln(concentration), about -0.00077, is essentially the same small slope as for reagent. Thus neither accessible amount index yields a clearly identifiable global loading law in this bounded ambient-water slice.

## Identifiability and scope
The data support a stable response plateau near pH_normalized ≈0.266–0.270 (pH ≈3.72–3.78), dissociation ≈0.07–0.08, and precipitation proxy ≈0.15 more strongly than any loading dependence. Equivalent explanations remain: genuinely buffered/plateau behavior, a latent total-acid quantity not aligned with the two public addition indices, or effects smaller than batch/instrument variation. Temperature, non-water solvents, catalysts/electrolyte profiles, and equilibration time were not varied, so no claims extend there. A decisive follow-up would use more replicate anchor pairs or staged within-vessel dilution to reduce between-batch variation, and independently verify which public addition maps to acid_total.
