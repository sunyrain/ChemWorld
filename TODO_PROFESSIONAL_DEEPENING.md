# ChemWorld Professional Deepening TODO

This file is the next professional roadmap after the first twelve items in
`TODO_PROFESSIONAL.md` are complete. It is intentionally more detailed than a
normal backlog. ChemWorld should mature by implementing narrowly scoped,
auditable physical-chemistry modules one slice at a time, not by filling the
world with proxies.

Status: planned. Do not mark this roadmap active until the first twelve
professional implementation slices in `TODO_PROFESSIONAL.md` are done and
pushed.

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

- [ ] `DEEP-D2A` vapor-pressure families:
  Antoine, Wagner/DIPPR, sublimation where relevant, derivative checks, and
  validity-domain enforcement.
- [ ] `DEEP-D2B` heat-capacity and enthalpy package:
  ideal gas, liquid, solid, latent heat, reference-state management, and reactor
  energy-balance integration.
- [ ] `DEEP-D2C` density and molar-volume package:
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
- [ ] `DEEP-D5D` sensitivity analysis:
  local kinetic sensitivities, uncertainty propagation, and explanation-task
  scoring hooks.

### D6 Reactors And Process Dynamics

- [ ] `DEEP-D6A` dynamic batch reactor:
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

## Activation Checklist

- [ ] The first twelve items in `TODO_PROFESSIONAL.md` are complete and pushed.
- [ ] `docs/professional_deepening_todo.md` is updated from this file.
- [ ] `TODO_PROFESSIONAL.md` points active developers here.
- [ ] The first deepening slice is claimed and pushed before implementation.
