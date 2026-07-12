# Give experimental intelligence its own world engine

**Static benchmarks ask what a model knows. ChemWorld asks how it experiments when the answer is hidden.**

ChemWorld is a replayable causal virtual laboratory. Under partial observability, finite budgets, and operational
constraints, agents choose operations and measurements, form hypotheses, and revise strategies from evidence.
Hidden kinetics, phase behavior, and process rules can change while the public task remains stable, so memorizing one
optimal recipe is not enough.

ChemWorld is not a universal real-reaction predictor. It is a research environment for making experimental decision
making scalable, comparable, and falsifiable.

## Why a world engine

Real chemical experiments are slow, costly, and risk-bearing. Static datasets test knowledge and prediction, but not
whether an agent selects an informative experiment, interprets failure, manages resources, or adapts when its model is
wrong.

| Static chemistry benchmark | ChemWorld |
| --- | --- |
| Answer a given question | Decide what experiment to do next |
| One-shot input and output | Repeated observation and action |
| Fixed data and rules | Intervenable hidden world rules |
| Error lowers a score | Error consumes budget and changes state |

## The central experiment

The same public task can run under different rate laws, reaction topologies, constitutive relations, or equipment
boundaries. Agents are not given a world label. They must use experiments to detect which assumptions still hold and
recover when the rules change.

## Three agent tracks

- **Campaign Design:** choose the next complete experiment—BO, safe BO, active learning, recipe-level LLMs.
- **Procedure Execution:** choose the next operation—hierarchical RL, state machines, operation-level LLMs.
- **Process Control:** continuously adjust equipment settings—SAC, MPC, system identification, world-model control.

World-model adaptation cuts across all three: infer the current world from history and recover quickly after a shift.

## Start here

| Goal | Page |
| --- | --- |
| Understand the research thesis | [Why ChemWorld](vision.md) |
| Define experimental intelligence | [Experimental Intelligence](experimental_intelligence.md) |
| Understand changing worlds | [Causal Worlds](causal_worlds.md) |
| Read the evaluation design | [Benchmark](benchmark_overview.md) |
| Inspect current evidence | [Research Findings](research_findings.md) |
| Understand the real-world path | [Real-world Bridge](real_world_bridge.md) |

For APIs and local setup, use the [Chinese technical documentation](../getting_started.md).

> Research status: benchmark candidate. Engine and replay controls are operational; formal cross-method adaptation,
> private evaluation, and external bridging remain incomplete.
