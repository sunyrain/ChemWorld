# Work I F/V/L frozen derived-data layer v0.1

Status: **frozen with explicit latent missingness**

- Derived-data SHA-256: `1d639b09215ade3b84e9c2e5a9e30479fed1387890ab272d29b0996e7a06a2c4`
- Data-contract SHA-256: `e3a941c5a4d958b8284a244947a4c3e1b4ae3639576d12e27a005dbb9baa363c`
- File manifest SHA-256: `deb80ae1e0fd40cb0bf40cee34d79e3450167624739dc990f4197be2ba6b542f`
- F: 6 fork pairs, 12 within-pair expectations, 24 original/replay traces.
- V: 30 original campaign profiles, 180 original lifecycles, 30 reliability-only retests.
- L: 60 terminal lifecycles, 36 retained discard units, 10 campaign cells.
- L outcomes: 6 resolved and 30 unresolved; complete-case substitution is forbidden and unused.
- Provider calls made by this build: 0.

The layer is additive to the existing G0/G2 source and keeps the release schema identifier stable.
It publishes only normalized rows, hashes, counts, registered bounds, and explicit failure labels;
raw hidden states and provider payloads are excluded. Downstream evidence-DAG, ledger,
release-manifest, data-card, manuscript, and figure regeneration remain owned by W1-D04/D05/P09.
