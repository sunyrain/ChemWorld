# Opaque crystallization pilot

Status: completed; failure: None
Original status: completed; retest repair present: False.

## Source batches

| Batch | Recovery | Purity | Size index | Fines |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 0.5096708536148071 | 1.0 | 0.06457862257957458 | 0.9892784357070923 |
| 2 | 0.30216771364212036 | 0.9607062339782715 | 0.0519833043217659 | 1.0 |
| 3 | 0.5019103288650513 | 0.9880661368370056 | 0.05868357792496681 | 1.0 |
| 4 | 0.4959200918674469 | 0.9716396927833557 | 0.042508065700531006 | 1.0 |
| 5 | 0.47750213742256165 | 0.9699636697769165 | 0.05309396609663963 | 0.9845878481864929 |
| 6 | 0.3489699959754944 | 0.9662621021270752 | 0.10139551758766174 | 1.0 |
| 7 | 0.41980835795402527 | 0.9862805008888245 | 0.04644249752163887 | 0.9825443625450134 |
| 8 | 0.5162596106529236 | 0.997520923614502 | 0.07002910226583481 | 0.9975425601005554 |
| 9 | 0.40026170015335083 | 0.9669342637062073 | 0.03297305107116699 | 0.9725327491760254 |
| 10 | 0.43194425106048584 | 0.9909398555755615 | 0.04737825691699982 | 0.8869724869728088 |
| 11 | 0.0 | 0.9865140914916992 | 0.39282339811325073 | 8.601322042522952e-05 |
| 12 | 0.008356365375220776 | 1.0 | 0.424535870552063 | 0.0 |

## K1

Mechanistic account

The materials are anonymous benchmark identities, so the conclusions are phenomenological rather than claims about real molecular structures.

Observations

At the full charge (0.040 mol reagent in 0.080 L solvent), reaction conversion was generally high, but crystal recovery and particle quality separated sharply. Batch 1 (S0/C0, 360 K reaction) gave conversion 1.00, reaction yield 0.616, crystal yield 0.510, and purity 1.00, but its fines fraction was 0.989. Thus reaction formation and crystal purity were not the main limitations; almost all particles were below 20 µm.

Changing process history alone did not resolve this. Batch 3 used S0/C0 with more seed, extended aging, and a thermal cycle; it retained crystal yield 0.502 and purity 0.988 but had fines 1.00. Batch 4 omitted seed and used prolonged staged cooling/aging, yet gave yield 0.496 and fines 1.00. Batch 9 held near 300 K for ten long aging periods rather than cooling deeply; recovery fell to 0.400 while fines remained 0.973. These results show strong history dependence but no evidence that simple extra residence time, seed omission, or the tested thermal cycle can coarsen the full-load population enough to satisfy the fines limit.

Material effects were meaningful but did not overcome the concentration effect. In comparable full-load runs, S2/C0 in batch 5 gave reaction selectivity 0.539 and crystal yield 0.478, whereas S3/C0 in batch 6 gave selectivity 0.459 and crystal yield 0.349. Batch 6 reported a larger normalized size channel (0.101), but fines remained clipped at 1.00. Near the 20 µm threshold, independently noisy size and fines channels can appear inconsistent, so that isolated size value should not be treated as proof of compliance. Catalyst comparison under the same S0 crystallization schedule was clearer: C3 in batch 8 outperformed C2 in batch 7 in selectivity (0.622 versus 0.512) and crystal yield (0.516 versus 0.420), although both remained fines-dominated (0.998 and 0.983). Batch 2, using S1/C1, was poorer still, with selectivity 0.373 and crystal yield 0.302, but solvent and catalyst effects are confounded in that batch.

Dilution caused the decisive change. Batch 10 halved the reagent charge to 0.020 mol while retaining 0.080 L S0 and used a small seed dose. It gave reaction selectivity 0.736, crystal yield 0.432, purity 0.991, and fines 0.887. This was a substantial fines improvement, although still outside specification. At 0.010 mol reagent in batch 11, with catalyst scaled proportionally, the final crystals were very large by the assay channels (normalized size 0.393, approximately 98 µm d50) and fines were essentially zero, but seed-excluded crystal yield was zero. The observed solids were therefore consistent with retained or grown seed rather than meaningful recovery of newly formed product. Batch 12 used 0.005 mol reagent, proportionally scaled catalyst, a 0.0005 g seed charge, and a slightly colder final crystallization temperature of 285 K. It produced purity 1.00, fines 0.00, normalized size 0.425 (approximately 106 µm d50), and seed-excluded crystal yield 0.00836. Batch 12 was consequently the highest-recovery completed batch satisfying both imposed quality limits, although it remained far below the 0.10 feasibility target.

Interpretation

A useful coupling approximation is

n_crystal,target / n_reagent,0 = Y_crystal ≈ X · S_rxn · f_precip · f_isolation,

where X is conversion, S_rxn is chemical selectivity, f_precip is the fraction of target transferred into crystals, and f_isolation represents filtration retention. For example, batch 1 had X·S_rxn ≈ 0.62, close to its measured reaction yield of 0.616, but only 0.510 appeared as seed-excluded crystals. In batch 11, conversion was 0.928 and reaction yield was 0.611, yet crystal yield was zero: substantial target existed, but the diluted liquor and 290 K endpoint apparently did not drive significant net precipitation. This demonstrates that optimizing the reaction alone is insufficient.

The crystallization trends are consistent with supersaturation control. With σ=(C−C*)/C*, nucleation commonly has a much steeper dependence on supersaturation than growth, schematically

J ≈ J0 exp[−B/(ln(1+σ))²],     G ≈ kg σ^g.

At full loading and deep cooling, high supersaturation would create many nuclei or secondary fines faster than existing particles could grow, explaining the high recoveries but fines fractions near one in batches 1 and 3–9. Dilution lowers σ and can suppress nucleation disproportionately, allowing a small number of seed particles to grow large. The transition was extreme: batch 10 still precipitated considerable product but failed the fines limit, whereas batch 11 crossed into an effectively seed-only regime. Batch 12 recovered only a small amount because its colder endpoint supplied slightly more driving force.

A population-balance representation is also useful:

∂n(L,t)/∂t + ∂[G(L,t)n(L,t)]/∂L = B_nuc δ(L−L0) + aggregation − breakage − loss.

The constrained observable is F20=∫₀²⁰ n(L)dL / ∫₀∞ n(L)dL, while the reported normalized size is approximately min(d50/250 µm,1). Because F20 is number-weighted, even a modest mass of large crystals can coexist with an unacceptable number of fine particles. This explains why good mass recovery did not imply acceptable particle quality.

Crystallization also purified the product strongly. Full-load reaction selectivities were often only 0.46–0.62, yet isolated crystal purities were usually 0.97–1.00. The target evidently had a favorable solid/liquid partition relative to byproducts under the tested conditions. The high purity therefore reflects selective solid formation, not necessarily intrinsically clean reaction chemistry.

Revisions and uncertainty

The experimental strategy was revised from full-load feasibility (batch 1), through seed-dose, aging, thermal-cycle, solvent, and catalyst tests (batches 2–9), to concentration control (batches 10–12). The first revisions established that additional aging and the tested thermal cycles did not cure full-load fines. The later dilution series revealed that supersaturation/loading was the dominant control variable.

The unresolved tradeoff is severe: high recovery at 0.020–0.040 mol charge produced excessive fines, while specification-compliant batches at 0.010 mol or below produced zero or very low seed-excluded recovery. Batch 12 is therefore a constraint-feasible recommendation, not a satisfactory optimization endpoint. Its measured recovery is also close enough to zero that assay noise and run-to-run process variation are important.

Untested alternatives include finely interpolating the charge between 0.010 and 0.020 mol, scaling catalyst proportionally, and mapping final temperatures between 285 and 290 K. That narrow region may permit meaningful precipitation without the nucleation burst seen in batch 10. Seed size distribution, seed addition temperature, gentler endpoint ramps, and controlled dissolution of fines followed by regrowth are also plausible levers, but the tested seed omission and thermal cycle did not establish their benefit. These are hypotheses for future study, not demonstrated mechanisms.

## Q

{
  "predictions": [
    {
      "crystal_fines_fraction": {
        "estimate": 0.94,
        "lower80": 0.78,
        "upper80": 1.0
      },
      "crystal_purity": {
        "estimate": 0.95,
        "lower80": 0.88,
        "upper80": 0.99
      },
      "crystal_size": {
        "estimate": 0.055,
        "lower80": 0.025,
        "upper80": 0.11
      },
      "crystal_yield": {
        "estimate": 0.255,
        "lower80": 0.14,
        "upper80": 0.37
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q01"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.9,
        "lower80": 0.68,
        "upper80": 1.0
      },
      "crystal_purity": {
        "estimate": 0.93,
        "lower80": 0.83,
        "upper80": 0.99
      },
      "crystal_size": {
        "estimate": 0.075,
        "lower80": 0.035,
        "upper80": 0.15
      },
      "crystal_yield": {
        "estimate": 0.21,
        "lower80": 0.09,
        "upper80": 0.34
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q02"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.94,
        "lower80": 0.78,
        "upper80": 1.0
      },
      "crystal_purity": {
        "estimate": 0.95,
        "lower80": 0.88,
        "upper80": 0.99
      },
      "crystal_size": {
        "estimate": 0.055,
        "lower80": 0.025,
        "upper80": 0.11
      },
      "crystal_yield": {
        "estimate": 0.255,
        "lower80": 0.14,
        "upper80": 0.37
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q03"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.98,
        "lower80": 0.88,
        "upper80": 1.0
      },
      "crystal_purity": {
        "estimate": 0.95,
        "lower80": 0.88,
        "upper80": 0.99
      },
      "crystal_size": {
        "estimate": 0.04,
        "lower80": 0.018,
        "upper80": 0.08
      },
      "crystal_yield": {
        "estimate": 0.27,
        "lower80": 0.14,
        "upper80": 0.39
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q04"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.94,
        "lower80": 0.78,
        "upper80": 1.0
      },
      "crystal_purity": {
        "estimate": 0.95,
        "lower80": 0.88,
        "upper80": 0.99
      },
      "crystal_size": {
        "estimate": 0.055,
        "lower80": 0.025,
        "upper80": 0.11
      },
      "crystal_yield": {
        "estimate": 0.255,
        "lower80": 0.14,
        "upper80": 0.37
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q05"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.985,
        "lower80": 0.88,
        "upper80": 1.0
      },
      "crystal_purity": {
        "estimate": 0.95,
        "lower80": 0.87,
        "upper80": 0.99
      },
      "crystal_size": {
        "estimate": 0.038,
        "lower80": 0.015,
        "upper80": 0.078
      },
      "crystal_yield": {
        "estimate": 0.27,
        "lower80": 0.15,
        "upper80": 0.39
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q06"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.96,
        "lower80": 0.82,
        "upper80": 1.0
      },
      "crystal_purity": {
        "estimate": 0.95,
        "lower80": 0.88,
        "upper80": 0.99
      },
      "crystal_size": {
        "estimate": 0.05,
        "lower80": 0.022,
        "upper80": 0.1
      },
      "crystal_yield": {
        "estimate": 0.265,
        "lower80": 0.145,
        "upper80": 0.385
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q07"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.72,
        "lower80": 0.38,
        "upper80": 0.96
      },
      "crystal_purity": {
        "estimate": 0.96,
        "lower80": 0.89,
        "upper80": 1.0
      },
      "crystal_size": {
        "estimate": 0.095,
        "lower80": 0.04,
        "upper80": 0.19
      },
      "crystal_yield": {
        "estimate": 0.23,
        "lower80": 0.1,
        "upper80": 0.36
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q08"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.965,
        "lower80": 0.82,
        "upper80": 1.0
      },
      "crystal_purity": {
        "estimate": 0.95,
        "lower80": 0.87,
        "upper80": 0.99
      },
      "crystal_size": {
        "estimate": 0.045,
        "lower80": 0.02,
        "upper80": 0.09
      },
      "crystal_yield": {
        "estimate": 0.245,
        "lower80": 0.125,
        "upper80": 0.365
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q09"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.96,
        "lower80": 0.82,
        "upper80": 1.0
      },
      "crystal_purity": {
        "estimate": 0.95,
        "lower80": 0.88,
        "upper80": 0.99
      },
      "crystal_size": {
        "estimate": 0.05,
        "lower80": 0.022,
        "upper80": 0.1
      },
      "crystal_yield": {
        "estimate": 0.265,
        "lower80": 0.145,
        "upper80": 0.385
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q10"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.74,
        "lower80": 0.35,
        "upper80": 0.96
      },
      "crystal_purity": {
        "estimate": 0.96,
        "lower80": 0.88,
        "upper80": 1.0
      },
      "crystal_size": {
        "estimate": 0.09,
        "lower80": 0.035,
        "upper80": 0.2
      },
      "crystal_yield": {
        "estimate": 0.18,
        "lower80": 0.05,
        "upper80": 0.31
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q11"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.99,
        "lower80": 0.9,
        "upper80": 1.0
      },
      "crystal_purity": {
        "estimate": 0.95,
        "lower80": 0.87,
        "upper80": 0.99
      },
      "crystal_size": {
        "estimate": 0.035,
        "lower80": 0.015,
        "upper80": 0.072
      },
      "crystal_yield": {
        "estimate": 0.3,
        "lower80": 0.18,
        "upper80": 0.42
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q12"
    }
  ],
  "rationale": "Q01/Q02: solvent S3 is expected to reduce recovery relative to S1 but modestly increase characteristic size; both remain fines-limited. Q03/Q04: the larger seed charge supplies more particles and surface area, giving slightly greater recovery but smaller number-weighted size and more fines. Q05/Q06: staged cooling should moderate the nucleation burst compared with immediately cooling to 278.15 K, so Q05 is coarser and less fines-rich, while Q06 recovers slightly more. Q07/Q08: the 300 K thermal excursion may dissolve preferentially small crystals and permit coarsening on recooling, but prior full-loading thermal cycling did not establish a reliable specification-level benefit; its interval therefore spans the fines threshold. Q09/Q10: another four hours at 278.15 K should add modest deposition and growth, slightly increasing yield and size, without curing the fine population. Q11/Q12: loading is the strongest lever. Lower loading suppresses nucleation and produces coarser particles but risks little seed-excluded precipitation; higher loading raises recovery while driving fines close to unity. All recipes contain seed, so particles are expected even when seed-excluded recovery is low. Purity is predicted to remain high because crystallization previously rejected reaction byproducts effectively. Uncertainty is widest near the sharp loading and thermal-history transition, especially for Q08 and Q11."
}

## K2

1. Status of the main claims

Supported by direct observations:
- Full-loading processes gave useful seed-excluded recovery but unacceptable fines. Batch 1 produced crystal yield 0.510 and purity 1.00, but fines were 0.989. Batches 3–9 likewise had crystal yields of about 0.35–0.52 and fines of 0.973–1.00. This directly supports the stated recovery/particle-quality tradeoff.
- Crystallization delivered high purity despite only moderate reaction selectivity. For example, batch 1 had reaction selectivity 0.619 but crystal purity 1.00; batch 6 had selectivity 0.459 and purity 0.966. Selective incorporation or rejection of impurities is a reasonable interpretation, although the measurements do not directly identify where each impurity went.
- Loading had a much larger apparent effect on particle quality than the tested material changes. Batch 10 at 0.020 mol reagent gave yield 0.432 and fines 0.887; batch 11 at 0.010 mol gave essentially zero seed-excluded yield and fines near zero; batch 12 at 0.005 mol gave yield 0.0084 and fines zero. By contrast, the full-loading solvent/catalyst screen in batches 2 and 5–8 never approached the fines specification.
- The tested full-loading aging, seed, and thermal-history changes did not solve the fines problem. Batch 3 used extensive aging and a thermal cycle, batch 4 omitted seed, and batch 9 aged for a long time near 300 K; all remained strongly fines-dominated.

Contradicted or weakened:
- A simple claim that longer residence or thermal cycling necessarily converts fines into large product crystals is contradicted by batches 3, 4, and 9. Those histories did not produce specification-compliant particles, and batch 9 lost recovery without a corresponding fines solution.
- A claim that material selection alone can solve the quality constraint at full loading is contradicted within the tested set: S1, S2, S3, C2, and C3 variants in batches 2 and 5–8 all failed the fines limit.
- The report treated dilution as the dominant causal variable, but that inference is stronger than the experimental design warrants. Batch 10 also had a different catalyst/reagent ratio from batches 11–12, and batches 10–12 used different cooling endpoints. The loading trend is real; its precise causal attribution is not isolated.

Still untested or interpretive:
- The proposed supersaturation–nucleation mechanism is consistent with the endpoints but was not directly measured. No time-resolved nucleation rate, solubility curve, mother-liquor concentration trajectory, aggregation rate, or breakage rate was obtained.
- The sharp transition between 0.010 and 0.020 mol reagent remains unmapped. It is unknown whether it is a smooth concentration response, a metastable-zone threshold, or partly stochastic.
- The suggestion that batch 12 recovered slightly more than batch 11 because of its colder endpoint is not causally established: reagent loading was also halved.
- Seed size distribution, seed addition temperature, and reproducibility near the apparent threshold remain untested.

2. One additional experiment

I would run 0.010 mol reagent in 0.080 L S0 with 0.00125 mol C0 and 0.001 g seed, reproducing batch 11 upstream. I would measure HPLC immediately before quenching, cool slowly to 290 K and measure particle size, then continue to 285 K and 278 K with particle-size measurements after each hold, followed by filtration and final assay. The intermediate measurements are non-destructive and make this a single batch with a resolved trajectory.

This experiment would distinguish three explanations:
- Insufficient cooling in batch 11: if seed-excluded yield becomes appreciable only after cooling below 290 K while size remains large and fines stay below 0.50, the low batch-11 recovery was mainly an endpoint/solubility problem.
- An unavoidable nucleation threshold: if recovery rises after deeper cooling but fines abruptly rise above 0.50 and size falls, the unresolved tradeoff is caused by crossing a supersaturation threshold.
- Insufficient target formation or an intrinsically seed-only dilute regime: if pre-quench HPLC shows low target formation, or if deep cooling still gives negligible seed-excluded yield while the seeded particles remain large, the limitation is upstream chemistry or insufficient available solute rather than the 290 K endpoint.

A particularly informative result would be moderate yield above 0.10 with fines below 0.50 at 285 K; that would falsify the pessimistic conclusion that the explored recovery/quality tradeoff is unavoidable. Conversely, a fines surge between 290 and 285 K would strongly support the nucleation-threshold interpretation.

3. Least effectively used observation and least reliable prediction

The observation used least effectively was batch 6’s combination of normalized crystal size 0.101 with fines reported as 1.00. I largely dismissed this as independent channel noise near the 20 µm boundary. That was plausible, but incomplete: it could also indicate a broad or bimodal population, clipping, or disagreement between assay summaries. The raw particle-size artifact or a replicate measurement would have been more informative than treating the size channel as merely anomalous.

The least reliable held-out prediction is Q08, the cool–reheat–recool thermal-history case. Its outcome depends on a non-monotonic balance among dissolution of fines, dissolution of product mass, Ostwald ripening, renewed nucleation, and reaction-product solubility. Batch 3 provided only weak negative evidence because it used a different solvent/catalyst/loading regime and a different thermal cycle. I therefore had little matched evidence for the predicted reduction in fines, and even the direction of the yield change is uncertain. Q11 is also uncertain because it lies near the observed loading transition, but Q08 requires the larger mechanistic extrapolation.

## Evaluation and resources

```json
{
  "prediction_evaluation": {
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "covered": 10,
        "mae": 0.08926212238484833,
        "mean_interval_width": 0.25416666666666665,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "covered": 12,
        "mae": 0.03366073505435194,
        "mean_interval_width": 0.1175,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "covered": 12,
        "mae": 0.018935429733862,
        "mean_interval_width": 0.09108333333333334,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "covered": 11,
        "mae": 0.04944285235396321,
        "mean_interval_width": 0.24250000000000002,
        "n": 12,
        "planned": 12
      }
    },
    "pair_correct": 17,
    "pair_n": 24,
    "pairs": [
      {
        "correct": true,
        "metric": "crystal_yield",
        "pair": "solvent"
      },
      {
        "correct": true,
        "metric": "crystal_purity",
        "pair": "solvent"
      },
      {
        "correct": true,
        "metric": "crystal_size",
        "pair": "solvent"
      },
      {
        "correct": true,
        "metric": "crystal_fines_fraction",
        "pair": "solvent"
      },
      {
        "correct": true,
        "metric": "crystal_yield",
        "pair": "seed"
      },
      {
        "correct": true,
        "metric": "crystal_purity",
        "pair": "seed"
      },
      {
        "correct": true,
        "metric": "crystal_size",
        "pair": "seed"
      },
      {
        "correct": false,
        "metric": "crystal_fines_fraction",
        "pair": "seed"
      },
      {
        "correct": true,
        "metric": "crystal_yield",
        "pair": "cooling_history"
      },
      {
        "correct": true,
        "metric": "crystal_purity",
        "pair": "cooling_history"
      },
      {
        "correct": true,
        "metric": "crystal_size",
        "pair": "cooling_history"
      },
      {
        "correct": false,
        "metric": "crystal_fines_fraction",
        "pair": "cooling_history"
      },
      {
        "correct": false,
        "metric": "crystal_yield",
        "pair": "thermal_history"
      },
      {
        "correct": true,
        "metric": "crystal_purity",
        "pair": "thermal_history"
      },
      {
        "correct": false,
        "metric": "crystal_size",
        "pair": "thermal_history"
      },
      {
        "correct": false,
        "metric": "crystal_fines_fraction",
        "pair": "thermal_history"
      },
      {
        "correct": true,
        "metric": "crystal_yield",
        "pair": "continue_growth"
      },
      {
        "correct": true,
        "metric": "crystal_purity",
        "pair": "continue_growth"
      },
      {
        "correct": true,
        "metric": "crystal_size",
        "pair": "continue_growth"
      },
      {
        "correct": true,
        "metric": "crystal_fines_fraction",
        "pair": "continue_growth"
      },
      {
        "correct": false,
        "metric": "crystal_yield",
        "pair": "upstream_loading"
      },
      {
        "correct": true,
        "metric": "crystal_purity",
        "pair": "upstream_loading"
      },
      {
        "correct": false,
        "metric": "crystal_size",
        "pair": "upstream_loading"
      },
      {
        "correct": true,
        "metric": "crystal_fines_fraction",
        "pair": "upstream_loading"
      }
    ],
    "presence_correct": 12,
    "quality_correct": 12,
    "valid": true
  },
  "tokens": {
    "basis": "cumulative thread snapshots differenced in source/K1/Q/K2 order",
    "complete": true,
    "monetary_cost_usd": null,
    "stages": [
      {
        "cached_input": 13687552,
        "input": 13798771,
        "output": 13754,
        "stage": "source",
        "uncached_input": 111219
      },
      {
        "cached_input": 0,
        "input": 65249,
        "output": 3162,
        "stage": "K1",
        "uncached_input": 65249
      },
      {
        "cached_input": 0,
        "input": 72405,
        "output": 3437,
        "stage": "Q",
        "uncached_input": 72405
      },
      {
        "cached_input": 65024,
        "input": 75762,
        "output": 2190,
        "stage": "K2",
        "uncached_input": 10738
      }
    ],
    "total": {
      "cached_input": 13752576,
      "input": 14012187,
      "input_plus_output": 14034730,
      "output": 22543,
      "uncached_input": 259611
    },
    "valid": true
  },
  "elapsed_s": 1880.7339999999967,
  "recommendation": {
    "selected_experiment_index": 12,
    "selection_rationale": "Best constraint-feasible completed batch: crystal purity 1.00 and fines fraction 0.00, with the highest observed seed-excluded crystal yield among feasible batches (0.0084); no batch met the 0.10 feasibility target while satisfying both quality limits."
  }
}
```
