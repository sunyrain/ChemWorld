# Work II EQ-E v0.2 five-world entity-mechanism design

## Question and task boundary

EQ-E asks how a selectable anonymous aqueous-medium identity maps to a joint bundle of effective
acid-ionization, solid-formation, cation-availability, and activity properties, and whether the
resulting response law transfers across concentration and experimental scale. The common species
graph and reaction equations are fixed in every world and every arm. The task is open-form mechanism
characterization and entity mapping, not parameter optimization, medium ranking, or closed-set
identity classification.

Every source completes exactly twelve independent batches and seals an evidence-backed
entity-conditioned mechanism map plus one completed evidentiary-anchor batch. There is no operation
recommendation. The canonical K1 and K2 prompts therefore use the frozen “task delivery” semantics;
K2 item 7 must state that operation recommendation is not applicable and examine the limits and
transferability of the sealed entity map instead.

## Five physical worlds

Each world contains selectors `0`, `1`, and `2`. A selector binds four private properties jointly:
effective pKa shift, log solubility product, precipitating-cation fraction, and activity-coefficient
ratio. A world is not one scalar perturbation: changing entity changes the full property bundle.
Every world retains the same direct weak-acid/free-ion-precipitation topology and has no aqueous
intermediate.

The five worlds deliberately vary the correlation structure of the two public qualitative
descriptors. W01 is concordant; W02 creates an ionization-versus-solid-formation trade-off; W03 changes
the numerical bundle behind a superficially similar ordering; W04 moves the high-ionization and
early-solid roles to selector 1; W05 supplies the counterbalancing non-collinear mapping. Across the
five worlds, every selector occupies `higher`, `intermediate`, and `lower` at least once on each
descriptor axis. This prevents a global selector ordering, selector-name heuristic, or one common
scalar from solving the block.

Private numerical profiles are frozen in
`configs/benchmark/work_ii_eq_entity_v0.2.design.json`. They are never participant-visible.

## Information intervention

All three arms receive the same common reaction background. This corrects the v0.1 small-gate
draft, where the common topology prose lived inside only the Aligned/MisIndexed dossier.

- **Opaque:** no instance-level selector-to-property mapping.
- **Aligned:** the correct local qualitative mapping for the current world, using only `higher`,
  `intermediate`, `lower` for both ionization and solid-formation tendency.
- **MisIndexed:** exactly the same rows, fields, vocabulary, and precision after the frozen
  no-fixed-point cycle `0 -> 1 -> 2 -> 0`.

No arm receives a numerical constant, response coordinate, Q identifier, recipe, answer label, or
prescribed experiment. Opaque is missing only the E-locus mapping, not common non-E chemistry.

## Source resources and posttests

Each independent session has twelve vessels, twelve final assays, twelve optional non-final
instrument uses, 180 operation attempts, 0.24 mol reagent, and 0.72 L solvent. The Agent may choose
any of the three media in every batch, repeat conditions, and allocate measurements freely. Its
goal is characterization; no public task score rewards choosing a particular medium or maximizing a
single response.

The participant posttest chain is exactly `K1 -> Q -> K2`. K1 and K2 are byte-identical to the
task-delivery variant of the canonical v1.1 protocol. There is no EQE supplement, entity-answer menu,
property-vector menu, or composite mechanism score.

## Twelve blind prediction queries

Q uses the canonical outer prompt followed by one fixed payload shared by all worlds and arms:

| Query block | Selectors | Concentration | Volume | Purpose |
|---|---|---:|---:|---|
| Q01–Q03 | 0, 1, 2 | 0.005 M | 0.024 L | low-concentration entity contrast |
| Q04–Q06 | 0, 1, 2 | 0.080 M | 0.024 L | interior entity contrast |
| Q07–Q09 | 0, 1, 2 | 0.600 M | 0.024 L | high-concentration entity contrast |
| Q10–Q12 | 0, 1, 2 | 0.080 M | 0.048 L | equal-concentration double-scale control |

For every query the Agent predicts `pH_normalized`, `acid_dissociation_fraction`, and
`precipitation_signal`, with a point estimate, 80% interval, and English rationale. Scoring retains
ordinary point/interval metrics and separately reports entity-contrast, within-entity
concentration-transfer, and same-concentration scale-transfer errors. No family-accuracy endpoint is
defined.

## Provider-free design gate

Before any model call, execute all twelve Q conditions in every `world x arm` cell: 15 campaigns,
180 batches, and 180 tolerance-zero exact replays. Arms must be physically identical at matched
actions and keyed noise. The gate fails closed unless:

1. all denominators complete with zero provider calls and exact replay;
2. at each of the three primary concentrations in every world, at least two public metrics span more
   than 0.015 across entities;
3. every entity has a pH response span above 0.06 and a non-pH response span above 0.015 across the
   registered concentration range;
4. equal-concentration scale-control gaps remain below 0.015;
5. every entity uses the same direct topology, has no aqueous intermediate, and solves below the
   residual threshold;
6. the qualitative Aligned descriptors agree with the registered local behavior, MisIndexed is a
   no-fixed-point field-matched permutation, Opaque has no instance mapping, and no private numeric or
   Q field leaks; and
7. every selector is counterbalanced across all three descriptor levels on both axes, with at least
   four distinct five-world mapping patterns.

This is a design qualification, not Agent evidence. A pass returns the design and gate report for
human review. It does not authorize a canary or bulk provider execution.

## Later execution, if separately approved

Run W01 Opaque/Aligned/MisIndexed as a three-worker canary. Release W02–W05 only when all three
twelve-batch source and K1/Q/K2 chains validate. The remaining matrix may use at most eight isolated
workers with automatic slot refill. Platform recovery preserves the original failure and resumes the
same thread only from the latest legal boundary. Reference truth consists of five independent
keyed-noise repeats per `world x query` (300 executions) and remains embargoed until all fifteen K2
reports seal.

Transport recovery is frozen separately from the scientific contract. Before the first accepted
source action, a failed provider connection may be restarted at most twice; after any accepted action,
the source is never silently replayed. K1/Q/K2 remain same-thread continuations. Their provider client
uses at most two request/stream retries and the Codex `total`-scope automatic history-compaction
threshold of 120,000 tokens. This threshold applies only to the posttest continuation, after all source
actions and observations are sealed, and therefore cannot change experimental selection or physics.
