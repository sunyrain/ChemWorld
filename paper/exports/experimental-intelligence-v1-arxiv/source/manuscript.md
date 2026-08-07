---
title: "ChemWorld: Programmable Chemical Worlds for Controlled and Replayable Agent Experimentation"
title_line_one: "ChemWorld: Programmable Chemical Worlds for"
title_line_two: "Controlled and Replayable Agent Experimentation"
subject: "Programmable chemical worlds as controlled experimental variables for agent research"
keywords: "programmable chemical worlds; world construction; controlled counterfactual experimentation; process-complete evidence; exact replay; autonomous chemistry"
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
  Autonomous chemistry needs an experimental regime in which researchers can control not
  only an agent or task but also the world that generates evidence. Physical laboratories
  provide real-material execution but rarely allow exact reset, matched counterfactuals or
  complete process observation; many digital environments organize interaction around fixed
  tasks, dynamics or objective queries. ChemWorld provides a complementary software-scale
  medium in which chemical worlds are explicit executable objects. Reusable process-model
  and transactional components compile into public world structures, while evaluator-owned
  constitutive and material laws remain private. One instrument contract joins initial state,
  typed operations, instruments, observations, resources, failure semantics, termination and
  evaluation. Researchers can therefore compose world topologies, vary continuous conditions,
  branch one private law at a time, repeat matched world identities and audit every
  simulator-side state and resource event without exposing private state to the agent. The 15
  registered tasks anchor interpretable examples but do not bound the construction surface.
  Full-census qualification covered every registered world unit and complete reference recipe,
  plus 52 coverage-generated compositions, including eight protocol-frozen non-reference
  reaction--distillation compositions. Invalid-action, module, interface and declaration
  probes produced their registered outcomes, with zero missing receipts or undeclared
  private-field exposure. Across eight deterministic use cases and six controlled private-law
  fork pairs, all qualified lifecycles closed and replayed exactly; a separate agent completed
  one lifecycle in a non-reference world through the same public instrument contract. Within
  the declared component and compatibility domain, these results establish that world
  construction can serve as a controlled experimental variable while agent-facing interaction
  remains stable and process evidence remains attributable and replayable. ChemWorld thereby
  turns simulated chemistry from a fixed task collection into a programmable experimental
  medium for controlled counterfactual agent studies, complementary to real-material evidence
  and calibration.
---

# 1. Introduction

Self-driving laboratories (SDLs) and chemistry agents have demonstrated that algorithms can
plan, execute and revise workflows on real materials [@boiko2023autonomous; @bran2024augmenting;
@szymanski2023alab; @dai2024mobile]. These campaigns also consume reagents and instrument
time, require safety infrastructure, depend on access to particular facilities and samples, and do not
generally offer exact reset or matched replay. Software environments provide inexpensive
repetition, but they commonly hold world dynamics fixed while varying tasks, conditions,
objectives or agents. The world that produces the evidence is therefore treated as background
rather than as a first-class experimental factor. A complementary regime is needed for
questions that require exact reset, matched counterfactuals, repeated failure injection,
complete process observation and direct intervention on the laws of the world. A programmable
virtual instrument can make these operations routine at software scale.

ChemWorld treats a chemical world as an explicit executable object rather than an opaque
task label. Its declared vocabulary contains reaction, thermal, phase, separation,
crystallization, distillation, continuous-flow, electrochemical and observation components.
We separate the complete simulated world $\mathcal{W}=(W_{\mathrm{pub}},\theta)$ from its
public task contract. $W_{\mathrm{pub}}$ contains the public component topology, public
parameter domains and interfaces; $\theta$ contains evaluator-owned constitutive and
material laws, hidden parameters and private initialization. The public task contract is
$T=(W_{\mathrm{pub}},S_{0,\mathrm{pub}},A,I,O,R,\tau,E)$: the public world description,
public initial-state projection, operations, instruments, observations, resources,
termination rule and evaluation surface. A scenario binds this contract to a concrete
private mechanism and seeds; a trajectory records the resulting operation--observation
sequence; and a controlled fork replaces one element of $\theta$ while preserving $T$.

This architecture creates a new locus of experimental control. ChemWorld can run wherever
the software and compute environment are available. World state can be reset exactly,
repeated to a planned denominator under explicit compute and storage budgets, and forked at
a named private law. The evaluator can inspect every hidden state transition and resource
event while the agent remains restricted to the public instrument contract. These properties
make high-observability counterfactual experimentation available before, alongside or between
physical campaigns without consuming physical reagents or creating direct wet-laboratory
exposure (Fig. 1).

The central question is whether simulated chemistry can become a programmable experimental
medium in which researchers control the world itself---not merely the task or agent---while
preserving the stable interactions and process-complete evidence required for matched,
replayable and attributable experiments. We address it through four linked contributions:

1. **World construction as an intervention surface.** A public component vocabulary and
   compatibility compiler turn world topology, continuous conditions, instrument
   configurations and evaluator-owned private mechanisms into explicit experimental choices.
2. **Stable experimental contracts across an expanding construction space.** One public task
   contract preserves typed operations, instruments, observations, resources, failures,
   termination and evaluation across reference and coverage-generated worlds. Pairwise
   discrete coverage, seeded space-filling continuous designs and ordered workflow
   interactions qualify this invariance without treating the reference tasks as a closed list.
3. **Process-complete evidence for replay and intervention attribution.** Atomic transactions,
   explicit failure and recovery, multi-resource ledgers and exact environment replay make
   each trajectory inspectable, while single-private-law forks isolate trace-level changes
   under an invariant public contract.
4. **Agent access through the same experimental medium.** Deterministic policies and a
   complete-agent run use the same public instrument contract, while 19 evaluator-visible
   process dimensions preserve evidence acquisition, resource deployment, failure and
   terminal commitment without exposing private state.

The original systems question---whether compositional expansion preserves executable
semantics---is therefore a qualification question rather than the scientific endpoint. This
paper establishes that qualification within the declared component and compatibility domain;
it does not compare agent capabilities or claim universal chemical fidelity. Modular
interfaces separate experimental semantics from model choice and provide extension points
for additional constitutive laws, calibrated process models and alternative agents.

```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/first-paper-world-instrument-v1/publication/figure-1-system-overview.pdf}
\caption{\textbf{ChemWorld composes declared modules into executable worlds with transactional semantics, deterministic replay and controlled forks.}
\textbf{A,} Reusable process and instrument modules expose shared declarations.
\textbf{B,} The compiler either produces a public contract $W_{\mathrm{pub}}$ with evaluator-owned private mechanisms or rejects an invalid composition before construction.
\textbf{C,} Typed actions traverse preflight, runtime-precondition, candidate-execution and post-execution validation gates; non-commit branches preserve committed state and record declared attempt consequences.
\textbf{D,} Replay reconstructs the bound world and submitted action trace, while controlled forks hold the public contract and actions fixed and change one private law.}
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
compute and software rather than reagents, instrument time and wet-laboratory safety oversight. This
division enables large controlled studies in software and focused real-material validation
where physical evidence is decisive.

## 2.2 Digital optimization, virtual laboratories and discovery worlds

Reaction-optimization and experiment-planning suites such as Summit and Olympus provide
scalable, repeatable comparisons over objective functions, while PC-Gym provides nonlinear
process-control environments with constraints and disturbances
[@felton2021summit; @hase2021olympus; @bloor2024pcgym]. ChemGymRL is one of the closest prior
virtual-chemistry environments to ChemWorld: an open, Gym-compatible laboratory organized
around vessels, shelves and modular reaction, extraction, distillation and characterization
benches [@beeler2024chemgymrl]. Its benches expose continuous or discrete action spaces,
support partial observations and chemical-outcome rewards, and admit new reactions, actions,
observations and bench implementations while retaining a stable agent interface. It is
therefore a flexible testbed for reinforcement-learning training and comparison. Closed-loop
materials environments further couple candidate generation, budgeted oracle feedback and
multi-objective search [@malik2026made; @abhyankar2026llema]. These systems establish the
value of inexpensive repeatability, interactive chemistry and controlled algorithm comparison.

ChemWorld builds on this modular virtual-experimentation idea but changes the unit of
abstraction from a bench to a compiled experimental world. Components declare their state
ownership, dependencies, parameter domains and public interfaces; a compatibility compiler
assembles valid selections into a common task contract spanning typed operations,
instruments, observations, resources, failure semantics, termination and evaluation.
ChemGymRL makes chemical benches customizable; ChemWorld makes chemical worlds
experimentally controllable. The former is well suited to rapid reinforcement-learning
training and bench-specific policy comparison; the latter targets matched world identities,
atomic action semantics, explicit multi-resource ledgers, evaluator-owned private state,
single-private-law forks and exact environment/action-trace reconstruction. This
environment-level replay is distinct from RL experience replay, and the comparison concerns
experimental control and auditability rather than replacement of the standard RL ecosystem.

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
[@moreau2013provdm]. ChemWorld joins these ideas to a stateful scientific substrate rather
than treating them as release metadata alone.

## 2.3 World construction as a locus of experimental control

ChemWorld's defining contribution is the conjunction of programmable construction,
controlled intervention and process-complete observation. Researchers can instantiate new
component topologies, vary continuous conditions, substitute a private constitutive or
material law, repeat matched world identities and inspect every simulator-side consequence.
The world is therefore no longer only the fixed background against which a task is solved; it
becomes part of the experimental design. The same contract preserves the agent-facing
boundary, so counterfactual worlds remain comparable without exposing their hidden
differences. Table 1 positions this operating regime alongside the representative emphasis of
adjacent experimental systems. The comparison is functional rather than performance-based:
it focuses on reset and repetition, intervention surface, public/private observability and
record scope.

```{=latex}
\begin{table*}[!t]
\centering
\small
\caption{\textbf{Complementary operating regimes for autonomous chemical experimentation.} ChemWorld combines software-scale repetition with explicit world composition, private-law intervention and process-complete replay.}
\label{tab:related-position}
\begin{tabularx}{\textwidth}{@{}L{0.18\textwidth}L{0.18\textwidth}L{0.20\textwidth}L{0.20\textwidth}Y@{}}
\toprule
System class & Representative emphasis & Replication regime & Experimental intervention & Observable record \\
\midrule
Physical SDL / chemistry robot & real-material execution and hardware integration & apparatus-, material- and time-bound physical repeats & protocol, material and hardware changes & sensor, automation and sample records \\
Optimization or control suite & rapid algorithm comparison over objectives or dynamics & software-scale repeated queries or control episodes & configurable objectives, datasets or process models & objective histories or controller traces \\
Interactive virtual lab / discovery world & sequential discovery or embodied procedure & resettable software episodes & task-specific objects, procedures and latent rules & action histories, observations and task state \\
ChemWorld & controlled experiments over composable executable worlds & exact reset, matched repetition and version-bound replay without direct wet-laboratory consumable use & declared component composition plus single-private-law forks under an invariant public contract & typed actions, evaluator-complete state, public observations, failures, resources, termination, lineage and exact environment replay \\
\bottomrule
\end{tabularx}
\end{table*}
```

# 3. Programmable world construction under a stable experimental contract

## 3.1 Declarative world construction and compatibility compilation

ChemWorld separates world construction from task-specific environment implementation. Rather
than encoding each experimental scenario as an independent environment, researchers declare
reusable components, their parameter domains, dependencies, owned state and public
interfaces. A component topology specifies which component families are connected. A
composition binds that topology to public parameters and instruments, while the evaluator
binds the private mechanism. Formally,

```{=latex}
\[
\mathcal{W}=(W_{\mathrm{pub}},\theta),\qquad
T=(W_{\mathrm{pub}},S_{0,\mathrm{pub}},A,I,O,R,\tau,E).
\]
```

The complete world identity binds both $W_{\mathrm{pub}}$ and $\theta$, whereas the task
identity specifies the public experimental objective and operating contract. To keep seeds from
silently serving several identity roles, we distinguish a world-specification identity,
scenario identity and task--world unit:

```{=latex}
\[
\begin{aligned}
\mathrm{world\text{-}spec\ ID}&=\operatorname{id}(W_{\mathrm{pub}},\theta),\\
\mathrm{scenario\ ID}&=\operatorname{id}(W_{\mathrm{pub}},\theta,\zeta_{\mathrm{init}},
\zeta_{\mathrm{dyn}},\zeta_{\mathrm{obs}}),\\
\mathrm{task\text{--}world\ unit}&=(\mathrm{task\ ID},\mathrm{scenario\ ID}).
\end{aligned}
\]
```

Here $\operatorname{id}$ denotes the deterministic identity construction over the listed
inputs; release-manifest content hashes are separate provenance objects.

The task--world overlap tests below use the last identity level: a generated row overlaps
the reference registry only when both its task identity and scenario identity match a
registered unit. This distinction keeps evaluator-owned laws and hidden initialization outside
the agent-facing runtime surface without treating them as part of the public contract.

The declared vocabulary contains reaction, thermal, phase, separation, crystallization,
distillation, continuous-flow, electrochemical and observation components. Reaction and
electrochemical components transform material state; thermal, phase, separation,
crystallization, distillation and continuous-flow components supply process-specific state
transitions; the observation component attaches synthetic instruments. Public operations are
typed actions rather than free-form simulator mutations.

The compatibility compiler first normalizes the declaration and then checks dependencies,
state ownership, unit agreement, supported parameter domains, resource feasibility,
instrument availability and the existence of a closed lifecycle. It fails closed on an
invalid declaration and returns structured diagnostics without constructing an environment.
A successful compile returns both an executable world and a public surface with auditable
contracts and records:
allowed operations, instruments, observations, resources, termination and evaluation.
Private laws and hidden state remain outside that surface. The common interfaces are designed
to admit additional or empirically calibrated formulations without redesigning the runtime,
transaction layer or agent-facing contract.

## 3.2 Contract-bound transactional execution

Once a world is compiled, every submitted operation enters the same contract-bound runtime.
For a bound mechanism $\theta$, resource ledger $R_t$ and recorded random stream $\xi_t$,
the runtime applies a schema, compatibility and resource preflight predicate
$P(s_t,a_t,R_t)$ before candidate execution. A passing action first produces

```{=latex}
\[
(\tilde{s}_{t+1},\tilde{R}_{t+1},\tilde{e}_{t+1})=
F_\theta(s_t,R_t,a_t,\xi_t).
\]
```

The committed runtime state includes the observation-RNG state $\rho_t$; $\xi_t$ denotes
the random variates addressed from that state. A non-commit branch restores $\rho_t$, so
rejected candidate execution does not advance future observation noise. A runtime commit-gate predicate
$C\in\{0,1\}$ may reject either a dispatchable action at a declared runtime-precondition
check or a generated candidate at subsequent state-integrity, solver, runtime-invariant or
observation-path validation. For the latter, the gate is written
$C(\tilde{s}_{t+1},\tilde{R}_{t+1},\tilde{e}_{t+1})$. The transaction commits only when both
predicates pass:

```{=latex}
\[
\begin{aligned}
P=1,\ C=1 &\quad\Longrightarrow\\[-0.15em]
(s_{t+1},R_{t+1},e^\star_{t+1})
&=(\tilde{s}_{t+1},\tilde{R}_{t+1},e^{\mathrm{acc}}_{t+1}).
\end{aligned}
\]
```

The two non-commit branches are recorded separately. If $P=0$, the runtime emits a
preflight-rejection event $e^{\mathrm{pre}}_{t+1}$ without candidate execution. If $P=1$
but $C=0$, it emits a runtime-rollback event $e^{\mathrm{roll}}_{t+1}$ and restores
the committed physical and observation-random-number state. For
$b\in\{\mathrm{pre},\mathrm{roll}\}$,

```{=latex}
\[
s_{t+1}=s_t,\qquad
R_{t+1}=G_b(R_t,a_t,e^b_{t+1}),\qquad
e^\star_{t+1}=e^b_{t+1}.
\]
```

The planned failure--recovery case exercises a $C=0$ receipt before candidate-state generation
at a declared runtime-precondition check. The qualification campaign did not assign
separate denominators to solver-diagnostic or candidate-observation fault injections.

The branch-specific ledger function installs only the protocol-declared attempt cost or
penalty. Candidate physical, observation and uncommitted resource effects are discarded.
Thus the record distinguishes a preflight rejection from a runtime rollback
while preserving the same atomic boundary around committed state. Public and evaluator
views are separate projections of the realized branch,

```{=latex}
\[
o_{t+1}=\pi_{\mathrm{pub}}(s_{t+1},e^\star_{t+1}),\qquad
\hat{o}_{t+1}=\pi_{\mathrm{eval}}(s_{t+1},e^\star_{t+1}).
\]
```

The event term denotes structured transaction metadata rather than the complete hidden
state. $R_t$ is part of the transaction record even when the public agent surface
exposes only declared resource fields. The evaluator projection is evaluator-defined and is
not equivalent to exposing all hidden state to the agent.

Replay equivalence binds the normalized contract, runtime and mechanism identities, scoring
identity, seeds and intervention record, then compares the full submitted action/transaction
trace---including committed actions, preflight rejections and rollbacks---against public
observations, transaction outcomes, affected-ledger declarations, world events and terminal
flags. Case qualification separately reconciles the corresponding resource deltas and rollback
receipts. The complete record therefore captures a full environment/action trace rather than
an endpoint or an RL-training replay buffer.

## 3.3 Expanding the construction surface under frozen qualification

The reference tasks anchor interpretable examples but do not define the boundary of the
executable world space. Because valid component selections compile to the same task contract,
ChemWorld can instantiate families of worlds that vary in component topology, continuous
operating conditions, instrument configuration, workflow ordering and private laws.
Compositional expansion is not the scientific endpoint; it is a stress test of whether the
experimental medium remains well defined as the world-construction space grows. The same
runtime, transaction, resource and observation semantics must therefore hold across these
compositions, separating the construction surface from the number of manually curated task
identities.

The public capability map contains 15 registered reference tasks, 28 typed operation kinds,
five synthetic instrument contracts and 62 ordered task-by-metric bindings. These tasks
anchor examples across the declared surface, while component composition supplies the
expansion mechanism. We use a protocol-frozen coverage design to sample and qualify this
expanding construction space systematically. Pairwise rows cover registered discrete
component and instrument interactions; seeded Latin hypercube designs sample authored
continuous domains; and ordered-workflow targets exercise critical process sequences. These
mechanisms determine which generated compositions enter qualification, rather than defining
the extent of the world space itself.

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
the authored domains, and their covered and required counts are retained pattern by pattern
in the machine-readable coverage record.

Pairwise rows qualify declared component and instrument interfaces, while seeded continuous
designs and ordered workflows target authored bounds and critical process orderings. They are
therefore construction-coverage targets, not a claim of semantic completeness over all
higher-order chemistry. Higher-order behavior is addressed where it is explicitly present in
a workflow, module probe or interface path.

```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/first-paper-world-instrument-v1/publication/figure-2-composition-and-qualification.pdf}
\caption{\textbf{A,} The 52 generated compositions separate into 18 topology-new worlds, eight identity-new reaction--distillation worlds that reuse a registered topology, and 26 additional registered-topology coverage rows.
\textbf{B,} Topology novelty and exact task--world identity novelty are independent coordinates relative to the 64 reference task--world units.
\textbf{C,} Protocol-frozen rows vary discrete component patterns, authored continuous operating conditions and ordered workflows.
\textbf{D,} Composition changes topology, operating conditions, workflow ordering and the public instrument surface while preserving one common world contract.
Coverage defines a finite construction sample rather than the extent of the world-design space; qualification outcomes are reported in Section 4 and Appendix Table 8.}
\label{fig:qualification}
\end{figure*}
```

# 4. Qualifying experimental invariance across composed worlds

## 4.1 Qualification across reference and generated worlds

We first tested the lower-level qualification question: whether an expanding construction
surface preserves the executable contract required for controlled experiments. Qualification
therefore treated each task--world pairing as an independent unit and required successful
compilation, complete lifecycle execution, resource reconciliation and exact replay. All
64/64 reference units passed, and boundary and categorical recipes produced 1,786/1,786
complete executions. The generated block passed for all 52/52 compositions, including all
eight non-reference reaction--distillation worlds. There were no failure classes, missing
receipts or undeclared private-field-exposure findings.

Compilation success alone was not a pass condition. Each generated composition had to
execute its complete workflow, close exactly once, reconcile declared and observed
resources and replay exactly. Seven deliberately broken declarations tested missing
dependencies, conflicting state ownership, unit mismatches, invalid domains, resource
impossibility and lifecycle gaps; all seven were rejected before environment construction.
The census therefore tests contract preservation after expansion, rather than merely the
ability to instantiate additional configurations.

## 4.2 Module and interface semantics

World-level success also depends on the internal and cross-component meaning of each
transition. Thirty-two module probes exercise zero input, declared boundaries, monotonic
directions, conservation and model-specific invariants. Seven cross-module paths then check
that material amount, unit, identity and state meaning survive transfer between modules.
When applicable, the checks also include charge, energy, phase balance and event
propagation. All 32 module probes and seven interface paths passed.

These results establish each formulation as an internally coherent executable module within
its declared model-card domain. The numerical fixtures and directional oracles are internal
qualification checks; they do not by themselves constitute an independent implementation or
external physical validation. Every module enters through declared interfaces that define
where future implementations may supply alternative or empirically calibrated formulations
while retaining the task contract, transaction layer and replay machinery. Together, the
module and interface checks establish the semantic conditions under which independently
authored components can participate in larger executable worlds.

## 4.3 Fail-closed transactions, resources and replay

Contract preservation also requires a common response to invalid operations. Every
submitted action first passes schema, compatibility and resource admission. An admitted
action commits only after runtime-precondition and candidate-invariant validation; a
non-committed action records its attempt and declared penalty but does not install candidate
physical state. The 192 negative probes contain 64 invalid-schema/unknown-operation probes,
64 campaign-resource-exhaustion probes and 64 runtime-precondition probes. All produced the
registered outcome and preserved committed state as required. The evidence therefore
qualifies 128 $P=0$ admission rejects and 64 $P=1,C=0$ runtime-precondition rollbacks.
Solver-diagnostic and candidate-observation fault paths remain fail-closed implementation
semantics, but this campaign did not assign them separate qualification denominators.

```{=latex}
\begin{table}[!b]
\centering
\scriptsize
\caption{\textbf{Reader-visible branch census for the 192 negative probes.} Counts are inherited from the frozen qualification report; no post hoc probe reclassification was used.}
\label{tab:transaction-branch-census}
\begin{tabularx}{\columnwidth}{@{}L{0.16\columnwidth}rY@{}}
\toprule
Branch & $n$ & Registered class and outcome \\
\midrule
$P=0$ & 64 & schema / unknown operation; validation rejection before runtime execution \\
$P=0$ & 64 & campaign-resource exhaustion; rejection before candidate installation \\
$P=1,\ C=0$ & 64 & runtime precondition failure; rollback preserves committed physical and observation-RNG state \\
\bottomrule
\end{tabularx}
\end{table}
```

Resource accounting separates material, sample, instrument use, process time, operation
count and terminal assay. Observation checks ensure that public packets contain only
task-declared fields. Exact replay reconstructs the same compiled world from its bound
contract and seeds, resubmits the full recorded sequence of submitted typed actions---including
committed actions, preflight rejections and runtime rollbacks---and compares rewards,
observations, termination flags, transaction metadata, affected-ledger declarations, world
events, state-delta summaries and state-integrity checks with zero numerical tolerance. Case
qualification separately reconciles the corresponding resource ledger and rollback receipts.
This version-bound guarantee makes the full environment transition, rather than only the
endpoint or action list, the reproducible unit. Thus, new worlds retain common module,
interface, transaction, resource, observation and replay semantics after compilation.

# 5. Process-complete evidence and controlled world intervention

## 5.1 Complete lifecycles across diverse workflows

Eight protocol-frozen use cases test whether the same lifecycle semantics remain intact
across distinct chemical workflows. They span reaction-to-crystallization,
resource-limited equilibrium characterization, planned failure and recovery, continuous
flow, electrochemistry, distillation, partition and a second crystallization world. The
cases include single-stage and multistage processing, constrained measurement and multiple
separation modalities. Each case is treated as an independent experimental unit, and every
submitted action is audited within its complete lifecycle.

Across the eight cases, all 89 submitted actions have complete schema, transaction,
state-integrity, event, resource and public-observation receipts. Eighty-eight actions
committed and one protocol-frozen action rolled back. Every case committed one final assay,
closed its lifecycle, reconciled resources and replayed exactly with zero numerical error.
These cases establish workflow-spanning execution under one lifecycle contract rather than
introducing separate semantics for each chemical process.

## 5.2 Planned failure, rollback and recovery

The failure--recovery case embeds one deliberate invalid operation inside an otherwise
complete experiment. Its first action passed schema, compatibility and campaign-resource
admission. Runtime precondition validation then found that a separable phase had not been
established, so the transaction entered the recorded $P=1,C=0$ non-commit branch before
candidate physical state was installed. It preserved committed physical state and
observation-RNG state, produced no ghost state, and reconciled the declared attempt
consequences. The following 18 actions continued from the last committed state and
completed the recovery path, final assay, resource reconciliation and exact replay of all
19 submitted actions.

Failure is therefore part of the experimental record rather than an episode-level
exception: its attempt consequences remain auditable, while rejected physical state is
excluded from all subsequent execution. The workflow can continue without erasing its
committed history or restarting the complete experimental unit.

## 5.3 Single-private-law counterfactual interventions

Complete execution and controlled attribution require different experimental designs. The
lifecycle cases test whether diverse workflows preserve common semantics; controlled forks
instead ask whether one hidden law can be changed while every public experimental condition
remains fixed. A controlled fork holds the public task contract and action sequence fixed
while changing one protocol-frozen private component.

```{=latex}
\[
\begin{aligned}
\mathcal{W}_{p}&=(W_{\mathrm{pub}},\theta_p),&
\mathcal{W}_{c}&=(W_{\mathrm{pub}},\theta_c),\\
\theta_p&\neq\theta_c,& T_p&=T_c=T.
\end{aligned}
\]
```

The fork qualification contains six parent--child pairs: two intervention classes across
three seeds. Each pair preserved nine versioned public-contract components: task, actions,
instruments, observations, resources, failures, scoring, material catalogue and
contracted invariant/safety surface. Parent and child therefore have distinct complete-world
identities without changing the public task tuple. They executed the same
fixed typed sequence with bound randomness. Repeating both variants produced 24
deterministic fork traces. All pairs passed lineage, single-target, public-invariance,
same-sequence executability, expected state and observation divergence, and exact replay
gates. The measured divergence is therefore a trace-level effect of one private-law
intervention under fixed actions and noise identity (Fig. 3C); direction is checked separately by the frozen divergence oracle,
and the magnitude oracle also requires the registered
absolute and relative thresholds.

```{=latex}
\begin{table*}[!t]
\centering
\scriptsize
\caption{\textbf{Reader-visible specification of the two controlled-fork classes.} Public task, actions, instruments, observations, resources, failures, scoring, material catalogue and the contracted invariant/safety surface remain unchanged in every row. Thresholds were frozen before execution and require both the listed absolute and relative magnitudes plus the stated direction.}
\label{tab:fork-specification}
\begin{tabularx}{\textwidth}{@{}L{0.12\textwidth}L{0.15\textwidth}L{0.25\textwidth}L{0.19\textwidth}Y@{}}
\toprule
Fork class & Private target & Parent $\rightarrow$ child law & Registered state channel & Registered public channel \\
\midrule
Partition constitutive law & phase-partition response & partition-base response $K^{1.00}\rightarrow K^{1.75}$ & terminal organic-product amount $P_{\mathrm{org}}$ increases; $\Delta\geq10^{-4}$ mol and relative difference $\geq0.05$ & final-assay \texttt{product\_in\_organic} increases; $\Delta\geq0.02$ and relative difference $\geq0.02$ \\
Electrochemical material law & hidden electrolyte-profile effects & public profile labels stay fixed; hidden effect-row mapping $(0,1,2,3)\rightarrow(2,1,0,3)$ & terminal selective-product amount \texttt{Red} decreases; $\Delta\geq10^{-6}$ mol and relative difference $\geq0.01$ & final-assay \texttt{ohmic\_efficiency} decreases; $\Delta\geq0.05$ and relative difference $\geq0.05$ \\
\bottomrule
\end{tabularx}
\end{table*}
```

In the electrochemical fork, the permutation reassigns hidden electrolyte-response profiles
to fixed public material labels. It therefore represents a matched change in private material
properties rather than an identifier remapping or a change in the public catalogue.

```{=latex}
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{figures/first-paper-world-instrument-v1/publication/figure-3-controlled-forks.pdf}
\caption{\textbf{Execution, intervention and agent access.}
\textbf{A,} Eight frozen execution cases span crystallization, resource-limited characterization, planned failure and recovery, continuous flow, electrochemistry, distillation and partition workflows under one shared lifecycle semantics.
\textbf{B,} A runtime-precondition failure at step 1 remains inside the same experimental record; recovery continues from committed state through 18 subsequent commits and final assay.
\textbf{C,} Controlled private-law forks hold the public contract, typed action sequence and bound randomness fixed while changing one private law, and a separate non-reference world supports deterministic qualification and a provider-driven agent lifecycle through the same public contract.}
\label{fig:controlled-forks}
\end{figure*}
```

# 6. Agent access through a common experimental contract

## 6.1 Evaluator-complete process readouts

Once complete trajectories are available, agent evaluation need not collapse an experiment
into a single endpoint. ChemWorld retains terminal commitment, evidence acquisition,
evidence-conditioned action, resource deployment and outcome trajectory as separate
evaluator-visible groups. Nineteen registered process dimensions preserve this structure
without a composite score. The evaluator can inspect complete simulator state, failure and
resource consequences while the agent remains restricted to the public task contract. This
is an agent-evaluation surface enabled by the qualified record, not a comparative agent
benchmark.

## 6.2 Agent-relevant interaction patterns

Two qualified interaction patterns illustrate what this evaluation surface makes possible.
In a resource-limited phase-observation world, an agent must decide whether additional pH or
UV--visible evidence justifies scarce sample and instrument expenditure, then terminate
explicitly when the evidence is sufficient. In the recovery world, a structured rollback
permits a revised typed action without erasing committed experimental history or restarting
the experiment. The deterministic cases in Section 5 qualify these interaction primitives;
comparative policy behavior is reserved for subsequent studies.

## 6.3 Complete-agent integration on a non-reference world

The separation between deterministic world qualification and provider-driven agent access
is summarized in Fig. 3C. The selected protocol-frozen non-reference reaction--distillation world was evaluated
through two independent execution units. A 12-action deterministic path qualified
construction, lifecycle closure and replay; a separate provider-driven language-model agent
then completed a 15-action lifecycle through the same public instrument contract. This
separation prevents agent behavior from serving as evidence for world qualification.

The fixed scaffold supplied the public task card, typed tool schemas, resource contract and
explicit termination/final-assay requirement. The agent received only this public surface
and issued every operation, including termination and final assay. One uninterrupted session
submitted 15 actions under one fixed model/provider configuration. All 15 committed and
closed the lifecycle, with zero rollback, right-censoring or undeclared private-field exposure.

The environment used 8,158.454 of 10,440 simulated process seconds, four of four instrument
uses and 0.00085 of 0.001 L sample. The complete record links each decision to its public
observation, hidden simulator consequence, transaction result and resource debit. The
recorded 15-step submitted-action trace---all 15 actions committed---replayed with zero
numerical mismatch, showing that
a provider-driven experiment can enter the same auditable record as deterministic use cases.
This is an interface-integration result rather than an agent-capability claim.

# 7. Discussion

## 7.1 World construction as an experimental variable

ChemWorld's principal methodological contribution is a new locus of experimental control.
Composition specifies what may vary in the world; the public contract specifies what must
remain comparable; and the transaction and record layers preserve the consequences of each
interaction. Researchers can therefore vary component topology, continuous conditions and
private laws, then reset and repeat matched worlds while inspecting simulator-side process
consequences under explicit compute and storage budgets. The result is not simply a larger
catalogue of environments but a qualified surface on which world construction itself can be
planned as an experimental variable.

The evidence supporting this claim remains deliberately layered. Full-census, module,
interface and negative-path qualification establish that declared worlds preserve a common
executable contract after composition. Process-complete cases and controlled forks then show
that the qualified substrate supports multistage workflows, failure recovery and attributable
private-law intervention. Finally, the same public instrument contract exposes these worlds
to an agent while the evaluator retains a complete process record. Separating world
correctness, experimental capability and agent access prevents any one layer from serving as
evidence for the others.

## 7.2 A substrate for controlled studies of experimental agency

Once the world can be varied independently of the public task contract, the research question
can move beyond whether an agent reaches an endpoint. A process-complete record reveals how
evidence, resources, failures and terminal commitment produced that endpoint. The 19 process
dimensions preserve these factors as separate evaluator-visible coordinates, supporting
future studies of measurement strategy, recovery after invalid actions, resource deployment
and decision timing that disappear when an experiment is reduced to one score. The
complete-agent unit shows that a provider-driven trajectory can enter this record without
being used to qualify the underlying world.

Controlled private-law forks add the matched counterfactual needed to study response to a
changed world. Parent and child expose the same actions, instruments and resources while one
hidden law changes under the same typed sequence and bound randomness. Outcome and
observation differences in the reported traces can therefore be assigned to that simulator
intervention. This paper establishes the substrate and attribution logic; it does not yet
claim comparative evidence about agent adaptation, law learning or scientific reliability.
Those questions require separately frozen policy protocols layered on the qualified worlds.

## 7.3 A modular bridge to physical experimentation

The released qualification establishes compositional expansion within the declared component
vocabulary and authored model domains. Those boundaries expose extension points rather than
fixed task walls. The
interfaces are designed to support additional constitutive laws, calibrated unit operations,
empirical instrument models and new agents through the same task contract, although the
present study does not measure third-party implementation effort or demonstrate that an
independently authored module inherits every guarantee without integration work.

ChemWorld and physical SDLs therefore provide complementary experimental regimes. Software
worlds supply controlled repetition, counterfactuals, evaluator-complete observability and
rapid hypothesis narrowing without direct wet-laboratory consumable use; physical systems
provide real-material execution and calibration. A shared experimental logic can use
software-scale evidence to focus subsequent laboratory work on the conditions and mechanisms
that require physical validation.

## 7.4 Qualification scope

The reported qualification establishes executable semantics and authored-model coherence for
this software-scale experimental regime within the declared component vocabulary and
compatibility domain, not universal chemical or physical fidelity. The synthetic instruments are controlled software observation models,
not calibrated replicas of particular devices. Coverage samples frozen authored axes and is
not an exhaustive enumeration of chemical space. The fork experiments establish the
registered single-private-law interventions, not every possible intervention type. The
module fixtures and directionality oracles primarily test internal consistency with the
authored models; they are not substitutes for an independent reference implementation,
fault-mutation study or empirical validation. The
complete-agent run demonstrates interface integration rather than agent capability or model
superiority. Exact replay is limited to the bound environment/action trace and does not imply
policy re-execution, cross-platform numerical identity or cross-version archival replay.

# 8. Methods

## 8.1 Construction and compatibility

A composition declaration specifies component roles and parameters plus the public task
surface. Normalization is deterministic. Compatibility checks cover dependencies, state
ownership, unit agreement, parameter domains, resource feasibility, operation exposure,
instrument availability and the existence of a closed lifecycle. A rejected declaration
returns structured diagnostics and does not construct an environment.

The task contract is the authoritative public boundary. Runtime validation is restricted
to the declared operations and instruments. Private constitutive laws, material identities
and hidden simulator state remain evaluator-owned in $\theta$; the public contract contains
$W_{\mathrm{pub}}$ and $S_{0,\mathrm{pub}}$, not the complete private world identity. The 15 registered tasks are mapped into
the same component and contract representation used by generated compositions.

## 8.2 Coverage design

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

## 8.3 Qualification measurements

For each case, the report records normalized construction input, compile diagnostics,
public contract, action sequence, schema and transaction status, state-integrity checks,
events, resource preflight and outcome, public observation, termination, trajectory size
and exact replay. Missing receipts, non-finite quantities, unexpected commits or
rollbacks, undeclared private-field exposure, denominator drift and replay mismatch fail the case.

Reference qualification covers 64 task--world units and 1,786 complete recipes. Generated
qualification covers 52 compositions. Negative qualification covers 192 invalid probes.
Module and interface qualification use 32 and seven units, respectively. Compile mutation
uses seven invalid declarations. Counts are exact qualification denominators.

The 32 process-module probes form an $8\times4$ design: each of reaction, thermal, phase,
separation, crystallization, distillation, continuous flow and electrochemistry contributes
one zero-input bounded-runtime probe, one valid low/high probe, one directionality probe and
one runtime-invariant probe. Valid low/high checks use numerical reference fixtures for
seven modules and a declared conceptual/synthetic fixture for crystallization;
directionality checks are declared conceptual/synthetic oracles. Every numerical fixture
records its own tolerance. Observation is qualified separately through instrument,
sample-accounting, bounded-signal and public/private-boundary checks. The seven compile
mutants comprise two missing-dependency cases and one case each for conflicting state
ownership, unit mismatch, invalid parameter domain, lifecycle hole and resource
impossibility.

## 8.4 Process-time envelopes

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

## 8.5 Deterministic use cases

The eight cases, seeds and action lists were protocol-frozen before execution. Their total expected
census was 89 submitted actions, 88 commits, one rollback and eight final assays. The
failure--recovery case specified the failing action and rollback class in advance. All
submitted actions were inspected as one deterministic census, isolating instrument
qualification from provider variance.

## 8.6 Controlled forks

Each fork declares a parent, a child, one protocol-frozen private intervention target, an
invariant public contract and expected divergence channels. Parent and child execute the same typed action
sequence. Gates require lineage validity, exactly one changed private target, invariant
public contract, executable sequence on both variants, expected physical and observation
divergence and exact replay under deterministic execution.

For an aligned checkpoint value $p$ in the parent and $c$ in the child, the oracle records the
signed change $\delta=c-p$, its magnitude $\Delta=|\delta|$, and the relative difference
${\Delta}/{\max(|p|,|c|,s_0)}$, where $s_0$ is the declared positive scale floor. A magnitude
passes only when both the absolute and relative thresholds for that expectation are met; the
direction oracle is checked separately from the magnitude.

## 8.7 Process readouts

The process profile retains 19 dimensions in five groups: terminal commitment, evidence
acquisition, evidence-conditioned action, resource deployment and outcome trajectory.
Undefined conditional quantities remain null rather than being set to zero. The resulting
coordinate vector preserves process structure for subsequent agent studies and supports
dimension-level comparison without a composite score. The released process-coordinate
contract supplies each dimension's numerator, denominator, value range, null condition and
boundary-case rule together with the computation binding used by the reports.

## 8.8 Complete-agent non-reference-world protocol

The formal unit is one complete lifecycle on the first protocol-frozen non-reference
reaction--distillation composition. The protocol binds one uninterrupted agent session, one
model/provider/scaffold configuration and at most 16 submitted actions through the public
instrument interface. Termination and final assay must be agent-issued. The action count,
tool calls and trajectory records must agree exactly; every action must commit; the
lifecycle must contain one termination and exactly one final assay; resources, public
boundary and exact replay must pass.

The reported unit ran on 5 August 2026 with OpenAI GPT-5.6-sol at medium reasoning effort
through the Codex subscription provider. This model, provider and scaffold binding applies
only to the interface-integration demonstration.

Provider accounting distinguishes one provider session, one logical agent turn, 15 action
calls and two read-only calls. The model, provider, reasoning effort, scaffold constraints,
public prompt template and execution date are bound before the run. Cumulative input is
separated into cached and uncached input; cached context is reused input, not repeated
output. The formal limits are 640,000 cumulative input tokens, 192,000 uncached input tokens
and 64,000 output tokens. Per-action wait is capped at 600 s, finalization at 300 s and
runner reserve at 600 s, giving a conservative method wall limit of 10,500 s. These method
resources are separate from the simulated process-time ledger.

## 8.9 Public boundary and exact replay

The evaluator owns hidden simulator identity and private state. Agent-facing task cards,
observations and histories are checked for hidden fields and absolute private paths. Replay
reconstructs the bound world from the same normalized contract, runtime, mechanism,
observation and scoring identities plus the recorded seeds and interventions. It then
resubmits every submitted typed action in recorded order, including committed actions,
validation/preflight rejections and runtime rollbacks, and compares rewards, every public
observation, termination and truncation flags, operation types, transaction status, rollback
reason, affected-ledger declarations, world events, state-delta summaries and state-integrity
checks. Case qualification joins this replay result to the separately reconciled resource
ledger and rollback receipts. The reported qualification uses numerical tolerance zero and
observed a maximum absolute error of zero.
In this paper, leakage means undeclared direct exposure of evaluator-owned fields, private
identifiers or absolute private paths. It does not mean inferential information about hidden
state conveyed through task-declared measurements.
We use exact replay narrowly for environment/action-trace reconstruction under the bound
software identities. Policy re-execution, cross-platform numerical reproduction and
cross-version archival replay are separate reproducibility questions and are not inferred
from a zero-error environment replay. The public release contains the environment evidence
needed for this reconstruction while keeping authentication data, private reasoning and
unrestricted provider payloads outside the research artifact.

# 9. Data and code availability

Code, configuration, processed reports, figure source data and release tooling are
available in the MIT-licensed ChemWorld repository at
[github.com/sunyrain/ChemWorld](https://github.com/sunyrain/ChemWorld). The tracked
materials regenerate the tables and figures and replay released simulator transitions and
resource changes. The current arXiv bundle contains the manuscript source, dependency lock,
processed evidence, figure data, coverage records and build manifest used for this
submission. At immutable public deposition, release metadata will bind this package to the
final full Git commit identifier and archive identifier; no archive DOI is claimed before
that deposition. Provider authentication, unrestricted response bodies, private reasoning
and hidden evaluator identities are excluded.

The release supports three complementary reproducibility layers. Processed evidence
regenerates the reported counts and figures. Released trajectories reconstruct environment
transitions, public observations and ledgers. Provider provenance binds the model,
configuration and call accounting for the complete-agent unit. Exact replay refers to the
executable world and its complete experimental record. In this paper, environment/action-trace
replay is distinct from policy re-execution, cross-platform numerical reproduction and
cross-version archival replay. Provider provenance supports audit of the complete-agent unit
but does not imply that a later model call will regenerate the same actions.

# 10. Conclusion

ChemWorld establishes a software-scale experimental regime in which world construction
itself can be controlled. Reusable components make topology, operating conditions,
instrument configuration and private mechanisms programmable; one public contract preserves
agent-facing operations, observations, resources, failures, termination and evaluation; and
every submitted action enters a version-bound replayable transaction record. The world is
therefore no longer only the fixed background of a task, but an explicit part of experimental
design.

The evidence establishes the conditions required for that shift. Full-census, module,
interface and negative-path qualification show that composed worlds preserve a common
executable contract. Process-complete use cases and controlled forks place failure, recovery
and single-private-law intervention inside attributable replayable experiments. A separate
complete-agent unit shows that the same public instrument contract can support
provider-driven action selection without using agent behavior to qualify the world itself.

Within the declared component vocabulary and authored model domains, ChemWorld thus provides
a programmable medium for controlled counterfactual studies of experimental agency,
resource-aware experimentation and systematic process analysis. It does not establish
universal chemical fidelity or agent superiority. Rather, it complements physical
laboratories: software worlds supply exact reset, matched intervention and complete
simulator-side records, while physical systems supply real-material evidence and calibration.

# Appendix. Extended capability, qualification and process records

## A. Reader-facing capability and use-case map

A reference task--world unit pairs a registered task identity with a scenario identity as
defined in Section 3.1. The 15 task identities below expand to 64 such units across their
declared scenario seeds. A generated row overlaps the reference set only when both its task
identity and scenario identity match a registered unit; the eight protocol-frozen
non-reference rows have zero such overlap.

## A.1 Representative instrument-use cases

The following cases isolate complementary process and record semantics; they do not define a
cross-task performance ranking.

- **Reaction to crystallization.** *Components:* reaction, thermal, crystallization and
  observation. *Record:* propagation through seeding, cooling, filtration and final assay.
- **Resource-limited characterization.** *Components:* phase and observation. *Record:*
  measurement choice, sample consumption and explicit stopping under a small budget.
- **Failure and recovery.** *Components:* reaction, thermal, phase, separation and
  observation. *Record:* atomic rollback, attempt consequences and continuation from
  committed state.
- **Controlled private-law fork.** *Components:* one registered component changed privately.
  *Record:* an invariant public contract with protocol-specified state/observation divergence.
- **Generated reaction to distillation.** *Components:* reaction, thermal, distillation and
  observation. *Record:* construction and replay outside the reference task identities; one
  complete-agent lifecycle closed under the same public contract.
- **Reference library.** *Components:* flow, electrochemistry, distillation, partition and
  crystallization. *Record:* breadth of reusable task recipes without a cross-task score.

## A.2 Registered tasks and component patterns

```{=latex}
\makeatletter
\setlength{\@dblfptop}{0pt}
\makeatother
\begin{table*}[!t]
\centering
\scriptsize
\caption{\textbf{Complete reference-task registry.} Seed counts define the scenario identities exercised for each task.}
\label{tab:reference-registry}
\begin{tabularx}{\textwidth}{@{}L{0.22\textwidth}L{0.32\textwidth}rY@{}}
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
\begin{table*}[!t]
\centering
\small
\caption{\textbf{Representative component-pattern library.} Reusable component combinations expose a common operation and instrument surface across single-process and multistage worlds.}
\label{tab:component-pattern-library}
\begin{tabularx}{\textwidth}{@{}L{0.19\textwidth}L{0.20\textwidth}YL{0.19\textwidth}@{}}
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

```{=latex}
\FloatBarrier
```

## B. Coverage reconstruction and qualification census

The coverage design below fixes the pattern, seed, continuous domain, workflow count and
generated denominator. Discrete factors include component-specific family or profile
choices and instrument profiles; the released machine-readable coverage records map every
discrete level, compatible pair, continuous stratum and ordered interaction to the rows
that cover it. Covered and required counts are identical for all four target classes:
60/60 levels, 180/180 compatible pairs, 212/212 continuous strata and 84/84 ordered
interactions.

```{=latex}
\begin{table*}[!t]
\centering
\small
\caption{\textbf{Topology and identity decomposition of the generated block.} Topology novelty compares exact component sets with the 15-task reference registry; task--world novelty uses exact registered identities.}
\label{tab:novelty-decomposition}
\begin{tabularx}{\textwidth}{@{}L{0.33\textwidth}rL{0.22\textwidth}Y@{}}
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
\begin{table*}[!t]
\centering
\scriptsize
\caption{\textbf{Protocol-frozen coverage design.} Bounds are inclusive authored domains; ``none'' denotes a purely discrete design.}
\label{tab:coverage-design}
\begin{tabularx}{\textwidth}{@{}L{0.21\textwidth}rYL{0.10\textwidth}r@{}}
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
\begin{table*}[!t]
\centering
\small
\caption{\textbf{Qualification census.} Every registered execution, probe, deterministic-use and controlled-fork denominator completed without missing receipts or unexpected outcomes.}
\label{tab:qualification-census}
\begin{tabularx}{\textwidth}{@{}YrrY@{}}
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

```{=latex}
\FloatBarrier
```

```{=latex}
\clearpage
\twocolumn[
\begin{@twocolumnfalse}
\subsection{C. Process-coordinate dictionary}\label{appendix-c.-process-coordinate-dictionary}
\noindent The 19 coordinates are campaign-level descriptions, not a composite score.
\(N_p\), \(N_c\), \(N_a\), \(N_d\) and \(N_m\) denote planned, closed, assayed,
discarded and measured lifecycles, with \(N_c=N_a+N_d\) because the frozen lifecycle
contract closes only by assay or discard. Undefined conditional quantities remain null;
they are never replaced by zero.
\par\medskip
\centering
\footnotesize
\renewcommand{\arraystretch}{0.88}
\captionsetup{hypcap=false}
\captionof{table}{\textbf{The 19 process coordinates.} Numerators, denominators, null rules and interpretation are fixed by the process-profile contract. None is interpreted as a globally better direction unless explicitly stated.}
\label{tab:process-coordinates}
\begin{tabularx}{\textwidth}{@{}L{0.16\textwidth}L{0.24\textwidth}L{0.20\textwidth}Y@{}}
\toprule
Coordinate & Definition & Null or boundary rule & Interpretation \\
\midrule
\multicolumn{4}{@{}l}{\textit{Terminal commitment}} \\
Closed lifecycle fraction & $N_c/N_p$ & defined as 0 when $N_p>0$ and none closes & completion gate; no preferred assay/discard mix \\
Assay commitment fraction & $N_a/N_c$ & null when $N_c=0$ & fraction of closed lifecycles committed to final assay \\
Discard fraction & $N_d/N_c$ & null when $N_c=0$ & fraction of closed lifecycles deliberately discarded \\
\addlinespace
\multicolumn{4}{@{}l}{\textit{Evidence acquisition}} \\
Measured lifecycle fraction & $N_m/N_c$ & null when $N_c=0$ & prevalence of at least one committed non-final measurement \\
Instrument uses per closed lifecycle & committed non-final measurements $/N_c$ & null when $N_c=0$ & measurement intensity \\
First-measurement timing & mean of preceding attempts $/$ attempts through termination & null when $N_m=0$ & lower values mean earlier evidence acquisition, not higher quality \\
\addlinespace
\multicolumn{4}{@{}l}{\textit{Evidence-conditioned action}} \\
Post-measure continuation prevalence & lifecycles with a later committed physical operation $/N_c$ & null when $N_c=0$ & prevalence of evidence followed by further investment among closed lifecycles \\
Post-measure operations per closed lifecycle & later committed physical operations $/N_c$ & null when $N_c=0$ & deployment intensity after first evidence \\
Threshold-eligible fraction & lifecycles with the frozen diagnostic and finite signal $/N_c$ & null when $N_c=0$ & denominator gate for the diagnostic decision rule \\
Evidence-to-terminal concordance & terminal choices matching the frozen signal rule $/$ eligible lifecycles & null when no lifecycle is eligible & agreement between declared evidence rule and assay/discard decision \\
\addlinespace
\multicolumn{4}{@{}l}{\textit{Resource deployment}} \\
Attempted operations per closed lifecycle & charged operation attempts $/N_c$ & null when $N_c=0$ & includes validation failures and transactional rollbacks \\
Committed operations per closed lifecycle & committed typed operations $/N_c$ & null when $N_c=0$ & installed operation intensity \\
Cost per closed lifecycle & campaign cost-ledger debit $/N_c$ & null when $N_c=0$ & includes declared failed-attempt charges \\
Risk debit per closed lifecycle & campaign risk-ledger debit $/N_c$ & null when $N_c=0$ & resource-card-specific risk deployment \\
\addlinespace
\multicolumn{4}{@{}l}{\textit{Outcome trajectory}} \\
Global-best discovery fraction & $(j^\star-1)/(N_a-1)$, $j^\star\in\{1,\ldots,N_a\}$ & null for no assay; defined as 0 for one assay & lower values mean earlier discovery of the observed best \\
Online incumbent retention & later assays retaining at least 90\% of the prior incumbent $/(N_a-1)$ & null when $N_a<2$ & stability after the first assay \\
Maximum incumbent drawdown & $\max(\text{prior incumbent}-\text{next assay},0)$ & null when $N_a<2$ & largest observed loss from the running best \\
Loss-episode recovery rate & recovered loss episodes $/$ observed loss episodes & null when no loss episode occurs; terminal unresolved losses count unrecovered & recovery after an observed loss \\
Terminal-to-best retention & terminal assayed score $/$ observed best assayed score & null when no positive assay exists & closeness of the terminal assay to the observed best \\
\bottomrule
\end{tabularx}
\end{@twocolumnfalse}
]
```

Outcome-trajectory coordinates are computed only after applying each task's frozen score
orientation and scale binding. Raw values are not interpreted across incompatible task
metrics.

```{=latex}
\clearpage
\twocolumn[
\begin{@twocolumnfalse}
\subsection{D. Component model cards and extension points}\label{appendix-d.-component-model-cards}
\centering
\footnotesize
\renewcommand{\arraystretch}{0.90}
\captionsetup{hypcap=false}
\captionof{table}{\textbf{Component model cards and extension points.} Each module declares its runtime formulation, authored model domain, qualification oracle and extension interface for future alternative or empirically calibrated implementations.}
\label{tab:component-model-cards}
\begin{tabularx}{\textwidth}{@{}L{0.12\textwidth}L{0.19\textwidth}L{0.18\textwidth}L{0.20\textwidth}Y@{}}
\toprule
Component & Runtime formulation & Principal authored domain & Qualification oracle & Intended use and extension path \\
\midrule
Reaction & stoichiometric mass-action network with Arrhenius temperature dependence & authored reaction families and bounded batch temperature/time & exact amount fixtures, monotonic response, material closure and runtime invariants & reaction-law extension point for future named-reaction calibration \\
Thermal & dynamic batch heat-release and jacket-energy balance & bounded temperature, duration, vessel pressure and volume & temperature/energy finiteness, bounds, event propagation and ledger reconciliation & thermal-contract extension point for future equipment-specific coefficients \\
Phase & stability-gated, activity-corrected liquid--liquid equilibrium with TPD-style diagnostics & declared phase identities, volumes and composition ranges & phase/material balance, directional partition response and state identity & activity-model extension point for future compound-specific thermodynamics \\
Separation & settling, entrainment, wash and transfer coupled to the phase model & bounded mix/settle time, extractant/wash volume and transfer fraction & amount/unit conservation, transfer identity and expected directional response & separation-interface extension point for future hardware-scale transport \\
Crystallization & van't Hoff solubility with seed, nucleation/growth cohorts, impurity occlusion and CSD summaries & bounded seed mass, cooling temperature and cooling time & material closure, solubility-direction checks, CSD and runtime-invariant receipts & law extension point for future calibrated nucleation and growth models \\
Distillation & bubble-gated, duty-limited VLE/Fenske fractionation with material and energy ledgers & bounded temperature/time, reflux ratio, fraction count and collected fraction & mass/energy closure, fraction identity, recovery/purity directions and equipment limits & operation-contract extension point for future compound and column models \\
Continuous flow & geometry-resolved plug-flow reactor with residence time, distributed thermal boundary and pressure drop & bounded flow, residence time and temperature & conversion direction, mass closure, pressure/geometry and solver diagnostics & runtime extension point for future reactor-specific transport or control models \\
Electrochemistry & Nernst potential, Butler--Volmer kinetics, limiting current, Randles transient and Faraday accounting & bounded potential, current and electrolysis time & charge/material closure, signed work, selectivity and limiting-current checks & electrochemical-law extension point for future material- and cell-specific parameters \\
Observation & state-coupled synthetic pH, UV--visible, HPLC, GC and final-assay contracts & task-declared instruments, sample and use budgets & instrument availability, sample consumption, finite/bounded signal and non-omniscience checks & instrument-schema extension point for future empirical response models \\
\bottomrule
\end{tabularx}
\end{@twocolumnfalse}
]
```
