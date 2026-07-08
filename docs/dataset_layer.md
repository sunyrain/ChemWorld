# Dataset Layer

ChemWorld can export trajectories as dataset artifacts for offline analysis and
agent training.

```bash
chemworld datasets export --submission runs/example.jsonl --format jsonl
chemworld datasets export --submission runs/example.jsonl --format parquet
chemworld datasets card --dataset datasets/chemworld_dataset.jsonl
```

JSONL is always supported. Parquet export uses pandas and requires `pyarrow` or
`fastparquet` in the local environment.

Dataset cards report:

- dataset-card schema version
- dataset id
- task ids
- world law versions
- env versions
- trajectory schema versions
- task/runtime/mechanism/scoring/observation protocol hash sets
- replay verification summary grouped by campaign
- commit hash
- seeds
- record count
- agent manifests
- license
- privacy/anonymization status
- privacy scan flags for agent metadata, explanations, participant fields, and
  obvious top-level sensitive fields
- known limitations

The replay summary is generated from the recorded actions and hashes. A dataset
card should therefore fail closed at the metadata level: if the task contract,
runtime profile, mechanism, scoring contract, or observation contract has
drifted, `replay_verification.verified` becomes false and the mismatch fields
are recorded.

Reference-reading note for this slice: the dataset-card design follows the same
general discipline visible in local reference repositories such as IDAES
environment/version metadata, Cantera YAML version fields, and thermo JSON
version metadata: exported artifacts should carry enough version and provenance
information to reject silent semantic drift.

Private-eval hidden parameters are never exported as public dataset metadata.
