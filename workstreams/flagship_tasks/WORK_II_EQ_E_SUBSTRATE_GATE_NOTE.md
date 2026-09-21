# Work II EQ-E multi-entity substrate and small gate

## Authorized scope

This step builds an executable numerical substrate for the EQ entity locus and runs a small provider-free gate. It does not authorize an EQ-E Agent canary or the 15-cell provider matrix.

## Entity question

Three anonymous selectable aqueous media (`medium-0`, `medium-1`, and `medium-2`) share exactly the same species graph and two equilibrium equations:

```text
HA(aq) <=> H+(aq) + A-(aq)
M+(aq) + A-(aq) <=> MA(s)
```

Each identity binds a private vector of acid-ionization, solubility, cation-loading, and activity properties. The scientific object is the mapping from entity identity to that joint property pattern. Changing one scalar for one common material would be P; adding or deleting a species or equation would be S. Neither is the EQ-E treatment.

## Public information arms for later design

- `Opaque`: no instance-level entity dossier.
- `Aligned`: a qualitative selector-to-property ordering with no numerical constant or recipe.
- `MisIndexed`: the same fields and precision under a fixed no-fixed-point cyclic permutation.

The small gate checks schema symmetry and leakage only. It does not call an Agent.

## Gate design

For each of three deterministic noise repeats, evaluate every entity at four common analytical concentrations and one same-concentration double-volume control: 15 conditions per repeat and 45 total numerical executions. Exact replay uses the same observation seeds.

Pass only if:

1. all 45 executions and exact replays complete with zero provider calls;
2. at every common concentration, at least two of the three public metrics span more than the preregistered identity threshold;
3. same-entity, same-concentration scale controls remain within tolerance;
4. every entity uses the identical direct-network equation set, has no aqueous intermediate, and solves below the residual threshold;
5. an identity-independent P null is refuted by the simultaneous same-coordinate response spans;
6. Opaque is null, Aligned and MisIndexed are field matched and unequal, the cyclic map has no fixed point, and no private numeric field leaks.

Failure is retained and repaired by version. A pass licenses five-world and O/A/M design work only; it does not license provider execution.
