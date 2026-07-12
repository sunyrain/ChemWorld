# Real-world Bridge

> **ChemWorld’s relationship to reality should not be reduced to whether one simulator is “realistic enough.”**

The Bridge question is whether virtual training reduces the experiments, risk, and cost needed to adapt to independent
models, real datasets, and narrow physical systems.

> Current status: this is a validation roadmap, not an operational physical-lab product.

## Validity ladder

| Level | Question |
| --- | --- |
| Contract validity | Are state, actions, conservation, and replay correct? |
| Decision validity | Does the world create meaningful experimental trade-offs? |
| Causal validity | Do interventions change rules and effective strategies? |
| Behavioral validity | Do agent rankings persist across independent backends? |
| Transfer validity | Does virtual training reduce target-system experiments? |
| Numerical validity | Are values accurate for a specific real system? |

Core primarily targets the first three. Bridge experiments test the fourth and fifth. Universal numerical prediction is
not the current goal.

## What may transfer

Measurement strategy, exploration order, uncertainty handling, failure recovery, safety habits, change detection, and
few-shot adaptation may transfer even when a virtual optimum does not.

## What cannot be copied directly

Anonymous catalyst doses, virtual risk scores, uncalibrated yields, virtual equipment settings, and rankings from a
single simulator cannot be treated as real recommendations.

## Bridge path

```text
Causal Core → independent backend → real dataset
→ shadow-mode physical lab → approved narrow closed loop
```

A Bridge Pack must bind material identity, action and observation mappings, units, equipment limits, calibration and
independent test data, uncertainty, safety approval, and replay provenance.

The primary metric is not zero-shot replication of a virtual recipe. It is transfer advantage at the same target-system
budget and the number of real experiments saved relative to learning from scratch.

Partition is a lower-risk first candidate; flow offers stronger control relevance but requires shadow-mode safety and
equipment validation. Crystallization and distillation should follow only after narrower bridges are established.
