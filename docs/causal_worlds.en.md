# Causal Worlds

> **ChemWorld is not defined by having many tasks. Its central capability is running the same public task under
> different, auditable hidden rules.**

A high score in one fixed simulator cannot tell us whether an agent learned to experiment or merely learned that
simulator. ChemWorld changes rate laws, reaction topology, constitutive behavior, or equipment boundaries while
holding task semantics and public tools stable.

## World, task, scenario, seed

| Concept | Meaning |
| --- | --- |
| World | The causal rules: kinetics, phases, equipment, instruments |
| Task | The experimental problem and success criteria |
| Scenario | One initial state and hidden instance inside a world |
| Seed | The deterministic index for reconstructing an instance |

Changing a seed often changes noise or initial conditions, not causal structure. Multi-seed robustness is therefore
not equivalent to mechanism adaptation.

## The public contract stays stable

Agents see the same goal, action schema, and instrument semantics across world families. They receive no world label
and cannot inspect hidden mechanism parameters. Useful adaptation must appear in chosen measurements, revised beliefs,
and changed actions.

## A minimal flow example

Under the same public task, increasing temperature can primarily accelerate the desired reaction, amplify a side
reaction, or reveal a heat-transfer limitation. A fixed recipe cannot diagnose these alternatives. An adaptive agent
must choose evidence that distinguishes them.

## Splits use world families

Train worlds support learning, Dev worlds support model selection, and Bench worlds are accessed once with frozen
methods. Mechanism cells should not overlap. Already inspected worlds are development evidence, not untouched
confirmation data.

## Current control evidence

Six research tasks expose executable mechanism or constitutive-law families. Across five worlds and five representative
recipes, nine task–mode combinations pass determinism, identifiability, bounded-response, conservation, and replay
controls. This validates the environment shift—not agent adaptation.

Next: [Benchmark](benchmark_overview.md) · [Research Findings](research_findings.md)
