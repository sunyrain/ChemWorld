# repeat-02 / C-W04-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T11:12:16.477054+00:00; available public operations: 0; reviewed through: None.

# Initial hypotheses

H1 [tentative] Catalyst and solvent identities are opaque; a first batch at moderate temperature with C0/S0 will establish conversion and crystallization feasibility. I expect longer reaction residence and controlled seeded cooling to improve recovery, while overly rapid/deep cooling may raise fines. This is a testable starting expectation, not material-specific knowledge.

Plan: screen catalyst/solvent combinations and reaction temperature, then refine seed dose, cooling rate, endpoint, and thermal history. Quality constraints take precedence over native score.

## Revision 2

Recorded: 2026-10-14T11:14:02.589582+00:00; available public operations: 68; reviewed through: runner-operation-0068.

# Working hypotheses after batches 1–4

H1 [supported in tested S0 scope] C0–C3 at 350 K/1 h all reach near-complete conversion, but selectivity is only moderate. HPLC events runner-operation-0007, -0019, -0033, -0049 show no decisive catalyst advantage given single noisy measurements; final assays suggest C1/C3 are worth retaining.

H2 [disconfirmed in tested scope] Simply extending/staging cooling and increasing seed from 0.02 g to 0.5 g did not solve fines. Final assays runner-operation-0013, -0027, -0043, -0068 all report fines about 0.99–1.00 and size indices below 0.08. Batch 2 gave the largest observed index (0.077) but still failed fines. The seed-dose comparison is confounded with catalyst and cooling history; nevertheless a large benefit is absent.

H3 [tentative] Solvent identity may dominate crystallization morphology. Next tests will screen S1–S3 with a retained catalyst and controlled slow cooling, then consider warm maturation/redissolution if morphology remains poor. A solvent giving clearly larger size/lower fines would change the optimization focus.

## Revision 3

Recorded: 2026-10-14T11:16:21.019415+00:00; available public operations: 189; reviewed through: runner-operation-0189.

# Final source-stage hypotheses

H1 [supported in tested conditions] Reaction performance depends strongly on temperature/solvent/catalyst combination. With C1/S3, 370 K for 1800 s produced near-complete conversion and about 0.61–0.64 selectivity/yield signals across batches 10–12 (HPLC events runner-operation-0148, -0163, -0179), outperforming the lower-temperature C0/S3 test (runner-operation-0132). This is a bounded empirical relationship, not an identified mechanism.

H2 [supported in tested conditions] High-temperature seeding followed by very slow staged cooling is necessary for acceptable morphology in S3. Batches 7, 8, 10–12 (final assays runner-operation-0111, -0126, -0157, -0173, -0189) had fines 0.19–0.28, whereas quenched/low-temperature-seeded batches generally had about 0.99–1.00 fines. The contrast is confounded partly by solvent, but batch 9 shows that S3 plus post-quench seeding alone did not suffice (runner-operation-0142).

H3 [supported in tested range] Extending the slow cascade to 250 K increased observed seed-excluded recovery while preserving purity and fines: batch 11 reached 0.565 yield with 0.991 purity and 0.227 fines (runner-operation-0173). Reducing S3 from 0.08 to 0.06 L in batch 12 gave the highest observed recovery, 0.574, with 0.996 purity and 0.187 fines (runner-operation-0189). The numerical advantage over batch 11 is modest relative to single-run uncertainty and is not proof of a concentration effect, but batch 12 is the best completed qualifying observation.

Decision: recommend batch 12. This would change if replication showed its recovery advantage is noise or if reduced solvent caused fines above 0.50; neither occurred in the completed campaign.
