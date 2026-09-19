# PA-W03-B12-discovery-E-Opaque

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
| 1 | {"cost": 0.41635000705718994, "impurity_signal": 0.001631465507671237, "phase_ratio": 1.0, "product_in_aqueous": 0.014660237357020378, "product_in_organic": 0.17268779873847961, "purity": 0.9512932300567627, "recovery": 0.18245895206928253, "safety_risk": 0.040138129144907, "score": 0.0453186072409153} |
| 2 | {"cost": 0.41635000705718994, "impurity_signal": 0.10539953410625458, "phase_ratio": 0.0, "product_in_aqueous": 0.6621577143669128, "product_in_organic": 0.008452002890408039, "purity": 0.8515135049819946, "recovery": 0.6339161396026611, "safety_risk": 0.057486604899168015, "score": 0.0} |
| 3 | {"cost": 0.41635000705718994, "impurity_signal": 0.0, "phase_ratio": 0.96914142370224, "product_in_aqueous": 0.0, "product_in_organic": 0.25865140557289124, "purity": 0.959822952747345, "recovery": 0.24416960775852203, "safety_risk": 0.0427095890045166, "score": 0.12293955683708191} |
| 4 | {"cost": 0.41635000705718994, "impurity_signal": 0.13580533862113953, "phase_ratio": 0.009506937116384506, "product_in_aqueous": 0.6161887049674988, "product_in_organic": 0.0, "purity": 0.844547688961029, "recovery": 0.6046163439750671, "safety_risk": 0.057031478732824326, "score": 0.0} |
| 5 | {"cost": 0.4323500096797943, "impurity_signal": 0.015565636567771435, "phase_ratio": 0.9829117059707642, "product_in_aqueous": 0.0, "product_in_organic": 0.3178023099899292, "purity": 0.9620992541313171, "recovery": 0.3146393299102783, "safety_risk": 0.06862150877714157, "score": 0.17184078693389893} |
| 6 | {"cost": 0.45794999599456787, "impurity_signal": 0.1280941367149353, "phase_ratio": 0.0, "product_in_aqueous": 0.6698896288871765, "product_in_organic": 0.0, "purity": 0.8402990698814392, "recovery": 0.6549468040466309, "safety_risk": 0.09912977367639542, "score": 0.0} |
| 7 | {"cost": 0.4419499933719635, "impurity_signal": 0.003477103542536497, "phase_ratio": 1.0, "product_in_aqueous": 0.007889077998697758, "product_in_organic": 0.2871590256690979, "purity": 0.9717639684677124, "recovery": 0.2854830026626587, "safety_risk": 0.09793778508901596, "score": 0.1432962715625763} |
| 8 | {"cost": 0.4265500009059906, "impurity_signal": 0.11685825139284134, "phase_ratio": 0.0, "product_in_aqueous": 0.8240285515785217, "product_in_organic": 0.0, "purity": 0.8538987636566162, "recovery": 0.8014545440673828, "safety_risk": 0.08390036225318909, "score": 0.0} |
| 9 | {"cost": 0.43814998865127563, "impurity_signal": 0.00917319767177105, "phase_ratio": 1.0, "product_in_aqueous": 0.0, "product_in_organic": 0.1978033483028412, "purity": 0.9727380871772766, "recovery": 0.21405459940433502, "safety_risk": 0.06446769833564758, "score": 0.06813284754753113} |
| 10 | {"cost": 0.45682498812675476, "impurity_signal": 0.13133622705936432, "phase_ratio": 0.015568170696496964, "product_in_aqueous": 0.8210539221763611, "product_in_organic": 0.005932251922786236, "purity": 0.8775498270988464, "recovery": 0.8340364694595337, "safety_risk": 0.10243894159793854, "score": 0.0} |
| 11 | {"cost": 0.4616999924182892, "impurity_signal": 0.021954474970698357, "phase_ratio": 1.0, "product_in_aqueous": 0.0, "product_in_organic": 0.2731524109840393, "purity": 0.9755328893661499, "recovery": 0.27121156454086304, "safety_risk": 0.08473006635904312, "score": 0.13217954337596893} |
| 12 | {"cost": 0.4419499933719635, "impurity_signal": 0.12053269147872925, "phase_ratio": 0.0, "product_in_aqueous": 0.7906625866889954, "product_in_organic": 0.003923420328646898, "purity": 0.8631640076637268, "recovery": 0.7967163324356079, "safety_risk": 0.11427796632051468, "score": 0.0} |

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

Observations: Before phase separation, every HPLC measurement placed more target in the aqueous phase than in the organic phase. A descriptive organic share, computed as organic/(organic+aqueous), ranged from about 0.16 to 0.40. Material choice mattered strongly. With solvent S0 under common volumes and mixing, changing extractant from X0 to X1, X2, and X3 changed the organic target signal from 0.152 (batch 1) to 0.368, 0.227, and 0.391 (batches 2–4). With X0 fixed, changing S0 to S1, S2, or S3 raised the organic signal from 0.152 to 0.313, 0.328, and 0.290 (batches 1 and 5–7). Thus S0–X0 was the most aqueous-favoring tested baseline pairing, while S0–X3 and S0–X1 produced the largest organic shares among the common-condition tests.

The phase-amount comparison used the same S1–X1 materials and mixing. Batch 8 used 0.02 L solvent and 0.06 L aqueous addition; batch 9 reversed those amounts. Their HPLC results were similar: organic target 0.198 versus 0.213 and aqueous target 0.778 versus 0.768. These differences are comparable to the declared HPLC uncertainty, so this experiment did not establish a substantial phase-amount effect for S1–X1 over that tested range.

Mixing produced a larger contrast for S2–X2. At 30 s and 200 rpm, batch 10 measured aqueous/organic target signals of 0.807/0.204. At 1200 s and 1000 rpm, batch 11 measured 0.695/0.298. The shift is much larger than the stated per-channel HPLC uncertainty, although duration and speed were changed together and neither condition was replicated.

Phase-retention assays independently checked where the target went. Organic-retained batches 1, 3, 5, 7, 9, and 11 gave final organic target values broadly consistent with their pre-separation organic signals. Aqueous-retained batches 2, 4, 6, 8, 10, and 12 likewise preserved approximately the pre-separation aqueous signal. Across these two groups, final assays averaged about 0.252 recovery, 0.966 purity, and 0.009 impurity signal after retaining organic, versus 0.721 recovery, 0.855 purity, and 0.123 impurity signal after retaining aqueous. The final phase ratios near one or zero chiefly encode which single phase was retained, rather than a new equilibrium measurement.

Inference: The primary behavior is aqueous-favored target partition with a material-pair-dependent organic transfer fraction. Neither solvent nor extractant should be assigned one universal rank: X1 and X3 performed well with S0, yet S1–X1 remained relatively aqueous-favoring in both volume configurations, and S3–X3 was less organic-favoring than S0–X3. This suggests pairing interactions in addition to material main effects. The S2–X2 contrast further suggests that transfer can be mass-transfer-limited: stronger/longer mixing moved more target into the organic phase. Retaining aqueous maximizes target recovery under all tested conditions, while retaining organic sacrifices recovery but yields a cleaner target-bearing fraction. The impurity therefore appears to prefer, or at least be measured more strongly in, the aqueous retained fraction.

Contribution of supplied information: The public material catalog supplied only anonymous identifiers and explicitly stated that equal solvent and extractant indices imply no shared identity or property. It therefore prevented unsupported chemical-property stories; all rankings above come from experiments. The instrument contracts supplied channel definitions, calibration status, uncertainty scales, and the fact that this is a bounded synthetic benchmark. Those details justify comparing changes with measurement uncertainty but do not reveal a molecular mechanism. The twelve experiments supplied the actual evidence: a common-condition S0 extractant series, an X0 solvent series, one controlled phase-amount contrast, one extreme mixing contrast, additional diagonal pairings, and alternating retained-phase confirmations.

Conjecture and competing explanations: A plausible account is equilibrium pairing selectivity overlaid by mixing-dependent approach to equilibrium, with an aqueous-preferring impurity. However, the apparent mixing effect could instead include unobserved batch variability, dispersion or sampling effects, because speed and duration were bundled and there were no replicates. Apparent pairing interactions are not cleanly separated from process variables for every diagonal pair; the full 4×4 material matrix was not measured. The weak volume result is established only for S1–X1 and cannot be generalized to all materials or more extreme ratios. Phase-dependent detector response or matrix effects could contribute to the purity and impurity contrast despite the declared calibrations. Extractant amount, reagent loading, and settling time were not independently varied, so saturation, loading, incomplete settling, and true distribution coefficients remain unresolved. Finally, the anonymous synthetic materials support predictions only inside this benchmark; no real-solvent identity, polarity, ionization mechanism, or real-world extraction behavior can be inferred.

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
        "estimate": 0.88,
        "lower90": 0.77,
        "upper90": 0.95
      },
      "product_in_organic": {
        "estimate": 0.12,
        "lower90": 0.05,
        "upper90": 0.23
      },
      "query_id": "Q01"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.76,
        "lower90": 0.61,
        "upper90": 0.89
      },
      "product_in_organic": {
        "estimate": 0.24,
        "lower90": 0.11,
        "upper90": 0.39
      },
      "query_id": "Q02"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.73,
        "lower90": 0.56,
        "upper90": 0.88
      },
      "product_in_organic": {
        "estimate": 0.27,
        "lower90": 0.12,
        "upper90": 0.44
      },
      "query_id": "Q03"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.5,
        "lower90": 0.32,
        "upper90": 0.7
      },
      "product_in_organic": {
        "estimate": 0.5,
        "lower90": 0.3,
        "upper90": 0.68
      },
      "query_id": "Q04"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.8,
        "lower90": 0.68,
        "upper90": 0.9
      },
      "product_in_organic": {
        "estimate": 0.2,
        "lower90": 0.1,
        "upper90": 0.32
      },
      "query_id": "Q05"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.56,
        "lower90": 0.41,
        "upper90": 0.71
      },
      "product_in_organic": {
        "estimate": 0.44,
        "lower90": 0.29,
        "upper90": 0.59
      },
      "query_id": "Q06"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.62,
        "lower90": 0.48,
        "upper90": 0.76
      },
      "product_in_organic": {
        "estimate": 0.38,
        "lower90": 0.24,
        "upper90": 0.52
      },
      "query_id": "Q07"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.39,
        "lower90": 0.22,
        "upper90": 0.61
      },
      "product_in_organic": {
        "estimate": 0.61,
        "lower90": 0.39,
        "upper90": 0.78
      },
      "query_id": "Q08"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.83,
        "lower90": 0.71,
        "upper90": 0.92
      },
      "product_in_organic": {
        "estimate": 0.17,
        "lower90": 0.08,
        "upper90": 0.29
      },
      "query_id": "Q09"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.8,
        "lower90": 0.67,
        "upper90": 0.9
      },
      "product_in_organic": {
        "estimate": 0.2,
        "lower90": 0.1,
        "upper90": 0.33
      },
      "query_id": "Q10"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.44,
        "lower90": 0.25,
        "upper90": 0.66
      },
      "product_in_organic": {
        "estimate": 0.56,
        "lower90": 0.34,
        "upper90": 0.75
      },
      "query_id": "Q11"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.39,
        "lower90": 0.21,
        "upper90": 0.62
      },
      "product_in_organic": {
        "estimate": 0.61,
        "lower90": 0.38,
        "upper90": 0.79
      },
      "query_id": "Q12"
    }
  ],
  "rationale": "All campaign HPLC results favored the aqueous phase for S0–X0, so Q01 should retain aqueous. With S0 fixed, X3 transferred substantially more target to organic than X0, making Q06 higher than Q05. Estimates otherwise extrapolate the observed material-pair ranking, a likely increase with extractant amount, and the observed benefit of stronger or longer mixing; intervals are wider for unmeasured extractant amounts and the unseen S2–X3 pairing and exclude random HPLC noise."
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

1. Most likely wrong or untested claim

No instance prior, nominal property dossier, or real-material mechanism was supplied. The supplied catalog only said that the anonymous solvent and extractant labels are independent and that equal indices have no intrinsic meaning. I have no evidence that this supplied claim is wrong.

The weakest self-developed assumption is the monotonic extractant-amount effect used in the predictions. Every campaign batch used 0.020 L extractant, so the increases or decreases predicted at 0.008, 0.019, and 0.030 L were untested extrapolations. The related assumption that separately favorable material effects can be combined for the unseen S2–X3 pair is also weak: batches 2–4 established extractant differences only with S0, while batches 5–7 established solvent differences only with X0. The unexpectedly aqueous-favoring diagonal pairs in batches 8–12 already warn against a simple additive law. Finally, batches 10 and 11 changed mixing time and speed simultaneously, so they did not establish separate laws for either variable.

2. One additional experiment

I would run a within-batch extractant-dose challenge with S0–X0, because it directly tests the largest unsupported step behind Q01 versus Q02. I would use Q01's solvent and aqueous amounts, add 0.008 L X0, mix for 900 s at 1200 rpm, settle for 300 s, and obtain a pre-separation HPLC measurement of both target fractions. I would then add enough X0 to bring the total to 0.030 L, repeat exactly the same mixing and settling, and take a second pre-separation HPLC measurement. The small first sample loss would be included in the inventory accounting.

A clear organic-fraction increase substantially exceeding combined measurement uncertainty would support the assumed positive dose response and make Q02-like extrapolation more credible. Little or no change would favor the alternative that the tested volume range mainly changes bulk phase amount without materially changing partition, consistent with the weak phase-amount contrast in batches 8 and 9. A decrease would overturn the monotonic assumption and suggest dilution, aggregation, phase-composition, or loading effects. This experiment would not resolve the separate uncertainty about S2–X3 compatibility.

3. Underused evidence, weak predictions, and consistency audit

The narrow HPLC phase-ratio range across the campaign was underused. Together with the small difference between batches 8 and 9, it could have justified a more conservative treatment of added phase volumes. The retained-phase final assays were also used mainly qualitatively; their agreement with the corresponding pre-separation HPLC channel could have been used more explicitly to constrain systematic phase-dependent bias. Conversely, terminal phase ratios of approximately zero or one should not be treated as equilibrium evidence because they followed phase removal.

Q08, Q11, and Q12 are the least reliable predictions because S2–X3 was never observed; their organic-majority point estimates relied on combining effects learned from different rows and columns of an incomplete pairing matrix. Q01–Q04 are also weak in magnitude because their extractant doses differ most from the sole tested dose. Q09 versus Q10 and Q11 versus Q12 are uncertain because the campaign's only mixing contrast, batches 10 and 11, bundled duration with speed and was performed on S2–X2 without replication. The Q01 aqueous-retention decision and the directional Q06-over-Q05 decision are comparatively better supported by batches 1 and 4, respectively, although their exact fractions remain uncertain.

There is no direct numerical contradiction between the sealed report and predictions, but there is a real inconsistency in evidential caution. The report said that phase-amount dependence was not established and that material ranks should not be assumed universal, yet the predictions imposed a positive extractant-dose trend and predicted organic-majority behavior for unmeasured S2–X3. Those were prospective extrapolations rather than findings from the campaign, and the prediction rationale should have emphasized their speculative status more strongly. This is a retrospective audit of the sealed outputs, not a modification of them, and no outcome truth has been used.

## Evaluation and resource use

```json
{
  "arm": "Opaque",
  "budget": 12,
  "goal": "discovery",
  "locus": "E",
  "system": "PA",
  "unit_id": "PA-W03-B12-discovery-E-Opaque",
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
    "valid": true,
    "metrics": {
      "product_in_organic": {
        "n": 12,
        "mae": 0.09831843746337725,
        "coverage90": 0.6666666666666666,
        "mean_width90": 0.30083333333333334,
        "interval_score90": 0.5430761672767931
      },
      "product_in_aqueous": {
        "n": 12,
        "mae": 0.09831843746337726,
        "coverage90": 0.6666666666666666,
        "mean_width90": 0.30083333333333334,
        "interval_score90": 0.5430761672767933
      }
    },
    "details": [
      {
        "query_id": "Q01",
        "metric": "product_in_organic",
        "estimate": 0.12,
        "lower90": 0.05,
        "upper90": 0.23,
        "truth": 0.14028028852564417,
        "absolute_error": 0.020280288525644175
      },
      {
        "query_id": "Q02",
        "metric": "product_in_organic",
        "estimate": 0.24,
        "lower90": 0.11,
        "upper90": 0.39,
        "truth": 0.37628859799060643,
        "absolute_error": 0.13628859799060644
      },
      {
        "query_id": "Q03",
        "metric": "product_in_organic",
        "estimate": 0.27,
        "lower90": 0.12,
        "upper90": 0.44,
        "truth": 0.33817705508866275,
        "absolute_error": 0.06817705508866273
      },
      {
        "query_id": "Q04",
        "metric": "product_in_organic",
        "estimate": 0.5,
        "lower90": 0.3,
        "upper90": 0.68,
        "truth": 0.6471988475728407,
        "absolute_error": 0.14719884757284074
      },
      {
        "query_id": "Q05",
        "metric": "product_in_organic",
        "estimate": 0.2,
        "lower90": 0.1,
        "upper90": 0.32,
        "truth": 0.35352236193438064,
        "absolute_error": 0.15352236193438062
      },
      {
        "query_id": "Q06",
        "metric": "product_in_organic",
        "estimate": 0.44,
        "lower90": 0.29,
        "upper90": 0.59,
        "truth": 0.6253264948801845,
        "absolute_error": 0.18532649488018454
      },
      {
        "query_id": "Q07",
        "metric": "product_in_organic",
        "estimate": 0.38,
        "lower90": 0.24,
        "upper90": 0.52,
        "truth": 0.5863161160362313,
        "absolute_error": 0.20631611603623135
      },
      {
        "query_id": "Q08",
        "metric": "product_in_organic",
        "estimate": 0.61,
        "lower90": 0.39,
        "upper90": 0.78,
        "truth": 0.6068680731369908,
        "absolute_error": 0.0031319268630092267
      },
      {
        "query_id": "Q09",
        "metric": "product_in_organic",
        "estimate": 0.17,
        "lower90": 0.08,
        "upper90": 0.29,
        "truth": 0.26801669600322914,
        "absolute_error": 0.09801669600322913
      },
      {
        "query_id": "Q10",
        "metric": "product_in_organic",
        "estimate": 0.2,
        "lower90": 0.1,
        "upper90": 0.33,
        "truth": 0.34018072751527934,
        "absolute_error": 0.14018072751527932
      },
      {
        "query_id": "Q11",
        "metric": "product_in_organic",
        "estimate": 0.56,
        "lower90": 0.34,
        "upper90": 0.75,
        "truth": 0.5539547895844652,
        "absolute_error": 0.006045210415534852
      },
      {
        "query_id": "Q12",
        "metric": "product_in_organic",
        "estimate": 0.61,
        "lower90": 0.38,
        "upper90": 0.79,
        "truth": 0.5946630732650762,
        "absolute_error": 0.015336926734923817
      },
      {
        "query_id": "Q01",
        "metric": "product_in_aqueous",
        "estimate": 0.88,
        "lower90": 0.77,
        "upper90": 0.95,
        "truth": 0.8597197114743559,
        "absolute_error": 0.02028028852564412
      },
      {
        "query_id": "Q02",
        "metric": "product_in_aqueous",
        "estimate": 0.76,
        "lower90": 0.61,
        "upper90": 0.89,
        "truth": 0.6237114020093936,
        "absolute_error": 0.13628859799060644
      },
      {
        "query_id": "Q03",
        "metric": "product_in_aqueous",
        "estimate": 0.73,
        "lower90": 0.56,
        "upper90": 0.88,
        "truth": 0.6618229449113372,
        "absolute_error": 0.06817705508866279
      },
      {
        "query_id": "Q04",
        "metric": "product_in_aqueous",
        "estimate": 0.5,
        "lower90": 0.32,
        "upper90": 0.7,
        "truth": 0.3528011524271592,
        "absolute_error": 0.1471988475728408
      },
      {
        "query_id": "Q05",
        "metric": "product_in_aqueous",
        "estimate": 0.8,
        "lower90": 0.68,
        "upper90": 0.9,
        "truth": 0.6464776380656193,
        "absolute_error": 0.15352236193438074
      },
      {
        "query_id": "Q06",
        "metric": "product_in_aqueous",
        "estimate": 0.56,
        "lower90": 0.41,
        "upper90": 0.71,
        "truth": 0.37467350511981545,
        "absolute_error": 0.1853264948801846
      },
      {
        "query_id": "Q07",
        "metric": "product_in_aqueous",
        "estimate": 0.62,
        "lower90": 0.48,
        "upper90": 0.76,
        "truth": 0.4136838839637687,
        "absolute_error": 0.2063161160362313
      },
      {
        "query_id": "Q08",
        "metric": "product_in_aqueous",
        "estimate": 0.39,
        "lower90": 0.22,
        "upper90": 0.61,
        "truth": 0.39313192686300924,
        "absolute_error": 0.0031319268630092267
      },
      {
        "query_id": "Q09",
        "metric": "product_in_aqueous",
        "estimate": 0.83,
        "lower90": 0.71,
        "upper90": 0.92,
        "truth": 0.7319833039967709,
        "absolute_error": 0.09801669600322904
      },
      {
        "query_id": "Q10",
        "metric": "product_in_aqueous",
        "estimate": 0.8,
        "lower90": 0.67,
        "upper90": 0.9,
        "truth": 0.6598192724847206,
        "absolute_error": 0.14018072751527944
      },
      {
        "query_id": "Q11",
        "metric": "product_in_aqueous",
        "estimate": 0.44,
        "lower90": 0.25,
        "upper90": 0.66,
        "truth": 0.4460452104155348,
        "absolute_error": 0.006045210415534796
      },
      {
        "query_id": "Q12",
        "metric": "product_in_aqueous",
        "estimate": 0.39,
        "lower90": 0.21,
        "upper90": 0.62,
        "truth": 0.40533692673492383,
        "absolute_error": 0.015336926734923817
      }
    ],
    "decisions": {
      "D1": {
        "submitted": "aqueous",
        "truth": "aqueous",
        "correct": true
      },
      "D2": {
        "submitted": "Q06",
        "truth": "Q06",
        "correct": true
      }
    }
  },
  "token_accounting": {
    "valid": true,
    "complete": true,
    "basis": "cumulative thread snapshots differenced in source/K1/Q/K2 order",
    "stages": [
      {
        "stage": "source",
        "input": 941853,
        "cached_input": 895616,
        "output": 5357,
        "uncached_input": 46237
      },
      {
        "stage": "K1",
        "input": 131612,
        "cached_input": 44544,
        "output": 3084,
        "uncached_input": 87068
      },
      {
        "stage": "Q",
        "input": 50489,
        "cached_input": 0,
        "output": 4274,
        "uncached_input": 50489
      },
      {
        "stage": "K2",
        "input": 54766,
        "cached_input": 46848,
        "output": 2143,
        "uncached_input": 7918
      }
    ],
    "total": {
      "input": 1178720,
      "cached_input": 987008,
      "output": 14858,
      "uncached_input": 191712,
      "input_plus_output": 1193578
    },
    "monetary_cost_usd": null
  },
  "elapsed_s": 735.359999999997,
  "retest_batches": 0,
  "retest_operations": 0,
  "retest_replay": null,
  "english_output": true
}
```

## Infrastructure recovery

Original failed attempt is retained separately. Mode: posttests; new source batches: 0. See [recovery accounting](recovery.json).
