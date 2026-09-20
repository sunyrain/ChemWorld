# Work II EQ bounded aqueous equilibrium protocol v1.0

This task profile inherits the source → K1 → Q → K2 ordering, truth embargo, write-once outputs, failure retention, and English free-text requirements of `WORK_II_CANONICAL_K1_Q_K2_PROTOCOL_V1_1.md`.

## Source commission

The Agent has one primary task: characterize the bounded aqueous equilibrium slice. It should identify effective relationships among total loading, liquid volume or dilution, pH, acid dissociation, and the precipitation proxy; distinguish supported relationships from equivalent explanations; and state uncertainty and limits. There is no yield-optimization task and no product-process objective.

Each source is an independent twelve-batch campaign with twelve optional non-final instrument uses and twelve final assays. Experimental choice is autonomous. The participant may use single-shot or staged additions and may repeat conditions. No fixed equation form, belief snapshot, or batch grouping is required.

## Three-arm parameter prior

The only manipulated prior locus is the effective acidity/dissociation and dilution-response relationship. Strict Opaque contains no instance-specific value, direction, tolerance, precipitation threshold, optimum, recipe, or calibrated informative region. Aligned and MisIndexed carry the same public anchor, claim schema, precision, source description, interval width, and 80% confidence statement. MisIndexed substitutes a pre-registered relationship from another frozen world and changes nothing else.

The shared public measurement contract states that `pH_normalized = pH / 14`, acid dissociation is a bounded fraction, and `precipitation_signal` is a bounded proxy. It also states that the environment's `equilibrium_confidence` is not the Agent's confidence and not a task score. These shared definitions are not prior-locus claims.

## K1

After the experiment recommendation or evidentiary anchor is sealed, request a complete, independently readable English report. It must explain the Agent's effective mechanism or relationships, the experiments and numerical observations that formed or changed them, possible equations, scope, uncertainty, identifiability limits, and plausible equivalent or competing explanations. It must distinguish observation, interpolation, extrapolation, and conjecture. No new experiment is allowed.

## Q

Only after K1 is sealed, reveal the twelve action lists bound in the machine config. For each query and each of the three registered prediction metrics, require a point estimate and an 80% prediction interval plus an English per-query rationale and shared rationale. All queries start independently from the same frozen world. The same questions are used for all arms. Q coordinates are absent from the source prompt and initial task contract.

Evaluate absolute error to the mean of five independently seeded reference observations, empirical 80% coverage over all five observations, interval width, and the standard interval score at alpha 0.2. Report each metric separately; do not collapse them into a new `equilibrium_confidence` score.

## K2

After K1 and Q are sealed and before any truth is returned, request an English seven-part retrospective:

1. Which supplied effective-acidity or dilution claims were supported, contradicted, or untested? If no instance claim was supplied, say so.
2. Which experiments actually formed or changed the account, and which choices depended on the prior, accumulated observations, or an untested assumption?
3. What competing or equivalent explanations remain, and what can the evidence distinguish?
4. What single additional legal experiment would be most informative, what would be measured, and how would possible results change the account?
5. How did the characterization objective shape experiment selection, including any trade-off between broad coverage, replication, and local identification?
6. What acquired evidence was underused, which predictions are least reliable, and which intervals may be too narrow or inconsistent with K1?
7. What are the limits of the sealed evidentiary anchor and of generalization across concentration, volume, staged additions, precipitation regime, and worlds?

K2 may cite prior outputs but cannot rewrite them. Truth generation and scoring begin only when every formal cell has a sealed K2.

