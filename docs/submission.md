# Submission Bundles

A submission bundle is a local folder that contains enough information for a
maintainer to replay, audit, and summarize an agent run.

Create a skeleton:

```bash
chemworld submission init my_submission \
  --agent-name scripted_chemistry \
  --agent-family baseline \
  --task-id reaction-optimization-standard
```

Required structure:

```text
my_submission/
  manifest.json
  trajectories/
    *.jsonl
  results/
    *.json
  explanations/
    *.json
```

Validate:

```bash
chemworld submission validate my_submission
```

Summarize:

```bash
chemworld submission summarize my_submission
```

`manifest.json` includes agent name, agent family, ChemWorld version, commit
hash, dependency file, command, task id, seeds, and optional LLM metadata.

The bundle protocol is local-first. It does not require a web account system or
remote evaluation service.

