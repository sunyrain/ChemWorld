# Work I Experimental Semantics Qualification

Qualification: `chemworld-work-i-experiment-semantics-91f7d5d5c49b9860`  
SHA-256: `91f7d5d5c49b98606825eee05832de60057a3e09677f1839443a33f0885013b3`

## Overall qualification

| Semantic surface | Qualified result |
| --- | --- |
| Typed operations | 28/28 committed in a valid context; 28/28 invalid probes preserved physical state |
| Instruments | 5/5 matched declared cost, sample consumption, and terminal precondition |
| Resources | hard preflight limits, attempt charging, committed-only stock debits, and snapshot replay passed |
| Failures | validation, precondition/constitution rollback, and resource rejection remain distinct and replayable |

## Operation qualification table

| Operation | Module | Kind | Valid | Invalid status | Physical state kept |
| --- | --- | --- | ---: | --- | ---: |
| `add_reagent` | `reaction` | `primitive` | True | `validation_failed` | True |
| `add_solvent` | `reaction` | `primitive` | True | `validation_failed` | True |
| `add_catalyst` | `reaction` | `primitive` | True | `validation_failed` | True |
| `heat` | `reaction` | `primitive` | True | `validation_failed` | True |
| `wait` | `reaction` | `primitive` | True | `validation_failed` | True |
| `sample` | `reaction` | `primitive` | True | `validation_failed` | True |
| `quench` | `reaction` | `primitive` | True | `rolled_back` | True |
| `add_phase` | `separation` | `primitive` | True | `validation_failed` | True |
| `add_extractant` | `separation` | `primitive` | True | `validation_failed` | True |
| `mix` | `separation` | `primitive` | True | `validation_failed` | True |
| `settle` | `separation` | `primitive` | True | `validation_failed` | True |
| `separate_phase` | `separation` | `primitive` | True | `validation_failed` | True |
| `wash` | `separation` | `macro` | True | `validation_failed` | True |
| `dry` | `separation` | `macro` | True | `rolled_back` | True |
| `concentrate` | `separation` | `macro` | True | `validation_failed` | True |
| `transfer` | `separation` | `primitive` | True | `validation_failed` | True |
| `seed_crystals` | `crystallization` | `domain` | True | `validation_failed` | True |
| `cool_crystallize` | `crystallization` | `domain` | True | `validation_failed` | True |
| `filter_crystals` | `crystallization` | `domain` | True | `rolled_back` | True |
| `evaporate` | `distillation` | `domain` | True | `validation_failed` | True |
| `distill` | `distillation` | `domain` | True | `validation_failed` | True |
| `collect_fraction` | `distillation` | `domain` | True | `validation_failed` | True |
| `set_flow_rate` | `continuous_flow` | `domain` | True | `validation_failed` | True |
| `run_flow` | `continuous_flow` | `domain` | True | `validation_failed` | True |
| `set_potential` | `electrochemistry` | `domain` | True | `validation_failed` | True |
| `electrolyze` | `electrochemistry` | `domain` | True | `validation_failed` | True |
| `terminate` | `reaction` | `terminal` | True | `rolled_back` | True |
| `measure` | `observation` | `primitive` | True | `validation_failed` | True |

## Instrument qualification table

| Instrument | Cost | Latency (s) | Sample (L) | Destructive | Requires termination | Probe passed |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `hplc` | 0.080 | 600 | 0.000200 | True | False | True |
| `gc` | 0.060 | 480 | 0.000150 | True | False | True |
| `uvvis` | 0.025 | 90 | 0.000050 | True | False | True |
| `ph_meter` | 0.018 | 45 | 0.000030 | True | False | True |
| `final_assay` | 0.160 | 1200 | 0.000300 | True | True | True |

## Transaction and resource interpretation

Only `committed` applies a candidate physical transition. `validation_failed`, `rolled_back`, and `campaign_resource_rejected` retain the pre-action physical state while preserving the declared attempt or process penalty in the audit trail. The campaign ledger reserves attempts before execution, debits stocks and vessel or instrument counts only for committed outcomes, hashes every event, and round-trips exactly from its snapshot.

Instrument latency is a declared scheduling quantity, not elapsed physical process time. These are synthetic instrument and executable-world semantics; the table does not claim calibration against physical laboratory devices or real-world safety.
