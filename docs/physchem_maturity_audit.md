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
| Reaction networks | Lite with a reference-validated ODE slice | YAML/JSON mechanisms, stoichiometric checks, rate-law tests, analytical irreversible/reversible first-order ODE cases, optional Cantera Arrhenius-rate check | Cantera-style thermochemistry, falloff, pressure dependence, heat-release-coupled reactor validation |
| Reactor models | Lite with a reference-validated CSTR multiplicity slice | batch, semi-batch, CSTR, PFR tests; analytical exothermic CSTR three-root ignition/extinction case with stability classification | broader Cantera/IDAES reactor-network validation, pressure modes, and heat-transfer variants |
| EOS | Lite with a reference-validated PR/SRK residual slice | ideal gas, PR/SRK roots, fugacity coefficients, explicit root policy, residual H/S/G tests, optional `thermo.eos` comparisons for methane/ethane/CO2 | volume translation, phase envelopes, flash derivatives, and broader CoolProp/teqp/thermopack validation |
| Phase equilibrium | Lite with a reference-validated Wilson/NRTL gamma slice | ideal VLE, Wilson/NRTL gamma checks against `thermo`, LLE split tests | UNIQUAC, phase stability, nonideal VLE/LLE task cases |
| Separations | Proxy/lite with a reference-validated VLE distillation shortcut slice | material-conserving extraction, VLE flash, VLE/Fenske shortcut distillation, crystallization, filtration, drying tests | rigorous MESH columns, thermodynamic extraction, crystallization kinetics, and broader equipment validation |
| Transport and heat transfer | Lite with reference-validated pipe-flow and heat-transfer slices | dimensionless numbers, explicit friction methods, `fluids` Haaland and single-phase pipe-pressure-drop optional checks; Nusselt branch metadata; counterflow exchanger duty-balance tests; optional `fluids.core.Nusselt` check | two-phase correlations, boiling/condensation, shell-side correction factors, fouling dynamics, equipment safety cards, and broader validity maps |
| Equilibrium chemistry | Lite/proxy | mass-action, acid/base, precipitation tests | Reaktoro-style Gibbs minimization and database-backed equilibria |
| Mechanism/scenario library | Lite | curated mechanism cards and validation tests | reference-validated mechanisms and professional task bindings |
| Spectroscopy/instruments | Synthetic/lite with reference-validated UV-vis and chromatography slices | state-coupled HPLC/GC/UV-vis/IR/NMR synthetic signals; UV-vis Beer-Lambert calibration tests; HPLC/GC retention-factor, plate-count, and resolution tests | empirical retention-index examples, IR empirical anchors, NMR coupling metadata, and broader public spectral examples |
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
- PRO-P6A is implemented: the first reactor multiplicity slice has an
  exothermic CSTR model card, inspected Cantera/IDAES reference notes,
  analytical steady-state roots, and stable/unstable/stable Jacobian-based
  classification tests.
- PRO-P7A is implemented: the distillation path no longer uses an unlabeled
  volatility-score proxy. It now uses a VLE-coupled shortcut model with
  Raoult/activity K-values, Fenske-style distribution-ratio tests, model-card
  metadata, and task maturity metadata for `reaction-to-distillation`.
- PRO-P10A is implemented for UV-vis only: Beer-Lambert absorbance, path length,
  sample dilution, blank absorbance, analytical calibration fitting, LOD/LOQ,
  model-card metadata, and species-signal tests are in place. Other instruments
  remain synthetic/lite until their own professional slices are implemented.
- PRO-P10B is implemented for HPLC/GC retention only: retention factor, dead
  time, theoretical plates, baseline width, adjacent resolution, calibration
  fitting, model-card metadata, and species-signal tests are in place. IR, NMR,
  and empirical retention-index prediction remain future slices.
- PRO-P3A is implemented for the cubic-EOS residual slice: PR/SRK states now
  expose explicit root-selection policy, `da_mix_dT`, residual enthalpy,
  residual entropy, residual Gibbs energy, model-card metadata, default EOS
  tests, and optional `thermo.eos` reference checks for methane, ethane, and
  carbon dioxide.
- PRO-P8A is implemented for the first heat-transfer and exchanger-duty slice:
  Nusselt branch metadata, Dittus-Boelter and Gnielinski validity warnings,
  strict validity failure mode, `h = Nu k / D` reference round-trip, counterflow
  e-NTU duty-balance metadata, model-card evidence, and tests are in place.
  Boiling, condensation, shell-side corrections, fouling dynamics, and
  equipment safety cards remain future deepening tasks.
