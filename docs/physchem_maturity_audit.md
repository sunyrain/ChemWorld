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
| Property correlations | Lite/proxy | vapor pressure, Cp, density, viscosity, surface tension tests | more reference-checked compounds and fewer placeholders |
| Reaction networks | Lite | YAML/JSON mechanisms, stoichiometric checks, rate-law tests | Cantera-style thermochemistry, falloff, pressure dependence |
| Reactor models | Lite | batch, semi-batch, CSTR, PFR tests | professional reactor-network validation and multiple-steady-state examples |
| EOS | Lite | ideal gas, PR, SRK tests | residual properties and reference validation against CoolProp/thermo/teqp |
| Phase equilibrium | Lite | ideal VLE, NRTL-lite, LLE split tests | full Wilson/NRTL/UNIQUAC, phase stability, nonideal reference cases |
| Separations | Proxy/lite | material-conserving extraction, flash, distillation, crystallization, filtration, drying tests | rigorous equipment models and thermodynamic coupling |
| Transport and heat transfer | Lite | dimensionless numbers, pressure drop, heat transfer tests | broader `fluids` comparisons and validity maps |
| Equilibrium chemistry | Lite/proxy | mass-action, acid/base, precipitation tests | Reaktoro-style Gibbs minimization and database-backed equilibria |
| Mechanism/scenario library | Lite | curated mechanism cards and validation tests | reference-validated mechanisms and professional task bindings |
| Spectroscopy/instruments | Synthetic/proxy | state-coupled HPLC/GC/UV-vis/IR/NMR synthetic signals | public calibration examples and empirical anchors |
| Reference validation | Partial | `chemicals`, `fluids`, `thermo` ideal VLE optional tests | CoolProp, Cantera, phasepy, Reaktoro, pycalphad coverage |

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

## Immediate Corrections

- `TODO.md` now describes the current P1-P12 batch as foundation/lite work.
- `TODO_PROFESSIONAL.md` is the canonical long-term professional roadmap.
- Docs should describe the current physical layer as compact and auditable, not
  as parity with Cantera, CoolProp, thermo, phasepy, Reaktoro, pycalphad, or
  IDAES.
