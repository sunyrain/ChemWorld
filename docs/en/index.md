# ChemWorld-Bench

<p class="cw-language-switch">
  <a class="cw-lang-button" href="../">中文</a>
  <a class="cw-lang-button cw-lang-button-primary" href="./">English</a>
</p>

ChemWorld-Bench is a research benchmark for closed-loop virtual chemical
experimentation. The formal Gymnasium entry point is `ChemWorld`: a shared
physical-chemical world where tasks are slices of the same world law rather
than separate mini-games.

Current scope:

- one shared `world_law_id`: `chemworld-physical-chemistry`;
- 14 registered task slices covering reaction optimization, safety,
  mechanism explanation, characterization, purification, partition discovery,
  crystallization, distillation, continuous flow, electrochemistry, and
  tool-agent planning;
- mechanism-driven runtime services, typed ledgers, transaction records,
  noisy instrument observations, virtual spectra, replay verification, and
  task-specific evaluation metrics;
- explicit maturity metadata so proxy, lite, reference-validated, and
  professional-candidate components are not mixed silently.

## Where To Start

| Reader goal | Start here |
| --- | --- |
| Understand the project in Chinese | [ChemWorld Overview ZH](../chemworld_overview_zh.md) |
| Inspect current implementation status | [Current Progress](../current_progress.md) |
| Understand the architecture | [Architecture](../architecture.md) and [Technical Architecture ZH](../technical_architecture_zh.md) |
| Run benchmark tasks | [Tasks](../tasks.md), [Task Cards](../task_cards.md), and [Benchmark Protocol](../benchmark_protocol.md) |
| Build an agent or optimizer | [Operations](../operations.md), [Action Schema](../action_schema.md), [Wrappers](../wrappers.md), and [Baseline Reference](../baseline_reference.md) |
| Audit environment consistency | [Environment Self-Consistency Audit ZH](../environment_self_consistency_audit_zh.md) |
| Use the 12-day course material | [Tutorial Curriculum ZH](../tutorial_curriculum_zh.md) |
| Prepare a release or paper artifact | [Release Checklist](../release_checklist.md) and [Paper Artifact](../paper_artifact.md) |

## Current Gate

The current documentation and implementation are expected to pass:

```bash
python -m ruff check .
python -m mypy src/chemworld
python -m pytest
python -m mkdocs build --strict
python scripts/audit_environment_consistency.py --tasks all --seeds 0 1 2
```

The latest local self-consistency audit reports zero replay failures, zero
spectra failures, zero invalid smoke steps, and zero constitution failures for
the registered task set.

## What ChemWorld Is Not

ChemWorld is not a real reaction predictor, DFT wrapper, process simulator, or
robot controller. It is a controllable virtual interaction environment for
agents, students, and optimizers. Physical modules are useful only within their
declared maturity limits, and benchmark claims must carry the task maturity
metadata produced by the registry.
