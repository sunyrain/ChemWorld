# Why ChemWorld

> **Why can experimental agents not learn only from real laboratories and static datasets?**

Experimental competence comes from interaction, yet real chemistry cannot supply failures at the scale, speed, and
safety profile available to language or game agents. ChemWorld therefore builds many controlled causal worlds in
which experimental strategy can be trained, compared, and falsified.

## What static data leaves out

Existing data can test factual knowledge and outcome prediction. It does not fully test whether an agent can:

- choose the next informative experiment;
- decide whether a measurement is worth its cost and sample consumption;
- revise a hypothesis after contradictory evidence;
- recover after kinetics, phase behavior, or equipment boundaries change.

## Hypothesis–experiment–revision

Experimental intelligence extends the embodied perception–action loop:

```text
observe → hypothesize → intervene → measure → revise
   ↑                                      ↓
   └──────── failure, cost, uncertainty ──┘
```

The goal is not merely to control a state, but to design evidence that distinguishes competing explanations.

## Why not one perfect digital twin

A universal high-fidelity model of arbitrary chemistry is neither available nor a sufficient training environment.
Even a detailed simulator may teach simulator-specific shortcuts. ChemWorld keeps the public experimental contract
stable while changing hidden causal rules, allowing adaptation itself to become the object of study.

Meaningful virtual worlds still require conservation, causal coupling, partial observability, declared domains, and
replay. The Core targets decision and causal validity before universal numerical fidelity.

## Core, Bench, Lab, Bridge

| Layer | Role | Status |
| --- | --- | --- |
| ChemWorld Engine / Core | Worlds, transitions, instruments, interventions, replay | Operational and evolving |
| ChemWorld Bench | Splits, resource contracts, adaptation metrics, private evaluation | Candidate protocol |
| ChemWorld Lab | Student Lab and Agent Observatory | Available locally |
| ChemWorld Bridge | Independent backends, real data, physical systems | Validation roadmap |

Next: [Experimental Intelligence](experimental_intelligence.md) · [Causal Worlds](causal_worlds.md)
