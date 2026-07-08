# Code Review Audit

Date: 2026-07-09

Scope: completed ChemWorld professional/deepening slices, with emphasis on
large files, redundant metadata, and reviewability risks.

## Findings

### High Priority: Remaining Large PhysChem Modules Mix Multiple Responsibilities

The largest remaining files still combine public specs, numerical kernels,
validation helpers, and export lists. This makes review harder and increases
merge-conflict risk during two-person development.

Largest current source files after this cleanup:

| File | Approximate role | Follow-up split target |
| --- | --- | --- |
| `src/chemworld/physchem/reaction_network.py` | network object, batch integration, detailed balance, sensitivities, mechanism loading, and public facade wrappers | split integration core, thermochemical coupling, sensitivity, and loaders |
| `src/chemworld/physchem/reaction_network_specs.py` | species/rate-law/reaction specs, reaction-equation parser, mechanism dict helpers | keep schema/parser layer separate from ODE integration and rate-law evaluation |
| `src/chemworld/physchem/reaction_rate_laws.py` | rate-law constants, mass-action/Arrhenius/reversible-rate evaluation, parameter validation, reaction lookup helpers | keep kinetic formula evaluation separate from ODE integration, thermochemical reports, and file loading |
| `src/chemworld/physchem/reaction_reference_cases.py` | analytical ODE reference cases, Cantera-comparable fixtures, and reference-case evaluation | keep validation fixtures separate from network integration, sensitivity, and mechanism loading |
| `src/chemworld/physchem/equilibrium_chemistry.py` | mass-action equilibrium, acid-base, precipitation, Gibbs minimization | split into mass-action, electrolyte/acid-base, precipitation, and Gibbs minimization helpers |
| `src/chemworld/physchem/eos.py` | cubic EOS specs, root solving, residuals, volume translation, provenance | split into EOS specs, cubic parameters, root policy, residual properties, volume translation, and provenance |
| `src/chemworld/physchem/spectroscopy.py` | calibration, chromatography, signal synthesis, feature heuristics | split into calibration, chromatography, signal synthesis, and feature libraries |
| `src/chemworld/runtime/domain_services.py` | lightweight operation composition surface with service delegation, constitution checks, and operation-record assembly | keep thin and do not add process-specific formulas back into this layer |
| `src/chemworld/runtime/crystallization_services.py` | seed addition, typed crystallizer seed-equipment status, cooling crystallization, typed solid/mother-liquor output phases, crystal purity/recovery metadata, and crystal filtration ledger updates | keep separate from mixed operation services and later bind solubility/crystal-size models more directly to mechanism cards |
| `src/chemworld/runtime/distillation_services.py` | shortcut VLE distillation, typed distillate/bottoms output phases, distillate purity/recovery metadata, heat-duty/cost/risk ledgers, and fraction collection | keep separate from mixed operation services and later bind VLE/component properties more directly to mechanism cards |
| `src/chemworld/runtime/electrochemical_services.py` | potential/current setup, Nernst/Butler-Volmer electrolysis calls, faradaic conversion, electrical work, and electrochemical metadata | keep separate from mixed operation services and later bind electrode/reaction specs more directly to mechanism cards |
| `src/chemworld/runtime/flow_services.py` | flow-rate setup, residence-time reaction advancement, flow conversion metadata, and flow campaign ledger updates | keep separate from mixed operation services and later bind reactor geometry/residence-time distributions more directly to mechanism cards |
| `src/chemworld/runtime/instrument_cost_services.py` | measurement cost, destructive sample consumption, and typed instrument equipment status | keep separate from observation generation and operation-record logging |
| `src/chemworld/runtime/reaction_thermal_services.py` | reaction ODE advancement, heat/wait integration, energy ledgers, and pressure/risk projection | keep separate from mixed operation services and later bind integration choices more directly to mechanism cards |
| `src/chemworld/runtime/phase_separation_services.py` | phase-ledger normalization, liquid-liquid partitioning, extraction, settling, washing, drying, concentrating, transfer, and downstream truth metadata | keep separate from crystallization/distillation and later migrate primary phase state from metadata into typed ledgers |
| `src/chemworld/runtime/primitive_services.py` | reagent, solvent, and catalyst addition, sampling, quench, evaporation, and invalid-action penalty updates | keep separate from composition and later bind primitive material additions more directly to typed ledgers |
| `src/chemworld/runtime/observation_services.py` | observation truth, noisy instrument signals, processed estimates, and scoring | keep separate from state-changing services and later bind observation/score specs more directly to mechanism/task cards |
| `src/chemworld/runtime/record_services.py` | operation-record assembly, constitution summaries, measurement cost/sample fields, and state-delta summaries | keep separate from state-changing services and later bind record schemas more directly to trajectory schema generation |

### Medium Priority: Model Cards Are Better As Metadata Modules

Many modules contain long `*_model_cards()` functions. These are valuable but
they are mostly metadata. Keeping them inside numerical kernels makes diffs
noisy whenever docs/provenance changes.

Action completed in this pass:

- moved all remaining PhysChem `*_model_cards()` functions into dedicated
  `*_cards.py` modules;
- moved card-only provenance constants with their card modules where needed;
- kept the public facade `chemworld.physchem` exporting the same model-card
  functions;
- kept numerical kernels focused on calculations, reports, and runtime data
  structures;
- did not change numerical behavior.

The new card modules are:

- `curated_property_cards.py`
- `electrochemistry_cards.py`
- `eos_cards.py`
- `equilibrium_cards.py`
- `equilibrium_chemistry_cards.py`
- `property_cards.py`
- `reaction_network_cards.py`
- `reactor_cards.py`
- `separation_cards.py`
- `spectroscopy_cards.py`
- `thermochemistry_cards.py`
- `transport_cards.py`

Recommended next mechanical cleanup:

1. Continue splitting `reaction_network.py` by integration core,
   thermochemical-coupling, sensitivity, and loader responsibilities.

### Medium Priority: Property Module Split Is Complete

`src/chemworld/physchem/properties.py` is now a thin facade. Property logic is
split by family:

- `property_reports.py`: shared constants, report contract, phase/fraction
  validation helpers;
- `property_equations.py`: supported correlation equations, validity checks,
  and equation derivatives;
- `property_packages.py`: component-level convenience wrapper;
- `vapor_pressure.py`: vapor/sublimation pressure reports and derivatives;
- `enthalpy.py`: heat-capacity, phase-transition, and mixture enthalpy reports;
- `volume_properties.py`: molar volume, density, and volume-mixture ledgers;
- `transport_properties.py`: viscosity, conductivity, diffusivity, and
  transport ledgers;
- `hazard_properties.py`: property-derived screening hazard proxies;
- `properties.py`: public aggregation facade.

This split reduced `properties.py` from a multi-thousand-line numerical module
to a small aggregation surface without changing public imports or numerical
behavior.

### Medium Priority: Reactor Module Split Is Complete

`src/chemworld/physchem/reactors.py` is now a thin facade. Reactor logic is
split by family and responsibility:

- `reactor_shared.py`: heat-transfer specs, jacket programs, feed specs,
  sampling specs, reactor states, results, and common validation;
- `reactor_solvers.py`: ODE solving, integration-result assembly, heat ledgers,
  material-balance helpers, and shared vector conversion;
- `batch_reactors.py`: batch and dynamic/event-driven batch models;
- `semibatch_reactors.py`: semi-batch model with explicit feed ledgers;
- `cstr_reactors.py`: dynamic and steady-state CSTR model;
- `pfr_reactors.py`: plug-flow reactor model;
- `cstr_multiplicity.py`: exothermic CSTR multiplicity reference case and
  root/stability solver;
- `reactors.py`: public aggregation facade.

This split reduced `reactors.py` from a broad numerical module to a small
aggregation surface while preserving public imports and numerical behavior.

### Medium Priority: Runtime V2 Is In Place, Domain Services Remain Broad

`ChemWorldEnv` now delegates operation execution to `chemworld.runtime`.
The active runtime path contains `ChemWorldRuntime`,
`OperationKernelRegistry`, `TaskRuntimeProfile`, `TransactionManager`,
`CompiledMechanism`, and typed state ledgers. The old
`chemworld.core.batch_reactor` runtime center has been removed from the running
path.

`src/chemworld/runtime/domain_services.py` is now a lightweight composition
surface rather than the physical runtime center. Observation/scoring,
operation-record assembly, reaction/thermal advancement, phase-ledger and
extraction-style separation operations, crystallization, distillation, flow,
electrochemical operation logic, measurement cost / destructive sampling, and
primitive material handling have been extracted to focused service modules.

Current hardening added a mechanism-aware species-role boundary. Runtime
services now resolve reactants, targets, impurities, catalyst species,
byproduct signals, and degradation markers through `MechanismSpeciesView`
rather than reading fixed species names throughout the service code. The
remaining legacy names are isolated as world-level fallback role bindings for
older benchmark mechanisms and tests.

Recommended follow-up:

- keep `domain_services.py` thin and do not add process-specific formulas back
  into the composition layer;
- keep operation kernels as small command handlers;
- continue moving mechanism-specific scoring and observation mapping into
  compiled mechanism cards;
- continue strengthening ledger-level replay beyond the current transaction
  metadata checks.
- continue shrinking the legacy fallback surface by letting reaction,
  separation, spectroscopy, and score specs carry all species bindings.

Current hardening also adds a golden-characterization test layer for the active
Runtime v2 path. Each formal task now has a scripted final-assay trajectory that
locks the mechanism id, final-assay score snapshot, campaign versus
single-experiment termination semantics, operation-kernel metadata, transaction
status, world-event payload, and affected-ledger signals.

The architecture test suite now also enforces the active Runtime v2 boundary:
`src/chemworld/envs` and `src/chemworld/runtime` must not import the removed
`chemworld.core.batch_reactor` runtime, and `ChemWorldEnv.step()` must delegate
process-operation dispatch to `runtime.apply_transaction()` instead of adding
inline branches for process operations.

The final Runtime v2 boundary audit also enforces that `LEGACY_*` species
fallback names are isolated to `runtime/species.py`. This is an intentional
temporary adapter for mechanisms whose initial state is still generated through
the older scalar-state shape. The next professional runtime slice is
`PRO-RUNTIME-A`: make scenario/mechanism initialization own species amounts
directly and then remove the `A/P/B/D/E` fallback constants from runtime species
resolution.

Replay verification now compares Runtime v2 transaction metadata in addition
to rewards and observations. The verifier rejects mechanism-hash drift,
operation-kernel metadata tampering, changed affected-ledger lists, altered
world events, modified state-patch summaries, transaction-status changes, and
state-delta summary drift.

### Low Priority: Facade Exports Are Large But Useful

`src/chemworld/physchem/__init__.py` is a large facade. It is not a correctness
risk, but merge conflicts are likely as new professional slices add exports.

Recommended follow-up:

- keep the facade for user ergonomics;
- consider grouped internal subfacades later, such as
  `chemworld.physchem.properties_api` and `chemworld.physchem.reactors_api`;
- avoid removing public names without a deliberate API decision.

## Cleanup Completed

- Extracted separation model-card metadata from the separation numerical kernel.
- Extracted the remaining PhysChem model-card metadata from numerical kernels.
- Added dedicated `*_cards.py` modules for property correlations, reactors,
  reaction networks, EOS, spectroscopy, transport, equilibrium, equilibrium
  chemistry, thermochemistry, electrochemistry, curated properties, and
  separations.
- Updated `chemworld.physchem.__init__` to import model-card functions directly
  from card modules.
- Preserved module-level model-card re-exports from the numerical kernels.
- Verified facade imports and model-card validation after the split.
- Split `properties.py` into property-family modules and kept
  `chemworld.physchem.properties` as a thin public facade.
- Verified property-specific tests and the full benchmark test suite after the
  split.
- Split `reactors.py` into reactor-family modules and kept
  `chemworld.physchem.reactors` as a thin public facade.
- Verified reactor-specific tests and the full benchmark test suite after the
  split.
- Introduced Runtime v2 with operation kernel registry, task runtime profiles,
  transaction manager, mechanism compiler, typed ledgers, and mechanism-hash
  trajectory metadata.
- Moved the former batch-reactor runtime implementation out of `core` and then
  split major state-changing process responsibilities into focused runtime
  services.
- Added `runtime/species.py` as the single species-role adapter between
  compiled mechanisms and the current semi-mechanistic domain services.
- Migrated reagent addition, catalyst addition, phase bookkeeping,
  electrochemical conversion, downstream truth values, flow conversion,
  distillation summaries, crystallization summaries, and observation truth
  scoring toward compiled-mechanism role mappings.
- Added regression tests using the `electrochemical_conversion` mechanism to
  verify non-`A/P/B/D/E` species can drive runtime services and observations.
- Added Runtime v2 golden-characterization tests covering all formal tasks with
  scripted final-assay trajectories, campaign/single-experiment semantics,
  operation-kernel metadata, transaction status, world events, affected ledgers,
  and final-assay score snapshots.
- Added architecture tests that enforce env/runtime import boundaries and keep
  concrete process-operation dispatch out of `ChemWorldEnv.step()`.
- Extended replay verification to check mechanism hash, kernel id/version,
  affected ledgers, world events, state-patch summaries, transaction status,
  rollback reason, and state-delta summaries with recursive tolerance-aware
  comparisons.
- Promoted Runtime v2 extraction phase bookkeeping from metadata to typed
  `PhaseLedger` records, added executable constitution checks for phase/vessel
  reverse indexes and metadata primary-state leakage, and synchronized
  destructive sampling/measurement with typed phase amounts.
- Promoted Runtime v2 flow and electrochemical setup from metadata keys to
  typed `EquipmentLedger` records, made flow/electrochemistry preconditions read
  equipment settings, and kept derived process metrics in metadata only.
- Extracted `ChemWorldObservationKernel` into
  `runtime/observation_services.py`, keeping noisy observations, raw signal
  assembly, processed estimates, uncertainty metadata, and observation scoring
  outside the state-changing domain-service module.
- Extracted `ChemWorldOperationRecorder` into `runtime/record_services.py`,
  keeping operation-record assembly, constitution summaries, measurement
  cost/sample fields, and state-delta summaries outside the state-changing
  domain-service module.
- Extracted `ChemWorldReactionThermalServices` into
  `runtime/reaction_thermal_services.py`, keeping heat/wait reaction
  integration, typed reactor stirring settings, energy-ledger updates, and pressure/risk
  projection outside the mixed domain-service module.
- Extracted `ChemWorldPhaseSeparationServices` into
  `runtime/phase_separation_services.py`, keeping phase-ledger normalization,
  partitioning, extraction, settling, phase selection, washing, drying,
  concentrating, transfer, and downstream truth metadata outside the mixed
  domain-service module.
- Extracted `ChemWorldElectrochemicalServices` into
  `runtime/electrochemical_services.py`, keeping potential/current setup,
  electrochemical mechanism binding, faradaic conversion, electrical-work
  ledgers, and electrochemical metadata outside the mixed domain-service
  module.
- Extracted `ChemWorldInstrumentCostServices` into
  `runtime/instrument_cost_services.py`, keeping measurement cost, destructive
  sample consumption, and typed instrument equipment status outside the mixed
  domain-service module.
- Promoted final-assay completion and timing out of runtime metadata into typed
  `instrument:final_assay` equipment status. Constitution preconditions now use
  typed instrument completion to block repeated final assays, and golden
  trajectories assert the old metadata keys do not reappear.
- Promoted crystallization seed status and seed mass out of runtime metadata
  into typed `crystallizer` equipment settings. Cooling crystallization now
  reads the typed seed configuration, and constitution/golden tests reject the
  old seed metadata keys.
- Promoted crystallized product and occluded impurity amounts out of runtime
  metadata into typed `solid` and `mother_liquor` phase records. Crystal
  filtration now reads the typed solid phase, while metadata retains only
  derived yield/purity/size summaries.
- Promoted distillate product and impurity amounts out of runtime metadata into
  typed `distillate` and `bottoms` phase records. Fraction collection now reads
  the typed distillate phase, while metadata retains only derived purity,
  recovery, and distillation-kernel summaries.
- Added a Runtime v2 final boundary audit that keeps the removed
  `chemworld.core.batch_reactor` runtime out of env/runtime imports and confines
  `LEGACY_*` species fallback bindings to `runtime/species.py`. The remaining
  follow-up is tracked as `PRO-RUNTIME-A` in `TODO_PROFESSIONAL.md`.
- Moved scenario initial-state generation onto compiled mechanism species,
  roles, and initial-amount policy. Non-fixed scenarios such as
  `electrochemical_conversion` and `reactive_distillation_lite` now reset with
  mechanism-owned species ledgers instead of fixed `A/P/B/D/E` state keys.
- Added a compiled reaction integration path for heat/wait-style advancement.
  Runtime reaction/thermal services now prefer compiled mechanism species,
  stoichiometry, rate-law evaluators, and reaction enthalpies; the old
  seven-slot ODE remains only as an explicit world-level reference fixture.
  Reagent charging also uses mechanism `initial_amount_policy`, so
  multi-reactant mechanisms such as reactive distillation add co-reactants in
  declared ratios.
- Quarantined the old fixed A/P/B/D/E seven-slot ODE in
  `world/reaction_reference.py`. The ordinary `world/reaction_kernel.py` now
  declares a compiled-mechanism runtime contract and no longer exports fixed
  species slots or the old reference integrator.
- Removed generic `LEGACY_*` species defaults and optional compiled-mechanism
  service constructors from env/runtime/eval paths. Runtime role resolution now
  requires a compiled mechanism; mechanisms with no catalyst species update
  catalyst equipment/cost without fabricating `Cat_active`. Golden final-assay
  scores were updated because the old `A`-specific metadata branch had counted
  `initial_A_mol` twice.
- Added compile-time mechanism role validation. All mechanisms still compile
  under the base library contract, while runtime task scenarios additionally
  require positive initial species, declared target species, impurity species,
  and role mappings that refer only to species present in the mechanism.
- Hardened Runtime v2 transaction consistency. Rollback transactions now append
  an explicit `rollback_penalty` patch, preserve the failed-candidate check
  names in a `transaction_rollback` event, and rebuild operation records from
  the final rollback state so `state_delta_summary`, returned state, patches,
  and event logs describe the same transaction outcome.
- Extracted `ChemWorldCrystallizationServices` into
  `runtime/crystallization_services.py`, keeping seed addition, cooling
  crystallization, crystal purity/recovery metadata, and crystal filtration
  outside the mixed domain-service module.
- Extracted `ChemWorldDistillationServices` into
  `runtime/distillation_services.py`, keeping shortcut VLE distillation,
  distillate purity/recovery metadata, heat-duty/cost/risk ledgers, and
  fraction collection outside the mixed domain-service module.
- Extracted `ChemWorldFlowServices` into `runtime/flow_services.py`, keeping
  flow-rate setup, residence-time reaction advancement, flow conversion
  metadata, and flow campaign ledger updates outside the mixed domain-service
  module.
- Extracted `ChemWorldPrimitiveOperationServices` into
  `runtime/primitive_services.py`, keeping reagent, solvent, and catalyst
  addition, sampling, quench, evaporation, and invalid-action penalty updates
  outside the composition layer.
- Promoted batch-reactor solvent, catalyst, and stirring configuration out of
  runtime metadata into typed `EquipmentLedger` settings. Reaction, thermal,
  electrochemical, and phase-partition services now read the typed reactor
  settings, and the constitution rejects these keys as primary metadata.
- Promoted phase-system readiness, settled status, and selected-phase state out
  of runtime metadata into typed `PhaseLedger` records. Constitution
  preconditions now read `PhaseRecord.settled/selected`, extraction,
  crystallization, and distillation outputs mark selected phases in typed
  ledgers, and golden trajectories assert these primary phase-status keys never
  reappear in state metadata.
- Extracted `reaction_network_specs.py` from `reaction_network.py`, keeping
  species/rate-law/reaction specs, reaction-equation parsing, and mechanism
  dict helpers outside the ODE integration and rate-law evaluation engine.
- Extracted `reaction_rate_laws.py` from `reaction_network.py`, keeping
  mass-action, Arrhenius, reversible Arrhenius, catalytic, deactivation,
  Langmuir-Hinshelwood, Michaelis-Menten, parameter validation, and reaction
  lookup helpers outside the network ODE/reference-case engine.
- Extracted `reaction_reference_cases.py` from `reaction_network.py`, keeping
  analytical first-order ODE cases, Cantera-comparable fixtures, and
  reference-case evaluation outside the network integration engine.

## Verification

Run these after every cleanup slice:

```bash
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m mypy src\chemworld
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m mkdocs build --strict
```

## Next Cleanup Order

1. Continue splitting `reaction_network.py` into integration core,
   thermochemistry coupling, sensitivities, and loaders.
2. Split `eos.py`, `spectroscopy.py`, and `equilibrium_chemistry.py` by
   algorithm family.
3. Keep `runtime/domain_services.py` thin while reducing legacy scalar-state
   adapter responsibilities in the focused runtime services.
