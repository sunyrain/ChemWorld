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

1. Add maturity metadata and model-card templates. Done in PRO-P0.
2. Expand `fluids` validation to friction factor and pressure drop. Done in
   PRO-P12A.
3. Replace placeholder property examples with curated reference-checked
   compounds. Done in PRO-P2A.
4. Implement Wilson and full binary NRTL with reference comparisons. Done in
   PRO-P4A.
5. Add Cantera-comparable irreversible and reversible reaction ODE cases.
   Done in PRO-P5A.
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

## Current Implementation

PRO-P0 is now implemented in `chemworld.physchem.maturity` and task metadata:

- `MaturityLevel` defines proxy, lite, reference-validated,
  professional-candidate, and professional states.
- `ModelCardTemplate` defines required sections for each physical module family.
- `ModelCard` and `ValidationEvidence` make professional claims auditable.
- `TaskMaturitySpec` appears in task cards and environment `task_info`.
- Proxy tasks must be explicitly marked as proxy-allowed and exploratory,
  teaching, smoke, or education.

PRO-P12A is now implemented for the first reference-validated transport slice:

- `darcy_friction_factor_details()` exposes method, regime, relative roughness,
  and validity warnings.
- `pipe_pressure_drop()` can run with an explicit `friction_method`, allowing
  reference comparisons to select the Haaland branch directly.
- `transport_model_cards()` declares the pipe-friction/single-phase-pressure
  drop slice as reference-validated with `fluids` optional-test evidence.
- Optional reference tests compare ChemWorld against `fluids.friction.Haaland`
  and `fluids.friction.one_phase_dP`.

PRO-P2A is now implemented for the first reference-validated property slice:

- `curated_property_package()` exposes water, ethanol, acetone, toluene,
  methane, and carbon dioxide as small auditable property packages.
- The curated vapor-pressure path uses Perry/DIPPR101 coefficients and the
  equation `Psat = exp(A + B/T + C ln(T) + D T^E)`.
- The curated ideal-gas heat-capacity path uses Poling/DIPPR100 polynomial
  coefficients scaled by `R` into SI units.
- `curated_property_model_cards()` records equations, assumptions, validity
  limits, failure modes, intended use, and optional `chemicals` validation
  evidence.
- Optional reference tests compare ChemWorld vapor pressure, ideal-gas Cp, and
  sensible enthalpy integrals against `chemicals.dippr.EQ101` and
  `chemicals.dippr.EQ100`.

PRO-P4A is now implemented for the first reference-validated nonideal activity
coefficient slice:

- `ActivityModelSpec` now supports explicit `wilson` and `nrtl` models with
  auditable parameter contracts.
- Wilson uses directional `Lambda_ij` pair parameters, including optional
  temperature-dependent `a + b/T + c ln(T) + dT + e/T^2 + fT^2` coefficients.
- NRTL uses directional `tau_ij`, `alpha_ij`, and `G_ij` matrices and supports
  binary or multicomponent mixtures through the same JSON-friendly pair-key
  contract.
- Missing Wilson/NRTL directional pairs and nonpositive Wilson/NRTL parameters
  fail during spec construction or evaluation instead of silently reverting to
  ideal behavior.
- `activity_model_cards()` records equations, assumptions, validity limits,
  failure modes, intended use, and optional `thermo` validation evidence.
- Optional reference tests compare ChemWorld Wilson and NRTL gamma values
  against `thermo.wilson.Wilson_gammas` and
  `thermo.nrtl.NRTL_gammas_binaries`.

PRO-P5A is now implemented for the first reference-validated reaction ODE
slice:

- `cantera_comparable_reaction_cases()` exposes ChemWorld-owned irreversible
  `A => B` and reversible `A <=> B` constant-volume, isothermal, first-order
  batch ODE cases.
- Each case has a balanced `ReactionNetworkSpec`, explicit rate parameters,
  evaluation times, and an analytical trajectory.
- `evaluate_reaction_ode_reference_case()` compares numerical integration
  against analytical solutions with explicit `rtol`/`atol`.
- `reaction_kinetics_model_cards()` records the validated slice, reference
  reading notes, equations, assumptions, validity limits, failure modes, and
  optional Cantera evidence.
- Optional reference tests compare ChemWorld's Arrhenius rate constant against
  `ct.ArrheniusRate` if Cantera is importable.
- This is not a claim that ChemWorld has reimplemented Cantera. Falloff,
  third-body effects, pressure dependence, thermochemistry-derived
  equilibrium constants, and heat-release-coupled reactors stay on the next
  professional TODO track.
