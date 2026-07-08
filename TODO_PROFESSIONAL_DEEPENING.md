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
| DEEP-D2D | whilesunny | Done | `chemicals.viscosity`, `chemicals.thermal_conductivity`, IDAES Fuller/Wilke transport-property examples, `thermo` transport-property method governance, existing ChemWorld transport users | liquid Andrade/Arrhenius viscosity report, gas Sutherland viscosity report, thermal-conductivity report, DIPPR9B gas conductivity, Wilke gas-mixture viscosity, DIPPR9H liquid-mixture conductivity, Fuller gas diffusivity estimate, thermal diffusivity report | caller-supplied local coefficients only; explicit temperature, pressure, molecular weight, diffusion-volume, composition, conductivity, and diffusivity units; no vendored property tables | Andrade/Sutherland report tests, DIPPR9B CO reference example, Wilke reference example, DIPPR9H reference example, Fuller pressure/temperature scaling, thermal diffusivity definition, invalid coefficient and composition failures | missing coefficients, invalid temperature/pressure, nonpositive viscosity/conductivity/diffusivity, composition mismatch, unsupported phase, out-of-range hard-fail, missing molecular weight for Wilke-style mixing | `src/chemworld/physchem/properties.py`, `src/chemworld/foundation/units.py`, `src/chemworld/physchem/__init__.py`, `tests/test_physchem_properties.py`, docs | reactor, heat-transfer, distillation, separation, and instrument tasks can request transport reports with explicit units, method family, validity, and uncertainty instead of unlabeled constants | claim pushed before implementation; code, tests, model card/docs, reference-reading note, validation examples | pushed after gates |
| DEEP-D3A | whilesunny | Done | `thermo.eos`, `phasepy` volume-translation/root solver notes, `thermopack` volume-shift hooks, existing ChemWorld PR/SRK residual EOS core | volume translation by component or mixture shift, translated molar volume reporting, root governance diagnostics, stable-root policy evidence, binary-interaction provenance records, regression cases beyond current residual slice | local EOS equations only; explicit units for translation shifts and binary parameters; source/provenance metadata for `k_ij` and volume shifts; no copied reference code or data tables | pure-liquid volume translation sanity case, vapor root unchanged warning, stable-root diagnostic ranking, binary-interaction provenance round trip, invalid translation and root-policy failures | nonpositive pressure/temperature, invalid root phase, negative translated volume, missing binary parameter provenance, inconsistent composition, unsupported EOS family | `src/chemworld/physchem/eos.py`, `src/chemworld/physchem/__init__.py`, `tests/test_eos.py`, docs | flash/distillation/generalization tasks can expose EOS volume/root provenance without unlabeled dense-fluid corrections | code, tests, model card/docs, reference-reading note, validation examples, public API exports, and local gates are complete | pushed after gates |
| DEEP-D7B | whilesunny | Done | IDAES distillation/unit-model docs, `thermo` flash/property-package workflows, existing ChemWorld shortcut distillation and separation score code | Fenske minimum stages, Underwood minimum reflux for saturated-liquid binary feed, Gilliland/Eduljee stage estimate, feed-stage estimate, pressure-profile warning and tray/stage accounting | local equations only; explicit relative-volatility, feed composition, distillate/bottoms compositions, reflux ratio, pressure, and provenance metadata; no copied reference code or data tables | binary benzene/toluene-style sanity case, reflux-ratio monotonicity, infeasible split failure, reflux below minimum failure, pressure-profile warning, model-card validation | invalid composition, alpha <= 1, distillate/bottoms purity impossible, reflux ratio <= Rmin, nonpositive pressure, feed composition outside products, missing provenance | `src/chemworld/physchem/separations.py`, `src/chemworld/physchem/__init__.py`, `tests/test_separations.py`, docs | distillation and purification tasks can expose stage/reflux/tray sizing with declared physical assumptions instead of unlabeled downstream proxies | code, tests, model card/docs, reference-reading note, validation examples, public API exports, and local gates are complete | pushed after gates |
| DEEP-R1A | whilesunny | Done | Gymnasium action-language patterns, ChemWorld Runtime v2 operation registry, LLM/tool-agent recipe validation needs | operation kind taxonomy, primitive/domain/macro/terminal operation contracts, macro recipe expansion into executable operations | no copied plugin code; contracts stay JSON-friendly and task-policy aware | operation contract serialization, macro wash/dry/concentrate expansion, schema validation after expansion, task-policy validation examples | unsupported macro, macro expansion with invalid payload, macro bypassing task disallowed operation, empty compiled sequence | `src/chemworld/world/operations.py`, `src/chemworld/world/recipes.py`, tests/docs | LLM and student recipe tools can propose high-level process macros while the runtime still executes auditable primitive/domain steps | operation kind contracts, macro expansion, task-aware recipe validation, docs, and local gates are complete | this commit |
| DEEP-R1B | whilesunny | Done | Gymnasium environment cards, ChemWorld Runtime v2 service split, IDAES-style unit-service boundaries | typed domain-service registry, operation-to-service map, service metadata in runtime/task info, service id in transaction events | no external plugin system; service contracts are JSON-friendly and reflect focused runtime services | operation coverage, service metadata serialization, runtime task_info exposure, world-event service id audit | missing operation mapping, duplicate service operation ownership, stale service contract after adding an operation | `src/chemworld/runtime/domain_services.py`, `src/chemworld/runtime/engine.py`, tests/docs | agents and auditors can see which physics service handled each operation without reading internal Python objects | code, tests, docs, public runtime metadata, and local gates are complete | this commit |
| DEEP-R1C | whilesunny | Done | Gymnasium environment cards, Runtime v2 profile contracts, focused service registry, Safety-Gymnasium-style task cost/safety contract | task runtime profile declares required domain services, validates operation/service/capability coverage at runtime startup, and serializes profile service requirements | no external plugin system; no broad plugin loader; validation is task-scoped rather than globally requiring every possible operation | profile serialization, missing service operation failure, missing capability failure, runtime task_info service requirement audit | stale service registry after adding operation, task allows operation whose service is absent, profile capability mismatch, over-broad global validation | `src/chemworld/runtime/kernels.py`, `src/chemworld/runtime/domain_services.py`, `src/chemworld/runtime/engine.py`, tests/docs | task cards and agents can inspect not only allowed operations but also the focused domain services and capabilities needed to execute them | code, tests, docs, runtime metadata, and local gates are complete | this commit |
| DEEP-D9B | whilesunny | Done | public organic spectroscopy band tables, chemicals developer notes on spectral data sources, existing ChemWorld signal synthesis | IR functional-group band catalog, formula/role-based feature assignment, Gaussian/Lorentzian broadening, band interference warnings, calibration examples, and model-card validation | local curated functional-group bands only; explicit wavenumber units and provenance; no copied empirical spectra or database tables | carbonyl/OH/CH/fingerprint band assignment, broad OH width, overlapping-band warning, transmittance bounds, invalid band failure, model-card validation | nonpositive wavenumber/width, unknown feature group, invalid transmittance mode, missing formula, overlapping unresolved bands | `src/chemworld/physchem/spectroscopy.py`, `src/chemworld/physchem/spectroscopy_cards.py`, `tests/test_spectroscopy.py`, docs | final-assay and IR raw-signal packets expose interpretable functional-group bands instead of generic role-only peaks | code, tests, docs, model card, public API exports, and local gates are complete | this commit |
| DEEP-D1A | liyijun | Claimed | `chemicals` identifier registries, `thermo` chemical constants/aliases, CoolProp fluid identifiers, existing ChemWorld component specs | canonical component identity records, alias/CAS/InChIKey-style identifiers where licensing permits, JSON round-trip and duplicate-identity checks | curated/local metadata only; explicit provenance per identity field; no copied identifier tables | alias and compact-CAS resolution, InChIKey-style lookup, JSON round-trip, duplicate identifier hard-fail, curated component provenance | unsupported identifier type, invalid CAS checksum, duplicate alias collision, missing provenance, molecular-weight mismatch | `src/chemworld/physchem/specs.py`, `src/chemworld/physchem/curated_properties.py`, `tests/test_physchem_core.py`, docs | task/property registries resolve components by stable identity instead of ambiguous display names | code, tests, docs/model-card notes, reference-reading note, validation examples, public API export if needed | claim commit |
| DEEP-D1B | liyijun | Claimed | IDAES unit metadata conventions, Cantera YAML unit declarations, existing ChemWorld `foundation.units` and property-correlation contracts | canonical dimension records for physical quantities, unit compatibility checks, JSON-friendly supported-unit manifest | ChemWorld-local unit table with explicit dimensions and canonical SI targets; no third-party unit registry dependency | amount/mass/volume/temperature/pressure/energy/power/viscosity/diffusivity/conductivity/instrument-response dimension checks | unsupported unit, mismatched dimension conversion, missing required dimension, ambiguous instrument response unit | `src/chemworld/foundation/units.py`, `src/chemworld/physchem/specs.py`, `tests/test_foundation.py`, `tests/test_physchem_core.py`, docs | benchmark/state/property specs reject unit-dimension mistakes before kernels run | code, tests, docs/model-card notes, reference-reading note, validation examples | claim commit |
| DEEP-D1C | liyijun | Claimed | `chemicals` and `thermo` source-priority patterns, CoolProp constants API, existing ChemWorld conflict policy | deterministic source priority, uncertainty-aware conflict resolution, warning versus hard-fail reports, dataset-card provenance | candidate field records carry source, value, unit, uncertainty, and notes; no bulk data vendoring | priority winner, tie/uncertainty warning, hard-fail mismatch, unit mismatch, JSON round-trip of resolution reports | missing source priority, incompatible units, unresolved tie, value outside uncertainty, silent overwrite attempt | `src/chemworld/physchem/specs.py`, `src/chemworld/physchem/curated_properties.py`, `tests/test_physchem_core.py`, docs | future curated component/property merges produce auditable conflict reports instead of hidden overwrites | code, tests, docs/model-card notes, reference-reading note, validation examples | claim commit |

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
- [x] `DEEP-D2D` transport-property package:
  viscosity, thermal conductivity, and diffusivity with uncertainty and
  calibration cases.

### D3 EOS And Flash

- [x] `DEEP-D3A` volume-translated cubic EOS and root governance:
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
- [x] `DEEP-D7B` distillation sizing:
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
- [x] `DEEP-D9B` IR slice:
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
