# Reaction And Separation Tasks

The first task expansion keeps one environment, `ChemWorld`, and adds downstream
processing to the same world state.

## Reaction-To-Purification

`reaction-to-purification` asks an agent to run a reaction, quench it, add a
phase/extractant, mix, settle, separate, wash or concentrate if useful, and then
terminate for final assay.

Official outputs include:

- reaction score;
- purity;
- recovery;
- phase ratio;
- product in organic and aqueous phases;
- impurity signal;
- solvent loss;
- process mass-balance error.

## Partition Discovery

`partition-discovery` narrows the task to learning how solvent and process
conditions affect product distribution across phases. It is useful for local
world-model learning because the agent must infer partition behavior from
partial instrument observations.

## Purity-Yield Tradeoff

`purity-yield-tradeoff` rewards downstream decision-making under competing
objectives. A high-yield reaction can still be a poor process if washing,
separation, or concentration causes high loss, high cost, or poor purity.

## Why This Matters

These tasks broaden the benchmark without creating disconnected environments.
The same constitution enforces units, non-negativity, action preconditions,
measurement cost, material ledgers, and safety signals across reaction and
separation.
