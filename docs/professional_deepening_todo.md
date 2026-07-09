# Professional Deepening TODO

This page mirrors `TODO_PROFESSIONAL_DEEPENING.md`. It is the next roadmap after
the first twelve professional implementation queue slices in
`TODO_PROFESSIONAL.md` are complete. That milestone does not mean the broad
P1-P12 professional modules are complete; the unchecked module items are the
work this roadmap decomposes.

The purpose is deliberately narrow: ChemWorld should mature by implementing
auditable, module-by-module physical chemistry kernels. It should not fill gaps
with proxies and then call them professional.

## Operating Rule

- Claim one concrete slice before coding.
- Pull and push TODO changes immediately so two-person development does not
  duplicate work.
- Read relevant local reference repositories first.
- Do not copy reference-library source code.
- Do not add broad placeholder files merely to increase code size; missing
  professional capability should stay unchecked until its equations,
  validation cases, limits, and task behavior exist.
- If a reference library is outdated, keep the equation or design insight only
  when it is still scientifically sound, then implement a smaller ChemWorld
  API with modern typing, explicit units, and benchmark-focused validation.
- A slice is done only when code, tests, model card, docs, validation examples,
  and task integration are present.

## Active Deepening Work

| ID | Owner | Status | Scope |
| --- | --- | --- | --- |
| `DEEP-D6A` | whilesunny | Done | Dynamic batch reactor with NASA7 reaction heat release, jacket control, variable-volume destructive sampling losses, material/energy ledgers, tests, model card, docs, and public reactor API integration. |
| `DEEP-D5D` | whilesunny | Done | Finite-difference kinetic parameter sensitivity reports with normalized response coefficients, uncertainty propagation summaries, explanation-task ranking hooks, tests, model card, and docs. |
| `DEEP-D2A` | whilesunny | Done | Vapor-pressure families with Antoine and Wagner/DIPPR forms, analytic temperature derivatives, validity-domain enforcement, sublimation-pressure report support, curated coefficient provenance, tests, model card, and downstream flash/distillation/safety integration notes. |
| `DEEP-D2B` | whilesunny | Done | Phase-tagged heat-capacity and enthalpy package with reference states, sensible enthalpy reports, signed latent-heat transitions, mixture enthalpy ledgers for reactor/flash heat duties, tests, model card, and provenance. |
| `DEEP-D2C` | whilesunny | Done | Density and molar-volume package with Rackett liquid volume, ideal/virial gas hooks, mixture specific-volume ledgers, compressibility warnings, tests, model card, and provenance. |
| `DEEP-D2D` | whilesunny | Done | Transport-property package with liquid/gas viscosity reports, DIPPR9B gas conductivity, DIPPR9H liquid-mixture conductivity, Wilke gas-mixture viscosity, Fuller gas diffusivity estimates, thermal diffusivity, uncertainty/validity metadata, tests, model card, and provenance. |
| `DEEP-D3A` | whilesunny | Done | Volume-translated cubic EOS and root-governance diagnostics with translated molar-volume reports, stable-root policy evidence, binary-interaction provenance, tests, model card, and docs. |
| `DEEP-D7B` | whilesunny | Done | Fenske-Underwood-Gilliland distillation sizing with minimum stages, minimum reflux, Gilliland/Eduljee stage estimate, feed-stage estimate, pressure-profile warnings, tests, model card, and docs. |
| `DEEP-R1A` | whilesunny | Done | Runtime operation taxonomy and macro compiler: primitive/domain/macro/terminal operation contracts, macro recipe expansion, compiled-step task-policy validation, and LLM/student recipe-tool integration. |
| `DEEP-R1B` | whilesunny | Done | Runtime domain-service registry with JSON-friendly service contracts, operation-to-service map, runtime/task-info exposure, and service id in transaction events. |
| `DEEP-R1C` | whilesunny | Done | Task runtime service contract: profile-declared required domain services, service/capability coverage validation at runtime startup, and serialized task-info service requirements. |
| `DEEP-D9B` | whilesunny | Done | IR functional-group spectrum slice with curated local band catalog, formula/role-based assignments, broadening, overlap warnings, calibration examples, tests, model card, and public signal API integration. |
| `DEEP-D5C` | whilesunny | Done | Mechanism schema and manifest slice: schema-versioned mechanism contracts, validation report, deterministic hash manifest, replay/submission audit hooks, docs, and tests. |
| `DEEP-D3B` | whilesunny | Done | Pure-fluid saturation solver: saturation pressure/temperature solve, normal boiling point wrapper, critical-region warnings, validity-bound checks, residual diagnostics, reference-reading hooks, tests, docs, model card, and public API exports. |
| `DEEP-D3C` | whilesunny | Done | Mixture bubble/dew flash slice: bubble/dew temperature reports, K-value initialization from pure saturation reports, Rachford-Rice diagnostics, nonconvergence guards, tests, docs, model card, and public API exports. |
| `DEEP-D3D` | whilesunny | Done | Gamma-phi VLE bridge slice: gamma/phi/Psat/K-value reports, vapor fugacity coefficient contract, binary azeotrope residual scan, crossing diagnostics, tests, docs, model card, and public API exports. |
| `DEEP-D4A` | whilesunny | Done | UNIQUAC activity-coefficient slice: structural r/q parameters, binary tau interactions, combinatorial/residual gamma terms, validation reports, model card, tests, docs, optional `thermo.uniquac` reference check, and activity-model API integration. |
| `DEEP-D1A` | liyijun | Claimed | Component identity registry with aliases, checksum-validated CAS, InChIKey-style identifiers where licensing permits, curated provenance, duplicate-identity checks, JSON round-trips, and task/property lookup integration. |
| `DEEP-D1B` | liyijun | Claimed | Unit-dimension checker with canonical dimensions for amount, mass, volume, temperature, pressure, energy, power, viscosity, diffusivity, conductivity, and instrument response, plus compatibility tests before kernels run. |
| `DEEP-D1C` | liyijun | Claimed | Data conflict policy with source-priority, uncertainty-aware warning versus hard-fail modes, unit compatibility checks, JSON-friendly resolution reports, and curated registry provenance. |
| `DEEP-D10A` | whilesunny | Done | Model-maturity gate audit for task, trajectory, baseline, and leaderboard outputs; benchmark artifacts expose proxy/lite/professional metadata and reject silent same-task maturity mixing. |
| `DEEP-D11A` | whilesunny | Claimed | Electrochemical ohmic-drop and electrolyte-resistance slice: solution resistance, uncompensated voltage drop, measured versus interfacial potential, energy-loss accounting, and runtime/task metadata. |

## Module Families

| Family | Deepening target |
| --- | --- |
| Component data and units | identity registry, strict dimensions, provenance, conflict policy |
| Properties | vapor pressure, Cp/enthalpy, density, transport properties |
| EOS and flash | volume-translated cubic EOS, root governance, saturation and mixture flash |
| Phase equilibrium | UNIQUAC, LLE, electrolyte/aqueous equilibria, Gibbs minimization |
| Kinetics | thermochemistry-coupled reversibility, falloff, mechanism schema, sensitivity |
| Reactors | dynamic batch, CSTR, PFR, solver backend, event/replay diagnostics |
| Separations | flash, distillation sizing, extraction, crystallization |
| Equipment and safety | phase-change heat transfer, two-phase pressure drop, relief envelope, equipment cards |
| Instruments | HPLC/GC method sensitivity, IR, NMR, MS |
| Benchmark datasets | maturity gates, dataset exports, official reports, solver manifests |
| Electrochemistry | ohmic drop, limiting current, controller modes, capacitive current, scenario cards |

## First Deepening Candidates

Do not start these until the current twelve-slice batch is complete.

1. `DEEP-D3A`: volume-translated cubic EOS and root-governance diagnostics.
   Done.
2. `DEEP-D2B`: heat-capacity/enthalpy package with reactor energy integration.
   Done.
3. `DEEP-D7B`: Fenske-Underwood-Gilliland distillation sizing.
   Done.
4. `DEEP-D6A`: dynamic batch reactor with heat release and jacket control.
   Done.
5. `DEEP-D9B`: IR functional-group spectrum slice.
6. `DEEP-D10A`: benchmark model-maturity gate.
   Done.
7. `DEEP-D8A`: phase-change and equipment heat transfer beyond the completed
   single-phase Nusselt/e-NTU slice.
8. `DEEP-D11A`: electrochemical ohmic-drop and electrolyte-resistance slice.
9. `DEEP-D11B`: mass-transfer limiting-current slice for electrode processes.

For the complete checklist, use the root file
`TODO_PROFESSIONAL_DEEPENING.md`.
