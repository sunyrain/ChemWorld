# Work II seed-0 persistent campaign pilot result

Status: **operational pilot passed; scientific arm contrast invalidated post hoc** on 2026-08-08.
The trajectories remain valid for session/resource/replay qualification, but not for prior-effect
interpretation.

## Exact execution denominator

- 3 prior arms, 1 world seed, 3 provider sessions.
- 4 complete experiments per arm: 12/12 completed.
- 24 operations per arm: 72/72 committed, 0 invalid or resource-rejected attempts.
- 4 typed checkpoints per arm: 12/12 committed in the same session as the operations.
- 72/72 replayed steps matched exactly with zero numerical mismatch.
- Total wall time: 3,259.9 s. Total provider usage: 4,457,978 input tokens, of which
  4,004,864 were cache hits and 453,114 were uncached; output was 23,781 tokens.

## What happened

| Arm | Belief trajectory | Experiment strategy | Best score | Final score |
|---|---|---|---:|---:|
| Opaque | no explicit-prior reliability | Complete 2×2 solvent/electrolyte factorial at fixed controls | 0.3906 | 0.3314 |
| Aligned nominal | 0.70 → 0.65 → 0.55 → 0.80 | Prior-guided E1/S0, a disconfirming high-forcing probe, then return and replicate E1/S0 | 0.5725 | 0.5725 |
| Misindexed nominal | 0.50 → 0.45 → 0.40 → 0.45 | Prior-guided start, controlled contrasts, then isolate E1/S0 and test nearby E1/S1 | 0.5643 | 0.5348 |

The opaque arm spent the campaign on a clean material factorial and concluded that the material
interaction was strong. The aligned arm used the dossier to reach a useful region quickly, reduced
trust after a poor high-forcing condition, and restored trust after returning to the best recipe.
Post-run boundary audit found that the public campaign resource card still encoded `prior_arm` and
`world_seed` in its `card_id/metadata`. Consequently, the apparent belief trajectories cannot be
used to claim prior confirmation or rejection, even though the material dossier and workspace path
were separately blinded. The numerical trajectories are retained only as shakedown observations.

## Resource interpretation

Cache-hit context accounted for 85.9–91.9% of input tokens across arms. The high cumulative input
does not indicate repeated generated answers; it is mostly the same long session context being
reused across MCP tool loops. Uncached input differed across the three shakedown cells, but the
resource-card leak means those differences must not be interpreted as an arm effect.

## Boundaries and next work

This run qualifies the persistent session, operation ownership, campaign ledger, checkpoint path,
paired noise and replay. It does not qualify prior-arm blinding and does not yet test law transfer:
held-out predictions and blind recommendations were committed but not independently executed.
Before the five-seed rerun, the public resource card was made arm/seed neutral, task-specific process
time and repeat caps were added, and cell success was made fail-closed on checkpoint, session,
resource and replay integrity. The neutral-card five-seed matrix is therefore the first run eligible
for blinded prior-condition interpretation; sealed evaluator execution follows separately.
