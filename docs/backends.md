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

## Reference Validation

Reference backends are not transition backends. They are optional external
packages used to check selected formulas or limiting cases during development.
The current validation layer lives in `chemworld.physchem.reference_validation`
and supports installed packages or local source snapshots under
`reference_repos/`.

Current executable checks compare ChemWorld with `chemicals`, `fluids`, and
`thermo` for ideal-gas molar volume, Rachford-Rice flash, curated DIPPR101
vapor-pressure points, curated Poling ideal-gas Cp and sensible enthalpy
integrals, Reynolds number, Prandtl number, Haaland Darcy friction factor,
single-phase Darcy-Weisbach pipe pressure drop, ideal Raoult-law bubble/dew
pressure, a controlled ideal two-phase TP flash, and fixed-parameter Wilson/NRTL
activity coefficients. These tests skip by default and run only when
`CHEMWORLD_RUN_REFERENCE_TESTS=1` is set.
