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
| `src/chemworld/physchem/reaction_network.py` | species/reaction specs, ODE cases, detailed balance, sensitivities, mechanism loading | split into mechanism specs, rate laws, integration/reference cases, thermochemical coupling, sensitivity, and loaders |
| `src/chemworld/physchem/equilibrium_chemistry.py` | mass-action equilibrium, acid-base, precipitation, Gibbs minimization | split into mass-action, electrolyte/acid-base, precipitation, and Gibbs minimization helpers |
| `src/chemworld/physchem/eos.py` | cubic EOS specs, root solving, residuals, volume translation, provenance | split into EOS specs, cubic parameters, root policy, residual properties, volume translation, and provenance |
| `src/chemworld/physchem/spectroscopy.py` | calibration, chromatography, signal synthesis, feature heuristics | split into calibration, chromatography, signal synthesis, and feature libraries |
| `src/chemworld/runtime/domain_services.py` | semi-mechanistic domain-service implementation used by Runtime v2 | split reaction, thermal, observation, separation, scoring, and operation-record assembly into narrower service modules |

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

1. Split `reaction_network.py` by mechanism-spec, rate-law, integration,
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

The broad file is now `src/chemworld/runtime/domain_services.py`. This is a
better boundary than a batch-reactor-centered runtime, but the file still mixes
reaction advancement, thermal updates, phase operations, observation helpers,
scoring helpers, and operation-record assembly.

Current hardening added a mechanism-aware species-role boundary. Runtime
services now resolve reactants, targets, impurities, catalyst species,
byproduct signals, and degradation markers through `MechanismSpeciesView`
rather than reading fixed species names throughout the service code. The
remaining legacy names are isolated as world-level fallback role bindings for
older benchmark mechanisms and tests.

Recommended follow-up:

- split `domain_services.py` into reaction, thermal, phase/separation,
  observation, instrument-cost, scoring, and operation-record services;
- keep operation kernels as small command handlers;
- continue moving mechanism-specific scoring and observation mapping into
  compiled mechanism cards;
- strengthen transaction-level replay tests.
- continue shrinking the legacy fallback surface by letting reaction,
  separation, spectroscopy, and score specs carry all species bindings.

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
- Moved the former batch-reactor runtime implementation out of `core` and into
  `runtime/domain_services.py` as the current semi-mechanistic service backend.
- Added `runtime/species.py` as the single species-role adapter between
  compiled mechanisms and the current semi-mechanistic domain services.
- Migrated reagent addition, catalyst addition, phase bookkeeping,
  electrochemical conversion, downstream truth values, flow conversion, and
  observation truth scoring toward compiled-mechanism role mappings.
- Added regression tests using the `electrochemical_conversion` mechanism to
  verify non-`A/P/B/D/E` species can drive runtime services and observations.

## Verification

Run these after every cleanup slice:

```bash
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m mypy src\chemworld
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m mkdocs build --strict
```

## Next Cleanup Order

1. Split `reaction_network.py` into specs, rate laws, thermochemistry coupling,
   sensitivities, loaders, and reference cases.
2. Split `eos.py`, `spectroscopy.py`, and `equilibrium_chemistry.py` by
   algorithm family.
3. Split `runtime/domain_services.py` into narrower domain-service modules and
   continue reducing legacy scalar-state adapter responsibilities.
