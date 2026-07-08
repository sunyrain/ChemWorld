# Professional Deepening TODO

This page mirrors `TODO_PROFESSIONAL_DEEPENING.md`. It is the next roadmap after
the first twelve professional implementation slices in `TODO_PROFESSIONAL.md`
are complete.

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
2. `DEEP-D2B`: heat-capacity/enthalpy package with reactor energy integration.
3. `DEEP-D7B`: Fenske-Underwood-Gilliland distillation sizing.
4. `DEEP-D6A`: dynamic batch reactor with heat release and jacket control.
   Done.
5. `DEEP-D9B`: IR functional-group spectrum slice.
6. `DEEP-D10A`: benchmark model-maturity gate.
7. `DEEP-D8A`: phase-change and equipment heat transfer beyond the completed
   single-phase Nusselt/e-NTU slice.
8. `DEEP-D11A`: electrochemical ohmic-drop and electrolyte-resistance slice.
9. `DEEP-D11B`: mass-transfer limiting-current slice for electrode processes.

For the complete checklist, use the root file
`TODO_PROFESSIONAL_DEEPENING.md`.
