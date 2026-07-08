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

Design rules:

- keep specs serializable with plain JSON types;
- fail early on unknown elements, invalid phases, invalid units, or invalid
  fractions;
- keep property correlations separate from component identity;
- add optional reference-backend comparisons only as skipped tests or adapters;
- do not copy source code from `reference_repos/`.

