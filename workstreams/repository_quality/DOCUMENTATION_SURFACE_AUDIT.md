# Documentation surface audit

Audit owner: **Codex `/root` — 清衡**
Audit batch: **QH-01**
Measured: **2026-08-12**
Mode: **read-only classification; `mkdocs.yml` and `docs/` were not changed**

## Conclusion

The apparent MkDocs “pages not included in nav” warning is not an orphan-page defect. The Chinese site has a
curated 24-page narrative navigation, while all 34 remaining Chinese Markdown pages are linked from
`docs/reference_index.md`. There are **zero unclassified Chinese public pages**. Nine `.en.md` files are locale
overlays managed by `mkdocs-static-i18n`, not separate Chinese navigation targets.

The current information architecture is therefore intentional:

```text
curated narrative navigation (24 pages)
└── technical reference index
    └── reference-only catalog (34 pages)

English locale overlays (9 pages)
└── independent compact English navigation
```

No navigation expansion is recommended during the active Work II development. Adding all 34 technical pages to
the primary navigation would make the public path harder to scan and duplicate the purpose of the reference index.

## Classification

### Curated Chinese navigation — 24 pages

`index.md`, `vision.md`, `experimental_intelligence.md`, `research_findings.md`,
`benchmark_release.md`, `limitations.md`, `real_world_bridge.md`, `one_experiment.md`,
`causal_worlds.md`, `worlds.md`, `interactive_task_lab.md`, `getting_started.md`,
`architecture.md`, `tasks.md`, `agent_tracks.md`, `agent_interface.md`,
`world_model_learning.md`, `llm_agent_harness.md`, `benchmark_overview.md`,
`flagship_experiments.md`, `benchmark_protocol.md`, `submission.md`,
`release_integrity.md`, and `reference_index.md`.

### Reference-only catalog — 34 pages

All are reachable from `reference_index.md`:

- world/runtime: `campaign_model.md`, `world_law.md`, `scenario_generation.md`,
  `mechanism_schema.md`, `backends.md`, `world_validity.md`;
- physics/instruments/materials: `physchem_core_design.md`, `model_maturity.md`,
  `reaction_separation_tasks.md`, `safety_cost.md`, `instrument_contracts.md`,
  `spectroscopy.md`, `material_identity.md`;
- Agent/authoring/operations: `world-authoring-contract.md`, `world-composition-contract.md`,
  `world-composition-examples.md`, `world-composition-coverage.md`,
  `world-capability-map.md`, `operations.md`, `action_schema.md`, `wrappers.md`,
  `agent_interaction_examples.md`;
- tasks/data/evaluation: `task_cards.md`, `env_cards.md`, `task_taxonomy.md`,
  `dataset_layer.md`, `baseline_reference.md`, `seed_suite.md`, `validation.md`,
  `local_eval_machine.md`, `api_reference.md`, `demos.md`;
- teaching/governance: `tutorial_curriculum_zh.md`, `ethics_and_data.md`.

Pages already present in the main navigation, such as `architecture.md`, `agent_interface.md`, `tasks.md`,
`llm_agent_harness.md`, `world_model_learning.md`, `submission.md`, and `release_integrity.md`, are also linked
contextually by the reference index but are not counted twice in the 34-page reference-only set.

### English locale overlays — 9 pages

`index.en.md`, `vision.en.md`, `experimental_intelligence.en.md`, `causal_worlds.en.md`,
`architecture.en.md`, `benchmark_overview.en.md`, `flagship_experiments.en.md`,
`research_findings.en.md`, and `real_world_bridge.en.md`.

The English navigation is deliberately smaller than the Chinese reference surface and is configured as an i18n
locale, not as an “English” bucket inside Chinese navigation.

### Internal or obsolete pages

None were identified under `docs/` by the current public-doc contract. Internal coordination, experiment notes,
evidence reports, and manuscript workflow records live outside `docs/` under `workstreams/` or `paper/`.

## Verification evidence

The existing public documentation audit already enforces:

- no missing or duplicate navigation targets;
- no unlisted public pages;
- local-link and image-reference integrity;
- bilingual navigation and locale isolation;
- current status and claim-boundary consistency;
- intentional navigation folding behavior.

At the repository review baseline, `tests/test_public_docs.py` passed and `mkdocs build --strict` completed
successfully. This QH-01 pass additionally compared all top-level Chinese `docs/*.md` files against both the
MkDocs navigation and links in `reference_index.md`, producing `24 nav / 34 reference-only / 0 unclassified`.

## Recommended follow-up

- Keep the current navigation unchanged during Work II development.
- Treat the MkDocs informational list of non-nav pages as expected unless the public-doc audit reports an
  unlisted page.
- When a new public page is added, require exactly one disposition: curated nav, reference index, locale overlay,
  or explicit non-site/internal placement outside `docs/`.
- Revisit English coverage as a content/product decision, not as a cleanup blocker.
