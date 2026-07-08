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
| Property correlations | Lite with reference-validated curated and vapor-pressure-report slices | vapor pressure, Cp, density, viscosity, surface tension tests; curated DIPPR101/Poling checks against `chemicals`; Antoine/Wagner/DIPPR vapor-pressure reports with analytic derivative checks | broader component coverage, liquid/solid Cp, latent heat, EOS saturation, and CoolProp checks |
| Reaction networks | Lite with reference-validated ODE, NASA7 thermochemistry, thermochemical detailed-balance, and local sensitivity slices | YAML/JSON mechanisms, stoichiometric checks, rate-law tests, analytical irreversible/reversible first-order ODE cases, optional Cantera Arrhenius-rate check, NASA7 Cp/H/S/G, reaction Delta H/G, K_eq, concentration-standard correction, thermochemical reverse-rate tests, and finite-difference first-order sensitivity tests | falloff, pressure dependence, adjoint/global sensitivities, and broader reactor-network validation |
| Reactor models | Lite with reference-validated CSTR multiplicity and dynamic batch heat-release slices | batch, dynamic batch, semi-batch, CSTR, PFR tests; analytical exothermic CSTR three-root ignition/extinction case with stability classification; NASA7 heat-release dynamic batch, jacket, and sampling-ledger tests | broader Cantera/IDAES reactor-network validation, pressure modes, wall thermal inertia, and phase-change variants |
| EOS | Lite with a reference-validated PR/SRK residual slice | ideal gas, PR/SRK roots, fugacity coefficients, explicit root policy, residual H/S/G tests, optional `thermo.eos` comparisons for methane/ethane/CO2 | volume translation, phase envelopes, flash derivatives, and broader CoolProp/teqp/thermopack validation |
| Phase equilibrium | Lite with a reference-validated Wilson/NRTL gamma slice | ideal VLE, Wilson/NRTL gamma checks against `thermo`, LLE split tests | UNIQUAC, phase stability, nonideal VLE/LLE task cases |
| Separations | Proxy/lite with a reference-validated VLE distillation shortcut slice | material-conserving extraction, VLE flash, VLE/Fenske shortcut distillation, crystallization, filtration, drying tests | rigorous MESH columns, thermodynamic extraction, crystallization kinetics, and broader equipment validation |
| Transport and heat transfer | Lite with reference-validated pipe-flow and heat-transfer slices | dimensionless numbers, explicit friction methods, `fluids` Haaland and single-phase pipe-pressure-drop optional checks; Nusselt branch metadata; counterflow exchanger duty-balance tests; optional `fluids.core.Nusselt` check | two-phase correlations, boiling/condensation, shell-side correction factors, fouling dynamics, equipment safety cards, and broader validity maps |
| Equilibrium chemistry | Lite/proxy with a reference-validated Gibbs-minimization slice | mass-action, acid/base, precipitation tests; fixed-TP ideal Gibbs minimization with element, charge, phase, and nonnegative-species constraints; analytical ideal-isomerization validation | database-backed aqueous speciation, activity-corrected electrolytes, redox/electron basis selection, and CALPHAD global phase selection |
| Electrochemistry | Lite with a reference-validated Nernst/BV/Faraday slice | Nernst equilibrium potential, Butler-Volmer current, Faraday charge-to-extent conversion, Faradaic efficiency, energy accounting, task metadata, and operation-summary tests | ohmic drop, limiting current, mass transfer, double-layer dynamics, porous electrodes, electrolyte speciation, and control-mode solvers |
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
  equilibrium, equilibrium chemistry, reaction kinetics, reactors, separations,
  transport, and spectroscopy/instruments.
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

Trajectory logs, suite results, baseline report rows, and baseline report
metadata now carry the same maturity fields. Baseline report generation rejects
inconsistent maturity metadata within a single task, so a benchmark result
cannot silently mix proxy and professional kernels.

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
- DEEP-D2A is implemented for vapor-pressure formula families: Antoine, Wagner,
  and DIPPR101 report pressure, analytic `dP/dT`, `dlnP/dT`, validity status,
  and method provenance; sublimation pressure can use the same path when
  coefficients are explicitly supplied.
- DEEP-D2B is implemented for phase-aware heat capacity and enthalpy: gas,
  liquid, and solid Cp correlations can be integrated into explicit reference
  state reports; signed latent-heat transitions build solid/liquid/gas paths;
  and `MixtureEnthalpyLedger` provides reactor/flash heat-duty contributions.
  Broad Zabransky/Lastovka/tabular Cp families, EOS departure enthalpy, and
  pressure-corrected thermodynamic packages remain future slices.
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
  carbon dioxide with a documented cubic-residual tolerance profile.
- PRO-P8A is implemented for the first heat-transfer and exchanger-duty slice:
  Nusselt branch metadata, Dittus-Boelter and Gnielinski validity warnings,
  strict validity failure mode, `h = Nu k / D` reference round-trip, counterflow
  e-NTU duty-balance metadata, model-card evidence, and tests are in place.
  Boiling, condensation, shell-side corrections, fouling dynamics, and
  equipment safety cards remain future deepening tasks.
- PRO-P9A is implemented for the first equilibrium-chemistry Gibbs slice:
  fixed-TP ideal Gibbs minimization, supplied species standard Gibbs energies,
  element constraints, charge constraints, phase restrictions, nonnegative
  bounds, linearly independent constraint selection, residual diagnostics,
  model-card metadata, and analytical ideal-isomerization tests are in place.
  Reaktoro-style databases, activity-corrected aqueous speciation, and CALPHAD
  global phase selection remain future work.
- PRO-P9B is implemented for the first electrochemistry slice: Nernst
  equilibrium potential, Butler-Volmer current, Faraday charge conversion,
  Faradaic efficiency, electrical-work accounting, model-card metadata, local
  identity tests, and `electrochemical-conversion` task integration are in
  place. This is still below a full electrochemical-cell model with ohmic drop,
  mass-transfer limiting current, double-layer dynamics, porous electrodes, and
  electrolyte speciation.
- PRO-P1A is implemented for the curated component registry: component records
  now include structured provenance and uncertainty metadata, checksum-validated
  CAS identity anchors, normalized alias/CAS resolution, conflict failures, and
  JSON round-trip tests.
- PRO-P11A is implemented for benchmark maturity exports: trajectory logs,
  suite results, baseline leaderboards, and baseline reports expose
  `kernel_maturity`, `physics_maturity`, and `proxy_allowed`, with consistency
  checks against silent maturity mixing.
- PRO-P12B is implemented for reference-validation reporting: comparison
  summaries, backend availability, and skipped optional backends can be written
  as one JSON-friendly validation report.
- PRO-P5B is implemented for the first thermochemistry slice: Cantera/RMG-style
  NASA7 temperature segments, Cp/H/S/G evaluation, Cantera-style YAML thermo
  parsing, segment-continuity diagnostics, reaction Delta H/S/G, equilibrium
  constants from species Gibbs energies, model-card metadata, and local
  identity tests are in place. This is not a full thermochemistry database,
  NASA9/Shomate/group-additivity engine, pressure correction, or
  heat-release-coupled reactor model.
- PRO-P1B/PRO-P11B/PRO-P12C add the next audit layer: component field conflicts
  resolve through explicit source-priority policy, task maturity can be exported
  as a manifest, and reference-validation reports include all tracked reference
  repositories, local checkout commits, backend versions, and declared
  tolerance profiles where available.
- PRO-P5C is implemented for thermochemical detailed-balance kinetics:
  reversible Arrhenius rates can declare `K_eq_source: nasa7`, consume supplied
  species thermochemistry, compute `K_c = exp(-Delta G/RT) * C0^(sum nu_i)`,
  and use `k_reverse = k_forward / K_c`. Tests cover zero net rate at
  equilibrium, ODE convergence to the NASA7 equilibrium ratio, explicit failure
  when thermochemistry is missing, and non-equal-molecularity concentration
  standard-state correction. Falloff, pressure dependence, and reactor
  heat-release coupling remain open.
- DEEP-D6A is implemented for dynamic batch heat-release coupling: the reactor
  energy balance can consume NASA7 reaction enthalpy, uses explicit jacket and
  heat-loss terms, and treats destructive sampling as a material-out and volume
  event. This closes a constant-density batch slice; pressure dynamics,
  gas-phase work, wall thermal inertia, and phase change remain open.
- DEEP-D5D is implemented for local kinetic sensitivity analysis:
  positive multiplier-like kinetic parameters are perturbed in log space,
  reports expose `d y / d ln(p)`, normalized sensitivities, uncertainty
  contributions, and explanation rankings, and tests compare the first-order
  product sensitivity against the analytical expression. This is not an
  adjoint/global sensitivity package.
