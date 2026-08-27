# Work II reviewer control analyses

## Denominators

- W2-50: 42/45 eligible; 3 retained failures.
- Typed-law capacity: 135/135 cells completed; 0 analysis failures; provider calls 0.

## Continuous law--action relation

Pooled law MAE versus normalized regret: Spearman -0.1327; versus selected rank: -0.0731.

| task | n | Spearman law MAE vs rank |
|---|---:|---:|
| electrochemical-conversion | 15 | 0.5237 |
| reaction-safety-constrained | 15 | -0.5916 |
| reaction-to-crystallization | 12 | -0.0072 |

## Typed-law capacity

Participant law to final prediction MAE: 0.153855.
Best full-schema MAE: 4.24654e-13; near-exact cells 135/135.
Term-matched MAE: 0.011427; near-exact cells 58/135.
Leave-one-query-out MAE: 0.078759.

The full-schema result is an in-domain representation-capacity control. It does not claim that the fitted oracle is a globally identified mechanism.
