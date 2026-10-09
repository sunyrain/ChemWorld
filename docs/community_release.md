# Current development distribution

The next community package is built from **sunyrain/ChemWorld main**, using its
current runtime. It is not the frozen paper package and is not a new published
release. Version 0.2.0 is currently retained in both package and core metadata;
do not upload this development build over the existing paper release. Final
version/tag/citation alignment requires the separately authorized release step.

## Package boundary

Build from a Git checkout (`uv build`) or rebuild the generated sdist. A raw
GitHub source ZIP is not a build input: use the sdist when Git is unavailable.
The build hook selects only version-controlled Python implementation/schema
files and explicitly approved runtime resources. Local untracked drafts, even
inside source/config directories, do not enter either distribution. Stage an
intended new public source file before building; review the package diff.

The sdist contains its exact source-file index for a Git-independent rebuild.
It includes minimal public examples and licensing/contribution guidance, not
papers, figures, research protocols, provider configurations, private evaluation
inputs, credentials, run logs or the full research archive. Built-in local
evaluation code is included; owning the package gives access to its simulator
implementation. It is **not** a security sandbox or a way to hide evaluator
truth from arbitrary local Python code.

Supported package workflows are public task inspection, current-runtime
experiments, logging, replay, evaluation, authoring and dataset export. Research
runners referring to external/frozen evidence remain checkout tools, not a
promise that those evidence files ship in the wheel. Never substitute current
physics to reproduce an old trajectory.

## UI scope

The provider-free Student Lab is reused from ChemWorld-Public and included in
the wheel. Start it with `chemworld-lab --no-browser`, then visit the printed
loopback URL (default `http://127.0.0.1:8876`). The checkout research Task Lab
remains a separate developer tool, not a wheel entry point. No remote hosted
service or model-provider execution is authorized by this development work.

Both writable servers check Host/Origin, same-site context, JSON content type,
body size (64 KiB), connection lifetime and concurrent handlers (16), plus a
server-wide 120-writes/minute limit. Student sessions are limited to 16; the
packaged Lab also caps each history at 1,000 operations. The checkout runner
permits two active jobs, 32 retained jobs, 200 steps/task and 10,000 events/job.
These are local abuse/resource bounds, not authentication or a hostile-code
sandbox. Do not expose either server through a reverse proxy or port forward.

The Lab exports native JSONL, uses the normal exact verifier, and closes sessions
without inserting an assay. Reset exports/closes the previous session. Keep the
download or copy the export text **before leaving the page**; process exit removes
temporary session storage. A download request is not proof the browser saved a
file. The checkout runner's cancellation is cooperative at its next event
checkpoint, not a promise to interrupt an in-flight provider/network request.
No paid/provider cancellation behavior has been tested.

The installed package is checked for static assets, session creation, committed
final assay, native export/replay and close. Browser checks cover labelled
controls, keyboard selection, final-assay count, replay feedback and close;
screen-reader/mobile and remote multi-user support are not claimed.

On macOS, the installed-wheel browser walkthrough reached one final assay and
reported exact replay of four operations (maximum error 0). A second one-action
session exported readable native JSONL and closed with zero final assays.
Keyboard operation selection and labelled export text were checked. The embedded
browser did not confirm a Blob download reaching disk; the copyable export is
verified, but filesystem download behavior across browsers is not yet certified.

### Included Lab assets

Python/HTML/CSS/JavaScript Lab sources originate from
[ChemWorld-Public at db98e800](https://github.com/sunyrain/ChemWorld-Public/tree/db98e8002fac0512ed9084a3c8c27985cb9fc405/src/chemworld/lab),
under the same MIT License, copyright 2026 ChemWorld Contributors. This work
adapts those sources to current interfaces and local safety/lifecycle handling;
it does not ship another runtime. The apparatus is drawn in CSS, not a copied
third-party image. No remotely loaded font, telemetry or provider is needed by
the packaged UI. Preserve the repository LICENSE when redistributing.

The remaining distributed Python sources, examples, documentation and finite
simulator configuration tables are repository-authored material under that same
MIT license. The included tables specify synthetic model contracts; they are not
redistributed experimental datasets or a validated chemistry database. No paper
figures, photographs, manuscript assets, proprietary reference data or external
font files are in the distribution allowlist. Dependencies are installed
separately and retain their own licenses; `uv.lock` identifies their versions,
not a relicensing grant. Source distributions include the lockfile and bilingual
quickstarts. Review any future third-party asset before extending the allowlist.

## Frozen paper reproduction

Use the independent [paper snapshot and its lockfile](https://github.com/sunyrain/ChemWorld-Public/tree/03e8026301c185fd6ba5bdbda7460765d9b3e724).
The binding is `configs/current.json` → `publication.frozen_release` in the
research checkout. Current main has one runtime, no old-physics compatibility
backend. Other historical trajectories require their own original execution
commit, not automatically the paper snapshot.

## External CI diagnosis (9 October 2026)

The public repository's failed CI run 31571033524 and documentation run
31571033531 at `db98e800` did **not** execute their build/test steps. GitHub's
check annotations report an account billing lock. This is an infrastructure
block, not evidence that source tests failed or passed. A successful Pages
deployment is likewise not package validation. This work does not change account
billing or publish to that separate repository.

The newly added development workflows at `29b46d4d` were blocked for the same
reason (for example check 113696715300); no cloud test step ran there either.
The same condition was independently confirmed at `a7badfc6`: the
[current-interface check](https://github.com/sunyrain/ChemWorld/runs/113744875024)
has an empty step list and an explicit billing-lock annotation. Restoring Actions
requires the repository account administrator; changing source code cannot fix it.

Local installation/matrix results and current-repository CI are reported
separately; never count a queued or billing-blocked job as passed.

## Development validation

Target matrix: Linux, Windows and macOS, each with Python 3.11 and 3.12.
Metadata allowing newer Python versions is not a claim that they were tested.
The workflow runs focused current-interface checks, then installs **both wheel
and sdist** into fresh environments outside the checkout using committed locked
dependencies. Documentation has a strict-build-only job, with no deployment,
tagging or package publication.

Run the same installation check locally:

```bash
uv sync --locked --extra dev --extra docs
uv run --no-sync python scripts/smoke_test_wheel.py --python 3.11
uv run --no-sync python scripts/smoke_test_wheel.py --python 3.12
uv run --no-sync mkdocs build --strict
```

At the first packaging batch, macOS arm64 **3.11.15 and 3.12.14 passed for both
archive types**: all 15 task resets, six current contracts, public resource loads,
the eight-operation manual example through final assay, and new-process CLI
run/verify/evaluate. Package checks compare actual clean and dirty archives
byte-for-byte, including a no-Git sdist rebuild. Linux/Windows jobs are not
counted as passed until execution results are available. No old qualification
or scientific result has been regenerated.

The final current-interface integration at `a7badfc6` passed **125 tests** and
the strict Chinese/English documentation build. After incorporating the optional
notebook-history extension at `5e226b86`, the affected Lab and offline-example
regression passed **45 tests**. Six existing scikit-learn GP arithmetic warnings
were reported, not suppressed. Focused type checking of the public Lab and
examples passed (nine directly checked files); package-wide typing still reports
errors in research modules outside this delivery. Do not interpret the focused
CI job as a claim that repository-wide typing is clean.
The final global check reports 192 errors in 36 files (449 files checked), in
evaluation/provider/agent modules and two core interface/resource modules. Those
owned-core issues were not hidden with ignores or reassigned to this UI release.

Both archive types were reinstalled on macOS arm64 Python **3.11.15 / 3.12.14**
after that integration. In addition to the checks above, each installation ran
the four-action custom agent, all seven offline research episodes and seven
independent-process replays, plus packaged-Lab final assay/export/replay/close.
The smoke report now records the actual OS, architecture, Python patch version
and replay denominator. These are provider-free software checks, not new paper
experiments or evidence of improved scientific predictions.

### Observed installation matrix

| Actual platform | Python | Wheel | sdist |
| --- | --- | --- | --- |
| macOS arm64 | 3.11.15 | Passed | Passed |
| macOS arm64 | 3.12.14 | Passed | Passed |
| Ubuntu 22.04 x86_64 | 3.11.15 | Passed | Passed |
| Ubuntu 22.04 x86_64 | 3.12.13 | Passed | Passed |
| Windows CI target | 3.11 / 3.12 | Not run | Not run |

The eight completed installations each passed the full smoke described above,
including seven new-process offline replays. Linux used the same execution code
at `5e226b86` with the smoke report enhancement at `9a2f90a7`; documentation-only
changes do not change those execution semantics. Initial server dependency
downloads stalled before tests. The fallback downloaded the exact official
Linux wheels named by `uv.lock`, verified their SHA-256 hashes and installed the
exported locked requirements from a temporary offline wheelhouse. It did not
borrow the server's existing Python 3.13 environment, change dependency versions,
run providers or replace an unfavorable experiment. Both Linux archive checks
then completed in fresh environments outside the source tree.

This is not a claim about every Linux distribution, macOS Intel, other Python
versions, Windows, screen readers or mobile browsers. The declared target matrix
is unchanged. **Cross-platform acceptance remains incomplete** until a Windows
runner executes both archive paths and GitHub's account-level Actions lock is
resolved. The latest workflow at `9a2f90a7` likewise has no executed steps; see
[its current-interface check](https://github.com/sunyrain/ChemWorld/runs/113761967642).
An administrator must restore Actions or provide an authorized Windows runner;
do not remove that matrix entry merely to turn this record green.
