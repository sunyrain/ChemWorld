---
title: "ChemWorld: A Composable Executable Chemical-World Substrate and Programmable Virtual Instrument"
title_line_one: "ChemWorld: A Composable Executable"
title_line_two: "Chemical-World Substrate and Programmable Virtual Instrument"
subject: "A composable executable chemical-world substrate and programmable virtual instrument"
keywords: "composable chemical worlds; executable chemistry; virtual scientific instrument; transactional semantics; exact replay; autonomous experimentation"
pdf_author: "Jiangjie Qiu; Yijun Li"
author:
  - name: "Jiangjie Qiu"
    affiliation_markers: "1"
  - name: "Yijun Li"
    affiliation_markers: "1"
affiliation:
  - id: "1"
    name: "Beijing Key Laboratory of Artificial Intelligence for Advanced Chemical Engineering Materials, State Key Laboratory of Chemical Engineering and Low-Carbon Technology, Department of Chemical Engineering, Tsinghua University, Beijing 100084, China"
correspondence: ""
date: ""
bibliography: experimental_intelligence_v1_references.bib
abstract: |
  Physical self-driving laboratories establish execution on real matter, but access,
  replication, safety and intervention are constrained by apparatus, materials and time;
  many digital benchmarks instead reduce an experiment to an objective-function query.
  We present ChemWorld as a complementary, composable executable chemical-world substrate
  and programmable virtual instrument. Reusable physical and transactional components
  compile into a world, and a public task contract attaches initial state, operations,
  instruments, observations, resources, failure rules, termination and evaluation. This
  software operating regime permits exact reset, repeatable matched worlds, complete
  simulator-side observation and private-law interventions without consuming physical
  reagents or creating laboratory hazards, while making no claim of virtual-to-real
  accuracy. The 15 registered tasks are reference examples rather than a bound on the
  construction space. Qualification covered 64/64 reference world units, 1,786/1,786
  complete reference recipes and 52/52 coverage-generated compositions, including eight
  frozen non-reference reaction--distillation compositions. All 192 invalid-action probes,
  32 module probes, seven interface paths and seven invalid declarations produced their
  registered outcomes, with zero missing receipts or public/private leakage. Across eight
  deterministic instrument-use cases, 89/89 submitted actions were audited: 88 committed,
  one planned failure rolled back without ghost state, all eight lifecycles closed, every
  resource ledger reconciled and every trajectory replayed with zero numerical mismatch.
  Six controlled single-private-component fork pairs preserved the public contract across
  24 provider-free traces. Finally, one complete agent closed the first frozen
  non-reference world in one uninterrupted session with 15/15 committed actions, explicit
  termination, a final assay and exact environment replay. The evidence qualifies a finite
  v1 virtual instrument; it does not establish arbitrary physics, laboratory prediction or
  agent superiority.
---

# 1. Introduction

Self-driving laboratories (SDLs) and chemistry agents have demonstrated that algorithms can
plan, execute and revise workflows on real materials. That physical validity is essential,
but it also makes matched replication expensive, slow and safety constrained: instruments
must be available, reagents and consumables are spent, failures can damage material or
equipment, and a laboratory state cannot usually be reset bit-for-bit. At the other extreme,
many digital optimization environments are inexpensive and repeatable but expose an
experiment mainly as a query that returns a value. A complementary virtual instrument is
needed for experiments that require controllable worlds, state-changing operations,
resource and failure semantics, complete process observation and exact environment replay.

ChemWorld treats a chemical world as an explicit executable object rather than an opaque
task label. Its v1 vocabulary contains reaction, thermal, phase, separation,
crystallization, distillation, continuous-flow, electrochemical and observation components.
A world is a compatible selection of these components, their parameters and private laws.
A task contract is $T=(W,S_0,A,I,O,R,\tau,E)$: the world, initial state, operations,
instruments, observations, resources, termination rule and evaluation surface. A scenario
instantiates the contract; a trajectory records the resulting operation--observation
sequence; and a controlled fork changes one private component while preserving the public
contract.

This architecture creates a different operating regime from a physical SDL. ChemWorld can
be run wherever the software and compute environment are available; a simulated experiment
does not consume physical reagents, create wet-laboratory waste or expose people and
equipment to chemical hazards; world state can be reset and replayed; every simulator-held
state transition and resource event can be audited; and private laws can be authored or
forked within the declared component interfaces. These are qualitative affordances, not a
measured cost or throughput comparison, and they do not confer laboratory validity. The
purpose is to make controlled, high-observability experimentation possible before or beside
physical execution (Fig. 1).

The central qualification question is therefore not whether an agent succeeds on a fixed
list. It is whether reusable components and their declared interfaces remain coherent when
assembled into coverage-guided combinations, including combinations absent from the
reference task identities. This paper contributes:

1. a public component vocabulary and task-contract model for constructing executable
   chemical worlds;
2. a compatibility checker that rejects missing dependencies, conflicting state owners,
   unit mismatches, invalid parameter domains, impossible resources and lifecycle holes
   before runtime;
3. a coverage-guided generator combining pairwise discrete coverage, seeded space-filling
   continuous samples and ordered workflow interactions;
4. full-census qualification of reference worlds, generated compositions, module limits,
   cross-module interfaces, transactional semantics, observation boundaries and exact
   replay;
5. deterministic instrument-use cases and controlled world forks that show what the
   apparatus records, without converting those records into a scalar intelligence score
   or a model ranking; and
6. a single complete-agent lifecycle on the first frozen non-reference composition, used only to
   demonstrate access through the same public instrument contract.

The scope is deliberately finite. We validate the declared v1 vocabulary and compatibility
domain, not arbitrary worlds or physical laws. The modules are synthetic or conceptual
models within stated domains, not digital twins. A complete agent is one possible user of
the instrument, but explaining its behaviour, isolating a model or scaffold effect and
measuring adaptation under changed laws require separate studies.

```{=latex}
\begin{figure*}[!tbp]
\centering
\includegraphics[width=\textwidth]{figures/first-paper-world-instrument-v1/publication/figure-1-system-overview.pdf}
\caption{\textbf{ChemWorld as a programmable virtual instrument from world construction to auditable experiment.}
\textbf{A,} Physical SDLs provide real-material validity, whereas the virtual substrate provides software access, exact reset, non-hazardous repetition and full simulator observability; the two regimes are complementary.
\textbf{B,} Reusable components and private laws compile through compatibility checks into a world and public task contract.
\textbf{C,} An agent or deterministic policy acts only through typed operations and instruments until explicit termination and final assay.
\textbf{D,} The immutable record joins state transitions, observations, resources, failures and lineage, enabling exact environment replay and controlled private-law forks.}
\label{fig:overview}
\end{figure*}
```

# 2. Relation to existing systems

## 2.1 Physical autonomous laboratories and chemistry agents

Physical autonomous laboratories establish what a purely virtual system cannot: execution
on real materials with real sensors, actuators, safety systems and hardware failure modes.
Coscientist and ChemCrow connect language-model planning to chemistry tools and robotic or
cloud-laboratory execution [@boiko2023autonomous; @bran2024augmenting]. A-Lab and mobile
robot systems demonstrate closed-loop synthesis and characterization
[@szymanski2023alab; @dai2024mobile], while ORGANA, ChemAgents and newer instrument-facing
systems extend this line toward visual feedback, long workflows, modular automation and
teachable operation [@darvish2025organa; @song2025chemagents; @panapitiya2026autolabs;
@pilon2026robochemflex; @vriza2026instruments].

ChemWorld does not replace this physical evidence. It addresses the complementary regime in
which exact matched replication, counterfactual laws, complete state access and repeated
failure injection are desirable. The marginal requirements are compute and software rather
than reagent, instrument and human-safety capacity. Consequently, ChemWorld can support
large controlled studies before physical validation, but any claim about real chemistry
must still be established in a laboratory.

## 2.2 Optimization suites, virtual laboratories and discovery worlds

Reaction-optimization and experiment-planning suites such as Summit and Olympus provide
scalable, repeatable comparisons over objective functions, while PC-Gym provides nonlinear
process-control environments with constraints and disturbances
[@felton2021summit; @hase2021olympus; @bloor2024pcgym]. ChemGymRL already establishes a
customizable, fine-grained virtual chemistry laboratory for reinforcement learning
[@beeler2024chemgymrl]. Closed-loop materials environments further couple candidate
generation, budgeted oracle feedback and multi-objective search [@malik2026made;
@abhyankar2026llema]. ChemWorld therefore does not claim novelty for simulation,
interactivity, resource budgets or closed loops individually.

Interactive scientific worlds broaden evaluation toward hypothesis formation, experiment
selection and law recovery. DiscoveryWorld, BoxingGym, SciGym, SciExplorer and NewtonBench
represent complementary approaches to long-horizon discovery and initially unknown systems
[@jansen2024discoveryworld; @gandhi2025boxinggym; @duan2025scigym;
@nagele2026sciexplorer; @zheng2026newtonbench]. Laboratory simulators such as LabUtopia and
Labimus emphasize embodied procedure and manipulation [@li2025labutopia; @wu2026labimus].
ChemWorld is narrower in embodiment and law diversity. Its distinctive unit is an
executable chemistry lifecycle in which typed operations change sample state, instruments
consume resources, invalid actions have transactional consequences, termination is
explicit, and the complete record is replayable.

## 2.3 Position and qualitative operating advantages

The adjacent systems should be compared by purpose rather than collapsed into one ranking.
Physical SDLs maximize empirical validity; optimization suites maximize controlled
algorithmic comparison; virtual laboratories and discovery worlds expose interactive task
structure. ChemWorld concentrates on composable world construction and process-level
observability. Within its declared model domain, researchers can instantiate new component
combinations, change private laws, repeat the same world many times, inspect hidden
simulator consequences and recover the complete resource and failure history. Table 1
summarizes these operating regimes; it is a capability comparison, not a performance or
cost benchmark.

```{=latex}
\begin{table*}[!tbp]
\centering
\small
\caption{\textbf{Qualitative operating regimes of adjacent experimental systems.} Entries describe typical capabilities rather than universal properties or measured superiority.}
\label{tab:related-position}
\begin{tabularx}{\textwidth}{@{}p{0.18\textwidth}p{0.18\textwidth}p{0.20\textwidth}p{0.20\textwidth}X@{}}
\toprule
System class & Primary evidence & Access and repetition & World or law control & Process observability and replay \\
\midrule
Physical SDL / chemistry robot & real-material execution and hardware integration & constrained by apparatus, consumables, time and safety & protocol and hardware changes; physical state cannot be reset exactly & sensor and automation logs; physical matter is not exactly replayable \\
Optimization or control suite & algorithmic comparison over objectives or dynamics & software-scalable and repeatable & usually fixed functions, datasets or process models & query or controller traces; lifecycle detail depends on the suite \\
Interactive virtual lab / discovery world & sequential manipulation, discovery or embodied procedure & software-scalable with controlled reset & environment-specific tasks and latent rules & action histories and observations; replay guarantees vary \\
ChemWorld & composable executable-world and instrument qualification & software access; no physical reagent use, wet-lab waste or chemical hazard & declared components and private-law forks within a bounded API & typed actions, hidden and public state, failures, resources, termination, lineage and exact environment replay \\
\bottomrule
\end{tabularx}
\end{table*}
```

# 3. A public construction surface for executable worlds

## 3.1 Components, worlds and task contracts

Each component declares the state it owns, the interfaces it consumes or produces, its
parameter domains and its contribution to the public operating surface. Reaction and
electrochemical components transform material state; thermal, phase, separation,
crystallization, distillation and continuous-flow components supply process-specific
state transitions; the observation component attaches synthetic instruments. Public
operations are typed actions rather than free-form simulator mutations.

The compiler first normalizes the declaration and then checks compatibility. It fails
closed on missing dependencies, multiple owners of the same state surface, unit
incompatibility, unsupported parameters, impossible resource declarations and workflows
that cannot reach termination. A successful compile returns both an executable task and a
reader-auditable public surface: allowed operations, instruments, observations, resources,
termination and evaluation. Private laws and hidden state remain outside that surface.

The public capability map contains 15 registered reference tasks, 28 typed operation
kinds, five synthetic instrument contracts and 62 ordered task-by-metric bindings. These
counts describe different objects. An operation kind is not a task; a task-metric binding
is not a unique endpoint; and an executed qualification recipe is not an independent agent
trial. The reference tasks span the declared surface but do not define its cardinality.

## 3.2 Coverage-guided generation

Composition generation is driven by coverage targets rather than by a desired number of
examples. Discrete component and instrument choices are arranged with pairwise covering
rows. Continuous temperature, time, flow, volume, potential, current, reflux and transfer
axes are sampled with seeded Latin hypercube designs. Ordered workflows separately require
critical interactions such as reaction before separation, quench before downstream
transfer and fraction collection before final measurement.

The frozen design contains eight component patterns, from phase--observation through
reaction--phase--separation--observation. It generated 52 compositions. Eight use a
reaction--thermal--distillation--observation topology that has zero identity overlap with
the 15 reference tasks. We call these \emph{frozen non-reference compositions}: their
components belong to the declared v1 vocabulary, but their task and world identities do
not belong to the frozen reference registry. This is more precise than calling them
arbitrary or wholly unseen worlds. The first generated row of this batch is the fixed
target for the complete-agent instrument demonstration and cannot be replaced after its
result is known.

# 4. Qualification of components, interfaces and runtime semantics

## 4.1 Reference and generated full censuses

The reference qualification treats a world unit as a task--world pairing rather than a
single task label. All 64/64 reference units passed. Boundary and categorical recipes
produced 1,786/1,786 complete executions. The generated block passed for all 52/52
compositions, including all eight non-reference reaction--distillation rows. There were no
failure classes, missing receipts or public/private leakage findings.

Compilation success alone was not a pass condition. Each generated composition had to
execute its complete workflow, close exactly once, reconcile declared and observed
resources and replay exactly. Seven deliberately broken declarations tested missing
dependencies, conflicting state ownership, unit mismatches, invalid domains, resource
impossibility and lifecycle gaps; all seven were rejected before environment construction.

## 4.2 Physical and cross-module checks

Thirty-two module probes exercise zero input, declared boundaries, monotonic directions,
conservation and model-specific invariants. The seven cross-module paths then check that
material amount, unit, identity and state meaning survive transfer between modules. When
applicable, the checks also include charge, energy, phase balance and event propagation.
All 32 module probes and seven interface paths passed.

These results establish internal qualification within each model card. They do not show
that the synthetic kinetics, spectra, phase equilibria or equipment responses predict a
particular physical laboratory. The validity claim is therefore interface and virtual-
instrument validity, not empirical chemical accuracy.

## 4.3 Transactions, resources, observations and replay

Every submitted action first passes schema, compatibility and resource preflight. A valid
action commits atomically. A rejected action records its attempt and declared penalty but
does not install candidate physical state. The 192 negative probes cover invalid schema,
preconditions, resource exhaustion, terminal closure and other fail-closed paths; all 192
produced the registered rejection and preserved state as required.

Resource accounting separates material, sample, instrument use, process time, operation
count and terminal assay. Observation checks ensure that public packets contain only
task-declared fields. Exact replay reconstructs the same compiled world from its bound
contract and seeds, resubmits the committed typed actions, and compares rewards,
observations, termination flags, transaction metadata, state-delta summaries, resource
events and constitution checks with zero numerical tolerance. It is an environment-level
claim under the bound software and model definitions, not reproduction of a physical batch
or a provider's token sequence.

```{=latex}
\begin{figure*}[!tbp]
\centering
\includegraphics[width=\textwidth]{figures/first-paper-world-instrument-v1/publication/figure-2-composition-and-qualification.pdf}
\caption{\textbf{Coverage-guided construction and full-census qualification.}
\textbf{A,} Eight frozen component patterns define the construction block; the highlighted reaction--distillation topology has zero identity overlap with the reference registry.
\textbf{B,} Pairwise discrete coverage, seeded continuous samples and ordered workflows determine 52 frozen rows rather than an arbitrary example count.
\textbf{C,} All reference units, reference recipes, generated compositions and non-reference compositions completed and replayed.
\textbf{D,} Module, interface, invalid-declaration and invalid-action probes all produced their registered outcomes, with zero missing receipts or public/private leakage. Counts are qualification denominators, not statistical samples.}
\label{fig:qualification}
\end{figure*}
```

# 5. Deterministic instrument-use cases

Eight frozen use cases test the recording surface without a provider. They cover a
reaction-to-crystallization workflow, resource-limited equilibrium characterization, an
intentional failure followed by recovery, continuous flow, electrochemistry, distillation,
partition and a second crystallization world. The cases are independent qualification
units; their actions are not treated as statistical replicates.

Across the eight cases, all 89 submitted actions have complete schema, transaction,
constitution, event, resource and public-observation receipts. Eighty-eight actions
committed. The first action of the failure--recovery case deliberately attempted phase
separation before its preconditions were satisfied. It rolled back, preserving physical
state and observation random-number state while reconciling the declared attempt
consequences. The following 18 actions completed the recovery path. Every case committed
one final assay, closed its lifecycle, reconciled resources and replayed exactly with zero
numerical error.

The generated reaction--distillation world also has a 12-action deterministic reference
path. It establishes construction, workflow execution and replay for the fixed non-reference
world, but it is not a substitute for the separate complete-agent unit reported below.
That unit originated every submitted action from one uninterrupted session and was judged
against its own lifecycle, provider-resource and replay gates.

```{=latex}
\begin{figure*}[!tbp]
\centering
\includegraphics[width=\textwidth]{figures/first-paper-world-instrument-v1/publication/figure-3-runtime-semantics.pdf}
\caption{\textbf{Deterministic cases exercise lifecycle and failure semantics.}
\textbf{A,} Eight frozen cases span single-process, multistage and reference-library workflows.
\textbf{B,} Eighty-eight of 89 submitted actions committed; one preregistered precondition failure rolled back.
\textbf{C,} The rollback preserved physical state and allowed the remaining 18-step recovery path to close.
\textbf{D,} All eight final assays, resource ledgers and exact replays passed.}
\label{fig:use-cases}
\end{figure*}
```

# 6. Controlled single-component forks

General composition and controlled attribution are different operations. Composition
assembles multiple declared components subject to compatibility rules. A world fork holds
the public task contract and action sequence fixed while changing one preregistered private
component.

The fork qualification contains six parent--child pairs: two intervention classes across
three seeds. Each pair preserved all nine public-contract components and executed the same
fixed sequence on parent and child. Repeating both variants produced 24 provider-free
traces. All pairs passed lineage, single-target, public-invariance, same-sequence
executability, expected state and observation divergence, exact replay and zero-provider
gates. The measured divergences demonstrate that a named private law can be manipulated
while the public instrument remains invariant. They do not establish arbitrary
multi-component authoring or agent adaptation.

# 7. Complete-agent use and process observability

An endpoint cannot reconstruct how it was reached. ChemWorld therefore keeps terminal
commitment, evidence acquisition, continued process investment, resource deployment,
failure and outcome trajectory as separate coordinates. Nineteen registered process
dimensions remain separate; no scalar intelligence score is formed. The important
advantage is observability: the evaluator can inspect complete simulator state and resource
consequences while the agent remains restricted to its public task contract.

The complete-agent demonstration used the first frozen non-reference
reaction--distillation world. It ran on 5 August 2026 with OpenAI GPT-5.6-sol at medium
reasoning effort through the Codex subscription provider. The fixed one-turn scaffold
supplied the public task card, typed tool schemas, resource contract and explicit
termination/final-assay requirement; it did not expose hidden state, repair actions or
auto-close the experiment. One uninterrupted session submitted 15 actions without restart
or model switch. All 15 committed; one explicit termination and one final assay closed the
lifecycle, with no rollback, right-censoring or public/private leakage.

The environment used 8,158.454 of 10,440 simulated process seconds, four of four instrument
uses and 0.00085 of 0.001 L sample. The 17 interface calls consist of the 15 state-changing
step calls plus one initial material-information read and one status read; they are not 17
submitted actions. Cumulative provider input was 493,092 tokens: 440,832 tokens were reused
cached context and 52,260 were uncached input. Cache hits therefore indicate context reuse
across the persistent tool-using turn, not repeated model output; output was 2,973 tokens.
These values are a resource ledger for one usability demonstration, not an efficiency
comparison. The complete 15-step environment trajectory replayed with zero numerical
mismatch.

```{=latex}
\begin{figure*}[!tbp]
\centering
\includegraphics[width=\textwidth]{figures/first-paper-world-instrument-v1/publication/figure-4-forks-and-agent.pdf}
\caption{\textbf{Controlled private-law interventions and complete-agent use of the same instrument surface.}
\textbf{A,} Parent and child worlds share the public contract and action sequence while one private constitutive or material law changes.
\textbf{B,} Six pairs and 24 provider-free traces pass lineage, public-invariance, divergence and exact-replay gates.
\textbf{C,} The fixed non-reference reaction--distillation world has an independent 12-step deterministic qualification path and a separate 15-step complete-agent lifecycle.
\textbf{D,} The agent closes the lifecycle within environment resources; 17 interface calls equal 15 step calls plus two read-only calls, and cached input denotes reused context rather than repeated output.}
\label{fig:forks-agent}
\end{figure*}
```

# 8. Discussion

## 8.1 What is established

The evidence establishes that ChemWorld has a real construction surface rather than only
a task catalogue. Declared components compile through explicit compatibility rules;
coverage-guided rows extend beyond the reference identities; and reference, generated and
non-reference compositions preserve the tested physical, transactional, resource, observation
and replay semantics. Controlled forks separately show that one named private component
can change under an invariant public contract.

The strongest evidence is deterministic and full-census. Every registered unit is shown
with its exact denominator, and every failure would remain visible. The qualification does
not rely on a favourable sample or on significance testing applied to repeated actions.
This is appropriate for a software-defined instrument whose first requirement is coherent
semantics.

The resulting practical advantage is experimental freedom rather than empirical fidelity.
Within the declared interfaces, a researcher can construct new topologies, vary continuous
conditions, substitute private constitutive or material laws, rerun matched identities and
observe the complete simulator-side process. Such experiments are available without
booking physical hardware, consuming reagents or introducing chemical risk, and can be
repeated until the intended study denominator is reached. These affordances can make
large-scale agent diagnosis and counterfactual design economically accessible, but they
remain simulations whose external validity must be established separately.

## 8.2 What is not established

The tested component vocabulary is finite, and compatibility is only claimed inside its
declared domains. Passing 52 generated compositions does not prove an infinite or arbitrary
world language. The physical models are synthetic or conceptual abstractions and have not
been calibrated as predictive replicas of laboratory equipment or materials. Exact replay
reproduces simulator state and public records, not physical matter or stochastic provider
decisions.

The current evidence also does not establish general agent competence. The deterministic
cases qualify the apparatus. The complete-agent non-reference-world unit
shows that one system could use the same public contract and close one frozen lifecycle;
it is not a benchmark, reliability estimate or comparison group. Model ranking,
behavioural mechanisms, rule learning, cross-model attribution and broad agent statistics
are explicitly outside this paper.

## 8.3 Why composition and process records matter

A fixed benchmark can reveal whether an algorithm performs well on its entries, but it
cannot by itself show that the environment is reusable. Composition qualification shifts
the unit of validation toward components and interfaces. Process records add a second
shift: they preserve evidence acquisition, resource use, failure and terminal commitment
instead of collapsing the interaction into one score. Together these properties make the
environment useful as a programmable virtual instrument, even when no claim is made about
the intelligence or rationality of its user.

The intended workflow is therefore staged: use ChemWorld to generate controlled worlds,
stress policies, observe failure and resource behaviour, and narrow hypotheses at software
scale; use physical SDLs or conventional experiments when the question requires real
materials, hardware interaction or empirical calibration. Treating the two systems as
complements avoids both overclaiming simulation and underusing its control and visibility.

# 9. Methods

## 9.1 Construction and compatibility

A composition declaration specifies component roles and parameters plus the public task
surface. Normalization is deterministic. Compatibility checks cover dependencies, state
ownership, unit agreement, parameter domains, resource feasibility, operation exposure,
instrument availability and the existence of a closed lifecycle. A rejected declaration
returns structured diagnostics and does not construct an environment.

The task contract is the authoritative public boundary. Runtime validation is restricted
to the declared operations and instruments. Private constitutive laws, material identities
and hidden simulator state remain evaluator-owned. The 15 registered tasks are mapped into
the same component and contract representation used by generated compositions.

## 9.2 Coverage design

The qualification design was frozen before data generation. Eight patterns were assigned
fixed seeds. Discrete axes use pairwise covering rows. Continuous axes use seeded Latin
hypercube samples inside the authored bounds. Each pattern contains one or two ordered
workflows chosen before execution. The frozen denominator is 52 generated cases, including
eight reaction--distillation cases absent from the registered task identities.

The coverage selection and pass rules are fixed before the reported qualification run and
cannot be changed in response to its outcomes. The reader-facing result is the complete
current frozen census; development diagnostics and superseded engineering runs are not part
of the scientific denominator.

## 9.3 Qualification measurements

For each case, the report records normalized construction input, compile diagnostics,
public contract, action sequence, schema and transaction status, constitution checks,
events, resource preflight and outcome, public observation, termination, trajectory size
and exact replay. Missing receipts, non-finite quantities, unexpected commits or
rollbacks, leakage, denominator drift and replay mismatch fail the case.

Reference qualification covers 64 task--world units and 1,786 complete recipes. Generated
qualification covers 52 compositions. Negative qualification covers 192 invalid probes.
Module and interface qualification use 32 and seven units, respectively. Compile mutation
uses seven invalid declarations. Counts are exact qualification denominators.

## 9.4 Process-time envelopes

Environment process time is derived by pattern rather than assigned as an arbitrary common
cap. For each pattern,

```{=latex}
\[
t_{\max}=t_{\mathrm{required\ stages}}+t_{\mathrm{implicit\ reserve}}+
t_{\mathrm{allowed\ repeats}}.
\]
```

The required term sums the upper bounds of necessary timed stages. The implicit reserve
covers authored quench and transfer operations. Repeat allowance is tied to explicit
per-operation repeat limits. The resulting limits are 0 s for phase observation; 3,600 s
for reaction--thermal observation; 1,860 s for phase separation; 11,100 s for reaction
crystallization; 10,440 s for reaction distillation; 7,200 s for continuous flow; 5,400 s
for electrochemistry; and 7,500 s for reaction--phase separation. A proposed action is
rejected before runtime if either cumulative process time or a repeat limit would be
exceeded.

## 9.5 Deterministic use cases

The eight cases, seeds and action lists were frozen before execution. Their total expected
census was 89 submitted actions, 88 commits, one rollback and eight final assays. The
failure--recovery case specified the failing action and rollback class in advance. All
submitted actions were inspected; no sampling was used. The provider-call denominator was
zero.

## 9.6 Controlled forks

Each fork declares a parent, a child, one private intervention target, an invariant public
contract and expected divergence channels. Parent and child execute the same typed action
sequence. Gates require lineage validity, exactly one changed private target, invariant
public contract, executable sequence on both variants, expected physical and observation
divergence, exact replay and zero provider calls.

## 9.7 Complete-agent non-reference-world protocol

The formal unit is one complete lifecycle on the first frozen non-reference
reaction--distillation composition. One uninterrupted agent session may submit at most 16
actions through the public instrument interface. There is no run-level restart, model
switch, host fallback, automatic repair, automatic termination or automatic final assay.
The action count, tool calls and trajectory records must agree exactly; every action must
commit; the lifecycle must contain a termination and exactly one final assay; resources,
public boundary and exact replay must pass.

Provider accounting distinguishes one provider session, one logical agent turn, 15 action
calls and two read-only calls. The model, provider, reasoning effort, scaffold constraints,
public prompt template and execution date are bound before the run. Cumulative input is
separated into cached and uncached input; cached context is reused input, not repeated
output. The formal limits are 640,000 cumulative input tokens, 192,000 uncached input tokens
and 64,000 output tokens. Per-action wait is capped at 600 s, finalization at 300 s and
runner reserve at 600 s, giving a conservative method wall limit of 10,500 s. These method
resources are separate from the simulated process-time ledger.

## 9.8 Process readouts

The process profile retains 19 dimensions in five groups: terminal commitment, evidence
acquisition, evidence-conditioned action, resource deployment and outcome trajectory.
Undefined conditional quantities remain null rather than being set to zero. These
coordinates are available for later agent studies but are not pooled into the current
substrate qualification or a composite intelligence score.

## 9.9 Public boundary and exact replay

The evaluator owns hidden simulator identity and private state. Agent-facing task cards,
observations and histories are checked for hidden fields and absolute private paths. Replay
reconstructs the bound world from the same normalized contract, runtime, mechanism,
observation and scoring identities plus the recorded seeds and interventions. It then
resubmits every committed typed action and compares rewards, every public observation,
termination and truncation flags, operation types, transaction status, rollback reason,
events, state-delta summaries, constitution checks and resource consequences. The reported
qualification uses numerical tolerance zero and observed a maximum absolute error of zero.
This guarantee is bound to the released software and model definitions; cross-version or
cross-platform replay must first reproduce those bindings and is not asserted merely from
the action list. Provider response bodies, private reasoning, authentication data and raw
local payloads are excluded from the release.

# 10. Data and code availability

Code, configuration, processed reports, figure source data and release tooling are
available in the MIT-licensed ChemWorld repository at
[github.com/sunyrain/ChemWorld](https://github.com/sunyrain/ChemWorld). The tracked
materials regenerate the tables and figures and replay released simulator transitions and
resource changes. Provider authentication, unrestricted response bodies, private reasoning
and hidden evaluator identities are excluded.

Three reproducibility levels should be distinguished. First, the reported counts and
figures can be regenerated from processed evidence. Second, released trajectories reproduce
environment transitions, public observations and ledgers. Third, stochastic provider
decisions are not exactly reproducible. Exact replay in this paper always refers to the
executable world and its records.

# 11. Conclusion

ChemWorld is a composable executable chemical-world substrate and programmable virtual
instrument. Its public construction surface assembles reusable components into legal
worlds; its qualification programme checks reference and generated compositions at the
component, interface, transaction, resource, observation and replay levels. The 15 tasks
are reference examples rather than the boundary of the platform. Deterministic use cases
and controlled forks show that the instrument records complete lifecycles, preserves
failed-action semantics and supports single-private-component interventions under an
invariant public contract.

The claim remains intentionally bounded. The results establish internal virtual-instrument
qualification within the declared v1 domain, not arbitrary task generation, laboratory
prediction or agent superiority. The single complete-agent non-reference-world lifecycle shows
instrument usability under its frozen contract but does not support a general competence
or comparative claim. What is established is the substrate on which such studies can be
conducted: an endpoint is a result, while the experimental process is a replayable record.

# Appendix A. Reader-facing capability map

A reference identity is a registered task identity paired with one of its declared public
world seeds. The 15 task identities below expand to 64 task--world units. A generated row
is counted as overlapping the reference set only when both its task identity and compiled
world identity match a registered unit; the eight frozen non-reference rows have zero such
overlap.

```{=latex}
\begin{table*}[!tbp]
\centering
\scriptsize
\caption{\textbf{Complete reference-task registry.} Seed counts define the public world identities exercised for each task.}
\label{tab:reference-registry}
\begin{tabularx}{\textwidth}{@{}p{0.22\textwidth}p{0.32\textwidth}rX@{}}
\toprule
Reference task identity & Component topology & World seeds & Public operation / instrument summary \\
\midrule
electrochemical-conversion & reaction + electrochemistry + observation & 5 & 6 operations; pH, UV--visible, final assay \\
equilibrium-characterization & reaction + thermal + observation & 5 & 9 operations; pH, UV--visible, final assay \\
flow-reaction-optimization & reaction + continuous flow + observation & 5 & 7 operations; HPLC, GC, UV--visible, final assay \\
low-budget-characterization & reaction + thermal + observation & 3 & 9 operations; HPLC, GC, UV--visible, final assay \\
partition-discovery & reaction + phase + separation + observation & 5 & 9 operations; HPLC, GC, UV--visible, final assay \\
public-private-generalization & reaction + thermal + observation & 5 & 9 operations; HPLC, GC, UV--visible, final assay \\
purity-yield-tradeoff & reaction + thermal + phase + separation + observation & 5 & 18 operations; HPLC, GC, UV--visible, final assay \\
reaction-mechanism-explanation & reaction + thermal + observation & 3 & 9 operations; HPLC, GC, UV--visible, final assay \\
reaction-optimization-standard & reaction + thermal + observation & 5 & 9 operations; HPLC, GC, UV--visible, final assay \\
reaction-safety-constrained & reaction + thermal + observation & 5 & 9 operations; HPLC, GC, UV--visible, final assay \\
reaction-to-assay & reaction + thermal + observation & 1 & 9 operations; HPLC, GC, UV--visible, final assay \\
reaction-to-crystallization & reaction + thermal + crystallization + observation & 5 & 12 operations; HPLC, final assay \\
reaction-to-distillation & reaction + thermal + distillation + observation & 5 & 12 operations; HPLC, GC, UV--visible, final assay \\
reaction-to-purification & reaction + thermal + phase + separation + observation & 5 & 18 operations; HPLC, GC, UV--visible, final assay \\
tool-agent-planning & reaction + thermal + phase + separation + observation & 2 & 18 operations; HPLC, GC, UV--visible, final assay \\
\bottomrule
\end{tabularx}
\end{table*}
```

```{=latex}
\begin{table*}[!tbp]
\centering
\small
\begin{tabularx}{\textwidth}{@{}p{0.19\textwidth}p{0.20\textwidth}Xp{0.19\textwidth}@{}}
\toprule
Component pattern & Principal state or process & Representative public operations & Representative instruments \\
\midrule
Phase + observation & bounded phase/equilibrium state & add solvent, add reagent, measure, terminate & pH, UV--visible, final assay \\
Reaction + thermal & batch reaction and temperature history & add, heat, quench, sample & HPLC, GC, final assay \\
Phase + separation & phase formation and transfer & mix, settle, separate, wash, transfer & HPLC, final assay \\
Reaction + crystallization & reaction followed by solid formation & heat, seed, cool, filter & HPLC, particle sizing, final assay \\
Reaction + distillation & reaction, evaporation and fractionation & heat, quench, evaporate, distil, collect & HPLC, GC, final assay \\
Reaction + continuous flow & flow, residence time and conversion & set flow, set temperature, run, sample & HPLC, GC, final assay \\
Reaction + electrochemistry & potential/current-driven conversion & set potential/current, electrolyse, sample & voltammetry, HPLC, final assay \\
Reaction + phase + separation & multistage reaction and purification & react, quench, separate, wash, concentrate, transfer & HPLC, GC, final assay \\
\bottomrule
\end{tabularx}
\end{table*}
```

# Appendix B. Coverage reconstruction and qualification census

The coverage design below fixes the pattern, seed, continuous domain, workflow count and
generated denominator. Discrete factors include component-specific family or profile
choices and instrument profiles; the released machine-readable coverage records map every
discrete level, compatible pair, continuous stratum and ordered interaction to the rows
that cover it.

```{=latex}
\begin{table*}[!tbp]
\centering
\scriptsize
\caption{\textbf{Frozen coverage design.} Bounds are inclusive authored domains; ``none'' denotes a purely discrete design.}
\label{tab:coverage-design}
\begin{tabularx}{\textwidth}{@{}p{0.21\textwidth}rXp{0.10\textwidth}r@{}}
\toprule
Pattern & Seed & Continuous axes and bounds & Workflows & Cases \\
\midrule
phase--observation & 101 & none & 1 & 6 \\
reaction--thermal--observation & 102 & heat 350--390 K; duration 600--1,800 s & 2 & 6 \\
phase--separation--observation & 103 & phase 0.010--0.020 L; extractant 0.010--0.025 L; mix 60--300 s; settle 120--600 s & 2 & 6 \\
reaction--crystallization--observation & 104 & reaction 350--390 K, 600--1,800 s; seed 0.002--0.010 g; cooling 275--305 K, 900--3,600 s & 2 & 6 \\
reaction--distillation--observation & 105 & reaction 350--390 K, 600--1,800 s; evaporation 325--345 K, 300--900 s; distillation 350--390 K, 900--2,400 s; reflux 1.0--3.0; transfer 0.65--0.95 & 2 & 8 \\
reaction--continuous-flow--observation & 106 & flow 0.5--5.0 mL min$^{-1}$; residence 60--600 s; temperature 330--390 K & 2 & 6 \\
reaction--electrochemistry--observation & 107 & potential 0.5--1.8 V; current 25--150 mA; electrolysis 300--1,800 s & 2 & 7 \\
reaction--phase--separation--observation & 108 & reaction 350--390 K, 600--1,800 s; phase/extractant 0.010--0.020/0.010--0.025 L; mix 60--300 s; settle 120--600 s; wash 0.003--0.010 L; concentrate 300--900 s; transfer 0.65--0.95 & 2 & 7 \\
\bottomrule
\end{tabularx}
\end{table*}
```

```{=latex}
\begin{table*}[!tbp]
\centering
\small
\begin{tabularx}{\textwidth}{@{}XrrX@{}}
\toprule
Qualification unit & Passed & Denominator & Failure classes \\
\midrule
Reference task--world units & 64 & 64 & 0 \\
Complete reference recipes & 1,786 & 1,786 & 0 \\
Coverage-generated compositions & 52 & 52 & 0 \\
Frozen non-reference reaction--distillation compositions & 8 & 8 & 0 \\
Invalid action probes & 192 & 192 & 0 unexpected outcomes \\
Module probes & 32 & 32 & 0 \\
Cross-module interface paths & 7 & 7 & 0 \\
Invalid compile mutants & 7 & 7 & 0 unexpected constructions \\
Deterministic use cases & 8 & 8 & 0 \\
Deterministic submitted actions & 89 & 89 & 0 missing receipts \\
Controlled fork pairs & 6 & 6 & 0 \\
Controlled fork traces & 24 & 24 & 0 \\
\bottomrule
\end{tabularx}
\end{table*}
```

# Appendix C. Instrument-use case library

```{=latex}
\begin{table*}[!tbp]
\centering
\small
\begin{tabularx}{\textwidth}{@{}p{0.20\textwidth}p{0.28\textwidth}X@{}}
\toprule
Scientific use & Components & What the record demonstrates \\
\midrule
Reaction to crystallization & reaction, thermal, crystallization, observation & propagation from reaction through seeding, cooling, filtration and final assay \\
Resource-limited characterization & phase, observation & measurement choice, sample consumption and explicit stopping under a small budget \\
Failure and recovery & reaction, thermal, phase, separation, observation & atomic rollback, attempt consequences and continuation from committed state \\
Controlled private-law fork & one registered component changed privately & invariant public contract with preregistered state/observation divergence \\
Generated reaction to distillation & reaction, thermal, distillation, observation & construction and replay outside the reference task identities; one complete-agent lifecycle closed under the same public contract \\
Reference library & flow, electrochemistry, distillation, partition, crystallization & breadth of reusable task recipes without a cross-task performance score \\
\bottomrule
\end{tabularx}
\end{table*}
```

# Appendix D. Process-coordinate dictionary

The 19 process dimensions remain separate and are grouped as follows.

**Terminal commitment:** closed-lifecycle fraction, assay fraction and discard fraction.

**Evidence acquisition:** measured-lifecycle fraction, non-final instrument uses per closed
lifecycle and normalized first-measurement position.

**Evidence-conditioned action:** continued-after-measurement fraction, post-measure process
operations per closed lifecycle, threshold-eligible fraction and threshold-decision
concordance.

**Resource deployment:** attempted operations per closed lifecycle, committed operations
per closed lifecycle, cost per closed lifecycle and risk per closed lifecycle.

**Outcome trajectory:** normalized best-discovery position, online incumbent-retention
rate, maximum absolute incumbent drawdown, loss-episode recovery rate and terminal-to-best
ratio. Mean and best endpoint scores are reported beside this profile and never enter a
composite score.

# Appendix E. Component model-card summary

Each module is qualified only inside its stated virtual-instrument domain. The table gives
the controlling formulation, principal authored domain, validation oracle and the boundary
that prevents the result from being read as laboratory calibration.

```{=latex}
\begin{table*}[!tbp]
\centering
\scriptsize
\begin{tabularx}{\textwidth}{@{}p{0.13\textwidth}p{0.25\textwidth}p{0.21\textwidth}p{0.20\textwidth}X@{}}
\toprule
Component & Runtime formulation & Principal v1 domain & Qualification oracle & Known boundary \\
\midrule
Reaction & stoichiometric mass-action network with Arrhenius temperature dependence & authored reaction families and bounded batch temperature/time & exact amount fixtures, monotonic response, material closure and runtime constitution & synthetic/reference slice; no claim of kinetic fit to a named wet-lab reaction \\
Thermal & dynamic batch heat-release and jacket-energy balance & bounded temperature, duration, vessel pressure and volume & temperature/energy finiteness, bounds, event propagation and ledger reconciliation & simplified vessel and heat-transfer representation \\
Phase & stability-gated, activity-corrected liquid--liquid equilibrium with TPD-style diagnostics & declared phase identities, volumes and composition ranges & phase/material balance, directional partition response and state identity & intrinsic distribution behaviour is benchmark-calibrated rather than compound-specific \\
Separation & settling, entrainment, wash and transfer coupled to the phase model & bounded mix/settle time, extractant/wash volume and transfer fraction & amount/unit conservation, transfer identity and expected directional response & no hydrodynamic or hardware-scale separation calibration \\
Crystallization & van't Hoff solubility with seed, nucleation/growth cohorts, impurity occlusion and CSD summaries & bounded seed mass, cooling temperature and cooling time & material closure, solubility-direction checks, CSD and runtime-constitution receipts & conceptual population-balance instrument, not a calibrated crystallizer \\
Distillation & bubble-gated, duty-limited VLE/Fenske fractionation with material and energy ledgers & bounded temperature/time, reflux ratio, fraction count and collected fraction & mass/energy closure, fraction identity, recovery/purity directions and equipment limits & simplified pseudo-component and stage representation \\
Continuous flow & geometry-resolved plug-flow reactor with residence time, distributed thermal boundary and pressure drop & bounded flow, residence time and temperature & conversion direction, mass closure, pressure/geometry and solver diagnostics & not a controller or digital twin of a particular flow platform \\
Electrochemistry & Nernst potential, Butler--Volmer kinetics, limiting current, Randles transient and Faraday accounting & bounded potential, current and electrolysis time & charge/material closure, signed work, selectivity and limiting-current checks & synthetic materials and electrodes; no cell-specific calibration \\
Observation & state-coupled synthetic pH, UV--visible, HPLC, GC and final-assay contracts & task-declared instruments, sample and use budgets & instrument availability, sample consumption, finite/bounded signal and non-omniscience checks & synthetic response definitions are not empirical spectra or chromatograms \\
\bottomrule
\end{tabularx}
\end{table*}
```

```{=latex}
\clearpage
```
