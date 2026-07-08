# ChemWorld Professional Deepening TODO

This file is the next professional roadmap after the first twelve implementation
queue slices in `TODO_PROFESSIONAL.md` are complete. It does not mean the broad
P1-P12 professional modules are complete. Those module-level unchecked boxes are
the reason this deepening roadmap exists. It is intentionally more detailed than
a normal backlog: ChemWorld should mature by implementing narrowly scoped,
auditable physical-chemistry modules one slice at a time, not by filling the
world with proxies.

Status: active. The first twelve professional implementation queue slices in
`TODO_PROFESSIONAL.md` are done and pushed; broad module-level unchecked boxes
remain open and must be handled here as concrete deepening slices.

## Deepening Contract

- Owner marker: `whilesunny` unless another teammate explicitly claims an item.
- Before coding, claim one concrete slice in this file and push the claim.
- Pull `main` before claiming and immediately after any remote TODO change.
- Complete and push each finished slice before starting another slice.
- Read relevant local reference repositories before implementation.
- Do not vendor, translate, or copy external source code.
- Do not implement a proxy as a placeholder for a professional module.
- Do not add broad placeholder files merely to increase code size. A missing
  professional capability should stay unchecked until its equations, validation
  cases, limits, and task behavior are implemented.
- If a reference library is outdated, document why and implement a smaller,
  clearer ChemWorld-local API with explicit units and validation boundaries.
- A slice is done only when code, tests, model card, docs, reference-reading
  note, validation examples, and task integration are all present.

## Slice Template

Each new item must use this structure before implementation starts:

```text
ID:
Owner:
Status:
Reference targets:
Equations or algorithms:
Data/provenance requirement:
Validation cases:
Failure modes:
Code areas:
Benchmark/task integration:
Exit criteria:
Last push:
```

## Active Deepening Work Board

| ID | Owner | Status | Reference targets | Equations or algorithms | Data/provenance requirement | Validation cases | Failure modes | Code areas | Benchmark/task integration | Exit criteria | Last push |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DEEP-D6A | whilesunny | Done | Cantera constant-volume/constant-pressure reactor energy equations, IDAES control-volume energy-balance docs, existing ChemWorld reactor and thermochemistry kernels | dynamic batch material balance, reaction enthalpy heat release, jacket heat transfer, variable-volume sampling loss, event-driven campaign reset policy | reuse local NASA7 species thermochemistry and model-card provenance; no copied reference code | adiabatic temperature rise, cooled reactor energy ledger, sampling mass loss, replay-safe event handling | negative volume/amount, impossible heat capacity, missing thermochemistry, solver nonconvergence, unsafe temperature runaway | `src/chemworld/physchem/reactors.py`, `src/chemworld/physchem/thermochemistry.py`, `tests/test_reactor_models.py`, docs | dynamic batch task kernels expose heat-release/jacket/sampling terms without proxy labels through public reactor API and model cards | code, tests, model card, docs, reference-reading note, validation examples, task-facing public API | this commit |
| DEEP-D5D | whilesunny | Done | Cantera reactor sensitivity interfaces, Cantera finite-difference Jacobian/adjoint notes, RMG/Arkane perturbation sensitivity reports, existing ChemWorld reaction-network perturbation API | finite-difference kinetic parameter sensitivities, normalized local response coefficients, uncertainty propagation summary, explanation-task ranking hooks | deterministic local perturbations only; no copied reference code; report parameter units and perturbation basis | irreversible first-order analytical sensitivity, reversible equilibrium response sanity check, zero-baseline handling, ranked explanation report | invalid perturbation size, missing parameter, nonpositive baseline observable, solver failure, unsupported parameter type | `src/chemworld/physchem/reaction_network.py`, `tests/test_reaction_network.py`, docs | explanation and mechanism-learning tasks can expose ranked sensitive reactions without proxy labels through public `ReactionSensitivityReport` API | code, tests, model card/docs, reference-reading note, validation examples | this commit |
| DEEP-D2A | whilesunny | Done | `chemicals` vapor-pressure families, `thermo` vapor-pressure method governance, existing ChemWorld curated property correlations | Antoine and Wagner/DIPPR vapor-pressure families, analytic temperature derivatives, validity-domain enforcement, sublimation extension where caller-supplied coefficients exist | curated coefficients with provenance and declared units; no copied reference code or bulk data vendoring | Antoine water analytical derivative, DIPPR derivative finite-difference check, sublimation-pressure report API, invalid temperature hard-fail/warning policy, monotonic pressure sanity cases | unsupported component, missing coefficient set, invalid temperature unit/range, Antoine singularity, Wagner critical-temperature boundary, derivative outside validity range | `src/chemworld/physchem/properties.py`, `src/chemworld/physchem/__init__.py`, `tests/test_physchem_properties.py`, docs | flash/distillation/safety tasks can request vapor pressure with explicit method, derivative, range status, and model-card provenance through public `VaporPressureReport` API | code, tests, model card/docs, reference-reading note, validation examples | this commit |
| DEEP-D2B | whilesunny | Done | `chemicals` heat-capacity/DIPPR families, `thermo` heat-capacity objects and property-package enthalpy conventions, existing ChemWorld Cp polynomial and reactor energy-balance users | phase-tagged Cp correlations, sensible enthalpy with reference state, latent heat across phase transitions, enthalpy ledger report for reactor/flash heat-duty integration | curated/local coefficients only; explicit units, phase labels, reference temperature, and no vendored third-party tables | ideal-gas Cp integral regression, liquid/solid Cp integral checks, latent heat sign convention, reference-state zero check, reactor-style mixture enthalpy ledger | missing phase Cp, invalid reference state, negative heat capacity, invalid phase transition, out-of-range hard-fail, unit mismatch | `src/chemworld/physchem/properties.py`, `src/chemworld/physchem/__init__.py`, `tests/test_physchem_properties.py`, reactor/separation docs | reactor energy balances and flash/distillation heat duties can consume phase-aware sensible/latent enthalpy reports with provenance instead of ad hoc heat numbers | code, tests, model card/docs, reference-reading note, validation examples, and public API exports are complete | this commit |
| DEEP-D2C | whilesunny | Done | `chemicals.volume`, `chemicals.virial`, `thermo.volume`, existing ChemWorld density and EOS users | liquid Rackett-style molar volume, ideal-gas molar volume report, second-virial gas hook, density/molar-volume conversion, mixture specific-volume ledger, compressibility warning report | local coefficients only; explicit critical constants/Zc provenance, molecular weight units, no vendored property tables | Rackett liquid-volume sanity case, ideal-gas density round-trip, virial compressibility root check, mixture density closure, invalid critical constants and negative density failures | missing molecular weight, invalid Tc/Pc/Zc, T >= Tc for Rackett liquid, nonpositive pressure/temperature, negative virial root, mixture fraction mismatch, out-of-range hard-fail | `src/chemworld/physchem/properties.py`, `src/chemworld/physchem/__init__.py`, `tests/test_physchem_properties.py`, docs | flash/distillation/separation tasks can request density and molar volume with explicit validity/compressibility status instead of unlabeled density proxies | claim pushed before implementation; code, tests, model card/docs, reference-reading note, validation examples | pushed after gates |
| DEEP-D2D | whilesunny | Claimed | `chemicals.viscosity`, `chemicals.thermal_conductivity`, `chemicals.diffusion`, `thermo` transport-property method governance, existing ChemWorld transport users | liquid Andrade/Arrhenius viscosity report, gas Sutherland viscosity report, thermal-conductivity report, Wilke-style gas mixture viscosity, log/linear liquid mixture rules, Fuller-style gas diffusivity estimate with validity and uncertainty flags | caller-supplied local coefficients only; explicit temperature, pressure, molecular weight, diffusion-volume, and composition units; no vendored property tables | water Andrade sanity case, gas Sutherland monotonicity, mixture-viscosity closure, conductivity positivity and validity policy, gas diffusivity pressure/temperature scaling, invalid coefficient and composition failures | missing coefficients, invalid temperature/pressure, nonpositive viscosity/conductivity/diffusivity, composition mismatch, unsupported phase, out-of-range hard-fail, missing molecular weight for Wilke-style mixing | `src/chemworld/physchem/properties.py`, `src/chemworld/physchem/transport.py`, `src/chemworld/physchem/__init__.py`, `tests/test_physchem_properties.py`, docs | reactor, heat-transfer, distillation, separation, and instrument tasks can request transport reports with explicit units, method family, validity, and uncertainty instead of unlabeled constants | claim pushed before implementation; code, tests, model card/docs, reference-reading note, validation examples | pending push |

## Module Deepening Map

### D1 Component Data And Units

- [ ] `DEEP-D1A` component identity registry:
  aliases, CAS/InChI-like placeholders where licensing permits, formula,
  charge, molecular weight, provenance, and JSON round-trip.
- [ ] `DEEP-D1B` unit-dimension checker:
  canonical dimensions for amount, mass, volume, temperature, pressure, energy,
  power, viscosity, diffusivity, conductivity, and instrument response.
- [ ] `DEEP-D1C` data conflict policy:
  deterministic source priority, uncertainty fields, warning vs hard-fail mode,
  and dataset-card provenance.

### D2 Property Correlations

- [x] `DEEP-D2A` vapor-pressure families:
  Antoine, Wagner/DIPPR, sublimation where relevant, derivative checks, and
  validity-domain enforcement.
- [x] `DEEP-D2B` heat-capacity and enthalpy package:
  ideal gas, liquid, solid, latent heat, reference-state management, and reactor
  energy-balance integration.
- [x] `DEEP-D2C` density and molar-volume package:
  liquid Rackett-style, ideal/virial gas hooks, mixture density, and explicit
  compressibility warnings.
- [ ] `DEEP-D2D` transport-property package:
  viscosity, thermal conductivity, and diffusivity with uncertainty and
  calibration cases.

### D3 EOS And Flash

- [ ] `DEEP-D3A` volume-translated cubic EOS and root governance:
  volume translation, stable-root policy diagnostics, binary-parameter
  provenance, and regression cases beyond the PRO-P3A PR/SRK residual slice.
- [ ] `DEEP-D3B` pure-fluid saturation solver:
  saturation pressure/temperature solve, critical-region warnings, and
  reference-backend comparisons.
- [ ] `DEEP-D3C` mixture bubble/dew flash:
  Rachford-Rice solve, K-value initialization, nonconvergence diagnostics, and
  task-level phase observations.
- [ ] `DEEP-D3D` nonideal EOS/activity bridge:
  gamma-phi VLE, azeotrope detection hooks, and public/private scenario
  parameter governance.

### D4 Phase Equilibrium And Electrolytes

- [ ] `DEEP-D4A` UNIQUAC slice:
  explicit structural parameters, binary interaction parameters, validation
  cases, and failure modes.
- [ ] `DEEP-D4B` LLE phase-split solver:
  tangent-plane-distance heuristic, initialization policy, mass-balance checks,
  and extraction-task integration.
- [ ] `DEEP-D4C` aqueous acid-base equilibrium:
  charge balance, activity simplifications, pH observation kernel, and
  precipitation hooks.
- [ ] `DEEP-D4D` Gibbs-minimization toy solver:
  small stoichiometric equilibrium examples with convexity and constraint
  diagnostics.

### D5 Reaction Thermochemistry And Kinetics

- [ ] `DEEP-D5A` thermochemistry-coupled reversibility:
  equilibrium constants from standard-state Gibbs energy, detailed balance, and
  reactor ODE integration.
- [ ] `DEEP-D5B` pressure-dependent and falloff kinetics:
  Troe/Lindemann-style compact slice, third-body efficiencies, and validation
  cases.
- [ ] `DEEP-D5C` mechanism schema:
  species, reactions, stoichiometry, rate laws, thermochemistry, and JSON
  manifests for benchmark scenarios.
- [x] `DEEP-D5D` sensitivity analysis:
  local kinetic sensitivities, uncertainty propagation, and explanation-task
  scoring hooks.

### D6 Reactors And Process Dynamics

- [x] `DEEP-D6A` dynamic batch reactor:
  heat release, jacket control, variable volume, sampling losses, and
  event-driven campaign reset policy.
- [ ] `DEEP-D6B` CSTR dynamics:
  dynamic mass/energy balance, residence time, stability, start-up/shutdown,
  and multiple steady-state tasks.
- [ ] `DEEP-D6C` PFR/plug-flow slice:
  axial integration, pressure drop coupling, heat-transfer boundary conditions,
  and validation cases.
- [ ] `DEEP-D6D` solver backend interface:
  deterministic tolerances, event handling, failure diagnostics, and replay
  verification.

### D7 Separations And Unit Operations

- [ ] `DEEP-D7A` rigorous flash unit:
  material and energy balance, vapor-liquid split, enthalpy duty, and
  nonideal-property hooks.
- [ ] `DEEP-D7B` distillation sizing:
  Fenske-Underwood-Gilliland shortcut, tray/stage accounting, reflux ratio, and
  pressure-profile warnings.
- [ ] `DEEP-D7C` extraction unit:
  distribution coefficients from activity/partition model, phase entrainment,
  wash sequence, and recovery/purity trade-off metrics.
- [ ] `DEEP-D7D` crystallization unit:
  solubility curve, supersaturation, nucleation/growth compact model, impurity
  occlusion, and crystal-size distribution metadata.

### D8 Transport, Equipment, And Safety

- [ ] `DEEP-D8A` phase-change and equipment heat transfer:
  boiling/condensation warning models, jacket/coil/shell-side correction
  factors, dynamic fouling evolution, and energy-ledger validation beyond the
  completed PRO-P8A single-phase Nusselt/e-NTU slice.
- [ ] `DEEP-D8B` two-phase pressure drop:
  replace homogeneous proxy with a documented correlation slice and validity
  limits.
- [ ] `DEEP-D8C` relief and safety envelope:
  pressure/temperature hazard envelopes, runaway indicators, and explicit
  safety-cost integration.
- [ ] `DEEP-D8D` equipment cards:
  vessel, pump, mixer, condenser, heat exchanger, and column specs with
  operating constraints.

### D9 Instruments And Spectroscopy

- [ ] `DEEP-D9A` empirical HPLC/GC method sensitivity:
  retention-index examples, temperature/mobile-phase sensitivity, detector
  response calibration, and asymmetric peak flags.
- [ ] `DEEP-D9B` IR slice:
  functional-group bands, broadening, interference, calibration examples, and
  model card.
- [ ] `DEEP-D9C` NMR slice:
  chemical shift anchors, multiplicity/coupling metadata, integration, solvent
  reference, and failure modes.
- [ ] `DEEP-D9D` MS slice:
  simple fragmentation metadata, isotope envelopes for small formulas, and
  detector response uncertainty.

### D10 Benchmark And Dataset Integration

- [ ] `DEEP-D10A` model-maturity gate:
  benchmark results cannot mix proxy and professional kernels without explicit
  task flags and result annotations.
- [ ] `DEEP-D10B` dataset export hardening:
  schema-versioned JSONL/Parquet, dataset cards, privacy status, and replay
  verification summary.
- [ ] `DEEP-D10C` reference-baseline reports:
  task-specific official tables, seed confidence intervals, and public/private
  generalization gaps.
- [ ] `DEEP-D10D` solver/provenance manifest:
  commit hash, dependency lock, optional backend versions, numerical tolerances,
  and hidden-scenario salt policy.

### D11 Electrochemistry And Electrode Processes

- [ ] `DEEP-D11A` ohmic-drop and electrolyte-resistance slice:
  solution resistance, uncompensated resistance, measured vs interfacial
  potential, energy-loss accounting, and potential-control failure modes.
- [ ] `DEEP-D11B` mass-transfer limiting-current slice:
  diffusion-layer approximation, limiting current, concentration depletion,
  current-efficiency loss, and validation cases with analytical plateaus.
- [ ] `DEEP-D11C` potentiostatic and galvanostatic controllers:
  controller semantics, current/potential clipping, ramp/hold recipes,
  operation logs, and replay-verification contracts.
- [ ] `DEEP-D11D` double-layer and capacitive-current slice:
  RC transient response, non-Faradaic current, startup artifacts, and instrument
  observations for current traces.
- [ ] `DEEP-D11E` electrochemical scenario cards:
  redox couple metadata, electrode area, electrolyte window, side-reaction
  thresholds, and public/private hidden-parameter generation.

## Activation Checklist

- [x] The first twelve implementation queue slices in `TODO_PROFESSIONAL.md`
      are complete and pushed.
- [x] Broad P1-P12 module checklists still contain open items; those open items
      are intentionally tracked as the deepening roadmap below.
- [x] `docs/professional_deepening_todo.md` is updated from this file.
- [x] `TODO_PROFESSIONAL.md` points active developers here.
- [x] The first deepening slice is claimed and pushed before implementation.
