# Why ChemWorld

> **Why can experimental agents not learn only from real laboratories and static datasets?**

Experimental competence grows through interaction, yet real chemistry cannot supply failures at the scale, speed,
or safety profile available to language or game agents. ChemWorld therefore builds controlled causal worlds in
which experimental strategy can be trained, compared, and falsified.

> **ChemWorld unifies a physical causal world substrate, an experimental interaction runtime, and task/evaluation
> contracts so that search, execution, identification, and adaptation can be studied as one experimental-intelligence
> problem.**

The agent, trainer, and model weights remain outside these layers. ChemWorld may provide training interactions or
evaluate a fixed-weight model, but the environment does not update agent weights or maintain its internal world model.

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
replay. The Engine targets decision and causal validity before universal numerical fidelity.

## System layers and product surfaces

The normative system has three layers:

| Layer | Question |
| --- | --- |
| Physical Causal World Substrate | What hidden physical worlds can exist, change, and produce outcomes? |
| Experimental Interaction Runtime | How does an agent execute experiments, measurements, failures, and lifecycle actions? |
| Task and Evaluation Contract | What must be achieved, what is visible, what is budgeted, and how is performance evaluated? |

Engine, Bench, Lab, and Bridge are user-facing product surfaces rather than architectural layers:

| Layer | Role | Status |
| --- | --- | --- |
| ChemWorld Engine | World substrate, runtime, instruments, interventions, replay | Operational and evolving |
| ChemWorld Bench | Splits, resource contracts, adaptation metrics, private evaluation | Candidate protocol |
| ChemWorld Lab | Student Lab and Agent Observatory | Available locally |
| ChemWorld Bridge | Independent backends, real data, physical systems | Validation roadmap |

ChemWorld targets structural completeness of the interaction stack across selected physical-chemistry archetypes;
chemical coverage and numerical fidelity are bounded and explicitly declared, not exhaustive.

Next: [Experimental Intelligence](experimental_intelligence.md) · [Causal Worlds](causal_worlds.md)
