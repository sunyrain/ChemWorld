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

The implementation slices currently cover the P1-P8 foundation:

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
- reaction-network, reactor, EOS, phase-equilibrium, equilibrium-chemistry,
  separation, transport, and heat-transfer kernels described below.

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
- additional curated mechanisms now cover parallel/series selectivity,
  catalyst deactivation, autocatalysis, reaction-to-extraction,
  reactive-distillation-lite, CSTR multiplicity, PFR hotspot risk, and
  electrochemical selectivity.

The reaction engine is intentionally compact, but it is not a placeholder. It
supports arbitrary balanced species/reaction networks, generates matrices for
downstream reactor models, and catches element-balance errors before an
environment starts. This makes the current five-reaction batch world just one
mechanism instance rather than a permanent architectural limit.

## Mechanism and Scenario Library

The P10 mechanism/scenario library is implemented in
`chemworld.physchem.mechanism_library`. It turns mechanism files into a curated
benchmark resource rather than a loose folder of examples.

Current mechanism coverage:

| Mechanism | Main purpose |
| --- | --- |
| `simple_batch_reaction` | reference target/side/degradation/coupling/catalyst-loss world |
| `parallel_series_reaction` | competing selectivity and late impurity formation |
| `reversible_reaction` | minimal reversible equilibrium-like kinetic case |
| `catalyst_deactivation` | hidden activity loss and temperature tradeoff |
| `autocatalytic_reaction` | nonlinear induction and seed sensitivity |
| `reaction_extraction` | reaction coupled to aqueous/organic phase transfer |
| `reactive_distillation_lite` | reversible esterification with volatile pseudo-species |
| `cstr_multiplicity` | exothermic autocatalytic continuous-reactor slice |
| `pfr_hotspot` | PFR hotspot and heat-removal planning slice |
| `electrochemical_conversion` | electrochemical selectivity and energy proxy |

The companion scenario cards live in
`configs/scenarios/mechanism_scenarios.yaml`. Each card declares:

- the mechanism file and `mechanism_id`;
- the intended scenario/task family;
- recommended reactor or process backend;
- module tags such as reaction, equilibrium, phase partition, distillation,
  CSTR, PFR, electrochemistry, and heat transfer;
- default initial amounts, operating windows, and benchmark conditions;
- target and impurity species for scoring;
- expected qualitative behavior for explanation tasks and sanity checks.

The public API exposes:

- `list_mechanism_paths()`;
- `list_mechanism_cards()`;
- `get_mechanism_card(card_or_mechanism_id)`;
- `load_library_mechanism(card_or_mechanism_id)`;
- `validate_mechanism_library()`.

`validate_mechanism_library()` is the CI-facing contract. It checks that every
mechanism file has a card, every card resolves to a file, every network passes
element conservation, and every card's initial/target/impurity species are
declared by the mechanism. This keeps task expansion anchored to a shared
physical-chemistry world instead of drifting into unrelated mini-games.

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

## Equilibrium-Chemistry Core

The P9 equilibrium-chemistry core is implemented in
`chemworld.physchem.equilibrium_chemistry`. It covers reaction equilibrium and
aqueous/electrolyte proxies that are separate from the VLE/LLE phase-equilibrium
layer:

| Capability | Current implementation |
| --- | --- |
| Reaction equilibrium spec | `EquilibriumReactionSpec` with stoichiometry, reference `log10(K)`, reaction enthalpy, and concentration activity model |
| Problem spec | `EquilibriumSystemSpec` at fixed temperature, pressure, and volume |
| Extent formulation | scalar extent bounds for single reactions and coupled extent-space least-squares for multi-reaction systems |
| Equilibrium constant | van't Hoff temperature dependence from `K_ref`, `T_ref`, and `Delta H` |
| Reaction quotient | concentration-based `Q` and `ln Q` utilities |
| Acid/base | monoprotic weak-acid equilibrium with electroneutrality, water autoionization, pH/pOH, and ionic strength |
| Water ion product | compact temperature interpolation for `K_w` |
| Precipitation | binary solubility-product precipitation with saturation index and material-balance error |
| Charge balance | single-ion electroneutrality adjustment and net charge equivalents |
| Ionic strength | molality-based and amount-based ionic-strength calculations |
| Solid solubility | eutectic-style mole-fraction solubility proxy |

The reference projects informed the architecture rather than the source code.
Reaktoro separates chemical state, equilibrium specifications, restrictions,
conditions, and solvers; Cantera exposes equilibrium through constrained pairs
such as `TP` and `HP`; thermo/chemicals provide focused electrolyte and
solubility utilities. ChemWorld localizes the same separation into lightweight
JSON-friendly specs and result objects suitable for benchmark replay.

This layer is intentionally not a full Gibbs-energy minimizer. It is the
professional first slice needed for ChemWorld tasks where agents must reason
about reversible chemistry, pH, precipitation thresholds, electroneutrality, and
ionic strength under finite experimental budgets.

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

## Transport and Heat-Transfer Core

The P8 transport core is implemented in `chemworld.physchem.transport`. It adds
the first local equipment-calculation layer needed by professional interaction
environments: flow, pressure, pumping, mixing, heat transfer, and compact
two-phase/packed-bed proxies.

| Capability | Current implementation |
| --- | --- |
| Dimensionless groups | Reynolds, Prandtl, Peclet, and internal-flow Nusselt estimates |
| Flow regime | laminar, transitional, and turbulent classification |
| Friction factor | laminar `64/Re`, Haaland turbulent approximation, smooth transition blend |
| Pipe pressure drop | Darcy-Weisbach friction, fittings loss, static head, and pump work |
| Mixing | impeller power and optional volumetric power density |
| Heat transfer | film/wall/fouling resistance to `U`, jacket heat duty, signed heat energy |
| Heat exchanger | counterflow effectiveness-NTU model with stream energy balance |
| Packed bed | Ergun pressure-drop calculation with viscous and inertial terms |
| Two-phase proxy | homogeneous pressure-drop model using quality-weighted mixture properties |

All transport results are JSON-friendly dataclasses. They expose the engineering
quantity, the units implied by the field names, the regime or model branch used,
and a metadata block with the equipment inputs. This keeps later world-law
modules honest: a task can penalize high pump work, high pressure drop, poor heat
removal, high mixing energy, or risky gas-liquid operation using the same
calculation surface that students and agents can inspect.

The module intentionally uses compact correlations instead of importing a heavy
process-simulation backend. The reference libraries informed the API shape:
`fluids` separates dimensionless groups, friction factors, and pressure-drop
wrappers; IDAES exposes equipment contracts in terms of `U`, `A`, `Q`, `NTU`,
and effectiveness. ChemWorld localizes those ideas into deterministic functions
that are small enough for benchmark replay and robust enough for task design.

## Boundaries

This layer is now a real local property-correlation, reaction-network, reactor,
cubic-EOS, compact phase-equilibrium, reaction-equilibrium/electrolyte,
downstream unit-operation, and transport/heat-transfer core, but it is not yet a
complete process simulator. It does not perform rigorous multiphase stability
analysis, database-grade flash calculations, global Gibbs minimization,
automatic reaction mechanism generation, CFD, detailed two-fluid hydrodynamics,
or exchanger network synthesis. Those will be built on top of these specs in
later TODO milestones.

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
- an equilibrium constant, reaction extent, pH calculation, solubility product,
  ion charge, or ionic strength input is nonphysical.
- a transport dimension, density, viscosity, heat-transfer coefficient, or
  equipment efficiency is nonphysical.

This gives later transition kernels a cleaner contract: invalid chemistry
metadata should fail before simulation begins.
