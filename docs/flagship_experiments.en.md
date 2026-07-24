# Flagship Experiments: Design, Evidence, and Freeze Status

> **A flagship experiment is not merely a runnable environment. It is a confirmatory evaluation with explicit controls, blinding, statistical units, and failure boundaries.**

## Two meanings of “flagship”

The homepage presents four research showcase worlds: partition discovery, reaction-to-crystallization,
reaction-to-distillation, and flow-reaction optimization. They illustrate the range of experimental reasoning.

The current mechanism-adaptation protocol has two formal flagship execution tasks:

| Formal task | Hidden changes | Diagnostic observations |
| --- | --- | --- |
| Reaction to Crystallization | reaction rate law, network topology, catalyst mapping | HPLC, final assay, and task score |
| Electrochemical Conversion | constitutive law, solvent mapping, electrolyte mapping | UV-Vis, final assay, and task score |

A homepage showcase therefore does not imply confirmatory online-change evidence. Conversely, electrochemistry is a
formal mechanism-adaptation task even though it is not one of the four homepage showcase cards.

## Current freeze state

| Layer | Question | Status |
| --- | --- | --- |
| Flagship semantics audit | Are controls, denominators, blinding, cohorts, and thresholds coherent? | RC23, 18/18 passed |
| A1 physical validity | Is each hidden intervention real, single-axis, and observable? | RC23, 81/81 checks passed |
| A2 controlled identifiability | Are candidate mechanisms separable under sufficient experiments? | fresh cohort pending |
| A3 online change identification | Can a policy acquire a reference, detect change, and attribute its family? | fresh cohort pending |
| Gates B–E | Detection, feedback causality, recovery, and autonomy | formal results pending |

`publication_ready=false`. Design validity cannot substitute for A2/A3 or establish that a complete Agent passes.

## Calibrated online semantics

The frozen truth support is `never, 6, 8, 10` with horizon 18. `τ=6` means that experiments 1–6 use the old world and
experiment 7 is the first experiment eligible to use the changed world. `never` is a first-class truth state; an
evaluator-only pseudo-checkpoint may be used for matching, but the hidden law remains unchanged.

The policy sees only the total horizon and that the world may remain stable or change at an unspecified time. It never
receives the minimum stable prefix, change-time support, certificate state, pseudo-checkpoint, or post-change checkpoint.

## A reference is more than an action checklist

The reference certificate requires both:

1. universal structural coverage of every declared diagnostic relation; and
2. predictive adequacy of the fit-only old-world model on held-out pre-change public observations, including a frozen
   standardized-error threshold and reference-age limit.

The requirement is universal across candidate change families and cannot be selected after observing the true family.

## Conditional and end-to-end reporting

For reference sufficiency `R`, correct change decision `D`, and correct family attribution `A`, the protocol reports
`P(R)`, `P(D|R)`, `P(A|D,R)`, and `P(R∧D∧A)`. Reference-acquisition failures are excluded only from the conditional
attribution denominator and remain failures in the end-to-end score.

The A3 thresholds for reference acquisition, detection recall, no-change false-positive rate, AUROC, Brier score,
conditional attribution, and joint success are frozen before execution. Development, A2, A3, and private confirmation
use four disjoint seed namespaces.

Reference acquisition is evaluated once per independent task/world-seed cluster with a Wilson interval. Detection,
AUROC, conditional attribution, and joint success use cluster bootstrap intervals, because candidate truth arms sharing
one stable-prefix world are paired observations rather than independent trials.

## Audit of the remaining flagship components

The unified audit also verifies:

- Gate 0 integrity and leakage controls;
- Gate B matched changed/no-change detection;
- Gate C identical-prefix local feedback tests and paired full campaigns;
- Gate D open-loop world effect, frozen no-update, adaptive, and oracle comparisons; and
- Gate E separate autonomous and assisted scientific scores.

No Gate C–E component showed the foundational semantic error found in the old A3 design. Their protocols are coherent,
but their empirical results remain pending.
