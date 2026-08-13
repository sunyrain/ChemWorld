# Work II A-P terminal D1 platform requalification

Status: frozen development requalification; provider order is DeepSeek then WellAU.

## Question and coverage

After correcting the provider failure taxonomy, pre-operation retry ownership and Windows atomic-write
handling, can the unchanged A-P terminal D1 design complete without conflating platform failures with
agent behavior? The block contains four fresh task-provider runs in this fixed order:

1. DeepSeek reaction-safety, then DeepSeek electrochemical;
2. WellAU reaction-safety, then WellAU electrochemical.

Every run starts at its first cell in a new output root. Each task-provider run contains world seed 2,
the frozen opaque/aligned/misindexed triplet, ten complete experiments per arm and belief checkpoints
at `0/2/4/7/10`. The full denominator is 12 initial provider sessions and 120 complete experiments.
Historical development outputs, including unfavorable and infrastructure-failed cells, remain retained
and are not resumed, overwritten or promoted into this denominator.

## Measurements and fixed rules

- Preserve operation trajectories, provider receipts, token usage, resource ledgers, belief snapshots,
  final recommendations, exact replay and every terminal failure.
- A scientific or agent-invalid failure is terminal and is never retried. One replacement process is
  allowed only for a typed infrastructure failure before any operation, provider usage, belief snapshot
  or recommendation exists; the failed attempt and its bound evidence remain append-only.
- The matrix stops only under the existing systemic pre-operation rule. No threshold, arm, world,
  checkpoint, experiment count or qualification rule changes after launch.
- Provider-specific resource envelopes are frozen prospectively for this fresh block from retained
  utilization diagnostics, not from scientific effect direction: DeepSeek uses 36,000,000 input,
  600,000 uncached-input and 160,000 output tokens per session; WellAU uses 1,800,000 input, 240,000
  uncached-input and 20,000 output tokens. Both use a 7,200-second wall-time limit. Unlimited spend
  authorization does not relax these resource or two-attempt limits.
- The original outcome-blind user authorization remains the scientific authorization. Its config/output
  binding is updated after historical development outcomes only for these platform corrections,
  provider-specific resource envelopes and fresh output roots; the scientific design is unchanged.

## Pass, failure and expected outputs

Platform requalification passes when all 12 cells reach a retained terminal state, all lifecycle and
evidence-integrity checks rebuild, and no unclassified platform event remains. Per-cell scientific
qualification is reported independently and may pass, fail or right-censor; no favorable scientific
conclusion is required for platform completion. Expected outputs are four machine-readable reports
with exact denominators and failures, plus one cross-provider development summary. This block remains
development evidence and does not authorize formal/R5 or C2 admission.
