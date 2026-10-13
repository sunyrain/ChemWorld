# C-12 — model-authored source notebook

Development replication. Each version is the model's scientific account, not verified environment truth. Posttest answers are separate in the JSON record.

## Revision 1

Recorded: 2026-10-13T04:41:13.400937+00:00; public operations available: 0; reviewed through: not specified.

# Pre-experiment hypotheses

**H1 [tentative]** Within the nominal dossier, solvent S2 should favor high crystal recovery and larger/cleaner particles because it combines lower solubility, lower nucleation tendency, faster growth, and lower impurity occlusion. S1 is the conservative comparator; S0 may create excess fines/occlusion.

**H2 [tentative]** A moderate seed dose followed by slow cooling and a growth hold should reduce fines relative to unseeded/rapid cooling, while overly large seed dose may depress the seed-excluded recovery metric.

**Reaction expectation** Catalyst C1 at moderate temperature is a reasonable starting point from nominal activity and lower variability than C2/C3. I will first establish feasibility, then vary solvent, catalyst, seeding, cooling rate, and growth hold. Evidence from paid assays will override these priors.

---

## Revision 2

Recorded: 2026-10-13T04:47:09.407732+00:00; public operations available: 241; reviewed through: runner-operation-0241.

# Final source-stage hypotheses

**H1 [partly supported, narrow scope]** Solvent S1 gave the best crystallization-stage recoveries in this campaign, but the solvent comparison is confounded by thermal and seed changes and was not replicated under one identical recipe. S1 batches reached about 0.45–0.48 recovery with high purity (final assays: events runner-operation-0043, -0088, -0146), whereas tested S2 and S3 examples were lower (runner-operation-0014, -0029, -0115). This is an empirical process choice, not proof of a solvent identity mechanism.

**H2 [rejected for fines control in tested range]** Moderate seeding and slow/staged cooling did not make a practically meaningful reduction in the number fraction below 20 µm. Low, absent, 0.05 g, and 1 g seed conditions all returned fines near 1 (runner-operation-0043, -0074, -0088, -0179). Differences of a few hundredths are not persuasive relative to single noisy assays and recipe confounding.

**H3 [unsupported]** Partial reheating/redissolution and recooling did not solve the fines problem: the recrystallized batch remained at final-assay fines 1.0 (runner-operation-0061). A long warm-growth history (50 repeated growth stages) also remained at fines 1.0 (runner-operation-0241), opposing a simple residence-time-limited growth explanation.

**Decision** No completed batch satisfies both purity >=0.80 and fines <=0.50. Batch 6 has the highest observed crystal recovery (0.477) and assay purity clipped at 1.0 (runner-operation-0088), but fails the fines constraint (1.0); its small numerical recovery lead over batches 10 and 9 is not evidence of a reproducible advantage. I will select batch 6 only as the highest-recovery completed fallback and explicitly flag it as infeasible on fines.

**Unresolved alternative** The persistent fine-particle population may reflect an untested interaction or crystallization regime rather than seed dose or simple residence time. A future campaign should first identify a condition that suppresses secondary nucleation before optimizing recovery.

---
