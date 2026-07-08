# ChemWorld PhysChem Core

This package contains compact physical-chemistry primitives used by ChemWorld
world-law modules. It is not a vendor copy of Cantera, thermo, chemicals, or
other reference projects.

Current scope:

- element metadata for benchmark-relevant elements;
- formula parsing with element conservation support;
- molecular-weight and elemental-fraction utilities;
- JSON-friendly `ComponentSpec`;
- self-contained `MixtureSpec`;
- explicit-unit `PropertyCorrelation` records.
- local property evaluators for vapor pressure, heat capacity, enthalpy,
  phase-change enthalpy, density, viscosity, surface tension, mixture rules,
  and safety proxies.
- public property-equation contracts for required coefficients, input
  dimensions, output dimensions, and model cards.
- curated reference-checked property packages for water, ethanol, acetone,
  toluene, methane, and carbon dioxide using DIPPR101 vapor pressure and
  Poling ideal-gas heat-capacity correlations.
- general reaction-network specs for species, reactions, stoichiometric
  matrices, element-balance checks, YAML/JSON mechanism loading, rate-law
  evaluation, and deterministic batch ODE integration.
- Cantera-comparable irreversible and reversible first-order reaction ODE
  reference cases with analytical trajectory validation and a reaction
  kinetics model card.
- NASA7 thermochemistry for species Cp/H/S/G, Cantera-style YAML thermo
  parsing, segment-continuity diagnostics, reaction Delta H/S/G, equilibrium
  constants from species Gibbs energies, and a thermochemistry model card.
- thermochemistry-coupled reversible Arrhenius rates with explicit
  dimensionless-to-concentration equilibrium conversion and
  `k_reverse = k_forward / K_c` detailed balance.
- finite-difference kinetic sensitivity reports with normalized local response
  coefficients, uncertainty propagation summaries, and explanation rankings.
- a curated mechanism/scenario library with balanced mechanism files, task
  cards, default initial states, operating windows, qualitative behavior
  metadata, and a programmatic validation report.
- spectroscopy and chromatography signal synthesis for mechanism-linked HPLC,
  GC, UV-vis, IR, and NMR raw signals with peak overlap, calibration curves,
  baseline drift, detection limits, and replicate measurements.
- a Beer-Lambert UV-vis calibration slice with explicit path length, sample
  dilution, molar absorptivity, blank absorbance, LOD/LOQ, and model-card
  evidence.
- an HPLC/GC chromatography retention slice with dead time, retention factor,
  theoretical plates, baseline peak width, adjacent resolution, calibration
  uncertainty, and model-card evidence.
- mechanism-backed reactor kernels for batch, semi-batch, CSTR, and PFR
  calculations with material and energy ledgers.
- dynamic batch reactor heat-release/sampling slice with NASA7 reaction
  enthalpy coupling, step/linear jacket temperature programs, destructive
  sampling events, and material/energy ledger evidence.
- an exothermic CSTR multiple-steady-state reference case with analytical
  energy-balance roots, stability classification, and a reactor model card.
- local equation-of-state calculations for ideal gas, Peng-Robinson, and SRK
  states with compressibility roots, explicit root-selection policies,
  fugacity coefficients, residual enthalpy, residual entropy, residual Gibbs
  energy, and model-card evidence.
- phase-equilibrium utilities for ideal, Margules, Wilson, and NRTL activity
  coefficients, Raoult K-values, isothermal flash, bubble/dew pressure, and
  liquid-liquid extraction splits.
- reaction-equilibrium and electrolyte utilities for mass-action reaction
  extents, van't Hoff equilibrium constants, fixed-TP ideal Gibbs minimization,
  weak-acid pH, water ion product, precipitation, charge balance, ionic
  strength, and solid solubility.
- electrochemical thermodynamics and charge accounting for Nernst equilibrium
  potentials, Butler-Volmer currents, Faraday charge-to-extent conversion,
  Faradaic efficiency, and electrical-work ledgers.
- downstream separation unit operations for multistage extraction,
  evaporation, VLE-coupled shortcut distillation, crystallization, filtration,
  drying, and purity/recovery/cost/risk scoring.
- fluid-mechanics and heat-transfer kernels for Reynolds/Prandtl/Peclet/Nusselt
  numbers, explicit Nusselt branch metadata, Darcy friction factors, pipe
  pressure drop, pump work, mixing power, jacket heat transfer, counterflow heat
  exchangers with hot/cold duty-balance checks, packed-bed pressure drop, and
  homogeneous two-phase pressure-drop proxies.
- optional reference-backend validation helpers for locally comparing selected
  ChemWorld formulas against `chemicals`, `fluids`, and later heavier
  scientific backends without making them runtime dependencies.

Design rules:

- keep specs serializable with plain JSON types;
- fail early on unknown elements, invalid phases, invalid units, or invalid
  fractions;
- fail early on unsupported property equations, missing coefficients,
  unit-dimension mismatches, phase-incompatible mixtures, duplicate policy
  tags, and component-disallowed property correlations;
- keep property correlations separate from component identity;
- keep mechanism definitions separate from reactor and task logic;
- keep species thermochemistry separate from kinetic rate-law parameters except
  when a rate law explicitly declares a thermochemical equilibrium source;
- keep mechanism scenario cards as the bridge between physical mechanism,
  benchmark task semantics, initial conditions, and qualitative expectations;
- keep virtual instruments as observation kernels over species amounts and
  processed estimates, not as hidden-state dumps;
- keep reactor residence time, feed/outlet flow, and heat-transfer contracts
  explicit;
- keep EOS component critical properties, mixture parameters, phase-root
  selection, fugacity outputs, residual properties, and departure metadata
  inspectable;
- keep phase-equilibrium models explicit about activity assumptions,
  vapor-pressure inputs, partition coefficients, and mass-balance errors;
- keep reaction-equilibrium and electrolyte models explicit about fixed
  constraints, supplied Gibbs energies, activity proxies, charge balance, phase
  restrictions, saturation state, and nonnegative extents or species amounts;
- keep electrochemical models explicit about sign conventions, electron number,
  activities, overpotential, Faradaic charge, electrical work, and the absence
  of full-cell effects such as ohmic drop or double-layer dynamics unless those
  effects have their own validated slice;
- keep unit-operation results as named outlet streams plus cost, risk,
  heat-duty, solvent-loss, and material-balance ledgers;
- keep transport/equipment calculations explicit about SI units, flow regime,
  pressure-drop components, heat-duty sign conventions, Nusselt-correlation
  validity limits, exchanger duty residuals, and equipment metadata;
- declare property units and validity ranges on every correlation;
- reject unbalanced reaction networks before simulation;
- add optional reference-backend comparisons only as skipped tests or adapters;
- do not copy source code from `reference_repos/`.
