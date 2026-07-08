# PhysChem Core Design

ChemWorld now includes a small `chemworld.physchem` layer. Its job is to make
the shared physical-chemical world more professional without turning the
benchmark into a heavy process simulator.

## Reference Reading

The local reference repositories were used as design references only:

- `chemicals` separates elemental bookkeeping, formula parsing, molecular
  weights, and composition utilities.
- `thermo` separates chemical constants from property-correlation packages and
  mixture state objects.
- `Cantera` uses declarative species, phase, and reaction specifications as the
  stable interface between mechanism files and numerical kernels.

ChemWorld localizes those ideas into a compact, auditable, JSON-friendly core.
No reference-project source code is copied.

## Current Scope

The first implementation slices cover the P1 and P2 TODO foundation:

- `ElementSpec`: benchmark-relevant element metadata.
- `parse_formula`: formula parsing with nested parentheses and charge stripping.
- `molecular_weight`: molecular weight from elemental composition.
- `ComponentSpec`: component identity, formula, charge, phase, safety tags, and
  allowed property-correlation IDs.
- `MixtureSpec`: self-contained mole/mass fraction state with component molecular
  weights, temperature, pressure, and phase label.
- `PropertyCorrelation`: portable correlation metadata with explicit units and
  validity ranges.
- `PropertyEvaluation`: a value, unit, inputs, validity warnings, and
  correlation provenance.
- `ComponentPropertyPackage`: a component-local correlation package that chooses
  an in-range method when multiple correlations exist.

## Property Core

The P2 property core is implemented in `chemworld.physchem.properties`. It
supports the following local evaluators:

| Property family | Supported equations |
| --- | --- |
| Vapor pressure | Antoine, Wagner |
| Heat capacity | Cp polynomial |
| Enthalpy | analytic Cp-polynomial sensible-enthalpy integral |
| Phase change | Watson heat-of-vaporization correlation |
| Density | linear liquid density, ideal gas density |
| Viscosity | Andrade liquid viscosity |
| Surface tension | critical-temperature power law |
| Mixture rules | mass-fraction specific-volume density, log-viscosity rule |
| Safety proxies | volatility risk from vapor pressure, thermal hazard proxy |

Every correlation declares:

- `property_id`;
- `equation_id`;
- coefficients;
- input units;
- output unit;
- validity ranges;
- source notes.

Evaluation uses canonical ChemWorld inputs such as `temperature_K` and
`pressure_Pa`, converts them into the correlation's declared input units, and
returns a `PropertyEvaluation`. Out-of-range inputs can warn, raise, or be
ignored through a `validity_policy`.

## Boundaries

This layer is now a real local property-correlation core, but it is not yet a
complete process simulator. It does not perform flash calculations, EOS solves,
activity-coefficient calculations, or reaction mechanism generation. Those will
be built on top of these specs in later TODO milestones.

## Validation Rules

The core fails early when:

- a formula has unknown elements or unsupported hydrate/dot syntax;
- mole or mass fractions are negative or do not sum to one;
- mixture temperature or pressure is nonpositive;
- a component phase is outside the supported phase labels;
- a property correlation references an unsupported unit;
- a validity range is reversed or degenerate.

This gives later transition kernels a cleaner contract: invalid chemistry
metadata should fail before simulation begins.
