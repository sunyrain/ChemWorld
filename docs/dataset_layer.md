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

- dataset id
- task ids
- world law versions
- env versions
- commit hash
- seeds
- record count
- agent manifests
- license
- privacy/anonymization status
- known limitations

Private-eval hidden parameters are never exported as public dataset metadata.
