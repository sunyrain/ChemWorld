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

The existing provider-free packaged Lab from ChemWorld-Public is the UI to reuse
against this runtime. It must pass local write-boundary, lifecycle, installed
asset and browser-path tests before being called supported here. Until that
integration is verified, the existing checkout Task Lab is not an installation
guarantee. Its writable routes still require the same security checks; labelling
them experimental does not waive those requirements. No remote hosted service
or model-provider execution is authorized by this development work.

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

Local installation/matrix results and current-repository CI are reported
separately; never count a queued or billing-blocked job as passed.
