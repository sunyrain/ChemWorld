# Operation Language

All ChemWorld tasks use the same event-action format:

```python
{
    "operation": "add_reagent",
    "payload": {"amount_mol": 0.01},
}
```

For convenience, payload fields may also be supplied flat:

```python
{"operation": "heat", "target_temperature_K": 385.0, "duration_s": 1200.0}
```

The action codec also accepts common aliases and maps them to canonical fields.
For example, `temperature_K` maps to `target_temperature_K`, `stirring_rpm` maps
to `stirring_speed_rpm`, catalyst `amount_mol` maps to `catalyst_amount_mol`,
and `phase` maps to `target_phase` for `separate_phase`.

## Action Abstraction Layer

ChemWorld separates the semantic action language from Gym/RL-friendly numeric
encodings:

- `EventAction`: human/LLM-facing JSON such as `{"operation": "heat", ...}`;
- `CanonicalAction`: normalized JSON with canonical operation, instrument, and
  phase names;
- `ActionCodec`: conversion between canonical JSON and stable numeric vectors;
- `OperationValidator`: task-aware and constitution-aware validity check.

This lets students, GPT agents, Bayesian optimizers, replay tools, and RL
libraries target the same underlying operation semantics.

## Reaction Operations

| Operation | Purpose |
| --- | --- |
| `add_reagent` | Add reactant A to the vessel |
| `add_solvent` | Add solvent and set solvent identity |
| `add_catalyst` | Add active catalyst and set catalyst identity |
| `heat` | Integrate reaction ODEs with jacket heating |
| `wait` | Integrate reaction ODEs without active heating |
| `sample` | Remove sample volume and material |
| `quench` | Cool the reactor and mark reaction quench |
| `terminate` | End processing before final assay |
| `measure` | Use an instrument to obtain partial observation |

## Separation Operations

| Operation | Purpose |
| --- | --- |
| `add_phase` | Add an aqueous or organic phase |
| `add_extractant` | Add extraction solvent |
| `mix` | Distribute product and impurities across phases |
| `settle` | Allow phases to separate |
| `separate_phase` | Retain selected phase with entrainment loss |
| `wash` | Reduce impurity at a small recovery cost |
| `dry` | Reduce solvent-loss signal |
| `concentrate` | Reduce volume with cost/risk tradeoff |
| `transfer` | Move retained material with handling loss |

For a reaction-to-purification workflow, use `quench` before downstream
processing and reserve `terminate` for the final stop before `final_assay`.
A typical order is:

```python
[
    {"operation": "add_solvent", "volume_L": 0.03, "solvent": 1},
    {"operation": "add_reagent", "amount_mol": 0.012},
    {"operation": "add_catalyst", "catalyst": 2, "amount_mol": 0.0004},
    {"operation": "heat", "temperature_K": 350.0, "duration_s": 1200.0, "stirring_rpm": 800.0},
    {"operation": "quench"},
    {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.012},
    {"operation": "add_extractant", "volume_L": 0.02, "solvent": 2},
    {"operation": "mix", "duration_s": 120.0, "stirring_rpm": 600.0},
    {"operation": "settle", "duration_s": 300.0},
    {"operation": "separate_phase", "phase": "organic"},
    {"operation": "wash", "phase": "organic", "volume_L": 0.01},
    {"operation": "dry", "phase": "organic", "duration_s": 300.0},
    {"operation": "concentrate", "phase": "organic", "target_volume_L": 0.008, "duration_s": 300.0},
    {"operation": "terminate"},
    {"operation": "measure", "instrument": "final_assay"},
]
```

`ActionMaskWrapper` reports which operation types are currently valid for the
task and state. It does not replace the physical constitution: payload values
are still checked by `ActionCodec` canonicalization and precondition logic.
