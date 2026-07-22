# Experimental Intelligence

> **Answering chemistry questions is not the same as conducting an experiment.**

Experimental intelligence turns knowledge into falsifiable action. An agent must identify what remains unknown,
choose operations or measurements that can resolve it, revise explanations when evidence disagrees, and keep moving
under safety, cost, and time constraints.

Formally, it is the capacity to acquire evidence, construct and revise actionable world models, and adapt decisions
through constrained interaction with partially observed physical systems. A world model may reside in weights,
context, external memory, an explicit belief state, or a surrogate. ChemWorld neither prescribes nor updates it.

## Six capabilities

| Capability | Meaning |
| --- | --- |
| Observe | Separate measured evidence from hidden state |
| Hypothesize | Maintain tentative, testable explanations |
| Design | Choose experiments that distinguish explanations |
| Operate | Control materials, equipment, and instruments legally |
| Update | Change beliefs and actions after new evidence |
| Constrain | Trade off outcome, risk, cost, and time |

## Measurement is an action

Measurements consume budget, time, money, or sample. A good strategy does not measure everything; it chooses the
channel most likely to reduce decision-relevant uncertainty.

## Failure is part of the task

Invalid preconditions, uninformative measurements, unsafe proposals, and poor hypotheses are recorded rather than
silently repaired. Recovery quality—recognizing the failure, selecting a corrective step, and avoiding repetition—is
an experimental capability.

## Declared, predictive, and actionable evidence

Mechanism understanding is not a single label-accuracy score:

1. **Declared:** the agent reports a mechanism distribution or change probability;
2. **Predictive:** it predicts the result of an unexecuted intervention;
3. **Actionable:** that judgment changes the next experiment and improves recovery or regret.

The evidence chain is declaration → counterfactual prediction → action change → task recovery. Current mechanism
protocols mainly cover declaration and action diagnostics; an independent predictive probe remains future protocol
work.

## Memory operates at two scales

- Within an experiment: what has entered the vessel and what conditions it has experienced.
- Across experiments: which recipes, results, failures, and hypotheses have already been tested.

## Useful metrics

Information efficiency, change detection, recovery experiments, adaptation regret, mechanism identification,
uncertainty calibration, constraint violations, and method resources complement task outcome.

> **Experimental competence is not guessing correctly on the first attempt; it is knowing what to measure after the
> guess fails.**

Next: [Causal Worlds](causal_worlds.md) · [Benchmark](benchmark_overview.md)
