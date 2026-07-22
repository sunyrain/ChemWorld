# Benchmark Design

> **How do we know that an agent learned to experiment rather than merely scoring well in a fixed world?**

ChemWorld Bench reports task outcomes, constraints, resources, and adaptation separately. It does not compress
different physical tasks and interaction levels into a single intelligence score.

## Evaluation units

```text
Campaign
└── Experiment
    └── Operation
```

Campaign Design compares complete experiments. Procedure Execution and Process Control additionally require operation,
measurement, and control-frequency accounting.

Each campaign is one canonical **Task × Scenario × Agent × Seed** cell. A Task is a stable public contract; a World is
a hidden physical-law instance; a Scenario adds initial state, intervention, reset/feedback condition, and seed.

## Suite roles

- **Core:** frozen formal method comparison; v0.4 contains four tasks and method freeze remains blocked.
- **Diagnostic:** identifiability, feedback use, counterfactual, adaptation, and autonomy attribution.
- **Extended:** environment coverage, training, teaching, and method development without an automatic ranking claim.

## Six reporting axes

1. Task-specific outcome and practical effect threshold.
2. Operational risk, legality, and failures.
3. Experiment, measurement, and process cost.
4. Adaptation speed after a world shift.
5. Information efficiency and uncertainty reduction.
6. Training compute, environment steps, tokens, cost, and latency.

An endpoint improvement does not compensate for an undeclared risk or resource regression.

## Generalization axes are distinct

New seeds test instance randomness; parameter extrapolation tests range shift; new mechanism families test causal
adaptation; independent backends test simulator-specific shortcuts; real data or physical systems test bridge validity.
None substitutes for another.

## Adaptation metrics

Change detection, mechanism identification, recovery experiments, adaptation regret, transfer advantage, and
constraint cost during adaptation describe how agents respond when old assumptions fail.

Mechanism evidence is also factorized into **Declared**, **Predictive**, and **Actionable** layers. Mechanism v0.2.1
mainly covers declaration and action diagnostics; an independent counterfactual-prediction probe remains future work.

Trajectory v0.2 separately records `environment_outcome`, `agent_visible_observation`, and `evaluation_outcome`.
Feedback permutations may alter only the visible layer. Local paired-prefix tests ask whether feedback changes behavior;
full campaigns ask whether that change improves utility.

## Trust chain

```text
submission → trajectory validation → deterministic replay
→ metric recomputation → constraint/resource audit → verified result
```

The current Engine and replay controls are operational. Formal method readiness remains 0/6. The v0.2.1
action/intervention audit passes and electrochemical Gate A cells pass, but reaction-to-crystallization family-wise
confidence bounds keep Gate A failed. Cross-method evaluation, real-LLM evaluation, private generalization, and
external bridge evidence remain incomplete.

Next: [Research Findings](research_findings.md) · [Real-world Bridge](real_world_bridge.md)
