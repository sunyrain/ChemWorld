---
title: "ChemWorld: Composable Chemical Worlds for Controlled and Replayable Agent Experimentation"
title_line_one: "ChemWorld: Composable Chemical Worlds for"
title_line_two: "Controlled and Replayable Agent Experimentation"
subject: "Composable chemical worlds for controlled and replayable agent experimentation"
keywords: "composable chemical worlds; programmable virtual instrument; controlled experimentation; transactional semantics; exact replay; autonomous chemistry"
pdf_author: "Jiangjie Qiu; Yijun Li; Xiaonan Wang"
author:
  - name: "Jiangjie Qiu"
    affiliation_markers: "1"
  - name: "Yijun Li"
    affiliation_markers: "1"
  - name: "Xiaonan Wang"
    affiliation_markers: "1,*"
affiliation:
  - id: "1"
    name: "Beijing Key Laboratory of Artificial Intelligence for Advanced Chemical Engineering Materials, State Key Laboratory of Chemical Engineering and Low-Carbon Technology, Department of Chemical Engineering, Tsinghua University, Beijing 100084, China"
correspondence: "wangxiaonan@tsinghua.edu.cn"
date: ""
bibliography: experimental_intelligence_v1_references.bib
abstract: |
  Autonomous chemistry needs both real-material execution and a software-scale experimental
  medium in which worlds can be reset exactly, repeated safely, observed completely and
  changed under controlled laws. ChemWorld provides this second capability as a composable
  executable chemical-world substrate and programmable virtual instrument. Reusable
  physical and transactional components compile into worlds, while one public task contract
  joins initial state, typed operations, instruments, observations, resources, failure
  semantics, termination and evaluation. Researchers can therefore create matched worlds,
  branch one private law at a time and audit every simulator-side state and resource event
  without directly consuming physical reagents or creating wet-laboratory chemical
  exposure. The 15 registered tasks serve as reference examples for a broader construction
  surface. Full-census qualification covered every registered world unit and complete
  reference recipe, plus 52 coverage-generated compositions, including eight protocol-defined
  non-reference reaction--distillation compositions. Invalid-action, module, interface and
  declaration probes produced their registered outcomes, with zero missing receipts or
  public/private leakage. Across eight deterministic use cases and six controlled private-law
  fork pairs, every committed lifecycle and environment-replay gate passed, and one complete
  agent closed a non-reference world through the same instrument interface. Together, these results show that
  compositional expansion can preserve executable semantics and turn simulated chemistry
  from a fixed task collection into a controlled, observable and replayable experimental
  medium. The released instrument spans nine declared component families and defines
  extension points for future alternative or empirically calibrated formulations.
---

# 1. Introduction

Self-driving laboratories (SDLs) and chemistry agents have demonstrated that algorithms can
plan, execute and revise workflows on real materials. A second experimental regime is
needed for questions that depend on exact reset, matched counterfactuals, repeated failure
injection, complete process observation and direct control over the laws of the world.
These operations are difficult to obtain from physical matter and are usually absent when a
digital experiment is represented only as an objective-function query. A programmable
virtual instrument can make them routine at software scale.

ChemWorld treats a chemical world as an explicit executable object rather than an opaque
task label. Its declared vocabulary contains reaction, thermal, phase, separation,
crystallization, distillation, continuous-flow, electrochemical and observation components.
A world is a compatible selection of these components, their parameters and private laws.
A task contract is $T=(W,S_0,A,I,O,R,\tau,E)$: the world, initial state, operations,
instruments, observations, resources, termination rule and evaluation surface. A scenario
instantiates the contract; a trajectory records the resulting operation--observation
sequence; and a controlled fork changes one private component while preserving the public
contract.

This architecture creates controlled experimental freedom. ChemWorld can run wherever the
software and compute environment are available. The software itself consumes no physical
reagents and creates no direct wet-laboratory chemical exposure. World state can be reset
exactly, repeated to a planned study denominator under explicit compute and storage budgets,
and forked at a named private law. The evaluator can inspect every hidden state transition
and resource event while the agent remains restricted to the public instrument contract. These
properties make high-observability counterfactual experimentation available before,
alongside or between physical campaigns (Fig. 1).

The central question is whether a chemical environment can expand beyond a fixed task list
without losing the semantics that make experiments interpretable. We address it through
four linked contributions:

1. **Composable executable worlds.** A public component vocabulary, compatibility compiler
   and unified task contract convert component selections and private laws into executable,
   reader-auditable instruments.
2. **Coverage-guided expansion.** Pairwise discrete coverage, seeded space-filling
   continuous designs and ordered workflow interactions extend qualification beyond the
   reference task identities.
3. **Process-complete semantics.** Atomic transactions, explicit failure and termination,
   multi-resource ledgers, public/private observation boundaries and exact environment
   replay make each trajectory an inspectable experimental record.
4. **Controlled intervention and agent access.** Single-private-law forks isolate
   trace-level world changes under an invariant public contract, fixed typed actions and
   bound randomness, while deterministic policies and a complete agent use the same
   instrument surface.

This paper qualifies the declared component and compatibility domain as a virtual
instrument. Its modular interfaces separate experimental semantics from model choice and
define extension points through which future implementations may introduce additional
constitutive laws, calibrated process models or alternative agents.

```{=latex}
\begin{figure*}[!tbp]
\centering
\includegraphics[width=\textwidth]{figures/first-paper-world-instrument-v1/publication/figure-1-system-overview.pdf}
\caption{\textbf{ChemWorld turns composable chemical worlds into controlled, auditable experiments.}
\textbf{A,} Physical SDLs provide real-material execution; the virtual substrate adds software access, exact reset, repetition without direct wet-lab exposure, matched counterfactuals and complete simulator observability.
\textbf{B,} Reusable components and private laws compile through compatibility checks into a world and public task contract.
\textbf{C,} An agent or deterministic policy acts only through typed operations and instruments until explicit termination and final assay.
\textbf{D,} The immutable record joins state transitions, observations, resources, failures and lineage, enabling exact environment replay and controlled private-law forks.}
\label{fig:overview}
\end{figure*}
```

# 2. Relation to existing experimental systems

## 2.1 Real-material execution and software-scale control

Physical autonomous laboratories provide the decisive evidence of execution on real
materials with real sensors, actuators and hardware. Coscientist and ChemCrow connect
language-model planning to chemistry tools and robotic or cloud-laboratory execution
[@boiko2023autonomous; @bran2024augmenting]. A-Lab and mobile robot systems demonstrate
closed-loop synthesis and characterization
[@szymanski2023alab; @dai2024mobile], while ORGANA, ChemAgents and newer instrument-facing
systems extend this line toward visual feedback, long workflows, modular automation and
teachable operation [@darvish2025organa; @song2025chemagents; @panapitiya2026autolabs;
@pilon2026robochemflex; @vriza2026instruments].

ChemWorld supplies the complementary evidence available from a fully controlled software
world: exact matched replication, counterfactual private laws, evaluator-complete state
access, deterministic reset and repeatable failure injection. Its marginal resources are
compute and software rather than reagent, instrument and human-safety capacity. This
division enables large controlled studies in software and focused real-material validation
where physical evidence is decisive.

## 2.2 Digital optimization, virtual laboratories and discovery worlds

Reaction-optimization and experiment-planning suites such as Summit and Olympus provide
scalable, repeatable comparisons over objective functions, while PC-Gym provides nonlinear
process-control environments with constraints and disturbances
[@felton2021summit; @hase2021olympus; @bloor2024pcgym]. ChemGymRL already establishes a
customizable, fine-grained virtual chemistry laboratory for reinforcement learning
[@beeler2024chemgymrl]. Closed-loop materials environments further couple candidate
generation, budgeted oracle feedback and multi-objective search [@malik2026made;
@abhyankar2026llema]. These systems establish the value of inexpensive repeatability,
interactive chemistry and controlled algorithm comparison.

Interactive scientific worlds broaden evaluation toward hypothesis formation, experiment
selection and law recovery. DiscoveryWorld, BoxingGym, SciGym, SciExplorer and NewtonBench
represent complementary approaches to long-horizon discovery and initially unknown systems
[@jansen2024discoveryworld; @gandhi2025boxinggym; @duan2025scigym;
@nagele2026sciexplorer; @zheng2026newtonbench]. Laboratory simulators such as LabUtopia and
Labimus emphasize embodied procedure and manipulation [@li2025labutopia; @wu2026labimus].
ChemWorld adds a distinct systems layer: world composition, instrumentation, private-law
intervention and replay are governed by one executable contract. Typed operations change
sample state, instruments consume explicit resources, invalid actions have transactional
consequences, termination is explicit, and the complete world transition can be rebuilt
from the released record. This combination supports experiments about both the agent and
the world it inhabits.

The construction and record layers also connect to established software-systems ideas.
Pairwise covering rows follow combinatorial interaction testing, which selects compact test
suites that cover registered parameter interactions [@cohen1997aetg]. The immutable record
specializes computational provenance---entities, activities, derivations and responsible
agents---to executable chemical-world transitions, resources and lineage
[@moreau2013provdm]. ChemWorld joins these ideas to a stateful scientific instrument rather
than treating them as release metadata alone.

## 2.3 A distinct operating regime: programmable experimental freedom

The defining ChemWorld advantage is the conjunction of composition, controlled
intervention and process-complete observation. Researchers can instantiate new component
topologies, vary continuous conditions, substitute a private constitutive or material law,
repeat matched world identities and inspect every simulator-side consequence. The same
contract also preserves the agent-facing boundary, so counterfactual worlds remain
comparable without exposing their hidden differences. Table 1 positions this capability
alongside the strongest use of adjacent experimental systems. The comparison is functional
rather than performance-based: it focuses on reset and repetition, intervention surface,
public/private observability and record scope.

```{=latex}
\begin{table*}[!tbp]
\centering
\small
\caption{\textbf{Complementary operating regimes for autonomous chemical experimentation.} ChemWorld combines software-scale repetition with explicit world composition, private-law intervention and process-complete replay.}
\label{tab:related-position}
\begin{tabularx}{\textwidth}{@{}p{0.18\textwidth}p{0.18\textwidth}p{0.20\textwidth}p{0.20\textwidth}X@{}}
\toprule
System class & Strongest use & Replication regime & Experimental intervention & Observable record \\
\midrule
Physical SDL / chemistry robot & real-material execution and hardware integration & apparatus-, material- and time-bound physical repeats & protocol, material and hardware changes & sensor, automation and sample records \\
Optimization or control suite & rapid algorithm comparison over objectives or dynamics & software-scale repeated queries or control episodes & configurable objectives, datasets or process models & objective histories or controller traces \\
Interactive virtual lab / discovery world & sequential discovery or embodied procedure & resettable software episodes & task-specific objects, procedures and latent rules & action histories, observations and task state \\
ChemWorld & controlled experiments over composable executable worlds & exact reset, matched repetition and version-bound replay without direct wet-laboratory consumable use & declared component composition plus single-private-law forks under an invariant public contract & typed actions, evaluator-complete state, public observations, failures, resources, termination, lineage and exact environment replay \\
\bottomrule
\end{tabularx}
\end{table*}
```

# 3. Composing executable worlds beyond a fixed task catalogue

## 3.1 One contract from world construction to experiment

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

For a bound mechanism $\theta$, resource ledger $R_t$ and recorded random stream $\xi_t$,
the runtime applies a preflight predicate $P(s_t,a_t,R_t)$ before installing a candidate
transition. A passing action produces $(\tilde{s}_{t+1},e_{t+1})=F_\theta(s_t,a_t,\xi_t)$
and commits $s_{t+1}=\tilde{s}_{t+1}$; a rejected action leaves $s_{t+1}=s_t$ while
recording a structured rejection event and ledger consequence. Public and evaluator views
are separate projections,

```{=latex}
\[
o_{t+1}=\pi_{\mathrm{pub}}(s_{t+1},e_{t+1}),\qquad
\hat{o}_{t+1}=\pi_{\mathrm{eval}}(s_{t+1},e_{t+1}).
\]
```

Replay equivalence therefore binds the normalized contract, runtime and mechanism identities,
scoring identity, seeds and intervention record, then compares the committed action trace,
public observations, transaction outcomes, resource deltas and terminal flags.

The public capability map contains 15 registered reference tasks, 28 typed operation
kinds, five synthetic instrument contracts and 62 ordered task-by-metric bindings. The
reference tasks anchor interpretable examples across the declared surface, while component
composition supplies the expansion mechanism. This separates the size of the executable
world space from the number of curated task identities.

## 3.2 Coverage-guided expansion

Composition generation is driven by coverage targets rather than by a desired number of
examples. Discrete component and instrument choices are arranged with pairwise covering
rows. Continuous temperature, time, flow, volume, potential, current, reflux and transfer
axes are sampled with seeded Latin hypercube designs. Ordered workflows separately require
critical interactions such as reaction before separation, quench before downstream
transfer and fraction collection before final measurement.

The protocol-frozen design contains eight component patterns and generated 52 compositions.
Comparison of exact component sets against the reference registry separates two forms of
expansion. Three patterns---phase--observation, phase--separation--observation and
reaction--thermal--continuous-flow--observation---are absent from the reference topologies
and contribute 18/52 generated cases. Five patterns reuse a registered component topology.
Within the latter group, the eight reaction--thermal--distillation--observation rows have
zero exact task--world identity overlap with the frozen registry. We call these
\emph{protocol-frozen non-reference compositions}: their topology is registered, but their
bound task and world identities are not. The first row of this eight-case block was fixed
before authoritative execution as the complete-agent target, linking agent use to the same
coverage design rather than to a separately selected example.

Every registered coverage target was attained. Across the eight patterns, the generated
suite covered 60/60 discrete levels, 180/180 compatible discrete pairs, 212/212 continuous
strata and 84/84 ordered workflow interactions. These are finite registered targets within
the authored domains, and their covered and required counts are retained pattern by
pattern in the machine-readable coverage record.

Pairwise rows qualify declared component and instrument interfaces, while seeded continuous
designs and ordered workflows target authored bounds and critical process orderings. They are
therefore construction-coverage targets, not a claim of semantic completeness over all
higher-order chemistry. Higher-order behavior is addressed where it is explicitly present in
a workflow, module probe or interface path.

# 4. Composition preserves executable and declared process semantics

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

## 4.2 Module and cross-module process checks

Thirty-two module probes exercise zero input, declared boundaries, monotonic directions,
conservation and model-specific invariants. The seven cross-module paths then check that
material amount, unit, identity and state meaning survive transfer between modules. When
applicable, the checks also include charge, energy, phase balance and event propagation.
All 32 module probes and seven interface paths passed.

These results qualify each formulation as an internally coherent virtual-instrument module
inside its model-card domain. Every module enters through declared interfaces that define
where future implementations may supply alternative or empirically calibrated formulations
while retaining the task contract, transaction layer and replay machinery.

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
events and constitution checks with zero numerical tolerance. This version-bound guarantee
makes the full environment transition, rather than only the endpoint or action list, the
reproducible unit.

```{=latex}
\begin{figure*}[!tbp]
\centering
\includegraphics[width=\textwidth]{figures/first-paper-world-instrument-v1/publication/figure-2-composition-and-qualification.pdf}
\caption{\textbf{Coverage-guided construction and full-census qualification.}
\textbf{A,} Three of eight component patterns, representing 18/52 cases, add topologies absent from the reference registry; the eight reaction--distillation rows instead reuse a registered topology while having zero exact task--world identity overlap.
\textbf{B,} The 52 protocol-frozen rows attain 60/60 registered discrete levels, 180/180 compatible pairs, 212/212 continuous strata and 84/84 ordered workflow interactions.
\textbf{C,} All reference units, reference recipes, generated compositions and non-reference compositions completed and replayed.
\textbf{D,} Module, interface, invalid-declaration and invalid-action probes all produced their registered outcomes, with zero missing receipts or public/private leakage. Counts report complete qualification denominators.}
\label{fig:qualification}
\end{figure*}
```

# 5. Process-complete execution across diverse chemical workflows

Eight frozen use cases test the recording surface with deterministic policies. They cover a
reaction-to-crystallization workflow, resource-limited equilibrium characterization, an
intentional failure followed by recovery, continuous flow, electrochemistry, distillation,
partition and a second crystallization world. The cases are independent qualification
units, with every submitted action audited inside its complete lifecycle.

Across the eight cases, all 89 submitted actions have complete schema, transaction,
constitution, event, resource and public-observation receipts. Eighty-eight actions
committed. The first action of the failure--recovery case deliberately attempted phase
separation before its preconditions were satisfied. It rolled back, preserving physical
state and observation random-number state while reconciling the declared attempt
consequences. The following 18 actions completed the recovery path. Every case committed
one final assay, closed its lifecycle, reconciled resources and replayed exactly with zero
numerical error.

The generated reaction--distillation world also has a 12-action deterministic reference
path. This creates two independent execution units on the same world: a fixed path that
qualifies construction and replay, and a complete-agent lifecycle that tests access through
the public instrument contract.

```{=latex}
\begin{figure*}[!tbp]
\centering
\includegraphics[width=\textwidth]{figures/first-paper-world-instrument-v1/publication/figure-3-runtime-semantics.pdf}
\caption{\textbf{Process-complete cases preserve lifecycle, resource and failure semantics.}
\textbf{A,} Eight frozen cases span single-process, multistage and reference-library workflows.
\textbf{B,} Eighty-eight of 89 submitted actions committed; one protocol-defined precondition failure rolled back.
\textbf{C,} The rollback preserved physical state and allowed the remaining 18-step recovery path to close.
\textbf{D,} All eight final assays, resource ledgers and exact replays passed.}
\label{fig:use-cases}
\end{figure*}
```

# 6. Controlled single-component forks

General composition and controlled attribution are different operations. Composition
assembles multiple declared components subject to compatibility rules. A world fork holds
the public task contract and action sequence fixed while changing one protocol-frozen
private component.

The fork qualification contains six parent--child pairs: two intervention classes across
three seeds. Each pair preserved nine versioned public-contract components: task, actions,
instruments, observations, resources, failures, scoring, material catalogue and
constitution/safety. These fork-certificate fields refine the public boundary of the task
contract rather than redefining its mathematical tuple. Parent and child executed the same
fixed typed sequence with bound randomness. Repeating both variants produced 24
deterministic fork traces. All pairs passed lineage, single-target, public-invariance,
same-sequence executability, expected state and observation divergence, and exact replay
gates. The measured divergence is therefore a trace-level effect of one private-law
intervention under fixed actions and noise identity.

# 7. Agent experimentation with evaluator-complete observability

An endpoint cannot reconstruct how it was reached. ChemWorld therefore keeps terminal
commitment, evidence acquisition, continued process investment, resource deployment,
failure and outcome trajectory as separate coordinates. Nineteen registered process
dimensions remain separate, preserving the experimental structure that a scalar score
would discard. The evaluator can inspect complete simulator state and resource consequences
while the agent remains restricted to its public task contract.

Two agent-facing interaction examples show what this contract exposes without turning the
paper into an agent benchmark. In a resource-limited phase-observation world, an agent can
choose whether to spend scarce sample and instrument uses on pH or UV--visible measurements,
then terminate explicitly when the evidence is sufficient. In a failure-recovery workflow,
a premature phase-separation request returns a structured rollback while preserving the last
committed state, allowing the agent to revise its next typed action rather than restart the
experiment. The deterministic reference traces qualify both interaction patterns; comparative
agent behavior remains a separate study.

The complete-agent demonstration used the first protocol-frozen non-reference
reaction--distillation world. It ran on 5 August 2026 with OpenAI GPT-5.6-sol at medium
reasoning effort through the Codex subscription provider. The fixed one-turn scaffold
supplied the public task card, typed tool schemas, resource contract and explicit
termination/final-assay requirement. The agent received only this public surface and issued
every operation, including termination and final assay. One uninterrupted session submitted
15 actions under the same model and scaffold. All 15 committed and closed the lifecycle,
with zero rollback, right-censoring or public/private leakage.

The environment used 8,158.454 of 10,440 simulated process seconds, four of four instrument
uses and 0.00085 of 0.001 L sample. The complete record links each decision to its public
observation, hidden simulator consequence, transaction result and resource debit. The
The recorded 15-step committed-action trace then replayed with zero numerical mismatch, showing that a
provider-driven experiment can enter the same auditable record as deterministic use cases.

```{=latex}
\begin{figure*}[!tbp]
\centering
\includegraphics[width=\textwidth]{figures/first-paper-world-instrument-v1/publication/figure-4-forks-and-agent.pdf}
\caption{\textbf{Controlled private-law interventions and complete-agent use of the same instrument surface.}
\textbf{A,} Parent and child worlds share the public contract and action sequence while one private constitutive or material law changes.
\textbf{B,} Six pairs and 24 deterministic traces pass lineage, public-invariance, divergence and exact-replay gates.
\textbf{C,} The fixed non-reference reaction--distillation world has an independent 12-step deterministic qualification path and a separate 15-step complete-agent lifecycle.
\textbf{D,} The agent closes the lifecycle within environment resources through explicit termination and final assay; every state transition and resource event enters the replayable record.}
\label{fig:forks-agent}
\end{figure*}
```

# 8. Discussion

## 8.1 Controlled experimental freedom at software scale

ChemWorld turns world construction into an experimental variable. Declared components
compile through explicit compatibility rules; coverage-guided rows extend beyond curated
task identities; and reference, generated and non-reference compositions preserve executable,
transactional, resource, observation and replay semantics. The result is a construction
surface rather than a catalogue of isolated environments.

Six capabilities become available together: qualified new component topologies, continuous
condition variation, private-law intervention, exact reset, matched repetition and
evaluator-complete process inspection. Researchers can exercise them without booking
physical hardware or creating direct wet-laboratory chemical exposure, and can repeat an
experiment to its planned denominator under explicit compute and storage budgets. This
makes large controlled studies, diagnostic stress tests and counterfactual designs
economically accessible at software scale.

The full-census qualification is central to this advantage. Every registered unit carries
an exact denominator and every unexpected outcome remains visible. Coherent semantics are
therefore established across the declared construction domain before a policy comparison,
controlled intervention study or scientific application is layered on top.

## 8.2 From endpoint benchmarks to controlled counterfactual process analysis

An endpoint reports what was achieved; a process-complete record reveals how evidence,
resources, failures and terminal commitment produced it. ChemWorld retains these signals as
19 separate coordinates and binds them to replayable state transitions. This supports
questions about measurement strategy, recovery after invalid actions, resource deployment
and decision timing that disappear when an experiment is reduced to one score.

Controlled private-law forks add a counterfactual dimension. Parent and child worlds expose
the same actions, instruments and resources while one hidden law changes under the same
typed sequence and bound randomness. Outcome and observation differences in the reported
traces can therefore be assigned to that simulator intervention. The same construction
surface can support future policy-robustness, adaptation, measurement-value, curriculum and
failure-recovery studies through separately frozen randomized or matched protocols.

## 8.3 An extensible bridge to physical experimentation

The released qualification applies to the declared component vocabulary and authored
model domains. Those boundaries expose explicit extension points rather than fixed task
walls. Future implementations may introduce additional constitutive laws, calibrated unit
operations, empirical instrument models and new agents through the same task contract. The
complete-agent unit demonstrates that provider-driven action selection already uses this
common surface, while comparative agent studies can retain the same environment, resource
and replay guarantees.

ChemWorld and physical SDLs therefore form a productive sequence. Software worlds provide
cheap repetition, controlled counterfactuals, complete observability and rapid hypothesis
narrowing; physical systems provide real-material execution and calibration. The shared
experimental logic allows software-scale evidence to focus subsequent laboratory work on
the conditions and mechanisms that matter most.

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

The authoritative qualification protocol was frozen before execution. The frozen object
includes eight component patterns, their discrete axes and compatible pairs, continuous
bounds, seeds, ordered workflows, pass/failure rules and the first reaction--distillation
row selected for complete-agent use. Discrete axes use pairwise covering rows. Continuous
axes use seeded Latin hypercube samples inside the authored bounds. Each pattern contains
one or two ordered workflows. The denominator is 52 generated cases, including 18 cases
across three topologies absent from the reference registry and eight registered-topology
reaction--distillation cases with zero exact task--world identity overlap.

The coverage selection and pass rules are fixed before the reported qualification run and
remain invariant across all outcomes. The reader-facing result is the complete frozen
census defined by that design.

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

The 32 physical-module probes form an $8\times4$ design: each of reaction, thermal, phase,
separation, crystallization, distillation, continuous flow and electrochemistry contributes
one zero-input bounded-runtime probe, one legal low/high probe, one directionality probe and
one runtime-constitution probe. Legal low/high checks use numerical reference fixtures for
seven modules and a declared conceptual/synthetic fixture for crystallization;
directionality checks are declared conceptual/synthetic oracles. Every numerical fixture
records its own tolerance. Observation is qualified separately through instrument,
sample-accounting, bounded-signal and public/private-boundary checks. The seven compile
mutants comprise two missing-dependency cases and one case each for conflicting state
ownership, unit mismatch, invalid parameter domain, lifecycle hole and resource
impossibility.

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

The eight cases, seeds and action lists were protocol-frozen before execution. Their total expected
census was 89 submitted actions, 88 commits, one rollback and eight final assays. The
failure--recovery case specified the failing action and rollback class in advance. All
submitted actions were inspected as one deterministic census, isolating instrument
qualification from provider variance.

## 9.6 Controlled forks

Each fork declares a parent, a child, one protocol-frozen private intervention target, an
invariant public contract and expected divergence channels. Parent and child execute the same typed action
sequence. Gates require lineage validity, exactly one changed private target, invariant
public contract, executable sequence on both variants, expected physical and observation
divergence and exact replay under deterministic execution.

## 9.7 Complete-agent non-reference-world protocol

The formal unit is one complete lifecycle on the first protocol-frozen non-reference
reaction--distillation composition. The protocol binds one uninterrupted agent session, one
model/provider/scaffold configuration and at most 16 submitted actions through the public
instrument interface. Termination and final assay must be agent-issued. The action count,
tool calls and trajectory records must agree exactly; every action must commit; the
lifecycle must contain one termination and exactly one final assay; resources, public
boundary and exact replay must pass.

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
Undefined conditional quantities remain null rather than being set to zero. The resulting
coordinate vector preserves process structure for subsequent agent studies and supports
dimension-level comparison without a composite score. The released process-coordinate
contract supplies each dimension's numerator, denominator, value range, null condition and
boundary-case rule together with the computation binding used by the reports.

## 9.9 Public boundary and exact replay

The evaluator owns hidden simulator identity and private state. Agent-facing task cards,
observations and histories are checked for hidden fields and absolute private paths. Replay
reconstructs the bound world from the same normalized contract, runtime, mechanism,
observation and scoring identities plus the recorded seeds and interventions. It then
resubmits every committed typed action and compares rewards, every public observation,
termination and truncation flags, operation types, transaction status, rollback reason,
events, state-delta summaries, constitution checks and resource consequences. The reported
qualification uses numerical tolerance zero and observed a maximum absolute error of zero.
We use exact replay narrowly for environment/action-trace reconstruction under the bound
software identities. Policy re-execution, cross-platform numerical reproduction and
cross-version archival replay are separate reproducibility questions and are not inferred
from a zero-error environment replay. The public release contains the environment evidence
needed for this reconstruction while keeping authentication data, private reasoning and
unrestricted provider payloads outside the research artifact.

# 10. Data and code availability

Code, configuration, processed reports, figure source data and release tooling are
available in the MIT-licensed ChemWorld repository at
[github.com/sunyrain/ChemWorld](https://github.com/sunyrain/ChemWorld). The tracked
materials regenerate the tables and figures and replay released simulator transitions and
resource changes. The public submission tag `first-paper-arxiv-2026-08-06` binds the
manuscript source, dependency lock, processed evidence, figure data, coverage records and
release metadata used for this version. Provider authentication, unrestricted response
bodies, private reasoning and hidden evaluator identities are excluded.

The release supports three complementary reproducibility layers. Processed evidence
regenerates the reported counts and figures. Released trajectories reconstruct environment
transitions, public observations and ledgers. Provider provenance binds the model,
configuration and call accounting for the complete-agent unit. Exact replay refers to the
executable world and its complete experimental record. In this paper, environment/action-trace
replay is distinct from policy re-execution, cross-platform numerical reproduction and
cross-version archival replay. Provider provenance supports audit of the complete-agent unit
but does not imply that a later model call will regenerate the same actions.

# 11. Conclusion

ChemWorld turns simulated chemistry from a fixed task collection into a programmable
experimental medium. Reusable components compile into executable worlds; one public
contract joins operations, instruments, observations, resources, failures, termination and
evaluation; and every committed transition enters a version-bound replayable record. The 15
reference tasks anchor the public surface, while coverage-guided construction expands it to
new world identities without changing the runtime contract.

The resulting advantage is controlled experimental freedom at software scale. Researchers
can reset worlds exactly, repeat matched experiments without physical consumables or
chemical hazard, inspect complete simulator-side consequences and change one private law
under an invariant agent interface. Full-census qualification, process-complete use cases,
controlled forks and a complete-agent lifecycle show that these capabilities operate
together across the declared construction domain. ChemWorld therefore provides an efficient and
extensible substrate for controlled counterfactual agent studies, resource-aware
experimentation and focused translation into physical laboratories.

# Appendix A. Reader-facing capability map

A reference identity is a registered task identity paired with one of its declared public
world seeds. The 15 task identities below expand to 64 task--world units. A generated row
is counted as overlapping the reference set only when both its task identity and compiled
world identity match a registered unit; the eight protocol-frozen non-reference rows have zero such
overlap.

```{=latex}
\makeatletter
\setlength{\@dblfptop}{0pt}
\makeatother
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
Reaction + thermal + observation & batch reaction and temperature history & add, heat, quench, sample & HPLC, GC, final assay \\
Phase + separation + observation & phase formation and transfer & mix, settle, separate, wash, transfer & HPLC, final assay \\
Reaction + thermal + crystallization + observation & reaction followed by solid formation & heat, seed, cool, filter & HPLC, particle sizing, final assay \\
Reaction + thermal + distillation + observation & reaction, evaporation and fractionation & heat, quench, evaporate, distil, collect & HPLC, GC, final assay \\
Reaction + thermal + continuous flow + observation & flow, residence time and conversion & set flow, set temperature, run, sample & HPLC, GC, final assay \\
Reaction + electrochemistry + observation & potential/current-driven conversion & set potential/current, electrolyse, sample & voltammetry, HPLC, final assay \\
Reaction + thermal + phase + separation + observation & multistage reaction and purification & react, quench, separate, wash, concentrate, transfer & HPLC, GC, final assay \\
\bottomrule
\end{tabularx}
\end{table*}
```

# Appendix B. Coverage reconstruction and qualification census

The coverage design below fixes the pattern, seed, continuous domain, workflow count and
generated denominator. Discrete factors include component-specific family or profile
choices and instrument profiles; the released machine-readable coverage records map every
discrete level, compatible pair, continuous stratum and ordered interaction to the rows
that cover it. Covered and required counts are identical for all four target classes:
60/60 levels, 180/180 compatible pairs, 212/212 continuous strata and 84/84 ordered
interactions.

```{=latex}
\begin{table*}[!tbp]
\centering
\small
\caption{\textbf{Topology and identity decomposition of the generated block.} Topology novelty compares exact component sets with the 15-task reference registry; task--world novelty uses exact registered identities.}
\label{tab:novelty-decomposition}
\begin{tabularx}{\textwidth}{@{}p{0.33\textwidth}r p{0.22\textwidth}X@{}}
\toprule
Generated group & Cases & Topology relation & Exact task--world relation \\
\midrule
phase--observation & 6 & absent from reference registry & zero overlap implied by component-set difference \\
phase--separation--observation & 6 & absent from reference registry & zero overlap implied by component-set difference \\
reaction--thermal--continuous-flow--observation & 6 & absent from reference registry & zero overlap implied by component-set difference \\
reaction--thermal--distillation--observation & 8 & registered topology & zero exact overlap in the protocol-frozen non-reference block \\
four remaining generated patterns & 26 & registered topologies & used for reference-topology coverage; no separate non-reference identity claim \\
\bottomrule
\end{tabularx}
\end{table*}
```

```{=latex}
\begin{table*}[!tbp]
\centering
\scriptsize
\caption{\textbf{Protocol-frozen coverage design.} Bounds are inclusive authored domains; ``none'' denotes a purely discrete design.}
\label{tab:coverage-design}
\begin{tabularx}{\textwidth}{@{}p{0.21\textwidth}rXp{0.10\textwidth}r@{}}
\toprule
Pattern & Seed & Continuous axes and bounds & Workflows & Cases \\
\midrule
phase--observation & 101 & none & 1 & 6 \\
reaction--thermal--observation & 102 & heat 350--390 K; duration 600--1,800 s & 2 & 6 \\
phase--separation--observation & 103 & phase 0.010--0.020 L; extractant 0.010--0.025 L; mix 60--300 s; settle 120--600 s & 2 & 6 \\
reaction--thermal--crystallization--observation & 104 & reaction 350--390 K, 600--1,800 s; seed 0.002--0.010 g; cooling 275--305 K, 900--3,600 s & 2 & 6 \\
reaction--thermal--distillation--observation & 105 & reaction 350--390 K, 600--1,800 s; evaporation 325--345 K, 300--900 s; distillation 350--390 K, 900--2,400 s; reflux 1.0--3.0; transfer 0.65--0.95 & 2 & 8 \\
reaction--thermal--continuous-flow--observation & 106 & flow 0.5--5.0 mL min$^{-1}$; residence 60--600 s; temperature 330--390 K & 2 & 6 \\
reaction--electrochemistry--observation & 107 & potential 0.5--1.8 V; current 25--150 mA; electrolysis 300--1,800 s & 2 & 7 \\
reaction--thermal--phase--separation--observation & 108 & reaction 350--390 K, 600--1,800 s; phase/extractant 0.010--0.020/0.010--0.025 L; mix 60--300 s; settle 120--600 s; wash 0.003--0.010 L; concentrate 300--900 s; transfer 0.65--0.95 & 2 & 7 \\
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
Protocol-frozen non-reference reaction--distillation compositions & 8 & 8 & 0 \\
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
Controlled private-law fork & one registered component changed privately & invariant public contract with protocol-defined state/observation divergence \\
Generated reaction to distillation & reaction, thermal, distillation, observation & construction and replay outside the reference task identities; one complete-agent lifecycle closed under the same public contract \\
Reference library & flow, electrochemistry, distillation, partition, crystallization & breadth of reusable task recipes without a cross-task performance score \\
\bottomrule
\end{tabularx}
\end{table*}
```

# Appendix D. Process-coordinate dictionary

**Terminal commitment:** closed-lifecycle fraction, assay fraction and discard fraction.

**Evidence acquisition:** measured-lifecycle fraction, non-final instrument uses per closed lifecycle
and normalized first-measurement position.

**Evidence-conditioned action:** continued-after-measurement fraction, post-measure operations
per closed lifecycle, threshold-eligible fraction and threshold-decision concordance.

**Resource deployment:** attempted and committed operations per closed lifecycle, cost per closed
lifecycle and risk per closed lifecycle.

**Outcome trajectory:** timing, retention, drawdown/recovery and terminal-to-best ratio.

```{=latex}
\begin{table*}[!tbp]
\centering
\scriptsize
\caption{\textbf{Appendix E. Component model cards and extension points.} Each module declares its virtual-instrument domain, runtime formulation, authored domain, qualification oracle and interface location for future alternative or empirically calibrated implementations.}
\begin{tabularx}{\textwidth}{@{}p{0.09\textwidth}p{0.21\textwidth}p{0.18\textwidth}p{0.20\textwidth}X@{}}
\toprule
Component & Runtime formulation & Principal authored domain & Qualification oracle & Intended use and extension path \\
\midrule
Reaction & stoichiometric mass-action network with Arrhenius temperature dependence & authored reaction families and bounded batch temperature/time & exact amount fixtures, monotonic response, material closure and runtime constitution & reaction-law extension point for future named-reaction calibration \\
Thermal & dynamic batch heat-release and jacket-energy balance & bounded temperature, duration, vessel pressure and volume & temperature/energy finiteness, bounds, event propagation and ledger reconciliation & thermal-contract extension point for future equipment-specific coefficients \\
Phase & stability-gated, activity-corrected liquid--liquid equilibrium with TPD-style diagnostics & declared phase identities, volumes and composition ranges & phase/material balance, directional partition response and state identity & activity-model extension point for future compound-specific thermodynamics \\
Separation & settling, entrainment, wash and transfer coupled to the phase model & bounded mix/settle time, extractant/wash volume and transfer fraction & amount/unit conservation, transfer identity and expected directional response & separation-interface extension point for future hardware-scale transport \\
Crystallization & van't Hoff solubility with seed, nucleation/growth cohorts, impurity occlusion and CSD summaries & bounded seed mass, cooling temperature and cooling time & material closure, solubility-direction checks, CSD and runtime-constitution receipts & law extension point for future calibrated nucleation and growth models \\
Distillation & bubble-gated, duty-limited VLE/Fenske fractionation with material and energy ledgers & bounded temperature/time, reflux ratio, fraction count and collected fraction & mass/energy closure, fraction identity, recovery/purity directions and equipment limits & operation-contract extension point for future compound and column models \\
Continuous flow & geometry-resolved plug-flow reactor with residence time, distributed thermal boundary and pressure drop & bounded flow, residence time and temperature & conversion direction, mass closure, pressure/geometry and solver diagnostics & runtime extension point for future reactor-specific transport or control models \\
Electrochemistry & Nernst potential, Butler--Volmer kinetics, limiting current, Randles transient and Faraday accounting & bounded potential, current and electrolysis time & charge/material closure, signed work, selectivity and limiting-current checks & electrochemical-law extension point for future material- and cell-specific parameters \\
Observation & state-coupled synthetic pH, UV--visible, HPLC, GC and final-assay contracts & task-declared instruments, sample and use budgets & instrument availability, sample consumption, finite/bounded signal and non-omniscience checks & instrument-schema extension point for future empirical response models \\
\bottomrule
\end{tabularx}
\end{table*}
```

```{=latex}
\clearpage
```
