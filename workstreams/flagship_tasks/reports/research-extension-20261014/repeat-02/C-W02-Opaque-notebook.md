# repeat-02 / C-W02-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T17:42:36.880520+00:00; available public operations: 0; reviewed through: None.

# Initial hypotheses

H1 [tentative] Catalyst and solvent identities are opaque; reaction conversion/selectivity may vary strongly across choices. Initial screen will hold charge and thermal program constant while changing catalyst/solvent.

H2 [tentative] Slow seeded cooling followed by a cold hold should reduce fines and improve recovery relative to fast or unseeded cooling. Prediction: moderate seed dose and slow cooling will meet purity >=0.80 and fines <=0.50 more reliably; hotter reaction or prolonged hot exposure may raise conversion but risk degradation.

Decision: use early batches for broad catalyst/solvent and crystallization-condition screening, then exploit the best feasible region. These claims will change if measured final assays show opposite trends.

## Revision 2

Recorded: 2026-10-13T17:47:02.703403+00:00; available public operations: 184; reviewed through: runner-operation-0184.

# Final source-stage hypotheses

H1 [supported in tested scope] Solvent identity dominated particle quality under the common C0 reaction and seeded/reheat program. S2 gave feasible fines (0.273 at event runner-operation-0123), whereas S0 and S1 remained above the 0.50 limit (events runner-operation-0060 and runner-operation-0108); S3 was borderline feasible at 0.462 but with lower recovery (runner-operation-0138). These are single-batch comparisons with assay noise, but the separations are substantially larger than the declared per-assay fines noise.

H2 [supported in tested scope] A small seed charge (0.001 g), slow cooling, one partial redissolution at 315 K, recooling, and a colder final stage can produce high-purity, low-fines crystals in S2. Batch 10 reached crystal_yield 0.6147, purity 0.9816, and fines 0.3014 (runner-operation-0153). Batch 12 reproduced feasibility with yield 0.6086, purity 0.9979, and fines 0.2920 (runner-operation-0184). Their yield difference is smaller than a cautious comparison based on the declared 0.01 assay noise, so which thermal variant is intrinsically superior remains unresolved.

H3 [supported, adverse concentration effect in tested scope] Reducing S2 volume from 0.06 L to 0.04 L did not materially increase observed recovery but sharply increased fines to 0.9937 (runner-operation-0168), compared with 0.3014 at 0.06 L (runner-operation-0153). Thus higher concentration is rejected for the present quality-constrained recommendation.

H4 [partly supported] Partial redissolution improved S0 particle quality relative to the early direct-cooling batches, but S0 still failed the fines limit (events runner-operation-0013, runner-operation-0025, and runner-operation-0060). This supports selective dissolution/growth as a useful direction but not as sufficient without a favorable solvent.

Decision: recommend completed batch 10 because it has the highest observed crystal recovery among batches satisfying purity >=0.80 and fines <=0.50. Batch 12 is a close feasible replicate/variant and the apparent recovery ordering should not be overinterpreted. Conditions that would change this decision: a replicate showing batch 12 or another S2 schedule has clearly higher recovery while retaining the quality constraints, or evidence that the batch-10 fines estimate is not representative.
