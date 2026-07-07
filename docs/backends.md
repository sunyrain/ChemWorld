# Backends

ChemWorld separates the shared world law from the implementation that advances
hidden state. The current backend is:

```text
semi_mechanistic
```

It uses Arrhenius reaction ODEs, a simplified energy balance, phase partition
heuristics, separation ledgers, and instrument-cost updates.

## Why This Exists

`WorldLawSpec` defines ontology, constitution, operation registry, transition
kernel registry, and observation kernel registry. A backend implements those
transition modules at a particular fidelity.

This prevents the current semi-mechanistic implementation from becoming the
entire meaning of ChemWorld. Future backends can target the same world law:

- Cantera-style reaction/thermodynamic backend;
- IDAES/DWSIM-style process backend;
- ASE/MLIP-style atomistic backend;
- real-lab adapter backend.

Those are roadmap targets, not current claims.
