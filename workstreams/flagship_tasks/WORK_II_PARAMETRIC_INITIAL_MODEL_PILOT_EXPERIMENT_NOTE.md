# Work II parametric initial-world-model pilot

Date: 2026-08-11
Status: design frozen before evaluator diagnostics or participant execution

## Question and tested units

Can one persistent WellAU `gpt-5.6-sol` medium campaign use experimental evidence to exploit or reject
an approximate but potentially wrong **process-parameter prior**, when material information is opaque
and the executable world is identical across arms?

- Task: `electrochemical-conversion`.
- Development world: `public-test`, `world_seed=0`; excluded from every formal denominator.
- Independent participant cells: `opaque`, `aligned_parametric`, `misspecified_parametric`.
- Each cell: one Codex process/session, four complete experiments, one shared within-cell campaign
  resource ledger and checkpoints before evidence and after experiments 1, 2 and 4.
- Material condition: `opaque_codes` in all three cells. The only arm difference is the agent-facing
  initial model of the potential/current operating window.

## Coverage and intervention construction

Before participant execution, an evaluator-only provider-free diagnostic executes a frozen reference
grid at electrolyte `0`, solvent `0`, reagent `0.01 mol` and duration `1800 s`:

- potential: `0.68, 0.82, 0.96, 1.10, 1.24 V`;
- current: `25, 45, 65, 85 mA`.

The aligned prior reports the best grid cell as an approximate local operating window with moderate
confidence. The misspecified prior uses the equal-format cell obtained by reflecting potential and
current indices about their grid midpoints; if that cell overlaps the aligned cell, use the farthest
non-overlapping cell under Manhattan distance. Both supplied arms use identical fields, wording,
confidence, precision and token budget and state that experimental evidence is authoritative. The
opaque arm receives no process-window claim.

The diagnostic qualifies the intervention only if all 20 recipes execute and replay exactly, the
aligned and misspecified cells are distinct, and their reference scores differ by at least `0.10`.
Failure ends this block without changing the grid or threshold.

## Measurements

- operation, experiment, checkpoint, provider, token, time, validation, recovery and resource
  denominators;
- experiment-1 and experiment-2 potential/current choices and distance to each supplied window;
- checkpoint prior reliability, held-out predictions and evidence references;
- final explicit-prediction error, executable-law error and prediction-to-law loss;
- blind recommendation versus observed incumbent, evaluated without provider calls;
- exact physical and campaign-resource replay.

## Pass and failure rules

Operational pilot pass requires all three cells to reach a retained terminal record, four complete
experiments and four valid checkpoints, one provider session per cell, exact replay, neutral public
paths/resource cards and no hidden arm or evaluator-truth leakage. Scientific outcomes are never a
pass criterion: acceptance, rejection, partial correction, no effect and harmful correction are all
retained. A persisted scientific trajectory is not replaced. Only a missing-infrastructure-only
failure before a persisted operation may use the existing single-resume rule.

## Expected outputs

- one evaluator diagnostic summary with all 20 recipes and exact denominators;
- one three-arm development config and matched initial-model payloads;
- one terminal summary and trajectory per participant cell plus a readable combined pilot summary;
- a go/no-go recommendation for the prespecified five-seed extension.
