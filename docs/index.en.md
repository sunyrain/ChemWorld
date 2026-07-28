<section class="cw-home-hero" markdown>

<span class="cw-eyebrow">A causal world engine for experimental intelligence</span>

# Give experimental intelligence its own world engine

**Static benchmarks ask what a model knows. ChemWorld asks how it experiments when the answer is hidden.**

ChemWorld is a replayable causal world-model environment. Under partial observability, finite budgets, and operational
constraints, agents choose operations and measurements, form hypotheses, and revise strategies from evidence.
Hidden kinetics, phase behavior, and process rules can change while the public task remains stable, so memorizing one
optimal recipe is not enough.

ChemWorld is not a universal real-reaction predictor. It is a research environment for making experimental decision
making scalable, comparable, and falsifiable.

<div class="cw-button-row" markdown>

[Read the research thesis](vision.md){ .md-button .md-button--primary }
[Understand causal worlds](causal_worlds.md){ .md-button }
[Inspect the evidence](research_findings.md){ .md-button }

</div>

<div class="cw-pill-row">
  <span class="cw-pill">Replay-verified trajectories</span>
  <span class="cw-pill">Causal world shifts</span>
  <span class="cw-pill">BO · RL · LLM · World Models</span>
</div>

</section>

## Current evidence

The legacy 2026-07-27 two-task static-S0 participant bundle is withdrawn and
no longer supports current rankings or manuscript numbers. The replacement
electrochemical protocol binds an explicit material family and balanced score.
The replacement reaction-to-crystallization protocol binds an independent
catalyst/solvent family and has passed a five-world by 16-material-pair
qualification. Both remain development evidence with `formal_result=false`.

Fixed-world S0 remains the current research priority, but new formal claims
require frozen classic baselines and multi-world Codex subscription runs.
Hidden world changes and mechanism replacement remain deferred until a
realistic drift model and separate research question are established.

Separately, all 15 complete-experiment adapters pass executable midpoint
smokes with zero dead coordinates and zero unresolved formalization blockers.
Only the two confirmatory tasks are in scope for the replacement formal model
evaluation.

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
- **Process Control:** choose bounded equipment setpoints and process-control actions—SAC, MPC, system
  identification, world-model control. This is not a claim of universal high-frequency continuous control.

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

The complete API and local setup reference currently lives in the
[Chinese technical documentation](https://sunyrain.github.io/ChemWorld/getting_started/).

> Research status: benchmark candidate. Engine and replay controls are operational; formal cross-method adaptation,
> private evaluation, and external bridging remain incomplete. RC28 Gate A passed on its frozen source, but its
> current source binding is stale and current `benchmark_ready=false` pending recertification.
