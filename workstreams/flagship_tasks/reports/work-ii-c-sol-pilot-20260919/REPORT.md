# Crystallization C-E pilot

Development pilot; GPT-5.6 Sol / medium. One world, three prior arms, no outcome-based retries.
Twelve paired prediction slots use nine unique recipes. Shared controls are dependent comparisons, not additional independent scientific samples.

Preparation batches: 19/19; status: completed; passed: True. Complete chains: 3/3; source batches: 36/36; posttests: 9/9.

Original complete chains: 2/3; additional retest attempts: 1. Original failures remain in the machine summary; repaired results never replace raw records.

| Arm | Status | Batches | Posttests | Recovery | Purity | Fines | Quality passes | Recovery target met |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| [Opaque](Opaque.md) | completed | 12/12 | 3/3 | 0.0 | 1.0 | 0.0 | True | False |
| [Aligned](Aligned.md) | completed | 12/12 | 3/3 | 0.3804089046365751 | 0.9875999612238897 | 0.42164028977292567 | True | True |
| [MisIndexed](MisIndexed.md) | completed | 12/12 | 3/3 | 0.0 | 1.0 | 0.0 | True | False |

## Preparation

```json
{
  "checks": {
    "anonymous_instruments": true,
    "opaque_has_no_dossier": true,
    "quality_witness": true,
    "same_observations": true,
    "same_physics": true,
    "solvent_swap_only": true
  },
  "failure": null,
  "operations": 328
}
```

All reference and source exact replays and recommendation retests are accounted separately in summary.json. A completed chain is execution completion, not scientific success.
