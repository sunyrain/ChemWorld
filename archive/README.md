# Historical material and recovery

The active manuscript entry is [paper/README.md](../paper/README.md). Current
English/Chinese documents and editable figures are listed in the
[bilingual guide](../paper/venues/ncs/README.md).

## 28 September 2026 closeout

Retired editorial scripts, figure candidates, older manuscript exports and Office
recovery copies are packaged under `archive/packages/2026-09-28/`. The
[file index](CONTENTS.tsv) maps every original path to its ZIP package. Each ZIP
preserves repository-relative paths, so files can be inspected or restored without
guessing their former location. Packages were verified against the original bytes
before the originals were removed from the active tree.

| Package | Contents |
| --- | --- |
| `retired-editorial-code.zip` | Superseded figure builders, layout patches and old Chinese export scripts |
| `figure-concepts.zip` | Unselected ImageGen concepts, alternative layouts, prompts and galleries |
| `superseded-figures.zip` | Earlier figure exports and comparison candidates |
| `figure-working-exports.zip` | Intermediate case/figure previews |
| `superseded-manuscripts.zip` | Earlier Word/PDF exports and superseded writing snapshots |
| `superseded-presentations.zip` | Earlier decks and WPS recovery copies |
| `local-user-materials.zip` | Preserved local conference-poster files |

The packages are **local, ignored files**, not uploaded release artifacts.
`CONTENTS.tsv` distinguishes Git-tracked files from local-only files. Retain a copy
of the packages when moving this workspace: local-only material cannot be recovered
from Git.

The seven packages contain **427 files (590.3 MiB before packing; 555.6 MiB packed)**,
including 31 retired editorial scripts. In addition, 38 old pytest temporary
directories were moved intact from the repository root to `archive/local-cache/`.
Their contents and links were preserved; these are local working residues, not
scientific releases. The pre-existing `paper.rar` was moved byte-for-byte to
`archive/local-originals/paper.rar` without unpacking or adding it to Git.

All previously tracked material is also present at source commit
`74d24c2e` (resolve the full commit with `git rev-parse 74d24c2e`). Git history,
branches and tags have not been rewritten or pruned. To inspect an old tracked
file, use `git show 74d24c2e:path/to/file`. Restore a selected file only when needed:

```powershell
git restore --source=74d24c2e -- path/to/file
```

For local ZIP recovery, extract into a separate temporary directory first and
copy only the required files back. Do not overlay an entire historical package
onto the current manuscript or tools.

## Material retained at its original paths

- Current manuscript sources, final bilingual documents, figure decks and their
  actual build dependencies, including some older-named shared renderer modules.
- Runtime and evaluation code, tests, frozen protocols, all scientific results,
  failures and machine-bound release/evidence assets.
- Raw runs, credentials and the locked environment; none enters these packages.
- Earlier scientific releases still required by reproducibility consumers.

Current manuscript/figure assets and `configs/current.json` passed 32 byte-identity
checks. The current figure imports and retained-data loading path, entry-point
links, 14 focused runtime/public-documentation/release-asset tests and Git whitespace
checks passed. Manuscript text and scientific results were not changed or rebuilt.

Archival is an editorial/workspace cleanup. It does not reclassify evidence,
change an experiment, or authorize running a retired tool. Historical records
may cite pre-closeout paths; use this index or the source commit to recover them.
