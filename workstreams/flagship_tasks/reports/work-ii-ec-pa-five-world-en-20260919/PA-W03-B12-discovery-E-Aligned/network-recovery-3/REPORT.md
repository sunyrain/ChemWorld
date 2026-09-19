# PA-W03-B12-discovery-E-Aligned

Development experiment; one independent source session.

Status: completed; completed batches: 12/12; posttests: 3/3.

## Research assignment

You are an autonomous scientist studying two-phase partition in a simulated lab.
Use only chemworld_lab and public_numerics. No filesystem, network, repository, hidden physics,
or general code execution is available. First read material_information. Follow research_goal.
Conduct 12 independent batches from the same initial mixture; conditions and repetition are
your choice. You have 12 additional instrument uses shared across batches and 12 final assays.
Follow actual tool schemas, legal operation ranges, and operational_state. Read all purchased
measurement outputs; preserve their batch, timing, and whether a phase has already been removed.
HPLC before separate_phase provides the two-phase readings. product_in_organic and
product_in_aqueous are fractions of this batch's fixed initial target inventory, NOT concentrations.
phase_ratio means organic volume divided by total two-phase volume. Solvent addition and initial
liquid contribute to actual volumes; an aqueous addition is not the entire aqueous volume.
separate_phase retains the requested phase and removes the other; it is not a sampling switch.
Instrument noise and sampling affect observed closure. Do not infer missing measurements as zero.
Use the current lawful workflow; explicitly terminate and measure final_assay for each batch.
An ended batch is not an ended campaign: use next_state until campaign_ended=true, then stop step.
There are no mandatory belief snapshots or fixed mechanism templates. After campaign terminal
return only status/summary JSON with a brief completion handoff; no best-batch recommendation.
Later turns request your mechanism, blind predictions and reflection. Do not answer them early.
Anonymous IDs are independent categories, not ordered numbers or real chemical identities.
You may use the public calculator to fit your own relationships within its supported operations.
No particular discovery or high score is required; report uncertainty and unavailable evidence.
Use English for all research notes, explanations and final reports.


Discover and test a predictive explanation of target partition between the two phases, including material pairing, phase amounts and mixing. Choose twelve experiments freely. Explain evidence, alternatives and limits. Predict new conditions and phase-retention decisions after the campaign. Native score is not this task's objective. No best recipe, prescribed law, or belief checkpoints are required.

## Batch outcomes

| Batch | Final measured outcomes |
| --- | --- |
| 1 | {"cost": 0.41635000705718994, "impurity_signal": 0.1179036796092987, "phase_ratio": 0.009452268481254578, "product_in_aqueous": 0.8432157635688782, "product_in_organic": 0.0012433052761480212, "purity": 0.8672172427177429, "recovery": 0.8395699262619019, "safety_risk": 0.06114867329597473, "score": 0.0} |
| 2 | {"cost": 0.4323500096797943, "impurity_signal": 0.0, "phase_ratio": 0.9997019171714783, "product_in_aqueous": 0.02075776644051075, "product_in_organic": 0.32647424936294556, "purity": 0.975248396396637, "recovery": 0.31053847074508667, "safety_risk": 0.06862150877714157, "score": 0.1754571497440338} |
| 3 | {"cost": 0.45794999599456787, "impurity_signal": 0.10838508605957031, "phase_ratio": 0.0, "product_in_aqueous": 0.6473185420036316, "product_in_organic": 0.005547169595956802, "purity": 0.8420343995094299, "recovery": 0.6453317999839783, "safety_risk": 0.09912977367639542, "score": 0.0} |
| 4 | {"cost": 0.4419499933719635, "impurity_signal": 0.026457572355866432, "phase_ratio": 1.0, "product_in_aqueous": 0.0, "product_in_organic": 0.2786765992641449, "purity": 0.9735644459724426, "recovery": 0.27451246976852417, "safety_risk": 0.09793778508901596, "score": 0.13687510788440704} |
| 5 | {"cost": 0.45794999599456787, "impurity_signal": 0.1265806257724762, "phase_ratio": 0.0, "product_in_aqueous": 0.6946924924850464, "product_in_organic": 0.0, "purity": 0.847101092338562, "recovery": 0.6935437321662903, "safety_risk": 0.09994383156299591, "score": 0.0} |
| 6 | {"cost": 0.45794999599456787, "impurity_signal": 0.014463111758232117, "phase_ratio": 0.9943565726280212, "product_in_aqueous": 0.0156232425943017, "product_in_organic": 0.22246459126472473, "purity": 0.9661800265312195, "recovery": 0.2351699024438858, "safety_risk": 0.08339095115661621, "score": 0.08809693157672882} |
| 7 | {"cost": 0.45794999599456787, "impurity_signal": 0.11504428088665009, "phase_ratio": 0.003050468396395445, "product_in_aqueous": 0.6430827379226685, "product_in_organic": 0.0, "purity": 0.8440849781036377, "recovery": 0.6333598494529724, "safety_risk": 0.09879007935523987, "score": 0.0} |
| 8 | {"cost": 0.41635000705718994, "impurity_signal": 0.005665012635290623, "phase_ratio": 0.9789910912513733, "product_in_aqueous": 0.0284495260566473, "product_in_organic": 0.37182459235191345, "purity": 0.9545015692710876, "recovery": 0.3884548246860504, "safety_risk": 0.0482814684510231, "score": 0.2153068333864212} |
| 9 | {"cost": 0.4118500053882599, "impurity_signal": 0.008014112710952759, "phase_ratio": 1.0, "product_in_aqueous": 0.0, "product_in_organic": 0.217049703001976, "purity": 0.9806706309318542, "recovery": 0.23330093920230865, "safety_risk": 0.05173975229263306, "score": 0.08449224382638931} |
| 10 | {"cost": 0.42085000872612, "impurity_signal": 0.11456926167011261, "phase_ratio": 0.015568170696496964, "product_in_aqueous": 0.4996277391910553, "product_in_organic": 0.005932251922786236, "purity": 0.8303298354148865, "recovery": 0.5126102566719055, "safety_risk": 0.06011790409684181, "score": 0.0} |
| 11 | {"cost": 0.41514167189598083, "impurity_signal": 0.023524809628725052, "phase_ratio": 1.0, "product_in_aqueous": 0.0, "product_in_organic": 0.29310086369514465, "purity": 0.9725182056427002, "recovery": 0.2911600172519684, "safety_risk": 0.04413541406393051, "score": 0.1491357386112213} |
| 12 | {"cost": 0.42010000348091125, "impurity_signal": 0.11244789510965347, "phase_ratio": 0.0, "product_in_aqueous": 0.560819149017334, "product_in_organic": 0.003923420328646898, "purity": 0.8267876505851746, "recovery": 0.5668728947639465, "safety_risk": 0.05589726194739342, "score": 0.0} |

Public operations and purchased measurements: [trajectory](public-trajectory.json).

## K1

### Question

The campaign has ended. Explain in English your account of this system's partition
behavior, the specific batches and measurements supporting it, the contributions of supplied
information and experiments, and remaining competing explanations or uncertain scope.
Your representation is unrestricted; no prescribed equation is required. Do not copy the
entire data table. Distinguish observations, inference and conjecture. Return the report
field. This report is sealed before prediction questions are presented.

### Response

Observations

All 12 batches used 0.020 mol reagent and 0.040 L solvent. Unless noted, they also used 0.040 L aqueous phase, 0.020 L extractant, mixing for 300 s at 600 rpm, and settling for 300 s. HPLC was measured before separation; the final assay was measured after one phase was retained.

Material pairing had a large effect under the common process. With X0, batches 1–4 changed solvent from S0 to S3. The measured organic target fractions were 0.152, 0.328, 0.320 and 0.296, respectively, while the aqueous fractions were 0.800, 0.704, 0.675 and 0.695. Thus S0–X0 was distinctly unfavorable to organic transfer, whereas S1–X0, S2–X0 and S3–X0 were similar and better.

Holding S2 fixed and changing extractant in batches 3, 5, 6 and 7 gave organic target fractions of 0.320 with X0, 0.298 with X1, 0.216 with X2 and 0.367 with X3. X3 was best in this tested S2 series, while X2 was unexpectedly weak. Batch 8 then tested S0–X3 and gave 0.376 organic versus 0.600 aqueous, much better than S0–X0 in batch 1. This crossover is direct evidence that solvent and extractant effects are not adequately described by independent marginal rankings.

As a concentration-based diagnostic, I combined the two target fractions with the measured phase ratio, treating phase_ratio as the organic volume fraction. The resulting apparent organic/aqueous concentration-ratio indices were approximately 0.93, 1.66, 1.84 and 1.77 for batches 1–4; 1.51, 1.05 and 2.50 for S2–X1, S2–X2 and S2–X3; and 2.90 for S0–X3 in batch 8. These are derived summaries, not directly observed equilibrium constants.

Phase amount produced the expected directional inventory shift for S0–X3. Batch 9 used 0.010 L extractant and 0.050 L added aqueous phase: phase_ratio was 0.094 and target was 0.233 organic/0.749 aqueous. Standard batch 8 had phase_ratio 0.178 and 0.376/0.600. Batch 10 used 0.030 L extractant and 0.030 L aqueous phase: phase_ratio rose to 0.309 and target shifted to 0.526 organic/0.485 aqueous. The corresponding apparent concentration-ratio indices were about 3.01, 2.90 and 2.42, so increasing organic phase amount raised organic recovery strongly but did not preserve one perfectly constant ratio.

Mixing also mattered. At the standard S0–X3 phase amounts, weak mixing in batch 11 (10 s, 100 rpm) gave 0.318 organic and 0.675 aqueous. Standard batch 8 gave 0.376 and 0.600. Intense mixing in batch 12 (1200 s, 1200 rpm) gave 0.470 and 0.555. Their apparent indices rose from about 1.74 to 2.90 to 3.49. Duration and speed were changed together, so their separate effects were not identified.

The phase-retention assays independently supported the allocation measurements. For organic-retention batches 2, 4, 6, 8, 9 and 11, final organic target estimates (0.326, 0.279, 0.222, 0.372, 0.217 and 0.293) were close to the preceding HPLC organic estimates (0.328, 0.296, 0.216, 0.376, 0.233 and 0.318), with little target in the discarded-phase channel. For aqueous-retention batches 1, 3, 5, 7, 10 and 12, final aqueous estimates (0.843, 0.647, 0.695, 0.643, 0.500 and 0.561) similarly tracked pre-separation values (0.800, 0.675, 0.708, 0.614, 0.485 and 0.555). This makes phase-label reversal or a gross separation failure unlikely.

Inference

My working account is a material-pair-specific partition process overlaid by finite mass-transfer kinetics and phase-volume leverage. The solvent–extractant pair determines a conditional affinity for the target; organic phase amount then converts that affinity into the fraction recoverable in each phase. Mixing controls how nearly the batch approaches its attainable allocation before separation. S0–X3 was the strongest tested pair, but that statement is conditional on the tested volume and mixing window and is not a claim of global optimality.

The volume results are qualitatively consistent with a distribution process: more organic phase captures more total target even when the inferred concentration ratio changes moderately. A useful predictive representation would therefore use at least three components—pair identity, organic/aqueous phase ratio, and a saturating mixing or mass-transfer term—rather than one universal partition coefficient. Because intense mixing continued to improve transfer beyond the standard treatment, the 300 s/600 rpm observations may not all be equilibrium measurements.

The retention evidence implies a simple decision principle within the observed range: retain the organic phase when organic target recovery is the objective, but retain the aqueous phase when the measured allocation remains predominantly aqueous. Even the strongest tested organic transfer did not eliminate substantial aqueous target, so discarding that phase entails a measurable recovery loss.

Supplied information versus experimental contribution

The supplied nominal dossier was useful as a prior: it suggested that S2 had the strongest marginal solvent profile, that X3 had a high marginal product-distribution tendency, and that X2 had high marginal selectivity. It also correctly warned that pair interactions, volume response and mixing response were undisclosed. The experiments supplied the decisive information. They showed that X2 could be weak with S2, that X3 paired especially well with S0, that changing organic phase amount moved inventory strongly, and that mixing remained influential. Therefore I retain the dossier as broad marginal context but would not use its rankings as substitutes for pairwise measurements.

Competing explanations and uncertain scope

The mixing trend is compatible with ordinary approach to equilibrium, but it could also reflect shear-dependent dispersion, emulsion carryover, phase sampling, or solvent-loss effects. Since speed and duration were confounded and there were no replicate batches, those alternatives cannot be separated.

The changing apparent ratio across phase amounts could indicate a genuinely nonlinear or composition-dependent partition law. It could instead arise because changing aqueous and extractant additions also changes matrix composition, measured phase volume, entrainment, or process noise. Accordingly, the calculated indices should not be treated as thermodynamic constants.

Pre-separation impurity signals were generally small (0–0.019), whereas aqueous-retention final assays showed impurity around 0.108–0.127 and lower purity than most organic-retention assays. This may indicate preferential aqueous impurity retention, but an assay- or matrix-specific shift is a viable alternative because the pre- and post-separation measurements used different instruments and sample states.

Coverage remains incomplete: only the X0 solvent row, the S2 extractant column, and S0–X3 were examined among the 16 possible pairs. Each tested condition had one batch, only three phase-amount settings and three jointly varied mixing settings were studied, and settling time, reagent loading and repeated extractions were not varied. Predictions should therefore be restricted to interpolation near these materials and operating ranges, with wider uncertainty for untested pairings, extrapolated phase ratios, or claims of equilibrium.

## Q

### Question

Using your research, predict the true two-phase target fractions immediately before the first HPLC sample in these 12 independent new batches. The denominator is each batch's fixed initial target inventory. Give a point estimate and a 90% uncertainty interval for each noiseless fraction; do not predict random instrument noise. No new experiments or changes to K1 are allowed. Predict before phase removal, not the terminal assay after selecting a phase. D1: Which phase should be retained in Q01 to keep more target? D2: Under the same material amounts, does Q05 or Q06 place more target in the organic phase? Both decisions allow uncertain. Supply one shared concise rationale in English, without a long explanation per question. Return the required JSON.
[{"query_id": "Q01", "actions": [{"operation": "add_solvent", "solvent": 0, "volume_L": 0.02}, {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.03}, {"operation": "add_extractant", "extractant": 0, "volume_L": 0.008}, {"operation": "mix", "duration_s": 900, "stirring_speed_rpm": 1200}, {"operation": "settle", "duration_s": 300}, {"operation": "measure", "instrument": "hplc"}, {"operation": "separate_phase", "target_phase": "organic"}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q02", "actions": [{"operation": "add_solvent", "solvent": 0, "volume_L": 0.02}, {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.03}, {"operation": "add_extractant", "extractant": 0, "volume_L": 0.03}, {"operation": "mix", "duration_s": 900, "stirring_speed_rpm": 1200}, {"operation": "settle", "duration_s": 300}, {"operation": "measure", "instrument": "hplc"}, {"operation": "separate_phase", "target_phase": "organic"}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q03", "actions": [{"operation": "add_solvent", "solvent": 0, "volume_L": 0.02}, {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.03}, {"operation": "add_extractant", "extractant": 3, "volume_L": 0.008}, {"operation": "mix", "duration_s": 900, "stirring_speed_rpm": 1200}, {"operation": "settle", "duration_s": 300}, {"operation": "measure", "instrument": "hplc"}, {"operation": "separate_phase", "target_phase": "organic"}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q04", "actions": [{"operation": "add_solvent", "solvent": 0, "volume_L": 0.02}, {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.03}, {"operation": "add_extractant", "extractant": 3, "volume_L": 0.03}, {"operation": "mix", "duration_s": 900, "stirring_speed_rpm": 1200}, {"operation": "settle", "duration_s": 300}, {"operation": "measure", "instrument": "hplc"}, {"operation": "separate_phase", "target_phase": "organic"}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q05", "actions": [{"operation": "add_solvent", "solvent": 0, "volume_L": 0.02}, {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.015}, {"operation": "add_extractant", "extractant": 0, "volume_L": 0.019}, {"operation": "mix", "duration_s": 900, "stirring_speed_rpm": 1200}, {"operation": "settle", "duration_s": 300}, {"operation": "measure", "instrument": "hplc"}, {"operation": "separate_phase", "target_phase": "organic"}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q06", "actions": [{"operation": "add_solvent", "solvent": 0, "volume_L": 0.02}, {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.015}, {"operation": "add_extractant", "extractant": 3, "volume_L": 0.019}, {"operation": "mix", "duration_s": 900, "stirring_speed_rpm": 1200}, {"operation": "settle", "duration_s": 300}, {"operation": "measure", "instrument": "hplc"}, {"operation": "separate_phase", "target_phase": "organic"}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q07", "actions": [{"operation": "add_solvent", "solvent": 2, "volume_L": 0.02}, {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.015}, {"operation": "add_extractant", "extractant": 0, "volume_L": 0.019}, {"operation": "mix", "duration_s": 900, "stirring_speed_rpm": 1200}, {"operation": "settle", "duration_s": 300}, {"operation": "measure", "instrument": "hplc"}, {"operation": "separate_phase", "target_phase": "organic"}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q08", "actions": [{"operation": "add_solvent", "solvent": 2, "volume_L": 0.02}, {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.015}, {"operation": "add_extractant", "extractant": 3, "volume_L": 0.019}, {"operation": "mix", "duration_s": 900, "stirring_speed_rpm": 1200}, {"operation": "settle", "duration_s": 300}, {"operation": "measure", "instrument": "hplc"}, {"operation": "separate_phase", "target_phase": "organic"}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q09", "actions": [{"operation": "add_solvent", "solvent": 0, "volume_L": 0.02}, {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.015}, {"operation": "add_extractant", "extractant": 0, "volume_L": 0.019}, {"operation": "mix", "duration_s": 120, "stirring_speed_rpm": 700}, {"operation": "settle", "duration_s": 300}, {"operation": "measure", "instrument": "hplc"}, {"operation": "separate_phase", "target_phase": "organic"}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q10", "actions": [{"operation": "add_solvent", "solvent": 0, "volume_L": 0.02}, {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.015}, {"operation": "add_extractant", "extractant": 0, "volume_L": 0.019}, {"operation": "mix", "duration_s": 1200, "stirring_speed_rpm": 700}, {"operation": "settle", "duration_s": 300}, {"operation": "measure", "instrument": "hplc"}, {"operation": "separate_phase", "target_phase": "organic"}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q11", "actions": [{"operation": "add_solvent", "solvent": 2, "volume_L": 0.02}, {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.015}, {"operation": "add_extractant", "extractant": 3, "volume_L": 0.019}, {"operation": "mix", "duration_s": 600, "stirring_speed_rpm": 200}, {"operation": "settle", "duration_s": 300}, {"operation": "measure", "instrument": "hplc"}, {"operation": "separate_phase", "target_phase": "organic"}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q12", "actions": [{"operation": "add_solvent", "solvent": 2, "volume_L": 0.02}, {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.015}, {"operation": "add_extractant", "extractant": 3, "volume_L": 0.019}, {"operation": "mix", "duration_s": 600, "stirring_speed_rpm": 1200}, {"operation": "settle", "duration_s": 300}, {"operation": "measure", "instrument": "hplc"}, {"operation": "separate_phase", "target_phase": "organic"}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}]

### Response

```json
{
  "D1_phase": "aqueous",
  "D2_query": "Q06",
  "predictions": [
    {
      "product_in_aqueous": {
        "estimate": 0.86,
        "lower90": 0.79,
        "upper90": 0.91
      },
      "product_in_organic": {
        "estimate": 0.14,
        "lower90": 0.09,
        "upper90": 0.21
      },
      "query_id": "Q01"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.62,
        "lower90": 0.52,
        "upper90": 0.71
      },
      "product_in_organic": {
        "estimate": 0.38,
        "lower90": 0.29,
        "upper90": 0.48
      },
      "query_id": "Q02"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.658,
        "lower90": 0.56,
        "upper90": 0.75
      },
      "product_in_organic": {
        "estimate": 0.342,
        "lower90": 0.25,
        "upper90": 0.44
      },
      "query_id": "Q03"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.339,
        "lower90": 0.25,
        "upper90": 0.44
      },
      "product_in_organic": {
        "estimate": 0.661,
        "lower90": 0.56,
        "upper90": 0.75
      },
      "query_id": "Q04"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.644,
        "lower90": 0.55,
        "upper90": 0.73
      },
      "product_in_organic": {
        "estimate": 0.356,
        "lower90": 0.27,
        "upper90": 0.45
      },
      "query_id": "Q05"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.362,
        "lower90": 0.27,
        "upper90": 0.46
      },
      "product_in_organic": {
        "estimate": 0.638,
        "lower90": 0.54,
        "upper90": 0.73
      },
      "query_id": "Q06"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.439,
        "lower90": 0.34,
        "upper90": 0.54
      },
      "product_in_organic": {
        "estimate": 0.561,
        "lower90": 0.46,
        "upper90": 0.66
      },
      "query_id": "Q07"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.377,
        "lower90": 0.28,
        "upper90": 0.48
      },
      "product_in_organic": {
        "estimate": 0.623,
        "lower90": 0.52,
        "upper90": 0.72
      },
      "query_id": "Q08"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.692,
        "lower90": 0.59,
        "upper90": 0.79
      },
      "product_in_organic": {
        "estimate": 0.308,
        "lower90": 0.21,
        "upper90": 0.41
      },
      "query_id": "Q09"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.648,
        "lower90": 0.54,
        "upper90": 0.75
      },
      "product_in_organic": {
        "estimate": 0.352,
        "lower90": 0.25,
        "upper90": 0.46
      },
      "query_id": "Q10"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.419,
        "lower90": 0.31,
        "upper90": 0.53
      },
      "product_in_organic": {
        "estimate": 0.581,
        "lower90": 0.47,
        "upper90": 0.69
      },
      "query_id": "Q11"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.384,
        "lower90": 0.28,
        "upper90": 0.49
      },
      "product_in_organic": {
        "estimate": 0.616,
        "lower90": 0.51,
        "upper90": 0.72
      },
      "query_id": "Q12"
    }
  ],
  "rationale": "I used a pair-specific distribution model with organic-phase volume leverage and a saturating mixing correction. The S0–X3 and S2–X3 pairings were assigned stronger organic affinity than their X0 counterparts, consistent with batches 1, 3, 7 and 8; phase-volume behavior was anchored by batches 8–10, and mixing by batches 8, 11 and 12. Fractions are complementary and represent noiseless pre-sampling allocation; intervals reflect sparse pairing coverage, unreplicated process variation, and extrapolation of mixing conditions, not HPLC noise."
}
```

## K2

### Question

Your mechanism report and predictions are sealed, and no truth has been supplied.
Answer three questions in English, citing batches without repeating the full report:
1. Which supplied claim or self-developed law is most likely wrong or still untested?
State explicitly if no instance prior was supplied.
2. With one more experiment, what would you do and measure to distinguish your leading
explanation from an alternative? How would different results change your judgment? Do not execute.
3. Which existing evidence was underused, which predictions are least reliable, and is there
any inconsistency between the report and predictions? Do not present hindsight as a
contemporaneous record or modify sealed outputs. Return the report field.

### Response

1. Most questionable claim or law

An instance prior was supplied: the nominal marginal material dossier. Its rankings were panel averages rather than instance-specific pair values, so batches 1, 6–8 do not prove the dossier wrong. They instead show why marginal rankings cannot determine a particular pair.

The least-tested self-developed law is my transferable “pair affinity × phase-volume leverage × saturating mixing” model. Mixing duration and speed were changed together in batches 11, 8 and 12, and only for S0–X3. Consequently, the assumed saturation curve and its transfer to X0 or S2–X3 may be wrong. Treating nominal extractant/total liquid volume as the future organic phase ratio is also weakly tested because measured phase_ratio varied with material and processing.

2. One discriminating experiment

I would repeat the S0–X3 composition of batch 8—0.040 L solvent, 0.040 L aqueous phase and 0.020 L extractant—but mix for 1200 s at the same 600 rpm used in batch 8, settle for 300 s, and measure pre-separation HPLC target fractions and phase_ratio. This changes duration without changing speed.

If organic target rose from batch 8’s 0.376 toward batch 12’s 0.470 while phase_ratio remained comparable, that would favor slow approach to partition equilibrium. If it stayed near batch 8 despite the longer duration, the batch-12 improvement would more likely depend on high shear, dispersion, entrainment or a sampling effect. A large phase_ratio change would specifically weaken the interpretation that target redistribution alone caused the apparent mixing benefit. Because there were no replicates, one intermediate result would remain ambiguous rather than establish a precise law.

3. Underused evidence, unreliable predictions and consistency

I underused the measured phase_ratio variation. At nominally identical phase amounts it ranged from about 0.178 to 0.213 across batches 8, 11 and 12, and also varied among material pairs. The predictions largely replaced that evidence with ratios calculated from nominal added volumes. I also used the retention assays mainly as qualitative validation, rather than exploiting their pre/post differences to quantify process or phase-carryover uncertainty. The observed departures of the two target fractions from exact closure, and the dossier’s material-specific variability information, could likewise have supported wider predictive intervals.

The least reliable predictions are Q11 and Q12 because they require an rpm effect for S2–X3 even though speed and duration were never independently varied and mixing behavior was measured only for S0–X3. Q01–Q04 are also weak because they combine untested 0.020 L solvent loading with phase ratios outside or near the edge of the directly studied settings; Q02 additionally extrapolates strong mixing for S0–X0. Q07 and Q08 transfer mixing behavior to S2 pairs from only one standard-condition observation per relevant pair.

There is no direct categorical contradiction between the sealed report and predictions, but there is tension. The report warned that no universal constant ratio was established and that the mixing mechanism was confounded, whereas the predictions operationalized a distribution-ratio formula with a transferable saturation correction. The predictions also forced aqueous and organic fractions to sum exactly to one, while the report noted possible matrix, loss and process effects and the observed HPLC sums did not close exactly. Thus the point estimates—and probably several intervals—were more structurally confident than the report justified. This is a retrospective critique of the sealed outputs, not a modification of them, and no truth feedback was available.

## Evaluation and resource use

```json
{
  "arm": "Aligned",
  "budget": 12,
  "goal": "discovery",
  "locus": "E",
  "system": "PA",
  "unit_id": "PA-W03-B12-discovery-E-Aligned",
  "world": {
    "world_id": "PA-W03",
    "world_interventions": [
      {
        "axis_id": "partition.distribution-coefficient",
        "mode": "extrapolation",
        "severity": -0.75
      }
    ],
    "world_seed": 2
  },
  "status": "completed",
  "source_status": "completed",
  "completed_batches": 12,
  "operations": 120,
  "posttests_completed": 3,
  "exact_replay": {
    "checked_steps": 120,
    "max_abs_error": 0.0,
    "mismatches": [],
    "verified": true
  },
  "failure": null,
  "source_failure": null,
  "interruption": null,
  "prediction_evaluation": {
    "decisions": {
      "D1": {
        "correct": true,
        "submitted": "aqueous",
        "truth": "aqueous"
      },
      "D2": {
        "correct": true,
        "submitted": "Q06",
        "truth": "Q06"
      }
    },
    "details": [
      {
        "absolute_error": 0.00028028852564415674,
        "estimate": 0.14,
        "lower90": 0.09,
        "metric": "product_in_organic",
        "query_id": "Q01",
        "truth": 0.14028028852564417,
        "upper90": 0.21
      },
      {
        "absolute_error": 0.003711402009393572,
        "estimate": 0.38,
        "lower90": 0.29,
        "metric": "product_in_organic",
        "query_id": "Q02",
        "truth": 0.37628859799060643,
        "upper90": 0.48
      },
      {
        "absolute_error": 0.003822944911337278,
        "estimate": 0.342,
        "lower90": 0.25,
        "metric": "product_in_organic",
        "query_id": "Q03",
        "truth": 0.33817705508866275,
        "upper90": 0.44
      },
      {
        "absolute_error": 0.013801152427159291,
        "estimate": 0.661,
        "lower90": 0.56,
        "metric": "product_in_organic",
        "query_id": "Q04",
        "truth": 0.6471988475728407,
        "upper90": 0.75
      },
      {
        "absolute_error": 0.0024776380656193475,
        "estimate": 0.356,
        "lower90": 0.27,
        "metric": "product_in_organic",
        "query_id": "Q05",
        "truth": 0.35352236193438064,
        "upper90": 0.45
      },
      {
        "absolute_error": 0.012673505119815465,
        "estimate": 0.638,
        "lower90": 0.54,
        "metric": "product_in_organic",
        "query_id": "Q06",
        "truth": 0.6253264948801845,
        "upper90": 0.73
      },
      {
        "absolute_error": 0.025316116036231295,
        "estimate": 0.561,
        "lower90": 0.46,
        "metric": "product_in_organic",
        "query_id": "Q07",
        "truth": 0.5863161160362313,
        "upper90": 0.66
      },
      {
        "absolute_error": 0.01613192686300924,
        "estimate": 0.623,
        "lower90": 0.52,
        "metric": "product_in_organic",
        "query_id": "Q08",
        "truth": 0.6068680731369908,
        "upper90": 0.72
      },
      {
        "absolute_error": 0.03998330399677086,
        "estimate": 0.308,
        "lower90": 0.21,
        "metric": "product_in_organic",
        "query_id": "Q09",
        "truth": 0.26801669600322914,
        "upper90": 0.41
      },
      {
        "absolute_error": 0.011819272484720644,
        "estimate": 0.352,
        "lower90": 0.25,
        "metric": "product_in_organic",
        "query_id": "Q10",
        "truth": 0.34018072751527934,
        "upper90": 0.46
      },
      {
        "absolute_error": 0.02704521041553476,
        "estimate": 0.581,
        "lower90": 0.47,
        "metric": "product_in_organic",
        "query_id": "Q11",
        "truth": 0.5539547895844652,
        "upper90": 0.69
      },
      {
        "absolute_error": 0.021336926734923822,
        "estimate": 0.616,
        "lower90": 0.51,
        "metric": "product_in_organic",
        "query_id": "Q12",
        "truth": 0.5946630732650762,
        "upper90": 0.72
      },
      {
        "absolute_error": 0.00028028852564410123,
        "estimate": 0.86,
        "lower90": 0.79,
        "metric": "product_in_aqueous",
        "query_id": "Q01",
        "truth": 0.8597197114743559,
        "upper90": 0.91
      },
      {
        "absolute_error": 0.003711402009393572,
        "estimate": 0.62,
        "lower90": 0.52,
        "metric": "product_in_aqueous",
        "query_id": "Q02",
        "truth": 0.6237114020093936,
        "upper90": 0.71
      },
      {
        "absolute_error": 0.003822944911337167,
        "estimate": 0.658,
        "lower90": 0.56,
        "metric": "product_in_aqueous",
        "query_id": "Q03",
        "truth": 0.6618229449113372,
        "upper90": 0.75
      },
      {
        "absolute_error": 0.01380115242715918,
        "estimate": 0.339,
        "lower90": 0.25,
        "metric": "product_in_aqueous",
        "query_id": "Q04",
        "truth": 0.3528011524271592,
        "upper90": 0.44
      },
      {
        "absolute_error": 0.002477638065619292,
        "estimate": 0.644,
        "lower90": 0.55,
        "metric": "product_in_aqueous",
        "query_id": "Q05",
        "truth": 0.6464776380656193,
        "upper90": 0.73
      },
      {
        "absolute_error": 0.012673505119815465,
        "estimate": 0.362,
        "lower90": 0.27,
        "metric": "product_in_aqueous",
        "query_id": "Q06",
        "truth": 0.37467350511981545,
        "upper90": 0.46
      },
      {
        "absolute_error": 0.025316116036231295,
        "estimate": 0.439,
        "lower90": 0.34,
        "metric": "product_in_aqueous",
        "query_id": "Q07",
        "truth": 0.4136838839637687,
        "upper90": 0.54
      },
      {
        "absolute_error": 0.01613192686300924,
        "estimate": 0.377,
        "lower90": 0.28,
        "metric": "product_in_aqueous",
        "query_id": "Q08",
        "truth": 0.39313192686300924,
        "upper90": 0.48
      },
      {
        "absolute_error": 0.03998330399677097,
        "estimate": 0.692,
        "lower90": 0.59,
        "metric": "product_in_aqueous",
        "query_id": "Q09",
        "truth": 0.7319833039967709,
        "upper90": 0.79
      },
      {
        "absolute_error": 0.011819272484720589,
        "estimate": 0.648,
        "lower90": 0.54,
        "metric": "product_in_aqueous",
        "query_id": "Q10",
        "truth": 0.6598192724847206,
        "upper90": 0.75
      },
      {
        "absolute_error": 0.027045210415534815,
        "estimate": 0.419,
        "lower90": 0.31,
        "metric": "product_in_aqueous",
        "query_id": "Q11",
        "truth": 0.4460452104155348,
        "upper90": 0.53
      },
      {
        "absolute_error": 0.021336926734923822,
        "estimate": 0.384,
        "lower90": 0.28,
        "metric": "product_in_aqueous",
        "query_id": "Q12",
        "truth": 0.40533692673492383,
        "upper90": 0.49
      }
    ],
    "metrics": {
      "product_in_aqueous": {
        "coverage90": 1.0,
        "interval_score90": 0.19166666666666665,
        "mae": 0.014866640632513292,
        "mean_width90": 0.19166666666666665,
        "n": 12
      },
      "product_in_organic": {
        "coverage90": 1.0,
        "interval_score90": 0.19166666666666665,
        "mae": 0.014866640632513311,
        "mean_width90": 0.19166666666666665,
        "n": 12
      }
    },
    "valid": true
  },
  "token_accounting": {
    "valid": true,
    "complete": true,
    "basis": "cumulative thread snapshots differenced in source/K1/Q/K2 order",
    "stages": [
      {
        "stage": "source",
        "input": 527940,
        "cached_input": 492928,
        "output": 5538,
        "uncached_input": 35012
      },
      {
        "stage": "K1",
        "input": 65086,
        "cached_input": 31232,
        "output": 3513,
        "uncached_input": 33854
      },
      {
        "stage": "Q",
        "input": 78827,
        "cached_input": 37760,
        "output": 3481,
        "uncached_input": 41067
      },
      {
        "stage": "K2",
        "input": 42029,
        "cached_input": 33408,
        "output": 1694,
        "uncached_input": 8621
      }
    ],
    "total": {
      "input": 713882,
      "cached_input": 595328,
      "output": 14226,
      "uncached_input": 118554,
      "input_plus_output": 728108
    },
    "monetary_cost_usd": null
  },
  "elapsed_s": 503.2189999999973,
  "retest_batches": 0,
  "retest_operations": 0,
  "retest_replay": null,
  "english_output": true
}
```

## Infrastructure recovery

Original failed attempt is retained separately. Mode: fresh_source_after_partial_network_failure; new source batches: 12. See [recovery accounting](recovery.json).
