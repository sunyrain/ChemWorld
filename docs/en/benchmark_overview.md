# Benchmark Design

> **How do we know that an agent learned to experiment rather than merely scoring well in a fixed world?**

ChemWorld Bench separates task outcomes, constraints, resources, and adaptation. It does not collapse physical tasks
and interaction levels into one intelligence score.

## Evaluation units

```text
Campaign
└── Experiment
    └── Operation
```

Campaign Design compares complete experiments. Procedure Execution and Process Control additionally require operation,
measurement, and control-frequency accounting.

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

## Trust chain

```text
submission → trajectory validation → deterministic replay
→ metric recomputation → constraint/resource audit → verified result
```

The current Engine and replay controls are operational. The complete cross-method adaptation matrix, multi-seed RL,
real-LLM evaluation, private generalization, and external bridge evidence remain incomplete.

Next: [Research Findings](research_findings.md) · [Real-world Bridge](real_world_bridge.md)
