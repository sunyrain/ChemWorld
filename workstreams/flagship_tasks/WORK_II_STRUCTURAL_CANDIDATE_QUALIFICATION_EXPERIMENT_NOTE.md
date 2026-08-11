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

## Expected outputs

1. One machine-readable five-world Q0/Q1 summary per candidate with exact denominators.
2. One Q2 matched-prior package and one 12-experiment D1 config for each passing candidate.
3. One readable comparison explaining why the candidate measures causal structure rather than
   endpoint magnitude.

