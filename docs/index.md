# ChemWorld-Bench

ChemWorld-Bench is an open benchmark for closed-loop virtual chemical
experimentation. It provides hidden semi-mechanistic worlds, standard action
and observation protocols, official baselines, trajectory logs, and leaderboard
metrics.

The first environment is `BatchReactorWorld`, a finite-budget event-driven
batch reactor world with yield, selectivity, cost, safety, and noisy
instrument observations. It uses a reusable Chemical World Model foundation:
ontology, executable physical constitution, state ledger, ODE transition
kernel, and instrument observation kernel.
