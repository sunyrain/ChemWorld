# Work II EQ-S v0.1 parameter-non-collapse preflight

**Status:** FAIL CLOSED before provider-free gate and before any provider call

**Provider calls:** 0

## Purpose

The approved EQ-S v0.1 contract requires the aqueous-ion-pair worlds to remain distinguishable from a direct-precipitation null after that null is allowed to refit pKa, log10(Ksp), the common cation fraction, and one activity-coefficient ratio. This preflight evaluated that requirement directly from the approved algebraic equations before implementing or freezing a provider-facing runner.

The registered fit set was `Q01,Q03,Q04,Q05,Q08,Q10`; the disjoint holdout set was `Q02,Q06,Q07,Q09,Q11,Q12`. The direct null was fitted over deliberately broad bounds:

```text
pKa:                       3 to 7
log10(Ksp):               -8 to -3
cation fraction:        0.01 to 0.50
activity coefficient:    0.1 to 10
optimizer seed:       20260920
```

The frozen proposed criterion was absolute held-out error above `0.018` (three final-assay noise scales) in at least two public metrics and at least three held-out conditions.

## Approved v0.1 result

| World | Approved beta (L/mol) | Approved log10(Ksp) | Holdouts passing 2-metric criterion | Largest held-out errors: pH / dissociation / precipitation |
|---|---:|---:|---:|---|
| EQ-S-W02 | 45 | -5.0 | 0/6 | 0.00516 / 0.00244 / 0.00258 |
| EQ-S-W04 | 140 | -4.6 | 0/6 | 0.01164 / 0.00364 / 0.00918 |

Both ion-pair worlds fail. The direct null absorbs their response by parameter refitting, so proceeding would relabel a practically P-like contrast as S.

## Minimal repair candidate v0.2

Keep the approved equations, pKa ladder, O/A/M dossiers, twelve Q conditions, scoring definitions, denominators, and execution order unchanged. Change only the private association/Ksp strength:

| World | Mechanism | pKa | Proposed common log10(Ksp) | Proposed beta (L/mol) |
|---|---|---:|---:|---:|
| EQ-S-W01 | direct | 4.6594047891 | -5.2 | absent |
| EQ-S-W02 | ion-pair intermediate | 4.8394047891 | -5.2 | 6000 |
| EQ-S-W03 | direct | 5.0194047891 | -5.2 | absent |
| EQ-S-W04 | ion-pair intermediate | 5.1994047891 | -5.2 | 8000 |
| EQ-S-W05 | direct | 5.3794047891 | -5.2 | absent |

Using one common Ksp removes Ksp as a structure-correlated nuisance. The pKa means remain exactly matched between mechanism families.

## Candidate repair preflight

| World | Holdouts passing 2-metric criterion | Public response spans: pH / dissociation / precipitation | Largest held-out errors: pH / dissociation / precipitation |
|---|---:|---|---|
| EQ-S-W02 | 6/6 | 0.2309 / 0.1486 / 0.0775 | 0.0400 / 0.0207 / 0.0482 |
| EQ-S-W04 | 4/6 | 0.2324 / 0.0976 / 0.0399 | 0.0327 / 0.0163 / 0.0277 |

The repaired candidates clear the preregistered non-collapse count while retaining nonzero, nonsaturated variation in all three public channels. These figures are development preflight evidence, not a passed provider-free gate. Exact replay, numerical stability, leakage, scale-control, scorer-fixture, and full null-fit checks still have to pass in the formal gate.

## Decision

v0.1 is retained as a failed design attempt. It must not be silently modified or provider-executed. The versioned v0.2 private-world repair requires human approval because beta and Ksp are scientific contract values.
