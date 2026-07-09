# ChemWorld PhysChem Core TODO

This roadmap defines how ChemWorld will independently implement a compact,
auditable physical-chemistry and chemical-engineering core. External open-source
projects are used as a feature map and validation inspiration only. We do not
copy their source code into ChemWorld.

Scope note: this file tracks the first foundation/lite batch. After P1-P12 are
settled, professional hardening moves to `TODO_PROFESSIONAL.md`. A checked item
in this file means "local ChemWorld foundation exists", not "professional
library parity".

## Two-Person Active Work Board

`TODO.md` is the shared source of truth for current work. Before coding, pull
`origin/main`, claim the task here with a real owner, commit that ownership
change, and push it. If the remote `TODO.md` changes while you are working,
pull immediately and update your plan before continuing. When one task is
finished, update its status and push immediately.

| Item | Owner | Status | Files / Area | Next Step | Last Push |
| --- | --- | --- | --- | --- | --- |
| Docs cleanup and two-person rules | Codex | Done | `TODO.md`, `docs/`, `mkdocs.yml` | use this board for the next active task | this commit |
| P1 physchem component/spec foundation | whilesunny | Done | `src/chemworld/physchem/`, `tests/`, `docs/physchem_core_design.md` | next: start P2 property-correlation core on top of these specs | this commit |
| P2 property-correlation lite core | whilesunny | Lite Done | `src/chemworld/physchem/`, `tests/`, `docs/physchem_core_design.md` | next: add reference-validated vapor pressure, enthalpy, and transport-property cases | this commit |
| P3 reaction-network lite engine | whilesunny | Lite Done | `src/chemworld/physchem/`, `tests/`, `docs/physchem_core_design.md`, `configs/mechanisms/` | next: add Cantera-comparable ODE and rate-law validation cases | this commit |
| P4 reactor-model lite core | whilesunny | Lite Done | `src/chemworld/physchem/reactors.py`, `tests/`, `docs/physchem_core_design.md` | next: add Cantera/IDAES-style reactor validation and multi-steady-state CSTR case | this commit |
| P5 EOS lite core | whilesunny | Lite Done | `src/chemworld/physchem/eos.py`, `tests/`, `docs/physchem_core_design.md` | next: validate PR/SRK against controlled CoolProp/thermo/teqp cases | this commit |
| P6 phase-equilibrium lite core | whilesunny | Lite Done | `src/chemworld/physchem/equilibrium.py`, `tests/`, `docs/physchem_core_design.md` | next: add Wilson/UNIQUAC, stability tests, and phasepy/thermo validation | this commit |
| P7 separation and unit operations | whilesunny | Lite + Reference Slice | `src/chemworld/physchem/separations.py`, `tests/`, `docs/physchem_core_design.md` | next: extend extraction/crystallization and rigorous columns beyond the VLE shortcut distillation slice | this commit |
| P8 fluid mechanics and heat-transfer lite core | whilesunny | Lite Done | `src/chemworld/physchem/transport.py`, `tests/test_transport.py`, `docs/physchem_core_design.md` | next: validate pressure-drop/heat-transfer correlations against fluids and public examples | this commit |
| P9 equilibrium-chemistry lite core | whilesunny | Lite Done | `src/chemworld/physchem/equilibrium_chemistry.py`, `tests/test_equilibrium_chemistry.py`, `docs/physchem_core_design.md` | next: add Reaktoro-style equilibrium validation and pH/precipitation benchmark tasks | this commit |
| P10 mechanism and scenario lite library | whilesunny | Lite Done | `configs/mechanisms/`, `configs/scenarios/`, `src/chemworld/physchem/mechanism_library.py`, `tests/`, `docs/physchem_core_design.md` | next: add reference-validated mechanism cards and task bindings | this commit |
| P11 synthetic instrument and spectroscopy layer | whilesunny | Lite Done | `src/chemworld/physchem/spectroscopy.py`, `src/chemworld/world/spectra.py`, `tests/`, `docs/physchem_core_design.md` | next: add public calibration examples and empirical spectrum anchors | this commit |
| P12 optional reference-backend validation | whilesunny | Review | `src/chemworld/physchem/reference_validation.py`, `tests/reference/`, `docs/physchem_core_design.md`, `TODO.md` | next: add controlled CoolProp/Cantera/Reaktoro/pycalphad comparison cases when dependencies are available | `f4172fe` |
| PhysChem maturity audit and proxy de-risking | whilesunny | Done | `TODO.md`, `TODO_PROFESSIONAL.md`, `docs/physchem_maturity_audit.md`, `docs/professional_todo.md`, `docs/physchem_core_design.md` | use `TODO_PROFESSIONAL.md` for post-P1-P12 professional hardening | this commit |
| P1/P2 audit and hardening | whilesunny | Done | `src/chemworld/physchem/specs.py`, `src/chemworld/physchem/properties.py`, `tests/`, `docs/physchem_core_design.md`, `TODO.md` | next: start P12 optional reference-backend validation after choosing first comparison targets | this commit |
| Code review audit and separation-card cleanup | whilesunny | Done | `src/chemworld/physchem/separations.py`, `src/chemworld/physchem/separation_cards.py`, `docs/code_review_audit.md` | next: extract remaining model-card functions into `*_cards.py` modules one slice at a time | this commit |
| PhysChem model-card metadata externalization | whilesunny | Done | `src/chemworld/physchem/*_cards.py`, model-card exports, audit docs | next: split `properties.py` by physical property family without changing numerical behavior | this commit |
| PhysChem properties module split | whilesunny | Done | `src/chemworld/physchem/properties.py`, property-family modules, tests, audit docs | next: split `reactors.py` by reactor family and solver helpers | this commit |
| PhysChem reactors module split | whilesunny | Done | `src/chemworld/physchem/reactors.py`, reactor-family modules, tests, audit docs | next: continue splitting `reaction_network.py` into integration core, thermochemical coupling, sensitivities, and loaders | this commit |
| Tutorial curriculum hardening and SOTA gap audit | whilesunny | Done | `notebooks/tutorials/`, `docs/`, SOTA references | next: continue splitting `reaction_network.py` into integration core, thermochemical coupling, sensitivities, and loaders | this commit |
| Tutorial encoding repair and workload expansion | whilesunny | Done | `notebooks/`, tutorial guidance generator, docs/tests | next: continue splitting `reaction_network.py` into integration core, thermochemical coupling, sensitivities, and loaders | this commit |
| High-level ChemWorld overview document | whilesunny | Done | `docs/`, `mkdocs.yml` | next: continue splitting `reaction_network.py` into integration core, thermochemical coupling, sensitivities, and loaders | this commit |
| Multi-step recipe alias usability | whilesunny | Done | `src/chemworld/action_codec.py`, tests/docs | common user-facing action aliases accepted; purification sequence documented and tested | this commit |
| Runtime v2 transactional kernel architecture | whilesunny | Done | `src/chemworld/runtime/`, `src/chemworld/envs/`, `src/chemworld/foundation/`, tests/docs | next: split `runtime/domain_services.py` and replace remaining fixed-species service logic with compiled-mechanism mappings | this commit |
| Runtime v2 mechanism-driven domain services | whilesunny | Done | `src/chemworld/runtime/`, `src/chemworld/foundation/`, `src/chemworld/world/`, tests/docs | mechanism species-role mapping, product phase-ledger key, non-fixed electrochemical runtime tests, and docs are complete | this commit |
| Runtime v2 observation/scoring service split | whilesunny | Done | `src/chemworld/runtime/`, tests/docs | observation truth, scoring, raw signal assembly, processed estimates, and uncertainty now live in `runtime/observation_services.py` | this commit |
| Runtime v2 operation-record service split | whilesunny | Done | `src/chemworld/runtime/`, tests/docs | operation record assembly, constitution summaries, measurement cost/sample logging, and state-delta summaries now live in `runtime/record_services.py` | this commit |
| Runtime v2 reaction/thermal service split | whilesunny | Done | `src/chemworld/runtime/`, tests/docs | reaction advancement, heat/wait integration, energy-ledger updates, and pressure/risk projection now live in `runtime/reaction_thermal_services.py` | this commit |
| Runtime v2 phase/separation service split | whilesunny | Done | `src/chemworld/runtime/`, tests/docs | phase ledger helpers and extraction-style downstream separation operations now live in `runtime/phase_separation_services.py` | this commit |
| Runtime v2 electrochemical service split | whilesunny | Done | `src/chemworld/runtime/`, tests/docs | potential setup and electrolysis conversion logic now live in `runtime/electrochemical_services.py` | this commit |
| Runtime v2 instrument-cost service split | whilesunny | Done | `src/chemworld/runtime/`, tests/docs | measurement cost, destructive sample consumption, and final-assay marker updates now live in `runtime/instrument_cost_services.py` | this commit |
| Runtime v2 crystallization service split | whilesunny | Done | `src/chemworld/runtime/`, tests/docs | seed addition, cooling crystallization, crystal purity/recovery metadata, and crystal filtration now live in `runtime/crystallization_services.py` | this commit |
| Runtime v2 distillation service split | whilesunny | Done | `src/chemworld/runtime/`, tests/docs | shortcut VLE distillation, distillate purity/recovery metadata, heat-duty/cost/risk ledgers, and fraction collection now live in `runtime/distillation_services.py` | this commit |
| Runtime v2 flow service split | whilesunny | Done | `src/chemworld/runtime/`, tests/docs | flow-rate setup, residence-time reaction advancement, flow conversion metadata, and flow campaign ledger updates now live in `runtime/flow_services.py` | this commit |
| Runtime v2 primitive operation service split | whilesunny | Done | `src/chemworld/runtime/`, tests/docs | reagent/solvent/catalyst addition, sampling, quench, evaporation, and invalid-action penalty now live in `runtime/primitive_services.py` | this commit |
| Reaction-network specs split | whilesunny | Done | `src/chemworld/physchem/`, tests/docs | species/rate-law/reaction specs, reaction-equation parsing, and mechanism dict helpers now live in `reaction_network_specs.py` | this commit |
| Reaction-network rate-law split | whilesunny | Done | `src/chemworld/physchem/`, tests/docs | rate-law constants, parameter validation, mass-action/Arrhenius/reversible-rate helpers, and reaction lookup now live in `reaction_rate_laws.py` | this commit |
| Reaction-network reference-case split | whilesunny | Done | `src/chemworld/physchem/`, tests/docs | analytical ODE reference cases, Cantera-comparable fixtures, and reference-case evaluation now live in `reaction_reference_cases.py` | this commit |
| Reaction-network sensitivity split | whilesunny | Done | `src/chemworld/physchem/reaction_network.py`, `src/chemworld/physchem/reaction_sensitivity.py`, tests/docs | finite-difference sensitivity reports, explanation rankings, and kinetic candidate scanning now live in `reaction_sensitivity.py` while the reaction-network facade preserves public imports | this commit |
| Runtime v2 phase-ledger helper split | whilesunny | Done | `src/chemworld/runtime/phase_separation_services.py`, `src/chemworld/runtime/phase_ledger_services.py`, tests/docs | phase-ledger normalization, species role mapping, process metrics, and state replacement helpers now live in `phase_ledger_services.py`; extraction operation handlers remain in `phase_separation_services.py` | this commit |
| ChemWorldEnv spaces and observation codec split | whilesunny | Done | `src/chemworld/envs/chemworld_env.py`, `src/chemworld/envs/spaces.py`, tests/docs | Gym action/observation spaces, nullable scalar boxes, and observation array codec now live in `envs/spaces.py`; `ChemWorldEnv` stays focused on reset/step/render orchestration | this commit |
| ChemWorldEnv reporting split | whilesunny | Done | `src/chemworld/envs/chemworld_env.py`, `src/chemworld/envs/reports.py`, tests/docs | task_info, constitution summary, render text, and step info payload construction now live in `envs/reports.py`; `ChemWorldEnv` keeps thin report proxy methods | this commit |
| Runtime v2 mechanism compiler split | whilesunny | Done | `src/chemworld/runtime/mechanisms.py`, `src/chemworld/runtime/mechanism_manifest.py`, `src/chemworld/runtime/mechanism_validation.py`, tests/docs | manifest, validation, hashing, and role-contract helpers now live outside the mechanism compiler facade without changing compiled mechanism behavior | this commit |
| Runtime v2 kernel/profile contract split | whilesunny | Active | `src/chemworld/runtime/kernels.py`, `src/chemworld/runtime/profiles.py`, `src/chemworld/runtime/kernel_contracts.py`, `src/chemworld/runtime/kernel_registry.py`, tests/docs | split task profiles, kernel data contracts, service operation kernel, and registry plumbing without changing transaction behavior | this commit |
| Runtime v2 golden characterization | whilesunny | Done | `tests/`, runtime/env docs | scripted golden final-assay trajectories now cover all formal tasks, including campaign/single-experiment semantics and runtime transaction metadata | this commit |
| Runtime v2 import and dispatch boundary audit | whilesunny | Done | `src/chemworld/envs/`, `src/chemworld/runtime/`, tests/docs | env/runtime import boundaries and ChemWorldEnv process-operation dispatch delegation are now enforced by architecture tests | this commit |
| Runtime v2 transaction replay golden | whilesunny | Done | `src/chemworld/eval/verify.py`, `tests/`, docs | verifier now replays and compares mechanism hash, kernel metadata, world events, state-patch summaries, transaction status, and state-delta summaries | this commit |
| Runtime v2 typed phase-ledger primary state | whilesunny | Done | `src/chemworld/foundation/state.py`, `src/chemworld/runtime/phase_separation_services.py`, tests/docs | phase/separation services now read/write typed `PhaseLedger`, destructive sampling keeps phases and scalar adapter aligned, and constitution rejects metadata phase-ledger primary state | this commit |
| Runtime v2 typed equipment-ledger primary state | whilesunny | Done | `src/chemworld/foundation/state.py`, `src/chemworld/foundation/constitution.py`, `src/chemworld/runtime/flow_services.py`, `src/chemworld/runtime/electrochemical_services.py`, tests/docs | flow and electrochemical setup now live in typed `EquipmentLedger` records, preconditions read equipment settings, and metadata keeps only derived process metrics | this commit |
| Runtime v2 batch-reactor typed operation settings | whilesunny | Done | `src/chemworld/foundation/state.py`, `src/chemworld/runtime/primitive_services.py`, `src/chemworld/runtime/reaction_thermal_services.py`, `src/chemworld/world/reaction_kernel.py`, tests/docs | solvent, catalyst, and stirring settings now live in typed reactor/mixer equipment settings; runtime metadata is rejected as primary state for these keys | this commit |
| Runtime v2 typed phase-status primary state | whilesunny | Done | `src/chemworld/foundation/state.py`, `src/chemworld/foundation/constitution.py`, `src/chemworld/runtime/phase_separation_services.py`, `src/chemworld/world/separation_kernel.py`, tests/docs | phase-system readiness, settled status, and selected phase now live in typed `PhaseLedger`; constitution and golden tests reject metadata primary state for these keys | this commit |
| Runtime v2 typed final-assay instrument status | whilesunny | Done | `src/chemworld/foundation/state.py`, `src/chemworld/foundation/constitution.py`, `src/chemworld/runtime/instrument_cost_services.py`, tests/docs | final-assay completion and timing now live in typed `instrument:final_assay` equipment status, with constitution and golden tests blocking metadata fallback | this commit |
| Runtime v2 typed crystallizer seed status | whilesunny | Done | `src/chemworld/foundation/state.py`, `src/chemworld/foundation/constitution.py`, `src/chemworld/runtime/crystallization_services.py`, tests/docs | crystallization seed status and seed mass now live in typed `crystallizer` equipment settings, with constitution and golden tests blocking metadata fallback | this commit |
| Runtime v2 typed crystallization output phases | whilesunny | Done | `src/chemworld/foundation/constitution.py`, `src/chemworld/runtime/crystallization_services.py`, `src/chemworld/world/separation_kernel.py`, tests/docs | crystallized product and impurity amounts now live in typed solid/mother-liquor phase records, with filter preconditions and constitution checks using typed phases | this commit |
| Runtime v2 typed distillation output phases | whilesunny | Done | `src/chemworld/foundation/constitution.py`, `src/chemworld/runtime/distillation_services.py`, tests/docs | distillate product and impurity amounts now live in typed distillate/bottoms phase records; collect-fraction preconditions and constitution checks read typed phases | this commit |
| Runtime v2 final audit and legacy fallback boundary | whilesunny | Done | runtime/env/eval scans, tests/docs/TODO_PROFESSIONAL | removed batch-runtime imports and legacy species fallback boundaries are enforced; mechanism-owned initial-state removal is tracked as PRO-RUNTIME-A | this commit |
| PRO-RUNTIME-A mechanism-owned initial-state generator | whilesunny | Done | `configs/mechanisms/`, `configs/scenarios/`, `src/chemworld/world/scenario.py`, `src/chemworld/world/state_factory.py`, `src/chemworld/runtime/species.py`, tests/docs | scenario initial states now use compiled mechanism species, roles, and initial-amount policy; lite reaction backend slots are mapped through mechanism roles, with full fallback removal still tracked in `TODO_PROFESSIONAL.md` | this commit |
| PRO-RUNTIME-A compiled reaction integrator | whilesunny | Done | `src/chemworld/runtime/mechanisms.py`, `src/chemworld/world/reaction_kernel.py`, `src/chemworld/runtime/reaction_thermal_services.py`, tests/docs | heat/wait and flow reaction advancement now use compiled mechanism species, stoichiometry, rate laws, and reaction enthalpies; mechanism initial-amount policy now drives multi-reactant reagent charging | this commit |
| PRO-RUNTIME-A runtime compiled mechanism required | whilesunny | Done | `src/chemworld/runtime/reaction_thermal_services.py`, `src/chemworld/world/reaction_kernel.py`, `src/chemworld/runtime/species.py`, tests/docs | reaction/thermal runtime now requires compiled mechanisms, no longer calls `reaction_backend_species_map`, and guards against missing compiled mechanisms with regression tests | this commit |
| PRO-RUNTIME-A seven-slot reference quarantine | whilesunny | Done | `src/chemworld/world/reaction_kernel.py`, `src/chemworld/world/reaction_reference.py`, tests/docs | fixed A/P/B/D/E ODE is now quarantined in an explicit reference fixture; ordinary reaction kernel declares compiled-mechanism runtime only and architecture tests block runtime imports | this commit |
| PRO-RUNTIME-A compiled mechanism required across runtime services | whilesunny | Done | `src/chemworld/runtime/`, tests/docs | env/runtime/eval now have no `LEGACY_*` species defaults and runtime/domain/observation services require compiled mechanisms; golden scores updated after removing duplicated `initial_A_mol` counting | this commit |
| PRO-RUNTIME-A mechanism role validation at compile time | whilesunny | Done | `src/chemworld/runtime/mechanisms.py`, mechanism tests/docs | compile-time validation now separates base mechanism-library checks from stricter runtime scenario role contracts for target, impurity, initial species, and observable mappings | this commit |
| PRO-RUNTIME-B transaction record consistency | whilesunny | Done | `src/chemworld/runtime/kernels.py`, `src/chemworld/runtime/transactions.py`, tests/docs | rollback transactions now append explicit rollback patches and rebuild operation records from the committed rollback state | this commit |
| PRO-RUNTIME-C operation taxonomy and macro compiler | whilesunny | Done | `src/chemworld/world/operations.py`, `src/chemworld/world/recipes.py`, tests/docs | operation contracts now classify primitive/domain/macro/terminal steps; recipe compilation expands macros and validates compiled steps against task policy | this commit |
| PRO-RUNTIME-D domain service registry | whilesunny | Done | `src/chemworld/runtime/domain_services.py`, `src/chemworld/runtime/engine.py`, tests/docs | runtime now exposes a typed DomainServiceRegistry, operation-to-service map, and domain service ids in operation events | this commit |
| PRO-RUNTIME-E task runtime service contract | whilesunny | Done | `src/chemworld/runtime/kernels.py`, `src/chemworld/runtime/domain_services.py`, `src/chemworld/runtime/engine.py`, tests/docs | TaskRuntimeProfile now declares required domain services and runtime startup validates service/capability coverage | this commit |
| PRO-RUNTIME-F precondition rollback transaction | whilesunny | Done | `src/chemworld/runtime/`, `src/chemworld/envs/`, tests/docs | operation precondition failures now enter Runtime v2 rollback events and process-only penalty patches; schema/task/payload failures remain env-level validation failures | this commit |
| PRO-RUNTIME-G task-scoped domain-service validation | whilesunny | Done | `src/chemworld/runtime/domain_services.py`, tests/docs | domain-service validation is task-profile scoped; unrelated future operations are not required by every task runtime | this commit |
| PRO-RUNTIME-H task-specific scoring contract | whilesunny | Done | `src/chemworld/world/scoring.py`, `src/chemworld/runtime/observation_services.py`, `src/chemworld/envs/`, tests/docs | score computation now reads a task-level scoring contract instead of always using the fixed reaction score formula | this commit |
| PRO-RUNTIME-I task-specific observation contract | whilesunny | Done | `src/chemworld/world/`, `src/chemworld/runtime/observation_services.py`, `src/chemworld/envs/`, tests/docs | processed observation keys now read a task/mechanism observation contract instead of exposing every global instrument field | this commit |
| PRO-RUNTIME-J task-aware raw-signal contract | whilesunny | Done | `src/chemworld/runtime/observation_services.py`, `src/chemworld/world/spectra.py`, tests/docs | environment raw signal generation now uses task-visible public role aggregates instead of passing full hidden species ledgers to agent-visible instrument packets | this commit |
| PRO-RUNTIME-K scoring and observation contract hashes | whilesunny | Done | `src/chemworld/world/`, `src/chemworld/envs/`, `src/chemworld/data/`, `src/chemworld/eval/verify.py`, tests/docs | deterministic scoring/observation contract hashes are recorded in task info, trajectories, schemas, and replay verification | this commit |
| PRO-RUNTIME-L task/profile contract hashes | whilesunny | Done | `src/chemworld/tasks.py`, `src/chemworld/runtime/kernels.py`, `src/chemworld/envs/`, `src/chemworld/data/`, `src/chemworld/eval/verify.py`, tests/docs | deterministic task-spec and runtime-profile hashes are recorded in task info, trajectories, schemas, and replay verification | this commit |
| PRO-RUNTIME-M downstream truth role cleanup | whilesunny | Done | `src/chemworld/world/separation_kernel.py`, `src/chemworld/world/species_roles.py`, tests/docs | downstream truth calculations now aggregate typed phase ledgers by mechanism-role species and no longer keep legacy species fallback constants | this commit |
| PRO-RUNTIME-N process metric ledger | whilesunny | Done | `src/chemworld/foundation/state.py`, `src/chemworld/runtime/flow_services.py`, `src/chemworld/runtime/electrochemical_services.py`, tests/docs | flow and electrochemical derived process metrics now live in typed `ProcessLedger.metrics`, with constitution checks blocking metadata fallback and observations/records reading the typed ledger | this commit |
| PRO-RUNTIME-O downstream metric ledger cleanup | whilesunny | Done | `src/chemworld/runtime/phase_separation_services.py`, `src/chemworld/runtime/crystallization_services.py`, `src/chemworld/runtime/distillation_services.py`, `src/chemworld/world/separation_kernel.py`, tests/docs | downstream separation, crystallization, and distillation derived metrics now live in typed `ProcessLedger.metrics`, with constitution checks blocking metadata fallback | this commit |
| DOC-ZH technical architecture UTF-8 repair | whilesunny | Done | `docs/technical_architecture_zh.md`, docs | Chinese architecture report is clean UTF-8 and reflects current Runtime v2, typed ledgers, mechanism contracts, dataset/replay, local evaluation, and remaining gaps | this commit |
| DEEP-D10B dataset export hardening | whilesunny | Done | `src/chemworld/data/datasets.py`, `src/chemworld/eval/verify.py`, tests/docs | dataset cards now include schema version, replay verification summaries, protocol hash manifests, privacy summaries, and Parquet/JSONL flattening keeps protocol hashes | this commit |

Status values:

- `Planned`: available and not started.
- `Active`: one owner is working on it now.
- `Blocked`: owner cannot proceed; handoff note required.
- `Review`: pushed and waiting for the other person to inspect.
- `Lite Done`: compact ChemWorld-local implementation exists with tests, but it
  is not professional-library parity.
- `Reference Done`: implementation has controlled numerical checks against at
  least one optional reference backend.
- `Done`: complete and pushed.

Ownership rules:

- Every `Active` task must have exactly one owner.
- Do not start another person's `Active` task unless they write a handoff note.
- Claim a task by editing this table and pushing before implementation.
- Finish a task by updating this table and pushing immediately.
- Keep completed units small; avoid batching unrelated work into one delayed
  push.

## Ground Rules

- Implement ChemWorld's own code, data contracts, tests, and documentation.
- Use original equations, textbooks, papers, and public reference data when
  implementing correlations or algorithms.
- Do not vendor large external projects into the benchmark core.
- Keep heavy ecosystem integrations as optional adapters, not required
  dependencies.
- Every implemented feature must expose:
  - a JSON-friendly spec;
  - unit metadata;
  - deterministic seed behavior where applicable;
  - reference tests;
  - failure modes and validity ranges;
  - documentation explaining assumptions.

## External Project Feature Map

The projects below are not implementation dependencies for the ChemWorld core.
They define the professional capability surface we want to cover gradually.

### Cantera

Primary domain: chemical kinetics, thermodynamics, transport, and reactor
networks.

Major capabilities to learn from:

- species and phase definitions;
- YAML/CTI-like mechanism loading;
- ideal gas, condensed phase, surface, and interface phase models;
- NASA polynomial thermochemistry;
- standard-state and mixture thermodynamics;
- elementary, reversible, falloff, pressure-dependent, and surface reactions;
- Arrhenius and modified Arrhenius rate laws;
- transport property models;
- chemical equilibrium calculations;
- zero-dimensional reactor networks;
- constant-volume and constant-pressure reactors;
- walls, reservoirs, flow devices, and reactor coupling;
- sensitivity analysis;
- one-dimensional flame and reacting-flow solvers;
- Python API around compiled numerical kernels.

ChemWorld independent implementation target:

- implement a compact reaction-network engine, not a detailed combustion
  platform;
- support YAML/JSON mechanism specs;
- support general stoichiometric matrices and multiple rate laws;
- keep Cantera as an optional validation/backend adapter later.

### CoolProp

Primary domain: high-accuracy thermophysical properties.

Major capabilities to learn from:

- pure-fluid and pseudo-pure-fluid properties;
- mixture properties;
- Helmholtz-energy equations of state;
- cubic equations of state;
- IF97 water/steam properties;
- humid-air properties;
- incompressible fluids and brines;
- phase identification;
- saturation properties;
- phase envelopes;
- partial derivatives and transport properties;
- tabular interpolation;
- wrappers for many languages.

ChemWorld independent implementation target:

- implement only a compact property backend:
  - vapor pressure;
  - liquid density;
  - heat capacity;
  - enthalpy;
  - latent heat;
  - viscosity proxy;
  - simple mixture rules;
  - Peng-Robinson and SRK;
  - flash calculations.
- keep CoolProp as optional reference validation, not core dependency.

### thermo

Primary domain: chemical-engineering thermodynamics in Python.

Major capabilities to learn from:

- pure-component constants;
- chemical object model;
- mixture object model;
- heat capacity correlations;
- vapor pressure correlations;
- volume and density correlations;
- viscosity and thermal-conductivity correlations;
- surface-tension correlations;
- enthalpy and entropy calculations;
- equations of state;
- cubic equation-of-state mixtures;
- fugacity coefficients;
- activity-coefficient models;
- flash calculations;
- vapor-liquid equilibrium;
- liquid-liquid equilibrium;
- property packages for process calculations.

ChemWorld independent implementation target:

- implement a smaller `physchem.properties` and `physchem.equilibrium`
  package;
- define a minimal component database and correlation registry;
- implement only benchmark-needed equations first.

### chemicals

Primary domain: chemical property correlations and data utilities.

Major capabilities to learn from:

- critical properties;
- acentric factor and corresponding-states utilities;
- vapor pressure;
- heat capacity;
- phase-change enthalpy;
- liquid and gas molar volume;
- virial volume;
- surface tension;
- solubility and Henry-law constants;
- combustion and reaction property helpers;
- safety and exposure data utilities;
- environmental property helpers;
- periodic-table and formula utilities;
- data lookup and correlation selection.

ChemWorld independent implementation target:

- implement a compact correlation library with explicit validity ranges;
- provide only the correlations used by current and near-term tasks;
- avoid embedding large data tables until provenance and licensing are clear.

### fluids

Primary domain: fluid mechanics and equipment calculations.

Major capabilities to learn from:

- friction factor correlations;
- pipe pressure drop;
- fittings and minor losses;
- pumps and compressors;
- control valves;
- two-phase pressure drop;
- open-channel flow;
- packed-bed pressure drop;
- particle settling;
- mixing and agitation correlations;
- separator and tank utilities;
- dimensionless numbers;
- flow-meter correlations;
- safety valve and relief calculations.

ChemWorld independent implementation target:

- implement only the process-interaction pieces needed for virtual labs:
  - Reynolds number;
  - friction factor;
  - pipe/tube pressure drop;
  - simple pump work;
  - mixing intensity;
  - packed-bed pressure drop later;
  - two-phase pressure drop later.

### phasepy

Primary domain: phase-equilibrium calculations.

Major capabilities to learn from:

- cubic equations of state;
- activity-coefficient models;
- vapor-liquid equilibrium;
- liquid-liquid equilibrium;
- vapor-liquid-liquid equilibrium;
- bubble and dew point calculations;
- flash calculations;
- phase stability;
- parameter fitting/regression;
- interfacial-tension and square-gradient-style calculations.

ChemWorld independent implementation target:

- replace the current partition proxy with:
  - ideal partition model;
  - NRTL/Wilson/UNIQUAC-lite;
  - binary and ternary LLE;
  - VLE bubble/dew/flash;
  - phase-stability checks.

### IDAES

Primary domain: process systems engineering, optimization, and flowsheets.

Major capabilities to learn from:

- Pyomo-based process models;
- property packages;
- unit model library;
- steady-state flowsheets;
- dynamic flowsheets;
- initialization workflows;
- algebraic and differential-algebraic optimization;
- parameter estimation;
- costing models;
- uncertainty and sensitivity workflows;
- power, carbon-capture, and chemical-process examples;
- solver integration and model diagnostics.

ChemWorld independent implementation target:

- do not reproduce IDAES;
- implement lightweight process-unit contracts:
  - unit state;
  - inlet/outlet ports;
  - material balance;
  - energy balance;
  - cost/risk accounting;
  - simplified optimization hooks.
- keep an IDAES adapter as a future professional backend.

### Reaktoro

Primary domain: chemical equilibrium, kinetics, and reactive transport.

Major capabilities to learn from:

- Gibbs-energy-minimization equilibrium;
- thermodynamic databases;
- aqueous, gaseous, liquid, mineral, and surface phases;
- activity models;
- equilibrium specs and constraints;
- chemical kinetics;
- reactive transport;
- inverse equilibrium problems;
- pH, charge, alkalinity, and geochemical constraints;
- precipitation/dissolution systems.

ChemWorld independent implementation target:

- implement a small equilibrium module:
  - mass-action equilibrium;
  - reaction extent solving;
  - acid/base toy equilibria later;
  - precipitation/dissolution proxy later.
- keep Reaktoro as optional validation for equilibrium-heavy tasks.

### pycalphad

Primary domain: CALPHAD thermodynamics and phase diagrams.

Major capabilities to learn from:

- TDB database parsing;
- Gibbs-energy model construction;
- multicomponent, multiphase equilibrium;
- phase diagram calculation;
- property calculation;
- equilibrium result data structures;
- parameter selection and fitting workflows;
- plotting and mapping of phase boundaries.

ChemWorld independent implementation target:

- do not implement full CALPHAD in the core;
- implement a small `solid_phase_equilibrium` abstraction;
- use pycalphad-style ideas only for future materials tasks.

### teqp

Primary domain: modern equations of state and thermodynamic derivatives.

Major capabilities to learn from:

- Helmholtz-energy equation-of-state formulation;
- multiparameter EOS models;
- cubic EOS support;
- mixture models;
- thermodynamic derivatives;
- critical point and phase-envelope tracing;
- fast numerical kernels;
- JSON-style model specifications.

ChemWorld independent implementation target:

- implement JSON-friendly EOS specs;
- implement Peng-Robinson and SRK first;
- add Helmholtz-style abstractions later if justified.

### thermopack

Primary domain: equation-of-state and phase-equilibrium package.

Major capabilities to learn from:

- cubic EOS;
- CPA EOS;
- SAFT-family EOS;
- association models;
- multiphase flash;
- phase envelopes;
- stability analysis;
- binary interaction parameters;
- hydrate and advanced phase behavior in specialized cases.

ChemWorld independent implementation target:

- focus on cubic EOS and simple activity models first;
- leave SAFT/CPA/hydrate behavior for long-term optional tasks.

### RMG-Py

Primary domain: reaction mechanism generation.

Major capabilities to learn from:

- species graph representation;
- thermochemistry estimation;
- kinetics family databases;
- reaction template matching;
- automatic mechanism generation;
- pressure-dependent reaction networks;
- reactor simulation;
- sensitivity and model analysis;
- solvation and liquid-phase extensions;
- mechanism reduction workflows.

ChemWorld independent implementation target:

- do not implement automatic mechanism generation initially;
- implement explicit mechanism loading and validation first;
- later add a small reaction-template toy generator for benchmark tasks.

### Optional Future: Heat-Transfer Utilities

Primary domain: heat-transfer correlations and equipment calculations.

Major capabilities to implement independently when needed:

- conduction through walls;
- convection coefficients;
- Nusselt/Reynolds/Prandtl correlations;
- jacketed reactor heat transfer;
- heat exchanger effectiveness;
- boiling/condensation proxies;
- thermal runaway indicators.

## ChemWorld Independent Implementation Plan

Maturity semantics for this section:

- A checked item means the compact ChemWorld-local version exists and is
  covered by local tests.
- It does not mean parity with Cantera, CoolProp, thermo, phasepy, IDAES,
  Reaktoro, pycalphad, teqp, thermopack, or RMG-Py.
- A module becomes `Reference Done` only after controlled optional tests compare
  selected numerical cases against a reference backend and document tolerances.
- A module becomes professional-grade only after validity ranges, model-limit
  notes, reference comparisons, failure modes, and task-level integration are
  all documented.
- The next-stage professional TODO expansion must wait until this twelve-area
  batch is settled. That later file should decompose every physical module into
  concrete implementation slices with reference targets and validation cases,
  not pre-fill the roadmap with proxy placeholders.

Current maturity summary:

| Area | Current maturity | Main reason it is not professional-grade yet |
| --- | --- | --- |
| P1 specs/units | Local foundation | Needs broader schema generation and component database governance |
| P2 properties | Lite with curated reference slice | Broader component coverage, liquid/solid Cp, latent heat, derivatives, and CoolProp checks remain open |
| P3 reaction networks | Lite with reference ODE slice | No Cantera-comparable thermochemistry, falloff, pressure dependence, or sensitivity validation |
| P4 reactors | Lite with CSTR multiplicity slice | Reactor models are ODE benchmark kernels, not industrial reactor-network solvers |
| P5 EOS | Lite | PR/SRK are local implementations without broad property-package validation |
| P6 phase equilibrium | Lite | No full phase stability, VLLE, Wilson/UNIQUAC, or robust parameter fitting |
| P7 separations | Proxy/lite | Unit operations are material-conserving benchmark proxies, not rigorous equipment models |
| P8 transport/heat transfer | Lite with pipe-flow reference slice | Useful correlations exist, but only limited heat-transfer reference checks are active |
| P9 equilibrium chemistry | Lite/proxy | No Gibbs minimization or database-backed aqueous/mineral equilibrium |
| P10 scenarios | Lite library | Mechanisms are curated benchmark scenarios, not generated mechanisms |
| P11 spectroscopy | Synthetic/proxy | Generates realistic signals, not database-grade spectral prediction |
| P12 reference validation | Partial | Chemicals, fluids, thermo, and selected Cantera rate checks execute; CoolProp/Reaktoro/pycalphad coverage remains open |

### P0: Governance, Scope, and Audit

- [ ] Create `docs/third_party_feature_map.md` from this TODO.
- [ ] Add a no-source-copy policy to contributor docs.
- [x] Add `docs/physchem_maturity_audit.md`.
- [x] Add `TODO_PROFESSIONAL.md` for the post-P1-P12 professional roadmap.
- [x] Add `docs/professional_todo.md` for the rendered professional roadmap.
- [x] Add a `docs/physchem_core_design.md` architecture page.
- [x] Add `src/chemworld/physchem/README.md` explaining module boundaries.
- [x] Add tests confirming the core package imports without optional external
      scientific backends.
- [ ] Add optional extras only after adapters exist:
  - [x] `physchem-ref`
  - [ ] `cantera`
  - [ ] `coolprop`
  - [ ] `idaes`
  - [ ] `equilibrium`

### P1: Data Structures and Units

- [x] `ComponentSpec`
  - [x] identifier;
  - [x] formula;
  - [x] molecular weight;
  - [x] charge;
  - [x] default phase;
  - [x] safety tags;
  - [x] allowed property correlations.
- [x] `MixtureSpec`
  - [x] component ids;
  - [x] mole fractions;
  - [x] mass fractions;
  - [x] phase label;
  - [x] temperature and pressure.
- [x] `PropertyCorrelation`
  - [x] equation id;
  - [x] coefficients;
  - [x] units;
  - [x] validity range;
  - [x] source note.
- [x] Extend unit checks for:
  - [x] pressure;
  - [x] energy;
  - [x] power;
  - [x] molar enthalpy;
  - [x] mass density;
  - [x] viscosity;
  - [x] heat-transfer coefficient.

Acceptance tests:

- [x] Formula parser conserves elements for `C2H6O`, `H2O`, `CO2`.
- [x] Mole fraction and mass fraction conversions are reversible.
- [x] Invalid units fail before transition kernels run.

### P2: Property Correlation Core

- [x] Vapor pressure:
  - [x] Antoine;
  - [x] Wagner-like placeholder;
  - [x] validity warnings.
- [x] Heat capacity:
  - [x] polynomial Cp;
  - [x] enthalpy integral;
  - [x] sensible heat.
- [x] Phase-change properties:
  - [x] heat of vaporization;
  - [x] heat of fusion placeholder.
- [x] Density:
  - [x] ideal gas density;
  - [x] liquid density correlation;
  - [x] mixture density rule.
- [x] Viscosity:
  - [x] liquid viscosity correlation;
  - [x] gas viscosity placeholder;
  - [x] mixture viscosity rule.
- [x] Surface tension:
  - [x] simple temperature-dependent proxy.
- [x] Safety properties:
  - [x] flammability proxy;
  - [x] volatility risk proxy;
  - [x] thermal hazard proxy.

Acceptance tests:

- [x] Water vapor pressure increases monotonically with temperature.
- [x] Cp integral has correct sign and units.
- [x] Density and viscosity remain positive within validity ranges.

### P3: General Reaction Network Engine

- [x] `SpeciesSpec`
  - [x] element composition;
  - [x] phase;
  - [x] charge;
  - [x] catalyst flag;
  - [x] observable aliases.
- [x] `ReactionSpec`
  - [x] equation string;
  - [x] stoichiometric coefficients;
  - [x] reversible flag;
  - [x] rate-law id;
  - [x] heat of reaction;
  - [x] equilibrium model id.
- [x] `ReactionNetworkSpec`
  - [x] species list;
  - [x] reaction list;
  - [x] stoichiometric matrix;
  - [x] element matrix;
  - [x] conservation checks.
- [x] Mechanism loader:
  - [x] JSON;
  - [x] YAML;
  - [x] schema validation;
  - [x] deterministic scenario parameter perturbation.
- [x] Rate laws:
  - [x] mass action;
  - [x] Arrhenius;
  - [x] modified Arrhenius;
  - [x] reversible Arrhenius;
  - [x] catalytic activity multiplier;
  - [x] catalyst deactivation;
  - [x] Langmuir-Hinshelwood-lite;
  - [x] Michaelis-Menten-lite;
  - [ ] electrochemical Butler-Volmer-lite later.

Acceptance tests:

- [x] Stoichiometric matrix for arbitrary network is correct.
- [x] Element balance catches impossible reactions.
- [x] `A -> P -> D` reproduces current qualitative behavior.
- [x] Network with 20 species and 30 reactions runs deterministically.

### P4: Reactor Models

- [x] Batch reactor:
  - [x] mole balance;
  - [x] energy balance;
  - [x] variable volume;
  - [x] heat-transfer jacket.
- [x] Semi-batch reactor:
  - [x] feed schedule;
  - [x] addition-limited selectivity;
  - [x] runaway risk.
- [x] CSTR:
  - [x] steady-state solve;
  - [x] dynamic startup;
  - [x] residence time;
  - [x] multiple steady-state example.
- [x] PFR:
  - [x] axial coordinate integration;
  - [x] temperature profile;
  - [ ] pressure-drop placeholder.
- [ ] Reactive flash:
  - [ ] reaction plus phase split;
  - [ ] equilibrium-limited reaction.
- [ ] Electrochemical cell:
  - [ ] charge balance;
  - [ ] current efficiency;
  - [ ] potential-selectivity proxy.

Acceptance tests:

- [ ] Batch and CSTR agree in limiting cases where expected.
- [x] PFR conversion increases with residence time.
- [x] Semi-batch feed rate changes selectivity.
- [x] Reactor state never creates negative species.

### P5: Equations of State

- [x] Ideal gas EOS.
- [x] Peng-Robinson EOS:
  - [x] pure component parameters;
  - [x] mixture rules;
  - [x] compressibility roots;
  - [x] fugacity coefficients.
- [x] SRK EOS:
  - [x] pure component parameters;
  - [x] mixture rules;
  - [x] fugacity coefficients.
- [x] Phase identification by root selection.
- [ ] Residual enthalpy placeholder.
- [x] EOS JSON spec.

Acceptance tests:

- [x] Ideal gas limit matches `PV=nRT`.
- [x] PR roots are real/filtered and stable.
- [x] Fugacity coefficients remain positive.

### P6: Activity Models and Phase Equilibrium

- [x] Ideal-solution activity model.
- [x] Margules binary model.
- [x] Wilson-lite.
- [x] NRTL-lite.
- [ ] UNIQUAC-lite.
- [x] Binary LLE solver.
- [ ] Ternary LLE placeholder.
- [x] Bubble point.
- [x] Dew point.
- [x] Isothermal flash.
- [ ] Adiabatic flash later.
- [ ] Phase-stability heuristic.

Acceptance tests:

- [x] Ideal binary flash has expected limiting behavior.
- [x] LLE split conserves material.
- [x] Increasing extractant volume changes recovery/purity tradeoff.
- [x] Distillation task uses VLE rather than fixed proxy where enabled.

### P7: Separation and Unit Operations

- [x] Liquid-liquid extraction:
  - [x] equilibrium stage;
  - [x] finite mixing efficiency;
  - [x] entrainment loss;
  - [x] solvent loss;
  - [ ] washing stages.
- [x] Evaporation:
  - [x] VLE-driven removal;
  - [x] heat duty;
  - [x] concentration risk.
- [x] VLE shortcut distillation:
  - [x] Raoult/activity-coefficient K-values;
  - [x] relative volatility from VLE keys;
  - [x] Fenske-style distillate/bottoms distribution ratios;
  - [x] reflux-scaled effective stages;
  - [x] fraction cut and heat-duty ledger.
- [x] Crystallization:
  - [x] solubility curve;
  - [x] supersaturation;
  - [x] nucleation/growth proxy;
  - [x] filtration loss.
- [x] Filtration:
  - [x] cake recovery;
  - [x] impurity retention;
  - [x] wash loss.
- [x] Drying:
  - [x] residual solvent;
  - [x] thermal degradation risk.

Acceptance tests:

- [x] Every unit operation has material balance checks.
- [x] Purity/recovery tradeoff is nontrivial.
- [x] Excessive purification increases cost and may reduce score.

### P8: Fluid Mechanics and Heat Transfer

- [x] Reynolds number.
- [x] Prandtl number.
- [x] Peclet number.
- [x] Internal-flow Nusselt number.
- [x] Pipe pressure drop.
- [x] Laminar/transitional/turbulent friction factor.
- [x] Pump work.
- [x] Mixing power.
- [x] Overall heat-transfer coefficient.
- [x] Jacket heat transfer.
- [x] Counterflow heat exchanger effectiveness-NTU model.
- [x] Packed-bed pressure drop.
- [x] Homogeneous two-phase pressure drop.

Acceptance tests:

- [x] Pressure drop increases with flow rate.
- [x] Heat-transfer rate increases with area and driving force.
- [x] Pump work is nonnegative.
- [x] Heat-exchanger stream energy is conserved.
- [x] Packed-bed pressure drop increases with superficial velocity.
- [x] Invalid equipment dimensions and policies fail fast.

### P9: Equilibrium Chemistry

- [x] Mass-action equilibrium solver.
- [x] Reaction extent formulation.
- [x] Equilibrium constant temperature dependence.
- [x] Acid/base equilibrium model.
- [x] Precipitation/dissolution proxy.
- [x] Charge balance.
- [x] Ionic strength calculation.
- [x] Water ion-product temperature proxy.
- [x] Solid solubility proxy.

Acceptance tests:

- [x] Equilibrium extent respects non-negativity.
- [x] Reversible reaction approaches expected equilibrium ratio.
- [x] Precipitation removes dissolved species only after saturation.
- [x] Weak-acid pH and charge balance are physically plausible.
- [x] Ionic strength matches molality and amount-based forms.

### P10: Mechanism and Scenario Library

- [x] `mechanisms/simple_batch_reaction.yaml`
- [x] `mechanisms/parallel_series_reaction.yaml`
- [x] `mechanisms/reversible_reaction.yaml`
- [x] `mechanisms/catalyst_deactivation.yaml`
- [x] `mechanisms/autocatalytic_reaction.yaml`
- [x] `mechanisms/reaction_extraction.yaml`
- [x] `mechanisms/reactive_distillation_lite.yaml`
- [x] `mechanisms/cstr_multiplicity.yaml`
- [x] `mechanisms/pfr_hotspot.yaml`
- [x] `mechanisms/electrochemical_conversion.yaml`

Acceptance tests:

- [x] Every mechanism loads from file.
- [x] Every mechanism passes conservation checks.
- [x] Every mechanism has a task card and expected qualitative behavior.

### P11: Instrument and Spectroscopy Coupling

- [x] Map species groups to HPLC peaks.
- [x] Map volatile species to GC peaks.
- [x] Map chromophores/proxy species to UV-vis bands.
- [x] Map functional-group proxies to IR bands.
- [x] Map species proxies to NMR shifts.
- [x] Support peak overlap.
- [x] Support calibration curves.
- [x] Support baseline drift.
- [x] Support instrument detection limits.
- [x] Support replicate measurements.

Acceptance tests:

- [x] Larger product amount increases product peak area.
- [x] Byproducts create visible impurity peaks.
- [x] Low concentration can fall below detection limit.
- [x] Processed estimates are consistent with raw signal within uncertainty.

### P12: Validation Against Reference Backends

These are optional tests that run only when external packages are installed.
They validate behavior but do not make external packages required.

- [x] Compare selected property correlations with `chemicals/thermo`.
- [x] Compare selected fluid calculations with `fluids`.
- [ ] Compare vapor pressure/enthalpy points with `CoolProp`.
- [x] Compare selected Arrhenius rate constants with `Cantera`.
- [ ] Compare simple reaction ODE cases with `Cantera`.
- [x] Compare simple LLE/VLE cases with `phasepy` or `thermo`.
- [ ] Compare equilibrium toy cases with `Reaktoro`.
- [ ] Compare solid-phase toy cases with `pycalphad`.

Current P12 note: the completed executable comparison set includes
`chemicals` ideal-gas/Rachford-Rice checks, curated DIPPR101 vapor-pressure and
Poling heat-capacity/enthalpy checks, `fluids` Reynolds/Prandtl/Haaland
friction/pipe-pressure-drop checks, `thermo` ideal VLE and Wilson/NRTL gamma
checks, and a selected Cantera `ArrheniusRate` check when Cantera is importable.
`phasepy` remains a useful design reference, but the local snapshot currently
requires a compiled Cython module before it can serve as an executable optional
backend.

Acceptance tests:

- [x] Optional tests skip cleanly when reference packages are absent.
- [x] Reference comparison tolerances are documented.
- [x] Divergences are recorded as model-limit notes, not hidden failures.

### P13: Benchmark Tasks Enabled by the New Core

- [ ] `multi-reaction-network-optimization`
- [ ] `reaction-calorimetry-safety`
- [ ] `reversible-reaction-equilibrium`
- [ ] `solvent-screening-with-activity-coefficients`
- [ ] `lle-extraction-design`
- [ ] `vle-flash-distillation`
- [ ] `cstr-steady-state-control`
- [ ] `pfr-hotspot-avoidance`
- [ ] `reactive-separation`
- [ ] `crystallization-solubility-design`
- [ ] `electrochemical-selectivity-energy`

Each task must define:

- [ ] scenario id;
- [ ] backend id;
- [ ] allowed operations;
- [ ] allowed instruments;
- [ ] budget;
- [ ] success metrics;
- [ ] hidden parameter split;
- [ ] public/private generalization test;
- [ ] baseline agents;
- [ ] explanation prompts.

## Implementation Order

### Milestone A: General Reaction Networks

- [ ] Build `physchem.reaction_network`.
- [ ] Load mechanism YAML/JSON.
- [ ] Replace fixed five-reaction code path for a new task.
- [ ] Keep current task behavior reproducible through a mechanism file.

### Milestone B: Minimal Property Core

- [ ] Build component and correlation registry.
- [ ] Add vapor pressure, heat capacity, density, and enthalpy.
- [ ] Wire energy balance to property backend.

### Milestone C: Phase Equilibrium Core

- [ ] Add activity models.
- [ ] Add binary LLE.
- [ ] Replace current extraction partition proxy where enabled.

### Milestone D: Reactor Expansion

- [ ] Add CSTR.
- [ ] Add PFR.
- [ ] Add semi-batch.
- [ ] Add task cards and baselines.

### Milestone E: Professional Validation

- [ ] Add optional external reference tests.
- [ ] Publish model cards for every physchem module.
- [ ] Update benchmark paper artifact.

## Explicit Non-Goals

- Do not claim real reaction prediction.
- Do not clone external libraries into the repository.
- Do not make heavy C++/Fortran packages required for core ChemWorld.
- Do not add proprietary chemical databases.
- Do not add large data tables without license review.
- Do not make the educational API depend on specialist process-simulation
  solvers.

## Reference Links For Feature Mapping

- Cantera: https://github.com/Cantera/cantera
- CoolProp: https://github.com/CoolProp/CoolProp
- thermo: https://github.com/CalebBell/thermo
- chemicals: https://github.com/CalebBell/chemicals
- fluids: https://github.com/CalebBell/fluids
- phasepy: https://github.com/gustavochm/phasepy
- IDAES: https://github.com/IDAES/idaes-pse
- Reaktoro: https://github.com/reaktoro/reaktoro
- pycalphad: https://github.com/pycalphad/pycalphad
- teqp: https://github.com/usnistgov/teqp
- thermopack: https://github.com/thermotools/thermopack
- RMG-Py: https://github.com/ReactionMechanismGenerator/RMG-Py
