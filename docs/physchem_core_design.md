# PhysChem Core Design

ChemWorld now includes a small `chemworld.physchem` layer. Its current job is
to provide a compact foundation/lite physical-chemistry core for benchmark
development. It is not professional-library parity with Cantera, CoolProp,
thermo, phasepy, IDAES, Reaktoro, pycalphad, teqp, thermopack, or RMG-Py.

The post-foundation professional roadmap is tracked separately in
`TODO_PROFESSIONAL.md` and summarized in the Professional TODO docs page.
Professional work must replace or harden proxies with explicit models,
reference reading notes, model cards, validity limits, and controlled numerical
validation.

## Reference Reading

The local reference repositories were used as design references only:

- `chemicals` separates elemental bookkeeping, formula parsing, molecular
  weights, and composition utilities.
- `thermo` separates chemical constants from property-correlation packages and
  mixture state objects.
- `Cantera` uses declarative species, phase, and reaction specifications as the
  stable interface between mechanism files and numerical kernels.

ChemWorld localizes those ideas into a compact, auditable, JSON-friendly core.
No reference-project source code is copied. When a local implementation is only
qualitative or educational, it must remain labeled as proxy/lite rather than
being presented as professional-grade physics.

## Current Scope

The implementation slices currently cover the P1-P12 foundation/lite batch:

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
- `property_equation_contracts()`: a public introspection API exposing required
  coefficients, accepted input dimensions, and output dimensions for every
  supported property equation.
- reaction-network, reactor, EOS, phase-equilibrium, equilibrium-chemistry,
  separation, transport, and heat-transfer kernels described below.

## Property Core

The P2 property core is implemented in `chemworld.physchem.properties`. It
supports the following local evaluators and now validates each one against a
declared equation contract before numerical evaluation:

| Property family | Supported equations |
| --- | --- |
| Vapor pressure | Antoine, Wagner, DIPPR101/Perry form |
| Heat capacity | Cp polynomial, Poling/DIPPR100 ideal-gas Cp slice |
| Enthalpy | analytic Cp-polynomial sensible-enthalpy integral |
| Phase change | Watson heat-of-vaporization correlation, constant heat-of-fusion proxy |
| Density | linear liquid density, ideal gas density |
| Viscosity | Andrade liquid viscosity, Sutherland gas viscosity |
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

The P1/P2 audit hardened the foundation around those evaluators:

- component identifiers reject whitespace and padded values;
- formula-derived molecular weight and manually supplied molecular weight must
  agree within a small tolerance;
- component aliases, safety tags, and allowed-correlation policies reject
  duplicates;
- mixture constructors validate component/phase compatibility before creating
  a phase-local state;
- property correlations reject unsupported equations, missing required
  coefficients, wrong unit dimensions, unknown input fields, and invalid
  validity-range variables;
- `ComponentPropertyPackage` enforces the component's
  `allowed_property_correlations` policy by correlation id, property id, or
  equation id;
- `PropertyCorrelation.model_card()` and `property_equation_contracts()` provide
  JSON-friendly audit records for docs, schema generation, and external review.

Acceptance coverage now includes formula parsing, mole/mass conversion
round-trips, JSON round-trips for component/mixture/correlation specs, unit
dimension failures before kernel use, monotonic water vapor pressure, Cp
integral sign and units, positive density/viscosity/phase-change values, gas
viscosity behavior, and component-level property policy failures.

PRO-P2A adds the first reference-validated curated property slice in
`chemworld.physchem.curated_properties`. It intentionally keeps the data set
small and auditable instead of vendoring a large third-party property database.
The current curated compounds are water, ethanol, acetone, toluene, methane,
and carbon dioxide. Each package includes component metadata, a DIPPR101/Perry
vapor-pressure correlation, a Poling/DIPPR100 ideal-gas heat-capacity
correlation scaled into SI units, validity ranges, source notes, and a model
card. Optional reference tests compare ChemWorld values against local
`chemicals` reference implementations for vapor pressure, ideal-gas Cp, and
sensible enthalpy integrals.

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

PRO-P5A adds the first reference-validated reaction ODE slice. The function
`cantera_comparable_reaction_cases()` now returns two ChemWorld-owned
constant-volume, isothermal, homogeneous batch ODE reference cases:

- an irreversible first-order `A => B` case with analytical
  `A(t) = A0 exp(-kt)`;
- a reversible first-order `A <=> B` case with finite `K_eq = k_f/k_r` and
  analytical relaxation to the equilibrium ratio.

`evaluate_reaction_ode_reference_case()` integrates each `ReactionNetworkSpec`
and compares the full trajectory against the analytical solution. The related
model card is exposed through `reaction_kinetics_model_cards()` and records
the inspected Cantera/RMG references: Cantera reaction equations and
`ArrheniusRate`, Cantera ReactorNet's ODE framing, RMG Arrhenius rate
coefficients, and RMG reverse-rate generation from `k_forward/K_eq`. Optional
reference tests additionally compare the local Arrhenius rate constant against
`ct.ArrheniusRate` if Cantera is available.

This closes a narrow professional slice, not the whole kinetics stack.
Falloff, third bodies, pressure-dependent rates, thermochemistry-derived
`K(T)`, and heat-release-coupled reactor validation remain explicit future
professional tasks.

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

## Spectroscopy and Instrument Coupling

The P11 spectroscopy core is implemented in
`chemworld.physchem.spectroscopy` and connected to the world observation layer
through `chemworld.world.spectra` and `chemworld.world.observation_kernel`.

Reference reading showed that the local professional references focus on
thermodynamics, reaction kinetics, reactor models, and process equipment rather
than HPLC/NMR-style virtual instrument synthesis. ChemWorld therefore implements
its own compact observation-kernel model instead of copying a spectroscopy
package. The design goal is not database-grade spectral prediction; it is a
realistic, auditable instrument layer for benchmark interaction.

Current capability:

| Instrument | Species mapping |
| --- | --- |
| HPLC | species groups map to retention-factor peaks with dead time, theoretical plates, baseline peak width, detector response calibration, and adjacent-peak resolution metadata |
| GC | volatile and vapor-like species map to retention-factor peaks with dead time, theoretical plates, baseline peak width, detector response calibration, and adjacent-peak resolution metadata |
| UV-vis | species amounts map to Beer-Lambert bands with path length, dilution, molar absorptivity, blank absorbance, LOD/LOQ calibration metadata, and proxy fallbacks when only aggregate score fields are available |
| IR | formula/role proxies map to fingerprint, carbonyl-like, O-H-like, and C-H-like bands |
| NMR | species roles map to compact 1H chemical-shift proxy peaks |

PRO-P10A adds a reference-validated UV-vis analytical slice. The implementation
uses the Beer-Lambert relation,

```text
A = A_blank + epsilon * l * c_cuvette
c_cuvette = c_reactor / dilution_factor
```

and exposes `BeerLambertBandSpec`, `beer_lambert_absorbance()`,
`fit_beer_lambert_calibration()`, `generate_beer_lambert_calibration()`, and
`spectroscopy_model_cards()`. Calibration fits report the effective slope
against reactor concentration, true molar absorptivity after dilution
correction, residual standard deviation, LOD, LOQ, and slope uncertainty. This
closes a narrow UV-vis calibration slice; it does not claim empirical UV-vis
database prediction.

PRO-P10B adds a reference-validated HPLC/GC chromatography slice. The
implementation uses public analytical chromatography equations,

```text
k' = (t_R - t_M) / t_M
t_R = t_M * (1 + k')
w_b = 4 * t_R / sqrt(N)
N = 16 * (t_R / w_b)^2
R_s = 2 * (t_R2 - t_R1) / (w_b1 + w_b2)
```

and exposes `ChromatographyMethodSpec`,
`fit_chromatography_calibration()`, `chromatographic_resolution()`, and related
helpers. HPLC/GC peaks now store dead time, retention factor, theoretical
plates, baseline width, and minimum adjacent resolution metadata. This closes a
narrow retention/plate-count slice; it does not claim empirical retention-index
prediction, gradient elution, column aging, or peak tailing.

Each signal spec declares:

- axis name, units, range, and point count;
- peak center, width, response factor, role assignment, and shape;
- calibration curve with slope, intercept, detection limit, and uncertainty;
- baseline intercept and baseline drift;
- replicate count and replicate raw signals;
- processed species-level estimates and uncertainty;
- peak-overlap metadata.

The world environment now passes hidden species amounts into the spectroscopy
synthesizer during measurement actions, but the returned observation does not
expose the hidden state ledger. Agents see only plot-ready raw signals,
calibrated estimates, uncertainty, instrument cost, and sample consumption.
This preserves partial observability while making HPLC/GC/UV-vis/IR/NMR outputs
depend on the actual mechanism state rather than only on aggregate score fields.

## Optional Reference Backend Validation

The P12 reference-validation layer is implemented in
`chemworld.physchem.reference_validation`. It does not make external scientific
packages runtime dependencies. Instead, it provides:

- `ReferenceBackendSpec` records for tracked external backends;
- `reference_backend_status()` to report installed packages, local
  `reference_repos/` availability, and optional import-probe errors;
- `reference_backend_context()` and `import_reference_module()` to temporarily
  import locally cloned reference repositories without vendoring them;
- `compare_scalar()` and `summarize_reference_comparisons()` to record
  ChemWorld/reference differences with explicit tolerances and model-limit
  notes.

The current executable optional checks cover formula-level comparisons that are
small enough to audit and stable enough to run locally:

| Reference backend | Current optional checks | Tolerance |
| --- | --- | --- |
| `chemicals` | ideal-gas molar volume via `chemicals.volume.ideal_gas`; Rachford-Rice vapor fraction and phase compositions via `chemicals.rachford_rice.Rachford_Rice_solution`; curated DIPPR101 vapor-pressure points via `chemicals.dippr.EQ101`; curated Poling ideal-gas Cp and sensible enthalpy integrals via `chemicals.dippr.EQ100` | `rtol=1e-12` |
| `fluids` | Reynolds and Prandtl numbers via `fluids.core`; Haaland Darcy friction factor and single-phase pipe pressure drop via `fluids.friction` | `rtol=1e-12` |
| `thermo` | ideal Raoult-law bubble/dew pressure and two-phase TP flash via `thermo.property_package.Ideal` with explicit constant vapor-pressure callables; fixed-lambda Wilson gamma via `thermo.wilson.Wilson_gammas`; fixed tau/alpha NRTL gamma via `thermo.nrtl.NRTL_gammas_binaries` | `rtol=1e-12` for bubble/dew and gamma checks; `rtol=1e-11` for flash solver roundoff |

Run the normal test path to confirm reference tests skip cleanly when optional
backends are not enabled:

```bash
python -m pytest tests/reference
```

Run the local reference comparisons against packages installed in the
environment or source trees under `reference_repos/`:

```bash
CHEMWORLD_RUN_REFERENCE_TESTS=1 python -m pytest tests/reference
```

On PowerShell:

```powershell
$env:CHEMWORLD_RUN_REFERENCE_TESTS = "1"
python -m pytest tests/reference
```

CoolProp, Cantera, phasepy, Reaktoro, and pycalphad are registered as reference
targets with explicit model-limit notes, but their numerical comparisons are
not marked complete until their compiled or optional dependencies are available
and the corresponding checks can run in a controlled environment. In the current
local snapshot, `phasepy` exposes useful LLE/VLE source structure for design
reading but cannot be imported directly without its compiled Cython extension,
so ChemWorld's completed VLE reference check uses `thermo` instead.

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

PRO-P6A adds the first reference-validated reactor multiplicity slice. The
function `cstr_multiple_steady_state_reference_case()` defines an exothermic
first-order CSTR with feed concentration, residence time, coolant temperature,
`UA`, heat-capacity density, heat of reaction, and Arrhenius parameters. The
solver `solve_cstr_multiple_steady_states()` reduces the coupled steady-state
material and energy balances to a scalar energy residual,

```text
0 = (-DeltaH) V k(T) C_A(T) - rhoCp q(T - T_f) - UA(T - T_c)
C_A(T) = C_Af / (1 + k(T) V/q)
```

and finds three roots for the default ignition/extinction case. Each root is
returned with conversion, reaction rate, heat generation, heat removal,
residual, dynamic-Jacobian eigenvalues, and a stable/unstable/marginal label.
The model card exposed through `reactor_model_cards()` records the inspected
Cantera stirred-reactor examples and IDAES CSTR control-volume contract. This
is a deliberately narrow professional slice, not a full Cantera or IDAES clone.

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
| Activity coefficients | ideal, Margules, Wilson, and NRTL models |
| Raoult K-values | activity-corrected `K_i = gamma_i Psat_i / phi_i P` |
| Flash | Rachford-Rice vapor fraction and liquid/vapor compositions |
| Bubble/dew pressure | iterative estimates with activity coefficients |
| LLE stage | material-conserving extraction split with partition coefficients, phase volumes, stage efficiency, and entrainment |

PRO-P4A hardens the nonideal activity path. Wilson and NRTL now use explicit
directional pair-key parameters instead of unlabeled proxy matrices. Wilson
supports fixed `Lambda_ij` values or temperature-dependent coefficient form
`a + b/T + c ln(T) + dT + e/T^2 + fT^2`. NRTL supports fixed or
temperature-dependent `tau_ij` terms, `alpha_ij` terms, and the standard
`G_ij = exp(-alpha_ij tau_ij)` local-composition sum. Missing off-diagonal
Wilson/NRTL interactions fail during `ActivityModelSpec` construction, so a
nonideal model cannot silently fall back to ideal behavior. Optional reference
tests compare the implemented gamma equations against `thermo.wilson` and
`thermo.nrtl`.

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
| VLE shortcut distillation | Raoult/activity K-values, relative volatilities, Fenske-style split ratios, reflux-scaled effective stages, heat duty, and purity/recovery/cost tradeoff |
| Crystallization | solubility-limited crystallization, cooling proxy, impurity occlusion, crystal-size proxy |
| Filtration | solid recovery, impurity retention, washing efficiency, and wash loss |
| Drying | solvent removal, residual solvent, heat duty, thermal degradation risk |

All units return a shared `SeparationResult` with named outlets and a
`SeparationLedger`. This makes downstream processing benchmarkable: a task can
reward purity and recovery while penalizing cost, risk, solvent loss, and
process mass-balance errors. Excessive purification is therefore not
automatically optimal, which is important for realistic reaction-to-purification
tasks.

PRO-P7A replaces the old score-based distillation split with
`vle_shortcut_distillation()`. The model first computes `K_i` values through the
shared phase-equilibrium layer,

```text
K_i = gamma_i Psat_i / (phi_i P)
alpha_i,HK = K_i / K_HK
N_eff = N_theoretical * tray_efficiency * R/(1+R)
(D_i/B_i)/(D_j/B_j) = (alpha_i/alpha_j)**N_eff
```

and then solves a single cut parameter so the requested total distillate amount
is met exactly. This gives agents a physically interpretable lever: vapor
pressure, activity model, pressure, reflux, stage count, and tray efficiency all
affect purity, recovery, energy cost, and risk. The environment's `distill`
operation now calls this kernel and records the VLE/Fenske metadata in the
state ledger. The model card exposed through `separation_model_cards()` records
the inspected IDAES flash/control-volume design, thermo `FlashVL` API, and
phasepy PT-flash algorithm. This is still a shortcut model, not a full MESH
column solver.

## Transport and Heat-Transfer Core

The P8 transport core is implemented in `chemworld.physchem.transport`. It adds
the first local equipment-calculation layer needed by professional interaction
environments: flow, pressure, pumping, mixing, heat transfer, and compact
two-phase/packed-bed proxies.

| Capability | Current implementation |
| --- | --- |
| Dimensionless groups | Reynolds, Prandtl, Peclet, and internal-flow Nusselt estimates |
| Flow regime | laminar, transitional, and turbulent classification |
| Friction factor | explicit `auto`, `laminar`, and `haaland` branches with method metadata and validity warnings |
| Pipe pressure drop | Darcy-Weisbach friction, fittings loss, static head, pump work, and recorded friction-method evidence |
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

The first reference-validated transport slice is now the single-phase pipe-flow
path. `transport_model_cards()` records a model card for laminar/Haaland Darcy
friction and Darcy-Weisbach pressure drop. Optional reference tests compare the
Haaland branch to `fluids.friction.Haaland` and the pipe pressure-drop result to
`fluids.friction.one_phase_dP` with `Method='Haaland'`. The homogeneous
two-phase function remains a compact benchmark proxy until a later professional
two-phase-correlation task replaces or validates it.

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
