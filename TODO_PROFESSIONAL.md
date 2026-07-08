# ChemWorld Professional-Grade Implementation TODO

This is the long-term TODO after the first foundation/lite batch in `TODO.md`.
It is intentionally stricter. The goal is not to fill the benchmark with
proxies, and not to clone old professional libraries. The goal is to read the
professional ecosystem, identify what is still sound or outdated, then implement
ChemWorld's own compact, modern, tested, and benchmark-oriented physical
chemistry core.

## Development Contract

- Owner markers currently in use: `whilesunny`, `liyijun`.
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
- This file is the post-foundation professional TODO. Future expansions must
  split every module into concrete implementation slices with reference targets,
  equations, validation cases, and task integration criteria; never pre-fill it
  with proxy placeholders.
- After the first twelve professional implementation slices are completed, move
  active work to `TODO_PROFESSIONAL_DEEPENING.md`. That next file is for
  module-by-module professional deepening, not for adding broad proxy coverage.
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
| PRO-P4A Wilson and full binary NRTL activity models | whilesunny | Done | `thermo.activity`, `thermo.wilson`, `thermo.nrtl`, `phasepy.actmodels` | `src/chemworld/physchem/equilibrium.py`, `tests/reference/test_optional_reference_backends.py`, model cards, docs | next: add nonideal VLE task cases and Wilson/NRTL parameter-library governance | this commit |
| PRO-P5A Cantera-comparable irreversible/reversible reaction ODE cases | whilesunny | Done | `cantera` reactor examples, `cantera` reaction-rate APIs, `rmg-py` Arrhenius/reverse-rate APIs | `src/chemworld/physchem/reaction_network.py`, `tests/test_reaction_network.py`, `tests/reference/test_optional_reference_backends.py`, model cards, docs | next: add falloff, third-body, pressure-dependent, and thermochemistry-coupled reverse-rate tasks | this commit |
| PRO-P6A CSTR multiple-steady-state professional example | whilesunny | Done | `cantera` stirred-reactor examples, `idaes-pse` CSTR/control-volume models, nonlinear reactor design equations | `src/chemworld/physchem/reactors.py`, `tests/test_reactor_models.py`, model cards, docs | next: add Cantera dynamic reactor-net cross-checks and plant-scale heat-transfer variants | this commit |
| PRO-P7A VLE-coupled shortcut distillation | whilesunny | Done | `idaes-pse` distillation/flash units, `thermo` flash/property-package APIs, `phasepy` VLE examples | `src/chemworld/physchem/separations.py`, `src/chemworld/core/batch_reactor.py`, `src/chemworld/tasks.py`, `tests/test_separations.py`, model cards, docs | next: add Underwood/Gilliland sizing, pressure-profile effects, and nonideal VLE task cases | this commit |
| PRO-P10A Beer-Lambert UV-vis calibration validation | whilesunny | Done | public Beer-Lambert equations, analytical calibration examples, local spectroscopy/instrument APIs | `src/chemworld/physchem/spectroscopy.py`, `src/chemworld/world/spectra.py`, `src/chemworld/tasks.py`, `tests/test_spectroscopy.py`, model cards, docs | next: add HPLC/GC retention calibration, IR empirical anchors, and NMR coupling metadata | this commit |
| PRO-P10B Chromatography retention and peak-broadening calibration | whilesunny | Done | public chromatography equations, plate-count/resolution equations, local spectroscopy/instrument APIs | `src/chemworld/physchem/spectroscopy.py`, `src/chemworld/world/spectra.py`, `src/chemworld/tasks.py`, `tests/test_spectroscopy.py`, model cards, docs | next: add empirical retention-index examples and method-condition sensitivity | this commit |
| PRO-P3A Peng-Robinson/SRK fugacity and residual properties | whilesunny | Done | `thermo.eos`, `phasepy.cubic`, `teqp` and `thermopack` EOS architecture notes | `src/chemworld/physchem/eos.py`, `src/chemworld/physchem/reference_validation.py`, `tests/test_eos.py`, `tests/reference/test_optional_reference_backends.py`, model cards, docs | next: add volume translation, phase envelopes, and flash derivative hooks | this commit |
| PRO-P8A heat-transfer correlations and exchanger duty validation | whilesunny | Done | `fluids.core`, IDAES heat-exchanger/unit-model docs, CoolProp property workflow notes | `src/chemworld/physchem/transport.py`, `tests/test_transport.py`, `tests/reference/test_optional_reference_backends.py`, model cards, docs | next: keep boiling/condensation, shell-side corrections, fouling dynamics, and equipment safety cards on the deepening roadmap | this commit |
| PRO-P1A component registry provenance and conflict policy | liyijun | Done | `chemicals`, `thermo`, `CoolProp` identifiers and constants APIs | `src/chemworld/physchem/specs.py`, `src/chemworld/physchem/curated_properties.py`, `tests/test_physchem_core.py`, `tests/test_physchem_properties.py`, docs | next: extend curated registry toward critical constants and source-priority merges | this commit |
| PRO-P11A maturity metadata exports and submission summaries | liyijun | Done | Gymnasium, Minari, Safety-Gymnasium result-metadata patterns | `src/chemworld/data/logging.py`, `src/chemworld/data/submission.py`, `src/chemworld/eval/baseline_report.py`, `src/chemworld/eval/suite.py`, docs, tests | next: add release-check gates that consume task maturity manifests | this commit |
| PRO-P12B validation summary export and optional-backend skip audit | liyijun | Done | current optional reference-backend tests and pytest skip patterns | `src/chemworld/physchem/reference_validation.py`, `tests/test_reference_validation.py`, docs | next: attach validation reports to official release artifacts | this commit |
| PRO-P9A Gibbs minimization toy solver | whilesunny | Done | `Reaktoro` equilibrium specs, Cantera equilibrate constraints, `pycalphad` Gibbs model architecture | `src/chemworld/physchem/equilibrium_chemistry.py`, `src/chemworld/physchem/maturity.py`, `tests/test_equilibrium_chemistry.py`, `tests/test_maturity.py`, model cards, docs | next: add aqueous database-backed speciation or electrochemical thermodynamics in a separate slice | this commit |
| PRO-P9B electrochemical thermodynamics and Butler-Volmer slice | whilesunny | Done | Cantera electrochemical examples, electrochemical equilibrium docs, existing ChemWorld electrochemistry proxy | `src/chemworld/physchem/electrochemistry.py`, `src/chemworld/core/batch_reactor.py`, `src/chemworld/world/electrochemistry.py`, tests, docs | next: add ohmic drop, mass-transfer limiting current, and galvanostatic/potentiostatic controller slices in the deepening TODO | this commit |
| PRO-P5B NASA7 thermochemistry and reaction Gibbs slice | whilesunny | Done | Cantera NASA7 species thermo, RMG thermo conventions, existing ChemWorld reaction-network thermochemistry gaps | `src/chemworld/physchem/thermochemistry.py`, `tests/test_thermochemistry.py`, docs | next: reaction enthalpy still needs a reactor energy-balance slice | this commit |
| PRO-P5C thermochemistry-coupled reversible kinetics slice | whilesunny | Done | Cantera/RMG reverse-rate conventions, local NASA7 thermochemistry, existing reversible rate-law gaps | `src/chemworld/physchem/reaction_network.py`, `src/chemworld/physchem/thermochemistry.py`, `tests/test_reaction_network.py`, docs | next: connect reaction enthalpy into reactor energy balances as a separate slice, without reopening detailed-balance kinetics | this commit |
| PRO-P1B component conflict policy and source-priority audit | liyijun | Done | `chemicals`, `thermo`, `CoolProp` constants/identifier priority patterns | `src/chemworld/physchem/specs.py`, `tests/test_physchem_core.py`, docs | next: apply conflict policy to additional component constants as they are curated | this commit |
| PRO-P11B task maturity manifest export | liyijun | Done | Gymnasium/Minari metadata manifest patterns and ChemWorld task cards | `src/chemworld/tasks.py`, `tests/test_maturity.py`, `docs/tasks.md`, `docs/baseline_reference.md` | next: wire maturity manifest into dataset/export commands | this commit |
| PRO-P12C reference backend version and tolerance manifest | liyijun | Done | optional reference-backend status probes and validation tolerance records | `src/chemworld/physchem/reference_validation.py`, `tests/test_reference_validation.py`, docs | next: add per-model tolerance profile lookup in optional reference tests | this commit |

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
  - [x] identifiers and aliases;
  - [x] formula and charge;
  - [x] molecular weight;
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

- [x] Component records round-trip through JSON.
- [x] Conflicting aliases fail unless explicitly resolved.
- [x] Reference values are compared with documented tolerances.

Reference-reading note for PRO-P1A:

- Local `reference_repos/` was absent. A shallow clone of `chemicals` and
  `thermo` was attempted before coding but the network download failed with
  early EOF, so no reference source was committed.
- Upstream source reading covered the `chemicals` identifier/database pattern:
  stable CAS/name keys, multiple alias indexes, and preferred records are kept
  separate from numerical property evaluation.
- Upstream source reading covered the `thermo` simple-interface style: user
  payloads are converted to explicit SI-oriented property records rather than
  letting ambiguous names drive numerical kernels.
- ChemWorld localizes those patterns as `ComponentProvenance`,
  `ComponentUncertainty`, `component_alias_index()`, and
  `resolve_component_identifier()` without copying reference source code.
- Follow-up local audit after cloning `reference_repos/chemicals`,
  `reference_repos/thermo`, and `reference_repos/coolprop` added
  checksum-validated `ComponentSpec.cas_number`, CAS/compact-CAS identity
  resolution, and curated-property CAS promotion out of ad hoc metadata.
- PRO-P1B extends that registry layer with `ComponentConflictPolicy`,
  `ComponentFieldCandidate`, and `resolve_component_field_conflict()` so future
  multi-source data merges can warn, hard-fail, or choose a deterministic
  source-priority winner with an auditable JSON record.

## P2: Professional Property Correlations

Reference targets: `chemicals`, `thermo`, `CoolProp`.

- [x] Vapor pressure:
  - [x] Antoine with validity domains;
  - [x] Wagner/DIPPR-style form;
  - [x] sublimation pressure where caller-supplied coefficients exist;
  - [x] derivative with respect to temperature.
- [x] Heat capacity and enthalpy:
  - [x] ideal-gas Cp;
  - [x] liquid Cp;
  - [x] solid Cp where needed;
  - [x] enthalpy integrals with reference states;
  - [x] latent heat correlations.
- [x] Density/volume:
  - [x] liquid molar volume;
  - [x] Rackett-style correlation;
  - [x] ideal gas and virial hooks;
  - [x] mixture density with validity limits.
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
- [x] Property package can be used by reactor energy balances without unit
      ambiguity.

Reference-reading note for DEEP-D2A:

- `reference_repos/chemicals/chemicals/vapor_pressure.py` exposes formula-level
  Antoine and Wagner vapor-pressure functions, plus tabular method families
  such as Antoine, Wagner, Landolt, and Perry/DIPPR101. ChemWorld localizes the
  formula and validity-bound pattern without vendoring those data tables.
- `reference_repos/chemicals/chemicals/dippr.py` implements `EQ101` and its
  first derivative through the `order=1` path. ChemWorld mirrors the analytic
  derivative for the local DIPPR101 vapor-pressure equation.
- `reference_repos/thermo/thermo/vapor_pressure.py` separates method ranking,
  validity limits, method-specific calculation, and derivative access through
  `VaporPressure`. ChemWorld keeps a smaller benchmark-facing contract:
  `VaporPressureReport` returns pressure, `dP/dT`, `dlnP/dT`, validity status,
  method family, and reference-reading provenance.
- This closes a compact formula-family/reporting slice. It does not add broad
  vapor-pressure data coverage, EOS-based saturation solves, IAPWS special
  water handling, or CoolProp-level critical-region behavior.

Reference-reading note for DEEP-D2B:

- `reference_repos/chemicals/chemicals/dippr.py` exposes DIPPR100 heat-capacity
  values and analytic temperature integrals. ChemWorld localizes this as the
  existing `cp_polynomial` evaluator plus strict sampled positive-Cp checks
  before sensible-enthalpy integration.
- `reference_repos/chemicals/chemicals/heat_capacity.py` maps gas, liquid, and
  solid heat-capacity method families to object-level integral APIs. ChemWorld
  does not import those data tables; it adds phase-tagged Cp contracts so task
  and reactor code can state which phase is being integrated.
- `reference_repos/chemicals/chemicals/phase_change.py` documents Watson
  vaporization enthalpy and constant/estimated phase-change families. ChemWorld
  uses caller-supplied Watson or constant latent-heat correlations and signs the
  latent heat by declared transition direction.
- `reference_repos/thermo/thermo/chemical.py` computes enthalpy by explicitly
  walking solid/liquid/gas reference paths through melting and boiling points.
  ChemWorld localizes that convention as `PhaseTransitionSpec`,
  `PhaseEnthalpyReport`, `phase_path_enthalpy_report()`, and
  `MixtureEnthalpyLedger`.
- This closes the reactor/flash heat-duty ledger slice. It does not add broad
  Zabransky/Lastovka/tabular heat-capacity methods, EOS departure enthalpy,
  pressure corrections, or large latent-heat databases.

Reference-reading note for DEEP-D2C:

- `reference_repos/chemicals/chemicals/volume.py` exposes ideal-gas, virial,
  Rackett, COSTALD, Yamada-Gunn, and Amgat-style liquid/mixture volume
  patterns. ChemWorld localizes the Rackett liquid-volume equation, ideal-gas
  molar-volume report, second-virial volume-root hook, and Amgat mixture
  molar-volume ledger without vendoring reference property tables.
- `reference_repos/chemicals/chemicals/virial.py` documents second-virial
  coefficient families and CRC polynomial forms. ChemWorld implements a compact
  caller-supplied CRC polynomial evaluator and explicit real-root failure for
  invalid virial gas-volume states.
- `reference_repos/thermo/thermo/volume.py` separates pure-liquid, gas, and
  mixture volume method dispatch. ChemWorld keeps a smaller benchmark-facing
  contract: reports expose molar volume, optional density, compressibility
  factor/status, validity warnings, model-card provenance, and explicit
  density/molar-volume conversion helpers.
- This closes the first density/molar-volume slice. It does not add broad
  DIPPR116/COSTALD/Yamada-Gunn tables, pressure-corrected liquid volume,
  corresponding-states gas density, or CoolProp-level density backends.

## P3: EOS And Residual Thermodynamics

Reference targets: `CoolProp`, `thermo`, `teqp`, `thermopack`.

- [ ] Refactor cubic EOS into a professional API:
  - [x] pure-parameter generation;
  - [x] binary interaction matrix;
  - [ ] volume translation hook;
  - [x] liquid/vapor/stable root policy;
  - [x] fugacity coefficients;
  - [x] residual enthalpy;
  - [x] residual entropy;
  - [x] departure functions.
- [ ] Add phase-envelope utilities:
  - [ ] saturation solve for pure fluids;
  - [ ] bubble/dew solve for mixtures;
  - [ ] critical-region warning.
- [ ] Add derivative hooks needed for flash and optimization.

Acceptance:

- [x] PR/SRK limiting cases match ideal gas at low pressure.
- [x] Selected methane/ethane/CO2 cases compare against reference backends.
- [x] Root selection is explicit and reproducible.

Reference-reading note for PRO-P3A:

- `reference_repos/thermo/thermo/eos.py` keeps cubic fugacity and departure
  properties together through `main_derivatives_and_departures`, `eos_lnphi`,
  and PR/SRK classes with `H_dep`, `S_dep`, and `phi` attributes.
- `reference_repos/phasepy/phasepy/cubic/cubicpure.py` and `cubicmix.py`
  expose `logfug`, `EntropyR`, and `EnthalpyR` APIs around cubic EOS roots.
- `reference_repos/thermopack/addon/pycThermopack/thermopack/thermo.py`
  exposes residual enthalpy/entropy and fugacity-coefficient API boundaries,
  but relies on compiled backends.
- `reference_repos/teqp/teqp/__init__.py` shows the larger architecture
  direction: fugacity, VLE, and critical-condition hooks are backend-level
  capabilities. ChemWorld localizes only the formula-level PR/SRK residual
  slice needed for benchmark replay.
- Follow-up opt-in reference testing with the cloned `thermo` snapshot records
  a separate `rtol=5e-5` tolerance profile for cubic-EOS residual properties,
  reflecting small independent-implementation convention differences rather
  than hiding them under the tighter activity/flash tolerance.

## P4: Activity Models And Phase Equilibrium

Reference targets: `thermo`, `phasepy`, `thermopack`.

- [ ] Activity models:
  - [ ] Margules formal model card;
  - [x] Wilson;
  - [x] NRTL full binary/ternary form;
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
- [x] At least one nonideal binary case compares against `thermo` or `phasepy`
      for the Wilson/NRTL gamma slice.
- [ ] LLE solver conserves mass and reports stability/initialization failures.

## P5: Reaction Thermochemistry And Kinetics

Reference targets: `Cantera`, `RMG-Py`, `thermo`.

- [ ] Species thermochemistry:
  - [x] NASA-polynomial parser or compact equivalent;
  - [x] Cp/H/S evaluation;
  - [x] reaction enthalpy from species data;
  - [x] equilibrium constants from Gibbs energy.
- [ ] Rate laws:
  - [x] elementary mass-action;
  - [x] reversible rates obeying detailed balance for the validated
        constant-K first-order ODE slice;
  - [x] reversible Arrhenius rates from NASA7 reaction Gibbs energy and
        concentration-standard-state correction;
  - [x] modified Arrhenius;
  - [ ] falloff/Troe-style placeholder with validation target;
  - [ ] pressure-dependent hooks;
  - [ ] heterogeneous catalytic rate template;
  - [x] Butler-Volmer electrochemical rate.
- [x] Sensitivity hooks:
  - [x] finite-difference sensitivities;
  - [x] local parameter perturbation reports.

Acceptance:

- [x] Simple irreversible and reversible ODE cases compare against analytical
      constant-volume first-order solutions, with optional Cantera
      `ArrheniusRate` comparison where available.
- [x] Energy balance uses reaction enthalpy from thermochemistry where
      available.
- [x] Invalid or unbalanced reactions fail before simulation.

## P6: Reactor And Process Dynamics

Reference targets: `Cantera`, `IDAES`.

- [ ] Batch reactor:
  - [x] constant-volume mode;
  - [ ] constant-pressure mode;
  - [x] heat-transfer wall/jacket;
  - [ ] pressure model;
  - [x] event handling for destructive sampling.
- [ ] Semi-batch reactor:
  - [ ] time-dependent feed;
  - [ ] addition-controlled selectivity;
  - [ ] overflow/pressure safety.
- [ ] CSTR:
  - [ ] dynamic startup;
  - [ ] steady-state solve;
  - [x] multiple steady-state example;
  - [x] stability classification.
- [ ] PFR:
  - [ ] axial integration;
  - [ ] heat-transfer profile;
  - [ ] pressure drop;
  - [ ] hotspot detection.
- [ ] Reactor networks:
  - [ ] reservoir/feed objects;
  - [ ] valves/flow devices;
  - [ ] serial/parallel reactors.

Reference-reading note for PRO-P6A:

- `cantera/doc/sphinx/userguide/reactor-tutorial.md` documents a CSTR as a
  single well-stirred reactor with inlet/outlet reservoirs and steady-state
  advancement through `ReactorNet.advance_to_steady_state`.
- `cantera/samples/python/reactors/continuous_reactor.py` shows the practical
  stirred-reactor construction using reservoirs, a mass-flow controller,
  pressure controller, reactor volume, and a reactor network.
- `idaes-pse/idaes/models/unit_models/cstr.py` builds a 0D control-volume CSTR
  with material, energy, and momentum balances.
- The IDAES `cstr_performance_eqn` relates reaction extent to
  `volume * reaction_rate`, which ChemWorld mirrors in the analytical
  exothermic CSTR multiplicity slice.
- ChemWorld's completed slice solves a scalar exothermic first-order CSTR
  energy-balance problem, finds three steady states, and classifies the
  stable/unstable/stable branches from the dynamic CSTR Jacobian. This is not a
  full reactor-network or process-control clone.

Reference-reading note for DEEP-D6A:

- `cantera/src/zeroD/Reactor.cpp` separates species production, wall heat
  `Qdot`, inlet/outlet enthalpy, and energy-equation terms. ChemWorld localizes
  that separation as a compact batch kernel rather than copying Cantera's
  reactor network.
- `cantera/src/zeroD/IdealGasReactor.cpp` uses a temperature-state energy
  equation with a heat-capacity left-hand side. ChemWorld's liquid-phase
  dynamic batch slice uses `rhoCp V dT/dt`.
- IDAES modular property/state definitions expose enthalpy and internal-energy
  flow/density terms for control-volume energy balances. ChemWorld keeps the
  same accounting idea in explicit material and energy ledgers.
- `DynamicBatchReactorModel` now implements `dn/dt = S r(n,T)`,
  `rhoCp V dT/dt = Q_jacket - Q_loss - sum(DeltaH_i(T) r_i V)`,
  optional NASA7 reaction enthalpy, time-dependent jacket setpoints, and
  destructive sampling events with `material_out` and volume ledgers. This
  closes the constant-volume dynamic batch heat-release/sampling slice, not
  constant-pressure, pressure dynamics, vapor-liquid expansion, or full
  process-control behavior.

Reference-reading note for DEEP-D5D:

- `cantera/include/cantera/zeroD/ReactorNet.h` and
  `cantera/interfaces/cython/cantera/reactor.pyx` define normalized
  sensitivity coefficients as `S = (1/y) dy/dp` for registered reaction
  multiplier parameters. ChemWorld localizes this as central finite
  differences in `ln(parameter)` for positive kinetic parameters.
- `rmg-py/arkane/sensitivity.py` perturbs kinetic/energy parameters, reruns the
  job, and reports finite-difference sensitivity coefficients. ChemWorld uses
  the same perturb-and-recompute idea but keeps a smaller JSON-friendly report.
- `finite_difference_reaction_sensitivities()` now scans multiplier-like
  positive kinetic parameters (`k`, `A`, `A_reverse`, `K_eq`, `vmax`, `Km`),
  computes `d y / d ln(p)`, normalized local sensitivity, uncertainty
  contribution estimates, and ranked explanation summaries. This is a local
  benchmark/explanation hook, not an adjoint, global Sobol, or pressure-dependent
  sensitivity solver.

Acceptance:

- [x] Selected reactor cases compare against Cantera or a documented analytical
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
  - [x] shortcut Fenske option;
  - [x] VLE-coupled task.
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

- [x] No distillation task uses an unlabeled distillation proxy in the benchmark default.
- [ ] Purity/recovery/cost tradeoffs are produced by declared physical models.

Reference-reading note for PRO-P7A:

- `idaes-pse/idaes/models/unit_models/flash.py` builds a static flash unit
  around a 0D control volume, phase-equilibrium state blocks, material balances,
  energy balances, momentum balances, and vapor/liquid outlet ports.
- `idaes-pse/.../activity_coeff_prop_pack.py` `_make_flash_eq` declares total
  and component flash balances and a smooth VLE flash formulation.
- `thermo/README.rst` and `thermo/thermo/flash/flash_vl.py` show `FlashVL`
  objects built from constants, property correlations, liquid/gas phase objects,
  and PT/VF flash specifications.
- `phasepy/phasepy/equilibrium/flash.py` solves PT flash using K-values,
  Rachford-Rice material balance, accelerated successive substitution, and
  Gibbs minimization fallback.
- ChemWorld localizes those ideas as `vle_shortcut_distillation`: VLE K-values
  come from Raoult/activity models, relative volatilities are derived from
  those K-values, and component split ratios satisfy a Fenske-style analytical
  identity. This is not a full MESH column solver.

## P8: Transport, Equipment, And Safety

Reference targets: `fluids`, `IDAES`, `CoolProp`.

- [ ] Pressure drop:
  - [ ] pipe friction;
  - [ ] fittings/minor losses;
  - [ ] packed bed;
  - [ ] two-phase warnings.
- [ ] Heat transfer:
  - [x] jacketed reactor;
  - [x] heat exchanger;
  - [ ] boiling/condensation warning models;
  - [x] fouling factor.
- [ ] Mixing:
  - [ ] impeller power;
  - [ ] mixing time;
  - [ ] mass-transfer coefficient proxy with validity limits.
- [ ] Safety:
  - [ ] pressure relief proxy;
  - [ ] runaway index;
  - [ ] flammability/volatility flags.

Acceptance:

- [x] Selected dimensionless and equipment calculations compare against
      `fluids`.
- [ ] Safety cost in tasks is traceable to declared physical terms.

Reference-reading note for PRO-P8A:

- `fluids.core.Nusselt`, `Prandtl`, and `Reynolds` define the dimensionless
  number contracts used for optional reference validation. The local
  `reference_repos/fluids` checkout did not include a complete
  `conv_internal` implementation, so ChemWorld implements the Dittus-Boelter
  and Gnielinski branches locally with explicit validity metadata rather than
  pretending to wrap a missing backend.
- `idaes-pse/idaes/models/unit_models/heat_exchanger.py` exposes heat-exchanger
  contracts around `U`, area, temperature-difference callbacks, and stream heat
  duties.
- `idaes-pse/idaes/models/unit_models/heat_exchanger_ntu.py` exposes the
  e-NTU contract: `C_min`, `C_max`, capacity ratio, `NTU = U A / C_min`, and
  duty as effectiveness times available heat.
- CoolProp high-level API docs reinforce that thermophysical-property backends
  should stay outside ChemWorld's default runtime; ChemWorld's heat-transfer
  slice therefore accepts explicit properties with SI units.
- ChemWorld localizes those ideas as
  `nusselt_internal_flow_details()`, explicit validity warnings,
  `strict_validity=True`, `internal_heat_transfer_coefficient()`, and
  `heat_exchanger_counterflow()` duty-balance metadata. This is not a claim of
  shell-and-tube design, boiling/condensation modeling, or dynamic fouling.

## P9: Equilibrium Chemistry And Electrochemistry

Reference targets: `Reaktoro`, `Cantera`, `pycalphad`.

- [x] Gibbs minimization toy solver:
  - [x] element constraints;
  - [x] charge constraints;
  - [x] phase restrictions;
  - [x] nonnegative species.
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
  - [x] Nernst potential;
  - [x] Butler-Volmer kinetics;
  - [x] Faradaic efficiency;
  - [x] energy accounting.

Acceptance:

- [ ] At least one aqueous equilibrium case compares against Reaktoro or a
      documented analytical case.
- [ ] Electrochemical tasks use charge and energy accounting, not only labels.

Reference-reading note for PRO-P9A:

- `reaktoro/Reaktoro/Equilibrium/EquilibriumSpecs.hpp` separates equilibrium
  problem declarations, equation constraints, control variables, and
  reactivity restrictions. ChemWorld adopts that separation at small scale as a
  fixed-TP spec with explicit species, phases, element balances, charge target,
  and phase restrictions.
- `reaktoro/Reaktoro/Equilibrium/SmartEquilibriumSolver.hpp` treats the initial
  state as both guess and mutable result, and reports solver outcome through a
  result object. ChemWorld localizes this as a JSON-friendly
  `GibbsMinimizationResult` with convergence, iterations, residuals, active
  phases, and solver metadata.
- Cantera's Python tutorial documents `equilibrate("TP")`, `equilibrate("HP")`,
  and the distinction between element-potential and Gibbs-minimization
  formulations. ChemWorld implements only the fixed-TP Gibbs slice in this
  task.
- `pycalphad/core/equilibrium.py` organizes equilibrium calculations around
  components, phases, conditions, `GM`, and `MU` outputs. ChemWorld mirrors the
  condition/phase/result-card shape, but does not implement CALPHAD databases,
  site-fraction models, or global phase-selection algorithms.
- ChemWorld's local solver minimizes
  `sum_i n_i G_i^0 + R T sum_i n_i ln(x_i_phase)` with explicit linear
  conservation constraints. It removes linearly redundant constraints before
  calling SLSQP and still reports full element and charge residuals after
  solving.

## P10: Instruments And Spectroscopy

Reference targets: public instrument equations and datasets, not primarily the
thermodynamic libraries.

- [x] Chromatography:
  - [x] HPLC retention-time model;
  - [x] GC volatility/retention model;
  - [x] peak broadening and overlap;
  - [x] calibration uncertainty.
- [ ] Spectroscopy:
  - [x] UV-vis Beer-Lambert model;
  - [ ] IR functional-group bands;
  - [ ] NMR shift proxy with coupling metadata;
  - [ ] optional MS fragment proxy.
- [ ] Instrument operations:
  - [ ] destructive sample accounting;
  - [x] UV-vis calibration runs;
  - [ ] replicate strategy;
  - [ ] detection-limit behavior.

Acceptance:

- [ ] Instrument signals are generated from species state, not score fields.
- [x] UV-vis has a Beer-Lambert model card and analytical sanity examples.
- [x] HPLC/GC have retention-factor, plate-count, and resolution model-card examples.
- [ ] Each instrument has a model card and at least one public sanity example.

Reference-reading note for PRO-P10A:

- `reference_repos/chemicals/docs/developers.rst` notes that IR, NMR, MS, and
  UV-Vis spectra are plausible future data additions and names public database
  sources such as NIST, but `chemicals` does not implement a UV-vis instrument
  kernel.
- Local reading covered `src/chemworld/physchem/spectroscopy.py` and
  `src/chemworld/world/spectra.py`, where ChemWorld already synthesized
  state-coupled spectra from species amounts.
- ChemWorld localizes the public Beer-Lambert relation as
  `BeerLambertBandSpec`, `beer_lambert_absorbance()`,
  `fit_beer_lambert_calibration()`, and `generate_beer_lambert_calibration()`.
  The implementation separates true molar absorptivity, path length, sample
  dilution, blank absorbance, effective calibration slope, LOD, and LOQ.

Reference-reading note for PRO-P10B:

- Local reading covered the existing HPLC/GC code path in
  `src/chemworld/physchem/spectroscopy.py` and `src/chemworld/world/spectra.py`.
  Before this task, retention centers were role-based constants with stable
  species offsets.
- `reference_repos/rmg-py/documentation/source/users/rmg/liquids.rst` cites
  chromatography and LSER references by Vitha-Carr and Poole, but does not
  implement HPLC/GC instrument kernels.
- ChemWorld localizes public chromatography equations as
  `chromatographic_retention_time()`, `chromatographic_retention_factor()`,
  `chromatographic_baseline_peak_width()`,
  `chromatographic_theoretical_plates()`, `chromatographic_resolution()`, and
  `fit_chromatography_calibration()`. HPLC/GC species peaks now carry dead
  time, retention factor, theoretical plates, baseline width, and adjacent
  resolution metadata.

## P11: Benchmark Task Integration

Reference targets: DiscoveryWorld-style scientific task design, Gymnasium,
Minari, Safety-Gymnasium.

- [x] Each task declares kernel maturity:
  - [x] proxy allowed;
  - [x] lite;
  - [x] reference validated;
  - [ ] professional.
- [ ] Add professional task families:
  - [ ] reference-validated VLE flash;
  - [ ] LLE solvent selection;
  - [ ] CSTR multiplicity;
  - [ ] PFR hotspot;
  - [ ] reaction calorimetry;
  - [ ] electrochemical selectivity;
  - [ ] crystallization purity/recovery.
- [x] Add dataset exports with maturity metadata.
- [x] Add leaderboard views by physics maturity level.

Acceptance:

- [x] A benchmark result cannot silently mix proxy and professional kernels.
- [x] Submission summaries report the physics maturity of every task.

Reference-reading note for PRO-P11A:

- Gymnasium's environment specification pattern keeps environment metadata
  serializable and separate from runtime state. ChemWorld localizes that idea by
  exporting task/kernel maturity through task cards, trajectory records, suite
  results, baseline reports, and submission summaries.
- Minari/Safety-Gymnasium-style dataset and safety metadata informed the
  decision to keep proxy allowance and physics maturity visible in every
  benchmark artifact rather than only in docs.
- PRO-P11B adds `task_maturity_manifest()` so release tooling can inspect the
  same task/kernel maturity records without running environments or baselines.

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

Reference-reading note for PRO-P4A:

- `thermo.activity.GibbsExcess` separates state, cached activity coefficients,
  excess Gibbs energy, derivatives, and JSON-friendly model metadata.
- `thermo.wilson.Wilson_gammas` documents the standard Wilson gamma equation
  and the directional `Lambda_ij` matrix; ChemWorld localizes this as explicit
  pair-key parameters instead of a heavy object hierarchy.
- `thermo.wilson.Wilson` supports temperature-dependent `Lambda_ij` through
  `a + b/T + c ln(T) + dT + e/T^2 + fT^2`; ChemWorld implements the same
  coefficient contract with strict missing-pair validation.
- `thermo.nrtl.NRTL_gammas_binaries` and `thermo.nrtl.NRTL` document the
  directional `tau_ij`, `alpha_ij`, and `G_ij = exp(-alpha_ij tau_ij)` sums;
  ChemWorld implements the general multicomponent form and validates binary
  examples against `thermo`.
- `phasepy.actmodels.wilson` and `phasepy.actmodels.nrtl` expose compact
  `ln gamma` functions over matrices. ChemWorld adopts the compact API spirit
  while keeping plain JSON-friendly specs and model cards.

Reference-reading note for PRO-P5A:

- `cantera/doc/sphinx/yaml/reactions.md` shows the shared reaction-language
  contract used here: `=>` for irreversible reactions, `<=>` for reversible
  reactions, and explicit `rate-constant` records.
- `cantera/test/python/test_reaction.py` verifies the Arrhenius form
  `A*T**b*exp(-Ea/RT)` through `ct.ArrheniusRate`.
- `cantera/doc/sphinx/reference/reactors/index.md` and reactor examples frame
  reactor integration as a coupled ODE/DAE system advanced by `ReactorNet`.
- `rmg-py/rmgpy/kinetics/arrhenius.pyx` implements
  `A*(T/T0)**n*exp(-Ea/RT)` for Arrhenius rate coefficients.
- `rmg-py/rmgpy/reaction.py` generates reverse Arrhenius data from
  `k_forward/K_eq`; ChemWorld's first validated reversible slice implements
  the constant-K version of that relationship.
- This task closes only the constant-volume, isothermal, homogeneous,
  first-order ODE slice. Falloff, third bodies, pressure dependence,
  thermochemistry-derived `K(T)`, and heat-release-coupled reactor validation
  remain open professional work.

Reference-reading note for PRO-P5B:

- `cantera/include/cantera/thermo/NasaPoly1.h` documents the NASA7 equations
  for `Cp/R`, `H/RT`, and `S/R`, including the coefficient order `a0..a6`.
- `cantera/src/thermo/NasaPoly2.cpp` shows the two-temperature-segment NASA7
  shape and validates continuity at the shared mid temperature.
- `cantera/test/data/yaml-ck-reactions.yaml` shows the Cantera YAML contract:
  `thermo: model: NASA7`, `temperature-ranges`, and segment coefficient
  `data`.
- `rmg-py/rmgpy/yaml_cantera2.py` exports sorted NASA polynomials into the
  same Cantera YAML NASA7 structure.
- `rmg-py/rmgpy/thermo/nasa.pyx` selects the valid NASA polynomial by
  temperature before computing Cp, H, and S.
- ChemWorld localizes this as `NASA7TemperatureSegment`,
  `NASA7SpeciesThermo`, `reaction_thermochemistry()`, and
  `equilibrium_constant_from_delta_g()`. It closes species Cp/H/S/G,
  reaction Delta H/S/G, and `K = exp(-Delta G/RT)`. It does not claim NASA9,
  Shomate, group additivity, pressure corrections, or thermochemistry-coupled
  reactor energy integration yet.

Reference-reading note for PRO-P5C:

- `cantera/include/cantera/thermo/IdealGasPhase.h` documents the microscopic
  reversibility bridge from thermodynamic equilibrium expressions to reverse
  rate constants, and distinguishes dimensionless activity equilibrium
  constants from concentration equilibrium constants used by kinetics managers.
- `cantera/include/cantera/thermo/ThermoPhase.h` explicitly defines `K_a`,
  `K_p`, and `K_c`, and states that kinetics managers require `K_c` for
  reverse rate constants.
- `rmg-py/rmgpy/solver/simple.pyx` populates forward rates, equilibrium
  constants, and reverse rates with `k_reverse = k_forward / K_eq` for
  reversible reactions.
- `rmg-py/rmgpy/kinetics/diffusionLimited.py` uses the same `k_forward / Keq`
  relationship before applying diffusion-limit corrections.
- ChemWorld localizes this as `thermochemical_detailed_balance()`,
  `thermochemical_concentration_equilibrium_constant()`, and
  `reverse_rate_constant_from_equilibrium()`. A `reversible_arrhenius` rate law
  can now declare `K_eq_source: nasa7`; when `species_thermo` is supplied,
  reverse rates come from NASA7 reaction Gibbs energy and
  `K_c = exp(-Delta G/RT) * C0^(sum nu_i)`. This closes the detailed-balance
  reverse-rate slice, not falloff, pressure dependence, or reactor
  heat-release coupling.

- [ ] `thermo`:
  - [x] ideal Raoult VLE bubble/dew/TP flash;
  - [x] nonideal activity-coefficient case;
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

- [x] Optional validation tests skip cleanly without external packages.
- [x] Running validation locally produces JSON-friendly comparison summaries.
- [ ] Model-limit divergences are documented rather than hidden.

Reference-reading note for PRO-P12B:

- Local optional-reference tests already used explicit pytest skip gates for
  unavailable packages. ChemWorld now mirrors that runtime behavior in a
  persistent `ReferenceValidationReport`.
- `skipped_reference_backends()` records package availability, failed import
  probes, comparison scope, and model-limit notes so missing optional packages
  are visible in validation artifacts.
- PRO-P12C extends backend status records with optional package versions when
  discoverable, all twelve local reference repository targets, short checkout
  commits when present, and declared tolerance profiles for common comparison
  families.

## First Professional Implementation Queue

This queue records the first twelve narrow implementation slices used to move
ChemWorld out of the proxy/lite phase. Completing this queue does not mean the
broad P1-P12 professional modules above are complete. Any unchecked boxes in the
module sections remain open professional work and should be claimed as concrete
deepening slices in `TODO_PROFESSIONAL_DEEPENING.md`.

1. `PRO-P0`: Add maturity metadata and model-card template to code/docs.
2. `PRO-P12A`: Expand reference validation for `fluids` friction factor and
   pressure drop. Done.
3. `PRO-P2A`: Replace placeholder vapor-pressure/enthalpy examples with
   curated reference-checked compounds. Done.
4. `PRO-P4A`: Implement Wilson and full binary NRTL with reference comparisons.
   Done.
5. `PRO-P5A`: Add Cantera-comparable irreversible and reversible reaction ODE
   cases. Done.
6. `PRO-P6A`: Add CSTR multiple-steady-state professional example.
   Done.
7. `PRO-P7A`: Replace simple distillation proxy with VLE-coupled shortcut
   distillation. Done.
8. `PRO-P10A`: Add Beer-Lambert UV-vis model card and calibration validation.
   Done.
9. `PRO-P10B`: Add HPLC/GC retention-factor and peak-broadening calibration.
   Done.
10. `PRO-P3A`: Add Peng-Robinson/SRK fugacity-coefficient and residual-property
    validation slice with explicit root-selection policy. Done.
11. `PRO-P8A`: Add reference-validated heat-transfer correlations and
    heat-exchanger duty checks for reactor/process energy ledgers. Done.
12. `PRO-P1A`: Harden the component registry with provenance, aliases,
    uncertainty fields, and conflict-resolution policy. Done.

After queue item 12 is completed, open `TODO_PROFESSIONAL_DEEPENING.md` as the
active professional roadmap. Do not use the deepening roadmap to mark broad
modules complete without concrete equations, reference readings, validation
cases, model cards, and task integration tests.

## Explicit Non-Goals

- Do not vendor external library code.
- Do not claim real reaction prediction without data and validation.
- Do not hide proxy kernels behind professional names.
- Do not require heavy compiled packages for the default educational install.
- Do not use large third-party data tables without license and provenance
  review.
