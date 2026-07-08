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
- general reaction-network specs for species, reactions, stoichiometric
  matrices, element-balance checks, YAML/JSON mechanism loading, rate-law
  evaluation, and deterministic batch ODE integration.
- mechanism-backed reactor kernels for batch, semi-batch, CSTR, and PFR
  calculations with material and energy ledgers.

Design rules:

- keep specs serializable with plain JSON types;
- fail early on unknown elements, invalid phases, invalid units, or invalid
  fractions;
- keep property correlations separate from component identity;
- keep mechanism definitions separate from reactor and task logic;
- keep reactor residence time, feed/outlet flow, and heat-transfer contracts
  explicit;
- declare property units and validity ranges on every correlation;
- reject unbalanced reaction networks before simulation;
- add optional reference-backend comparisons only as skipped tests or adapters;
- do not copy source code from `reference_repos/`.
