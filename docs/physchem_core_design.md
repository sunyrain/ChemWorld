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

## Reactor Model Core

The P4 reactor core is implemented in `chemworld.physchem.reactors`. It turns
mechanism-backed reaction networks into executable reactor models with material
and energy ledgers:

| Reactor model | Current implementation |
| --- | --- |
| Batch reactor | constant-volume mole balance, optional jacket heat, heat loss, reaction heat |
| Semi-batch reactor | scheduled feeds, variable volume, feed heat, material-in ledger |
| CSTR | dynamic well-mixed tank with inlet/outlet flows and steady-state integration helper |
| PFR | steady plug-flow model integrated over residence time |

All reactor results expose:

- `initial_state` and `final_state`;
- per-species amount trajectories;
- temperature trajectory;
- jacket-energy, reaction-heat, and heat-loss ledgers;
- feed and outlet material ledgers where relevant;
- element-based material-balance error;
- convenience metrics such as conversion and yield.

The implementation follows the same separation used by professional simulators:
mechanism files define chemistry, reactor models define transport and residence
time, and task/world layers define objectives and observations. This makes it
possible to add semi-batch, CSTR, PFR, reactive flash, and continuous-flow tasks
without creating separate toy environments.

## Equation-Of-State Core

The P5 EOS core is implemented in `chemworld.physchem.eos`. It gives ChemWorld a
local thermodynamic backend for gas and dense-fluid calculations:

| EOS capability | Current implementation |
| --- | --- |
| Ideal gas | molar volume, pressure, normalized composition, unit fugacity coefficients |
| Pure cubic parameters | Peng-Robinson and SRK `a alpha`, `b`, alpha, kappa |
| Mixture rules | classical one-fluid `a_mix`, `b_mix`, optional binary interaction `k_ij` |
| Compressibility | real admissible cubic `Z` roots |
| Phase root selection | vapor, liquid, and residual-Gibbs-style stable root selector |
| Fugacity | component fugacity coefficients for PR and SRK mixtures |

The EOS layer is JSON-friendly through `EOSComponentSpec`, `CubicEOSSpec`,
`EOSMixtureParameters`, and `EOSState`. It is designed to support future VLE,
flash, reactive flash, distillation, pressure-risk, and vapor-loss tasks without
making CoolProp, thermo, teqp, or thermopack required runtime dependencies.

## Phase-Equilibrium Core

The P6 phase-equilibrium core is implemented in
`chemworld.physchem.equilibrium`. It adds the first working bridge between EOS,
property correlations, and downstream separation tasks:

| Equilibrium capability | Current implementation |
| --- | --- |
| Activity coefficients | ideal, Margules, and NRTL-lite models |
| Raoult K-values | activity-corrected `K_i = gamma_i Psat_i / phi_i P` |
| Flash | Rachford-Rice vapor fraction and liquid/vapor compositions |
| Bubble/dew pressure | iterative estimates with activity coefficients |
| LLE stage | material-conserving extraction split with partition coefficients, phase volumes, stage efficiency, and entrainment |

This is still compact, but it is enough to make future extraction, evaporation,
distillation, solvent-screening, and purity/recovery tasks depend on shared
thermodynamic rules rather than fixed hand-tuned proxies.

## Separation Unit-Operation Core

The P7 separation core is implemented in `chemworld.physchem.separations`. It
wraps phase-equilibrium calculations into downstream processing units with
explicit outlet streams, cost/risk ledgers, heat duty, solvent loss, and material
balance errors:

| Unit operation | Current implementation |
| --- | --- |
| Liquid-liquid extraction | multistage extraction using partition coefficients, finite stage efficiency, entrainment, and solvent loss |
| Evaporation / flash | VLE-driven vapor/liquid split from K-values, heat duty, and concentration risk |
| Simple distillation | volatility-score separation with reflux, stage efficiency, distillate cut, heat duty, and purity/recovery tradeoff |
| Crystallization | solubility-limited crystallization, cooling proxy, impurity occlusion, crystal-size proxy |
| Filtration | solid recovery, impurity retention, washing efficiency, and wash loss |
| Drying | solvent removal, residual solvent, heat duty, thermal degradation risk |

All units return a shared `SeparationResult` with named outlets and a
`SeparationLedger`. This makes downstream processing benchmarkable: a task can
reward purity and recovery while penalizing cost, risk, solvent loss, and
process mass-balance errors. Excessive purification is therefore not
automatically optimal, which is important for realistic reaction-to-purification
tasks.

## Boundaries

This layer is now a real local property-correlation, reaction-network, reactor,
cubic-EOS, compact phase-equilibrium, and downstream unit-operation core, but it
is not yet a complete process simulator. It does not perform rigorous multiphase
stability analysis, database-grade flash calculations, automatic reaction
mechanism generation, or detailed transport calculations. Those will be built on
top of these specs in later TODO milestones.

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
