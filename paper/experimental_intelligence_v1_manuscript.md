# Experimental Intelligence in Executable Chemical Worlds

Status: working manuscript v0.2, 2026-08-01. Not submission-ready.

Evidence and experiment authority:
`workstreams/arxiv_v1/EXPERIMENTAL_INTELLIGENCE_V1_MASTER_PLAN_ZH.md` and
`workstreams/arxiv_v1/reports/experimental-intelligence-experiment-ledger-v0.1.json`.

## Abstract

Artificial-intelligence systems for science are commonly evaluated by endpoint
predictions, optimized conditions, or a small number of experiments in a fixed
physical setting. These evaluations cannot reliably distinguish a lucky
discovery from stable experimental learning, nor separate the effects of prior
information, physical context, evidence use, and stochastic agent behavior.
Here we introduce ChemWorld, an executable chemical-world environment for
studying experimental intelligence under controlled conditions. Agents act on
stateful chemical processes through typed operations, actively select
measurements, incur material and instrument costs, encounter explicit failures,
and must autonomously terminate and assay experiments. Every transition is
transactional, resource-accounted, identity-bound, and exactly replayable.

Across 29,580 compiled-experiment physical trials, the same language-model
scaffold showed task-dependent optimization, while correct and deliberately
misindexed material information altered experimental choices without producing
uniform performance recovery. Optimization, held-out prediction, declared
directional knowledge, and unsupported mechanistic claims provided different
capability profiles. In a separate agent-directed study, native Codex completed
60 of 60 electrochemical experiments through 815 self-selected primitive
operations. Endpoint performance concealed distinct trajectories of discovery,
loss, retention, and recovery: material information was associated with later
discovery but stronger retention and smaller drawdown on average, with a
reversal in one physical world.

[PENDING G2 v0.5: report the within-world five-trajectory replication for each
of two deliberately selected physical worlds. Do not pool the worlds into a
general-population prior-effect estimate.]

ChemWorld therefore treats a scientific agent not only as a task participant
but as an experimentally measurable system. The results show why scientific
competence cannot be reduced to an endpoint score and establish controlled
chemical worlds as a complementary instrument for studying how agents
experiment.

## 1. Introduction

Scientific agents are increasingly asked to propose experiments, interpret
measurements, and operate automated laboratories. Their evaluation, however,
usually compresses experimental work into a prediction or a vector-valued
query. Even when an agent produces a high-scoring condition, the observed
endpoint does not reveal whether the condition was discovered by chance,
whether the agent used intermediate evidence, whether it retained the resulting
strategy, or whether it could recover after abandoning it.

Real laboratories provide indispensable evidence about physical execution and
deployment. They are less suited to repeatedly cloning a hidden physical
system, changing only the information supplied to the agent, matching the
observation stream, and sampling many independent decision trajectories. Static
optimization benchmarks provide scale and clean objective functions but remove
the stateful experimental process whose scientific use is at issue. These two
settings therefore leave a methodological gap: a controlled apparatus for
studying the behavior of the experimenting agent.

ChemWorld fills this gap with executable, task-bounded chemical and chemical-
engineering worlds. An experiment is a state-changing sequence of operations
and measurements. The agent controls additions, process conditions,
measurements, termination, and final assay under a campaign-wide resource
endowment. Invalid operations and failures are retained rather than repaired
into valid actions. Hidden evaluator state is separated from the public agent
view, while world, source, observation, resource, and trajectory identities are
cryptographically bound for audit and replay.

We use ChemWorld to study experimental intelligence: the structured response of
an agent to interventions, observations, and experimental consequences. Our
experiments intervene on prior material information, physical world identity,
and experimental control authority. We measure lifecycle autonomy, discovery,
retention, drawdown, recovery, predictive calibration, and resource use rather
than collapsing them into a single leaderboard score.

The study makes five contributions. First, it provides an executable chemical-
world substrate spanning stateful operations, instruments, failures, resources,
and replay. Second, it introduces an agent-directed primitive-control interface
in which measurement and lifecycle decisions remain with the agent. Third, it
formalizes trajectory-level measures of experimental behavior. Fourth, it shows
that task performance, prior response, prediction, and recovery need not agree.
Fifth, it uses fresh trajectories within fixed physical worlds to test whether
observed experimental phenotypes are repeatable or dominated by one-off model
sampling.

## 2. Relation to existing systems

Chemistry agents and self-driving laboratories have established that language-
model systems can retrieve chemical knowledge, call specialist tools, compile
protocols, and act through cloud or robotic laboratories. Coscientist connected
planning, documentation search, code, and experimental automation, while
ChemCrow combined a language model with eighteen chemistry tools and physical
synthesis. A-Lab and mobile robotic laboratories provide stronger evidence than
ChemWorld for real chemical execution and deployment. These systems answer
whether an agent can be connected to, and produce useful outcomes in, the real
laboratory. They do not generally provide the cloned physical identities,
paired information interventions, or fresh-trajectory replication needed to
estimate whether the resulting experimental behavior is stable
([Boiko et al., 2023](https://doi.org/10.1038/s41586-023-06792-0);
[Bran et al., 2024](https://doi.org/10.1038/s42256-024-00832-8);
[Szymanski et al., 2023](https://doi.org/10.1038/s41586-023-06734-w);
[Kotopanov et al., 2024](https://doi.org/10.1038/s41586-024-08173-7)).

Virtual environments address complementary constraints. Summit and Olympus
already support reproducible in-silico reaction optimization, PC-Gym supports
nonlinear chemical-process control, and ChemGymRL provides interconnected
virtual chemistry benches with fine-grained agent actions. We therefore do not
claim the first virtual chemistry laboratory or use optimizer ranking as the
primary novelty. ChemWorld instead combines chemical primitive control with
controlled interventions on the experimenting agent, campaign-wide physical
resource accounting, immutable failure evidence, and state-level replay
([Beeler et al., 2024](https://doi.org/10.1039/D3DD00183K);
[Bloor et al., 2024](https://arxiv.org/abs/2410.22093)).

Interactive discovery benchmarks already test hypothesis formation,
experimentation, and explanation. DiscoveryWorld supplies long-horizon
fictional scientific tasks; BoxingGym evaluates experimental design and model
discovery in generative probabilistic environments; and SciGym supplies a dry
laboratory of hundreds of systems-biology models. More recent benchmarks go
further in explicit law recovery. NewtonBench contains 324 counterfactual
physics-law tasks, DiscoverPhysics evaluates prediction and explanation in 22
non-canonical physical worlds, and ActiveSciBench-Chem contains 57 enzyme-
kinetics mechanism tasks. These systems currently exceed ChemWorld in the
scale and formal evaluation of law recovery. ChemWorld addresses a different
unit of interaction: the agent must construct and advance a stateful chemical
experiment, decide when to characterize it, and bear inventory and vessel
opportunity costs rather than only select the next query or initial condition
([Jansen et al., 2024](https://proceedings.neurips.cc/paper_files/paper/2024/hash/13836f251823945316ae067350a5c366-Abstract-Datasets_and_Benchmarks_Track.html);
[Gandhi et al., 2025](https://arxiv.org/abs/2501.01540);
[Duan et al., 2025](https://arxiv.org/abs/2507.02083);
[Zheng et al., 2025](https://arxiv.org/abs/2510.07172);
[Wiemann et al., 2026](https://arxiv.org/abs/2605.26087);
[Kabra et al., 2026](https://arxiv.org/abs/2605.24043)).

Prediction--understanding dissociation and process-level evaluation are also
not unique claims. CausaLab separates task success from recovered causal
structure, and ReplaySCM evaluates executable mechanism replay. Most directly,
Corral reports across more than 25,000 runs that successful outcomes can conceal
evidence neglect and failures of belief revision. A July 2026 robotic-chemistry
stress test likewise makes physical executability and evidence-driven
replanning measurable. ChemWorld complements these studies by grounding
process evidence in chemical actions, measurements, resources, and subsequent
physical consequences, while permitting paired interventions on prior
information and repeat trajectories in the same physical world
([Yang et al., 2026](https://arxiv.org/abs/2605.26029);
[Batzoglou, 2026](https://arxiv.org/abs/2605.08197);
[Ríos-García et al., 2026](https://arxiv.org/abs/2604.18805);
[Guo et al., 2026](https://arxiv.org/abs/2607.23045)).

Finally, LabUtopia and MATTERIX provide substantially richer perception,
manipulation, laboratory geometry, and sim-to-real capabilities, while
LabOSBench and LabRobFail isolate instrument-control and robotic-failure
competencies. ChemWorld intentionally abstracts those problems. Its niche is
not a more realistic robot simulator, but a controlled experimental science of
experimenting agents grounded in executable chemistry
([Li et al., 2025](https://arxiv.org/abs/2505.22634);
[Darvish et al., 2026](https://doi.org/10.1038/s43588-025-00924-4);
[Zou et al., 2026](https://arxiv.org/abs/2606.16802);
[Wang et al., 2026](https://arxiv.org/abs/2607.23704)).

## 3. ChemWorld as an apparatus for studying agents

### 3.1 Stateful chemical worlds

ChemWorld separates a physical causal substrate, an experimental interaction
runtime, and a versioned task/evaluation contract. The substrate contains typed
material, phase, vessel, equipment, thermal, and process states. Operations
route through task-allowed domain services and update these states atomically.
The task contract determines the public objective, allowed operations and
instruments, observation mask, budget, scoring law, and termination semantics.

The present release registers 15 tasks, 28 operation types, five instrument
types, and 37 public scalar observation keys. All registered complete-
experiment adapters pass 415 midpoint, coordinate-boundary, and categorical
execution cases. Sixty-two declared success metrics bind to explicit evaluator
endpoints. These are environment-design qualifications; formal agent results in
this manuscript are limited to electrochemical conversion and reaction-to-
crystallization, with autonomous primitive-control results currently limited to
electrochemical conversion.

### 3.2 Agent-directed experimentation

In agent-directed control, each decision selects exactly one typed operation.
The environment validates the operation, preflights the resource ledger,
commits or rejects the state transition, and returns only public outcomes. The
agent may then select a new operation or request an allowed measurement. An
experiment is not complete when the process is merely terminated: the agent
must also request a final assay. A valid final assay closes the vessel and, in
campaign mode, makes a fresh vessel available in the same hidden world.

The official runner performs no automatic action repair, termination, or final
assay. Invalid and resource-rejected proposals consume their declared operation
attempt and remain in the trajectory. Material, solvent, vessel, instrument,
operation, model-call, token, and wall-time resources are recorded on separate
axes rather than combined into a hidden scalar budget.

### 3.3 Controlled identities and replay

Each run binds the task and scoring contracts, physical world and material
instance, observation-noise namespace, resource card, method envelope, model
configuration, source tree, and agent-local seed. Primitive transitions can be
replayed from the durable trajectory, and resource receipts can be reconstructed
from the same operations. Provider-session receipts remain separate from
physical-transition replay.

This design makes it possible to hold a chemical world fixed while changing the
information given to the agent, and to distinguish physical-world identity from
a fresh model trajectory. Native Codex does not expose a reproducible provider
sampling seed; a fresh trajectory is therefore an independent session-level
realization, not a deterministically replayed model random-number stream.

## 4. Compiled experiments reveal task- and prior-dependent behavior

Compiled-experiment control is used here as a low-agency calibration, not as the
ontological starting point of ChemWorld. On each exploration turn the agent
selects a complete experiment and a compiler executes the task-defined
procedure. This interface supports direct calibration against Latin hypercube,
Gaussian-process, random-forest, and related typed optimization methods.

The nonduplicated active corpus contains 27,300 classic-baseline physical
experiments and 2,280 participant experiments across opaque, nominal, and
misindexed material-information conditions. The opaque participant slice is
shared between the original two-task study and the three-arm study and is
counted only once.

### 4.1 Optimization performance depends on the chemical task

In electrochemical conversion, the participant mean was 0.7150, compared with
0.6159 for the strongest information-matched structured RF-EI baseline. The
paired descriptive difference was +0.0991 with a world-bootstrap 95% interval
of +0.0103 to +0.1748. The strongest privileged-descriptor calibration scored
0.6441, and its comparison interval crossed zero.

In reaction-to-crystallization, the participant mean was 0.5355 and the best
classic method, LHS, scored 0.5708. The paired difference was -0.0353 with a
95% interval of -0.0650 to -0.0085. These comparisons were not preregistered as
superiority tests and do not support a general language-model-versus-classic-
optimization ranking. They instead establish task-dependent behavior under a
shared participant scaffold.

### 4.2 Correct material information has task-dependent value

Anonymous nominal material properties increased the electrochemical mean from
0.7150 to 0.7874, a paired difference of +0.0724 with a familywise 97.5%
interval of +0.0074 to +0.1546. The crystallization mean increased from 0.5355
to 0.5615, but its interval of -0.0130 to +0.0630 included zero. Correct
material information therefore had clear value in the sampled electrochemical
worlds but uncertain value in crystallization.

### 4.3 Prior manipulation, action correction, and recovery are distinct

Deliberately misindexed material properties increased the first misleading-
action rate from zero to 0.7 in electrochemistry and to 1.0 in crystallization.
Electrochemical misleading-action share declined later in the campaign, but
performance did not recover to the opaque condition. Crystallization recovered
in endpoint performance but did not satisfy the differential action-correction
criterion. Neither task passed the preregistered joint recovery rule.

The result does not show that agents generally recover from incorrect priors.
It shows that prior manipulation, later behavioral change, and performance
recovery are empirically separable events.

## 5. Optimization and cognition provide different capability profiles

The electrochemical participant combined a final recommendation score of
0.7150 with held-out directional accuracy of 0.744 and a Brier score of 0.186.
Crystallization scored 0.5355 with held-out accuracy of 0.478 and Brier score of
0.298, despite higher declared directional accuracy. Structural-edge and
mechanism-tag F1 scores were low in both tasks, and unsupported-claim rates were
0.611 and 0.714. All final recommendations reproduced tested conditions and
produced no gain over the validated incumbent in any of the twenty task-world
cells.

These measurements do not establish a general psychology of language models.
They demonstrate why endpoint optimization, outcome-held-out prediction,
declared confidence, structural explanation, and method synthesis must remain
separate endpoints when evaluating scientific agents.

## 6. Autonomous experimentation exposes discovery, loss, and recovery

### 6.1 Native Codex closes complete experimental lifecycles

The autonomous development matrix placed native Codex (`gpt-5.6-sol`, medium
reasoning) in five paired electrochemical worlds under opaque or anonymous
nominal material information. Each cell received a campaign-wide endowment of
six vessels, six final assays, eighteen nonfinal instrument uses, 0.48 mol of
reagent, 0.96 L of solvent, and a nonbinding 144-attempt safety ceiling.

All ten cells and all sixty vessels completed. The agent submitted 815 primitive
operations, including 164 nonfinal instrument measurements and sixty final
assays (224 measurement operations in total), with no invalid or resource-
rejected operation. All sixty provider sessions completed, and all resource,
replay, and physical-pair audits passed.

### 6.2 Endpoint summaries conceal different learning trajectories

The opaque and nominal arms had mean best scores of 0.6314 and 0.7093, but the
direction and magnitude varied strongly by world. Different time and resource
estimands also disagreed: nominal-minus-opaque was negative for mean batch AUC
and realized-attempt AUC but positive for fixed-144-operation AUC.

Individual campaigns revealed more substantial differences. One opaque agent
found a score of 0.7865 in its first experiment and ended at 0.3824, whereas its
nominal counterpart rose from 0.2492 to a best of 0.8544 and ended at 0.8352.
Another opaque campaign ended at zero after previously scoring 0.6050, while
the matched nominal campaign recovered from several declines and ended at
0.7894. Similar endpoint summaries can therefore obscure early discovery,
catastrophic loss, stable retention, and late recovery.

### 6.3 Material information is associated with trajectory stability, not a
uniform performance gain

The global best appeared at mean normalized progress 0.32 in the opaque arm and
0.80 in the nominal arm. Online incumbent retention was 0.52 and 0.72;
maximum absolute drawdown was 0.3326 and 0.0915; terminal-to-global-best ratio
was 0.67 and 0.94. Three of six opaque loss episodes and four of five nominal
episodes recovered. Diagnostic-aligned control changes were followed by a
positive next-batch score change in 4/14 opaque and 8/17 nominal batches.

These are descriptive development results. In one selected world, retention,
drawdown, and terminal-to-best effects reversed. The apparent average stability
of the nominal arm may therefore reflect physical-world context, a single
provider trajectory, or their interaction.

## 7. Fresh trajectories test within-world repeatability

[PENDING EXPERIMENTAL RESULTS]

We selected two physical worlds only after the development study because their
nominal-minus-opaque trajectory patterns opposed one another. The development
trajectories are excluded from the replication estimand. In each world, five
fresh trajectory replicates pair opaque and nominal information, producing ten
pair blocks and twenty cells. Pair order and arm-first order are frozen and
balanced.

The analysis reports all five paired differences separately within each world,
followed by the median, range, sign count, and sign consistency. The two worlds
are not pooled into a population-level p-value. Completed and right-censored
cells remain in the manifest, and no cell is replaced after an accepted
operation.

This section will choose exactly one preregistered interpretation branch:

1. repeatable within-world but opposing between-world patterns;
2. frequent within-world reversals indicating large trajectory stochasticity;
3. endpoint instability with repeatability in selected lifecycle or trajectory
   metrics.

The branch is selected by the frozen audit output, not by narrative preference.

## 8. Discussion

ChemWorld changes what can be measured about a scientific agent. A high endpoint
can result from early luck followed by abandonment, while slower improvement can
produce a more stable terminal policy. Correct prior information can alter
actions without uniformly improving outcomes. Later action correction need not
imply cognitive correction or performance recovery. These distinctions are
invisible when an experiment is represented only as an input vector and final
score.

The environment is complementary to physical laboratory automation. It does not
test robot manipulation, real instrument integration, or sim-to-real transfer.
Instead, it enables repeated, identity-controlled experiments on agent behavior
that would be difficult or costly to isolate in a single real chemical system.
Physical deployment and controlled behavioral evaluation address different
parts of the scientific-agent problem.

The present work also has important limits. ChemWorld contains a bounded set of
physical and constitutive models rather than arbitrary chemistry. Its spectra
and assays are synthetic state-coupled instruments, not empirical spectral
predictors. Formal compiled-experiment results cover two tasks; autonomous
results cover one task and selected worlds. Native Codex sampling is not seed-
controlled. Diagnostic-to-control temporal alignment is not a causal estimate
of feedback value. No claim is made about general prior benefit, superiority to
classic optimization, or real-laboratory transfer.

The central result is methodological and empirical: scientific agents can be
studied as experimental systems, and their competence is multidimensional.
Executable chemical worlds provide the controlled apparatus required to expose
that structure.

## 9. Methods

### 9.1 Environment and task qualification

[Describe state ledgers, runtime services, operations, instruments, task
contracts, the 415-case design audit, and 62 endpoint bindings.]

### 9.2 Compiled-experiment protocols

[Describe v1.0 and v1.2 freezes, ten independent worlds per task, twenty
exploration experiments, predictive checks, blind validation, classic methods,
paired intervals, multiplicity boundaries, and nonduplicated accounting.]

### 9.3 Agent-directed primitive protocol

[Describe MCP transport, one decision per operation, no repair/closeout,
campaign resource card, six-vessel campaign, persistent file-backed memory,
public affordances, and hidden-information boundary.]

### 9.4 Trajectory endpoints

[Give exact definitions of discovery fraction, 90% online retention, frozen-
incumbent loss/recovery, drawdown, terminal-to-best, three running-best AUCs,
and diagnostic-aligned control change.]

### 9.5 Fresh-trajectory replication

[Describe selected-world status, exclusion of development trajectories,
trajectory replicate semantics, pair schedule, immutable attempts, retries,
right-censoring, and per-world descriptive analysis.]

### 9.6 Provenance, provider accounting, and replay

[Describe source/config/physical identity hashes, provider receipts, resource
ledger reconstruction, exact replay, local raw data, release snapshots, and
the independent-checkout attestation required before submission.]

## 10. Data and code availability

[BLOCKED: `benchmark/releases/chemworld-serious-v1` is empty. Before release,
provide a frozen derived cell table, trajectory and receipt hash index, a small
replayable trajectory subset, a data card, and a durable archive location for
the full local raw corpus.]

## 11. Remaining work before arXiv

1. Execute and audit 20 G2 v0.5 cells, representing 120 planned physical
   experiment opportunities and 120 provider sessions.
2. Close the five current evidence-pipeline registry/freshness errors.
3. Recertify G0 artifacts on one release candidate or publish exact historical
   source snapshots for every arm.
4. Build one frozen derived table and generate all figures from it.
5. Populate the release directory and complete clean-wheel, full-test, replay,
   and independent-checkout attestations.
6. Complete references, statistical-language review, data card, and final
   claim audit.

No new G0 scientific experiment is required for this manuscript. The only
required new scientific matrix contains 120 G2 experiment opportunities.
