# PA-W05-B12-discovery-E-Opaque

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
| 1 | {"cost": 0.41635000705718994, "impurity_signal": 0.012120882980525494, "phase_ratio": 1.0, "product_in_aqueous": 0.014660237357020378, "product_in_organic": 0.14381472766399384, "purity": 0.8810092806816101, "recovery": 0.15358586609363556, "safety_risk": 0.037697337567806244, "score": 0.02077648974955082} |
| 2 | {"cost": 0.41635000705718994, "impurity_signal": 0.014000712893903255, "phase_ratio": 0.9997019171714783, "product_in_aqueous": 0.02075776644051075, "product_in_organic": 0.3204129636287689, "purity": 0.9245204925537109, "recovery": 0.30447718501091003, "safety_risk": 0.03967851772904396, "score": 0.1703050583600998} |
| 3 | {"cost": 0.41635000705718994, "impurity_signal": 0.4724771976470947, "phase_ratio": 0.0, "product_in_aqueous": 0.778445303440094, "product_in_organic": 0.005547169595956802, "purity": 0.6162369251251221, "recovery": 0.7764585018157959, "safety_risk": 0.05479985475540161, "score": 0.0} |
| 4 | {"cost": 0.41635000705718994, "impurity_signal": 0.0490233339369297, "phase_ratio": 1.0, "product_in_aqueous": 0.0, "product_in_organic": 0.32615962624549866, "purity": 0.9183104038238525, "recovery": 0.32199549674987793, "safety_risk": 0.040009476244449615, "score": 0.1772356778383255} |
| 5 | {"cost": 0.4323500096797943, "impurity_signal": 0.48632609844207764, "phase_ratio": 0.0, "product_in_aqueous": 0.7238441109657288, "product_in_organic": 0.0, "purity": 0.5973905324935913, "recovery": 0.7226954102516174, "safety_risk": 0.07771339267492294, "score": 0.0} |
| 6 | {"cost": 0.45794999599456787, "impurity_signal": 0.03494168445467949, "phase_ratio": 0.9943565726280212, "product_in_aqueous": 0.0156232425943017, "product_in_organic": 0.2877923846244812, "purity": 0.9115462303161621, "recovery": 0.30049771070480347, "safety_risk": 0.08091337978839874, "score": 0.14362555742263794} |
| 7 | {"cost": 0.4419499933719635, "impurity_signal": 0.4796369671821594, "phase_ratio": 0.003050468396395445, "product_in_aqueous": 0.762255072593689, "product_in_organic": 0.0, "purity": 0.6126342415809631, "recovery": 0.7525321841239929, "safety_risk": 0.10856295377016068, "score": 0.0} |
| 8 | {"cost": 0.41514167189598083, "impurity_signal": 0.4858437478542328, "phase_ratio": 0.0, "product_in_aqueous": 0.9244715571403503, "product_in_organic": 0.0, "purity": 0.6344106197357178, "recovery": 0.9018975496292114, "safety_risk": 0.05576121807098389, "score": 0.0} |
| 9 | {"cost": 0.42260000109672546, "impurity_signal": 0.024267302826046944, "phase_ratio": 1.0, "product_in_aqueous": 0.0, "product_in_organic": 0.1642744392156601, "purity": 0.8913506865501404, "recovery": 0.18052569031715393, "safety_risk": 0.038019273430109024, "score": 0.03963327780365944} |
| 10 | {"cost": 0.43654999136924744, "impurity_signal": 0.09736128151416779, "phase_ratio": 1.0, "product_in_aqueous": 0.0009292740724049509, "product_in_organic": 0.4800584614276886, "purity": 0.8472504019737244, "recovery": 0.48803800344467163, "safety_risk": 0.037973061203956604, "score": 0.3079567849636078} |
| 11 | {"cost": 0.40959998965263367, "impurity_signal": 0.5169742703437805, "phase_ratio": 0.008578194305300713, "product_in_aqueous": 0.9551854729652405, "product_in_organic": 0.0011032409965991974, "purity": 0.6633995175361633, "recovery": 0.964781641960144, "safety_risk": 0.05108562856912613, "score": 0.0} |
| 12 | {"cost": 0.4419499933719635, "impurity_signal": 0.015980303287506104, "phase_ratio": 0.9891050457954407, "product_in_aqueous": 0.0054099163971841335, "product_in_organic": 0.18434536457061768, "purity": 0.9011581540107727, "recovery": 0.19188560545444489, "safety_risk": 0.09208410233259201, "score": 0.05724206566810608} |

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

OBSERVATIONS

All 12 batches used 0.020 mol reagent. HPLC was measured after mixing and settling but before phase removal; the final assay was measured after retaining one phase. Under the common condition—0.040 L solvent, 0.040 L added aqueous phase, 0.020 L extractant, 300 s at 600 rpm—the S0–X0 baseline (batch 1) gave product_in_organic 0.123, product_in_aqueous 0.829, phase_ratio 0.169, and recovery 0.150.

Material contrasts at that common condition were substantial. With S0 fixed, changing X0 to X1, X2, and X3 produced organic signals of 0.322, 0.189, and 0.344 in batches 2–4, versus 0.123 for X0. With X0 fixed, S1, S2, and S3 produced 0.269, 0.282, and 0.248 in batches 5–7. Thus every tested alternative solvent improved organic transfer relative to the observed S0–X0 baseline, while X1 and X3 were the strongest tested extractants with S0. The S3–X3 cross-combination in batch 12 gave only 0.206 organic and 0.820 aqueous, despite X3’s strong result with S0.

Mixing affected S0–X0. Low mixing (batch 8, 10 s at 100 rpm) gave organic 0.098 and recovery 0.095; the standard batch gave 0.123 and 0.150; combined high-speed/long mixing (batch 9, 1800 s at 1200 rpm) gave 0.180 and 0.190. Phase amount had the largest direct effect: the high-extractant design in batch 10 (0.060 L extractant; HPLC phase_ratio 0.609) gave organic 0.499, aqueous 0.512, and recovery 0.468. The low-extractant design in batch 11 (0.005 L; phase_ratio 0.063) gave organic 0.060, aqueous 0.933, and recovery 0.034.

Post-separation assays corroborated the retention decisions. Examples include batch 2 organic 0.320 after retention versus 0.322 before separation; batch 6, 0.288 versus 0.282; batch 10, 0.480 versus 0.499; batch 3 aqueous 0.778 versus 0.806; and batch 11 aqueous 0.955 versus 0.933. Across the study, retained-organic results stayed close to the pre-separation organic signal, and retained-aqueous results stayed close to the corresponding aqueous signal. Aqueous-retained final assays also showed much higher impurity signal, approximately 0.47–0.52, and lower purity, approximately 0.60–0.66, than most organic-retained assays.

INFERENCE

Partition is governed jointly by available phase capacity, material pairing, and mixing history. Increasing the organic/extractant phase raises the total amount found there, while decreasing it leaves nearly all target in the aqueous phase. A rough volume-normalized diagnostic, calculated as the organic-to-aqueous signal ratio corrected by the measured phase-volume ratio, was about 0.73 for standard S0–X0, 1.61 for S0–X1, 0.91 for S0–X2, 2.20 for S0–X3, and 1.31–1.50 for S1–S3 with X0. This supports genuine material effects beyond phase volume alone, but it is a descriptive normalization rather than a validated thermodynamic coefficient.

The mixing series implies that the standard protocol may not reach a mixing-independent equilibrium: stronger and much longer mixing increased organic transfer. Because time and speed changed together, the evidence establishes a combined mixing-severity effect, not which variable controls it. The poor S3–X3 result relative to the strong separate S3–X0 and S0–X3 results argues against a purely additive ranking of solvents and extractants; pairing-specific interaction is important.

The retention assays support a practical phase decision rule: retain organic when the desired objective is the extracted target fraction, but retain aqueous when conservation of most target is more important, especially at low organic volume or weak extraction. The systematically high impurity signal in retained aqueous phases suggests that the impurity preferentially remains there or becomes more visible in that matrix.

CONTRIBUTIONS OF SUPPLIED INFORMATION AND EXPERIMENTS

The supplied catalog deliberately provided only anonymous, independent S and X labels and no property dossier. It therefore prevented importing real-material polarity or identity assumptions; all ranking above comes from the campaign. The public instrument contract identified HPLC as the nonfinal instrument that simultaneously reports both phase products, phase ratio, recovery, purity, and impurity, so it was used in every batch. Final assays then provided an independent, lower-noise check after phase retention. Controlled one-factor material comparisons, two extreme phase-volume tests, two mixing-severity tests, alternating phase retention, and the S3–X3 interaction test supplied the causal structure of the account.

COMPETING EXPLANATIONS AND LIMITS

The apparent mixing dependence could reflect incomplete mass transfer, emulsion behavior, or a matrix-dependent measurement effect; equilibrium was not demonstrated. The phase-volume experiments changed several absolute volumes together, so phase fraction is not cleanly separated from dilution or concentration effects. Material-pair coverage was sparse: only S0 with all X, all S with X0, and one off-axis pair were tested, so interactions for the remaining combinations are unknown. Most conditions were unreplicated, and the low, standard, and high mixing batches are not true replicates. Differences close to the declared instrument noise should not be overinterpreted.

Finally, product fields are synthetic assay observables rather than direct species inventories. The high aqueous impurity signal may represent real co-retention, matrix response, or both. The inferred volume-normalized affinities should therefore be used only within the studied volume, loading, mixing, and anonymous-material domain; extrapolation to other loadings, multiple extraction stages, different settling times, or real chemical identities remains conjectural.

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
        "estimate": 0.885,
        "lower90": 0.82,
        "upper90": 0.93
      },
      "product_in_organic": {
        "estimate": 0.115,
        "lower90": 0.07,
        "upper90": 0.18
      },
      "query_id": "Q01"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.671,
        "lower90": 0.58,
        "upper90": 0.75
      },
      "product_in_organic": {
        "estimate": 0.329,
        "lower90": 0.25,
        "upper90": 0.42
      },
      "query_id": "Q02"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.682,
        "lower90": 0.55,
        "upper90": 0.8
      },
      "product_in_organic": {
        "estimate": 0.318,
        "lower90": 0.2,
        "upper90": 0.45
      },
      "query_id": "Q03"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.363,
        "lower90": 0.25,
        "upper90": 0.5
      },
      "product_in_organic": {
        "estimate": 0.637,
        "lower90": 0.5,
        "upper90": 0.75
      },
      "query_id": "Q04"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.693,
        "lower90": 0.61,
        "upper90": 0.77
      },
      "product_in_organic": {
        "estimate": 0.307,
        "lower90": 0.23,
        "upper90": 0.39
      },
      "query_id": "Q05"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.387,
        "lower90": 0.27,
        "upper90": 0.51
      },
      "product_in_organic": {
        "estimate": 0.613,
        "lower90": 0.49,
        "upper90": 0.73
      },
      "query_id": "Q06"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.451,
        "lower90": 0.32,
        "upper90": 0.58
      },
      "product_in_organic": {
        "estimate": 0.549,
        "lower90": 0.42,
        "upper90": 0.68
      },
      "query_id": "Q07"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.338,
        "lower90": 0.14,
        "upper90": 0.65
      },
      "product_in_organic": {
        "estimate": 0.662,
        "lower90": 0.35,
        "upper90": 0.86
      },
      "query_id": "Q08"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.784,
        "lower90": 0.68,
        "upper90": 0.87
      },
      "product_in_organic": {
        "estimate": 0.216,
        "lower90": 0.13,
        "upper90": 0.32
      },
      "query_id": "Q09"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.708,
        "lower90": 0.6,
        "upper90": 0.8
      },
      "product_in_organic": {
        "estimate": 0.292,
        "lower90": 0.2,
        "upper90": 0.4
      },
      "query_id": "Q10"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.424,
        "lower90": 0.18,
        "upper90": 0.73
      },
      "product_in_organic": {
        "estimate": 0.576,
        "lower90": 0.27,
        "upper90": 0.82
      },
      "query_id": "Q11"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.359,
        "lower90": 0.15,
        "upper90": 0.68
      },
      "product_in_organic": {
        "estimate": 0.641,
        "lower90": 0.32,
        "upper90": 0.85
      },
      "query_id": "Q12"
    }
  ],
  "rationale": "Predictions interpolate the pre-separation HPLC evidence using phase-volume balance, volume-normalized material effects, and the observed increase in organic transfer with mixing severity. Q01 remains strongly aqueous-dominant, while X3 outperformed X0 with S0, making Q06 organic-richer than Q05. Intervals are widest for untested S2–X3 because the S3–X3 batch showed that solvent and extractant effects are not reliably additive."
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

1. No instance prior was supplied. The material dossier contained only anonymous labels and explicitly supplied no property estimates. The least-tested self-developed law is the use of a volume-normalized, equilibrium-like partition factor that is adjusted smoothly for mixing and then transported to new phase volumes. Batches 8, 1, and 9 show that transfer still changed with jointly altered time and speed, so equilibrium was not established. Batch 12 also shows that material effects are not safely additive: S3–X3 was much weaker than combining the separate S3 and X3 main effects would suggest. A further untested assumption in the predictions was target conservation between the two reported phases, making the two fractions sum to one.

2. I would run S2–X3 under the common campaign condition: 0.040 L S2, 0.040 L aqueous phase, 0.020 L X3, 0.020 mol reagent, 300 s at 600 rpm, and 300 s settling. I would measure pre-separation HPLC product_in_organic, product_in_aqueous, and phase_ratio, then retain organic and use the final assay as a matrix/retention check. This directly completes the material contrast defined by batches 1, 4, 6, and 12. An organic fraction around 0.55–0.65 would favor an approximately multiplicative main-effect account; roughly 0.20–0.30 would favor strong pairing-specific suppression like that seen in batch 12; an intermediate result would support partial interaction and would narrow, but not eliminate, uncertainty. This experiment would not by itself resolve the separate concern that the prediction batches omit the 0.020 mol reagent used throughout the campaign.

3. The pre-separation recovery, purity, impurity, and phase-ratio observations were underused in the predictions; the model relied mainly on the two target fractions. The post-retention assays were used qualitatively but not formally to estimate matrix bias or mass-balance uncertainty. Batch 12 deserved greater quantitative weight as evidence against transporting X3’s S0 effect to other solvents. The least reliable predictions are Q08, Q11, and Q12 because S2–X3 was never observed and the only off-axis interaction test contradicted simple additivity. All predictions also inherit uncertainty from the reagent mismatch, while Q09–Q12 additionally depend on a mixing response inferred from only three confounded time/speed settings.

There is no direct numerical contradiction between the sealed report and predictions, but there is tension. The report warned that equilibrium, material additivity, conservation, and separate time/speed effects were unverified; the predictions nevertheless required point estimates and therefore imposed smooth volume/mixing interpolation, complementary aqueous/organic fractions, and a midpoint extrapolation for S2–X3. The wide S2–X3 intervals acknowledged some of this, but several other intervals were probably too confident given the untested reagent transfer and mixing assumptions. This is a present critique of the sealed outputs, not a revision of their contemporaneous record.

## Evaluation and resource use

```json
{
  "arm": "Opaque",
  "budget": 12,
  "goal": "discovery",
  "locus": "E",
  "system": "PA",
  "unit_id": "PA-W05-B12-discovery-E-Opaque",
  "world": {
    "world_id": "PA-W05",
    "world_interventions": [
      {
        "axis_id": "partition.distribution-coefficient",
        "mode": "extrapolation",
        "severity": 0.45
      },
      {
        "axis_id": "partition.phase-volume-ratio",
        "mode": "extrapolation",
        "severity": -0.8
      }
    ],
    "world_seed": 4
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
        "absolute_error": 0.0004815553969664821,
        "estimate": 0.115,
        "lower90": 0.07,
        "metric": "product_in_organic",
        "query_id": "Q01",
        "truth": 0.11548155539696649,
        "upper90": 0.18
      },
      {
        "absolute_error": 0.0028155082820296995,
        "estimate": 0.329,
        "lower90": 0.25,
        "metric": "product_in_organic",
        "query_id": "Q02",
        "truth": 0.3261844917179703,
        "upper90": 0.42
      },
      {
        "absolute_error": 0.027339789293603534,
        "estimate": 0.318,
        "lower90": 0.2,
        "metric": "product_in_organic",
        "query_id": "Q03",
        "truth": 0.29066021070639647,
        "upper90": 0.45
      },
      {
        "absolute_error": 0.03963920386133124,
        "estimate": 0.637,
        "lower90": 0.5,
        "metric": "product_in_organic",
        "query_id": "Q04",
        "truth": 0.5973607961386688,
        "upper90": 0.75
      },
      {
        "absolute_error": 0.002108971848294061,
        "estimate": 0.307,
        "lower90": 0.23,
        "metric": "product_in_organic",
        "query_id": "Q05",
        "truth": 0.30489102815170593,
        "upper90": 0.39
      },
      {
        "absolute_error": 0.03882987480455902,
        "estimate": 0.613,
        "lower90": 0.49,
        "metric": "product_in_organic",
        "query_id": "Q06",
        "truth": 0.574170125195441,
        "upper90": 0.73
      },
      {
        "absolute_error": 0.015598093085172016,
        "estimate": 0.549,
        "lower90": 0.42,
        "metric": "product_in_organic",
        "query_id": "Q07",
        "truth": 0.533401906914828,
        "upper90": 0.68
      },
      {
        "absolute_error": 0.10721393069550955,
        "estimate": 0.662,
        "lower90": 0.35,
        "metric": "product_in_organic",
        "query_id": "Q08",
        "truth": 0.5547860693044905,
        "upper90": 0.86
      },
      {
        "absolute_error": 0.013206863826723841,
        "estimate": 0.216,
        "lower90": 0.13,
        "metric": "product_in_organic",
        "query_id": "Q09",
        "truth": 0.22920686382672384,
        "upper90": 0.32
      },
      {
        "absolute_error": 0.0009838074019817844,
        "estimate": 0.292,
        "lower90": 0.2,
        "metric": "product_in_organic",
        "query_id": "Q10",
        "truth": 0.29298380740198177,
        "upper90": 0.4
      },
      {
        "absolute_error": 0.07164250431405872,
        "estimate": 0.576,
        "lower90": 0.27,
        "metric": "product_in_organic",
        "query_id": "Q11",
        "truth": 0.5043574956859412,
        "upper90": 0.82
      },
      {
        "absolute_error": 0.09780537108559295,
        "estimate": 0.641,
        "lower90": 0.32,
        "metric": "product_in_organic",
        "query_id": "Q12",
        "truth": 0.5431946289144071,
        "upper90": 0.85
      },
      {
        "absolute_error": 0.0004815553969664821,
        "estimate": 0.885,
        "lower90": 0.82,
        "metric": "product_in_aqueous",
        "query_id": "Q01",
        "truth": 0.8845184446030335,
        "upper90": 0.93
      },
      {
        "absolute_error": 0.0028155082820296995,
        "estimate": 0.671,
        "lower90": 0.58,
        "metric": "product_in_aqueous",
        "query_id": "Q02",
        "truth": 0.6738155082820297,
        "upper90": 0.75
      },
      {
        "absolute_error": 0.027339789293603478,
        "estimate": 0.682,
        "lower90": 0.55,
        "metric": "product_in_aqueous",
        "query_id": "Q03",
        "truth": 0.7093397892936035,
        "upper90": 0.8
      },
      {
        "absolute_error": 0.039639203861331185,
        "estimate": 0.363,
        "lower90": 0.25,
        "metric": "product_in_aqueous",
        "query_id": "Q04",
        "truth": 0.4026392038613312,
        "upper90": 0.5
      },
      {
        "absolute_error": 0.002108971848294061,
        "estimate": 0.693,
        "lower90": 0.61,
        "metric": "product_in_aqueous",
        "query_id": "Q05",
        "truth": 0.695108971848294,
        "upper90": 0.77
      },
      {
        "absolute_error": 0.03882987480455902,
        "estimate": 0.387,
        "lower90": 0.27,
        "metric": "product_in_aqueous",
        "query_id": "Q06",
        "truth": 0.425829874804559,
        "upper90": 0.51
      },
      {
        "absolute_error": 0.01559809308517196,
        "estimate": 0.451,
        "lower90": 0.32,
        "metric": "product_in_aqueous",
        "query_id": "Q07",
        "truth": 0.46659809308517197,
        "upper90": 0.58
      },
      {
        "absolute_error": 0.10721393069550944,
        "estimate": 0.338,
        "lower90": 0.14,
        "metric": "product_in_aqueous",
        "query_id": "Q08",
        "truth": 0.44521393069550946,
        "upper90": 0.65
      },
      {
        "absolute_error": 0.01320686382672398,
        "estimate": 0.784,
        "lower90": 0.68,
        "metric": "product_in_aqueous",
        "query_id": "Q09",
        "truth": 0.770793136173276,
        "upper90": 0.87
      },
      {
        "absolute_error": 0.0009838074019816734,
        "estimate": 0.708,
        "lower90": 0.6,
        "metric": "product_in_aqueous",
        "query_id": "Q10",
        "truth": 0.7070161925980183,
        "upper90": 0.8
      },
      {
        "absolute_error": 0.07164250431405877,
        "estimate": 0.424,
        "lower90": 0.18,
        "metric": "product_in_aqueous",
        "query_id": "Q11",
        "truth": 0.49564250431405876,
        "upper90": 0.73
      },
      {
        "absolute_error": 0.09780537108559301,
        "estimate": 0.359,
        "lower90": 0.15,
        "metric": "product_in_aqueous",
        "query_id": "Q12",
        "truth": 0.456805371085593,
        "upper90": 0.68
      }
    ],
    "metrics": {
      "product_in_aqueous": {
        "coverage90": 1.0,
        "interval_score90": 0.28500000000000003,
        "mae": 0.03480545615798523,
        "mean_width90": 0.28500000000000003,
        "n": 12
      },
      "product_in_organic": {
        "coverage90": 1.0,
        "interval_score90": 0.285,
        "mae": 0.03480545615798524,
        "mean_width90": 0.285,
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
        "input": 373680,
        "cached_input": 321152,
        "output": 4220,
        "uncached_input": 52528
      },
      {
        "stage": "K1",
        "input": 53586,
        "cached_input": 25472,
        "output": 3090,
        "uncached_input": 28114
      },
      {
        "stage": "Q",
        "input": 67471,
        "cached_input": 31616,
        "output": 4420,
        "uncached_input": 35855
      },
      {
        "stage": "K2",
        "input": 36767,
        "cached_input": 27648,
        "output": 1537,
        "uncached_input": 9119
      }
    ],
    "total": {
      "input": 531504,
      "cached_input": 405888,
      "output": 13267,
      "uncached_input": 125616,
      "input_plus_output": 544771
    },
    "monetary_cost_usd": null
  },
  "elapsed_s": 514.0620000000054,
  "retest_batches": 0,
  "retest_operations": 0,
  "retest_replay": null,
  "english_output": true
}
```
