# Work I F/V/L evidence binding v0.1

Status: **13/13 new nodes current; latent scientific gate remains blocked**

- Evidence graph SHA-256: `a7f7ef76e69fb9532197f8b7352da24ecd6103cdc1ced11f68f86bde5577a2af`
- D01 data-contract SHA-256: `e3a941c5a4d958b8284a244947a4c3e1b4ae3639576d12e27a005dbb9baa363c`
- D03 derived-data SHA-256: `1d639b09215ade3b84e9c2e5a9e30479fed1387890ab272d29b0996e7a06a2c4`
- D03 manifest SHA-256: `deb80ae1e0fd40cb0bf40cee34d79e3450167624739dc990f4197be2ba6b542f`

The DAG now records the F qualification and certificate; V formal audit, validity report,
and delivery manifest; L frozen contract, reconstructability, synthetic replay qualification,
formal shadow receipts, and analysis; plus the D01 contract and D03 derived layer/manifest.
Bindings fail closed on stale embedded hashes, dependency file hashes, registered record counts,
manifest bytes, or changes to the 6-resolved/30-unresolved latent boundary.

All 13 new nodes are source-current. The L formal-shadow and analysis nodes intentionally have
`gate_state=blocked`: current provenance does not convert an incomplete latent result into a
positive scientific gate. Complete-case substitution remains false.

The registry refresh also detected an existing `runtime_affordance` guarded-source mismatch,
raising the pre-existing stale-binding count from 10 to 11. D04 preserves that truth and does
not regenerate the unrelated runtime audit or the ten historical RC28/pre-arXiv bindings.
Experiment-ledger, release-manifest, and data-card integration remains W1-D05.
