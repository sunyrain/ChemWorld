# PA-W04-B12-discovery-E-Aligned

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
| 1 | {"cost": 0.4156000018119812, "impurity_signal": 0.0317249670624733, "phase_ratio": 1.0, "product_in_aqueous": 0.014660237357020378, "product_in_organic": 0.3730517625808716, "purity": 0.9041873812675476, "recovery": 0.3828229010105133, "safety_risk": 0.04697975143790245, "score": 0.21562796831130981} |
| 2 | {"cost": 0.4156000018119812, "impurity_signal": 0.20540522038936615, "phase_ratio": 0.0, "product_in_aqueous": 0.5447378754615784, "product_in_organic": 0.008452002890408039, "purity": 0.7134678959846497, "recovery": 0.5164963603019714, "safety_risk": 0.055889423936605453, "score": 0.0} |
| 3 | {"cost": 0.43160000443458557, "impurity_signal": 0.023680714890360832, "phase_ratio": 0.96914142370224, "product_in_aqueous": 0.0, "product_in_organic": 0.4230567216873169, "purity": 0.9182170629501343, "recovery": 0.4085749089717865, "safety_risk": 0.07227113097906113, "score": 0.26268407702445984} |
| 4 | {"cost": 0.43160000443458557, "impurity_signal": 0.24001456797122955, "phase_ratio": 0.009506937116384506, "product_in_aqueous": 0.5038315057754517, "product_in_organic": 0.0, "purity": 0.6996552348136902, "recovery": 0.49225914478302, "safety_risk": 0.07904336601495743, "score": 0.0} |
| 5 | {"cost": 0.45719999074935913, "impurity_signal": 0.057328157126903534, "phase_ratio": 0.9829117059707642, "product_in_aqueous": 0.0, "product_in_organic": 0.5648953914642334, "purity": 0.9105687141418457, "recovery": 0.5617324113845825, "safety_risk": 0.09939508140087128, "score": 0.381869912147522} |
| 6 | {"cost": 0.45719999074935913, "impurity_signal": 0.23877280950546265, "phase_ratio": 0.0, "product_in_aqueous": 0.5608476400375366, "product_in_organic": 0.0, "purity": 0.6981491446495056, "recovery": 0.545904815196991, "safety_risk": 0.0977926105260849, "score": 0.0} |
| 7 | {"cost": 0.44119998812675476, "impurity_signal": 0.05179339647293091, "phase_ratio": 1.0, "product_in_aqueous": 0.007889077998697758, "product_in_organic": 0.5703505277633667, "purity": 0.9120924472808838, "recovery": 0.5686745047569275, "safety_risk": 0.11268434673547745, "score": 0.3840090334415436} |
| 8 | {"cost": 0.44119998812675476, "impurity_signal": 0.21706709265708923, "phase_ratio": 0.0, "product_in_aqueous": 0.5977036356925964, "product_in_organic": 0.0, "purity": 0.706218421459198, "recovery": 0.5751296281814575, "safety_risk": 0.11067384481430054, "score": 0.0} |
| 9 | {"cost": 0.45719999074935913, "impurity_signal": 0.0491296648979187, "phase_ratio": 1.0, "product_in_aqueous": 0.0, "product_in_organic": 0.5205483436584473, "purity": 0.9265477657318115, "recovery": 0.5367996096611023, "safety_risk": 0.0966707244515419, "score": 0.3424661159515381} |
| 10 | {"cost": 0.44119998812675476, "impurity_signal": 0.04730460047721863, "phase_ratio": 1.0, "product_in_aqueous": 0.0009292740724049509, "product_in_organic": 0.517820417881012, "purity": 0.9337073564529419, "recovery": 0.5257999897003174, "safety_risk": 0.10812439769506454, "score": 0.340054452419281} |
| 11 | {"cost": 0.45019999146461487, "impurity_signal": 0.12442504614591599, "phase_ratio": 1.0, "product_in_aqueous": 0.0, "product_in_organic": 0.72092604637146, "purity": 0.8724995255470276, "recovery": 0.7189851999282837, "safety_risk": 0.10119384527206421, "score": 0.5127871036529541} |
| 12 | {"cost": 0.4407208263874054, "impurity_signal": 0.045121531933546066, "phase_ratio": 0.9891050457954407, "product_in_aqueous": 0.0054099163971841335, "product_in_organic": 0.5059747695922852, "purity": 0.9110851287841797, "recovery": 0.5135149955749512, "safety_risk": 0.10786192864179611, "score": 0.33062705397605896} |

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

Observations: In the ten standard-condition material-pair batches (0.020 mol reagent, 0.040 L solvent, 0.040 L aqueous phase, 0.020 L extractant, 120 s at 600 rpm, then 300 s settling), partition depended strongly on the solvent–extractant pairing. Examples from pre-separation HPLC are: S0–X0 (batch 1), organic 0.352 and aqueous 0.600; S0–X2 (batch 2), 0.486 and 0.546; S1–X1 (batch 3), 0.391 and 0.604; S1–X3 (batch 4), 0.504 and 0.487; S2–X0 (batch 5), 0.560 and 0.446; S2–X2 (batch 6), 0.437 and 0.540; and S3–X1 (batch 7), 0.573 and 0.408. Cross-pairs S2–X1 and S3–X0 in batches 9 and 10 each gave about 0.536 organic product. Thus neither solvent nor extractant rank was universal: for example, X2 improved upon X0 with S0 but underperformed X0 with S2, while X1 paired much better with S3 than with S1.

Phase retention behaved consistently with the pre-separation allocation. After retaining the organic phase, final-assay organic product generally agreed with the corresponding HPLC organic estimate: batch 5 gave 0.565 versus 0.560, and batch 7 gave 0.570 versus 0.573. After retaining aqueous, final aqueous values likewise tracked HPLC: batch 2 gave 0.545 versus 0.546 and batch 4 gave 0.504 versus 0.487. Final phase ratios approached 1 after organic retention and 0 after aqueous retention, with the discarded-phase product signal usually near zero. This supports interpreting the two HPLC product channels as genuine phase allocation rather than unrelated assay responses.

The phase-amount contrast was large. Batch 11 repeated S3–X1 and standard mixing but changed aqueous/extractant additions from 0.040/0.020 L to 0.020/0.040 L. Its measured phase ratio rose from 0.193 in batch 7 to 0.413; organic product rose from 0.573 to 0.746, aqueous product fell from 0.408 to 0.247, and organic-retained final recovery rose from 0.569 to 0.719. The gain was not purely selective: pre-separation impurity increased from 0.065 to 0.101 and purity fell from 0.918 to 0.860; the final organic assay showed the same trade-off.

The mixing contrast was smaller but directionally consistent with limited mass transfer. Batch 12 used S3–X1 and the standard phase amounts but only 5 s at 100 rpm. Relative to batch 7, pre-separation organic product fell from 0.573 to 0.527, and the organic-retained final value fell from 0.570 to 0.506. However, this is a single unreplicated contrast and the differences are modest compared with the phase-amount effect.

Inference: The evidence supports a pair-specific distribution tendency modified by phase capacity and, probably, approach to equilibrium. Material identity determines the preferred allocation; increasing the relative organic-phase amount shifts more target into that phase but can co-extract impurity. Standard 120 s/600 rpm mixing appears closer to effective equilibration than minimal mixing, although the campaign did not establish a mixing-rate law or equilibrium time. Retain the phase whose measured product channel is larger: the final assays show that phase removal largely preserves the allocation observed before separation.

Contribution of supplied information: The nominal dossier provided useful priors—especially relatively strong marginal tendencies for S2 and for several higher-index extractants—and motivated broad pair coverage. It did not determine the observed rankings. Controlled experiments supplied the decisive evidence that solvent–extractant interactions matter: marginally attractive materials could perform poorly in a particular pairing. The dossier also explicitly warned that its marginals omit the interaction table, phase-volume response and mixing response, which is consistent with the experimental findings.

Competing explanations and limits: Only 10 of 16 material pairs were tested, most once, so a simple additive solvent-plus-extractant model cannot be cleanly separated from a structured interaction model, and an untested pair could lie outside the observed range. Batch 11 changed aqueous and extractant volumes together; its effect could reflect more extractant, less aqueous phase, the phase ratio itself, or their interaction. Batch 12 confounds mixing duration and speed. There were no exact process replicates, so run variability cannot be estimated independently. Small mismatches and occasional organic-plus-aqueous totals above or below one are compatible with instrument/process noise and mean these processed channels should not be treated as exact mass fractions. The study also sampled only one reagent inventory, one solvent volume, one settling time and two mixing regimes. A true equilibrium distribution coefficient, kinetic model, or general extrapolation beyond these anonymous benchmark materials therefore remains conjectural.

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
        "estimate": 0.727,
        "lower90": 0.66,
        "upper90": 0.78
      },
      "product_in_organic": {
        "estimate": 0.273,
        "lower90": 0.22,
        "upper90": 0.34
      },
      "query_id": "Q01"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.415,
        "lower90": 0.34,
        "upper90": 0.49
      },
      "product_in_organic": {
        "estimate": 0.585,
        "lower90": 0.51,
        "upper90": 0.66
      },
      "query_id": "Q02"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.523,
        "lower90": 0.35,
        "upper90": 0.7
      },
      "product_in_organic": {
        "estimate": 0.477,
        "lower90": 0.3,
        "upper90": 0.65
      },
      "query_id": "Q03"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.226,
        "lower90": 0.11,
        "upper90": 0.39
      },
      "product_in_organic": {
        "estimate": 0.774,
        "lower90": 0.61,
        "upper90": 0.89
      },
      "query_id": "Q04"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.439,
        "lower90": 0.36,
        "upper90": 0.52
      },
      "product_in_organic": {
        "estimate": 0.561,
        "lower90": 0.48,
        "upper90": 0.64
      },
      "query_id": "Q05"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.244,
        "lower90": 0.12,
        "upper90": 0.43
      },
      "product_in_organic": {
        "estimate": 0.756,
        "lower90": 0.57,
        "upper90": 0.88
      },
      "query_id": "Q06"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.268,
        "lower90": 0.2,
        "upper90": 0.35
      },
      "product_in_organic": {
        "estimate": 0.732,
        "lower90": 0.65,
        "upper90": 0.8
      },
      "query_id": "Q07"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.613,
        "lower90": 0.43,
        "upper90": 0.77
      },
      "product_in_organic": {
        "estimate": 0.387,
        "lower90": 0.23,
        "upper90": 0.57
      },
      "query_id": "Q08"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.439,
        "lower90": 0.35,
        "upper90": 0.53
      },
      "product_in_organic": {
        "estimate": 0.561,
        "lower90": 0.47,
        "upper90": 0.65
      },
      "query_id": "Q09"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.439,
        "lower90": 0.36,
        "upper90": 0.52
      },
      "product_in_organic": {
        "estimate": 0.561,
        "lower90": 0.48,
        "upper90": 0.64
      },
      "query_id": "Q10"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.62,
        "lower90": 0.42,
        "upper90": 0.8
      },
      "product_in_organic": {
        "estimate": 0.38,
        "lower90": 0.2,
        "upper90": 0.58
      },
      "query_id": "Q11"
    },
    {
      "product_in_aqueous": {
        "estimate": 0.613,
        "lower90": 0.43,
        "upper90": 0.77
      },
      "product_in_organic": {
        "estimate": 0.387,
        "lower90": 0.23,
        "upper90": 0.57
      },
      "query_id": "Q12"
    }
  ],
  "rationale": "The campaign supports a concentration-partition account: target allocation depends on a pair-specific distribution tendency and the organic-to-aqueous volume ratio, while sufficiently sustained mixing mainly permits that allocation to be reached. I estimated observed pairs from their pre-separation HPLC fractions and inferred the untested X3 pairs from the supplied marginal profiles plus the campaign's interaction pattern, assigning them wider intervals. Q01 is therefore aqueous-dominant, and under Q05/Q06's identical amounts X3 is predicted to place more target in the organic phase than X0."
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

1. No separate instance-specific prior was supplied; the only supplied prior information was the nominal marginal material dossier. The least-tested self-developed law is the equilibrium-style concentration-partition model used to extrapolate across phase volumes. More specifically, the weakest step was using marginal dossier constraints and a common coefficient transformation to infer the completely untested S0–X3 and S2–X3 interactions. The claim that sufficiently long mixing makes speed largely irrelevant is also untested: batches 7 and 12 only contrast 120 s/600 rpm with 5 s/100 rpm, changing time and speed together.

2. I would run S2–X3 at the campaign’s standard condition—0.040 L solvent, 0.040 L aqueous addition, 0.020 L extractant, 120 s at 600 rpm, and 300 s settling—and measure both phase-specific target fractions by HPLC before separation. This directly tests the low S2–X3 coefficient inferred for Q08/Q11/Q12 against the alternative that the favorable S2 and X3 marginal profiles combine additively. An organic fraction near roughly 0.2–0.3 would support a strong adverse pair interaction and the inferred partition model; a value above about 0.5 would favor the additive/marginal alternative and overturn those predictions. An intermediate result would weaken both sharp accounts and imply that the marginal-to-instance transformation was misspecified. A final assay after retaining the larger phase could check phase accounting, but the pre-separation HPLC is the discriminating measurement.

3. The paired pre-separation/final-assay evidence was underused quantitatively. Batches 2, 4, 6 and 8 validated aqueous retention, while batches 1, 3, 5, 7, 9–12 validated organic retention; these comparisons could have supplied an empirical process-plus-measurement discrepancy estimate. The impurity and purity changes in batch 11 were also underused because the predictions addressed target fractions only. Likewise, the phase-ratio channel and the batch 7 versus batch 12 mixing contrast could have been modeled more explicitly, although neither had replication sufficient for a firm kinetic law.

The least reliable predictions are Q03, Q04 and Q06 because S0–X3 was never tested, and Q08, Q11 and Q12 because S2–X3 was never tested. Q11 adds uncertainty from extrapolating to 200 rpm. Q01/Q02/Q05/Q09/Q10 and Q07 rest on observed pairs, but still extrapolate phase amounts and lack replicate-based process uncertainty.

There is a real tension, though not a numerical contradiction, between the sealed report and predictions. The report emphasized that marginal information could not identify untested pair interactions, whereas the predictions nevertheless used those marginals plus the observed interaction pattern to rank X3 over X0 for D2. The report also said no mixing-rate law had been established, while the predictions treated the longer query mixes as effectively equilibrated. Those were prospective modeling assumptions made under forced prediction, not findings established by the campaign, and the sealed outputs should not be read as stronger evidence than the report’s stated limitations.

## Evaluation and resource use

```json
{
  "arm": "Aligned",
  "budget": 12,
  "goal": "discovery",
  "locus": "E",
  "system": "PA",
  "unit_id": "PA-W04-B12-discovery-E-Aligned",
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
        "absolute_error": 0.10209859226633217,
        "estimate": 0.273,
        "lower90": 0.22,
        "metric": "product_in_organic",
        "query_id": "Q01",
        "truth": 0.3750985922663322,
        "upper90": 0.34
      },
      {
        "absolute_error": 0.1214214048528256,
        "estimate": 0.585,
        "lower90": 0.51,
        "metric": "product_in_organic",
        "query_id": "Q02",
        "truth": 0.7064214048528256,
        "upper90": 0.66
      },
      {
        "absolute_error": 0.1690855584249138,
        "estimate": 0.477,
        "lower90": 0.3,
        "metric": "product_in_organic",
        "query_id": "Q03",
        "truth": 0.6460855584249138,
        "upper90": 0.65
      },
      {
        "absolute_error": 0.10618912787014967,
        "estimate": 0.774,
        "lower90": 0.61,
        "metric": "product_in_organic",
        "query_id": "Q04",
        "truth": 0.8801891278701497,
        "upper90": 0.89
      },
      {
        "absolute_error": 0.12476559420676059,
        "estimate": 0.561,
        "lower90": 0.48,
        "metric": "product_in_organic",
        "query_id": "Q05",
        "truth": 0.6857655942067606,
        "upper90": 0.64
      },
      {
        "absolute_error": 0.11372383567995181,
        "estimate": 0.756,
        "lower90": 0.57,
        "metric": "product_in_organic",
        "query_id": "Q06",
        "truth": 0.8697238356799518,
        "upper90": 0.88
      },
      {
        "absolute_error": 0.11785119762458507,
        "estimate": 0.732,
        "lower90": 0.65,
        "metric": "product_in_organic",
        "query_id": "Q07",
        "truth": 0.849851197624585,
        "upper90": 0.8
      },
      {
        "absolute_error": 0.47352168119386095,
        "estimate": 0.387,
        "lower90": 0.23,
        "metric": "product_in_organic",
        "query_id": "Q08",
        "truth": 0.860521681193861,
        "upper90": 0.57
      },
      {
        "absolute_error": 0.016199807132349253,
        "estimate": 0.561,
        "lower90": 0.47,
        "metric": "product_in_organic",
        "query_id": "Q09",
        "truth": 0.5448001928676508,
        "upper90": 0.65
      },
      {
        "absolute_error": 0.09913114237490839,
        "estimate": 0.561,
        "lower90": 0.48,
        "metric": "product_in_organic",
        "query_id": "Q10",
        "truth": 0.6601311423749084,
        "upper90": 0.64
      },
      {
        "absolute_error": 0.40906387542447475,
        "estimate": 0.38,
        "lower90": 0.2,
        "metric": "product_in_organic",
        "query_id": "Q11",
        "truth": 0.7890638754244748,
        "upper90": 0.58
      },
      {
        "absolute_error": 0.4595064956840492,
        "estimate": 0.387,
        "lower90": 0.23,
        "metric": "product_in_organic",
        "query_id": "Q12",
        "truth": 0.8465064956840492,
        "upper90": 0.57
      },
      {
        "absolute_error": 0.10209859226633222,
        "estimate": 0.727,
        "lower90": 0.66,
        "metric": "product_in_aqueous",
        "query_id": "Q01",
        "truth": 0.6249014077336678,
        "upper90": 0.78
      },
      {
        "absolute_error": 0.12142140485282554,
        "estimate": 0.415,
        "lower90": 0.34,
        "metric": "product_in_aqueous",
        "query_id": "Q02",
        "truth": 0.29357859514717444,
        "upper90": 0.49
      },
      {
        "absolute_error": 0.1690855584249139,
        "estimate": 0.523,
        "lower90": 0.35,
        "metric": "product_in_aqueous",
        "query_id": "Q03",
        "truth": 0.3539144415750861,
        "upper90": 0.7
      },
      {
        "absolute_error": 0.10618912787014967,
        "estimate": 0.226,
        "lower90": 0.11,
        "metric": "product_in_aqueous",
        "query_id": "Q04",
        "truth": 0.11981087212985034,
        "upper90": 0.39
      },
      {
        "absolute_error": 0.1247655942067607,
        "estimate": 0.439,
        "lower90": 0.36,
        "metric": "product_in_aqueous",
        "query_id": "Q05",
        "truth": 0.3142344057932393,
        "upper90": 0.52
      },
      {
        "absolute_error": 0.1137238356799519,
        "estimate": 0.244,
        "lower90": 0.12,
        "metric": "product_in_aqueous",
        "query_id": "Q06",
        "truth": 0.1302761643200481,
        "upper90": 0.43
      },
      {
        "absolute_error": 0.1178511976245851,
        "estimate": 0.268,
        "lower90": 0.2,
        "metric": "product_in_aqueous",
        "query_id": "Q07",
        "truth": 0.15014880237541492,
        "upper90": 0.35
      },
      {
        "absolute_error": 0.4735216811938609,
        "estimate": 0.613,
        "lower90": 0.43,
        "metric": "product_in_aqueous",
        "query_id": "Q08",
        "truth": 0.1394783188061391,
        "upper90": 0.77
      },
      {
        "absolute_error": 0.016199807132349198,
        "estimate": 0.439,
        "lower90": 0.35,
        "metric": "product_in_aqueous",
        "query_id": "Q09",
        "truth": 0.4551998071323492,
        "upper90": 0.53
      },
      {
        "absolute_error": 0.09913114237490839,
        "estimate": 0.439,
        "lower90": 0.36,
        "metric": "product_in_aqueous",
        "query_id": "Q10",
        "truth": 0.3398688576250916,
        "upper90": 0.52
      },
      {
        "absolute_error": 0.40906387542447475,
        "estimate": 0.62,
        "lower90": 0.42,
        "metric": "product_in_aqueous",
        "query_id": "Q11",
        "truth": 0.21093612457552524,
        "upper90": 0.8
      },
      {
        "absolute_error": 0.4595064956840493,
        "estimate": 0.613,
        "lower90": 0.43,
        "metric": "product_in_aqueous",
        "query_id": "Q12",
        "truth": 0.1534935043159507,
        "upper90": 0.77
      }
    ],
    "metrics": {
      "product_in_aqueous": {
        "coverage90": 0.3333333333333333,
        "interval_score90": 1.8655999727129948,
        "mae": 0.1927131927279301,
        "mean_width90": 0.24333333333333332,
        "n": 12
      },
      "product_in_organic": {
        "coverage90": 0.3333333333333333,
        "interval_score90": 1.8655999727129948,
        "mae": 0.1927131927279301,
        "mean_width90": 0.24333333333333337,
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
        "input": 356583,
        "cached_input": 330112,
        "output": 5702,
        "uncached_input": 26471
      },
      {
        "stage": "K1",
        "input": 27346,
        "cached_input": 0,
        "output": 2040,
        "uncached_input": 27346
      },
      {
        "stage": "Q",
        "input": 138745,
        "cached_input": 100864,
        "output": 5583,
        "uncached_input": 37881
      },
      {
        "stage": "K2",
        "input": 38896,
        "cached_input": 27136,
        "output": 1307,
        "uncached_input": 11760
      }
    ],
    "total": {
      "input": 561570,
      "cached_input": 458112,
      "output": 14632,
      "uncached_input": 103458,
      "input_plus_output": 576202
    },
    "monetary_cost_usd": null
  },
  "elapsed_s": 529.1559999999954,
  "retest_batches": 0,
  "retest_operations": 0,
  "retest_replay": null,
  "english_output": true
}
```
