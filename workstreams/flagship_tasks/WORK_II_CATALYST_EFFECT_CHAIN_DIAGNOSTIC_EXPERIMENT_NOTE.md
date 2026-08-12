# Work II catalyst-effect chain diagnostic

Date: 2026-08-12

Status: frozen before execution

## Question and coverage

Why is the public stable-catalyst versus deactivating-catalyst effect small in reaction-safety?
The diagnostic separates catalyst functionality from catalyst-deactivation identifiability without
changing any mechanism parameter, task boundary, score, noise level, or effect gate.

The provider-free seed-0 block uses one fixed reagent/solvent/catalyst identity and stirring setting.
It covers `3 temperatures x 3 durations`. Each process context contains a no-catalyst control plus
deactivating and stable laws at `3 positive catalyst doses`, for `63` executions total:

- temperatures: `350, 410, 465 K`;
- durations: `1,800, 7,200, 14,400 s`;
- positive doses: `0.000120, 0.000315, 0.000520 mol`;
- fixed charge: `0.015 mol` reagent in `0.025 L` solvent, catalyst identity `1`, `675 rpm`.

Each execution is repeated from a fresh environment to check deterministic replay. No provider or
participant session is used. A campaign reset check separately verifies that final assay creates a
fresh physical batch rather than carrying catalyst ageing into the next experiment.

## Measurements and frozen interpretation rules

Record the charged, post-heat, post-quench and final states; `A/P/B/D/Cat_active/Cat_dead` amounts;
initial and post-heat reaction-rate vectors; exact catalyst inventory; noiseless truth metrics;
public HPLC/final-assay metrics; temperature, risk and score.

- A runtime implementation defect is reported if catalyst dose is not written exactly to
  `Cat_active`, catalyst total is not conserved, no-catalyst target rate is nonzero beyond numerical
  tolerance, stable topology does not remove only deactivation, a destructive measurement does not
  read the pre-withdrawal sample or withdraw material and its remaining initial-charge basis in the
  same proportion, or official exact replay fails.
- Catalyst functionality is supported if positive-dose target rate and target product exceed the
  no-catalyst control in the same context, with a maximum noiseless yield effect of at least `0.10`.
- Dose masking is supported only if the high-dose mean stable-minus-deactivating yield gap is at
  least `0.003` below the middle-dose mean while more than half of the catalyst remains active.
- Endpoint compression is supported only if at least two cells have an integrated target-formation
  gap exceeding the yield gap by at least `0.003`.
- Scenario calibration is flagged if catalyst functionality fails, or if the declared high-temperature
  deactivation tradeoff is not robust in at least two cells. A robust cell requires a yield decrease
  of at least `0.03` from the middle to high temperature and a deactivation-specific
  difference-in-differences of at least `0.01`.

The diagnostic classifies the existing result as experiment-design masking, task identifiability,
parameter calibration, runtime implementation, or a documented combination. It does not authorize
provider execution or retrospective changes to W2-33/W2-34.

## Outputs

One tracked machine-readable summary with all `63` executions and failures, one concise Chinese
analysis, and an updated Work II TODO entry. Raw provider payloads and raw run directories are not
created.
