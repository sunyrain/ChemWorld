# PA-W04-B12-discovery-E-MisIndexed

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
| 1 | {"cost": 0.4468500018119812, "impurity_signal": 0.03752589970827103, "phase_ratio": 1.0, "product_in_aqueous": 0.014660237357020378, "product_in_organic": 0.4197867214679718, "purity": 0.9023033976554871, "recovery": 0.4295578598976135, "safety_risk": 0.04929394647479057, "score": 0.2553526759147644} |
| 2 | {"cost": 0.46285000443458557, "impurity_signal": 0.04208726808428764, "phase_ratio": 0.9997019171714783, "product_in_aqueous": 0.02075776644051075, "product_in_organic": 0.6077476143836975, "purity": 0.9225901961326599, "recovery": 0.5918118357658386, "safety_risk": 0.0840163454413414, "score": 0.41453951597213745} |
| 3 | {"cost": 0.48844999074935913, "impurity_signal": 0.04820610210299492, "phase_ratio": 0.96914142370224, "product_in_aqueous": 0.0, "product_in_organic": 0.6301302313804626, "purity": 0.9093948602676392, "recovery": 0.6156484484672546, "safety_risk": 0.10414063930511475, "score": 0.43869656324386597} |
| 4 | {"cost": 0.47244998812675476, "impurity_signal": 0.06687715649604797, "phase_ratio": 1.0, "product_in_aqueous": 0.0, "product_in_organic": 0.5599609017372131, "purity": 0.9251939058303833, "recovery": 0.55579674243927, "safety_risk": 0.11203032732009888, "score": 0.37596675753593445} |
| 5 | {"cost": 0.48844999074935913, "impurity_signal": 0.059082500636577606, "phase_ratio": 0.9829117059707642, "product_in_aqueous": 0.0, "product_in_organic": 0.5845072269439697, "purity": 0.9106931090354919, "recovery": 0.5813442468643188, "safety_risk": 0.10083600878715515, "score": 0.3985399305820465} |
| 6 | {"cost": 0.48844999074935913, "impurity_signal": 0.04620513692498207, "phase_ratio": 0.9943565726280212, "product_in_aqueous": 0.0156232425943017, "product_in_organic": 0.49587780237197876, "purity": 0.9249323606491089, "recovery": 0.508583128452301, "safety_risk": 0.09503309428691864, "score": 0.32049816846847534} |
| 7 | {"cost": 0.48844999074935913, "impurity_signal": 0.05307561904191971, "phase_ratio": 1.0, "product_in_aqueous": 0.007889077998697758, "product_in_organic": 0.6406486630439758, "purity": 0.9196967482566833, "recovery": 0.6389726400375366, "safety_risk": 0.1052730455994606, "score": 0.44376248121261597} |
| 8 | {"cost": 0.48844999074935913, "impurity_signal": 0.05235166847705841, "phase_ratio": 0.9789910912513733, "product_in_aqueous": 0.0284495260566473, "product_in_organic": 0.6138283610343933, "purity": 0.9012895226478577, "recovery": 0.6304585933685303, "safety_risk": 0.10414063930511475, "score": 0.42101001739501953} |
| 9 | {"cost": 0.46985000371932983, "impurity_signal": 0.06205926090478897, "phase_ratio": 1.0, "product_in_aqueous": 0.0, "product_in_organic": 0.6179654598236084, "purity": 0.9210666418075562, "recovery": 0.6342167258262634, "safety_risk": 0.10414063930511475, "score": 0.4252706468105316} |
| 10 | {"cost": 0.5070499777793884, "impurity_signal": 0.2083849310874939, "phase_ratio": 0.015568170696496964, "product_in_aqueous": 0.376346230506897, "product_in_organic": 0.005932251922786236, "purity": 0.6593735814094543, "recovery": 0.3893287181854248, "safety_risk": 0.1087951585650444, "score": 0.0} |
| 11 | {"cost": 0.48724165558815, "impurity_signal": 0.058362122625112534, "phase_ratio": 1.0, "product_in_aqueous": 0.0, "product_in_organic": 0.5012694001197815, "purity": 0.9236192107200623, "recovery": 0.4993285834789276, "safety_risk": 0.0949343889951706, "score": 0.32607901096343994} |
| 12 | {"cost": 0.49219998717308044, "impurity_signal": 0.06605029851198196, "phase_ratio": 0.9891050457954407, "product_in_aqueous": 0.0054099163971841335, "product_in_organic": 0.6958651542663574, "purity": 0.9081707000732422, "recovery": 0.7034053802490234, "safety_risk": 0.11035243421792984, "score": 0.4920338988304138} |

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

Observations: All 12 batches used 0.030 mol reagent and were measured by HPLC before phase separation and by final assay after retaining one phase. Under the standard 0.040 L solvent/0.040 L aqueous/0.020 L extractant condition with 300 s mixing at 600 rpm, the solvent screen with X0 showed that S0 was distinctly unfavorable: batch 1 HPLC reported product_in_organic 0.399, product_in_aqueous 0.553 and recovery 0.426. Batches 2–4 using S1, S2 and S3 respectively gave organic-product signals of 0.609, 0.598 and 0.577, with recoveries of 0.598, 0.612 and 0.577. The S2/X0 repeat, batch 8, gave 0.618 organic, 0.358 aqueous and 0.615 recovery, broadly reproducing batch 3 while showing meaningful run-to-run variation.

At fixed S2 and standard processing, changing extractant mattered. Batches 5–7 gave organic-product signals of 0.580 for X1, 0.490 for X2 and 0.643 for X3. Thus X3 was strongest and X2 weakest in this particular S2 pairing, although each had only one run. The two phase-amount perturbations produced smaller changes than mixing: aqueous-rich batch 9 (0.020 L solvent/0.060 L aqueous/0.020 L X0) gave 0.634 organic and 0.348 aqueous; solvent-rich batch 10 (0.060/0.020/0.020 L) gave 0.649 organic and 0.362 aqueous. These changes are comparable to reference-run variability and also alter composition, not merely a clean phase-volume ratio.

Mixing produced the clearest process trend. Weakly mixed batch 11 (10 s, 100 rpm) gave 0.526 organic, 0.467 aqueous and 0.500 recovery. Strongly mixed batch 12 (1200 s, 900 rpm) gave 0.717 organic, 0.308 aqueous and 0.692 recovery. The standard S2/X0 repeats lay between them at about 0.60–0.62 organic and about 0.61 recovery. This ordering supports a substantial mixing/transport effect.

Phase retention was directly tested. In the organic-retention batches, final assays generally reported product_in_organic close to the pre-separation organic signal, product_in_aqueous near zero, and final phase_ratio near 1. Batch 12, for example, finished at 0.696 organic and 0.005 aqueous. Batch 10 retained the aqueous phase instead and finished at 0.376 aqueous, 0.006 organic, phase_ratio 0.0156, purity 0.659 and impurity_signal 0.208. By contrast, organic-retention batches generally had purity near 0.90–0.93 and impurity signals near 0.04–0.07. The reported phase_ratio therefore behaves mainly as a retained-phase composition indicator; it should not be interpreted directly as an equilibrium distribution coefficient.

Inference: The target preferentially enters the organic phase for most tested pairings, but the extent depends on both the solvent–extractant pairing and mixing. S0/X0 is clearly less favorable than the other screened X0 pairings. With S2, X3 appears more favorable for target transfer than X2, indicating a pairing-specific interaction rather than independent material rankings alone. More energetic or prolonged mixing probably increases approach to the system’s attainable partition state; the weak-mixing result looks transport-limited. Retaining the organic phase is supported experimentally when the goal is to retain target and reject impurity, whereas retaining the aqueous phase loses most of the organic-partitioned target and concentrates more impurity.

Contribution of supplied information: The nominal dossier correctly identified S2 as having the strongest marginal solvent profile and made S2/X0 a rational reference condition. It also warned that marginal profiles omit solvent–extractant interactions, phase-volume response and mixing response. The experiments supplied those missing comparisons. They only partly followed the marginal expectations: S2 was strong, but S1 was similar; X3 outperformed X0 in the S2 pairing, while X2—despite favorable nominal selectivity information—gave the lowest target-in-organic signal. This discrepancy is evidence for interaction effects, possible dossier misindexing, or sampling variability rather than proof that the dossier is false.

Conjecture and remaining uncertainty: The mixing trend may reflect interphase mass-transfer kinetics, but increased conversion or another mixing-dependent process could produce the same channel changes; the data do not isolate equilibrium partition from reaction or transport. Only S2 was tested across all extractants, so most of the 4×4 pairing matrix remains unknown. X1–X3 and most volume/mixing settings lack replication, while the two S2/X0 standard runs show appreciable process scatter. The volume tests confounded aqueous amount with solvent amount and did not vary extractant volume independently. Settling time, reagent loading, multistage extraction, phase carryover and intermediate mixing intensities were not varied. Consequently, the evidence supports qualitative material, mixing and retention effects within this anonymous synthetic benchmark, but not a universal quantitative law or claims about real substances.

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
        "estimate": 0.588,
        "lower90": 0.43,
        "upper90": 0.73
      },
      "product_in_organic": {
        "estimate": 0.412,
        "lower90": 0.27,
        "upper90": 0.57
      },
      "query_id": "Q01"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.275,
        "lower90": 0.16,
        "upper90": 0.42
      },
      "product_in_organic": {
        "estimate": 0.725,
        "lower90": 0.58,
        "upper90": 0.84
      },
      "query_id": "Q02"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.551,
        "lower90": 0.35,
        "upper90": 0.75
      },
      "product_in_organic": {
        "estimate": 0.449,
        "lower90": 0.25,
        "upper90": 0.65
      },
      "query_id": "Q03"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.247,
        "lower90": 0.12,
        "upper90": 0.44
      },
      "product_in_organic": {
        "estimate": 0.753,
        "lower90": 0.56,
        "upper90": 0.88
      },
      "query_id": "Q04"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.296,
        "lower90": 0.18,
        "upper90": 0.44
      },
      "product_in_organic": {
        "estimate": 0.704,
        "lower90": 0.56,
        "upper90": 0.82
      },
      "query_id": "Q05"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.266,
        "lower90": 0.13,
        "upper90": 0.47
      },
      "product_in_organic": {
        "estimate": 0.734,
        "lower90": 0.53,
        "upper90": 0.87
      },
      "query_id": "Q06"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.152,
        "lower90": 0.08,
        "upper90": 0.27
      },
      "product_in_organic": {
        "estimate": 0.848,
        "lower90": 0.73,
        "upper90": 0.92
      },
      "query_id": "Q07"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.134,
        "lower90": 0.06,
        "upper90": 0.27
      },
      "product_in_organic": {
        "estimate": 0.866,
        "lower90": 0.73,
        "upper90": 0.94
      },
      "query_id": "Q08"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.416,
        "lower90": 0.29,
        "upper90": 0.56
      },
      "product_in_organic": {
        "estimate": 0.584,
        "lower90": 0.44,
        "upper90": 0.71
      },
      "query_id": "Q09"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.317,
        "lower90": 0.21,
        "upper90": 0.46
      },
      "product_in_organic": {
        "estimate": 0.683,
        "lower90": 0.54,
        "upper90": 0.79
      },
      "query_id": "Q10"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.213,
        "lower90": 0.12,
        "upper90": 0.36
      },
      "product_in_organic": {
        "estimate": 0.787,
        "lower90": 0.64,
        "upper90": 0.88
      },
      "query_id": "Q11"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.148,
        "lower90": 0.08,
        "upper90": 0.27
      },
      "product_in_organic": {
        "estimate": 0.852,
        "lower90": 0.73,
        "upper90": 0.92
      },
      "query_id": "Q12"
    }
  ],
  "rationale": "Predictions interpolate the pre-separation evidence on a partition-odds scale using extractant-to-other-liquid volume, observed solvent/extractant effects, and the monotonic mixing trend. Stronger mixing and more extractant shift target organic; S0/X0 at Q01's low extractant loading remains aqueous-majority. X3 exceeded X0 with S2, so Q06 is slightly favored over Q05, but its untested S0 interaction causes wider intervals. Intervals represent structural and run-to-run uncertainty, not HPLC noise."
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

No instance-level prior prediction was supplied. The supplied information was only a marginal material-property dossier, explicitly incomplete and possibly misindexed.

The least-tested self-developed law is the prediction model’s assumption that target partition odds scale directly with extractant-to-other-liquid volume, with an approximately additive correction for mixing duration and speed. Every campaign batch used 0.020 L extractant in 0.100 L total liquid, including the apparent “volume” tests in batches 9 and 10; those tests exchanged solvent and aqueous volumes without changing extractant fraction. Thus the volume-odds rule used for Q01–Q08 was extrapolated rather than experimentally established. Likewise, transferring the X3-over-X0 effect from S2 (batches 7 versus 3/8) to the untested S0/X3 pairing assumed material-effect additivity despite the report’s emphasis on pair interactions. The dossier’s marginal rankings are not decisively falsified by one observation per extractant.

2. One additional discriminating experiment

I would repeat the standard S2/X0 composition in one vessel and obtain staged HPLC measurements: first after weak mixing like batch 11, then after substantially more vigorous mixing like batch 12, keeping phase amounts and settling treatment fixed. I would examine both target phase fractions, their sum relative to initial inventory, impurity signal, and purity.

The leading mass-transfer explanation predicts that added mixing will raise the organic fraction by approximately the decrease in the aqueous fraction, leaving total target accounting and impurity chemistry substantially unchanged and eventually approaching a plateau. An alternative mixing-dependent reaction or degradation explanation predicts a change in total target accounting, impurity signal, or purity rather than a nearly conservative redistribution. A large dependence on settling or unstable phase-ratio readings would instead favor emulsion or sampling carryover. Conservative redistribution would strengthen the transfer interpretation; nonconservative target or impurity changes would make the chemical-change alternative more credible.

3. Underused evidence, reliability, and consistency

The near-unity sums of the two pre-separation target channels were underused; they support redistribution more directly than the recovery channel does. The pre-separation phase_ratio measurements, all near the fixed 0.20 extractant fraction, also reveal that batches 9 and 10 did not actually test different extractant fractions. The close correspondence between pre-separation organic signal and the organic-retained final assay was useful confirmation but could have been quantified more explicitly. Conversely, variability between nominally repeated S2/X0 batches 3 and 8 should have carried more weight when setting predictive intervals. The nominal marginal dossier was also underused when extrapolating to S0/X3, where it points in a different direction from the single S2 extractant comparison.

The least reliable predictions are Q03, Q04 and Q06 because S0/X3 was never tested. Q01–Q04 also extrapolate to extractant fractions outside the campaign. Q05–Q08 depend strongly on the unvalidated volume law, while Q11–Q12 rely on separating speed from duration using only batches 11, 3/8 and 12. The Q05-versus-Q06 decision is therefore especially fragile. Q01’s retention decision is also uncertain because its organic-fraction interval crossed 0.5.

There is no direct numerical contradiction between the sealed report and predictions, but there is a clear tension: the report said phase-volume effects were confounded and rejected a universal quantitative law, whereas the predictions imposed a specific volume-odds law to answer out-of-support queries. The predictions also selected Q06 even though the report emphasized unmeasured pair interactions; their rationale acknowledged this uncertainty, but the categorical decision was stronger than the evidence. Some intervals, particularly for the extreme-volume and unseen-pair queries, were likely too narrow. These are retrospective assessments of the sealed outputs, not revisions to them.

## Evaluation and resource use

```json
{
  "arm": "MisIndexed",
  "budget": 12,
  "goal": "discovery",
  "locus": "E",
  "system": "PA",
  "unit_id": "PA-W04-B12-discovery-E-MisIndexed",
  "world": {
    "world_id": "PA-W04",
    "world_interventions": [
      {
        "axis_id": "partition.phase-volume-ratio",
        "mode": "extrapolation",
        "severity": 0.8
      }
    ],
    "world_seed": 3
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
        "absolute_error": 0.03690140773366779,
        "estimate": 0.412,
        "lower90": 0.27,
        "metric": "product_in_organic",
        "query_id": "Q01",
        "truth": 0.3750985922663322,
        "upper90": 0.57
      },
      {
        "absolute_error": 0.018578595147174415,
        "estimate": 0.725,
        "lower90": 0.58,
        "metric": "product_in_organic",
        "query_id": "Q02",
        "truth": 0.7064214048528256,
        "upper90": 0.84
      },
      {
        "absolute_error": 0.19708555842491376,
        "estimate": 0.449,
        "lower90": 0.25,
        "metric": "product_in_organic",
        "query_id": "Q03",
        "truth": 0.6460855584249138,
        "upper90": 0.65
      },
      {
        "absolute_error": 0.1271891278701497,
        "estimate": 0.753,
        "lower90": 0.56,
        "metric": "product_in_organic",
        "query_id": "Q04",
        "truth": 0.8801891278701497,
        "upper90": 0.88
      },
      {
        "absolute_error": 0.018234405793239317,
        "estimate": 0.704,
        "lower90": 0.56,
        "metric": "product_in_organic",
        "query_id": "Q05",
        "truth": 0.6857655942067606,
        "upper90": 0.82
      },
      {
        "absolute_error": 0.13572383567995183,
        "estimate": 0.734,
        "lower90": 0.53,
        "metric": "product_in_organic",
        "query_id": "Q06",
        "truth": 0.8697238356799518,
        "upper90": 0.87
      },
      {
        "absolute_error": 0.001851197624585077,
        "estimate": 0.848,
        "lower90": 0.73,
        "metric": "product_in_organic",
        "query_id": "Q07",
        "truth": 0.849851197624585,
        "upper90": 0.92
      },
      {
        "absolute_error": 0.0054783188061390264,
        "estimate": 0.866,
        "lower90": 0.73,
        "metric": "product_in_organic",
        "query_id": "Q08",
        "truth": 0.860521681193861,
        "upper90": 0.94
      },
      {
        "absolute_error": 0.03919980713234916,
        "estimate": 0.584,
        "lower90": 0.44,
        "metric": "product_in_organic",
        "query_id": "Q09",
        "truth": 0.5448001928676508,
        "upper90": 0.71
      },
      {
        "absolute_error": 0.02286885762509161,
        "estimate": 0.683,
        "lower90": 0.54,
        "metric": "product_in_organic",
        "query_id": "Q10",
        "truth": 0.6601311423749084,
        "upper90": 0.79
      },
      {
        "absolute_error": 0.002063875424474726,
        "estimate": 0.787,
        "lower90": 0.64,
        "metric": "product_in_organic",
        "query_id": "Q11",
        "truth": 0.7890638754244748,
        "upper90": 0.88
      },
      {
        "absolute_error": 0.005493504315950748,
        "estimate": 0.852,
        "lower90": 0.73,
        "metric": "product_in_organic",
        "query_id": "Q12",
        "truth": 0.8465064956840492,
        "upper90": 0.92
      },
      {
        "absolute_error": 0.03690140773366779,
        "estimate": 0.588,
        "lower90": 0.43,
        "metric": "product_in_aqueous",
        "query_id": "Q01",
        "truth": 0.6249014077336678,
        "upper90": 0.73
      },
      {
        "absolute_error": 0.018578595147174415,
        "estimate": 0.275,
        "lower90": 0.16,
        "metric": "product_in_aqueous",
        "query_id": "Q02",
        "truth": 0.29357859514717444,
        "upper90": 0.42
      },
      {
        "absolute_error": 0.19708555842491393,
        "estimate": 0.551,
        "lower90": 0.35,
        "metric": "product_in_aqueous",
        "query_id": "Q03",
        "truth": 0.3539144415750861,
        "upper90": 0.75
      },
      {
        "absolute_error": 0.12718912787014966,
        "estimate": 0.247,
        "lower90": 0.12,
        "metric": "product_in_aqueous",
        "query_id": "Q04",
        "truth": 0.11981087212985034,
        "upper90": 0.44
      },
      {
        "absolute_error": 0.018234405793239317,
        "estimate": 0.296,
        "lower90": 0.18,
        "metric": "product_in_aqueous",
        "query_id": "Q05",
        "truth": 0.3142344057932393,
        "upper90": 0.44
      },
      {
        "absolute_error": 0.13572383567995192,
        "estimate": 0.266,
        "lower90": 0.13,
        "metric": "product_in_aqueous",
        "query_id": "Q06",
        "truth": 0.1302761643200481,
        "upper90": 0.47
      },
      {
        "absolute_error": 0.001851197624585077,
        "estimate": 0.152,
        "lower90": 0.08,
        "metric": "product_in_aqueous",
        "query_id": "Q07",
        "truth": 0.15014880237541492,
        "upper90": 0.27
      },
      {
        "absolute_error": 0.005478318806139082,
        "estimate": 0.134,
        "lower90": 0.06,
        "metric": "product_in_aqueous",
        "query_id": "Q08",
        "truth": 0.1394783188061391,
        "upper90": 0.27
      },
      {
        "absolute_error": 0.03919980713234922,
        "estimate": 0.416,
        "lower90": 0.29,
        "metric": "product_in_aqueous",
        "query_id": "Q09",
        "truth": 0.4551998071323492,
        "upper90": 0.56
      },
      {
        "absolute_error": 0.02286885762509161,
        "estimate": 0.317,
        "lower90": 0.21,
        "metric": "product_in_aqueous",
        "query_id": "Q10",
        "truth": 0.3398688576250916,
        "upper90": 0.46
      },
      {
        "absolute_error": 0.0020638754244747537,
        "estimate": 0.213,
        "lower90": 0.12,
        "metric": "product_in_aqueous",
        "query_id": "Q11",
        "truth": 0.21093612457552524,
        "upper90": 0.36
      },
      {
        "absolute_error": 0.00549350431595072,
        "estimate": 0.148,
        "lower90": 0.08,
        "metric": "product_in_aqueous",
        "query_id": "Q12",
        "truth": 0.1534935043159507,
        "upper90": 0.27
      }
    ],
    "metrics": {
      "product_in_aqueous": {
        "coverage90": 0.9166666666666666,
        "interval_score90": 0.2694818797835828,
        "mae": 0.050889040964807286,
        "mean_width90": 0.26916666666666667,
        "n": 12
      },
      "product_in_organic": {
        "coverage90": 0.9166666666666666,
        "interval_score90": 0.2694818797835828,
        "mae": 0.050889040964807265,
        "mean_width90": 0.26916666666666667,
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
        "input": 331985,
        "cached_input": 304512,
        "output": 4273,
        "uncached_input": 27473
      },
      {
        "stage": "K1",
        "input": 28817,
        "cached_input": 0,
        "output": 2167,
        "uncached_input": 28817
      },
      {
        "stage": "Q",
        "input": 106555,
        "cached_input": 68352,
        "output": 5277,
        "uncached_input": 38203
      },
      {
        "stage": "K2",
        "input": 38978,
        "cached_input": 28672,
        "output": 1923,
        "uncached_input": 10306
      }
    ],
    "total": {
      "input": 506335,
      "cached_input": 401536,
      "output": 13640,
      "uncached_input": 104799,
      "input_plus_output": 519975
    },
    "monetary_cost_usd": null
  },
  "elapsed_s": 532.1879999999946,
  "retest_batches": 0,
  "retest_operations": 0,
  "retest_replay": null,
  "english_output": true
}
```
