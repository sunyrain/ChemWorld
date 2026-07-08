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
| `src/chemworld/physchem/properties.py` | property reports, vapor pressure, enthalpy, volume, transport, hazard helpers, model cards | split into property specs/reports, vapor pressure, enthalpy, volume/density, transport-property reports, hazard helpers, and `property_cards.py` |
| `src/chemworld/physchem/reactors.py` | reactor specs, batch, dynamic batch, semi-batch, CSTR, PFR, CSTR multiplicity, model cards | split into reactor specs, batch/dynamic batch, CSTR, PFR, numerical solver helpers, and `reactor_cards.py` |
| `src/chemworld/physchem/reaction_network.py` | species/reaction specs, ODE cases, detailed balance, sensitivities, mechanism loading, model cards | split into mechanism specs, rate laws, integration/reference cases, thermochemical coupling, sensitivity, loaders, and `reaction_network_cards.py` |
| `src/chemworld/physchem/eos.py` | cubic EOS specs, root solving, residuals, volume translation, provenance, model cards | split into EOS specs, cubic parameters, root policy, residual properties, volume translation, provenance, and `eos_cards.py` |
| `src/chemworld/physchem/spectroscopy.py` | calibration, chromatography, signal synthesis, feature heuristics, model cards | split into calibration, chromatography, signal synthesis, feature libraries, and `spectroscopy_cards.py` |
| `src/chemworld/core/batch_reactor.py` | task runtime, constitution factory, hidden world parameter/state transitions | migrate foundation/world-law pieces out of `core` and keep runtime orchestration small |

### Medium Priority: Model Cards Are Better As Metadata Modules

Many modules contain long `*_model_cards()` functions. These are valuable but
they are mostly metadata. Keeping them inside numerical kernels makes diffs
noisy whenever docs/provenance changes.

Action completed in this pass:

- moved separation model cards into
  `src/chemworld/physchem/separation_cards.py`;
- kept `separation_model_cards()` public through both `chemworld.physchem` and
  `chemworld.physchem.separations`;
- did not change separation numerical behavior.

Recommended next mechanical cleanups:

1. Move `property_correlation_model_cards()` to `property_cards.py`.
2. Move `reactor_model_cards()` to `reactor_cards.py`.
3. Move `reaction_kinetics_model_cards()` to `reaction_network_cards.py`.
4. Move `eos_model_cards()` to `eos_cards.py`.
5. Move `spectroscopy_model_cards()` to `spectroscopy_cards.py`.
6. Move `transport_model_cards()` to `transport_cards.py`.

Each move should keep the old public import path re-exported until a deliberate
public API cleanup pass.

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
- Added `chemworld.physchem.separation_cards`.
- Updated `chemworld.physchem.__init__` to import separation cards directly.
- Preserved the existing `chemworld.physchem.separations.separation_model_cards`
  public path through re-export.
- Verified separation and maturity tests after the split.

## Verification

Run these after every cleanup slice:

```bash
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m mypy src\chemworld
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m mkdocs build --strict
```

## Next Cleanup Order

1. Extract all remaining model-card functions into `*_cards.py` modules.
2. Split `properties.py` by physical property family.
3. Split `reactors.py` by reactor family and solver helpers.
4. Split `reaction_network.py` into specs, rate laws, thermochemistry coupling,
   sensitivities, loaders, and reference cases.
5. Move `core.batch_reactor` responsibilities into `world` and `foundation`
   modules.
