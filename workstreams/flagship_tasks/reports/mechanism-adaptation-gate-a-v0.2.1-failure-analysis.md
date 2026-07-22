# Gate A v0.2.1 failure analysis and v0.2.2 resolution

## Executive decision

The v0.2.1 result is retained as a failed **post-change-only evaluator diagnostic**. It
does not establish that the reaction-to-crystallization environment is unidentifiable
within the protocol budget, because that evaluator omitted the frozen pre-change
history and did not coherently pair nuisance realizations across candidates and
actions. It must not be interpreted as an Agent failure.

Gate A v0.2.2 corrects those evaluator defects without changing the frozen accuracy
thresholds. It passes, but the reaction material-law family clears its per-family
Wilson threshold by a narrow margin and therefore remains the principal robustness
target.

## What failed in v0.2.1

At four post-change experiments, the active oracle achieved 0.8952 top-1 accuracy
(188/210; 95% Wilson interval 0.8465--0.9298). The overall lower bound exceeded the
0.80 threshold, but three reaction-to-crystallization families failed the required
0.70 per-family recall lower bound:

| Task-qualified family | Correct | Recall | 95% Wilson lower bound | Gate result |
| --- | ---: | ---: | ---: | --- |
| reaction material-law counterfactual | 24/30 | 0.8000 | 0.6269 | fail |
| reaction no-change | 20/30 | 0.6667 | 0.4878 | fail |
| reaction rate-law family | 24/30 | 0.8000 | 0.6269 | fail |
| reaction topology family | 30/30 | 1.0000 | 0.8865 | pass |
| all three electrochemical families | 30/30 each | 1.0000 | 0.8865 | pass |

The dominant confusion was relational: reaction no-change was predicted as a
material-law change in 9/30 cases; reaction material-law change was predicted as
no-change in 5/30 cases; and reaction rate-law change was predicted as no-change in
6/30 cases. The mean maximum posterior was about 0.99 despite these errors, so the
failure was not merely low confidence from too few trials.

## Root causes

1. **The evaluator discarded pre-change memory.** The protocol includes two
   pre-change experiments, but v0.2.1 classified only observations from a newly
   instantiated post-change world. A material-label permutation and no-change are
   fundamentally relational hypotheses; they should be compared against the same
   world's baseline response.
2. **Nuisance integration was marginal rather than joint.** Candidate/action
   predictives were fitted from independently drawn world seeds. Multiple actions
   from one held-out world were then multiplied as conditionally independent
   likelihoods. The report field `nuisance_integration.performed=true` therefore
   overstated what the implementation actually guaranteed.
3. **Candidate twins did not share held-out worlds.** Candidate families used
   candidate-index-shifted seed ranges. This estimated population classification,
   not changed-versus-no-change behavior in paired copies of the same hidden world.
4. **World and observation randomness were coupled.** The environment exposed one
   seed for both hidden-world generation and observation noise. A strict no-change
   reset needs unchanged hidden laws with a separately reproducible measurement-noise
   stream.
5. **The diagonal Gaussian approximation was overconfident.** It ignored important
   cross-action and shared-world dependence. This remains a calibration limitation
   even after the relational evidence path is repaired.

## v0.2.2 correction

The corrected certificate:

- retains the same hidden-world seed across pre-change and post-change phases;
- reuses each held-out world seed across all candidate twins;
- separates observation-noise seeds between phases;
- replays the same two public complete recipes before and after reset;
- encodes only agent-derivable post-minus-pre public observation/reward contrasts;
- selects the two-recipe batch using prior expected information from disjoint fitting
  seeds, before any held-out outcomes are generated; and
- preserves the frozen overall 0.80 and per-family 0.70 Wilson lower-bound thresholds.

The active oracle reaches 206/210 = 0.9810 top-1 accuracy (95% Wilson interval
0.9521--0.9926). Six task-qualified families are 30/30. Reaction material-law
counterfactual is 26/30 = 0.8667 with lower bound 0.7032, so all formal Gate A rules
pass at two matched post-change experiments. The fixed two-recipe decoder reaches
207/210 = 0.9857 and also passes.

## Interpretation boundary

Gate A now establishes that the selected environment mechanisms are identifiable to
this evaluator-side diagnosis system under the matched two-experiment protocol. It
does **not** show that DeepSeek or any other evaluated Agent detects the change,
identifies the family, uses feedback well, recovers performance, or manages the
experiment lifecycle. Those are Gates B--E. Gate 0 integrity evidence also remains a
precondition for formal Agent claims.

The minimum passing margin is only 0.0032 in Wilson-lower-bound units for the reaction
material-law family. A separately versioned robustness replication and posterior
calibration audit should therefore accompany, but not retroactively redefine, the
v0.2.2 certificate.
