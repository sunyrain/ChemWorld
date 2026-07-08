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

## Reaction Network Core

The P3 reaction-network core is implemented in
`chemworld.physchem.reaction_network`. It replaces hard-coded reaction lists
with declarative mechanism files and reusable numerical machinery:

| Capability | Current implementation |
| --- | --- |
| Species records | `SpeciesSpec` with formula, phase, charge, catalyst flag, observable aliases |
| Reaction records | `ReactionSpec` with equation string, stoichiometry, reversibility, heat of reaction |
| Network records | `ReactionNetworkSpec` with species/reaction ids, stoichiometric matrix, element matrix |
| Mechanism files | JSON and YAML loaders for portable mechanism definitions |
| Conservation | element-balance residuals and fail-fast checks for impossible reactions |
| Rate laws | mass action, Arrhenius, modified Arrhenius, reversible Arrhenius |
| Catalysis | catalyst activity multiplier and catalyst deactivation |
| Surface / biochemical proxies | Langmuir-Hinshelwood-lite and Michaelis-Menten-lite |
| Simulation | deterministic batch ODE integration with nonnegative amount projection |
| Scenario variation | seed-based parameter perturbation for public/private world splits |

Example mechanism files live under `configs/mechanisms/`:

- `simple_batch_reaction.yaml`: target reaction, side reaction, degradation,
  coupling impurity, and catalyst deactivation.
- `reversible_reaction.yaml`: a small equilibrium-like reversible case.

The reaction engine is intentionally compact, but it is not a placeholder. It
supports arbitrary balanced species/reaction networks, generates matrices for
downstream reactor models, and catches element-balance errors before an
environment starts. This makes the current five-reaction batch world just one
mechanism instance rather than a permanent architectural limit.

## Boundaries

This layer is now a real local property-correlation and reaction-network core,
but it is not yet a complete process simulator. It does not perform flash
calculations, EOS solves, activity-coefficient calculations, automatic reaction
mechanism generation, or detailed transport calculations. Those will be built
on top of these specs in later TODO milestones.

## Validation Rules

The core fails early when:

- a formula has unknown elements or unsupported hydrate/dot syntax;
- mole or mass fractions are negative or do not sum to one;
- mixture temperature or pressure is nonpositive;
- a component phase is outside the supported phase labels;
- a property correlation references an unsupported unit;
- a validity range is reversed or degenerate.
- a reaction references an unknown species;
- a reaction is not element balanced;
- a rate coefficient is negative, non-finite, or not numeric.

This gives later transition kernels a cleaner contract: invalid chemistry
metadata should fail before simulation begins.
