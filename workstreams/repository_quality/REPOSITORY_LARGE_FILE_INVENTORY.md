# Repository large-file inventory

Audit owner: **Codex `/root` — 清衡**
Audit batch: **QH-01**
Measured: **2026-08-12**
Mode: **read-only inventory; no file was moved, deleted, rewritten, or re-bound**

## Purpose and threshold

This inventory supports `CL-RP-01` and `CL-RP-05` in
`CLEANUP_CLOSEOUT_TODOLIST.md`. The tracked-file decision threshold for this pass is **5 MiB**.
Ignored root-level presentation files are also listed when they exceed 1 MiB because they affect the
working-directory footprint and are easy to mistake for repository release assets.

Sizes describe the current checkout, not Git history. The checkout contains about 365 MiB of tracked
files and the Git object packs occupy about 257 MiB. These are diagnostic values, not release gates.

## Tracked files above 5 MiB

| Path | Size | Classification | Current authority and consumers | Producer or recovery route | Decision |
| --- | ---: | --- | --- | --- | --- |
| `workstreams/arxiv_v1/reports/first-paper-composition-qualification-v1-design-v3.json` | 77.83 MiB | immutable formal result; currently stale | Directly referenced by `configs/current.json` as the Work I composition qualification and by the evidence pipeline, paper figure data, manifest, ledger, and tests. Current gate state is invalidated because its runtime binding is stale. | Frozen Work I composition qualification runner; a future authorized Work I closeout must rerun the complete block from its first unit. | **Retain now.** It cannot be moved or compacted until Work I requalification defines the replacement artifact and all consumers migrate atomically. Candidate for external release storage only after that migration is designed. |
| `workstreams/arxiv_v1/reports/first-paper-composition-qualification-v1.json` | 77.82 MiB | legacy formal/development predecessor and compatibility input | Not selected by `configs/current.json`; still named by the original experiment note, the runner's default output, older deterministic-use-case and agent-use reports. | Original composition qualification runner and Git history. | **Do not delete in QH-01.** First change the current runner default and audit immutable/legacy replay consumers. Likely external/archive candidate after a compatibility migration. |
| `paper/exports/experimental-intelligence-v1/experimental-intelligence-v1-concept-atlas.pdf` | 10.62 MiB | generated publication proof asset | Bound by `paper/exports/experimental-intelligence-v1/publication-proof-manifest.json` and checked by `tests/test_publication_v1_artifacts.py`; not a current evidence-registry node. | `paper/tools/render_publication_v1_pdf.py` and its retained source assets. | **Retain through the current publication cycle.** Decide in `CL-RP-04` whether the PDF belongs in a versioned release asset rather than ordinary development history. |

Together, the two composition reports account for about **155.65 MiB**, more than 40% of the tracked
checkout. They must not be removed merely because their content overlaps: one is the current-but-stale
formal node, while the other remains embedded in historical and compatibility bindings.

## Important 1–5 MiB families

These do not cross the current decision threshold but materially contribute to growth and should be
handled as families rather than by ad hoc deletion:

| Family | Observed examples | Classification | Follow-up |
| --- | --- | --- | --- |
| Work I deterministic-use-case reports | three files around 3.35 MiB each (`v1`, `design-v2`, `design-v3`) | current stale formal result plus superseded/compatibility copies | Include in the Work I replacement and legacy-reference migration under `CL-RP-03`. |
| Work I policy-control bundles | many individual JSON bundles around 1.4–2.1 MiB | immutable formal/qualification evidence | Preserve until a release data package can retain digests, schemas, compact summaries, and retrievable full payloads. |
| Work II RC certificates and decisions | multiple 1.4–1.9 MiB JSON files across RC15–RC29 | mixture of historical, immutable, and current references | Resolve through `configs/current.json`; never choose by RC suffix. Build an immutable-reference audit before migration. |
| Paper PNG/TIFF/PDF assets | many 1–2 MiB figures and a 1.51 MiB arXiv PDF | source assets, development figures, and release deliverables are mixed | Classify by source/rebuildable/deliverable in `CL-RP-04`; do not recompress publication evidence without visual and manifest validation. |

## Ignored root-level presentation files

The following files are untracked and ignored locally by `.git/info/exclude` through `*.pptx`:

| File | Size | Observed role | Decision |
| --- | ---: | --- | --- |
| `2026科学智能大会poster.pptx` | 21.09 MiB | likely editable conference-poster source | Keep local during the active poster workflow. Confirm the canonical source before any move. |
| `2026科学智能大会poster (1).pptx` | 12.15 MiB | likely duplicate or earlier copy | Do not delete without owner confirmation. Compare provenance and slide content during `CL-RP-05`. |
| `2026科学智能大会poster-paper2-development-v3.pptx` | 0.26 MiB | smaller Work II development poster | Keep local; confirm whether it is the canonical Work II poster source. |

Because these files are ignored and untracked, they do not inflate Git clones. They do clutter the repository root
and lack recorded provenance. `CL-RP-05` remains open until the main process identifies the canonical asset and
authorizes relocation or removal.

## Safe migration contract

No large artifact should move until all of the following are true:

1. its role is classified as current, immutable release, historical/compatibility, generated, or local-only;
2. every current-registry, manifest, test, manuscript, script, and immutable-artifact reference is enumerated;
3. the replacement storage has a stable retrieval URL or release identifier and a cryptographic digest;
4. ordinary clone, wheel smoke, public replay, and publication builds do not silently require the removed payload;
5. historical formal evidence remains verifiable without rewriting its content;
6. one atomic migration updates current consumers and adds an explicit compatibility or retrieval record;
7. the relevant Work I/Work II release tests pass after the migration.

This audit authorizes no deletion. The next safe action is a machine-readable reference map for the two
composition reports and the publication proof family after the active Work II write set is quiet.
