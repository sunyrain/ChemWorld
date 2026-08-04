# Work I related-work reconstruction v0.1

> **SUPERSEDED 2026-08-04.** Historical drafting handoff; use
> [`../FIRST_PAPER_TODOLIST.md`](../FIRST_PAPER_TODOLIST.md) for current work.

Historical status: **INTEGRATION READY FOR THE RETIRED WORK I DRAFT**
Task: `W1-S08`  
Owner: `codex-1`  
Evidence cutoff: `2026-08-02`  
Target integrator: `W1-S10`

This isolated handoff is grounded in
`workstreams/arxiv_v1/reports/related-work-evidence-v0.1.json` and the corresponding
primary-source audit. It does not edit the manuscript or bibliography.

## Related work — replacement text

### Physical autonomous laboratories and chemistry agents

Chemistry agents and self-driving laboratories establish that machine-guided workflows
can act on real materials. Coscientist connects language-model planning, documentation,
code, liquid handling, and cloud-laboratory execution, while ChemCrow combines a
language model with a broad chemistry-tool suite and robotic synthesis
[@boiko2023autonomous; @bran2024augmenting]. A-Lab and autonomous mobile-robot systems
demonstrate closed-loop synthesis and characterization in physical laboratories
[@szymanski2023alab; @dai2024mobile]. ORGANA and ChemAgents extend this line toward
visual feedback, long workflows, multi-agent orchestration, and execution across
chemistry tasks or laboratory settings [@darvish2025organa; @song2025chemagents].
Peer-reviewed 2026 systems emphasize hardware-ready protocol generation,
literature-to-robot translation, digital-twin checking, affordable modular automation, and teachable or
adaptive instrument operation [@panapitiya2026autolabs; @pagel2026acra;
@hsu2026prism; @pilon2026robochemflex; @vriza2026instruments; @chen2026xray].

These systems provide physical validity, perception, motion, safety, hardware
integration, and deployment evidence that ChemWorld does not. Their laboratory scale
and replication limits follow from the reality of the experiments rather than from a
defect in their design. ChemWorld addresses a complementary measurement problem: it
uses virtual chemical worlds to repeat a matched simulator-world identity, intervene on
information or a preregistered private world component, and retain every operation,
failure, resource event, and terminal decision for exact environment replay. It should
therefore be read as a controlled behavioral apparatus that can inform later physical
studies, not as a replacement for a self-driving laboratory or as evidence of
virtual-to-real transfer.

### Optimization suites and executable scientific worlds

Reaction-optimization and experiment-planning suites such as Summit and Olympus offer
controlled, scalable comparisons over objective functions, and the PC-Gym preprint
provides nonlinear process-control environments with disturbances and constraints
[@felton2021summit; @hase2021olympus; @bloor2024pcgym]. ChemGymRL already establishes a
fine-grained, operable virtual chemistry laboratory for reinforcement learning
[@beeler2024chemgymrl]. Peer-reviewed closed-loop materials frameworks further couple
candidate generation, budgeted oracle feedback, constraints, memory, and multi-objective search
[@malik2026made; @abhyankar2026llema]. These systems answer important optimization,
control, and discovery questions; ChemWorld does not claim that a chemistry simulator,
a closed loop, a resource budget, or interactive chemical operations are new by
themselves.

Interactive discovery environments broaden evaluation from optimization to active
hypothesis formation, experiment selection, explanation, and law recovery.
DiscoveryWorld evaluates long-horizon scientific discovery in a virtual environment;
the BoxingGym and SciGym preprints study active experimental design and model inference;
and peer-reviewed SciExplorer and NewtonBench evaluate exploration or generalization
across initially unknown or counterfactual physical systems [@jansen2024discoveryworld;
@gandhi2025boxinggym; @duan2025scigym; @nagele2026sciexplorer;
@zheng2026newtonbench]. ChemWorld is narrower in law diversity and discovery scope. Its
distinctive experimental unit is a chemistry-native lifecycle in which typed operations
change sample state, measurements consume resources, invalid actions preserve explicit
failure consequences, and the agent itself chooses assay or discard. The first paper
uses controlled forks to qualify the apparatus; it does not demonstrate general rule
learning or adaptation under changed laws, which remains Work II.

### Measuring agents as experimental subjects

Recent research also treats the agent and its environment as objects of measurement.
A 2026 process-level preprint shows that successful scientific outputs need not coincide
with scientifically grounded reasoning, and a peer-reviewed behavioral-science review
calls for systematic observations and interventions on situated agents
[@riosgarcia2026scientifically; @chen2026agentbehavior]. An environment-engineering
preprint shows that permissions, artifacts, budgets, and interaction structure can materially
shape agent performance [@xin2026eurekagent]. A 2026 robotic-chemistry stress-test
preprint directly measures physical workflow executability and feedback-driven
replanning over many workstations [@guo2026stresstesting]. These studies preclude a
priority claim for measuring scientific agency, studying process rather than outcome,
or engineering an agent environment.

ChemWorld contributes a domain-specific intersection rather than a general behavioral
science. The complete agent system is treated as the experimental subject; a stateful
chemical runtime supplies controlled interventions and observable consequences. The
registered readouts separate evidence acquisition, continued investment, terminal
commitment, resource deployment, outcome, and trajectory dynamics. Known deterministic
policies serve as a positive control before complete-system profiles are interpreted,
and fresh sessions distinguish exactly replayable environment history from a new model
decision trajectory. This supports bounded, auditable claims about behavior in virtual
chemical worlds. It does not identify mental states, isolate a model-only causal effect,
or establish a universal scalar ranking.

### Position and boundary

The adjacent literatures therefore supply complementary strengths: physical
laboratories establish execution and deployment; optimization and process-control
suites establish scalable algorithmic comparison; interactive worlds test discovery
and law recovery; and process-level evaluations establish that scientific behavior
cannot be inferred from success alone. ChemWorld occupies their controlled overlap. It
uses executable chemistry as a measurement apparatus for asking how evidence, prior
information, resources, state-changing actions, and terminal choices shape an
experimenting system's trajectory. The present evidence covers a bounded virtual
apparatus, two formally exercised task families in compiled controls, complete-system
profiles in one primitive-control task, and two deliberately selected fresh-session
worlds. It includes no visual manipulation, real instrument, wet-laboratory, or
sim-to-real validation.

## Capability comparison matrix

| Literature family | Strongest evidence it supplies | Primary evaluated unit | ChemWorld's complementary unit | Claim not made here |
| --- | --- | --- | --- | --- |
| Chemistry agents and self-driving laboratories | Real synthesis, characterization, perception, robotics, safety, and deployment | Physical workflow or campaign | Matched virtual lifecycle and its evidence/resource/terminal trajectory | Replacement of physical laboratories or physical validity |
| Protocol/tool agents | Tool breadth, protocol correctness, literature translation, and hardware-ready execution | Tool call, procedure, or compiled protocol | Agent-selected state-changing experiment under hidden process state | First chemistry tool agent or first autonomous protocol execution |
| Optimization and process-control suites | Controlled algorithm comparison, objective regret, constraints, and tracking | Candidate query or control step | Resource-coupled experimental lifecycle with measurements and terminal choice | BO superiority or process-control novelty |
| Virtual chemistry and embodied laboratory simulation | Fine-grained chemical actions, perception, manipulation, and simulated hardware | Bench action or embodied task | Identity-controlled intervention on experimental behavior | First virtual chemistry laboratory or embodied-agent realism |
| Interactive discovery and law-recovery worlds | Hypothesis testing, active experimental design, explanations, and mechanism recovery | Query, hypothesis, model, or discovered law | Chemistry-native lifecycle profile under frozen world and information identity | First discovery environment, general rule learning, or Work II adaptation |
| Agent process and behavioral evaluation | Trace-level reasoning, environment effects, workflow executability, and behavioral interventions | Agent trace or situated behavior | Preregistered known-policy control plus complete-system and fresh-session profiles | First process-level evaluation or general AI-agent behavioral science |
| ChemWorld Work I | Controlled single-component forks, known-policy validity, immutable trajectories, resource ledgers, and terminal-policy accounting | Campaign profile, complete-system × matched cell, or selected-world fresh pair | The bounded intersection itself | Universal score, model ranking, real-lab transfer, or unlimited world generation |

## Source-by-source citation handoff

| Citation key | Evidence-record ID | Status in evidence record | Use in replacement text | Boundary carried into prose |
| --- | --- | --- | --- | --- |
| `boiko2023autonomous` | `coscientist` | peer reviewed | tool-to-laboratory execution | real execution is stronger; no replacement claim |
| `bran2024augmenting` | `chemcrow` | peer reviewed | chemistry tool breadth and synthesis | tool breadth is not ChemWorld's novelty |
| `szymanski2023alab` | `alab` | peer reviewed | autonomous physical synthesis | physical validity and replication serve different questions |
| `dai2024mobile` | physical mobile-robot audit entry | peer reviewed | exploratory physical chemistry | motion and hardware autonomy are out of scope |
| `darvish2025organa` | `organa` | peer reviewed | visual feedback and long workflow | ChemWorld has no robotic perception claim |
| `song2025chemagents` | `chemagents` | peer reviewed | multi-agent laboratory orchestration | cross-laboratory execution is not claimed |
| `panapitiya2026autolabs` | `autolabs` | peer reviewed | hardware-ready protocol generation | protocol compilation differs from autonomous experiment choice |
| `pagel2026acra` | `acra` | peer reviewed | literature-to-robot translation | literature reproducibility is not the Work I estimand |
| `hsu2026prism` | `prism` | peer reviewed | digital-twin protocol validation | ChemWorld is not a robotics digital twin |
| `pilon2026robochemflex` | `robochem_flex` | peer reviewed | affordable physical closed loop | no physical-reaction optimization claim |
| `vriza2026instruments` | `teachable_instrument_agents` | peer reviewed | teachable real-instrument agents | no real-instrument evidence in Work I |
| `chen2026xray` | `agentic_xray_scientist` | peer reviewed | stepwise virtual-to-real instrument operation | stepwise instrument control is not claimed as novel |
| `felton2021summit` | Summit audit entry | peer reviewed | reaction-optimization benchmark | no optimizer horse race |
| `hase2021olympus` | Olympus audit entry | peer reviewed | experiment-planning benchmark | candidate-query benchmarks answer a different question |
| `bloor2024pcgym` | `pcgym` | preprint | chemical process-control environments | no control-benchmark novelty |
| `beeler2024chemgymrl` | `chemgymrl` | peer reviewed | interactive virtual chemistry | rejects first-virtual-lab wording |
| `malik2026made` | `made` | peer reviewed | budgeted closed-loop materials discovery | no first-closed-loop-materials claim |
| `abhyankar2026llema` | `llema` | peer reviewed | multi-objective materials discovery | candidate-oracle search differs from sample lifecycle |
| `jansen2024discoveryworld` | `discoveryworld` | peer reviewed | long-horizon virtual discovery | rejects first-discovery-environment wording |
| `gandhi2025boxinggym` | `boxinggym` | preprint | experimental design and model discovery | query-based design differs from physical-state actions |
| `duan2025scigym` | `scigym` | preprint | iterative systems-biology experimentation | ChemWorld is smaller in dynamic-system scale |
| `nagele2026sciexplorer` | `sciexplorer` | peer reviewed | active law discovery | Work I does not claim general law recovery |
| `zheng2026newtonbench` | `newtonbench` | peer reviewed | counterfactual-law generalization | fork qualification is not agent adaptation |
| `riosgarcia2026scientifically` | `corral` | preprint | process-level scientific-agent evaluation | rejects process-evaluation priority |
| `chen2026agentbehavior` | `ai_agent_behavioral_science` | peer-reviewed review | situated-agent behavioral framing | domain apparatus, not general framing, is the increment |
| `xin2026eurekagent` | `eurekagent` | preprint | environment engineering | permissions/budgets are not claimed as new |
| `guo2026stresstesting` | `robotic_chemistry_stress_test` | preprint | physical workflow executability and replanning | physical agency measurement already exists |

## Prohibited claims and integration checks

W1-S10 must not introduce any of the following when copy-editing this section:

- first interactive scientific-discovery environment or first virtual chemistry lab;
- first closed-loop materials-discovery, law-recovery, process-level, or behavioral-
  science evaluation of agents;
- superiority over physical laboratories, chemistry tools, optimizers, process
  controllers, embodied simulators, or discovery benchmarks;
- replacement of self-driving laboratories or evidence of virtual-to-real transfer;
- arbitrary or unlimited world generation, arbitrary component recombination, or
  general third-party world DSL support;
- agent rule learning, mechanism adaptation under changed laws, or another Work II
  result;
- general model or backend superiority, a causal model-only effect, inferred mental
  states, or a universal scalar intelligence score;
- language that treats the platform's 15 registered tasks as 15 formal agent-result
  tasks or describes synthetic instrument packets as empirical spectra.

The final section should retain the 2026 preprint labels where applicable and should be
rechecked only if the release date moves beyond the evidence cutoff or a new directly
overlapping work is deliberately added.
