# ChemWorld PhysChem Core TODO

This roadmap defines how ChemWorld will independently implement a compact,
auditable physical-chemistry and chemical-engineering core. External open-source
projects are used as a feature map and validation inspiration only. We do not
copy their source code into ChemWorld.

## Two-Person Active Work Board

`TODO.md` is the shared source of truth for current work. Before coding, pull
`origin/main`, claim the task here with a real owner, commit that ownership
change, and push it. If the remote `TODO.md` changes while you are working,
pull immediately and update your plan before continuing. When one task is
finished, update its status and push immediately.

| Item | Owner | Status | Files / Area | Next Step | Last Push |
| --- | --- | --- | --- | --- | --- |
| Docs cleanup and two-person rules | Codex | Done | `TODO.md`, `docs/`, `mkdocs.yml` | use this board for the next active task | this commit |
| P1 physchem component/spec foundation | whilesunny | Done | `src/chemworld/physchem/`, `tests/`, `docs/physchem_core_design.md` | next: start P2 property-correlation core on top of these specs | this commit |
| P2 full property-correlation core | whilesunny | Done | `src/chemworld/physchem/`, `tests/`, `docs/physchem_core_design.md` | next: connect the property package to energy balance and start P3 reaction-network specs | this commit |
| P3 general reaction-network engine | whilesunny | Done | `src/chemworld/physchem/`, `tests/`, `docs/physchem_core_design.md`, `configs/mechanisms/` | next: connect mechanism-backed networks to batch/semi-batch/CSTR/PFR reactor models in P4 | this commit |
| P4 reactor model core | whilesunny | Done | `src/chemworld/physchem/reactors.py`, `tests/`, `docs/physchem_core_design.md` | next: replace selected task/world transition paths with mechanism-backed reactor kernels, then start P5 EOS | this commit |
| P5 equation-of-state core | whilesunny | Done | `src/chemworld/physchem/eos.py`, `tests/`, `docs/physchem_core_design.md` | next: build activity models and VLE/LLE flash on top of EOS and property packages | this commit |
| P6 phase-equilibrium core | whilesunny | Done | `src/chemworld/physchem/equilibrium.py`, `tests/`, `docs/physchem_core_design.md` | next: replace extraction and evaporation task proxies with phase-equilibrium kernels, then start P7 separations | this commit |
| P7 separation and unit operations | whilesunny | Done | `src/chemworld/physchem/separations.py`, `tests/`, `docs/physchem_core_design.md` | next: implement fluid mechanics and heat-transfer utilities in P8, then wire separations into world tasks | this commit |
| P8 fluid mechanics and heat transfer | whilesunny | Done | `src/chemworld/physchem/transport.py`, `tests/test_transport.py`, `docs/physchem_core_design.md` | next: implement equilibrium chemistry in P9, then connect transport signals into world tasks and scoring | this commit |

Status values:

- `Planned`: available and not started.
- `Active`: one owner is working on it now.
- `Blocked`: owner cannot proceed; handoff note required.
- `Review`: pushed and waiting for the other person to inspect.
- `Done`: complete and pushed.

Ownership rules:

- Every `Active` task must have exactly one owner.
- Do not start another person's `Active` task unless they write a handoff note.
- Claim a task by editing this table and pushing before implementation.
- Finish a task by updating this table and pushing immediately.
- Keep completed units small; avoid batching unrelated work into one delayed
  push.

## Ground Rules

- Implement ChemWorld's own code, data contracts, tests, and documentation.
- Use original equations, textbooks, papers, and public reference data when
  implementing correlations or algorithms.
- Do not vendor large external projects into the benchmark core.
- Keep heavy ecosystem integrations as optional adapters, not required
  dependencies.
- Every implemented feature must expose:
  - a JSON-friendly spec;
  - unit metadata;
  - deterministic seed behavior where applicable;
  - reference tests;
  - failure modes and validity ranges;
  - documentation explaining assumptions.

## External Project Feature Map

The projects below are not implementation dependencies for the ChemWorld core.
They define the professional capability surface we want to cover gradually.

### Cantera

Primary domain: chemical kinetics, thermodynamics, transport, and reactor
networks.

Major capabilities to learn from:

- species and phase definitions;
- YAML/CTI-like mechanism loading;
- ideal gas, condensed phase, surface, and interface phase models;
- NASA polynomial thermochemistry;
- standard-state and mixture thermodynamics;
- elementary, reversible, falloff, pressure-dependent, and surface reactions;
- Arrhenius and modified Arrhenius rate laws;
- transport property models;
- chemical equilibrium calculations;
- zero-dimensional reactor networks;
- constant-volume and constant-pressure reactors;
- walls, reservoirs, flow devices, and reactor coupling;
- sensitivity analysis;
- one-dimensional flame and reacting-flow solvers;
- Python API around compiled numerical kernels.

ChemWorld independent implementation target:

- implement a compact reaction-network engine, not a detailed combustion
  platform;
- support YAML/JSON mechanism specs;
- support general stoichiometric matrices and multiple rate laws;
- keep Cantera as an optional validation/backend adapter later.

### CoolProp

Primary domain: high-accuracy thermophysical properties.

Major capabilities to learn from:

- pure-fluid and pseudo-pure-fluid properties;
- mixture properties;
- Helmholtz-energy equations of state;
- cubic equations of state;
- IF97 water/steam properties;
- humid-air properties;
- incompressible fluids and brines;
- phase identification;
- saturation properties;
- phase envelopes;
- partial derivatives and transport properties;
- tabular interpolation;
- wrappers for many languages.

ChemWorld independent implementation target:

- implement only a compact property backend:
  - vapor pressure;
  - liquid density;
  - heat capacity;
  - enthalpy;
  - latent heat;
  - viscosity proxy;
  - simple mixture rules;
  - Peng-Robinson and SRK;
  - flash calculations.
- keep CoolProp as optional reference validation, not core dependency.

### thermo

Primary domain: chemical-engineering thermodynamics in Python.

Major capabilities to learn from:

- pure-component constants;
- chemical object model;
- mixture object model;
- heat capacity correlations;
- vapor pressure correlations;
- volume and density correlations;
- viscosity and thermal-conductivity correlations;
- surface-tension correlations;
- enthalpy and entropy calculations;
- equations of state;
- cubic equation-of-state mixtures;
- fugacity coefficients;
- activity-coefficient models;
- flash calculations;
- vapor-liquid equilibrium;
- liquid-liquid equilibrium;
- property packages for process calculations.

ChemWorld independent implementation target:

- implement a smaller `physchem.properties` and `physchem.equilibrium`
  package;
- define a minimal component database and correlation registry;
- implement only benchmark-needed equations first.

### chemicals

Primary domain: chemical property correlations and data utilities.

Major capabilities to learn from:

- critical properties;
- acentric factor and corresponding-states utilities;
- vapor pressure;
- heat capacity;
- phase-change enthalpy;
- liquid and gas molar volume;
- virial volume;
- surface tension;
- solubility and Henry-law constants;
- combustion and reaction property helpers;
- safety and exposure data utilities;
- environmental property helpers;
- periodic-table and formula utilities;
- data lookup and correlation selection.

ChemWorld independent implementation target:

- implement a compact correlation library with explicit validity ranges;
- provide only the correlations used by current and near-term tasks;
- avoid embedding large data tables until provenance and licensing are clear.

### fluids

Primary domain: fluid mechanics and equipment calculations.

Major capabilities to learn from:

- friction factor correlations;
- pipe pressure drop;
- fittings and minor losses;
- pumps and compressors;
- control valves;
- two-phase pressure drop;
- open-channel flow;
- packed-bed pressure drop;
- particle settling;
- mixing and agitation correlations;
- separator and tank utilities;
- dimensionless numbers;
- flow-meter correlations;
- safety valve and relief calculations.

ChemWorld independent implementation target:

- implement only the process-interaction pieces needed for virtual labs:
  - Reynolds number;
  - friction factor;
  - pipe/tube pressure drop;
  - simple pump work;
  - mixing intensity;
  - packed-bed pressure drop later;
  - two-phase pressure drop later.

### phasepy

Primary domain: phase-equilibrium calculations.

Major capabilities to learn from:

- cubic equations of state;
- activity-coefficient models;
- vapor-liquid equilibrium;
- liquid-liquid equilibrium;
- vapor-liquid-liquid equilibrium;
- bubble and dew point calculations;
- flash calculations;
- phase stability;
- parameter fitting/regression;
- interfacial-tension and square-gradient-style calculations.

ChemWorld independent implementation target:

- replace the current partition proxy with:
  - ideal partition model;
  - NRTL/Wilson/UNIQUAC-lite;
  - binary and ternary LLE;
  - VLE bubble/dew/flash;
  - phase-stability checks.

### IDAES

Primary domain: process systems engineering, optimization, and flowsheets.

Major capabilities to learn from:

- Pyomo-based process models;
- property packages;
- unit model library;
- steady-state flowsheets;
- dynamic flowsheets;
- initialization workflows;
- algebraic and differential-algebraic optimization;
- parameter estimation;
- costing models;
- uncertainty and sensitivity workflows;
- power, carbon-capture, and chemical-process examples;
- solver integration and model diagnostics.

ChemWorld independent implementation target:

- do not reproduce IDAES;
- implement lightweight process-unit contracts:
  - unit state;
  - inlet/outlet ports;
  - material balance;
  - energy balance;
  - cost/risk accounting;
  - simplified optimization hooks.
- keep an IDAES adapter as a future professional backend.

### Reaktoro

Primary domain: chemical equilibrium, kinetics, and reactive transport.

Major capabilities to learn from:

- Gibbs-energy-minimization equilibrium;
- thermodynamic databases;
- aqueous, gaseous, liquid, mineral, and surface phases;
- activity models;
- equilibrium specs and constraints;
- chemical kinetics;
- reactive transport;
- inverse equilibrium problems;
- pH, charge, alkalinity, and geochemical constraints;
- precipitation/dissolution systems.

ChemWorld independent implementation target:

- implement a small equilibrium module:
  - mass-action equilibrium;
  - reaction extent solving;
  - acid/base toy equilibria later;
  - precipitation/dissolution proxy later.
- keep Reaktoro as optional validation for equilibrium-heavy tasks.

### pycalphad

Primary domain: CALPHAD thermodynamics and phase diagrams.

Major capabilities to learn from:

- TDB database parsing;
- Gibbs-energy model construction;
- multicomponent, multiphase equilibrium;
- phase diagram calculation;
- property calculation;
- equilibrium result data structures;
- parameter selection and fitting workflows;
- plotting and mapping of phase boundaries.

ChemWorld independent implementation target:

- do not implement full CALPHAD in the core;
- implement a small `solid_phase_equilibrium` abstraction;
- use pycalphad-style ideas only for future materials tasks.

### teqp

Primary domain: modern equations of state and thermodynamic derivatives.

Major capabilities to learn from:

- Helmholtz-energy equation-of-state formulation;
- multiparameter EOS models;
- cubic EOS support;
- mixture models;
- thermodynamic derivatives;
- critical point and phase-envelope tracing;
- fast numerical kernels;
- JSON-style model specifications.

ChemWorld independent implementation target:

- implement JSON-friendly EOS specs;
- implement Peng-Robinson and SRK first;
- add Helmholtz-style abstractions later if justified.

### thermopack

Primary domain: equation-of-state and phase-equilibrium package.

Major capabilities to learn from:

- cubic EOS;
- CPA EOS;
- SAFT-family EOS;
- association models;
- multiphase flash;
- phase envelopes;
- stability analysis;
- binary interaction parameters;
- hydrate and advanced phase behavior in specialized cases.

ChemWorld independent implementation target:

- focus on cubic EOS and simple activity models first;
- leave SAFT/CPA/hydrate behavior for long-term optional tasks.

### RMG-Py

Primary domain: reaction mechanism generation.

Major capabilities to learn from:

- species graph representation;
- thermochemistry estimation;
- kinetics family databases;
- reaction template matching;
- automatic mechanism generation;
- pressure-dependent reaction networks;
- reactor simulation;
- sensitivity and model analysis;
- solvation and liquid-phase extensions;
- mechanism reduction workflows.

ChemWorld independent implementation target:

- do not implement automatic mechanism generation initially;
- implement explicit mechanism loading and validation first;
- later add a small reaction-template toy generator for benchmark tasks.

### Optional Future: Heat-Transfer Utilities

Primary domain: heat-transfer correlations and equipment calculations.

Major capabilities to implement independently when needed:

- conduction through walls;
- convection coefficients;
- Nusselt/Reynolds/Prandtl correlations;
- jacketed reactor heat transfer;
- heat exchanger effectiveness;
- boiling/condensation proxies;
- thermal runaway indicators.

## ChemWorld Independent Implementation Plan

### P0: Governance, Scope, and Audit

- [ ] Create `docs/third_party_feature_map.md` from this TODO.
- [ ] Add a no-source-copy policy to contributor docs.
- [ ] Add a `docs/physchem_core_design.md` architecture page.
- [ ] Add `src/chemworld/physchem/README.md` explaining module boundaries.
- [ ] Add tests confirming the core package imports without optional external
      scientific backends.
- [ ] Add optional extras only after adapters exist:
  - [ ] `physchem-ref`
  - [ ] `cantera`
  - [ ] `coolprop`
  - [ ] `idaes`
  - [ ] `equilibrium`

### P1: Data Structures and Units

- [ ] `ComponentSpec`
  - [ ] identifier;
  - [ ] formula;
  - [ ] molecular weight;
  - [ ] charge;
  - [ ] default phase;
  - [ ] safety tags;
  - [ ] allowed property correlations.
- [ ] `MixtureSpec`
  - [ ] component ids;
  - [ ] mole fractions;
  - [ ] mass fractions;
  - [ ] phase label;
  - [ ] temperature and pressure.
- [ ] `PropertyCorrelation`
  - [ ] equation id;
  - [ ] coefficients;
  - [ ] units;
  - [ ] validity range;
  - [ ] source note.
- [ ] Extend unit checks for:
  - [ ] pressure;
  - [ ] energy;
  - [ ] power;
  - [ ] molar enthalpy;
  - [ ] mass density;
  - [ ] viscosity;
  - [ ] heat-transfer coefficient.

Acceptance tests:

- [ ] Formula parser conserves elements for `C2H6O`, `H2O`, `CO2`.
- [ ] Mole fraction and mass fraction conversions are reversible.
- [ ] Invalid units fail before transition kernels run.

### P2: Property Correlation Core

- [ ] Vapor pressure:
  - [ ] Antoine;
  - [ ] Wagner-like placeholder;
  - [ ] validity warnings.
- [ ] Heat capacity:
  - [ ] polynomial Cp;
  - [ ] enthalpy integral;
  - [ ] sensible heat.
- [ ] Phase-change properties:
  - [ ] heat of vaporization;
  - [ ] heat of fusion placeholder.
- [ ] Density:
  - [ ] ideal gas density;
  - [ ] liquid density correlation;
  - [ ] mixture density rule.
- [ ] Viscosity:
  - [ ] liquid viscosity correlation;
  - [ ] gas viscosity placeholder;
  - [ ] mixture viscosity rule.
- [ ] Surface tension:
  - [ ] simple temperature-dependent proxy.
- [ ] Safety properties:
  - [ ] flammability proxy;
  - [ ] volatility risk proxy;
  - [ ] thermal hazard proxy.

Acceptance tests:

- [ ] Water vapor pressure increases monotonically with temperature.
- [ ] Cp integral has correct sign and units.
- [ ] Density and viscosity remain positive within validity ranges.

### P3: General Reaction Network Engine

- [ ] `SpeciesSpec`
  - [ ] element composition;
  - [ ] phase;
  - [ ] charge;
  - [ ] catalyst flag;
  - [ ] observable aliases.
- [ ] `ReactionSpec`
  - [ ] equation string;
  - [ ] stoichiometric coefficients;
  - [ ] reversible flag;
  - [ ] rate-law id;
  - [ ] heat of reaction;
  - [ ] equilibrium model id.
- [ ] `ReactionNetworkSpec`
  - [ ] species list;
  - [ ] reaction list;
  - [ ] stoichiometric matrix;
  - [ ] element matrix;
  - [ ] conservation checks.
- [ ] Mechanism loader:
  - [ ] JSON;
  - [ ] YAML;
  - [ ] schema validation;
  - [ ] deterministic scenario parameter perturbation.
- [ ] Rate laws:
  - [ ] mass action;
  - [ ] Arrhenius;
  - [ ] modified Arrhenius;
  - [ ] reversible Arrhenius;
  - [ ] catalytic activity multiplier;
  - [ ] catalyst deactivation;
  - [ ] Langmuir-Hinshelwood-lite;
  - [ ] Michaelis-Menten-lite;
  - [ ] electrochemical Butler-Volmer-lite later.

Acceptance tests:

- [ ] Stoichiometric matrix for arbitrary network is correct.
- [ ] Element balance catches impossible reactions.
- [ ] `A -> P -> D` reproduces current qualitative behavior.
- [ ] Network with 20 species and 30 reactions runs deterministically.

### P4: Reactor Models

- [ ] Batch reactor:
  - [ ] mole balance;
  - [ ] energy balance;
  - [ ] variable volume;
  - [ ] heat-transfer jacket.
- [ ] Semi-batch reactor:
  - [ ] feed schedule;
  - [ ] addition-limited selectivity;
  - [ ] runaway risk.
- [ ] CSTR:
  - [ ] steady-state solve;
  - [ ] dynamic startup;
  - [ ] residence time;
  - [ ] multiple steady-state example.
- [ ] PFR:
  - [ ] axial coordinate integration;
  - [ ] temperature profile;
  - [ ] pressure-drop placeholder.
- [ ] Reactive flash:
  - [ ] reaction plus phase split;
  - [ ] equilibrium-limited reaction.
- [ ] Electrochemical cell:
  - [ ] charge balance;
  - [ ] current efficiency;
  - [ ] potential-selectivity proxy.

Acceptance tests:

- [ ] Batch and CSTR agree in limiting cases where expected.
- [ ] PFR conversion increases with residence time.
- [ ] Semi-batch feed rate changes selectivity.
- [ ] Reactor state never creates negative species.

### P5: Equations of State

- [ ] Ideal gas EOS.
- [ ] Peng-Robinson EOS:
  - [ ] pure component parameters;
  - [ ] mixture rules;
  - [ ] compressibility roots;
  - [ ] fugacity coefficients.
- [ ] SRK EOS:
  - [ ] pure component parameters;
  - [ ] mixture rules;
  - [ ] fugacity coefficients.
- [ ] Phase identification by root selection.
- [ ] Residual enthalpy placeholder.
- [ ] EOS JSON spec.

Acceptance tests:

- [ ] Ideal gas limit matches `PV=nRT`.
- [ ] PR roots are real/filtered and stable.
- [ ] Fugacity coefficients remain positive.

### P6: Activity Models and Phase Equilibrium

- [ ] Ideal-solution activity model.
- [ ] Margules binary model.
- [ ] Wilson-lite.
- [ ] NRTL-lite.
- [ ] UNIQUAC-lite.
- [ ] Binary LLE solver.
- [ ] Ternary LLE placeholder.
- [ ] Bubble point.
- [ ] Dew point.
- [ ] Isothermal flash.
- [ ] Adiabatic flash later.
- [ ] Phase-stability heuristic.

Acceptance tests:

- [ ] Ideal binary flash has expected limiting behavior.
- [ ] LLE split conserves material.
- [ ] Increasing extractant volume changes recovery/purity tradeoff.
- [ ] Distillation task uses VLE rather than fixed proxy where enabled.

### P7: Separation and Unit Operations

- [ ] Liquid-liquid extraction:
  - [ ] equilibrium stage;
  - [ ] finite mixing efficiency;
  - [ ] entrainment loss;
  - [ ] solvent loss;
  - [ ] washing stages.
- [ ] Evaporation:
  - [ ] VLE-driven removal;
  - [ ] heat duty;
  - [ ] concentration risk.
- [ ] Simple distillation:
  - [ ] relative volatility;
  - [ ] reflux purity/recovery tradeoff;
  - [ ] fraction cut.
- [ ] Crystallization:
  - [ ] solubility curve;
  - [ ] supersaturation;
  - [ ] nucleation/growth proxy;
  - [ ] filtration loss.
- [ ] Filtration:
  - [ ] cake recovery;
  - [ ] impurity retention;
  - [ ] wash loss.
- [ ] Drying:
  - [ ] residual solvent;
  - [ ] thermal degradation risk.

Acceptance tests:

- [ ] Every unit operation has material balance checks.
- [ ] Purity/recovery tradeoff is nontrivial.
- [ ] Excessive purification increases cost and may reduce score.

### P8: Fluid Mechanics and Heat Transfer

- [x] Reynolds number.
- [x] Prandtl number.
- [x] Peclet number.
- [x] Internal-flow Nusselt number.
- [x] Pipe pressure drop.
- [x] Laminar/transitional/turbulent friction factor.
- [x] Pump work.
- [x] Mixing power.
- [x] Overall heat-transfer coefficient.
- [x] Jacket heat transfer.
- [x] Counterflow heat exchanger effectiveness-NTU model.
- [x] Packed-bed pressure drop.
- [x] Homogeneous two-phase pressure drop.

Acceptance tests:

- [x] Pressure drop increases with flow rate.
- [x] Heat-transfer rate increases with area and driving force.
- [x] Pump work is nonnegative.
- [x] Heat-exchanger stream energy is conserved.
- [x] Packed-bed pressure drop increases with superficial velocity.
- [x] Invalid equipment dimensions and policies fail fast.

### P9: Equilibrium Chemistry

- [ ] Mass-action equilibrium solver.
- [ ] Reaction extent formulation.
- [ ] Equilibrium constant temperature dependence.
- [ ] Acid/base toy model.
- [ ] Precipitation/dissolution proxy.
- [ ] Charge balance.
- [ ] Ionic strength placeholder.

Acceptance tests:

- [ ] Equilibrium extent respects non-negativity.
- [ ] Reversible reaction approaches expected equilibrium ratio.
- [ ] Precipitation removes dissolved species only after saturation.

### P10: Mechanism and Scenario Library

- [ ] `mechanisms/simple_batch_reaction.yaml`
- [ ] `mechanisms/parallel_series_reaction.yaml`
- [ ] `mechanisms/reversible_reaction.yaml`
- [ ] `mechanisms/catalyst_deactivation.yaml`
- [ ] `mechanisms/autocatalytic_reaction.yaml`
- [ ] `mechanisms/reaction_extraction.yaml`
- [ ] `mechanisms/reactive_distillation_lite.yaml`
- [ ] `mechanisms/cstr_multiplicity.yaml`
- [ ] `mechanisms/pfr_hotspot.yaml`
- [ ] `mechanisms/electrochemical_conversion.yaml`

Acceptance tests:

- [ ] Every mechanism loads from file.
- [ ] Every mechanism passes conservation checks.
- [ ] Every mechanism has a task card and expected qualitative behavior.

### P11: Instrument and Spectroscopy Coupling

- [ ] Map species groups to HPLC peaks.
- [ ] Map volatile species to GC peaks.
- [ ] Map chromophores/proxy species to UV-vis bands.
- [ ] Map functional-group proxies to IR bands.
- [ ] Map species proxies to NMR shifts.
- [ ] Support peak overlap.
- [ ] Support calibration curves.
- [ ] Support baseline drift.
- [ ] Support instrument detection limits.
- [ ] Support replicate measurements.

Acceptance tests:

- [ ] Larger product amount increases product peak area.
- [ ] Byproducts create visible impurity peaks.
- [ ] Low concentration can fall below detection limit.
- [ ] Processed estimates are consistent with raw signal within uncertainty.

### P12: Validation Against Reference Backends

These are optional tests that run only when external packages are installed.
They validate behavior but do not make external packages required.

- [ ] Compare selected property correlations with `chemicals/thermo`.
- [ ] Compare selected fluid calculations with `fluids`.
- [ ] Compare vapor pressure/enthalpy points with `CoolProp`.
- [ ] Compare simple reaction ODE cases with `Cantera`.
- [ ] Compare simple LLE/VLE cases with `phasepy` or `thermo`.
- [ ] Compare equilibrium toy cases with `Reaktoro`.
- [ ] Compare solid-phase toy cases with `pycalphad`.

Acceptance tests:

- [ ] Optional tests skip cleanly when reference packages are absent.
- [ ] Reference comparison tolerances are documented.
- [ ] Divergences are recorded as model-limit notes, not hidden failures.

### P13: Benchmark Tasks Enabled by the New Core

- [ ] `multi-reaction-network-optimization`
- [ ] `reaction-calorimetry-safety`
- [ ] `reversible-reaction-equilibrium`
- [ ] `solvent-screening-with-activity-coefficients`
- [ ] `lle-extraction-design`
- [ ] `vle-flash-distillation`
- [ ] `cstr-steady-state-control`
- [ ] `pfr-hotspot-avoidance`
- [ ] `reactive-separation`
- [ ] `crystallization-solubility-design`
- [ ] `electrochemical-selectivity-energy`

Each task must define:

- [ ] scenario id;
- [ ] backend id;
- [ ] allowed operations;
- [ ] allowed instruments;
- [ ] budget;
- [ ] success metrics;
- [ ] hidden parameter split;
- [ ] public/private generalization test;
- [ ] baseline agents;
- [ ] explanation prompts.

## Implementation Order

### Milestone A: General Reaction Networks

- [ ] Build `physchem.reaction_network`.
- [ ] Load mechanism YAML/JSON.
- [ ] Replace fixed five-reaction code path for a new task.
- [ ] Keep current task behavior reproducible through a mechanism file.

### Milestone B: Minimal Property Core

- [ ] Build component and correlation registry.
- [ ] Add vapor pressure, heat capacity, density, and enthalpy.
- [ ] Wire energy balance to property backend.

### Milestone C: Phase Equilibrium Core

- [ ] Add activity models.
- [ ] Add binary LLE.
- [ ] Replace current extraction partition proxy where enabled.

### Milestone D: Reactor Expansion

- [ ] Add CSTR.
- [ ] Add PFR.
- [ ] Add semi-batch.
- [ ] Add task cards and baselines.

### Milestone E: Professional Validation

- [ ] Add optional external reference tests.
- [ ] Publish model cards for every physchem module.
- [ ] Update benchmark paper artifact.

## Explicit Non-Goals

- Do not claim real reaction prediction.
- Do not clone external libraries into the repository.
- Do not make heavy C++/Fortran packages required for core ChemWorld.
- Do not add proprietary chemical databases.
- Do not add large data tables without license review.
- Do not make the educational API depend on specialist process-simulation
  solvers.

## Reference Links For Feature Mapping

- Cantera: https://github.com/Cantera/cantera
- CoolProp: https://github.com/CoolProp/CoolProp
- thermo: https://github.com/CalebBell/thermo
- chemicals: https://github.com/CalebBell/chemicals
- fluids: https://github.com/CalebBell/fluids
- phasepy: https://github.com/gustavochm/phasepy
- IDAES: https://github.com/IDAES/idaes-pse
- Reaktoro: https://github.com/reaktoro/reaktoro
- pycalphad: https://github.com/pycalphad/pycalphad
- teqp: https://github.com/usnistgov/teqp
- thermopack: https://github.com/thermotools/thermopack
- RMG-Py: https://github.com/ReactionMechanismGenerator/RMG-Py
