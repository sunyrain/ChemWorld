# ChemWorld Professional-Grade Implementation TODO

This is the long-term TODO after the first foundation/lite batch in `TODO.md`.
It is intentionally stricter. The goal is not to fill the benchmark with
proxies, and not to clone old professional libraries. The goal is to read the
professional ecosystem, identify what is still sound or outdated, then implement
ChemWorld's own compact, modern, tested, and benchmark-oriented physical
chemistry core.

## Development Contract

- Owner marker: `whilesunny`.
- Before coding a professional module, claim the task in this file and push the
  claim.
- Read at least one relevant local reference repository before implementing:
  `reference_repos/cantera`, `reference_repos/coolprop`,
  `reference_repos/thermo`, `reference_repos/chemicals`,
  `reference_repos/fluids`, `reference_repos/phasepy`,
  `reference_repos/idaes-pse`, `reference_repos/reaktoro`,
  `reference_repos/pycalphad`, `reference_repos/teqp`,
  `reference_repos/thermopack`, or `reference_repos/rmg-py`.
- Do not copy source code from reference repositories.
- Do not mark a task done because a proxy exists.
- A module is complete only when implementation, model card, validity limits,
  failure modes, tests, and at least one controlled validation path exist.
- If a reference library appears outdated, document the limitation and implement
  the ChemWorld version with a clearer API, modern typing, explicit units, and
  benchmark-focused scope.

## Status Vocabulary

| Status | Meaning |
| --- | --- |
| Planned | Not started |
| Claimed | Owner has reserved the task and pushed the claim |
| Reading | Reference repos and primary equations are being audited |
| Implementing | ChemWorld-local implementation is under development |
| Validation | Numerical/reference comparisons are being written |
| Review | Pushed and waiting for another human/agent review |
| Done | Professional acceptance criteria are satisfied |
| Blocked | Explicit blocker with handoff note |

## Professional Acceptance Criteria

Every professional module must ship:

- `Spec` dataclasses with explicit units and JSON serialization;
- deterministic behavior under controlled seeds where relevant;
- a model card documenting equations, assumptions, limits, and intended use;
- at least one reference-reading note naming the local reference files or API
  surfaces inspected;
- fast local unit tests for invariants and edge cases;
- optional reference-backend tests where a package can run locally;
- task integration tests showing the model changes the benchmark behavior;
- no hidden clipping of invalid physical states unless documented as a solver
  recovery policy;
- failure modes that produce explicit validation errors rather than silent
  proxy behavior.

## Active Work Board

| Item | Owner | Status | Reference Targets | Code Areas | Next Step | Last Push |
| --- | --- | --- | --- | --- | --- | --- |
| Professional TODO bootstrap | whilesunny | Done | all reference repos | `TODO_PROFESSIONAL.md`, `docs/professional_todo.md`, `docs/physchem_maturity_audit.md` | claim the first professional implementation item before coding | this commit |
| PRO-P0 maturity metadata and model-card templates | whilesunny | Done | IDAES, thermo, Cantera, Gymnasium-style metadata | `src/chemworld/physchem/maturity.py`, `src/chemworld/tasks.py`, `docs/physchem_maturity_audit.md`, tests | next: claim PRO-P12A or PRO-P2A for reference-validated numerical hardening | this commit |
| PRO-P12A fluids friction factor and pressure-drop validation | whilesunny | Done | `fluids.friction`, `fluids.core`, Haaland and Darcy-Weisbach references | `src/chemworld/physchem/transport.py`, `src/chemworld/physchem/reference_validation.py`, `tests/reference/test_optional_reference_backends.py`, docs | next: extend pressure-drop validation to heat-transfer correlations or claim PRO-P2A | this commit |
| PRO-P2A curated vapor-pressure and enthalpy property cases | whilesunny | Done | `chemicals.vapor_pressure`, `chemicals.heat_capacity`, `chemicals.dippr`, `thermo.heat_capacity` | `src/chemworld/physchem/curated_properties.py`, `src/chemworld/physchem/properties.py`, `tests/reference/test_optional_reference_backends.py`, docs | next: extend the curated registry toward critical properties, liquid Cp, latent heat, and CoolProp checks | this commit |
| PRO-P4A Wilson and full binary NRTL activity models | whilesunny | Claimed | `thermo.activity`, `thermo.nrtl`, `phasepy`, `thermopack` | `src/chemworld/physchem/equilibrium.py`, reference tests, model cards, docs | read local activity-model APIs, then replace NRTL-lite with explicit Wilson/NRTL parameter contracts and reference checks | pending push |

## P0: Governance And Model Maturity

- [x] Define a machine-readable maturity enum:
  - [x] `proxy`;
  - [x] `lite`;
  - [x] `reference_validated`;
  - [x] `professional_candidate`;
  - [x] `professional`.
- [x] Add model-card templates for:
  - [x] properties;
  - [x] EOS;
  - [x] phase equilibrium;
  - [x] reaction kinetics;
  - [x] reactors;
  - [x] separations;
  - [x] transport;
  - [x] spectroscopy/instruments.
- [x] Add CI checks that docs cannot call a module professional unless the
      model card and validation evidence exist.
- [x] Add a `proxy_allowed` flag only for educational or exploratory tasks.
- [x] Add task metadata showing whether each task uses proxy, lite, or
      professional kernels.

Reference-reading note for PRO-P0:

- `thermo.activity.GibbsExcess` separates model parameters from state and
  exposes JSON-friendly serialization/hash behavior.
- `thermo.property_package.PropertyPackage` exposes explicit flash tolerances
  and fixed validity bounds.
- Cantera YAML files expose description, generator, input files, unit systems,
  phase models, species thermo models, and transport model declarations.
- IDAES component/property blocks use explicit configuration declarations and
  property-package metadata.

## P1: Component Data, Units, And Property Registry

Reference targets: `chemicals`, `thermo`, `CoolProp`.

- [ ] Build a curated component registry with provenance:
  - [ ] identifiers and aliases;
  - [ ] formula and charge;
  - [ ] molecular weight;
  - [ ] critical properties;
  - [ ] acentric factor;
  - [ ] normal boiling/melting points;
  - [ ] phase-change properties;
  - [ ] safety metadata.
- [ ] Add strict unit dimensions for every property input/output.
- [ ] Add uncertainty/provenance fields to property records.
- [ ] Add conflict-resolution policy when multiple data sources disagree.
- [x] Add reference comparisons for selected public compounds:
  - [x] water;
  - [x] ethanol;
  - [x] acetone;
  - [x] toluene;
  - [x] methane;
  - [x] carbon dioxide.

Acceptance:

- [ ] Component records round-trip through JSON.
- [ ] Conflicting aliases fail unless explicitly resolved.
- [ ] Reference values are compared with documented tolerances.

## P2: Professional Property Correlations

Reference targets: `chemicals`, `thermo`, `CoolProp`.

- [ ] Vapor pressure:
  - [ ] Antoine with validity domains;
  - [x] Wagner/DIPPR-style form;
  - [ ] sublimation pressure where needed;
  - [ ] derivative with respect to temperature.
- [ ] Heat capacity and enthalpy:
  - [x] ideal-gas Cp;
  - [ ] liquid Cp;
  - [ ] solid Cp where needed;
  - [x] enthalpy integrals with reference states;
  - [ ] latent heat correlations.
- [ ] Density/volume:
  - [ ] liquid molar volume;
  - [ ] Rackett-style correlation;
  - [ ] ideal gas and virial hooks;
  - [ ] mixture density with validity limits.
- [ ] Transport properties:
  - [ ] gas viscosity;
  - [ ] liquid viscosity;
  - [ ] thermal conductivity;
  - [ ] diffusivity proxy with validity warning.
- [ ] Safety properties:
  - [ ] flash-point proxy;
  - [ ] vapor hazard;
  - [ ] thermal runaway flags.

Acceptance:

- [x] Correlations expose validity-range warnings and hard-fail mode for the
      curated DIPPR101/Poling slice.
- [x] Public reference cases compare against `chemicals` for the curated
      DIPPR101 vapor-pressure and Poling ideal-gas Cp/enthalpy slice.
- [ ] Property package can be used by reactor energy balances without unit
      ambiguity.

## P3: EOS And Residual Thermodynamics

Reference targets: `CoolProp`, `thermo`, `teqp`, `thermopack`.

- [ ] Refactor cubic EOS into a professional API:
  - [ ] pure-parameter generation;
  - [ ] binary interaction matrix;
  - [ ] volume translation hook;
  - [ ] liquid/vapor/stable root policy;
  - [ ] fugacity coefficients;
  - [ ] residual enthalpy;
  - [ ] residual entropy;
  - [ ] departure functions.
- [ ] Add phase-envelope utilities:
  - [ ] saturation solve for pure fluids;
  - [ ] bubble/dew solve for mixtures;
  - [ ] critical-region warning.
- [ ] Add derivative hooks needed for flash and optimization.

Acceptance:

- [ ] PR/SRK limiting cases match ideal gas at low pressure.
- [ ] Selected methane/ethane/CO2 cases compare against reference backends.
- [ ] Root selection is explicit and reproducible.

## P4: Activity Models And Phase Equilibrium

Reference targets: `thermo`, `phasepy`, `thermopack`.

- [ ] Activity models:
  - [ ] Margules formal model card;
  - [ ] Wilson;
  - [ ] NRTL full binary/ternary form;
  - [ ] UNIQUAC;
  - [ ] UNIFAC-style extension only after data governance is solved.
- [ ] Phase stability:
  - [ ] tangent-plane-distance heuristic;
  - [ ] phase-split initialization policy;
  - [ ] azeotrope detection hooks.
- [ ] Flash solvers:
  - [ ] isothermal-isobaric VLE;
  - [ ] bubble point;
  - [ ] dew point;
  - [ ] LLE;
  - [ ] VLLE candidate workflow;
  - [ ] adiabatic flash later.

Acceptance:

- [ ] Ideal VLE stays reference validated against `thermo`.
- [ ] At least one nonideal binary case compares against `thermo` or `phasepy`.
- [ ] LLE solver conserves mass and reports stability/initialization failures.

## P5: Reaction Thermochemistry And Kinetics

Reference targets: `Cantera`, `RMG-Py`, `thermo`.

- [ ] Species thermochemistry:
  - [ ] NASA-polynomial parser or compact equivalent;
  - [ ] Cp/H/S evaluation;
  - [ ] reaction enthalpy from species data;
  - [ ] equilibrium constants from Gibbs energy.
- [ ] Rate laws:
  - [ ] elementary mass-action;
  - [ ] reversible rates obeying detailed balance;
  - [ ] modified Arrhenius;
  - [ ] falloff/Troe-style placeholder with validation target;
  - [ ] pressure-dependent hooks;
  - [ ] heterogeneous catalytic rate template;
  - [ ] Butler-Volmer electrochemical rate.
- [ ] Sensitivity hooks:
  - [ ] finite-difference sensitivities;
  - [ ] local parameter perturbation reports.

Acceptance:

- [ ] Simple irreversible and reversible ODE cases compare against Cantera.
- [ ] Energy balance uses reaction enthalpy from thermochemistry where
      available.
- [ ] Invalid or unbalanced reactions fail before simulation.

## P6: Reactor And Process Dynamics

Reference targets: `Cantera`, `IDAES`.

- [ ] Batch reactor:
  - [ ] constant-volume and constant-pressure modes;
  - [ ] heat-transfer wall/jacket;
  - [ ] pressure model;
  - [ ] event handling.
- [ ] Semi-batch reactor:
  - [ ] time-dependent feed;
  - [ ] addition-controlled selectivity;
  - [ ] overflow/pressure safety.
- [ ] CSTR:
  - [ ] dynamic startup;
  - [ ] steady-state solve;
  - [ ] multiple steady-state example;
  - [ ] stability classification.
- [ ] PFR:
  - [ ] axial integration;
  - [ ] heat-transfer profile;
  - [ ] pressure drop;
  - [ ] hotspot detection.
- [ ] Reactor networks:
  - [ ] reservoir/feed objects;
  - [ ] valves/flow devices;
  - [ ] serial/parallel reactors.

Acceptance:

- [ ] Selected reactor cases compare against Cantera or a documented analytical
      case.
- [ ] Campaign tasks can select professional reactor kernels.

## P7: Separation Unit Models

Reference targets: `IDAES`, `thermo`, `phasepy`, `fluids`.

- [ ] Liquid-liquid extraction:
  - [ ] stage equilibrium from activity/partition model;
  - [ ] multistage counter-current option;
  - [ ] solvent selection hooks;
  - [ ] entrainment and loss model.
- [ ] Distillation:
  - [ ] MESH-lite stage model;
  - [ ] reflux and boilup;
  - [ ] shortcut Fenske-Underwood-Gilliland option;
  - [ ] VLE-coupled task.
- [ ] Evaporation/flash:
  - [ ] VLE-coupled vapor removal;
  - [ ] heat duty from enthalpy;
  - [ ] solvent-loss risk.
- [ ] Crystallization:
  - [ ] solubility curve;
  - [ ] supersaturation;
  - [ ] nucleation/growth proxy with model card;
  - [ ] impurity occlusion.
- [ ] Filtration/drying:
  - [ ] cake resistance;
  - [ ] washing efficiency;
  - [ ] drying curve;
  - [ ] thermal degradation coupling.

Acceptance:

- [ ] No separation task uses an unlabeled proxy in the benchmark default.
- [ ] Purity/recovery/cost tradeoffs are produced by declared physical models.

## P8: Transport, Equipment, And Safety

Reference targets: `fluids`, `IDAES`, `CoolProp`.

- [ ] Pressure drop:
  - [ ] pipe friction;
  - [ ] fittings/minor losses;
  - [ ] packed bed;
  - [ ] two-phase warnings.
- [ ] Heat transfer:
  - [ ] jacketed reactor;
  - [ ] heat exchanger;
  - [ ] boiling/condensation warning models;
  - [ ] fouling factor.
- [ ] Mixing:
  - [ ] impeller power;
  - [ ] mixing time;
  - [ ] mass-transfer coefficient proxy with validity limits.
- [ ] Safety:
  - [ ] pressure relief proxy;
  - [ ] runaway index;
  - [ ] flammability/volatility flags.

Acceptance:

- [ ] Selected dimensionless and equipment calculations compare against
      `fluids`.
- [ ] Safety cost in tasks is traceable to declared physical terms.

## P9: Equilibrium Chemistry And Electrochemistry

Reference targets: `Reaktoro`, `Cantera`, `pycalphad`.

- [ ] Gibbs minimization toy solver:
  - [ ] element constraints;
  - [ ] charge constraints;
  - [ ] phase restrictions;
  - [ ] nonnegative species.
- [ ] Aqueous chemistry:
  - [ ] acid/base;
  - [ ] precipitation/dissolution;
  - [ ] ionic strength/activity corrections;
  - [ ] pH measurement model.
- [ ] Solid-phase equilibrium:
  - [ ] small CALPHAD-inspired Gibbs model;
  - [ ] phase-fraction solve;
  - [ ] phase-boundary task later.
- [ ] Electrochemistry:
  - [ ] Nernst potential;
  - [ ] Butler-Volmer kinetics;
  - [ ] Faradaic efficiency;
  - [ ] energy accounting.

Acceptance:

- [ ] At least one aqueous equilibrium case compares against Reaktoro or a
      documented analytical case.
- [ ] Electrochemical tasks use charge and energy accounting, not only labels.

## P10: Instruments And Spectroscopy

Reference targets: public instrument equations and datasets, not primarily the
thermodynamic libraries.

- [ ] Chromatography:
  - [ ] HPLC retention-time model;
  - [ ] GC volatility/retention model;
  - [ ] peak broadening and overlap;
  - [ ] calibration uncertainty.
- [ ] Spectroscopy:
  - [ ] UV-vis Beer-Lambert model;
  - [ ] IR functional-group bands;
  - [ ] NMR shift proxy with coupling metadata;
  - [ ] optional MS fragment proxy.
- [ ] Instrument operations:
  - [ ] destructive sample accounting;
  - [ ] calibration runs;
  - [ ] replicate strategy;
  - [ ] detection-limit behavior.

Acceptance:

- [ ] Instrument signals are generated from species state, not score fields.
- [ ] Each instrument has a model card and at least one public sanity example.

## P11: Benchmark Task Integration

Reference targets: DiscoveryWorld-style scientific task design, Gymnasium,
Minari, Safety-Gymnasium.

- [ ] Each task declares kernel maturity:
  - [ ] proxy allowed;
  - [ ] lite;
  - [ ] reference validated;
  - [ ] professional.
- [ ] Add professional task families:
  - [ ] reference-validated VLE flash;
  - [ ] LLE solvent selection;
  - [ ] CSTR multiplicity;
  - [ ] PFR hotspot;
  - [ ] reaction calorimetry;
  - [ ] electrochemical selectivity;
  - [ ] crystallization purity/recovery.
- [ ] Add dataset exports with maturity metadata.
- [ ] Add leaderboard views by physics maturity level.

Acceptance:

- [ ] A benchmark result cannot silently mix proxy and professional kernels.
- [ ] Submission summaries report the physics maturity of every task.

## P12: Reference Validation Matrix

Reference targets: all local reference repositories.

- [x] `chemicals`:
  - [x] ideal gas molar volume;
  - [x] Rachford-Rice flash;
  - [x] vapor pressure points;
  - [x] enthalpy/heat-capacity points.
- [ ] `fluids`:
  - [x] Reynolds number;
  - [x] Prandtl number;
  - [x] friction factor;
  - [x] pressure drop;
  - [ ] heat-transfer correlations.

Reference-reading note for PRO-P12A:

- `fluids.friction.friction_laminar` documents the standard Darcy `64/Re`
  branch and its normal laminar range.
- `fluids.friction.Haaland` exposes the explicit turbulent rough-pipe
  correlation and its nominal Reynolds/roughness validity range.
- `fluids.friction.friction_factor` uses a method-dispatch API with a default
  high-accuracy turbulent solver and laminar override below transition.
- `fluids.friction.one_phase_dP` wraps Reynolds number, friction-factor
  selection, and Darcy-Weisbach pressure drop for single-phase pipe flow.
- `fluids.two_phase.two_phase_dP` is a multi-correlation dispatcher; ChemWorld's
  homogeneous two-phase pressure-drop function remains a lite/proxy model and is
  not claimed as reference-validated by this task.

Reference-reading note for PRO-P2A:

- `chemicals.vapor_pressure.Psat_data_Perrys2_8` exposes Perry/DIPPR101
  vapor-pressure coefficients with per-compound temperature ranges.
- `chemicals.dippr.EQ101` evaluates the same vapor-pressure equation as
  `exp(A + B/T + C ln(T) + D T^E)`.
- `chemicals.heat_capacity.Cp_data_Poling` stores Poling ideal-gas Cp
  polynomial coefficients in dimensionless gas-constant-scaled form.
- `chemicals.dippr.EQ100` evaluates the Cp polynomial and its analytical
  integral; ChemWorld uses the same polynomial form after scaling coefficients
  by `R` into J/(mol*K).
- `thermo.heat_capacity.HeatCapacityGas` registers the Poling polynomial as a
  DIPPR100 model with `R`-scaled coefficients, confirming the unit conversion
  used locally.
- `thermo.vapor_pressure.VaporPressure` informed the separation between a
  component-local method registry, validity ranges, and method selection. The
  current ChemWorld slice remains curated rather than a full property database.
- [ ] `thermo`:
  - [x] ideal Raoult VLE bubble/dew/TP flash;
  - [ ] nonideal activity-coefficient case;
  - [ ] cubic EOS mixture case;
  - [ ] property-package enthalpy case.
- [ ] `CoolProp`:
  - [ ] pure-fluid saturation;
  - [ ] enthalpy/density point;
  - [ ] mixture warning policy.
- [ ] `Cantera`:
  - [ ] simple irreversible ODE;
  - [ ] reversible equilibrium-linked ODE;
  - [ ] batch reactor energy case.
- [ ] `phasepy`:
  - [ ] binary VLE;
  - [ ] binary LLE;
  - [ ] phase stability case.
- [ ] `IDAES`:
  - [ ] unit model interface reading note;
  - [ ] material/energy port contract comparison.
- [ ] `Reaktoro`:
  - [ ] acid/base or precipitation case;
  - [ ] Gibbs minimization toy case.
- [ ] `pycalphad`:
  - [ ] binary solid-phase toy case.
- [ ] `teqp` / `thermopack`:
  - [ ] EOS architecture reading note;
  - [ ] selected EOS comparison if dependencies run locally.
- [ ] `RMG-Py`:
  - [ ] mechanism schema reading note;
  - [ ] reaction-family design note.

Acceptance:

- [ ] Optional validation tests skip cleanly without external packages.
- [ ] Running validation locally produces JSON-friendly comparison summaries.
- [ ] Model-limit divergences are documented rather than hidden.

## First Professional Implementation Queue

1. `PRO-P0`: Add maturity metadata and model-card template to code/docs.
2. `PRO-P12A`: Expand reference validation for `fluids` friction factor and
   pressure drop. Done.
3. `PRO-P2A`: Replace placeholder vapor-pressure/enthalpy examples with
   curated reference-checked compounds. Done.
4. `PRO-P4A`: Implement Wilson and full binary NRTL with reference comparisons.
   Claimed by whilesunny.
5. `PRO-P5A`: Add Cantera-comparable irreversible and reversible reaction ODE
   cases.
6. `PRO-P6A`: Add CSTR multiple-steady-state professional example.
7. `PRO-P7A`: Replace simple distillation proxy with VLE-coupled shortcut
   distillation.
8. `PRO-P10A`: Add Beer-Lambert UV-vis model card and calibration validation.

## Explicit Non-Goals

- Do not vendor external library code.
- Do not claim real reaction prediction without data and validation.
- Do not hide proxy kernels behind professional names.
- Do not require heavy compiled packages for the default educational install.
- Do not use large third-party data tables without license and provenance
  review.
