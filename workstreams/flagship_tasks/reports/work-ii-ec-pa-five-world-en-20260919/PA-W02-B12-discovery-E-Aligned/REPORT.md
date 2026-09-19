# PA-W02-B12-discovery-E-Aligned

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
| 1 | {"cost": 0.47635000944137573, "impurity_signal": 0.01737910322844982, "phase_ratio": 1.0, "product_in_aqueous": 0.014660237357020378, "product_in_organic": 0.3179311752319336, "purity": 0.9271557331085205, "recovery": 0.3277023136615753, "safety_risk": 0.042892295867204666, "score": 0.16877546906471252} |
| 2 | {"cost": 0.47635000944137573, "impurity_signal": 0.20963075757026672, "phase_ratio": 0.0, "product_in_aqueous": 0.47859546542167664, "product_in_organic": 0.008452002890408039, "purity": 0.6804139614105225, "recovery": 0.4503539204597473, "safety_risk": 0.08773481100797653, "score": 0.0} |
| 3 | {"cost": 0.47635000944137573, "impurity_signal": 0.01615975983440876, "phase_ratio": 0.96914142370224, "product_in_aqueous": 0.0, "product_in_organic": 0.4318270981311798, "purity": 0.9349672198295593, "recovery": 0.4173452854156494, "safety_risk": 0.04644053056836128, "score": 0.2701388895511627} |
| 4 | {"cost": 0.47635000944137573, "impurity_signal": 0.05617830529808998, "phase_ratio": 1.0, "product_in_aqueous": 0.0, "product_in_organic": 0.5566297769546509, "purity": 0.9410083293914795, "recovery": 0.5524656772613525, "safety_risk": 0.05257323011755943, "score": 0.3731353282928467} |
| 5 | {"cost": 0.4923500120639801, "impurity_signal": 0.03634076192975044, "phase_ratio": 0.9829117059707642, "product_in_aqueous": 0.0, "product_in_organic": 0.5002908110618591, "purity": 0.9361817240715027, "recovery": 0.49712783098220825, "safety_risk": 0.07278817892074585, "score": 0.32695600390434265} |
| 6 | {"cost": 0.5179499983787537, "impurity_signal": 0.23319312930107117, "phase_ratio": 0.0, "product_in_aqueous": 0.4863084554672241, "product_in_organic": 0.0, "purity": 0.6718740463256836, "recovery": 0.4713656008243561, "safety_risk": 0.12949404120445251, "score": 0.0} |
| 7 | {"cost": 0.5019500255584717, "impurity_signal": 0.021481527015566826, "phase_ratio": 1.0, "product_in_aqueous": 0.007889077998697758, "product_in_organic": 0.46649420261383057, "purity": 0.9483627676963806, "recovery": 0.46481817960739136, "safety_risk": 0.10187721997499466, "score": 0.29573115706443787} |
| 8 | {"cost": 0.4923500120639801, "impurity_signal": 0.014217344112694263, "phase_ratio": 0.9789910912513733, "product_in_aqueous": 0.0284495260566473, "product_in_organic": 0.35264644026756287, "purity": 0.9313703775405884, "recovery": 0.36927667260169983, "safety_risk": 0.0675937682390213, "score": 0.19900541007518768} |
| 9 | {"cost": 0.5179499983787537, "impurity_signal": 0.02234521135687828, "phase_ratio": 1.0, "product_in_aqueous": 0.0, "product_in_organic": 0.3964168429374695, "purity": 0.9601254463195801, "recovery": 0.4126680791378021, "safety_risk": 0.08679278194904327, "score": 0.23695430159568787} |
| 10 | {"cost": 0.49935001134872437, "impurity_signal": 0.024690978229045868, "phase_ratio": 1.0, "product_in_aqueous": 0.0009292740724049509, "product_in_organic": 0.40896669030189514, "purity": 0.9626874327659607, "recovery": 0.4169462323188782, "safety_risk": 0.08679278194904327, "score": 0.24752876162528992} |
| 11 | {"cost": 0.536549985408783, "impurity_signal": 0.03436798229813576, "phase_ratio": 1.0, "product_in_aqueous": 0.0, "product_in_organic": 0.40413767099380493, "purity": 0.9566212892532349, "recovery": 0.40219682455062866, "safety_risk": 0.08679278194904327, "score": 0.24351702630519867} |
| 12 | {"cost": 0.5167416930198669, "impurity_signal": 0.24150635302066803, "phase_ratio": 0.0, "product_in_aqueous": 0.6965757012367249, "product_in_organic": 0.003923420328646898, "purity": 0.7379035949707031, "recovery": 0.7026294469833374, "safety_risk": 0.1357472985982895, "score": 0.0} |

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

All pre-separation comparisons used HPLC after settling. Under the common 0.040 L solvent, 0.040 L aqueous-phase, 0.020 L extractant, 300 s/600 rpm mixing condition, partition depended strongly on the solvent–extractant pair. With S0, changing X0→X1→X2→X3 changed the organic target signal from 0.297 to 0.552, 0.400 and 0.574, respectively; the corresponding aqueous signals were 0.655, 0.480, 0.595 and 0.417 (batches 1–4). With X0, changing S0→S1→S2→S3 gave organic signals of 0.297, 0.495, 0.511 and 0.469 (batches 1, 5–7). Thus both identities matter, and their effects are not captured by one universal ranking. In particular, diagonal pairs S1–X1 and S2–X2 were relatively aqueous-favoring: organic signals were 0.357 and 0.412 in batches 8 and 9.

The controlled S2–X2 volume series showed little resolved phase-amount effect. Standard batch 9 gave aqueous/organic target signals of 0.569/0.412 and phase ratio 0.194. The aqueous-rich batch 10 (0.020 L solvent, 0.060 L aqueous, 0.020 L extractant) gave 0.583/0.428 and phase ratio 0.209; the organic-rich batch 11 (0.060/0.020/0.020 L) gave 0.564/0.429 and 0.213. These differences are comparable to the declared HPLC uncertainties, especially 0.015 for each product channel and 0.018 for phase ratio. Observed phase ratios across the standard pair screen were only about 0.17–0.22, so nominal addition volumes should not be equated directly with the measured final phase fraction.

Mixing produced a clearer change. Relative to standard S2–X2 batch 9, weak mixing in batch 12 (10 s/100 rpm rather than 300 s/600 rpm) reduced the organic target signal from 0.412 to 0.334, increased the aqueous signal from 0.569 to 0.691, and reduced pre-separation recovery from 0.422 to 0.309. The phase-ratio readings, 0.194 and 0.195, were essentially unchanged. Because these measurements preceded phase removal, this contrast is not caused by the different later retention choices.

Phase-retention assays behaved consistently with the pre-separation allocation. For example, retaining organic gave final organic target values of 0.318 for S0–X0, 0.557 for S0–X3, 0.500 for S1–X0 and 0.396 for standard S2–X2, close to their respective pre-separation organic signals. Retaining aqueous gave final aqueous target values of 0.479 in batch 2, 0.486 in batch 6 and 0.697 in weak-mix batch 12. The final phase-ratio channel became approximately 1 after organic retention and 0 after aqueous retention, as expected from the physical selection rather than as independent evidence about the original equilibrium.

Retention also exposed a selectivity tradeoff. The nine organic-retained final assays averaged about 0.944 purity and 0.027 impurity signal, whereas the three aqueous-retained assays averaged about 0.697 purity and 0.228 impurity signal. Thus the aqueous phase could contain more target in some batches, especially weakly mixed batch 12, but it also retained substantially more impurity under the tested conditions.

Inference

The most economical account is a pair-specific distribution equilibrium approached through finite mass transfer. Solvent and extractant jointly determine the target distribution coefficient; the interaction is appreciable, because rankings change with the partner and the S1–X1 and S2–X2 diagonal results are weaker than a simple marginal ranking would suggest. Adequate mixing moves target toward the organic phase for S2–X2, while weak contact leaves more target aqueous. Within the tested addition range, changing phase amounts had a much smaller effect than changing material pairing or mixing, or its effect was obscured by measurement noise and the system’s pre-existing liquid inventory.

The retention results further imply that the impurity partitions preferentially into, or is more concentrated in, the retained aqueous material. Organic retention therefore sacrifices any target left aqueous but provides a much cleaner retained fraction. This explanation fits both the target-channel continuity across separation and the large purity/impurity contrast in the final assays.

Contribution of supplied information versus experiments

The supplied dossier was useful as an incomplete prior: its marginal summaries suggested relatively strong nominal product distribution/selectivity for solvent S2 and extractants X2/X3. It explicitly warned that solvent and extractant indices are independent labels and withheld the interaction table, phase-volume law and mixing response. I therefore used it to choose informative pairings, not as outcome evidence. The experiments supplied the decisive information: the S0 and X0 cross-sections demonstrated partner dependence; S1–X1 and S2–X2 showed that favorable marginals do not guarantee a favorable pair; the repeated S2–X2 process variants isolated the small volume response and much larger weak-mixing response; and pre/post-separation measurements tested phase-retention consequences.

Competing explanations and uncertain scope

The weak-mixing result supports kinetic limitation, but only one weak condition was tested. It could alternatively reflect a threshold mixing failure, transient emulsion behavior, or another mixing-sensitive process rather than a smooth mass-transfer law. Likewise, the phase-volume series has no replication and its observed differences are near instrumental uncertainty, so it supports “no large effect in this range,” not volume independence. The elevated impurity after aqueous retention may reflect true impurity partition, but concentration/dilution or final-assay basis effects remain possible contributors.

Only nine distinct material pairs were sampled, with most pairs unreplicated; the full 4×4 interaction surface is therefore unidentified. Material effects, extractant-volume effects and broader solvent/aqueous ratios were not independently mapped, and settling duration was fixed. The anonymous synthetic materials have no warranted real-chemical interpretation. Consequently, the account is predictive only within this benchmark, near the tested volumes, reagent loading, 300 s settling time and mixing regimes.

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
        "estimate": 0.77,
        "lower90": 0.66,
        "upper90": 0.86
      },
      "product_in_organic": {
        "estimate": 0.23,
        "lower90": 0.14,
        "upper90": 0.34
      },
      "query_id": "Q01"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.47,
        "lower90": 0.37,
        "upper90": 0.57
      },
      "product_in_organic": {
        "estimate": 0.53,
        "lower90": 0.43,
        "upper90": 0.63
      },
      "query_id": "Q02"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.53,
        "lower90": 0.42,
        "upper90": 0.64
      },
      "product_in_organic": {
        "estimate": 0.47,
        "lower90": 0.36,
        "upper90": 0.58
      },
      "query_id": "Q03"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.23,
        "lower90": 0.16,
        "upper90": 0.32
      },
      "product_in_organic": {
        "estimate": 0.77,
        "lower90": 0.68,
        "upper90": 0.84
      },
      "query_id": "Q04"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.49,
        "lower90": 0.4,
        "upper90": 0.58
      },
      "product_in_organic": {
        "estimate": 0.51,
        "lower90": 0.42,
        "upper90": 0.6
      },
      "query_id": "Q05"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.25,
        "lower90": 0.18,
        "upper90": 0.34
      },
      "product_in_organic": {
        "estimate": 0.75,
        "lower90": 0.66,
        "upper90": 0.82
      },
      "query_id": "Q06"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.3,
        "lower90": 0.22,
        "upper90": 0.39
      },
      "product_in_organic": {
        "estimate": 0.7,
        "lower90": 0.61,
        "upper90": 0.78
      },
      "query_id": "Q07"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.24,
        "lower90": 0.14,
        "upper90": 0.4
      },
      "product_in_organic": {
        "estimate": 0.76,
        "lower90": 0.6,
        "upper90": 0.86
      },
      "query_id": "Q08"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.53,
        "lower90": 0.42,
        "upper90": 0.64
      },
      "product_in_organic": {
        "estimate": 0.47,
        "lower90": 0.36,
        "upper90": 0.58
      },
      "query_id": "Q09"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.49,
        "lower90": 0.4,
        "upper90": 0.58
      },
      "product_in_organic": {
        "estimate": 0.51,
        "lower90": 0.42,
        "upper90": 0.6
      },
      "query_id": "Q10"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.28,
        "lower90": 0.16,
        "upper90": 0.46
      },
      "product_in_organic": {
        "estimate": 0.72,
        "lower90": 0.54,
        "upper90": 0.84
      },
      "query_id": "Q11"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.24,
        "lower90": 0.13,
        "upper90": 0.4
      },
      "product_in_organic": {
        "estimate": 0.76,
        "lower90": 0.6,
        "upper90": 0.87
      },
      "query_id": "Q12"
    }
  ],
  "rationale": "I treated the aqueous and organic values as complementary fractions of the fixed initial target inventory. Estimates combine the measured pair-specific partitioning with the extractant share of total added liquid; the strong-mixing cases are treated as near equilibrium, while shorter or slower mixing is allowed to retain more target aqueous. S0–X0 at Q01's low extractant fraction is therefore aqueous-majority, and replacing X0 with X3 at otherwise identical Q05/Q06 conditions raises the predicted organic fraction. Intervals widen for the unmeasured S2–X3 pairing and for mixing extrapolations."
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

1. The most likely wrong or still-untested self-developed law is the quantitative rule used in the sealed predictions: treating the extractant share of total added liquid as the organic-phase fraction and combining it with a fixed pair-specific equilibrium coefficient. The campaign never varied extractant volume or total added volume: batches 9–11 kept extractant at 0.020 L and total liquid additions at 0.100 L while only exchanging solvent and aqueous amounts. They therefore could not validate the large effects predicted for 0.008–0.030 L extractant. Likewise, S2–X3 was never tested. No instance-specific prior was supplied; the supplied material dossier contained only marginal nominal summaries and explicitly withheld pair interactions, volume response and mixing response.

2. I would run S0–X0 with the same 0.100 L total addition and the same 300 s/600 rpm mixing and 300 s settling as batch 1, but increase extractant from 0.020 to 0.050 L while keeping solvent at 0.040 L and reducing added aqueous liquid to 0.010 L. I would measure pre-separation HPLC phase ratio and both target fractions. The prediction law implies a phase ratio near 0.50 and, using batch 1’s inferred distribution behavior, an organic target fraction around 0.65 rather than batch 1’s roughly 0.32. Such a joint shift would support the volume-fraction/equilibrium account. A phase ratio and organic fraction remaining near batch 1 would favor a fixed or pre-existing phase-inventory explanation. A changed phase ratio without the corresponding target shift would indicate that the distribution coefficient, mixing efficiency, or phase composition is coupled to the amounts, invalidating the simple law.

3. Underused evidence included the raw chromatographic peaks and uncertainty packets, the pre/post-separation differences between HPLC and final assay, and the dossier’s impurity/selectivity marginals. Those data could have been used to check systematic measurement offsets and constrain uncertainty, rather than relying mainly on processed target channels. The explicit instrument uncertainties were also not formally propagated; the sealed intervals were judgmental.

The least reliable predictions are Q08, Q11 and Q12 because they require the entirely unmeasured S2–X3 interaction, with Q11 and Q12 additionally extrapolating mixing-speed behavior from only batches 9 and 12. Q01–Q04 are also weak because their extractant fractions lie outside the experimental design. Q09 is uncertain because no mixing-response curve was measured between the single weak condition and the standard condition. The Q05-versus-Q06 ordering is comparatively better supported by the large S0–X3 versus S0–X0 difference in batches 4 and 1, although its magnitude remains volume-dependent. The Q01 aqueous-retention decision is plausible but still rests on the untested dose law.

There is a real tension between the sealed report and sealed predictions. The report correctly said that batches 9–11 resolved no phase-amount effect and supported only ‘no large effect in this range,’ yet the predictions imposed a specific volume law and gave fairly narrow intervals for substantial extractant-volume effects. The report also emphasized that one weak-mixing batch could not distinguish a smooth kinetic law from a threshold or emulsion effect, whereas the predictions assumed a monotonic approach to equilibrium for Q09–Q12. Finally, the report stressed pair interactions, but the S2–X3 predictions necessarily leaned on marginal tendencies despite lacking a direct pair measurement. These are retrospective limitations of the sealed outputs, not revisions to them.

## Evaluation and resource use

```json
{
  "arm": "Aligned",
  "budget": 12,
  "goal": "discovery",
  "locus": "E",
  "system": "PA",
  "unit_id": "PA-W02-B12-discovery-E-Aligned",
  "world": {
    "world_id": "PA-W02",
    "world_interventions": [
      {
        "axis_id": "partition.distribution-coefficient",
        "mode": "extrapolation",
        "severity": 0.75
      }
    ],
    "world_seed": 1
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
        "absolute_error": 0.04308823152771654,
        "estimate": 0.23,
        "lower90": 0.14,
        "metric": "product_in_organic",
        "query_id": "Q01",
        "truth": 0.27308823152771655,
        "upper90": 0.34
      },
      {
        "absolute_error": 0.04701273840193332,
        "estimate": 0.53,
        "lower90": 0.43,
        "metric": "product_in_organic",
        "query_id": "Q02",
        "truth": 0.5770127384019333,
        "upper90": 0.63
      },
      {
        "absolute_error": 0.06698108967949434,
        "estimate": 0.47,
        "lower90": 0.36,
        "metric": "product_in_organic",
        "query_id": "Q03",
        "truth": 0.5369810896794943,
        "upper90": 0.58
      },
      {
        "absolute_error": 0.027968648023910747,
        "estimate": 0.77,
        "lower90": 0.68,
        "metric": "product_in_organic",
        "query_id": "Q04",
        "truth": 0.7979686480239108,
        "upper90": 0.84
      },
      {
        "absolute_error": 0.04343651456511233,
        "estimate": 0.51,
        "lower90": 0.42,
        "metric": "product_in_organic",
        "query_id": "Q05",
        "truth": 0.5534365145651123,
        "upper90": 0.6
      },
      {
        "absolute_error": 0.03339443887333049,
        "estimate": 0.75,
        "lower90": 0.66,
        "metric": "product_in_organic",
        "query_id": "Q06",
        "truth": 0.7833944388733305,
        "upper90": 0.82
      },
      {
        "absolute_error": 0.056203244957912624,
        "estimate": 0.7,
        "lower90": 0.61,
        "metric": "product_in_organic",
        "query_id": "Q07",
        "truth": 0.7562032449579126,
        "upper90": 0.78
      },
      {
        "absolute_error": 0.01072546653056905,
        "estimate": 0.76,
        "lower90": 0.6,
        "metric": "product_in_organic",
        "query_id": "Q08",
        "truth": 0.7707254665305691,
        "upper90": 0.86
      },
      {
        "absolute_error": 0.035290114105165804,
        "estimate": 0.47,
        "lower90": 0.36,
        "metric": "product_in_organic",
        "query_id": "Q09",
        "truth": 0.43470988589483417,
        "upper90": 0.58
      },
      {
        "absolute_error": 0.02556274829502969,
        "estimate": 0.51,
        "lower90": 0.42,
        "metric": "product_in_organic",
        "query_id": "Q10",
        "truth": 0.5355627482950297,
        "upper90": 0.6
      },
      {
        "absolute_error": 0.007332997327959223,
        "estimate": 0.72,
        "lower90": 0.54,
        "metric": "product_in_organic",
        "query_id": "Q11",
        "truth": 0.7126670026720408,
        "upper90": 0.84
      },
      {
        "absolute_error": 0.0028722581280150594,
        "estimate": 0.76,
        "lower90": 0.6,
        "metric": "product_in_organic",
        "query_id": "Q12",
        "truth": 0.757127741871985,
        "upper90": 0.87
      },
      {
        "absolute_error": 0.04308823152771657,
        "estimate": 0.77,
        "lower90": 0.66,
        "metric": "product_in_aqueous",
        "query_id": "Q01",
        "truth": 0.7269117684722834,
        "upper90": 0.86
      },
      {
        "absolute_error": 0.04701273840193332,
        "estimate": 0.47,
        "lower90": 0.37,
        "metric": "product_in_aqueous",
        "query_id": "Q02",
        "truth": 0.42298726159806666,
        "upper90": 0.57
      },
      {
        "absolute_error": 0.06698108967949434,
        "estimate": 0.53,
        "lower90": 0.42,
        "metric": "product_in_aqueous",
        "query_id": "Q03",
        "truth": 0.4630189103205057,
        "upper90": 0.64
      },
      {
        "absolute_error": 0.02796864802391083,
        "estimate": 0.23,
        "lower90": 0.16,
        "metric": "product_in_aqueous",
        "query_id": "Q04",
        "truth": 0.20203135197608918,
        "upper90": 0.32
      },
      {
        "absolute_error": 0.04343651456511238,
        "estimate": 0.49,
        "lower90": 0.4,
        "metric": "product_in_aqueous",
        "query_id": "Q05",
        "truth": 0.4465634854348876,
        "upper90": 0.58
      },
      {
        "absolute_error": 0.03339443887333049,
        "estimate": 0.25,
        "lower90": 0.18,
        "metric": "product_in_aqueous",
        "query_id": "Q06",
        "truth": 0.2166055611266695,
        "upper90": 0.34
      },
      {
        "absolute_error": 0.056203244957912624,
        "estimate": 0.3,
        "lower90": 0.22,
        "metric": "product_in_aqueous",
        "query_id": "Q07",
        "truth": 0.24379675504208737,
        "upper90": 0.39
      },
      {
        "absolute_error": 0.010725466530569105,
        "estimate": 0.24,
        "lower90": 0.14,
        "metric": "product_in_aqueous",
        "query_id": "Q08",
        "truth": 0.22927453346943089,
        "upper90": 0.4
      },
      {
        "absolute_error": 0.035290114105165804,
        "estimate": 0.53,
        "lower90": 0.42,
        "metric": "product_in_aqueous",
        "query_id": "Q09",
        "truth": 0.5652901141051658,
        "upper90": 0.64
      },
      {
        "absolute_error": 0.02556274829502969,
        "estimate": 0.49,
        "lower90": 0.4,
        "metric": "product_in_aqueous",
        "query_id": "Q10",
        "truth": 0.4644372517049703,
        "upper90": 0.58
      },
      {
        "absolute_error": 0.007332997327959223,
        "estimate": 0.28,
        "lower90": 0.16,
        "metric": "product_in_aqueous",
        "query_id": "Q11",
        "truth": 0.28733299732795925,
        "upper90": 0.46
      },
      {
        "absolute_error": 0.0028722581280150317,
        "estimate": 0.24,
        "lower90": 0.13,
        "metric": "product_in_aqueous",
        "query_id": "Q12",
        "truth": 0.24287225812801502,
        "upper90": 0.4
      }
    ],
    "metrics": {
      "product_in_aqueous": {
        "coverage90": 1.0,
        "interval_score90": 0.21,
        "mae": 0.03332237420134578,
        "mean_width90": 0.21,
        "n": 12
      },
      "product_in_organic": {
        "coverage90": 1.0,
        "interval_score90": 0.20999999999999996,
        "mae": 0.03332237420134577,
        "mean_width90": 0.20999999999999996,
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
        "input": 486237,
        "cached_input": 450176,
        "output": 4480,
        "uncached_input": 36061
      },
      {
        "stage": "K1",
        "input": 67547,
        "cached_input": 32768,
        "output": 3204,
        "uncached_input": 34779
      },
      {
        "stage": "Q",
        "input": 348456,
        "cached_input": 297344,
        "output": 9589,
        "uncached_input": 51112
      },
      {
        "stage": "K2",
        "input": 51073,
        "cached_input": 34432,
        "output": 1794,
        "uncached_input": 16641
      }
    ],
    "total": {
      "input": 953313,
      "cached_input": 814720,
      "output": 19067,
      "uncached_input": 138593,
      "input_plus_output": 972380
    },
    "monetary_cost_usd": null
  },
  "elapsed_s": 622.9369999999981,
  "retest_batches": 0,
  "retest_operations": 0,
  "retest_replay": null,
  "english_output": true
}
```
