# Work II structural/mechanistic candidate qualification — experiment note

状态：**provider-free design freeze；尚未产生新结果**  
适用阶段：W2-28；任何 candidate 必须先通过 Q0–Q2，才可生成 12-experiment participant config。

## Question

Can two task families expose a falsifiable difference between alternative causal structures, rather
than merely a difference in endpoint magnitude or in a fitted numerical optimum? The screen asks
whether a participant could, in principle, distinguish the supplied aligned and misspecified
mechanistic models using only public interventions and observations.

The two frozen candidates are:

1. **Electrochemical transport limitation:** a transport-limited current branch with diminishing
   high-current benefit versus a kinetic-only monotonic-current model.
2. **Crystallization nucleation/growth structure:** seed-mediated growth and suppression of fines
   versus a primary-nucleation-dominated model in which seed mass has negligible causal effect.

These candidates replace the rejected “which whole module dominates the endpoint score?” screens.
The earlier distillation, crystallization-module-dominance and partition-module-dominance results
remain immutable rejected development evidence.

## Tested units and coverage

- Two tasks × five development world seeds (`0–4`), evaluated separately in every world.
- Electrochemical Q1 uses a fixed 3 × 3 controlled-potential/current grid at one frozen material
  and duration context.
- Crystallization Q1 uses a fixed 3 × 3 seed-mass/cooling-severity grid after one frozen reaction
  precursor stage.
- Every grid point is one provider-free complete experiment with exact replay. A separately keyed
  noisy validation set contains three candidate groups × three replicates per world.
- Q2 constructs one opaque, aligned and misspecified initial-model package only after all five
  worlds pass Q0 and Q1. Participant/provider execution is forbidden in this note.

## Measurements

- Electrochemical: selective-product yield, Faradaic efficiency, transport efficiency, ohmic
  efficiency, energy efficiency, safety risk, current slope and high-current curvature.
- Crystallization: crystal yield, size, CSD quality, fines fraction and the seed × cooling
  interaction.
- Both: completed/physical/platform failures, exact replay, observation noise, effect sizes,
  counterfactual disagreement, matched baseline error, blind identifiability and prior word/schema
  matching.

## Pass/failure rules

For each candidate and every world:

- all registered outcomes are classified as completed or physical failure, with zero platform or
  unclassified failures; all noisy validations exact-replay;
- both registered intervention axes produce an observable effect of at least
  `max(0.03, 6 sigma_observed)` on a candidate-owned metric;
- the topology-specific signature is at least `max(0.03, 6 sigma_observed)`: high-current
  saturation/efficiency loss for electrochemistry, and a seed × cooling interaction or seed-driven
  fines/CSD contrast for crystallization;
- the aligned and misspecified models have matched baseline error and confidence, disagree on at
  least 40% of registered held-out query-metric pairs, and each has at least one public
  counterexample region;
- all five worlds pass separately. Means cannot hide a failed world.

A scientific rejection is retained and does not authorize threshold, task, seed or query changes.
A platform defect restarts the complete affected candidate from world 0 with the same frozen
design. Passing Q0–Q2 authorizes only a 12-experiment D1 configuration; it does not support a
participant capability claim.

### Frozen executable design

- Electrochemical fixed context: electrolyte profile `0`, solvent `0`, reagent `0.012 mol`, probe
  potential `0.80 V`, probe current `90 mA`, probe duration `300 s`, controlled duration `1800 s`.
  The registered grid is controlled potential `{0.75, 1.05, 1.35} V` × controlled current
  `{15, 91, 190} mA`.
- Crystallization fixed precursor context: catalyst `0`, solvent `0`, reagent `0.015 mol`, reaction
  temperature `398.15 K`, reaction duration `7200 s`, stirring `675 rpm`, catalyst amount
  `0.000315 mol`, crystallization duration `7200 s`. The registered grid is seed mass
  `{0.001, 0.008, 0.015} g` × crystallization temperature `{310, 290, 270} K`; lower temperature is
  the more severe cooling intervention.
- For both candidates the separately keyed noisy validation groups are grid coordinates
  `(low, low)`, `(middle, middle)` and `(high, high)`, with three replicates per group. Validation
  noise is estimated within group and never by mixing different interventions.
- The electrochemical axis effects are evaluated on selective-product yield and transport/Faradaic
  efficiency. Its topology signature is the largest registered high-current transport/Faradaic
  efficiency loss or diminishing high-current yield gain. The crystallization axis effects are
  evaluated on crystal yield, CSD quality and fines fraction. Its topology signature is the largest
  registered seed × cooling interaction or seed-driven CSD/fines contrast.
- `physical_failure` is an outcome class, not a platform attribution. In this provider-free block it
  is `protocol_owned_physical_boundary`; in a later participant campaign the same schema-valid
  boundary event is `participant_induced_physical_boundary`. Only compiler/payload, observation,
  ledger, replay or execution-contract defects are `platform_failure`.

## Expected outputs

1. One machine-readable five-world Q0/Q1 summary per candidate with exact denominators.
2. One Q2 matched-prior package and one 12-experiment D1 config for each passing candidate.
3. One readable comparison explaining why the candidate measures causal structure rather than
   endpoint magnitude.
