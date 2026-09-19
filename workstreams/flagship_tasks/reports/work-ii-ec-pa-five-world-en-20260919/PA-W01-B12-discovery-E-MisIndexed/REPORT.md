# PA-W01-B12-discovery-E-MisIndexed

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
| 1 | {"cost": 0.4501500129699707, "impurity_signal": 0.03513253107666969, "phase_ratio": 1.0, "product_in_aqueous": 0.014660237357020378, "product_in_organic": 0.5866897702217102, "purity": 0.9312151074409485, "recovery": 0.5964609384536743, "safety_risk": 0.08412608504295349, "score": 0.39722028374671936} |
| 2 | {"cost": 0.41894999146461487, "impurity_signal": 0.015166918747127056, "phase_ratio": 0.9997019171714783, "product_in_aqueous": 0.02075776644051075, "product_in_organic": 0.382332444190979, "purity": 0.9349101781845093, "recovery": 0.3663966655731201, "safety_risk": 0.03986183926463127, "score": 0.22293661534786224} |
| 3 | {"cost": 0.43094998598098755, "impurity_signal": 0.1621190905570984, "phase_ratio": 0.0, "product_in_aqueous": 0.43468785285949707, "product_in_organic": 0.005547169595956802, "purity": 0.714627742767334, "recovery": 0.43270108103752136, "safety_risk": 0.08541682362556458, "score": 0.0} |
| 4 | {"cost": 0.43814998865127563, "impurity_signal": 0.05104493349790573, "phase_ratio": 1.0, "product_in_aqueous": 0.0, "product_in_organic": 0.5172856450080872, "purity": 0.9449974298477173, "recovery": 0.513121485710144, "safety_risk": 0.09578393399715424, "score": 0.33969277143478394} |
| 5 | {"cost": 0.4501500129699707, "impurity_signal": 0.0419079065322876, "phase_ratio": 0.9829117059707642, "product_in_aqueous": 0.0, "product_in_organic": 0.5426892638206482, "purity": 0.9315674901008606, "recovery": 0.5395262837409973, "safety_risk": 0.08346161991357803, "score": 0.3629947006702423} |
| 6 | {"cost": 0.4501500129699707, "impurity_signal": 0.19464434683322906, "phase_ratio": 0.0, "product_in_aqueous": 0.5524793863296509, "product_in_organic": 0.0, "purity": 0.7374663949012756, "recovery": 0.5375365614891052, "safety_risk": 0.10534214973449707, "score": 0.0} |
| 7 | {"cost": 0.4501500129699707, "impurity_signal": 0.034649331122636795, "phase_ratio": 1.0, "product_in_aqueous": 0.007889077998697758, "product_in_organic": 0.6028368473052979, "purity": 0.9409188032150269, "recovery": 0.6011608242988586, "safety_risk": 0.0843692198395729, "score": 0.41162240505218506} |
| 8 | {"cost": 0.41894999146461487, "impurity_signal": 0.0390145480632782, "phase_ratio": 0.9789910912513733, "product_in_aqueous": 0.0284495260566473, "product_in_organic": 0.6078543663024902, "purity": 0.9187458753585815, "recovery": 0.6244845986366272, "safety_risk": 0.04330288618803024, "score": 0.4159321188926697} |
| 9 | {"cost": 0.43094998598098755, "impurity_signal": 0.17029066383838654, "phase_ratio": 0.011666297912597656, "product_in_aqueous": 0.3842002749443054, "product_in_organic": 0.0, "purity": 0.7082693576812744, "recovery": 0.4012357294559479, "safety_risk": 0.08446058630943298, "score": 0.0} |
| 10 | {"cost": 0.4489416778087616, "impurity_signal": 0.03374611213803291, "phase_ratio": 1.0, "product_in_aqueous": 0.0009292740724049509, "product_in_organic": 0.48669949173927307, "purity": 0.953380286693573, "recovery": 0.4946790337562561, "safety_risk": 0.08253734558820724, "score": 0.31360164284706116} |
| 11 | {"cost": 0.44339999556541443, "impurity_signal": 0.032125264406204224, "phase_ratio": 1.0, "product_in_aqueous": 0.0, "product_in_organic": 0.4086468517780304, "purity": 0.9621454477310181, "recovery": 0.4067060053348541, "safety_risk": 0.0878794714808464, "score": 0.247349813580513} |
| 12 | {"cost": 0.4569000005722046, "impurity_signal": 0.06707114726305008, "phase_ratio": 0.9891050457954407, "product_in_aqueous": 0.0054099163971841335, "product_in_organic": 0.7385397553443909, "purity": 0.9118756055831909, "recovery": 0.7460800409317017, "safety_risk": 0.08287498354911804, "score": 0.528307318687439} |

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

Observations: All comparisons used 0.020 mol reagent. Except for the deliberate volume and mixing tests, batches used 0.030 L solvent, 0.030 L aqueous phase, 0.030 L extractant, 300 s mixing at 600 rpm, and 600 s settling. The pre-separation HPLC measurements show that partition depended strongly on the solvent–extractant pair. With X0, changing solvent from S0 (batch 2) to S2 (batch 1) raised product_in_organic from 0.384 to 0.566 and lowered product_in_aqueous from 0.648 to 0.386. At fixed S2, X2 (batch 6) gave 0.445 organic/0.531 aqueous, whereas X3 (batch 7) gave 0.605/0.376. Crossed combinations were important: S0–X3 (batch 8) and S1–X2 (batch 9) both produced about 0.61–0.62 organic and 0.36 aqueous, despite S0–X0 and S2–X2 performing poorly. Thus neither solvent nor extractant has a universal ranking independent of its partner.

Phase amount had a large, directional effect for S2–X3. Reducing extractant to 0.015 L while increasing aqueous phase to 0.045 L (batch 11) produced phase_ratio 0.180 and 0.433 organic/0.559 aqueous. Equal 0.030 L amounts (batch 7) produced phase_ratio 0.326 and 0.605/0.376. Increasing extractant to 0.045 L while reducing aqueous phase to 0.015 L (batch 12) produced phase_ratio 0.495 and 0.760/0.265. The corresponding organic shares of measured target were approximately 0.437, 0.617, and 0.741. A concentration-ratio calculation using the measured phase ratios gives apparent distribution factors near 3.53, 3.33, and 2.92, respectively. Their rough similarity supports a volume-times-affinity account, although the spread shows that a single exact coefficient is not established.

Mixing affected approach to the high-organic state. For the same S2–X3 materials and equal phase amounts, short, slow mixing—10 s at 100 rpm in batch 10—gave 0.505 organic/0.506 aqueous, versus 0.605/0.376 after 300 s at 600 rpm in batch 7. Apparent distribution factor fell from about 3.33 to 1.92, and recovery from 0.578 to 0.474. This is consistent with incomplete mass transfer under weak mixing.

Phase-retention measurements validate how the pre-separation signals should be used. When the organic phase was retained, final-assay product_in_organic closely tracked the preceding HPLC value: 0.603 after 0.605 in batch 7, 0.608 after 0.612 in batch 8, and 0.739 after 0.760 in batch 12; product_in_aqueous was then near zero. Conversely, aqueous retention in batches 3, 6, and 9 yielded final aqueous product of 0.435, 0.552, and 0.384, with organic product near zero. Aqueous-retained samples also had much larger final impurity signals (0.162–0.195) and lower purities (0.708–0.737) than the organic-retained samples, which were generally around 0.03–0.07 impurity and 0.91–0.96 purity. Thus, under the tested conditions, retaining organic generally captures the target-rich and cleaner phase; retaining aqueous is appropriate only if the desired material is specifically the aqueous fraction.

Inference: The most economical account is a pair-specific equilibrium preference modified by phase capacity and by kinetic approach to equilibrium. The target usually favors the extractant-rich organic phase, but the magnitude of that preference is governed by solvent–extractant interactions rather than independent marginal rankings. Increasing organic-phase amount raises total organic capture even when the inferred concentration preference changes only moderately. Adequate mixing is required to realize that preference. Separation then physically selects the corresponding target inventory, while much of the impurity appears comparatively enriched in the aqueous retained fraction.

Contribution of supplied information: The nominal dossier correctly suggested that product distribution and selectivity could be favorable and identified S2 and X0 as promising marginal starting points. It was useful as a prior for the initial comparisons, but it explicitly lacked the interaction table and process response. The experiments supplied the decisive evidence: X3 was superior to X0 with S2, S0 became strong when paired with X3, and X2 became strong with S1. These reversals demonstrate why the marginal dossier alone could not predict pair performance. Experimental measurements were therefore treated as authoritative.

Competing explanations and uncertain scope: The volume series is compatible with a partition coefficient model, but changing extractant and aqueous amounts may also change concentration-dependent chemistry, recovery, or instrument response; the apparent factors of 2.92–3.53 are not identical. The mixing comparison changed duration and speed simultaneously, so it cannot distinguish contact time from agitation intensity; incomplete equilibrium, droplet-area limitations, or phase-sampling effects remain alternatives. The material matrix was sparse rather than a complete replicated 4×4 factorial design, so untested pair rankings remain uncertain and material main effects cannot be cleanly separated from interactions. Each condition had one process realization, although instrument uncertainties were much smaller than several observed contrasts. The phase_ratio channel was used as an empirical phase-volume proxy, not assumed to be an exact geometric volume fraction. Finally, the conclusions are best confined to 0.020 mol reagent, the tested 0.015–0.045 L phase amounts, 10–300 s/100–600 rpm mixing contrasts, and 600 s settling; behavior outside those ranges, at other reagent loadings, or after repeated extractions was not tested.

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
        "estimate": 0.841,
        "lower90": 0.76,
        "upper90": 0.9
      },
      "product_in_organic": {
        "estimate": 0.159,
        "lower90": 0.1,
        "upper90": 0.24
      },
      "query_id": "Q01"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.585,
        "lower90": 0.5,
        "upper90": 0.67
      },
      "product_in_organic": {
        "estimate": 0.415,
        "lower90": 0.33,
        "upper90": 0.5
      },
      "query_id": "Q02"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.65,
        "lower90": 0.55,
        "upper90": 0.74
      },
      "product_in_organic": {
        "estimate": 0.35,
        "lower90": 0.26,
        "upper90": 0.45
      },
      "query_id": "Q03"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.331,
        "lower90": 0.25,
        "upper90": 0.42
      },
      "product_in_organic": {
        "estimate": 0.669,
        "lower90": 0.58,
        "upper90": 0.75
      },
      "query_id": "Q04"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.61,
        "lower90": 0.52,
        "upper90": 0.7
      },
      "product_in_organic": {
        "estimate": 0.39,
        "lower90": 0.3,
        "upper90": 0.48
      },
      "query_id": "Q05"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.353,
        "lower90": 0.27,
        "upper90": 0.44
      },
      "product_in_organic": {
        "estimate": 0.647,
        "lower90": 0.56,
        "upper90": 0.73
      },
      "query_id": "Q06"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.386,
        "lower90": 0.3,
        "upper90": 0.48
      },
      "product_in_organic": {
        "estimate": 0.614,
        "lower90": 0.52,
        "upper90": 0.7
      },
      "query_id": "Q07"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.365,
        "lower90": 0.28,
        "upper90": 0.45
      },
      "product_in_organic": {
        "estimate": 0.635,
        "lower90": 0.55,
        "upper90": 0.72
      },
      "query_id": "Q08"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.635,
        "lower90": 0.54,
        "upper90": 0.73
      },
      "product_in_organic": {
        "estimate": 0.365,
        "lower90": 0.27,
        "upper90": 0.46
      },
      "query_id": "Q09"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.61,
        "lower90": 0.52,
        "upper90": 0.7
      },
      "product_in_organic": {
        "estimate": 0.39,
        "lower90": 0.3,
        "upper90": 0.48
      },
      "query_id": "Q10"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.38,
        "lower90": 0.3,
        "upper90": 0.48
      },
      "product_in_organic": {
        "estimate": 0.62,
        "lower90": 0.52,
        "upper90": 0.7
      },
      "query_id": "Q11"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.365,
        "lower90": 0.28,
        "upper90": 0.45
      },
      "product_in_organic": {
        "estimate": 0.635,
        "lower90": 0.55,
        "upper90": 0.72
      },
      "query_id": "Q12"
    }
  ],
  "rationale": "Predictions use pair-specific partition preferences inferred from the pre-separation campaign measurements, scaled by extractant versus solvent-plus-aqueous volume and reduced modestly where mixing may not fully equilibrate. S0–X0 favors aqueous at low extractant volume, while replacing X0 with X3 strongly increases organic partition; hence retain aqueous in Q01 and expect Q06 to exceed Q05 in organic target. Intervals reflect sparse pair coverage, volume extrapolation, and unresolved mixing kinetics, while excluding random HPLC noise; complementary fractions are constrained to sum to one."
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

1. No instance prior was supplied. The supplied dossier contained only marginal, panel-averaged material tendencies and explicitly withheld the pair-interaction and process laws. The least-tested self-developed law is therefore my approximation that each solvent–extractant pair has a nearly constant equilibrium distribution preference, with phase amounts acting mainly through capacity and mixing acting mainly through approach to equilibrium. Batches 7, 11, and 12 support that picture for S2–X3, but their inferred distribution factors were not identical. The claimed kinetic interpretation is also weakly identified: batches 7 and 10 changed both mixing duration and speed, so incomplete mass transfer cannot yet be separated from agitation-dependent phase structure, sampling, or chemistry. A universal ranking inferred from the supplied marginal dossier would be wrong: batches 2 versus 8 and 6 versus 9 show strong pairing reversals.

2. I would run one within-batch perturbation experiment using the well-characterized S2–X3 pair and the equal-volume recipe from batch 7. After weak mixing matching batch 10 (10 s, 100 rpm) and settling, I would take an HPLC sample and record organic target, aqueous target, phase ratio, recovery, impurity, and raw peak areas. Without removing either phase, I would then remix strongly—preferably 900 s at 1200 rpm—settle again, and repeat HPLC. A rise from the batch-10-like split toward the batch-7 organic fraction, with conserved total target and stable impurity, would strongly favor reversible mass-transfer limitation. Little movement after strong remixing would weaken that explanation and favor a persistent phase-state, sampling, or batch-specific effect. A change accompanied by loss of total target or altered impurity/purity would instead suggest mixing-dependent chemistry or degradation rather than partition kinetics alone.

3. The raw chromatographic artifacts and peak areas were underused; the analysis relied mainly on processed estimates. They could have tested mass balance and whether phase or mixing changes altered peak assignments. The paired pre-separation/final-assay evidence was used qualitatively but not incorporated quantitatively into uncertainty, and the dossier’s impurity/selectivity information was not formally modeled. The least reliable predictions are Q03, which extrapolates S0–X3 to very little extractant from only batch 8, and Q09–Q12, because their time/speed effects were extrapolated from a single confounded mixing contrast on S2–X3. Q01 and Q07 also extrapolate pair behavior to phase amounts not tested for those pairs. The qualitative D1 and D2 decisions are more secure than those absolute fractions: Q01 has low organic capacity with the weak S0–X0 pair, while batch 8 versus batch 2 strongly supports X3 over X0 with S0.

There is no direct logical contradiction between the sealed report and predictions: saying the target usually prefers the organic phase does not require the organic phase to contain more total target when it is very small, as in Q01. There is, however, a methodological tension. The report calculated apparent factors using measured phase-ratio estimates, whereas the predictions scaled pair preferences primarily with charged extractant versus solvent-plus-aqueous volumes. The report also left mixing kinetics unresolved, while the predictions assumed substantial saturation at longer or faster mixing and therefore predicted only modest Q09–Q12 differences. Those are contemporaneous modeling choices, not established results, and their uncertainty may be understated.

## Evaluation and resource use

```json
{
  "system": "PA",
  "world": {
    "world_id": "PA-W01",
    "world_seed": 0,
    "world_interventions": []
  },
  "goal": "discovery",
  "locus": "E",
  "arm": "MisIndexed",
  "budget": 12,
  "unit_id": "PA-W01-B12-discovery-E-MisIndexed",
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
        "absolute_error": 0.03941319904315638,
        "estimate": 0.159,
        "lower90": 0.1,
        "metric": "product_in_organic",
        "query_id": "Q01",
        "truth": 0.19841319904315638,
        "upper90": 0.24
      },
      {
        "absolute_error": 0.06106007721878304,
        "estimate": 0.415,
        "lower90": 0.33,
        "metric": "product_in_organic",
        "query_id": "Q02",
        "truth": 0.476060077218783,
        "upper90": 0.5
      },
      {
        "absolute_error": 0.08526070797039204,
        "estimate": 0.35,
        "lower90": 0.26,
        "metric": "product_in_organic",
        "query_id": "Q03",
        "truth": 0.435260707970392,
        "upper90": 0.45
      },
      {
        "absolute_error": 0.06133309192217473,
        "estimate": 0.669,
        "lower90": 0.58,
        "metric": "product_in_organic",
        "query_id": "Q04",
        "truth": 0.7303330919221748,
        "upper90": 0.75
      },
      {
        "absolute_error": 0.06185719230871395,
        "estimate": 0.39,
        "lower90": 0.3,
        "metric": "product_in_organic",
        "query_id": "Q05",
        "truth": 0.45185719230871396,
        "upper90": 0.48
      },
      {
        "absolute_error": 0.06486092033991842,
        "estimate": 0.647,
        "lower90": 0.56,
        "metric": "product_in_organic",
        "query_id": "Q06",
        "truth": 0.7118609203399184,
        "upper90": 0.73
      },
      {
        "absolute_error": 0.06409503730267652,
        "estimate": 0.614,
        "lower90": 0.52,
        "metric": "product_in_organic",
        "query_id": "Q07",
        "truth": 0.6780950373026765,
        "upper90": 0.7
      },
      {
        "absolute_error": 0.06101711838237933,
        "estimate": 0.635,
        "lower90": 0.55,
        "metric": "product_in_organic",
        "query_id": "Q08",
        "truth": 0.6960171183823793,
        "upper90": 0.72
      },
      {
        "absolute_error": 0.01646486462907698,
        "estimate": 0.365,
        "lower90": 0.27,
        "metric": "product_in_organic",
        "query_id": "Q09",
        "truth": 0.348535135370923,
        "upper90": 0.46
      },
      {
        "absolute_error": 0.04601083067532108,
        "estimate": 0.39,
        "lower90": 0.3,
        "metric": "product_in_organic",
        "query_id": "Q10",
        "truth": 0.4360108306753211,
        "upper90": 0.48
      },
      {
        "absolute_error": 0.019795960501287624,
        "estimate": 0.62,
        "lower90": 0.52,
        "metric": "product_in_organic",
        "query_id": "Q11",
        "truth": 0.6397959605012876,
        "upper90": 0.7
      },
      {
        "absolute_error": 0.04795297032789092,
        "estimate": 0.635,
        "lower90": 0.55,
        "metric": "product_in_organic",
        "query_id": "Q12",
        "truth": 0.6829529703278909,
        "upper90": 0.72
      },
      {
        "absolute_error": 0.03941319904315643,
        "estimate": 0.841,
        "lower90": 0.76,
        "metric": "product_in_aqueous",
        "query_id": "Q01",
        "truth": 0.8015868009568435,
        "upper90": 0.9
      },
      {
        "absolute_error": 0.06106007721878304,
        "estimate": 0.585,
        "lower90": 0.5,
        "metric": "product_in_aqueous",
        "query_id": "Q02",
        "truth": 0.5239399227812169,
        "upper90": 0.67
      },
      {
        "absolute_error": 0.08526070797039198,
        "estimate": 0.65,
        "lower90": 0.55,
        "metric": "product_in_aqueous",
        "query_id": "Q03",
        "truth": 0.564739292029608,
        "upper90": 0.74
      },
      {
        "absolute_error": 0.06133309192217479,
        "estimate": 0.331,
        "lower90": 0.25,
        "metric": "product_in_aqueous",
        "query_id": "Q04",
        "truth": 0.26966690807782523,
        "upper90": 0.42
      },
      {
        "absolute_error": 0.061857192308714004,
        "estimate": 0.61,
        "lower90": 0.52,
        "metric": "product_in_aqueous",
        "query_id": "Q05",
        "truth": 0.548142807691286,
        "upper90": 0.7
      },
      {
        "absolute_error": 0.06486092033991842,
        "estimate": 0.353,
        "lower90": 0.27,
        "metric": "product_in_aqueous",
        "query_id": "Q06",
        "truth": 0.28813907966008157,
        "upper90": 0.44
      },
      {
        "absolute_error": 0.06409503730267652,
        "estimate": 0.386,
        "lower90": 0.3,
        "metric": "product_in_aqueous",
        "query_id": "Q07",
        "truth": 0.3219049626973235,
        "upper90": 0.48
      },
      {
        "absolute_error": 0.06101711838237933,
        "estimate": 0.365,
        "lower90": 0.28,
        "metric": "product_in_aqueous",
        "query_id": "Q08",
        "truth": 0.30398288161762066,
        "upper90": 0.45
      },
      {
        "absolute_error": 0.016464864629076925,
        "estimate": 0.635,
        "lower90": 0.54,
        "metric": "product_in_aqueous",
        "query_id": "Q09",
        "truth": 0.6514648646290769,
        "upper90": 0.73
      },
      {
        "absolute_error": 0.04601083067532108,
        "estimate": 0.61,
        "lower90": 0.52,
        "metric": "product_in_aqueous",
        "query_id": "Q10",
        "truth": 0.5639891693246789,
        "upper90": 0.7
      },
      {
        "absolute_error": 0.019795960501287624,
        "estimate": 0.38,
        "lower90": 0.3,
        "metric": "product_in_aqueous",
        "query_id": "Q11",
        "truth": 0.3602040394987124,
        "upper90": 0.48
      },
      {
        "absolute_error": 0.04795297032789092,
        "estimate": 0.365,
        "lower90": 0.28,
        "metric": "product_in_aqueous",
        "query_id": "Q12",
        "truth": 0.31704702967210907,
        "upper90": 0.45
      }
    ],
    "metrics": {
      "product_in_aqueous": {
        "coverage90": 1.0,
        "interval_score90": 0.17416666666666666,
        "mae": 0.05242683088514758,
        "mean_width90": 0.17416666666666666,
        "n": 12
      },
      "product_in_organic": {
        "coverage90": 1.0,
        "interval_score90": 0.17416666666666666,
        "mae": 0.05242683088514758,
        "mean_width90": 0.17416666666666666,
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
        "input": 1128148,
        "cached_input": 1078016,
        "output": 5871,
        "uncached_input": 50132
      },
      {
        "stage": "K1",
        "input": 147172,
        "cached_input": 100224,
        "output": 3049,
        "uncached_input": 46948
      },
      {
        "stage": "Q",
        "input": 168029,
        "cached_input": 109952,
        "output": 4038,
        "uncached_input": 58077
      },
      {
        "stage": "K2",
        "input": 58906,
        "cached_input": 49920,
        "output": 1495,
        "uncached_input": 8986
      }
    ],
    "total": {
      "input": 1502255,
      "cached_input": 1338112,
      "output": 14453,
      "uncached_input": 164143,
      "input_plus_output": 1516708
    },
    "monetary_cost_usd": null
  },
  "elapsed_s": 541.109000000055,
  "retest_batches": 0,
  "retest_operations": 0,
  "retest_replay": null,
  "english_output": true
}
```
