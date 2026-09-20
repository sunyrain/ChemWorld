# Work II EQ-S Mechanism-Structure Design v0.1

**Status:** revised draft for human approval; design only; no provider execution authorization

**Approval checkpoint:** two equation-level mechanism families, five private worlds, three public information arms, twelve sealed prediction queries, and the structural scorer

**Not authorized by this document:** provider-free gate execution, Agent/provider calls, W01 canary, remaining twelve cells, reference-truth generation, or formal benchmark claims

## 1. Mechanistic question

EQ-S v0.1 asks which equilibrium reaction network operates in the bounded weak-acid/precipitation world:

1. **direct free-ion precipitation**, with no stable dissolved ion-pair intermediate; or
2. **aqueous ion-pair intermediate**, where a distinct dissolved `MA(aq)` species participates in the mass balances before solid formation.

This is an S-locus because the species graph and equation set change. pKa, Ksp, association strength, and activity coefficients are P-locus quantities and remain private nuisance parameters.

The former path-memory proposal is rejected for this version. Addition order is not the defining contrast, and all registered Q conditions use the same one-shot preparation order.

## 2. Common chemistry and public observables

`HA` is the bounded weak acid, `A-` its conjugate base, and `M+` a co-delivered precipitating cation at one fixed common stoichiometric fraction. The identity and stoichiometry are unchanged across the five worlds, so this is not an E-locus intervention.

Both families share acid dissociation and the same solid phase:

```text
HA(aq) <=> H+(aq) + A-(aq)                  Ka
MA(s)   <=> M+(aq) + A-(aq)                Ksp
```

The three public outputs keep one definition across both families:

```text
pH_normalized = pH / 14
acid_dissociation_fraction = n_A- / n_A,total
precipitation_signal = n_MA(s) / n_A,total
```

The dissociation output preserves the existing EQ meaning as the free conjugate-base fraction; paired and solid material remain visible indirectly through mass balance and the precipitation channel. All outputs remain clipped to the existing `[0, 1]` public contract. Numerical residual and environment confidence remain diagnostics, not Agent uncertainty or task scores.

## 3. Competing mechanism families

### 3.1 Family D: direct free-ion precipitation

Species graph:

```text
HA <=> H+ + A-
M+ + A- <=> MA(s)
```

There is no distinct dissolved `MA(aq)` node. The analytical balances are:

```text
C_A V = n_HA + n_A- + n_MA(s)
C_M V = n_M+          + n_MA(s)
```

Together with charge balance, acid dissociation, and the Ksp complementarity condition, this is an algebraic endpoint model.

### 3.2 Family I: aqueous ion-pair intermediate

Species graph:

```text
HA <=> H+ + A-
M+ + A- <=> MA(aq)                           beta
M+ + A- <=> MA(s)
```

The additional relationship and balances are:

```text
[MA(aq)] = beta * a_M+ * a_A-
C_A V = n_HA + n_A- + n_MA(aq) + n_MA(s)
C_M V = n_M+          + n_MA(aq) + n_MA(s)
```

The soluble pair is deprotonated acid but not precipitate. It therefore changes the concentration-dependent coupling among pH, total deprotonation, and solid formation.

### 3.3 Non-collapse requirement

Family I is not defined as “Family D with beta set to a different number.” `MA(aq)` is absent from Family D's species set and mass balances. The later provider-free gate must additionally demonstrate that refitting pKa, Ksp, the common cation fraction, and one activity-coefficient ratio in Family D cannot reproduce held-out Family-I responses across the registered concentration range. If that test fails, EQ-S fails rather than being relabeled as a parameter task.

## 4. Five private physical worlds

The structural pattern alternates across centered pKa and log10(Ksp) nuisance ladders. The mean pKa and mean log10(Ksp) are exactly equal between the two mechanism families, preventing a linear structure/parameter confound.

| World | Private pKa | Private log10(Ksp) | Mechanism family | Private beta (L/mol) | MisIndexed donor |
|---|---:|---:|---|---:|---|
| EQ-S-W01 | 4.6594047891 | -5.2 | direct free-ion precipitation | absent | EQ-S-W02 |
| EQ-S-W02 | 4.8394047891 | -5.0 | aqueous ion-pair intermediate | 45 | EQ-S-W01 |
| EQ-S-W03 | 5.0194047891 | -4.8 | direct free-ion precipitation | absent | EQ-S-W04 |
| EQ-S-W04 | 5.1994047891 | -4.6 | aqueous ion-pair intermediate | 140 | EQ-S-W03 |
| EQ-S-W05 | 5.3794047891 | -4.4 | direct free-ion precipitation | absent | EQ-S-W04 |

The numerical values are private authoring candidates. Approval freezes them for the provider-free gate; it does not assert that the gate will pass. A gate failure requiring any scientific-value change returns to human review.

## 5. Three information arms

### Opaque

`initial_world_model = null`. The Agent receives only the common task, legal operation, instrument, resource, and measurement contracts. It is not told that an ion pair is the benchmarked distinction and is not shown the candidate mechanism families.

### Aligned

The Agent receives the correct equation-level mechanism dossier. It identifies the species topology and symbolic balance structure but includes no pKa, Ksp, beta, activity coefficient, numerical transition point, response slope, optimal recipe, or Q coordinate.

### MisIndexed

The Agent receives the same dossier schema, field order, scope, confidence, and symbolic precision, populated from the registered opposite-family donor. `MisIndexed` is retained as the matrix label; its semantic subtype is `mechanism_misspecification`.

### Matched dossier schema

```json
{
  "schema_version": "chemworld-eq-mechanism-prior-0.1",
  "locus": "S",
  "scope": "bounded weak-acid/precipitation equilibrium characterization",
  "network_family": "direct_free_ion_precipitation | aqueous_ion_pair_intermediate",
  "acid_step": "HA(aq) <=> H+(aq) + A-(aq)",
  "dissolved_branch": "MA(aq) absent | M+(aq) + A-(aq) <=> MA(aq)",
  "solid_step": "M+(aq) + A-(aq) <=> MA(s)",
  "dissolved_acid_balance": "HA + A- | HA + A- + MA(aq)",
  "diagnostic_implication": "three-metric concentration response should follow the stated species graph",
  "confidence": {
    "coverage": 0.8,
    "source_class": "independent bounded mechanism study",
    "qualification": "local reaction-network claim; not a universal aqueous-chemistry law"
  }
}
```

The vertical bars show the two possible values in this review document. An actual payload contains one family-specific value per field.

| World | Opaque | Aligned mechanism | MisIndexed mechanism |
|---|---|---|---|
| EQ-S-W01 | null | direct | ion-pair intermediate |
| EQ-S-W02 | null | ion-pair intermediate | direct |
| EQ-S-W03 | null | direct | ion-pair intermediate |
| EQ-S-W04 | null | ion-pair intermediate | direct |
| EQ-S-W05 | null | direct | ion-pair intermediate |

Every wrong prior is therefore wrong in reaction-network topology, not merely in a numerical constant.

## 6. Sealed twelve-query Q panel

Every Q batch begins independently from the same initial world. All use `add_solvent -> add_reagent -> terminate -> final_assay`; path order is deliberately held constant. The panel probes equation shape through concentration, dilution, and scale controls.

### Block A: concentration sweep at fixed 0.024 L

| Query | Reagent (mol) | Analytical concentration (mol/L) | Role |
|---|---:|---:|---|
| Q01 | 0.00001 | 0.0004167 | low-concentration asymptote |
| Q02 | 0.00010 | 0.0041667 | pre-transition response |
| Q03 | 0.00060 | 0.0250000 | low/intermediate response |
| Q04 | 0.00300 | 0.1250000 | association-sensitive response |
| Q05 | 0.01200 | 0.5000000 | high-concentration response |
| Q06 | 0.03000 | 1.2500000 | boundary extrapolation |

### Block B: dilution sweep at fixed 0.003 mol

| Query | Solvent (L) | Analytical concentration (mol/L) | Role |
|---|---:|---:|---|
| Q07 | 0.006 | 0.5000000 | concentrated dilution endpoint |
| Q08 | 0.018 | 0.1666667 | near-transition dilution endpoint |
| Q09 | 0.048 | 0.0625000 | diluted response |
| Q10 | 0.075 | 0.0400000 | high-dilution response |

Q04 also belongs to the fixed-amount sequence at 0.024 L.

### Block C: constant-concentration scale controls

| Query | Solvent (L) | Reagent (mol) | Concentration (mol/L) | Role |
|---|---:|---:|---:|---|
| Q11 | 0.012 | 0.00030 | 0.025 | small-scale control |
| Q03 | 0.024 | 0.00060 | 0.025 | middle-scale anchor |
| Q12 | 0.072 | 0.00180 | 0.025 | large-scale control |

Q05/Q07 provide a second same-concentration control at 0.5 mol/L. These controls detect unintended amount-, volume-, or implementation-scale artifacts; they are not expected to create a mechanism difference.

The exact executable actions are in `configs/benchmark/work_ii_eq_structural_v0.1.design.json`. Q coordinates and truth remain unavailable during source experimentation.

## 7. K1, K2, and EQS

K1 and K2 retain the approved universal English protocol, with EQ-S-specific additions rather than a replacement rubric.

- K1: give a complete mechanistic report, state a reaction network and balances, explain how concentration and dilution experiments changed it, cite real batch IDs and values, and distinguish observations from extrapolation.
- K2: identify which evidence supports or contradicts an aqueous intermediate, distinguish a topology change from parameter refitting, give the strongest parameter-only competing explanation, and propose one decisive follow-up without running it.
- EQS: return a machine-readable family, aqueous-intermediate assessment, selected equation IDs, rationale, and cited source batches.

Registered EQS enums:

```text
network_family:
  direct_free_ion_precipitation
  aqueous_ion_pair_intermediate
  indeterminate

aqueous_intermediate:
  absent
  present
  indeterminate

equation_ids:
  acid_dissociation
  free_ion_solid_equilibrium
  aqueous_ion_pair_association
```

EQS does not request numerical pKa, Ksp, or beta estimates; those would be P questions.

## 8. Structural scorer

The primary scorer is deterministic and has no LLM judge.

### 8.1 Numeric Q prediction block

For 12 queries x 3 metrics x 5 independent reference executions:

- point-estimate MAE;
- empirical 80% interval coverage;
- mean 80% interval width;
- interval score under the existing EQ convention.

### 8.2 Equation-topology block

Truth equation sets are:

```text
direct = {acid_dissociation, free_ion_solid_equilibrium}
ion_pair = {acid_dissociation, free_ion_solid_equilibrium,
            aqueous_ion_pair_association}
```

Report by arm and overall:

- exact network-family accuracy;
- intermediate-presence accuracy;
- exact equation-set accuracy;
- equation-set Jaccard score;
- abstention rate, with `indeterminate` valid but never counted correct.

Contradictory outputs, such as `direct` plus `aqueous_intermediate=present`, fail schema validation rather than being silently repaired.

### 8.3 Mechanism-response-shape block

For Q01-Q06, set `x_i = log10(reagent_mol_i / 0.024 L)`. For each public metric, compute adjacent divided slopes and interior changes in slope:

```text
s_i = (y_(i+1) - y_i) / (x_(i+1) - x_i)
k_i = s_(i+1) - s_i
```

Compare predicted and reference `s_i` and `k_i`. Report concentration-slope MAE and concentration-curvature MAE. This tests whether the Agent learned the equation shape rather than only isolated endpoints.

For the fixed-amount dilution sequence Q07-Q08-Q04-Q09-Q10, compute the same quantities against `log10(1 / volume_L)` and report dilution-slope and dilution-curvature MAE.

For scale controls Q11-Q03-Q12 and Q07-Q05, report the predicted and observed same-concentration invariance errors. These are negative controls and are reported separately, not rewarded as evidence for either family.

### 8.4 Parameter-only non-collapse diagnostic

This is a provider-free truth diagnostic, not an Agent score. Fit a direct-family null over pKa, log10(Ksp), common cation fraction, and one activity-coefficient ratio using the registered fit subset; evaluate a disjoint held-out subset. The gate must show:

- direct worlds are recoverable by the direct null within replay/noise tolerance;
- each ion-pair world retains held-out lack-of-fit above three final-assay noise scales in at least two public metrics and at least three held-out conditions.

The fit/holdout partition and optimizer seed must be frozen before the gate. Failure means the proposed S axis collapses toward P and cannot proceed.

### 8.5 Arm comparisons

The independent analysis unit is the world-arm session. Report Aligned-Opaque and MisIndexed-Opaque contrasts for topology, numerical calibration, and response-shape metrics. With five worlds, results remain descriptive/exact-randomization-ready; no high-powered population claim is allowed.

No weighted composite score is authorized. It must remain visible whether a prior improves mechanism selection while harming quantitative calibration.

## 9. Provider-free gate after approval

The later gate fails closed unless all of the following pass:

1. exactly 5 worlds x 3 arms x 12 source batches;
2. zero provider calls;
3. Opaque is null and contains no candidate-family or equation hint;
4. Aligned and MisIndexed match in schema, scope, confidence, field order, and symbolic precision;
5. every MisIndexed donor has the opposite reaction-network topology;
6. no public S prior contains pKa, Ksp, beta, activity coefficients, transition coordinates, slopes, recipes, or Q coordinates;
7. all twelve Q conditions are legal, independently reset, fixed, and source-hidden;
8. exact replay, resource accounting, reset isolation, and numerical stability pass;
9. the Q concentration and dilution sweeps contain measurable but non-saturated response variation in every world;
10. scale controls remain invariant within registered replay/noise tolerance;
11. the parameter-only non-collapse diagnostic passes for all five worlds;
12. the topology and response-shape scorers reproduce hand-computed fixtures exactly.

These are requirements to be tested later, not claims that the gate has passed.

## 10. Execution after approval

```text
approve revised design
  -> implement coupled equilibrium solvers and structural scorer
  -> run provider-free gate with zero provider calls
  -> freeze passing code, configuration, prompts, queries, and hashes
  -> run EQ-S-W01 Opaque / Aligned / MisIndexed canary
  -> if all three 12-batch -> K1 -> Q -> K2 -> EQS chains pass,
     fill W02-W05 with at most eight isolated workers
  -> seal all 15 EQS outputs
  -> generate reference truth and score
  -> export English per-session and aggregate reports
```

Formal size: 15 independent source sessions, 180 source batches, 60 sealed posttests, and 300 reference executions.

Engineering-only repairs that preserve the frozen scientific contract may proceed automatically. Any change to mechanism equations, world values, arm content, Q coordinates, scorer definitions, or denominators returns to human approval.

## 11. E-locus hold point

EQ-E remains unauthorized for bulk execution. Its next artifact is a multi-entity substrate plus a small provider-free non-collapse gate showing that entity mapping cannot be absorbed by pKa/Ksp refitting (P) or by selecting the direct-versus-ion-pair equation family (S).

## 12. Human decision requested

Approval of revised v0.1 accepts:

1. direct free-ion precipitation versus an aqueous ion-pair intermediate as the S axis;
2. the five private world assignments and nuisance values in Section 4;
3. formula-level O/A/M dossiers with no numerical-parameter disclosure;
4. the concentration/dilution/scale Q panel in Section 6;
5. deterministic topology, response-shape, and parameter-non-collapse scoring.

Requested response: approve as written, or identify a world, arm field, Q condition, or scoring rule to revise.
