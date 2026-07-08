# Professional TODO

The repository root file `TODO_PROFESSIONAL.md` is the canonical professional
implementation roadmap. It starts after the first foundation/lite batch in
`TODO.md`.

The professional roadmap exists because ChemWorld should not become a pile of
qualitative proxies. The long-term path is to inspect professional libraries,
identify where they remain useful or outdated, then implement ChemWorld's own
compact, modern, unit-explicit, benchmark-oriented physical chemistry core.

## Rules

- Do not copy source from reference repositories.
- Do not mark a professional task done because a proxy exists.
- Read relevant local reference repositories before implementation.
- Record what was read and what design choices were accepted or rejected.
- Implement local typed APIs with explicit units and JSON-friendly specs.
- Add model cards, validity ranges, failure modes, and validation tests.
- Keep optional heavy packages out of the default runtime.

## Module Queue

| Professional area | Reference targets | First hardening goal |
| --- | --- | --- |
| Data and properties | `chemicals`, `thermo`, `CoolProp` | curated component records and reference-checked property points |
| EOS | `CoolProp`, `thermo`, `teqp`, `thermopack` | PR/SRK residual properties and reference validation |
| Activity and phase equilibrium | `thermo`, `phasepy`, `thermopack` | Wilson, full NRTL, phase stability, nonideal VLE/LLE validation |
| Reaction kinetics | `Cantera`, `RMG-Py`, `thermo` | thermochemistry, detailed balance, falloff hooks, Cantera-comparable ODEs |
| Reactors | `Cantera`, `IDAES` | professional batch/CSTR/PFR validation and multiple steady states |
| Separations | `IDAES`, `thermo`, `phasepy`, `fluids` | VLE-coupled distillation and thermodynamic extraction models |
| Transport and heat transfer | `fluids`, `IDAES`, `CoolProp` | broader pressure-drop and heat-transfer reference comparisons |
| Equilibrium chemistry | `Reaktoro`, `Cantera`, `pycalphad` | Gibbs minimization, aqueous equilibria, and solid-phase toy models |
| Instruments | public instrument equations/datasets | model cards and calibration examples for HPLC/GC/UV-vis/IR/NMR |
| Benchmark integration | Gymnasium, Minari, Safety-Gymnasium, DiscoveryWorld | task metadata showing proxy/lite/reference/professional kernels |

## First Professional Queue

1. Add maturity metadata and model-card templates.
2. Expand `fluids` validation to friction factor and pressure drop.
3. Replace placeholder property examples with curated reference-checked
   compounds.
4. Implement Wilson and full binary NRTL with reference comparisons.
5. Add Cantera-comparable irreversible and reversible reaction ODE cases.
6. Add a CSTR multiple-steady-state professional example.
7. Replace simple distillation proxy with VLE-coupled shortcut distillation.
8. Add Beer-Lambert UV-vis model card and calibration validation.

## Completion Bar

A professional item is done only when these are all true:

- implementation exists;
- model card exists;
- validity limits are documented;
- invalid inputs fail explicitly;
- local tests cover invariants and edge cases;
- optional reference validation exists where practical;
- benchmark task integration reports the model maturity level.
