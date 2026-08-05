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
  Executable chemistry environments are commonly presented as fixed task suites, although
  an instrument-like platform also requires an account of how worlds are constructed and
  whether their semantics survive composition. We present ChemWorld as a composable
  executable chemical-world substrate and programmable virtual instrument. A world is
  declared from a finite vocabulary of reusable physical and transactional components;
  a task contract attaches an initial state, operations, instruments, observations,
  resources, termination and evaluation. The 15 registered tasks are reference examples,
  not an exhaustive benchmark or a bound on the world space. Qualification covered 64/64
  reference world units and 1,786/1,786 complete reference recipes, together with 52/52
  coverage-generated compositions, including eight frozen reaction--distillation
  compositions absent from the reference identities. All 192 invalid-action probes, 32
  module probes, seven interface paths and seven compile-time mutants produced their
  registered outcomes, with zero missing receipts or public-state leakage. Across eight
  deterministic instrument-use cases, 89/89 submitted actions were audited: 88 committed,
  the single planned failure rolled back without ghost state, all eight lifecycles closed,
  every resource ledger reconciled and every trajectory replayed exactly. Six controlled
  single-private-component fork pairs additionally preserved the public contract across 24
  provider-free traces. These results qualify reusable components and coverage-guided
  compositions inside the declared v1 domain; they do not validate every possible task,
  establish laboratory accuracy or rank agent systems. One complete agent then operated
  the fixed unseen world in a single uninterrupted session: all 15 submitted actions
  committed, one termination and one final assay closed the lifecycle, the declared
  process and provider resources remained within their separate limits, and the complete
  trajectory replayed exactly.
---

# 1. Introduction

An executable chemistry environment is often introduced by listing the tasks that it can
run. That list is useful, but it does not answer three architectural questions: what a
world is made from, which combinations are legal, and whether a newly assembled world
preserves the semantics of the underlying apparatus. A reusable scientific environment
must compose physical modules, operations, instruments, resources and termination without
silently changing units, state identity, failure behaviour or replay.

ChemWorld addresses this problem by treating a chemical world as an explicit executable
object rather than an opaque task label. Its v1 vocabulary contains reaction, thermal,
phase, separation, crystallization, distillation, continuous-flow, electrochemical and
observation components. A world is a compatible selection of these components, their
parameters and private laws. A task contract is
$T=(W,S_0,A,I,O,R,\tau,E)$: the world, initial state, operations, instruments,
observations, resources, termination rule and evaluation surface. A scenario instantiates
that contract; a trajectory is the resulting operation--observation sequence; and a world
fork is a controlled intervention that changes one private component while preserving the
public contract. Keeping these layers distinct prevents a finite task catalogue from being
mistaken for the space of worlds or trajectories (Fig. 1).

Existing platforms expose complementary parts of this problem. Optimization suites such
as Summit and Olympus provide repeatable algorithmic comparisons, but commonly represent
an experiment as a value-returning query [@felton2021summit; @hase2021olympus]. Physical
self-driving laboratories and chemistry agents establish whether workflows can be
executed on real apparatus [@boiko2023autonomous; @bran2024augmenting;
@szymanski2023alab; @dai2024mobile; @darvish2025organa; @vriza2026instruments].
Interactive scientific worlds extend evaluation toward active experiment selection and
law recovery [@jansen2024discoveryworld; @gandhi2025boxinggym; @duan2025scigym;
@nagele2026sciexplorer; @zheng2026newtonbench]. ChemWorld is complementary to each: it
provides a controlled virtual apparatus in which construction, action authority,
observations, resources, failure and replay are explicit, while making no claim of
physical-laboratory transfer.

The central qualification question is therefore not whether a system succeeds on a fixed
list of tasks. It is whether reusable components and their declared interfaces remain
coherent when assembled into coverage-guided combinations, including combinations not
represented by the reference task identities. This paper contributes:

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
6. a single complete-agent lifecycle on the first frozen unseen composition, used only to
   demonstrate access through the same public instrument contract.

The scope is deliberately finite. We validate the declared v1 vocabulary and compatibility
domain, not every possible task. The physical modules are synthetic or conceptual models
within stated domains, not digital twins. A complete agent is one possible user of the
instrument, but explaining why it acts, attributing behaviour to a model or scaffold, and
measuring adaptation under changed laws require a separate study.

```{=latex}
\begin{figure*}[!tbp]
\centering
\includegraphics[width=\textwidth]{figures/first-paper-world-instrument-v1/publication/figure-1-object-hierarchy.pdf}
\caption{\textbf{Object hierarchy and public instrument contract.}
\textbf{A,} Reusable physical and transactional components compile into a world.
\textbf{B,} A task contract attaches the initial state, actions, instruments, observations, resources, termination and evaluation surface.
\textbf{C,} Scenarios instantiate a task, trajectories record interaction, and a world fork is a separate single-private-component intervention.
\textbf{D,} Fifteen registered tasks are reference points across the declared surface, not the size of the world space.}
\label{fig:hierarchy}
\end{figure*}
```

# 2. A public construction surface for executable worlds

## 2.1 Components, worlds and task contracts

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

## 2.2 Coverage-guided generation

Composition generation is driven by coverage targets rather than by a desired number of
examples. Discrete component and instrument choices are arranged with pairwise covering
rows. Continuous temperature, time, flow, volume, potential, current, reflux and transfer
axes are sampled with seeded Latin hypercube designs. Ordered workflows separately require
critical interactions such as reaction before separation, quench before downstream
transfer and fraction collection before final measurement.

The frozen design contains eight component patterns, from phase--observation through
reaction--phase--separation--observation. It generated 52 compositions. Eight use a
reaction--thermal--distillation--observation pattern that is absent from the 15 reference
task identities and was frozen after the constructor and compatibility rules were fixed.
The first generated row of this unseen batch is also the fixed target for the complete-agent
instrument demonstration; it cannot be replaced after its result is known.

```{=latex}
\begin{figure*}[!tbp]
\centering
\includegraphics[width=\textwidth]{figures/first-paper-world-instrument-v1/publication/figure-2-composition-coverage.pdf}
\caption{\textbf{Coverage-guided construction beyond the reference task identities.}
\textbf{A,} Eight component patterns define the frozen construction blocks.
\textbf{B,} Pairwise discrete coverage, seeded space-filling continuous samples and ordered workflow interactions determine the generated rows.
\textbf{C,} The 15 reference tasks provide a structural basis, while 52 generated compositions exercise additional combinations.
\textbf{D,} Eight frozen reaction--distillation compositions are unseen with respect to the reference identities; unseen does not mean unbounded or arbitrary.}
\label{fig:coverage}
\end{figure*}
```

# 3. Qualification of components, interfaces and runtime semantics

## 3.1 Reference and generated full censuses

The reference qualification treats a world unit as a task--world pairing rather than a
single task label. All 64/64 reference units passed. Boundary and categorical recipes
produced 1,786/1,786 complete executions. The generated block passed for all 52/52
compositions, including all eight unseen reaction--distillation rows. There were no
failure classes, missing receipts or public/private leakage findings.

Compilation success alone was not a pass condition. Each generated composition had to
execute its complete workflow, close exactly once, reconcile declared and observed
resources and replay exactly. Seven deliberately broken declarations tested missing
dependencies, conflicting state ownership, unit mismatches, invalid domains, resource
impossibility and lifecycle gaps; all seven were rejected before environment construction.

## 3.2 Physical and cross-module checks

Thirty-two module probes exercise zero input, declared boundaries, monotonic directions,
conservation and model-specific invariants. The seven cross-module paths then check that
material amount, unit, identity and state meaning survive transfer between modules. When
applicable, the checks also include charge, energy, phase balance and event propagation.
All 32 module probes and seven interface paths passed.

These results establish internal qualification within each model card. They do not show
that the synthetic kinetics, spectra, phase equilibria or equipment responses predict a
particular physical laboratory. The validity claim is therefore interface and virtual-
instrument validity, not empirical chemical accuracy.

## 3.3 Transactions, resources, observations and replay

Every submitted action first passes schema, compatibility and resource preflight. A valid
action commits atomically. A rejected action records its attempt and declared penalty but
does not install candidate physical state. The 192 negative probes cover invalid schema,
preconditions, resource exhaustion, terminal closure and other fail-closed paths; all 192
produced the registered rejection and preserved state as required.

Resource accounting separates material, sample, instrument use, process time, operation
count and terminal assay. Observation checks ensure that public packets contain only
task-declared fields. Exact replay reconstructs environment transitions, observations and
resource consequences from the immutable record; it does not reproduce a physical batch
or a provider's token sequence.

```{=latex}
\begin{figure*}[!tbp]
\centering
\includegraphics[width=\textwidth]{figures/first-paper-world-instrument-v1/publication/figure-3-qualification-census.pdf}
\caption{\textbf{Full-census qualification of the virtual instrument.}
\textbf{A,} All reference and generated world units passed their complete workflows.
\textbf{B,} Module and interface probes cover physical invariants and cross-module transfer.
\textbf{C,} Invalid declarations and actions fail closed before or without physical-state commit.
\textbf{D,} Missing receipts, public-state leakage and registered failure classes were all zero. Counts are qualification denominators, not statistical samples.}
\label{fig:qualification}
\end{figure*}
```

# 4. Deterministic instrument-use cases

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
path. It establishes construction, workflow execution and replay for the fixed unseen
world, but it is not a substitute for the separate complete-agent unit reported below.
That unit originated every submitted action from one uninterrupted session and was judged
against its own lifecycle, provider-resource and replay gates.

```{=latex}
\begin{figure*}[!tbp]
\centering
\includegraphics[width=\textwidth]{figures/first-paper-world-instrument-v1/publication/figure-4-use-cases-and-recovery.pdf}
\caption{\textbf{Deterministic cases exercise lifecycle and failure semantics.}
\textbf{A,} Eight frozen cases span single-process, multistage and reference-library workflows.
\textbf{B,} Eighty-eight of 89 submitted actions committed; one preregistered precondition failure rolled back.
\textbf{C,} The rollback preserved physical state and allowed the remaining 18-step recovery path to close.
\textbf{D,} All eight final assays, resource ledgers and exact replays passed.}
\label{fig:use-cases}
\end{figure*}
```

# 5. Controlled single-component forks

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

```{=latex}
\begin{figure*}[!tbp]
\centering
\includegraphics[width=\textwidth]{figures/first-paper-world-instrument-v1/publication/figure-5-controlled-forks.pdf}
\caption{\textbf{Controlled forks change one private component under an invariant public contract.}
\textbf{A,} Parent and child share operations, instruments, observations, resources, failure rules, termination and evaluation.
\textbf{B,} The intervention changes one private constitutive or material law.
\textbf{C,} Six pairs and 24 provider-free traces pass all registered gates.
\textbf{D,} Physical-state and public-observation divergences occur in the preregistered channels while both sides replay exactly.}
\label{fig:forks}
\end{figure*}
```

# 6. Process records beyond endpoints

An endpoint cannot reconstruct how it was reached. ChemWorld therefore keeps terminal
commitment, evidence acquisition, continued process investment, resource deployment,
failure and outcome trajectory as separate coordinates. Nineteen registered process
dimensions remain separate; no unregistered scalar intelligence score is formed.

One archived matched trajectory pair illustrates the distinction without supporting a
model comparison. The raw terminal-score contrast was only 0.003, yet the same pair
differed by 0.400 in normalized best-discovery position, 0.400 in online incumbent
retention, $-0.306$ score units in maximum drawdown and 0.173 in terminal-to-best ratio.
The pair was selected from an already released, deliberately limited two-world study and
is retained only as a worked instrument-readout example. It does not estimate a provider,
information or population effect. Its role is to show that endpoint proximity does not
imply process equivalence.

The complete-agent demonstration used the first frozen unseen reaction--distillation
world. One uninterrupted session submitted 15 actions without restart, model switch, host
action repair, automatic termination or automatic final assay. All 15 actions committed;
one explicit termination and one final assay closed the lifecycle, with no rollback,
right-censoring or public-state leakage. The environment used 8,158.454 of 10,440 process
seconds, four of four instrument uses and 0.00085 of 0.001 L sample. The provider ledger
recorded one session, one logical turn and 17 instrument-interface calls. Cumulative input
was 493,092 tokens, of which 440,832 were reused cached context and 52,260 were uncached;
output was 2,973 tokens. These counts are resource accounting for one demonstration, not
an efficiency comparison. The 15-step trajectory replayed exactly with zero numerical
error. Earlier failed executions remain in the record and were not replaced or reclassified
as successes.

```{=latex}
\begin{figure*}[!tbp]
\centering
\includegraphics[width=\textwidth]{figures/first-paper-world-instrument-v1/publication/figure-6-instrument-records.pdf}
\caption{\textbf{Instrument records distinguish endpoint, process and execution status.}
\textbf{A,} The fixed unseen reaction--distillation world exposes a public contract and a 12-action deterministic reference path.
\textbf{B,} The separate complete-agent unit closed one lifecycle with 15/15 committed actions, one termination and one final assay; it is not replaced by the deterministic reference path.
\textbf{C,} Environment process time and provider-session resources are different ledgers with independent limits.
\textbf{D,} An archived matched pair has a near-zero terminal contrast but marked differences in discovery, retention, drawdown and terminal retention. The example is descriptive and supports no model ranking.}
\label{fig:records}
\end{figure*}
```

# 7. Discussion

## 7.1 What is established

The evidence establishes that ChemWorld has a real construction surface rather than only
a task catalogue. Declared components compile through explicit compatibility rules;
coverage-guided rows extend beyond the reference identities; and reference, generated and
unseen compositions preserve the tested physical, transactional, resource, observation
and replay semantics. Controlled forks separately show that one named private component
can change under an invariant public contract.

The strongest evidence is deterministic and full-census. Every registered unit is shown
with its exact denominator, and every failure would remain visible. The qualification does
not rely on a favourable sample or on significance testing applied to repeated actions.
This is appropriate for a software-defined instrument whose first requirement is coherent
semantics.

## 7.2 What is not established

The tested component vocabulary is finite, and compatibility is only claimed inside its
declared domains. Passing 52 generated compositions does not prove an infinite or arbitrary
world language. The physical models are synthetic or conceptual abstractions and have not
been calibrated as predictive replicas of laboratory equipment or materials. Exact replay
reproduces simulator state and public records, not physical matter or stochastic provider
decisions.

The current evidence also does not establish general agent competence. The deterministic
cases qualify the apparatus. The archived trajectory pair only demonstrates that process
coordinates can add information beyond an endpoint. The complete-agent unseen-world unit
shows that one system could use the same public contract and close one frozen lifecycle;
it is not a benchmark, reliability estimate or comparison group. Model ranking,
behavioural mechanisms, rule learning, cross-model attribution and broad agent statistics
are explicitly outside this paper.

## 7.3 Why composition and process records matter

A fixed benchmark can reveal whether an algorithm performs well on its entries, but it
cannot by itself show that the environment is reusable. Composition qualification shifts
the unit of validation toward components and interfaces. Process records add a second
shift: they preserve evidence acquisition, resource use, failure and terminal commitment
instead of collapsing the interaction into one score. Together these properties make the
environment useful as a programmable virtual instrument, even when no claim is made about
the intelligence or rationality of its user.

# 8. Methods

## 8.1 Construction and compatibility

A composition declaration specifies component roles and parameters plus the public task
surface. Normalization is deterministic. Compatibility checks cover dependencies, state
ownership, unit agreement, parameter domains, resource feasibility, operation exposure,
instrument availability and the existence of a closed lifecycle. A rejected declaration
returns structured diagnostics and does not construct an environment.

The task contract is the authoritative public boundary. Runtime validation is restricted
to the declared operations and instruments. Private constitutive laws, material identities
and hidden simulator state remain evaluator-owned. The 15 registered tasks are mapped into
the same component and contract representation used by generated compositions.

## 8.2 Coverage design

The qualification design was frozen before data generation. Eight patterns were assigned
fixed seeds. Discrete axes use pairwise covering rows. Continuous axes use seeded Latin
hypercube samples inside the authored bounds. Each pattern contains one or two ordered
workflows chosen before execution. The frozen denominator is 52 generated cases, including
eight reaction--distillation cases absent from the registered task identities.

The coverage selection and pass rules cannot be changed in response to results. A platform
defect may be corrected, but the affected qualification block must then restart from its
first case. This rule was applied after process-time and resource-rejection defects were
identified: the full composition block and all affected deterministic cases were rerun.

## 8.3 Qualification measurements

For each case, the report records normalized construction input, compile diagnostics,
public contract, action sequence, schema and transaction status, constitution checks,
events, resource preflight and outcome, public observation, termination, trajectory size
and exact replay. Missing receipts, non-finite quantities, unexpected commits or
rollbacks, leakage, denominator drift and replay mismatch fail the case.

Reference qualification covers 64 task--world units and 1,786 complete recipes. Generated
qualification covers 52 compositions. Negative qualification covers 192 invalid probes.
Module and interface qualification use 32 and seven units, respectively. Compile mutation
uses seven invalid declarations. Counts are exact qualification denominators.

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

The eight cases, seeds and action lists were frozen before execution. Their total expected
census was 89 submitted actions, 88 commits, one rollback and eight final assays. The
failure--recovery case specified the failing action and rollback class in advance. All
submitted actions were inspected; no sampling was used. The provider-call denominator was
zero.

## 8.6 Controlled forks

Each fork declares a parent, a child, one private intervention target, an invariant public
contract and expected divergence channels. Parent and child execute the same typed action
sequence. Gates require lineage validity, exactly one changed private target, invariant
public contract, executable sequence on both variants, expected physical and observation
divergence, exact replay and zero provider calls.

## 8.7 Complete-agent unseen-world protocol

The formal unit is one complete lifecycle on the first frozen unseen
reaction--distillation composition. One uninterrupted agent session may submit at most 16
actions through the public instrument interface. There is no run-level restart, model
switch, host fallback, automatic repair, automatic termination or automatic final assay.
The action count, tool calls and trajectory records must agree exactly; every action must
commit; the lifecycle must contain a termination and exactly one final assay; resources,
public boundary and exact replay must pass.

Provider accounting distinguishes one provider session, one logical agent turn, individual
instrument tool calls and any backend response count exposed by the provider. Cumulative
input is separated into cached and uncached input; cached context is reused input, not
repeated output. The formal limits are 640,000 cumulative input tokens, 192,000 uncached
input tokens and 64,000 output tokens. Per-action wait is capped at 600 s, finalization at
300 s and runner reserve at 600 s, giving a conservative method wall limit of 10,500 s.
These method resources are separate from the simulated process-time ledger.

## 8.8 Process readouts

The process profile retains 19 dimensions in five groups: terminal commitment, evidence
acquisition, evidence-conditioned action, resource deployment and outcome trajectory.
Undefined conditional quantities remain null rather than being set to zero. The selected
worked pair uses normalized best-discovery position, online incumbent retention at a 0.90
retention threshold, maximum absolute incumbent drawdown and terminal-to-best ratio. It is
a descriptive illustration selected from an archived matched design, not a new experiment
or an inferential comparison.

## 8.9 Public boundary and exact replay

The evaluator owns hidden simulator identity and private state. Agent-facing task cards,
observations and histories are checked for hidden fields and absolute private paths. Replay
uses committed typed actions, state and random-number receipts, public observations and
resource events. Provider response bodies, private reasoning, authentication data and raw
local payloads are excluded from the release.

# 9. Data and code availability

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

# 10. Conclusion

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
prediction or agent superiority. The single complete-agent unseen-world lifecycle shows
instrument usability under its frozen contract but does not support a general competence
or comparative claim. What is established is the substrate on which such studies can be
conducted: an endpoint is a result, while the experimental process is a replayable record.

# Appendix A. Reader-facing capability map

| Component pattern | Principal state or process | Representative public operations | Representative instruments |
| --- | --- | --- | --- |
| Phase + observation | bounded phase/equilibrium state | add solvent, add reagent, measure, terminate | pH, UV--visible, final assay |
| Reaction + thermal | batch reaction and temperature history | add, heat, quench, sample | HPLC, GC, final assay |
| Phase + separation | phase formation and transfer | mix, settle, separate, wash, transfer | HPLC, final assay |
| Reaction + crystallization | reaction followed by solid formation | heat, seed, cool, filter | HPLC, particle sizing, final assay |
| Reaction + distillation | reaction, evaporation and fractionation | heat, quench, evaporate, distil, collect | HPLC, GC, final assay |
| Reaction + continuous flow | flow, residence time and conversion | set flow, set temperature, run, sample | HPLC, GC, final assay |
| Reaction + electrochemistry | potential/current-driven conversion | set potential/current, electrolyse, sample | voltammetry, HPLC, final assay |
| Reaction + phase + separation | multistage reaction and purification | react, quench, separate, wash, concentrate, transfer | HPLC, GC, final assay |

# Appendix B. Qualification census

| Qualification unit | Passed | Denominator | Failure classes |
| --- | ---: | ---: | --- |
| Reference task--world units | 64 | 64 | 0 |
| Complete reference recipes | 1,786 | 1,786 | 0 |
| Coverage-generated compositions | 52 | 52 | 0 |
| Frozen unseen reaction--distillation compositions | 8 | 8 | 0 |
| Invalid action probes | 192 | 192 | 0 unexpected outcomes |
| Module probes | 32 | 32 | 0 |
| Cross-module interface paths | 7 | 7 | 0 |
| Invalid compile mutants | 7 | 7 | 0 unexpected constructions |
| Deterministic use cases | 8 | 8 | 0 |
| Deterministic submitted actions | 89 | 89 | 0 missing receipts |
| Controlled fork pairs | 6 | 6 | 0 |
| Controlled fork traces | 24 | 24 | 0 |

# Appendix C. Instrument-use case library

| Scientific use | Components | What the record demonstrates |
| --- | --- | --- |
| Reaction to crystallization | reaction, thermal, crystallization, observation | propagation from reaction through seeding, cooling, filtration and final assay |
| Resource-limited characterization | phase, observation | measurement choice, sample consumption and explicit stopping under a small budget |
| Failure and recovery | reaction, thermal, phase, separation, observation | atomic rollback, attempt consequences and continuation from committed state |
| Controlled private-law fork | one registered component changed privately | invariant public contract with preregistered state/observation divergence |
| Generated reaction to distillation | reaction, thermal, distillation, observation | construction and replay outside the reference task identities; one complete-agent lifecycle closed under the same public contract |
| Reference library | flow, electrochemistry, distillation, partition, crystallization | breadth of reusable task recipes without a cross-task performance score |

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
