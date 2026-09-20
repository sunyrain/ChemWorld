# MisIndexed crystallization pilot

Status: completed; failure: None
Original status: failed; retest repair present: True.

## Source batches

| Batch | Recovery | Purity | Size index | Fines |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 0.4277282655239105 | 1.0 | 0.06945314258337021 | 0.9892544746398926 |
| 2 | 0.3236852288246155 | 0.9544191360473633 | 0.03921293467283249 | 1.0 |
| 3 | 0.0 | 1.0 | 0.3926112651824951 | 0.009809541516005993 |
| 4 | 0.3681006133556366 | 0.9732241630554199 | 0.019862143322825432 | 1.0 |
| 5 | 0.007350972853600979 | 0.988280177116394 | 0.3904413878917694 | 0.0 |
| 6 | 0.3581167459487915 | 0.9698396325111389 | 0.07305201143026352 | 1.0 |
| 7 | 0.3825238347053528 | 0.9924719929695129 | 0.025036633014678955 | 0.9825161695480347 |
| 8 | 0.28585299849510193 | 0.9893703460693359 | 0.06115390360355377 | 0.9973776936531067 |
| 9 | 0.39261215925216675 | 0.9744181632995605 | 0.015650443732738495 | 0.9724926948547363 |
| 10 | 0.006556279491633177 | 1.0 | 0.3772909939289093 | 0.0 |
| 11 | 0.0 | 0.9865140914916992 | 0.39282339811325073 | 8.601322042522952e-05 |
| 12 | 0.008356365375220776 | 1.0 | 0.424535870552063 | 0.0 |

## K1

Mechanistic account

Observations

The reaction was generally driven to near-complete conversion, so catalyst/temperature mainly affected selectivity rather than conversion. With solvent S2, batch 1 (C1, 360 K) gave conversion 1.000, selectivity 0.534, and reaction yield 0.531. C3 at 345 K was similarly effective: batches 4–12 generally gave reaction yields about 0.537–0.552 and selectivities about 0.522–0.557. Under different thermal conditions, C0 and C2 were poorer: batch 2 gave reaction yield 0.422/selectivity 0.428, while batch 3 gave 0.414/0.388. Because catalyst and temperature were not varied factorially, this supports—but does not prove—that C3 is the best robust catalyst in the tested region.

Solvent S2 supported both strong reaction performance and substantial crystallization recovery. Replacing it with S3 in batch 8 reduced reaction yield to 0.465 and selectivity to 0.472; crystal recovery was 0.286, but fines remained 0.997. Thus S3 did not resolve the particle-quality problem. This is consistent with the nominal dossier: S2 has high relative growth, low nucleation tendency, low impurity occlusion, and lower solubility. The observed fixed-world response nevertheless shows that sufficiently deep supersaturation overwhelms those nominal advantages.

Reaction–crystallization coupling

A useful reaction approximation is

Y_target ≈ X × S_target,

where X is conversion and S_target is target selectivity. Since X was usually near one, improving reaction selectivity directly increased the maximum recoverable target inventory. Seed-excluded crystal recovery can be written

R_x = n(target in recovered crystals, excluding seed) / n(initial reactant),

with R_x bounded approximately by reaction yield. Crystallization also purified strongly: batches with meaningful recovery usually had crystal purity around 0.95–1.00 despite reaction byproduct signals around 0.30–0.37. I interpret this as preferential incorporation of target and rejection of reaction impurities. However, very pure, low-recovery batches can largely represent seed-dominated solids, so purity alone is not evidence of successful product recovery.

The central relationship was a sharp recovery–particle-size tradeoff. In S2, cooling deeply produced substantial recovery but extensive secondary nucleation. Batch 4, cooled to 298 K, recovered 0.368 but had fines fraction 1.000 and normalized size 0.0199, corresponding to a number-weighted d50 of about 5 micrometres. Batch 1, cooled to 285 K, recovered 0.428 but still had fines 0.989 and d50 about 17 micrometres. In contrast, warm endpoints preserved large particles but recovered almost no newly formed product: batch 5 at 302 K gave recovery 0.00735, fines 0, and d50 about 98 micrometres; batch 10 at 301 K gave recovery 0.00656, fines 0, and d50 about 94 micrometres.

This can be rationalized using supersaturation S=C/C*(T). A schematic kinetic model is

J = k_n(S−1)^m,
G = k_g(S−1)^g,

where J is nucleation rate and G is growth rate. If m exceeds g, a small decrease in temperature near the supersaturation threshold causes nucleation to rise much faster than growth. A population balance,

∂n(L,t)/∂t + ∂[G n(L,t)]/∂L = B(t)δ(L−L0),

then explains why the number fraction below 20 micrometres can approach one even when appreciable crystal mass is recovered. The reported fines metric is number-weighted, so a large population of tiny secondary crystals dominates it.

Process-history dependence

Final temperature alone was not sufficient to predict the outcome. Batch 6 first crystallized at 298 K, reheated to 303 K, held, and recooled to 300 K. It retained recovery 0.358 but had fines 1.000 and d50 about 18 micrometres. Batch 7 used a stronger 310 K reheat after the 298 K excursion and still ended with recovery 0.383 and fines 0.983. I infer that the initial deep-cooling event created a large fine-particle population that the reheating steps did not fully dissolve; subsequent cooling then regrew or regenerated that population. This interpretation is more consistent with the results than an equilibrium-only solubility model.

Seeding also depended on supersaturation history. Increasing the seed charge alone did not prevent fines after deep cooling: batch 9 used about 1 g of seed and cooled to 298 K, yet recovered 0.393 with fines 0.972. Conversely, direct operation near 300–301 K with about 2 g of seed preserved a seed-dominated coarse population. Batch 11, held only 1,800 s at 300 K, showed essentially zero seed-excluded recovery, fines 0.000086, and d50 about 98 micrometres. Extending the corresponding hold to 7,200 s in batch 12 raised recovery to 0.00836 while retaining purity 1.000, fines reported as 0, and d50 about 106 micrometres. This suggests an induction/growth period near 300 K, followed by a likely nucleation cliff if supersaturation or residence time is increased too far.

Recommended batch and unresolved tradeoff

The sealed recommendation remains batch 12 because it had the greatest measured seed-excluded recovery among batches satisfying both purity ≥0.80 and fines ≤0.50. Its measured recovery was 0.00836, purity 1.000, fines 0, normalized size 0.4245, and CSD quality 0.9897. It did not reach the 0.10 feasibility target. The campaign therefore found two regimes rather than a fully satisfactory optimum: a high-recovery/fine-particle regime and a coarse, specification-compliant/very-low-recovery regime.

Revisions and uncertainty

The initial approach emphasized deep cooling for recovery, but batches 1–2 revealed severe fines. Warm-endpoint trials then established that coarse seed-dominated solids were possible, while batches 6–7 tested and rejected simple thermal cycling as a sufficient cure for fines formed during an earlier deep-cooling excursion. Larger seed charges in batches 9, 11, and 12 showed that seeding helps only when the process avoids the deep-supersaturation nucleation regime.

These conclusions are uncertain because most conditions were tested once, catalyst comparisons were confounded with temperature and time, and final-assay noise is material relative to the very small compliant recoveries. Reported zeros may also reflect clipping/noise rather than exact physical zeros. Particle-size readings before filtration and final-assay values were broadly consistent in regime classification, but not exact replicates. Untested possibilities include a finely resolved temperature window between 300 and 301 K, gentler continuous ramps, removal immediately after limited growth, alternative agitation histories, or a designed factorial study separating catalyst, temperature, seed surface area, and crystallization residence time. Such approaches might locate an intermediate state with recovery above 0.10 before secondary nucleation dominates, but the completed campaign provides no direct evidence that this window exists.

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
        "estimate": 0.33,
        "lower80": 0.2,
        "upper80": 0.45
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q01"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.91,
        "lower80": 0.7,
        "upper80": 1.0
      },
      "crystal_purity": {
        "estimate": 0.97,
        "lower80": 0.9,
        "upper80": 1.0
      },
      "crystal_size": {
        "estimate": 0.06,
        "lower80": 0.025,
        "upper80": 0.13
      },
      "crystal_yield": {
        "estimate": 0.31,
        "lower80": 0.17,
        "upper80": 0.44
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
        "estimate": 0.33,
        "lower80": 0.2,
        "upper80": 0.45
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q03"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.84,
        "lower80": 0.58,
        "upper80": 0.98
      },
      "crystal_purity": {
        "estimate": 0.95,
        "lower80": 0.88,
        "upper80": 0.99
      },
      "crystal_size": {
        "estimate": 0.075,
        "lower80": 0.035,
        "upper80": 0.15
      },
      "crystal_yield": {
        "estimate": 0.34,
        "lower80": 0.21,
        "upper80": 0.46
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
        "estimate": 0.33,
        "lower80": 0.2,
        "upper80": 0.45
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q05"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.985,
        "lower80": 0.9,
        "upper80": 1.0
      },
      "crystal_purity": {
        "estimate": 0.94,
        "lower80": 0.86,
        "upper80": 0.99
      },
      "crystal_size": {
        "estimate": 0.03,
        "lower80": 0.012,
        "upper80": 0.075
      },
      "crystal_yield": {
        "estimate": 0.35,
        "lower80": 0.22,
        "upper80": 0.47
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q06"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.965,
        "lower80": 0.83,
        "upper80": 1.0
      },
      "crystal_purity": {
        "estimate": 0.95,
        "lower80": 0.88,
        "upper80": 0.99
      },
      "crystal_size": {
        "estimate": 0.045,
        "lower80": 0.018,
        "upper80": 0.095
      },
      "crystal_yield": {
        "estimate": 0.34,
        "lower80": 0.21,
        "upper80": 0.46
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q07"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.94,
        "lower80": 0.7,
        "upper80": 1.0
      },
      "crystal_purity": {
        "estimate": 0.95,
        "lower80": 0.87,
        "upper80": 0.99
      },
      "crystal_size": {
        "estimate": 0.055,
        "lower80": 0.02,
        "upper80": 0.13
      },
      "crystal_yield": {
        "estimate": 0.32,
        "lower80": 0.18,
        "upper80": 0.45
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q08"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.94,
        "lower80": 0.75,
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
        "upper80": 0.115
      },
      "crystal_yield": {
        "estimate": 0.31,
        "lower80": 0.18,
        "upper80": 0.43
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q09"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.965,
        "lower80": 0.83,
        "upper80": 1.0
      },
      "crystal_purity": {
        "estimate": 0.95,
        "lower80": 0.88,
        "upper80": 0.99
      },
      "crystal_size": {
        "estimate": 0.045,
        "lower80": 0.018,
        "upper80": 0.095
      },
      "crystal_yield": {
        "estimate": 0.34,
        "lower80": 0.21,
        "upper80": 0.46
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q10"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.72,
        "lower80": 0.38,
        "upper80": 0.94
      },
      "crystal_purity": {
        "estimate": 0.97,
        "lower80": 0.9,
        "upper80": 1.0
      },
      "crystal_size": {
        "estimate": 0.09,
        "lower80": 0.04,
        "upper80": 0.18
      },
      "crystal_yield": {
        "estimate": 0.24,
        "lower80": 0.1,
        "upper80": 0.38
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q11"
    },
    {
      "crystal_fines_fraction": {
        "estimate": 0.985,
        "lower80": 0.9,
        "upper80": 1.0
      },
      "crystal_purity": {
        "estimate": 0.92,
        "lower80": 0.82,
        "upper80": 0.98
      },
      "crystal_size": {
        "estimate": 0.032,
        "lower80": 0.012,
        "upper80": 0.075
      },
      "crystal_yield": {
        "estimate": 0.36,
        "lower80": 0.22,
        "upper80": 0.49
      },
      "particles_present": true,
      "quality_feasible": false,
      "query_id": "Q12"
    }
  ],
  "rationale": "Identical recipes receive identical predictions: Q01/Q03/Q05 and Q07/Q10. For the solvent pair, S3 is expected to improve impurity rejection and intrinsic growth/nucleation balance relative to S1, but its lower solubility and weaker reaction activity offset this with deeper supersaturation and slightly lower recovery. Increasing seed from 0.006 to 0.05 g should enlarge particles and reduce fines modestly, but prior batches showed that seed loading cannot suppress secondary nucleation under deep cooling. Staged cooling is expected to be less damaging than an immediate 278.15 K excursion, so Q06 has the smallest particles and most fines. Reheating in Q08 may dissolve some fines, but campaign thermal-cycle batches showed strong history persistence and renewed nucleation on recooling. An additional low-temperature growth period raises recovery slightly in Q10 versus Q09 but is more likely to generate secondary fines than to ripen them. Lower upstream loading in Q11 reduces supersaturation, sacrificing recovery while giving the only material chance of approaching the fines limit; higher loading in Q12 does the reverse. All batches are seeded and therefore should contain particles. Purity is likely acceptable throughout, but the estimated fines fractions make every central prediction quality-infeasible. Intervals represent model uncertainty in transferring from the campaign to substantially different charge, catalyst loading, solvent, and thermal conditions, not final-assay measurement noise."
}

## K2

1. Status of the main claims

Supported by direct observations:
- Near-complete conversion made selectivity a major upstream limitation. Batch 1 had conversion 1.000, selectivity 0.534 and reaction yield 0.531; the C3/S2 batches similarly had roughly 0.99–1.00 conversion and reaction yields around 0.54. The interpretation that selectivity controls available target is therefore reasonable, although the approximate relation yield ≈ conversion × selectivity is not exact.
- Crystallization usually rejected impurities effectively. Meaningful-recovery batches 1, 4, 6–9 had crystal purities of about 0.95–1.00 despite appreciable reaction byproduct signals. Preferential target crystallization is an interpretation; the high measured purities themselves are observations.
- A strong recovery–particle-quality tradeoff was directly observed. Batch 4 recovered 0.368 but had fines 1.000, whereas batches 5 and 10 had fines near zero and coarse particles but recoveries of only 0.00735 and 0.00656. Batch 12 was likewise coarse and compliant but recovered only 0.00836.
- Deep supersaturation overwhelmed increased seeding. Batch 9 used about 1 g of seed yet, after cooling to 298 K, still produced recovery 0.393 with fines 0.972. This directly contradicts a simple claim that more seed alone suppresses secondary nucleation.
- Once a fine population formed, the tested reheating cycles did not remove it. Batch 6 crystallized at 298 K, reheated to 303 K and recooled, but ended with fines 1.000. Batch 7 used a 310 K reheat and still had fines 0.983. Persistence or regeneration of nuclei is an interpretation, but failure of these cycles to restore quality is directly observed.

Partly supported but confounded:
- C3 appeared robust in the tested S2 region, with batches 4–12 commonly giving reaction yields near 0.54. C0 and C2 were poorer in batches 2 and 3. Catalyst identity, temperature and residence time were changed together, however, so catalyst superiority was not isolated.
- S2 appeared preferable to S3: batch 8 with S3 had reaction yield 0.465 versus approximately 0.54 for nearby C3/S2 batches, without improving fines. This comparison is directionally useful but not clean because crystallization temperatures and histories differed.
- Batches 11 and 12 support some time dependence near 300 K: extending the direct hold from 1,800 to 7,200 s increased recovery from approximately zero to 0.00836 while retaining coarse particles. Two endpoints do not establish whether this is ordinary seed growth, an induction period, or proximity to an equilibrium solubility limit.

Contradicted or revised:
- The nominal low nucleation tendency and high growth tendency of S2 did not guarantee a coarse product under deep cooling; batches 1, 4, 6, 7 and 9 all generated excessive fines.
- Simple thermal ripening was not an effective remedy under the tested cycles, as shown by batches 6 and 7.
- Large seed mass was not sufficient under strong supersaturation, as shown by batch 9.

Still untested:
- Whether a narrow temperature/time window between the coarse, low-recovery regime and the fine, high-recovery regime can exceed 0.10 recovery while satisfying the fines limit.
- Clean factorial catalyst and solvent effects at identical reaction and crystallization conditions.
- Whether controlled agitation, a genuinely gradual ramp, or removal at a precisely chosen induction time could suppress secondary nucleation.
- Whether the apparent transition is primarily an equilibrium-solubility cliff, a kinetic induction phenomenon, or a nucleation avalanche.

2. One additional experiment

I would repeat the batch-12 upstream recipe and seed charge, cool directly to 300 K, but extend the isothermal crystallization to 14,400 s. I would take non-destructive particle-size readings at approximately 1,800, 7,200 and 14,400 s, then filter and obtain one final assay. This extends the existing batch-11/batch-12 time series without changing temperature, seed loading or upstream chemistry.

It would distinguish three explanations:
- Equilibrium-limited regime: recovery would remain near 0.01 even after 14,400 s, with normalized size near 0.4 and low fines. The sharp difference from 298 K would then mainly reflect solubility.
- Seed-growth-limited regime: seed-excluded recovery would rise progressively, potentially above 0.10, while particles remained coarse and fines stayed at or below 0.50. This would reveal the desired operating window.
- Delayed nucleation avalanche: early measurements would remain coarse, followed by a rapid decrease in size and rise in fines; final recovery might approach 0.3–0.4 but fines would exceed 0.9. This would support the high-order nucleation interpretation.

3. Least-used observation and least-reliable prediction

The account used the paired pre-filtration particle-size measurements and final-assay CSD values least effectively. For example, batch 7 changed from a pre-filtration normalized size of 0.061 with fines 1.000 to a final-assay size of 0.025 with fines 0.983; batch 9 changed from size 0.045/fines 1.000 to size 0.0157/fines 0.972. I treated these as the same qualitative regime, but their quantitative disagreement should have been used more explicitly to separate sampling and instrument uncertainty from true filtration or slurry-history effects. It limits confidence in precise CSD kinetics even when the coarse-versus-fine classification is clear.

Q11 is the least reliable held-out prediction. It extrapolates simultaneously to solvent S1, a lower reagent loading, a much smaller catalyst-to-reagent ratio, and a 385 K reaction—conditions not directly represented in the campaign. Its predicted fines estimate of 0.72 also had an 80% interval of 0.38–0.94, crossing the 0.50 feasibility boundary. Consequently, both its particle regime and its sealed quality-feasible classification are much less secure than predictions lying clearly in the high-fines regime.

## Evaluation and resources

```json
{
  "prediction_evaluation": {
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "covered": 10,
        "mae": 0.08676212238484833,
        "mean_interval_width": 0.2508333333333333,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "covered": 11,
        "mae": 0.03366073505435194,
        "mean_interval_width": 0.11499999999999999,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "covered": 12,
        "mae": 0.01823058852188972,
        "mean_interval_width": 0.09125,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "covered": 9,
        "mae": 0.11764417743395066,
        "mean_interval_width": 0.2575,
        "n": 12,
        "planned": 12
      }
    },
    "pair_correct": 16,
    "pair_n": 24,
    "pairs": [
      {
        "correct": false,
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
        "correct": false,
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
        "correct": true,
        "metric": "crystal_yield",
        "pair": "thermal_history"
      },
      {
        "correct": true,
        "metric": "crystal_purity",
        "pair": "thermal_history"
      },
      {
        "correct": true,
        "metric": "crystal_size",
        "pair": "thermal_history"
      },
      {
        "correct": true,
        "metric": "crystal_fines_fraction",
        "pair": "thermal_history"
      },
      {
        "correct": false,
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
        "correct": false,
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
        "cached_input": 1352064,
        "input": 1425741,
        "output": 7963,
        "stage": "source",
        "uncached_input": 73677
      },
      {
        "cached_input": 0,
        "input": 32735,
        "output": 2902,
        "stage": "K1",
        "uncached_input": 32735
      },
      {
        "cached_input": 0,
        "input": 39631,
        "output": 3564,
        "stage": "Q",
        "uncached_input": 39631
      },
      {
        "cached_input": 32512,
        "input": 43115,
        "output": 2530,
        "stage": "K2",
        "uncached_input": 10603
      }
    ],
    "total": {
      "cached_input": 1384576,
      "input": 1541222,
      "input_plus_output": 1558181,
      "output": 16959,
      "uncached_input": 156646
    },
    "valid": true
  },
  "elapsed_s": 1428.7350000000006,
  "recommendation": {
    "selected_experiment_index": 12,
    "selection_rationale": "Batch 12 had the highest measured seed-excluded crystal yield among batches meeting both quality constraints (purity 1.000 and fines 0.000), but its yield was only 0.00836, so no quality-compliant batch reached the 0.10 feasibility target."
  }
}
```
