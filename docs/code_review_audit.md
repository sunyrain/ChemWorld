# Code Review Audit

Date: 2026-07-08

Scope: completed ChemWorld professional/deepening slices, with emphasis on
large files, redundant metadata, and reviewability risks.

## Findings

### High Priority: Large PhysChem Modules Mix Multiple Responsibilities

The largest files still combine public specs, numerical kernels, validation
helpers, model cards, and export lists. This makes review harder and increases
merge-conflict risk during two-person development.

Largest current source files after this cleanup:

| File | Approximate role | Follow-up split target |
| --- | --- | --- |
| `src/chemworld/physchem/properties.py` | property reports, vapor pressure, enthalpy, volume, transport-property ledgers, hazard helpers | split into property specs/reports, vapor pressure, enthalpy, volume/density, transport-property reports, and hazard helpers |
| `src/chemworld/physchem/reactors.py` | reactor specs, batch, dynamic batch, semi-batch, CSTR, PFR, CSTR multiplicity | split into reactor specs, batch/dynamic batch, CSTR, PFR, and numerical solver helpers |
| `src/chemworld/physchem/reaction_network.py` | species/reaction specs, ODE cases, detailed balance, sensitivities, mechanism loading | split into mechanism specs, rate laws, integration/reference cases, thermochemical coupling, sensitivity, and loaders |
| `src/chemworld/physchem/equilibrium_chemistry.py` | mass-action equilibrium, acid-base, precipitation, Gibbs minimization | split into mass-action, electrolyte/acid-base, precipitation, and Gibbs minimization helpers |
| `src/chemworld/physchem/eos.py` | cubic EOS specs, root solving, residuals, volume translation, provenance | split into EOS specs, cubic parameters, root policy, residual properties, volume translation, and provenance |
| `src/chemworld/physchem/spectroscopy.py` | calibration, chromatography, signal synthesis, feature heuristics | split into calibration, chromatography, signal synthesis, and feature libraries |
| `src/chemworld/core/batch_reactor.py` | task runtime, constitution factory, hidden world parameter/state transitions | migrate foundation/world-law pieces out of `core` and keep runtime orchestration small |

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

1. Split `properties.py` by physical property family while preserving public
   imports through a thin aggregation module.

### Medium Priority: Runtime Still Depends On `core.batch_reactor`

`ChemWorldEnv` still imports the main runtime pieces and constitution factory
from `chemworld.core.batch_reactor`. That file remains a broad orchestration
module. This is acceptable for the current benchmark, but it is the next major
architecture cleanup if the goal is a professional world-law layer.

Recommended follow-up:

- move constitution construction into `foundation` or `world.world_law`;
- move hidden parameter/world generation into `world.parameters`;
- move reaction/separation event execution into dedicated world kernels;
- leave `core.batch_reactor` as a thin scenario/runtime bridge or remove it
after tests are migrated.

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

## Verification

Run these after every cleanup slice:

```bash
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m mypy src\chemworld
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m mkdocs build --strict
```

## Next Cleanup Order

1. Split `properties.py` by physical property family.
2. Split `reactors.py` by reactor family and solver helpers.
3. Split `reaction_network.py` into specs, rate laws, thermochemistry coupling,
   sensitivities, loaders, and reference cases.
4. Split `eos.py`, `spectroscopy.py`, and `equilibrium_chemistry.py` by
   algorithm family.
5. Move `core.batch_reactor` responsibilities into `world` and `foundation`
   modules.
