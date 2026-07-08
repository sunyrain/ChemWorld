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
- Do not open the next-stage professional TODO expansion until the current
  twelve-area queue is settled; when it is opened, every line must be a concrete
  implementation slice with reference targets, equations, validation cases, and
  task integration criteria rather than a proxy placeholder.
- After the first twelve professional implementation slices are finished, active
  work moves to `TODO_PROFESSIONAL_DEEPENING.md` and the
  [Professional Deepening TODO](professional_deepening_todo.md) docs page.

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
   Done in PRO-P6A.
7. Replace simple distillation proxy with VLE-coupled shortcut distillation.
   Done in PRO-P7A.
8. Add Beer-Lambert UV-vis model card and calibration validation.
   Done in PRO-P10A.
9. Add HPLC/GC retention-factor and peak-broadening calibration.
   Done in PRO-P10B.
10. Add Peng-Robinson/SRK fugacity-coefficient and residual-property validation.
    Done in PRO-P3A.
11. Add heat-transfer correlations and heat-exchanger duty checks.
    Done in PRO-P8A.
12. Harden the component registry with provenance, aliases, uncertainty fields,
    and conflict-resolution policy. Done in PRO-P1A.

After item 12 is done, the next active roadmap is the
[Professional Deepening TODO](professional_deepening_todo.md). That roadmap is
not a proxy backlog; each item must name equations, reference targets,
validation cases, model cards, and benchmark integration.

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

PRO-P5B is now implemented for the NASA7 thermochemistry and reaction Gibbs
slice:

- `NASA7TemperatureSegment` implements the Cantera/RMG NASA7 coefficient order
  and evaluates `Cp/R`, `H/RT`, and `S/R` inside declared temperature ranges.
- `NASA7SpeciesThermo.from_cantera_yaml_thermo()` parses the compact
  Cantera-style `model: NASA7`, `temperature-ranges`, and coefficient `data`
  structure.
- `NASA7SpeciesThermo.evaluate()` returns Cp, enthalpy, entropy, and Gibbs
  energy in explicit SI molar units.
- `reaction_thermochemistry()` forms reaction Delta H, Delta S, Delta G, and
  equilibrium constants by stoichiometric summation of species standard states.
- `continuity_report()` flags gaps or jumps between adjacent NASA7 temperature
  segments.
- `thermochemistry_model_cards()` records the inspected Cantera/RMG references,
  equations, validity limits, failure modes, and local tests.
- This is a professional thermochemistry slice, not a full Cantera/RMG
  thermochemistry database. NASA9, Shomate, group additivity, pressure
  corrections, and reactor-energy coupling remain future deepening tasks.

PRO-P5C is now implemented for thermochemistry-coupled reversible kinetics:

- `thermochemical_detailed_balance()` computes forward and reverse rate
  constants for a `reversible_arrhenius` reaction using NASA7 reaction Gibbs
  energy.
- `thermochemical_concentration_equilibrium_constant()` keeps the distinction
  between dimensionless `K = exp(-Delta G/RT)` and the concentration
  equilibrium constant used by mass-action rates:
  `K_c = K * C0^(sum nu_i)`.
- `reverse_rate_constant_from_equilibrium()` exposes the audited
  `k_reverse = k_forward / K_c` relationship used by the local rate law.
- `evaluate_rate_law()` and `ReactionNetworkSpec.integrate_batch()` can now use
  supplied `species_thermo` when a reversible Arrhenius rate declares
  `K_eq_source: nasa7`.
- Tests cover zero net rate at the thermochemical equilibrium ratio,
  long-time ODE convergence to the NASA7 equilibrium ratio, missing
  thermochemistry failure, and non-equal-molecularity concentration-standard
  correction.
- This is not a full pressure-dependent, falloff, gas-expansion, or
  pressure-dependent reactor model. DEEP-D6A wires reaction enthalpy into a
  constant-density dynamic batch energy-balance slice.

DEEP-D5D is now implemented for local kinetic sensitivity analysis:

- `finite_difference_reaction_sensitivities()` reruns a
  `ReactionNetworkSpec` under central log-parameter perturbations.
- `kinetic_sensitivity_parameter_candidates()` scans positive multiplier-like
  kinetic parameters including `k`, `A`, `A_reverse`, `K_eq`, `vmax`, and
  `Km`.
- `ReactionSensitivityReport` records baseline observable value,
  per-parameter `d y / d ln(p)`, normalized `S = (1/y) d y / d ln(p)`,
  local uncertainty contributions, ranked entries, and explanation summaries.
- Tests compare the first-order irreversible product sensitivity against the
  analytical `k t exp(-kt)/(1-exp(-kt))` expression and cover zero-baseline
  normalization and explicit failure modes.
- This is a local finite-difference benchmark/explanation hook, not a global
  Sobol analysis, adjoint sensitivity solver, or pressure-dependent kinetics
  package.

PRO-P6A is now implemented for the first reference-validated reactor
multiplicity slice:

- `cstr_multiple_steady_state_reference_case()` exposes a ChemWorld-owned
  exothermic first-order CSTR case with explicit feed, volume, heat-transfer,
  coolant, heat-capacity, Arrhenius, and temperature-bound parameters.
- `solve_cstr_multiple_steady_states()` solves the scalar steady-state energy
  balance, returns three ignition/extinction roots, and classifies local
  stability from the dynamic CSTR Jacobian.
- `CSTRMultiplicitySpec.network()` exposes the corresponding balanced
  `ReactionNetworkSpec`, keeping reactor examples tied to the shared chemistry
  representation.
- `reactor_model_cards()` records assumptions, validity limits, failure modes,
  inspected Cantera/IDAES references, and analytical validation evidence.
- This closes a narrow professional slice for multiple steady states. It does
  not claim full Cantera reactor-network parity or IDAES process-model parity.

DEEP-D6A is now implemented for the dynamic batch heat-release and sampling
slice:

- `DynamicBatchReactorModel` integrates species and temperature trajectories
  for a constant-density batch reactor.
- The energy equation is
  `rhoCp V dT/dt = Q_jacket - Q_loss - sum_i DeltaH_i(T) r_i V`.
- If NASA7 species thermochemistry is supplied, reaction heat comes from
  `reaction_thermochemistry()` at the current temperature; otherwise the local
  reaction `delta_h_J_per_mol` field is used.
- `JacketTemperatureProgram` supports step or linear jacket setpoints over
  time.
- `SamplingEventSpec` removes a well-mixed destructive sample, reduces volume,
  records `material_out_mol`, and preserves element material balance.
- `reactor_model_cards()` now includes
  `dynamic_batch_heat_release_jacket_sampling` with equations, assumptions,
  validity limits, failure modes, Cantera/IDAES reference reading, and test
  evidence.
- This closes the dynamic constant-density batch heat-release/sampling slice,
  not constant-pressure expansion, gas-phase work, wall thermal inertia,
  vapor-liquid phase change, or full process-control dynamics.

PRO-P7A is now implemented for the first reference-validated distillation
shortcut slice:

- `vle_shortcut_distillation()` replaces arbitrary volatility-score splitting
  with Raoult/activity VLE `K_i` values, relative volatilities, reflux-scaled
  effective stages, and a solved total distillate cut.
- Component distribution ratios satisfy the Fenske-style identity
  `(D_i/B_i)/(D_j/B_j) = (alpha_i/alpha_j)**N_eff`, which is checked in local
  tests.
- The ChemWorld `distill` operation now records `distillation_model =
  "vle_shortcut_distillation"` and stores the VLE/Fenske metadata in the
  campaign state ledger.
- The `reaction-to-distillation` task metadata now reports the distillation
  module as `reference_validated` rather than proxy.
- `separation_model_cards()` records equations, assumptions, validity limits,
  failure modes, inspected IDAES/thermo/phasepy references, and analytical
  validation evidence.
- This is still a shortcut column model, not a rigorous MESH tray-by-tray
  solver with pressure profile, hydraulics, Underwood/Gilliland sizing, or
  azeotrope detection.

PRO-P10A is now implemented for the UV-vis analytical calibration slice:

- `BeerLambertBandSpec` declares wavelength, molar absorptivity, path length,
  sample dilution, blank absorbance, detection limit, and noise.
- `beer_lambert_absorbance()` implements `A = A_blank + epsilon * l * c`.
- `fit_beer_lambert_calibration()` and
  `generate_beer_lambert_calibration()` fit calibration standards and report
  effective slope, dilution-corrected molar absorptivity, residual standard
  deviation, LOD, LOQ, and slope uncertainty.
- UV-vis species spectra now carry `beer_lambert_uvvis` metadata and use
  `uvvis_beer_lambert_calibration_v1`.
- `spectroscopy_model_cards()` documents equations, assumptions, limits,
  failure modes, reference reading, and analytical validation evidence.
- IR, NMR, MS, and empirical spectral databases still need their own
  professional slices.

PRO-P10B is now implemented for the HPLC/GC retention and peak-broadening slice:

- `ChromatographyMethodSpec` declares dead time, theoretical plates,
  role-specific retention factors, detector response factors, detection limit,
  and calibration noise.
- `chromatographic_retention_time()`,
  `chromatographic_retention_factor()`,
  `chromatographic_baseline_peak_width()`,
  `chromatographic_theoretical_plates()`, and
  `chromatographic_resolution()` implement the analytical equations used by the
  virtual method.
- `fit_chromatography_calibration()` estimates retention factor and theoretical
  plates from calibration retention times and baseline widths.
- HPLC/GC species spectra now carry `chromatography_retention_plate` metadata,
  `hplc_retention_plate_calibration_v1` or
  `gc_retention_plate_calibration_v1`, and adjacent-peak resolution summaries.
- This is still a compact benchmark instrument kernel, not empirical retention
  index prediction, gradient elution, column aging, or asymmetric peak tailing.

PRO-P3A is now implemented for the first reference-validated cubic-EOS residual
property slice:

- `CubicPureParameters` now records the attractive parameter derivative
  `da_alpha_dT`, and `EOSMixtureParameters` records `da_mix_dT`.
- `evaluate_cubic_eos()` returns explicit `root_selection_policy`,
  residual enthalpy, residual entropy, residual Gibbs energy, and residual
  property metadata in `EOSState`.
- `cubic_residual_properties()` implements PR/SRK departure-property formulas
  for molar `H^R`, `S^R`, and `G^R`.
- `eos_model_cards()` documents equations, assumptions, validity limits,
  failure modes, inspected references, and validation evidence.
- Default tests cover low-pressure ideal-gas limits, liquid/vapor/stable root
  policies, Gibbs consistency with fugacity coefficients, and model-card
  metadata.
- Optional reference tests compare methane, ethane, and carbon dioxide pure
  vapor-root PR/SRK `Z`, `phi`, `H_dep`, and `S_dep` against `thermo.eos` when
  `CHEMWORLD_RUN_REFERENCE_TESTS=1`.
- This is not a complete EOS/flash package. Volume translation, phase
  envelopes, saturation solvers, mixture flash derivatives, and critical-region
  handling remain on the later professional TODO track.

PRO-P8A is now implemented for the first reference-validated heat-transfer and
exchanger-duty slice:

- `nusselt_internal_flow_details()` exposes the selected Nusselt branch,
  flow regime, friction factor, validity warnings, and optional
  `strict_validity=True` failure behavior.
- The local heat-transfer branches cover a constant fully developed laminar
  relation, Dittus-Boelter, and Gnielinski. Auto mode uses a smooth
  laminar-to-Gnielinski transition for benchmark rollouts, while explicit
  branches can fail on validity warnings in tests or validators.
- `internal_heat_transfer_coefficient()` keeps the `h = Nu k / D` contract
  explicit, and optional reference tests round-trip that definition against
  `fluids.core.Nusselt`.
- `heat_exchanger_counterflow()` now reports hot-side heat lost, cold-side heat
  gained, maximum possible duty, and the duty-balance residual in addition to
  effectiveness and outlet temperatures.
- `transport_model_cards()` records the inspected `fluids`, IDAES
  heat-exchanger, IDAES e-NTU, and CoolProp property-workflow references.
- This is still a scoped single-phase heat-transfer slice. Boiling,
  condensation, shell-side correction factors, fouling dynamics, and equipment
  safety cards remain future deepening tasks rather than proxy-filled claims.

PRO-P9A is now implemented for the first reference-validated equilibrium
chemistry Gibbs-minimization slice:

- `GibbsSpeciesSpec` declares species id, phase, element counts, charge, and
  supplied standard Gibbs energy.
- `GibbsMinimizationSpec` declares a fixed-TP small-system equilibrium problem
  with optional phase restrictions and target charge.
- `solve_gibbs_minimization()` minimizes an ideal phase-mixture Gibbs objective
  subject to element balances, charge balance, phase restrictions, and
  nonnegative species amounts.
- The solver removes linearly redundant element/charge constraints before
  calling SLSQP, then still reports full element and charge residuals in
  `GibbsMinimizationResult`.
- Tests cover the analytical ideal isomerization relation
  `n_B/n_A = exp[-(G_B^0-G_A^0)/RT]`, phase-restricted salt behavior,
  solid-forming behavior, failure modes, and model-card validation.
- `equilibrium_chemistry_model_cards()` records inspected Reaktoro
  `EquilibriumSpecs`/solver interfaces, Cantera equilibrium documentation, and
  pycalphad `conditions + phases + GM/MU` architecture.
- This is not a database-backed aqueous speciation solver, a Reaktoro clone, or
  a CALPHAD global phase-selection algorithm.

PRO-P9B is now implemented for the first electrochemical thermodynamics and
charge-accounting slice:

- `ElectrodeReactionSpec` declares electron number, standard potential,
  reaction-quotient exponents, exchange-current density, electrode area, charge
  transfer coefficients, Faradaic efficiency, and selectivity parameters.
- `nernst_potential()` implements `E_eq = E0 - RT/(nF) ln Q`.
- `butler_volmer_current()` implements signed Butler-Volmer current with the
  usual anodic/cathodic exponential branches and bounded exponents for
  numerical stability.
- `faradaic_extent_mol()` and `run_electrolysis()` convert current and duration
  into reaction extent, product/byproduct amounts, Faradaic charge, electrical
  work, reversible-work proxy, and energy efficiency.
- The `electrolyze` operation in `ChemWorld` now records equilibrium potential,
  overpotential, kinetic/current-limited current, charge, Faradaic charge,
  Faradaic efficiency, and electrical work in the operation summary.
- `electrochemical-conversion` task maturity now reports
  `nernst_butler_volmer_faradaic_v1` rather than the old electrochemistry proxy.
- This is not a full electrochemical-cell or battery simulator. Ohmic drop,
  double-layer dynamics, explicit mass-transfer limiting current, porous
  electrodes, electrolyte speciation, and potentiostatic/galvanostatic
  controllers remain deepening tasks.

PRO-P1A is now implemented for component registry provenance and conflict
policy:

- `ComponentProvenance` and `ComponentUncertainty` make component-level source
  tables, source keys, source paths, and uncertainty notes JSON-friendly.
- `ComponentSpec` round-trips those records without breaking older component
  declarations.
- `component_alias_index()` and `resolve_component_identifier()` normalize
  aliases and reject cross-component conflicts before task or property kernels
  bind to an ambiguous component.
- Curated property packages now attach structured provenance/uncertainty to
  water, ethanol, acetone, toluene, methane, and carbon dioxide.
- This remains a small curated registry, not a vendored chemicals, thermo, or
  CoolProp database.

PRO-P11A is now implemented for benchmark maturity exports:

- Trajectory JSONL records carry `kernel_maturity`, `physics_maturity`, and
  `proxy_allowed`.
- Suite results and baseline report rows retain those fields.
- `BaselineReport` includes a task maturity manifest and a maturity summary by
  physics level.
- Report generation fails if results for the same benchmark task contain mixed
  maturity metadata, preventing silent proxy/professional result mixing.

PRO-P12B is now implemented for reference-validation summary export and skip
auditing:

- `ReferenceValidationReport` combines scalar comparison summaries with
  backend availability reports.
- `skipped_reference_backends()` records unavailable or failed optional
  reference backends with explicit reasons and comparison scope.
- `write_reference_validation_report()` writes the audit payload as JSON.
- This does not make optional backends required for the default install; it
  makes their absence visible in validation artifacts.

PRO-P1B is now implemented for component source-priority conflict auditing:

- `ComponentConflictPolicy` declares warning, hard-fail, or source-priority
  preference behavior.
- `ComponentFieldCandidate` records candidate values, source ids, priority, and
  uncertainty metadata.
- `resolve_component_field_conflict()` returns a JSON-friendly audit record or
  raises before ambiguous component data can reach a physical kernel.

PRO-P11B is now implemented for task maturity manifests:

- `task_maturity_manifest()` exports task/kernel maturity metadata without
  running an environment.
- The manifest is grouped by task id and by physics maturity level, and lists
  proxy-allowed tasks explicitly.

PRO-P12C is now implemented for reference backend version and tolerance
manifests:

- `ReferenceBackendStatus` includes an optional installed package version.
- `ReferenceToleranceProfile` records declared tolerances for common optional
  reference-comparison families.
- `ReferenceValidationReport` now carries those tolerance profiles alongside
  comparisons, backend statuses, and skipped-backend records.
