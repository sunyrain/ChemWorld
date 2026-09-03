# Anonymous supplementary package

This directory documents the generated supplementary archive for *Causal Dissection of Scientific
Agents: Breaks from Evidence to Action*.

The publication reanalysis field `formal_result=false` means that this provider-free synthesis did
not create a new formal execution. It does not relabel the retained formal and development source
blocks, whose evidence roles remain explicit in the packaged data.

Build the archive from the repository root with:

```powershell
uv run --no-sync python paper\tools\build_prior_discovery_supplement.py
```

The builder writes
`paper/exports/prior-discovery-iclr2027/prior-discovery-iclr2027-supplement.zip`. The archive is a
publication projection, not a copy of local run directories. It contains:

- a sanitized publication report and cell-level derived records for the four-condition, C2 and B3
  analyses;
- all 45 public B2 summaries, configuration-level expression counts, the retrospective coding
  function, and the participant-visible identifiability audit;
- all figure source tables used by the venue-neutral figure bundle;
- public protocol projections for the longitudinal, matched-evidence, identifiable-law, and
  four-condition action assays;
- the exact system prompts or prompt-generating function sources used by the reported assays;
- representative strict response schemas and the executable-law contract;
- a chronological platform-recovery and oracle-qualification provenance record;
- a content manifest and a standalone verification script.

The archive intentionally excludes raw provider payloads, private reasoning, credentials, provider
authentication settings, local paths, run roots, thread or request identifiers, private seeds, and
author identity. Source paths are replaced by semantic roles plus SHA-256 digests. Failed,
right-censored, donor-blocked, and unstarted scheduled units remain visible in the released
denominators.

After extracting the archive, run:

```powershell
python verify_supplement.py
```

The verifier uses only the Python standard library. It validates every packaged file digest,
recomputes the four-condition contrasts and the C2/B3 failure-aware denominators from packaged
cell-level records, and independently reruns the B2 expression coding. It does not contact a model
provider or rerun a physical simulation.
