# PA-W04-B24-discovery-E-MisIndexed

Development experiment; one independent source session.

Status: completed; completed batches: 24/24; posttests: 3/3.

## Research assignment

You are an autonomous scientist studying two-phase partition in a simulated lab.
Use only chemworld_lab and public_numerics. No filesystem, network, repository, hidden physics,
or general code execution is available. First read material_information. Follow research_goal.
Conduct 24 independent batches from the same initial mixture; conditions and repetition are
your choice. You have 24 additional instrument uses shared across batches and 24 final assays.
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


Discover and test a predictive explanation of target partition between the two phases, including material pairing, phase amounts and mixing. Choose 24 experiments freely. Explain evidence, alternatives and limits. Predict new conditions and phase-retention decisions after the campaign. Native score is not this task's objective. No best recipe, prescribed law, or belief checkpoints are required.

## Batch outcomes

| Batch | Final measured outcomes |
| --- | --- |
| 1 | {"cost": 0.41635000705718994, "impurity_signal": 0.03752589970827103, "phase_ratio": 1.0, "product_in_aqueous": 0.014660237357020378, "product_in_organic": 0.4197867214679718, "purity": 0.9023033976554871, "recovery": 0.4295578598976135, "safety_risk": 0.04929394647479057, "score": 0.2553526759147644} |
| 2 | {"cost": 0.41635000705718994, "impurity_signal": 0.04785703867673874, "phase_ratio": 0.9997019171714783, "product_in_aqueous": 0.02075776644051075, "product_in_organic": 0.64407879114151, "purity": 0.9195711016654968, "recovery": 0.6281429529190063, "safety_risk": 0.06374748796224594, "score": 0.4454209804534912} |
| 3 | {"cost": 0.41635000705718994, "impurity_signal": 0.039180830121040344, "phase_ratio": 0.96914142370224, "product_in_aqueous": 0.0, "product_in_organic": 0.5361047983169556, "purity": 0.9092122316360474, "recovery": 0.5216229557991028, "safety_risk": 0.05571334436535835, "score": 0.35877493023872375} |
| 4 | {"cost": 0.41635000705718994, "impurity_signal": 0.0850253701210022, "phase_ratio": 1.0, "product_in_aqueous": 0.0, "product_in_organic": 0.6464963555335999, "purity": 0.9118257761001587, "recovery": 0.6423321962356567, "safety_risk": 0.0657242015004158, "score": 0.44952189922332764} |
| 5 | {"cost": 0.4323500096797943, "impurity_signal": 0.061346977949142456, "phase_ratio": 0.9829117059707642, "product_in_aqueous": 0.0, "product_in_organic": 0.5990756750106812, "purity": 0.9094410538673401, "recovery": 0.5959126949310303, "safety_risk": 0.0840163454413414, "score": 0.41092315316200256} |
| 6 | {"cost": 0.4323500096797943, "impurity_signal": 0.04888040944933891, "phase_ratio": 0.9943565726280212, "product_in_aqueous": 0.0156232425943017, "product_in_organic": 0.45591554045677185, "purity": 0.9144634008407593, "recovery": 0.4686208665370941, "safety_risk": 0.07500677555799484, "score": 0.2865302264690399} |
| 7 | {"cost": 0.4323500096797943, "impurity_signal": 0.05870553106069565, "phase_ratio": 1.0, "product_in_aqueous": 0.007889077998697758, "product_in_organic": 0.645618736743927, "purity": 0.9130380153656006, "recovery": 0.6439427137374878, "safety_risk": 0.08810511231422424, "score": 0.44798699021339417} |
| 8 | {"cost": 0.4323500096797943, "impurity_signal": 0.040106937289237976, "phase_ratio": 0.9789910912513733, "product_in_aqueous": 0.0284495260566473, "product_in_organic": 0.5398989319801331, "purity": 0.9089815616607666, "recovery": 0.55652916431427, "safety_risk": 0.08016403019428253, "score": 0.3581700026988983} |
| 9 | {"cost": 0.45794999599456787, "impurity_signal": 0.06205926090478897, "phase_ratio": 1.0, "product_in_aqueous": 0.0, "product_in_organic": 0.6179654598236084, "purity": 0.9210666418075562, "recovery": 0.6342167258262634, "safety_risk": 0.10414063930511475, "score": 0.4252706468105316} |
| 10 | {"cost": 0.45794999599456787, "impurity_signal": 0.058490123599767685, "phase_ratio": 1.0, "product_in_aqueous": 0.0009292740724049509, "product_in_organic": 0.5906593799591064, "purity": 0.926535427570343, "recovery": 0.5986389517784119, "safety_risk": 0.10083600878715515, "score": 0.4019675552845001} |
| 11 | {"cost": 0.45794999599456787, "impurity_signal": 0.05237202346324921, "phase_ratio": 1.0, "product_in_aqueous": 0.0, "product_in_organic": 0.5090059638023376, "purity": 0.9348352551460266, "recovery": 0.5070651173591614, "safety_risk": 0.09503309428691864, "score": 0.33265507221221924} |
| 12 | {"cost": 0.45794999599456787, "impurity_signal": 0.05551457032561302, "phase_ratio": 0.9891050457954407, "product_in_aqueous": 0.0054099163971841335, "product_in_organic": 0.6447298526763916, "purity": 0.9151456952095032, "recovery": 0.6522700786590576, "safety_risk": 0.1052730455994606, "score": 0.4485688805580139} |
| 13 | {"cost": 0.4419499933719635, "impurity_signal": 0.05565223842859268, "phase_ratio": 0.9946475625038147, "product_in_aqueous": 0.0, "product_in_organic": 0.5642699003219604, "purity": 0.9317703247070312, "recovery": 0.5660829544067383, "safety_risk": 0.11203032732009888, "score": 0.38016465306282043} |
| 14 | {"cost": 0.4419499933719635, "impurity_signal": 0.07162868976593018, "phase_ratio": 0.9981326460838318, "product_in_aqueous": 0.0056363963522017, "product_in_organic": 0.6401615142822266, "purity": 0.9155886173248291, "recovery": 0.6457698345184326, "safety_risk": 0.11759418994188309, "score": 0.44376036524772644} |
| 15 | {"cost": 0.4419499933719635, "impurity_signal": 0.05909335985779762, "phase_ratio": 1.0, "product_in_aqueous": 0.005629774183034897, "product_in_organic": 0.5970768332481384, "purity": 0.9110872745513916, "recovery": 0.6266185641288757, "safety_risk": 0.11551742255687714, "score": 0.40695229172706604} |
| 16 | {"cost": 0.4419499933719635, "impurity_signal": 0.05772729218006134, "phase_ratio": 1.0, "product_in_aqueous": 0.0, "product_in_organic": 0.4731772243976593, "purity": 0.905764102935791, "recovery": 0.49222126603126526, "safety_risk": 0.10659254342317581, "score": 0.30220064520835876} |
| 17 | {"cost": 0.45794999599456787, "impurity_signal": 0.04953175038099289, "phase_ratio": 1.0, "product_in_aqueous": 0.0, "product_in_organic": 0.63857102394104, "purity": 0.9116791486740112, "recovery": 0.65184086561203, "safety_risk": 0.1052730455994606, "score": 0.4427853524684906} |
| 18 | {"cost": 0.45794999599456787, "impurity_signal": 0.21042177081108093, "phase_ratio": 0.0, "product_in_aqueous": 0.36525046825408936, "product_in_organic": 0.0, "purity": 0.6406936049461365, "recovery": 0.3508070409297943, "safety_risk": 0.09466501325368881, "score": 0.0} |
| 19 | {"cost": 0.4573499858379364, "impurity_signal": 0.15541549026966095, "phase_ratio": 1.0, "product_in_aqueous": 0.0, "product_in_organic": 0.8571054339408875, "purity": 0.8482134938240051, "recovery": 0.8319510221481323, "safety_risk": 0.08561046421527863, "score": 0.6285396218299866} |
| 20 | {"cost": 0.451200008392334, "impurity_signal": 0.034799348562955856, "phase_ratio": 0.9952297806739807, "product_in_aqueous": 0.004928150679916143, "product_in_organic": 0.3153468370437622, "purity": 0.9559805989265442, "recovery": 0.31032705307006836, "safety_risk": 0.17911264300346375, "score": 0.16802901029586792} |
| 21 | {"cost": 0.45682498812675476, "impurity_signal": 0.041924793273210526, "phase_ratio": 1.0, "product_in_aqueous": 0.011142526753246784, "product_in_organic": 0.5218324065208435, "purity": 0.919951319694519, "recovery": 0.5405274033546448, "safety_risk": 0.09654103219509125, "score": 0.3424432873725891} |
| 22 | {"cost": 0.45682498812675476, "impurity_signal": 0.042771462351083755, "phase_ratio": 1.0, "product_in_aqueous": 0.0, "product_in_organic": 0.5346643924713135, "purity": 0.920394778251648, "recovery": 0.5256571769714355, "safety_risk": 0.0969034805893898, "score": 0.35446473956108093} |
| 23 | {"cost": 0.4641999900341034, "impurity_signal": 0.04911866411566734, "phase_ratio": 0.990826427936554, "product_in_aqueous": 0.0, "product_in_organic": 0.668234646320343, "purity": 0.9141287207603455, "recovery": 0.6696600914001465, "safety_risk": 0.10827073454856873, "score": 0.46891680359840393} |
| 24 | {"cost": 0.4641999900341034, "impurity_signal": 0.07585160434246063, "phase_ratio": 0.9959251880645752, "product_in_aqueous": 0.008013817481696606, "product_in_organic": 0.7273409962654114, "purity": 0.9120369553565979, "recovery": 0.7215451002120972, "safety_risk": 0.11331961303949356, "score": 0.5178459286689758} |

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

The controlled material screen was batches 1–16. Each used 0.020 mol reagent, 0.040 L solvent, 0.040 L aqueous phase, 0.020 L extractant, 300 s mixing at 600 rpm, and 300 s settling. Only the solvent–extractant pairing changed. Pre-separation HPLC showed substantial, reproducible-scale differences relative to its stated ±0.015 uncertainties. Examples include:
• Batch 1, S0–X0: organic target 0.399 and aqueous target 0.553 (organic/aqueous ≈0.72).
• Batch 4, S0–X3: 0.664 organic and 0.327 aqueous (ratio ≈2.03).
• Batch 6, S1–X1: 0.450 organic and 0.527 aqueous (≈0.85).
• Batch 7, S1–X2: 0.648 organic and 0.333 aqueous (≈1.95).
• Batch 12, S2–X3: 0.666 organic and 0.359 aqueous (≈1.85).
• Batch 16, S3–X3: 0.497 organic and 0.515 aqueous (≈0.97).
Across the complete matrix, organic/aqueous ratios ranged approximately 0.72–2.03. Thus several differences are much larger than analytical noise.

Solvent marginal mean organic signals across the four extractants were approximately S0 0.553, S1 0.559, S2 0.611, and S3 0.571. Extractant marginal means across solvents were X0 0.545, X1 0.583, X2 0.573, and X3 0.593. These averages conceal strong crossovers: X3 was excellent with S0 and S2 but weak with S3, while X2 was strong with S1 but less so with S0 or S2.

The organic-retention operation behaved consistently with physical phase selection. In batches 1–16, the post-separation final-assay organic target differed from the corresponding pre-separation HPLC organic target by only about −0.003 mean bias and 0.014 mean absolute difference. Examples are batch 2, 0.645 before separation versus 0.644 final, and batch 12, 0.666 versus 0.645. Final aqueous signals after retaining organic were generally near zero, and the reported phase_ratio changed from roughly 0.17–0.22 before separation to roughly 0.97–1.00 afterward. Consequently, that phase_ratio channel appears primarily to describe retained-phase composition or holdup, not the target’s equilibrium distribution coefficient.

Purity was comparatively stable in the material screen (roughly 0.895–0.950 by HPLC), while impurity signals ranged about 0.029–0.077. Pairing therefore changed target allocation more dramatically than bulk purity, although impurity tradeoffs remained.

Batches 17–24 extended the screen with a repeat, alternate aqueous retention, phase-amount extremes, and a mixing-duration/speed corner design. A specific endpoint contrast is batch 12 versus batch 24: both used S2–X3 and the baseline phase amounts, but batch 24 used 1800 s at 1200 rpm. Its final assay gave organic target 0.727, recovery 0.722, impurity 0.0759, and purity 0.912, compared with batch 12’s organic target 0.645, recovery 0.652, impurity 0.0555, and purity 0.915. The target and recovery increases greatly exceed the final-assay ±0.01 noise scale, while impurity also increased.

INFERENCE

A compact explanation is a pair-specific partition preference combined with incomplete or condition-dependent mass transfer. Solvent and extractant jointly determine the target’s effective affinity for the organic phase; neither material has a context-independent ranking. Mixing duration and speed control approach to the accessible partition state, interfacial transport, or phase disengagement. Separation then largely preserves whichever phase is retained. Because final recovery closely follows the retained organic target signal, recovery in these assays is phase-specific rather than a measure of total target present in both phases.

The batch-12/batch-24 contrast supports mixing-condition sensitivity and is compatible with improved transfer toward the organic phase under stronger, longer mixing. The simultaneous impurity increase suggests that stronger mixing may enhance nonselective co-transfer as well. However, duration and speed both changed in that particular contrast, so it does not alone identify which factor dominates.

SUPPLIED INFORMATION VERSUS EXPERIMENTS

The supplied dossier was useful as a prior: it suggested S2 had the strongest solvent-panel product-distribution tendency and described X0–X2 as stronger marginal extractants than X3 in some respects. The observed solvent averages broadly supported S2. The extractant result did not reduce to the dossier’s marginal ordering: X3 had the highest experimental average organic signal and produced both excellent and poor pairs. This is consistent with the dossier’s explicit warning that marginal profiles omit the solvent–extractant interaction table and may be incomplete or misindexed. The full 4×4 experiment, rather than equal index labels or marginal properties, established the interaction and crossover behavior. The labels remain anonymous benchmark identifiers; no real chemical identity or property is inferred.

COMPETING EXPLANATIONS AND LIMITS

The organic and aqueous channels may reflect more than equilibrium partitioning. Pair-dependent reaction yield, target speciation, emulsion or entrainment, unequal phase sampling, or matrix-dependent instrument response could mimic changes in a distribution coefficient. Likewise, the batch-24 mixing effect could represent slower equilibration, altered conversion, better sampling, temporary dispersion, or co-extraction rather than a changed thermodynamic equilibrium. The higher impurity signal under that condition is compatible with several of these alternatives.

Most conditions were single runs. Material comparisons are well covered combinatorially but not replicated extensively; phase-volume and mixing corners have much less replication. The study mainly used one reagent loading, one addition order, one baseline settling time, and a bounded range of phase volumes and mixing conditions. Therefore the evidence supports interpolation within this synthetic campaign more strongly than extrapolation to other loadings, orders, settling regimes, repeated extractions, or real substances. A quantitative equilibrium law, independent speed and duration effects, and a definitive phase-volume scaling rule remain uncertain.

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
        "estimate": 0.64,
        "lower90": 0.53,
        "upper90": 0.75
      },
      "product_in_organic": {
        "estimate": 0.36,
        "lower90": 0.25,
        "upper90": 0.47
      },
      "query_id": "Q01"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.32,
        "lower90": 0.23,
        "upper90": 0.42
      },
      "product_in_organic": {
        "estimate": 0.68,
        "lower90": 0.58,
        "upper90": 0.77
      },
      "query_id": "Q02"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.38,
        "lower90": 0.28,
        "upper90": 0.49
      },
      "product_in_organic": {
        "estimate": 0.62,
        "lower90": 0.51,
        "upper90": 0.72
      },
      "query_id": "Q03"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.14,
        "lower90": 0.08,
        "upper90": 0.22
      },
      "product_in_organic": {
        "estimate": 0.86,
        "lower90": 0.78,
        "upper90": 0.92
      },
      "query_id": "Q04"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.34,
        "lower90": 0.26,
        "upper90": 0.43
      },
      "product_in_organic": {
        "estimate": 0.66,
        "lower90": 0.57,
        "upper90": 0.74
      },
      "query_id": "Q05"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.15,
        "lower90": 0.1,
        "upper90": 0.22
      },
      "product_in_organic": {
        "estimate": 0.85,
        "lower90": 0.78,
        "upper90": 0.9
      },
      "query_id": "Q06"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.17,
        "lower90": 0.11,
        "upper90": 0.24
      },
      "product_in_organic": {
        "estimate": 0.83,
        "lower90": 0.76,
        "upper90": 0.89
      },
      "query_id": "Q07"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.16,
        "lower90": 0.1,
        "upper90": 0.23
      },
      "product_in_organic": {
        "estimate": 0.84,
        "lower90": 0.77,
        "upper90": 0.9
      },
      "query_id": "Q08"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.42,
        "lower90": 0.33,
        "upper90": 0.52
      },
      "product_in_organic": {
        "estimate": 0.58,
        "lower90": 0.48,
        "upper90": 0.67
      },
      "query_id": "Q09"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.35,
        "lower90": 0.27,
        "upper90": 0.44
      },
      "product_in_organic": {
        "estimate": 0.65,
        "lower90": 0.56,
        "upper90": 0.73
      },
      "query_id": "Q10"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.21,
        "lower90": 0.14,
        "upper90": 0.29
      },
      "product_in_organic": {
        "estimate": 0.79,
        "lower90": 0.71,
        "upper90": 0.86
      },
      "query_id": "Q11"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.17,
        "lower90": 0.11,
        "upper90": 0.24
      },
      "product_in_organic": {
        "estimate": 0.83,
        "lower90": 0.76,
        "upper90": 0.89
      },
      "query_id": "Q12"
    }
  ],
  "rationale": "I treated the two target fractions as complementary and used the controlled 4×4 screen to estimate pair-specific organic affinity, scaled its odds by extractant-to-aqueous volume ratio, and applied a modest saturating mixing adjustment supported by the stronger-mixing S2–X3 result. The intervals represent uncertainty in that volume/mixing extrapolation, not random HPLC noise. Q01 is predicted aqueous-dominant, while replacing X0 with X3 makes Q06 more organic-rich than Q05."
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

1. No instance-level prior was supplied; only a marginal material dossier was provided. The least-tested self-developed law is my prediction rule that pair-specific partition odds scale simply with extractant-to-aqueous volume ratio, plus a modest saturating correction for mixing. Batches 1–16 identify material interactions at one common volume and mixing condition, but do not establish that functional form. Batches 19–20 were intended to test volume extremes, while batches 21–24 tested mixing corners, yet I did not quantitatively incorporate most of those outcomes. The dossier’s marginal rankings are not necessarily wrong, because it explicitly omitted pair interactions.

2. I would run one sequential time-course batch using S2–X3 and the same phase amounts as batches 12 and 24. After standardized settling, I would take small HPLC samples after cumulative mixing at 30, 300, 900, and 1800 seconds while holding speed fixed, measuring target in both phases, their sum, impurity, purity, and phase ratio. A monotonic organic-fraction approach to a plateau with nearly constant total target and purity would strengthen the mass-transfer-to-equilibrium explanation. Changes in total target, purity, or impurity concurrent with redistribution would instead favor reaction/speciation or degradation. A transient organic increase that reverses with additional settling would favor dispersion, entrainment, or sampling bias. A flat trajectory would weaken the claimed mixing effect and suggest that the batch-12/batch-24 difference reflects another uncontrolled factor.

3. The most underused evidence was the late diagnostic block: the repeat and alternate retention in batches 17–18, the phase-volume contrasts in batches 19–20, and the other mixing corners in batches 21–23. I also underused raw chromatographic artifacts and the relationship among impurity, purity, total target signal, and phase ratio. The least reliable predictions are Q01–Q04, because they extrapolate the unverified volume-scaling law, and Q09–Q12, especially low-speed Q11, because speed and duration effects were not cleanly quantified. Q05 versus Q06 is comparatively better supported by the large S0–X0 versus S0–X3 contrast in batches 1 and 4, although its new amounts and mixing still require extrapolation.

There is a real tension, though not a post-truth correction, between the sealed report and predictions: the report explicitly called phase-volume scaling and separate speed/duration effects uncertain, whereas the predictions necessarily imposed specific volume-odds and mixing rules. Their intervals attempted to acknowledge that uncertainty but may be too narrow. The predictions also used batch 24’s post-separation final assay as evidence for a pre-separation mixing effect; batches 1–16 showed that retained-organic final assays usually tracked pre-separation organic HPLC closely, but that proxy is not guaranteed under every condition. Finally, forcing the predicted phase fractions to be complementary assumes essentially all initial target remains represented in the two measured phases; the screening data support that approximately, but conversion, degradation, or inaccessible target would violate it.

## Evaluation and resource use

```json
{
  "arm": "MisIndexed",
  "budget": 24,
  "goal": "discovery",
  "locus": "E",
  "system": "PA",
  "unit_id": "PA-W04-B24-discovery-E-MisIndexed",
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
  "completed_batches": 24,
  "operations": 240,
  "posttests_completed": 3,
  "exact_replay": {
    "checked_steps": 240,
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
        "mae": 0.01970254682385099,
        "coverage90": 1.0,
        "mean_width90": 0.1625,
        "interval_score90": 0.1625
      },
      "product_in_aqueous": {
        "n": 12,
        "mae": 0.019702546823851013,
        "coverage90": 1.0,
        "mean_width90": 0.1625,
        "interval_score90": 0.1625
      }
    },
    "details": [
      {
        "query_id": "Q01",
        "metric": "product_in_organic",
        "estimate": 0.36,
        "lower90": 0.25,
        "upper90": 0.47,
        "truth": 0.3750985922663322,
        "absolute_error": 0.0150985922663322
      },
      {
        "query_id": "Q02",
        "metric": "product_in_organic",
        "estimate": 0.68,
        "lower90": 0.58,
        "upper90": 0.77,
        "truth": 0.7064214048528256,
        "absolute_error": 0.026421404852825514
      },
      {
        "query_id": "Q03",
        "metric": "product_in_organic",
        "estimate": 0.62,
        "lower90": 0.51,
        "upper90": 0.72,
        "truth": 0.6460855584249138,
        "absolute_error": 0.02608555842491378
      },
      {
        "query_id": "Q04",
        "metric": "product_in_organic",
        "estimate": 0.86,
        "lower90": 0.78,
        "upper90": 0.92,
        "truth": 0.8801891278701497,
        "absolute_error": 0.020189127870149703
      },
      {
        "query_id": "Q05",
        "metric": "product_in_organic",
        "estimate": 0.66,
        "lower90": 0.57,
        "upper90": 0.74,
        "truth": 0.6857655942067606,
        "absolute_error": 0.02576559420676061
      },
      {
        "query_id": "Q06",
        "metric": "product_in_organic",
        "estimate": 0.85,
        "lower90": 0.78,
        "upper90": 0.9,
        "truth": 0.8697238356799518,
        "absolute_error": 0.01972383567995184
      },
      {
        "query_id": "Q07",
        "metric": "product_in_organic",
        "estimate": 0.83,
        "lower90": 0.76,
        "upper90": 0.89,
        "truth": 0.849851197624585,
        "absolute_error": 0.019851197624585093
      },
      {
        "query_id": "Q08",
        "metric": "product_in_organic",
        "estimate": 0.84,
        "lower90": 0.77,
        "upper90": 0.9,
        "truth": 0.860521681193861,
        "absolute_error": 0.020521681193860997
      },
      {
        "query_id": "Q09",
        "metric": "product_in_organic",
        "estimate": 0.58,
        "lower90": 0.48,
        "upper90": 0.67,
        "truth": 0.5448001928676508,
        "absolute_error": 0.03519980713234916
      },
      {
        "query_id": "Q10",
        "metric": "product_in_organic",
        "estimate": 0.65,
        "lower90": 0.56,
        "upper90": 0.73,
        "truth": 0.6601311423749084,
        "absolute_error": 0.01013114237490842
      },
      {
        "query_id": "Q11",
        "metric": "product_in_organic",
        "estimate": 0.79,
        "lower90": 0.71,
        "upper90": 0.86,
        "truth": 0.7890638754244748,
        "absolute_error": 0.0009361245755252767
      },
      {
        "query_id": "Q12",
        "metric": "product_in_organic",
        "estimate": 0.83,
        "lower90": 0.76,
        "upper90": 0.89,
        "truth": 0.8465064956840492,
        "absolute_error": 0.01650649568404927
      },
      {
        "query_id": "Q01",
        "metric": "product_in_aqueous",
        "estimate": 0.64,
        "lower90": 0.53,
        "upper90": 0.75,
        "truth": 0.6249014077336678,
        "absolute_error": 0.015098592266332256
      },
      {
        "query_id": "Q02",
        "metric": "product_in_aqueous",
        "estimate": 0.32,
        "lower90": 0.23,
        "upper90": 0.42,
        "truth": 0.29357859514717444,
        "absolute_error": 0.02642140485282557
      },
      {
        "query_id": "Q03",
        "metric": "product_in_aqueous",
        "estimate": 0.38,
        "lower90": 0.28,
        "upper90": 0.49,
        "truth": 0.3539144415750861,
        "absolute_error": 0.02608555842491389
      },
      {
        "query_id": "Q04",
        "metric": "product_in_aqueous",
        "estimate": 0.14,
        "lower90": 0.08,
        "upper90": 0.22,
        "truth": 0.11981087212985034,
        "absolute_error": 0.020189127870149676
      },
      {
        "query_id": "Q05",
        "metric": "product_in_aqueous",
        "estimate": 0.34,
        "lower90": 0.26,
        "upper90": 0.43,
        "truth": 0.3142344057932393,
        "absolute_error": 0.025765594206760722
      },
      {
        "query_id": "Q06",
        "metric": "product_in_aqueous",
        "estimate": 0.15,
        "lower90": 0.1,
        "upper90": 0.22,
        "truth": 0.1302761643200481,
        "absolute_error": 0.019723835679951895
      },
      {
        "query_id": "Q07",
        "metric": "product_in_aqueous",
        "estimate": 0.17,
        "lower90": 0.11,
        "upper90": 0.24,
        "truth": 0.15014880237541492,
        "absolute_error": 0.019851197624585093
      },
      {
        "query_id": "Q08",
        "metric": "product_in_aqueous",
        "estimate": 0.16,
        "lower90": 0.1,
        "upper90": 0.23,
        "truth": 0.1394783188061391,
        "absolute_error": 0.020521681193860913
      },
      {
        "query_id": "Q09",
        "metric": "product_in_aqueous",
        "estimate": 0.42,
        "lower90": 0.33,
        "upper90": 0.52,
        "truth": 0.4551998071323492,
        "absolute_error": 0.035199807132349215
      },
      {
        "query_id": "Q10",
        "metric": "product_in_aqueous",
        "estimate": 0.35,
        "lower90": 0.27,
        "upper90": 0.44,
        "truth": 0.3398688576250916,
        "absolute_error": 0.010131142374908364
      },
      {
        "query_id": "Q11",
        "metric": "product_in_aqueous",
        "estimate": 0.21,
        "lower90": 0.14,
        "upper90": 0.29,
        "truth": 0.21093612457552524,
        "absolute_error": 0.000936124575525249
      },
      {
        "query_id": "Q12",
        "metric": "product_in_aqueous",
        "estimate": 0.17,
        "lower90": 0.11,
        "upper90": 0.24,
        "truth": 0.1534935043159507,
        "absolute_error": 0.0165064956840493
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
        "input": 992221,
        "cached_input": 947200,
        "output": 4343,
        "uncached_input": 45021
      },
      {
        "stage": "K1",
        "input": 135204,
        "cached_input": 88448,
        "output": 4202,
        "uncached_input": 46756
      },
      {
        "stage": "Q",
        "input": 51536,
        "cached_input": 0,
        "output": 2764,
        "uncached_input": 51536
      },
      {
        "stage": "K2",
        "input": 56182,
        "cached_input": 54144,
        "output": 650,
        "uncached_input": 2038
      }
    ],
    "total": {
      "input": 1235143,
      "cached_input": 1089792,
      "output": 11959,
      "uncached_input": 145351,
      "input_plus_output": 1247102
    },
    "monetary_cost_usd": null
  },
  "elapsed_s": 1066.9530000000086,
  "retest_batches": 0,
  "retest_operations": 0,
  "retest_replay": null,
  "english_output": true
}
```

## Infrastructure recovery

Original failed attempt is retained separately. Mode: posttests; new source batches: 0. See [recovery accounting](recovery.json).
