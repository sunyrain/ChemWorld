# PhysChem Maturity Audit

ChemWorld now has a broad local physical-chemistry foundation, but broad does
not mean professional-grade. This page makes the current status explicit so the
project does not confuse proxy/lite kernels with validated scientific models.

## Maturity Levels

| Level | Meaning | Can be used in official benchmark claims? |
| --- | --- | --- |
| Proxy | Qualitative behavior only; useful for early task design | No, unless the task is explicitly labeled educational/proxy |
| Lite | Local implementation with units, invariants, and tests | Yes for alpha tasks, but not as professional physics |
| Reference validated | Selected cases compare against optional reference backends | Yes for scoped benchmark claims |
| Professional candidate | Model card, validity range, validation matrix, and task integration exist | Yes, with stated limits |
| Professional | Multiple validation cases, failure modes, documentation, and maintenance policy exist | Yes |

## Current Audit

| Area | Current level | Evidence | Main gap |
| --- | --- | --- | --- |
| Component specs and units | Lite | `chemworld.physchem.specs`, local unit tests | broader curated component database and schema governance |
| Property correlations | Lite with a reference-validated curated slice | vapor pressure, Cp, density, viscosity, surface tension tests; curated DIPPR101/Poling checks against `chemicals` | broader component coverage, liquid/solid Cp, latent heat, derivatives, and CoolProp checks |
| Reaction networks | Lite | YAML/JSON mechanisms, stoichiometric checks, rate-law tests | Cantera-style thermochemistry, falloff, pressure dependence |
| Reactor models | Lite | batch, semi-batch, CSTR, PFR tests | professional reactor-network validation and multiple-steady-state examples |
| EOS | Lite | ideal gas, PR, SRK tests | residual properties and reference validation against CoolProp/thermo/teqp |
| Phase equilibrium | Lite with a reference-validated Wilson/NRTL gamma slice | ideal VLE, Wilson/NRTL gamma checks against `thermo`, LLE split tests | UNIQUAC, phase stability, nonideal VLE/LLE task cases |
| Separations | Proxy/lite | material-conserving extraction, flash, distillation, crystallization, filtration, drying tests | rigorous equipment models and thermodynamic coupling |
| Transport and heat transfer | Lite with reference-validated pipe-flow slice | dimensionless numbers, explicit friction methods, `fluids` Haaland and single-phase pipe-pressure-drop optional checks | broader `fluids` comparisons, heat-transfer validation, and validity maps |
| Equilibrium chemistry | Lite/proxy | mass-action, acid/base, precipitation tests | Reaktoro-style Gibbs minimization and database-backed equilibria |
| Mechanism/scenario library | Lite | curated mechanism cards and validation tests | reference-validated mechanisms and professional task bindings |
| Spectroscopy/instruments | Synthetic/proxy | state-coupled HPLC/GC/UV-vis/IR/NMR synthetic signals | public calibration examples and empirical anchors |
| Reference validation | Partial | `chemicals` ideal gas, Rachford-Rice, curated vapor pressure/Cp/enthalpy; `fluids` Reynolds/Prandtl/friction/pipe drop; and `thermo` ideal VLE optional tests | CoolProp, Cantera, phasepy, Reaktoro, pycalphad coverage |

## Policy

- Proxy kernels must be named as proxy kernels.
- A proxy can support exploration, but cannot close a professional TODO item.
- A local lite implementation can close a foundation TODO item only when tests
  cover units, invariants, and failure modes.
- A professional TODO item closes only when reference reading, model card,
  validation, and task integration are all present.
- If a professional reference library appears outdated, ChemWorld should still
  document what was inspected, identify the outdated assumption, and implement a
  clearer local alternative.

## Machine-Readable Metadata

PRO-P0 adds the first code-level contract for these rules in
`chemworld.physchem.maturity`.

Public objects:

- `MaturityLevel`: `proxy`, `lite`, `reference_validated`,
  `professional_candidate`, and `professional`.
- `ModelCardTemplate`: required model-card sections for properties, EOS, phase
  equilibrium, reaction kinetics, reactors, separations, transport, and
  spectroscopy/instruments.
- `ModelCard`: JSON-friendly model-card record with equations, assumptions,
  validity limits, failure modes, units, reference-reading notes, validation
  evidence, model-limit notes, and intended use.
- `ValidationEvidence`: optional reference-test or documented analytical
  evidence.
- `ModuleMaturity` and `TaskMaturitySpec`: task-level declarations of which
  modules are proxy, lite, reference-validated, or professional.

Current task cards and `env.reset()` task info now expose:

- `kernel_maturity`;
- `physics_maturity`;
- `proxy_allowed`.

If a task uses a proxy kernel, `proxy_allowed` must be true and the task must be
tagged as teaching, smoke, exploratory, or education. This makes proxy use
visible to students, agents, leaderboard tooling, and paper artifacts.

## Reference-Reading Notes

The first maturity implementation was designed after inspecting local reference
repositories:

- `thermo` separates model parameters from state and exposes JSON-friendly
  serialization for activity models.
- `thermo` property packages define flash tolerances and fixed temperature and
  pressure bounds.
- Cantera YAML files keep description, generator, source files, units, phase
  models, species models, and transport models explicit.
- IDAES declares component and property capabilities through structured config
  blocks and property-package metadata.

ChemWorld localizes those ideas into small dataclasses rather than importing or
copying the reference implementations.

## Immediate Corrections

- `TODO.md` now describes the current P1-P12 batch as foundation/lite work.
- `TODO_PROFESSIONAL.md` is the canonical long-term professional roadmap.
- Docs should describe the current physical layer as compact and auditable, not
  as parity with Cantera, CoolProp, thermo, phasepy, Reaktoro, pycalphad, or
  IDAES.
- PRO-P0 is implemented: maturity enum, model-card templates, task maturity
  metadata, proxy policy checks, and tests are now in the codebase.
- PRO-P2A is implemented: the first curated property slice has model-card
  metadata and optional `chemicals` reference checks for DIPPR101 vapor
  pressure, Poling ideal-gas Cp, and sensible enthalpy integrals.
- PRO-P4A is implemented: the first nonideal activity-coefficient slice has
  Wilson/NRTL model cards, explicit directional pair-parameter contracts, and
  optional `thermo` reference checks for binary gamma values.
