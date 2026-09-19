# PA-W03-B12-discovery-E-MisIndexed

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
| 1 | {"cost": 0.47635000944137573, "impurity_signal": 0.001631465507671237, "phase_ratio": 1.0, "product_in_aqueous": 0.014660237357020378, "product_in_organic": 0.17268779873847961, "purity": 0.9512932300567627, "recovery": 0.18245895206928253, "safety_risk": 0.040138129144907, "score": 0.0453186072409153} |
| 2 | {"cost": 0.47635000944137573, "impurity_signal": 0.10803710669279099, "phase_ratio": 0.0, "product_in_aqueous": 0.7676535248756409, "product_in_organic": 0.008452002890408039, "purity": 0.8681256771087646, "recovery": 0.7394119501113892, "safety_risk": 0.09904835373163223, "score": 0.0} |
| 3 | {"cost": 0.4923500120639801, "impurity_signal": 0.0, "phase_ratio": 0.96914142370224, "product_in_aqueous": 0.0, "product_in_organic": 0.3235694169998169, "purity": 0.9637078642845154, "recovery": 0.3090876340866089, "safety_risk": 0.06862150877714157, "score": 0.17811986804008484} |
| 4 | {"cost": 0.4923500120639801, "impurity_signal": 0.13664788007736206, "phase_ratio": 0.009506937116384506, "product_in_aqueous": 0.6278996467590332, "product_in_organic": 0.0, "purity": 0.8461317420005798, "recovery": 0.6163272857666016, "safety_risk": 0.11821743845939636, "score": 0.0} |
| 5 | {"cost": 0.5179499983787537, "impurity_signal": 0.016438936814665794, "phase_ratio": 0.9829117059707642, "product_in_aqueous": 0.0, "product_in_organic": 0.34551364183425903, "purity": 0.9623986482620239, "recovery": 0.34235066175460815, "safety_risk": 0.08785449713468552, "score": 0.19539542496204376} |
| 6 | {"cost": 0.5179499983787537, "impurity_signal": 0.13298769295215607, "phase_ratio": 0.0, "product_in_aqueous": 0.7811337113380432, "product_in_organic": 0.0, "purity": 0.8551321029663086, "recovery": 0.7661908864974976, "safety_risk": 0.14121100306510925, "score": 0.0} |
| 7 | {"cost": 0.5019500255584717, "impurity_signal": 0.0073271444998681545, "phase_ratio": 1.0, "product_in_aqueous": 0.007889077998697758, "product_in_organic": 0.35208651423454285, "purity": 0.9673709869384766, "recovery": 0.35041049122810364, "safety_risk": 0.10081125050783157, "score": 0.1984846442937851} |
| 8 | {"cost": 0.5019500255584717, "impurity_signal": 0.11592771857976913, "phase_ratio": 0.0, "product_in_aqueous": 0.8137021660804749, "product_in_organic": 0.0, "purity": 0.853238582611084, "recovery": 0.7911281585693359, "safety_risk": 0.15446485579013824, "score": 0.0} |
| 9 | {"cost": 0.48945000767707825, "impurity_signal": 0.014530058018863201, "phase_ratio": 1.0, "product_in_aqueous": 0.0, "product_in_organic": 0.3642507791519165, "purity": 0.9753153324127197, "recovery": 0.38050201535224915, "safety_risk": 0.07106854766607285, "score": 0.2096131592988968} |
| 10 | {"cost": 0.49524998664855957, "impurity_signal": 0.016875825822353363, "phase_ratio": 1.0, "product_in_aqueous": 0.0009292740724049509, "product_in_organic": 0.37680062651634216, "purity": 0.9778773188591003, "recovery": 0.3847801685333252, "safety_risk": 0.07106854766607285, "score": 0.22018760442733765} |
| 11 | {"cost": 0.491225004196167, "impurity_signal": 0.023237992078065872, "phase_ratio": 1.0, "product_in_aqueous": 0.0, "product_in_organic": 0.29192042350769043, "purity": 0.9733077883720398, "recovery": 0.28997957706451416, "safety_risk": 0.0674789771437645, "score": 0.1481323540210724} |
| 12 | {"cost": 0.4961000084877014, "impurity_signal": 0.012086383998394012, "phase_ratio": 0.9891050457954407, "product_in_aqueous": 0.0054099163971841335, "product_in_organic": 0.4354894757270813, "purity": 0.9643869400024414, "recovery": 0.4430297315120697, "safety_risk": 0.07437609881162643, "score": 0.27071458101272583} |

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

Observations: All batches used 0.04 mol reagent. Batches 1–8 screened material pairs at 0.04 L solvent, 0.04 L aqueous phase, 0.02 L extractant, 300 s/600 rpm mixing and 300 s settling. Pre-separation HPLC target signals (organic, aqueous) were: B1 S0/X0 (0.152, 0.800), B2 S0/X2 (0.263, 0.769), B3 S1/X0 (0.292, 0.703), B4 S1/X2 (0.380, 0.611), B5 S2/X0 (0.341, 0.665), B6 S2/X2 (0.216, 0.760), B7 S3/X1 (0.355, 0.626), and B8 S3/X3 (0.209, 0.768). Thus every tested system favored the aqueous phase, but organic transfer varied substantially and depended on the pair rather than either label alone. In particular, X2 was relatively effective with S1 but weak with S2, while X0 improved from S0 through S1 to S2.

Phase-retention assays corroborated the phase assignments. Organic-retained batches had final phase ratios about 0.97–1.00, aqueous target signals near 0–0.015, and organic target signals broadly consistent with the preceding HPLC result. Aqueous-retained batches had phase ratios about 0–0.010, organic target signals near 0–0.008, and retained aqueous target signals consistent with HPLC. The impurity evidence was asymmetric: pre-separation HPLC impurity signals were near zero, and organic-retained final assays were also low (0–0.023), whereas aqueous-retained B2, B4, B6 and B8 showed impurity signals of 0.108–0.137 and lower purities of 0.846–0.868. Organic retention therefore selected a cleaner but smaller target fraction under the tested conditions.

Batches 9–12 tested process effects on S1/X2. Changing solvent/aqueous/extractant volumes from 0.04/0.04/0.02 L (B4) to 0.03/0.05/0.02 L (B9) or 0.05/0.03/0.02 L (B10) produced only modest HPLC changes: organic target 0.380, 0.380 and 0.395, respectively, with no clean monotonic change in the aqueous signal. By contrast, mixing showed a clear ordered response at fixed volumes: low mixing in B11 (30 s, 100 rpm) gave organic target 0.317; the 300 s, 600 rpm condition in B4 gave 0.380; and high mixing in B12 (1200 s, 1200 rpm) gave 0.457. Organic-retained final assays preserved the trend: B11 0.292, the comparable moderate-mixing organic-retained B9/B10 results 0.364–0.377, and B12 0.435.

Inference: Partition behavior is best described as a strong solvent–extractant interaction superimposed on incomplete mixing-dependent approach to transfer. Within the narrow volume window tested, material pairing and mixing were more influential than phase-amount changes. The aqueous phase remained the majority target reservoir, while organic retention traded total target recovery for markedly better impurity rejection. The measured phase-ratio channel stayed mostly near 0.18–0.22 before separation and changed little across recipes, so it appears to describe bulk phase amount rather than the target distribution itself; it should not be substituted for the target-specific organic/aqueous measurements.

Contribution of prior information: The supplied dossier correctly framed the labels as anonymous, independent materials and warned that marginal properties could not determine pair performance. Its relatively favorable marginal expectations for S2 and X0/X2 motivated informative screening, but experiments were decisive: S2/X0 was useful, whereas S2/X2 was weak and S1/X2 was strongest among the tested baseline pairs. This crossover is direct evidence that the undisclosed interaction term matters and that marginal rankings alone are inadequate.

Competing explanations and limits: The mixing trend may represent kinetic equilibration, improved interfacial contact, or a mixing-dependent recovery effect rather than a changed equilibrium partition coefficient. Duration and speed were varied together, so their separate contributions are unidentified. There were no replicate batches, and independent channel noise/process variability can explain small differences, especially the narrow volume effects. Only eight of sixteen material pairs were screened; X1 and X3 received especially sparse coverage. Volume effects were tested only around one pair at fixed total liquid, settling was fixed at 300 s, and reagent loading was fixed. Alternating retained phases across early batches could confound final-assay comparisons, although pre-separation HPLC avoids that problem for the pairing conclusions. Finally, organic and aqueous processed signals are independently noisy and do not always sum to one, so they support comparative partition trends rather than exact mass-balance fractions. Extrapolation should therefore be limited to nearby volumes and mixing conditions, with new pairings or equilibrium claims treated as conjectural.

## Q

### Question

Using your research, predict the true two-phase target fractions immediately before the first HPLC sample in these 12 independent new batches. The denominator is each batch's fixed initial target inventory. Give a point estimate and a 90% uncertainty interval for each noiseless fraction; do not predict random instrument noise. No new experiments or changes to K1 are allowed. Predict before phase removal, not the terminal assay after selecting a phase. D1: Which phase should be retained in Q01 to keep more target? D2: Under the same material amounts, does Q05 or Q06 place more target in the organic phase? Both decisions allow uncertain. Supply one shared concise rationale in English, without a long explanation per question. Return the required JSON.
[{"query_id": "Q01", "actions": [{"operation": "add_solvent", "solvent": 0, "volume_L": 0.02}, {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.03}, {"operation": "add_extractant", "extractant": 0, "volume_L": 0.008}, {"operation": "mix", "duration_s": 900, "stirring_speed_rpm": 1200}, {"operation": "settle", "duration_s": 300}, {"operation": "measure", "instrument": "hplc"}, {"operation": "separate_phase", "target_phase": "organic"}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q02", "actions": [{"operation": "add_solvent", "solvent": 0, "volume_L": 0.02}, {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.03}, {"operation": "add_extractant", "extractant": 0, "volume_L": 0.03}, {"operation": "mix", "duration_s": 900, "stirring_speed_rpm": 1200}, {"operation": "settle", "duration_s": 300}, {"operation": "measure", "instrument": "hplc"}, {"operation": "separate_phase", "target_phase": "organic"}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q03", "actions": [{"operation": "add_solvent", "solvent": 0, "volume_L": 0.02}, {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.03}, {"operation": "add_extractant", "extractant": 3, "volume_L": 0.008}, {"operation": "mix", "duration_s": 900, "stirring_speed_rpm": 1200}, {"operation": "settle", "duration_s": 300}, {"operation": "measure", "instrument": "hplc"}, {"operation": "separate_phase", "target_phase": "organic"}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q04", "actions": [{"operation": "add_solvent", "solvent": 0, "volume_L": 0.02}, {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.03}, {"operation": "add_extractant", "extractant": 3, "volume_L": 0.03}, {"operation": "mix", "duration_s": 900, "stirring_speed_rpm": 1200}, {"operation": "settle", "duration_s": 300}, {"operation": "measure", "instrument": "hplc"}, {"operation": "separate_phase", "target_phase": "organic"}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q05", "actions": [{"operation": "add_solvent", "solvent": 0, "volume_L": 0.02}, {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.015}, {"operation": "add_extractant", "extractant": 0, "volume_L": 0.019}, {"operation": "mix", "duration_s": 900, "stirring_speed_rpm": 1200}, {"operation": "settle", "duration_s": 300}, {"operation": "measure", "instrument": "hplc"}, {"operation": "separate_phase", "target_phase": "organic"}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q06", "actions": [{"operation": "add_solvent", "solvent": 0, "volume_L": 0.02}, {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.015}, {"operation": "add_extractant", "extractant": 3, "volume_L": 0.019}, {"operation": "mix", "duration_s": 900, "stirring_speed_rpm": 1200}, {"operation": "settle", "duration_s": 300}, {"operation": "measure", "instrument": "hplc"}, {"operation": "separate_phase", "target_phase": "organic"}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q07", "actions": [{"operation": "add_solvent", "solvent": 2, "volume_L": 0.02}, {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.015}, {"operation": "add_extractant", "extractant": 0, "volume_L": 0.019}, {"operation": "mix", "duration_s": 900, "stirring_speed_rpm": 1200}, {"operation": "settle", "duration_s": 300}, {"operation": "measure", "instrument": "hplc"}, {"operation": "separate_phase", "target_phase": "organic"}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q08", "actions": [{"operation": "add_solvent", "solvent": 2, "volume_L": 0.02}, {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.015}, {"operation": "add_extractant", "extractant": 3, "volume_L": 0.019}, {"operation": "mix", "duration_s": 900, "stirring_speed_rpm": 1200}, {"operation": "settle", "duration_s": 300}, {"operation": "measure", "instrument": "hplc"}, {"operation": "separate_phase", "target_phase": "organic"}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q09", "actions": [{"operation": "add_solvent", "solvent": 0, "volume_L": 0.02}, {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.015}, {"operation": "add_extractant", "extractant": 0, "volume_L": 0.019}, {"operation": "mix", "duration_s": 120, "stirring_speed_rpm": 700}, {"operation": "settle", "duration_s": 300}, {"operation": "measure", "instrument": "hplc"}, {"operation": "separate_phase", "target_phase": "organic"}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q10", "actions": [{"operation": "add_solvent", "solvent": 0, "volume_L": 0.02}, {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.015}, {"operation": "add_extractant", "extractant": 0, "volume_L": 0.019}, {"operation": "mix", "duration_s": 1200, "stirring_speed_rpm": 700}, {"operation": "settle", "duration_s": 300}, {"operation": "measure", "instrument": "hplc"}, {"operation": "separate_phase", "target_phase": "organic"}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q11", "actions": [{"operation": "add_solvent", "solvent": 2, "volume_L": 0.02}, {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.015}, {"operation": "add_extractant", "extractant": 3, "volume_L": 0.019}, {"operation": "mix", "duration_s": 600, "stirring_speed_rpm": 200}, {"operation": "settle", "duration_s": 300}, {"operation": "measure", "instrument": "hplc"}, {"operation": "separate_phase", "target_phase": "organic"}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}, {"query_id": "Q12", "actions": [{"operation": "add_solvent", "solvent": 2, "volume_L": 0.02}, {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.015}, {"operation": "add_extractant", "extractant": 3, "volume_L": 0.019}, {"operation": "mix", "duration_s": 600, "stirring_speed_rpm": 1200}, {"operation": "settle", "duration_s": 300}, {"operation": "measure", "instrument": "hplc"}, {"operation": "separate_phase", "target_phase": "organic"}, {"operation": "terminate"}, {"operation": "measure", "instrument": "final_assay"}]}]

### Response

```json
{
  "D1_phase": "aqueous",
  "D2_query": "uncertain",
  "predictions": [
    {
      "product_in_aqueous": {
        "estimate": 0.873,
        "lower90": 0.79,
        "upper90": 0.94
      },
      "product_in_organic": {
        "estimate": 0.127,
        "lower90": 0.06,
        "upper90": 0.21
      },
      "query_id": "Q01"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.647,
        "lower90": 0.53,
        "upper90": 0.75
      },
      "product_in_organic": {
        "estimate": 0.353,
        "lower90": 0.25,
        "upper90": 0.47
      },
      "query_id": "Q02"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.888,
        "lower90": 0.75,
        "upper90": 0.96
      },
      "product_in_organic": {
        "estimate": 0.112,
        "lower90": 0.04,
        "upper90": 0.25
      },
      "query_id": "Q03"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.68,
        "lower90": 0.51,
        "upper90": 0.82
      },
      "product_in_organic": {
        "estimate": 0.32,
        "lower90": 0.18,
        "upper90": 0.49
      },
      "query_id": "Q04"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.669,
        "lower90": 0.57,
        "upper90": 0.76
      },
      "product_in_organic": {
        "estimate": 0.331,
        "lower90": 0.24,
        "upper90": 0.43
      },
      "query_id": "Q05"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.701,
        "lower90": 0.57,
        "upper90": 0.83
      },
      "product_in_organic": {
        "estimate": 0.299,
        "lower90": 0.17,
        "upper90": 0.43
      },
      "query_id": "Q06"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.416,
        "lower90": 0.32,
        "upper90": 0.52
      },
      "product_in_organic": {
        "estimate": 0.584,
        "lower90": 0.48,
        "upper90": 0.68
      },
      "query_id": "Q07"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.452,
        "lower90": 0.3,
        "upper90": 0.65
      },
      "product_in_organic": {
        "estimate": 0.548,
        "lower90": 0.35,
        "upper90": 0.7
      },
      "query_id": "Q08"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.719,
        "lower90": 0.63,
        "upper90": 0.8
      },
      "product_in_organic": {
        "estimate": 0.281,
        "lower90": 0.2,
        "upper90": 0.37
      },
      "query_id": "Q09"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.677,
        "lower90": 0.58,
        "upper90": 0.77
      },
      "product_in_organic": {
        "estimate": 0.323,
        "lower90": 0.23,
        "upper90": 0.42
      },
      "query_id": "Q10"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.509,
        "lower90": 0.33,
        "upper90": 0.71
      },
      "product_in_organic": {
        "estimate": 0.491,
        "lower90": 0.29,
        "upper90": 0.67
      },
      "query_id": "Q11"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.463,
        "lower90": 0.3,
        "upper90": 0.66
      },
      "product_in_organic": {
        "estimate": 0.537,
        "lower90": 0.34,
        "upper90": 0.7
      },
      "query_id": "Q12"
    }
  ],
  "rationale": "I extrapolated a two-phase volume-ratio partition model from the pre-separation HPLC results, increasing organic transfer with stronger or longer mixing. S0/X0 and S2/X0 are anchored by observed batches; X3 combinations rely mainly on the weaker marginal prior and therefore have wider intervals. Q01 should remain predominantly aqueous. The marginal prior slightly favors X0 in Q05, but unmeasured S0–X3 interaction uncertainty is larger than that predicted difference, so Q05 versus Q06 is unresolved."
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

1. No instance-specific prior, pair table, or true mechanism was supplied; the only supplied information was an aggregate marginal material dossier that explicitly warned it could be incomplete or misindexed. The least-tested self-developed law is my later volume-ratio model, especially the assumption that solvent plus added aqueous liquid forms one effective phase and that extractant volume is the other. Batches 9 and 10 changed solvent and aqueous additions while keeping their sum and extractant volume fixed, so they did not actually identify that volume law. The claim that stronger mixing reflects approach to equilibrium also remains provisional: B11, B4, and B12 varied duration and speed together, leaving kinetics, interfacial area, and process recovery confounded.

2. I would run one S1/X2 experiment at the established 0.04/0.04/0.02 L composition and take small pre-separation HPLC samples after successive fixed-speed mixing intervals—ideally 30, 300, 900, and 1800 s at 1200 rpm—then assay both separated phases for target and mass balance. A monotonic rise followed by a stable plateau, with complementary aqueous loss and good mass balance, would strengthen the kinetic-approach-to-equilibrium explanation. An immediate plateau would imply that the B11/B4/B12 ordering was mainly speed-dependent or batch variation. Continued drift without a plateau, noncomplementary phase signals, or changing total target recovery would instead favor emulsion/sampling, degradation, or measurement/recovery effects rather than a simple partition equilibrium.

3. Underused evidence includes the raw HPLC and final-assay artifacts, their calibration/uncertainty metadata, the final recovery and impurity channels, and the dossier’s impurity/selectivity marginals. I relied primarily on processed target signals and did not inspect spectra or formally propagate measurement uncertainty. The least reliable predictions are those for untested X3 pairings—Q03, Q04, Q06, and especially S2/X3 in Q08, Q11, and Q12. Q11–Q12 are additionally weak because they require separating speed from duration, which the campaign never did; Q02 also extrapolates to an extractant amount beyond the tested range.

There is a real tension between the sealed report and predictions. The report limited volume conclusions to a narrow tested region and said speed and duration were unidentified, whereas the predictions imposed a specific volume-ratio law and separate mixing extrapolations. The predictions also forced aqueous and organic fractions to sum to one even though the report warned that the processed channels were independently noisy and did not always close exactly. Those choices were prospective modeling assumptions made under sparse evidence, not findings established by the campaign, and they should not be presented retrospectively as observed laws.

## Evaluation and resource use

```json
{
  "arm": "MisIndexed",
  "budget": 12,
  "goal": "discovery",
  "locus": "E",
  "system": "PA",
  "unit_id": "PA-W03-B12-discovery-E-MisIndexed",
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
        "mae": 0.09589664412726108,
        "coverage90": 0.75,
        "mean_width90": 0.24916666666666665,
        "interval_score90": 0.9836706625694801
      },
      "product_in_aqueous": {
        "n": 12,
        "mae": 0.09589664412726111,
        "coverage90": 0.75,
        "mean_width90": 0.24916666666666668,
        "interval_score90": 0.9836706625694802
      }
    },
    "details": [
      {
        "query_id": "Q01",
        "metric": "product_in_organic",
        "estimate": 0.127,
        "lower90": 0.06,
        "upper90": 0.21,
        "truth": 0.14028028852564417,
        "absolute_error": 0.013280288525644168
      },
      {
        "query_id": "Q02",
        "metric": "product_in_organic",
        "estimate": 0.353,
        "lower90": 0.25,
        "upper90": 0.47,
        "truth": 0.37628859799060643,
        "absolute_error": 0.023288597990606452
      },
      {
        "query_id": "Q03",
        "metric": "product_in_organic",
        "estimate": 0.112,
        "lower90": 0.04,
        "upper90": 0.25,
        "truth": 0.33817705508866275,
        "absolute_error": 0.22617705508866276
      },
      {
        "query_id": "Q04",
        "metric": "product_in_organic",
        "estimate": 0.32,
        "lower90": 0.18,
        "upper90": 0.49,
        "truth": 0.6471988475728407,
        "absolute_error": 0.32719884757284073
      },
      {
        "query_id": "Q05",
        "metric": "product_in_organic",
        "estimate": 0.331,
        "lower90": 0.24,
        "upper90": 0.43,
        "truth": 0.35352236193438064,
        "absolute_error": 0.02252236193438062
      },
      {
        "query_id": "Q06",
        "metric": "product_in_organic",
        "estimate": 0.299,
        "lower90": 0.17,
        "upper90": 0.43,
        "truth": 0.6253264948801845,
        "absolute_error": 0.32632649488018456
      },
      {
        "query_id": "Q07",
        "metric": "product_in_organic",
        "estimate": 0.584,
        "lower90": 0.48,
        "upper90": 0.68,
        "truth": 0.5863161160362313,
        "absolute_error": 0.002316116036231386
      },
      {
        "query_id": "Q08",
        "metric": "product_in_organic",
        "estimate": 0.548,
        "lower90": 0.35,
        "upper90": 0.7,
        "truth": 0.6068680731369908,
        "absolute_error": 0.05886807313699072
      },
      {
        "query_id": "Q09",
        "metric": "product_in_organic",
        "estimate": 0.281,
        "lower90": 0.2,
        "upper90": 0.37,
        "truth": 0.26801669600322914,
        "absolute_error": 0.01298330399677089
      },
      {
        "query_id": "Q10",
        "metric": "product_in_organic",
        "estimate": 0.323,
        "lower90": 0.23,
        "upper90": 0.42,
        "truth": 0.34018072751527934,
        "absolute_error": 0.017180727515279326
      },
      {
        "query_id": "Q11",
        "metric": "product_in_organic",
        "estimate": 0.491,
        "lower90": 0.29,
        "upper90": 0.67,
        "truth": 0.5539547895844652,
        "absolute_error": 0.06295478958446521
      },
      {
        "query_id": "Q12",
        "metric": "product_in_organic",
        "estimate": 0.537,
        "lower90": 0.34,
        "upper90": 0.7,
        "truth": 0.5946630732650762,
        "absolute_error": 0.05766307326507614
      },
      {
        "query_id": "Q01",
        "metric": "product_in_aqueous",
        "estimate": 0.873,
        "lower90": 0.79,
        "upper90": 0.94,
        "truth": 0.8597197114743559,
        "absolute_error": 0.013280288525644113
      },
      {
        "query_id": "Q02",
        "metric": "product_in_aqueous",
        "estimate": 0.647,
        "lower90": 0.53,
        "upper90": 0.75,
        "truth": 0.6237114020093936,
        "absolute_error": 0.023288597990606452
      },
      {
        "query_id": "Q03",
        "metric": "product_in_aqueous",
        "estimate": 0.888,
        "lower90": 0.75,
        "upper90": 0.96,
        "truth": 0.6618229449113372,
        "absolute_error": 0.22617705508866282
      },
      {
        "query_id": "Q04",
        "metric": "product_in_aqueous",
        "estimate": 0.68,
        "lower90": 0.51,
        "upper90": 0.82,
        "truth": 0.3528011524271592,
        "absolute_error": 0.32719884757284085
      },
      {
        "query_id": "Q05",
        "metric": "product_in_aqueous",
        "estimate": 0.669,
        "lower90": 0.57,
        "upper90": 0.76,
        "truth": 0.6464776380656193,
        "absolute_error": 0.02252236193438073
      },
      {
        "query_id": "Q06",
        "metric": "product_in_aqueous",
        "estimate": 0.701,
        "lower90": 0.57,
        "upper90": 0.83,
        "truth": 0.37467350511981545,
        "absolute_error": 0.3263264948801845
      },
      {
        "query_id": "Q07",
        "metric": "product_in_aqueous",
        "estimate": 0.416,
        "lower90": 0.32,
        "upper90": 0.52,
        "truth": 0.4136838839637687,
        "absolute_error": 0.002316116036231275
      },
      {
        "query_id": "Q08",
        "metric": "product_in_aqueous",
        "estimate": 0.452,
        "lower90": 0.3,
        "upper90": 0.65,
        "truth": 0.39313192686300924,
        "absolute_error": 0.05886807313699077
      },
      {
        "query_id": "Q09",
        "metric": "product_in_aqueous",
        "estimate": 0.719,
        "lower90": 0.63,
        "upper90": 0.8,
        "truth": 0.7319833039967709,
        "absolute_error": 0.012983303996770945
      },
      {
        "query_id": "Q10",
        "metric": "product_in_aqueous",
        "estimate": 0.677,
        "lower90": 0.58,
        "upper90": 0.77,
        "truth": 0.6598192724847206,
        "absolute_error": 0.017180727515279437
      },
      {
        "query_id": "Q11",
        "metric": "product_in_aqueous",
        "estimate": 0.509,
        "lower90": 0.33,
        "upper90": 0.71,
        "truth": 0.4460452104155348,
        "absolute_error": 0.06295478958446521
      },
      {
        "query_id": "Q12",
        "metric": "product_in_aqueous",
        "estimate": 0.463,
        "lower90": 0.3,
        "upper90": 0.66,
        "truth": 0.40533692673492383,
        "absolute_error": 0.05766307326507619
      }
    ],
    "decisions": {
      "D1": {
        "submitted": "aqueous",
        "truth": "aqueous",
        "correct": true
      },
      "D2": {
        "submitted": "uncertain",
        "truth": "Q06",
        "correct": false
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
        "input": 677689,
        "cached_input": 628480,
        "output": 6054,
        "uncached_input": 49209
      },
      {
        "stage": "K1",
        "input": 32248,
        "cached_input": 3456,
        "output": 1764,
        "uncached_input": 28792
      },
      {
        "stage": "Q",
        "input": 163021,
        "cached_input": 77440,
        "output": 5866,
        "uncached_input": 85581
      },
      {
        "stage": "K2",
        "input": 49277,
        "cached_input": 0,
        "output": 1181,
        "uncached_input": 49277
      }
    ],
    "total": {
      "input": 922235,
      "cached_input": 709376,
      "output": 14865,
      "uncached_input": 212859,
      "input_plus_output": 937100
    },
    "monetary_cost_usd": null
  },
  "elapsed_s": 699.1720000000059,
  "retest_batches": 0,
  "retest_operations": 0,
  "retest_replay": null,
  "english_output": true
}
```

## Infrastructure recovery

Original failed attempt is retained separately. Mode: posttests; new source batches: 0. See [recovery accounting](recovery.json).
