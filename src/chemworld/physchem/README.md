# ChemWorld PhysChem Core

This package contains compact physical-chemistry primitives used by ChemWorld
world-law modules. It is not a vendor copy of Cantera, thermo, chemicals, or
other reference projects.

Current scope:

- element metadata for benchmark-relevant elements;
- formula parsing with element conservation support;
- molecular-weight and elemental-fraction utilities;
- JSON-friendly `ComponentSpec`;
- self-contained `MixtureSpec`;
- explicit-unit `PropertyCorrelation` records.
- local property evaluators for vapor pressure, heat capacity, enthalpy,
  phase-change enthalpy, density, viscosity, surface tension, mixture rules,
  and safety proxies.

Design rules:

- keep specs serializable with plain JSON types;
- fail early on unknown elements, invalid phases, invalid units, or invalid
  fractions;
- keep property correlations separate from component identity;
- declare property units and validity ranges on every correlation;
- add optional reference-backend comparisons only as skipped tests or adapters;
- do not copy source code from `reference_repos/`.
