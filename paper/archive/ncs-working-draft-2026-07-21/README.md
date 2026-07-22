# Archived Nature Computational Science working manuscript

This is the 2026-07-21 NCS working-draft snapshot. It is historical, not part of the current
evidence DAG, and it must not block the mechanism-adaptation benchmark work. Its pending slots and
old evidence bindings are intentionally preserved for provenance rather than maintained as current
claims.

The draft follows the journal's current Article structure:

- an unheaded introduction;
- Results with topical subheadings;
- a Discussion without subheadings;
- Online Methods;
- no more than six planned display items.

Incomplete experiments are represented by visible `PENDING-*` slots. A pending slot may be replaced
only after the evidence path named in `evidence-ledger.json` exists, passes its own release gate and
is bound into the manuscript ledger. Development and preflight results may be described as such but
must not be promoted to formal benchmark comparisons.

## Build and audit

From this archive directory on Windows:

```powershell
.\paper\archive\ncs-working-draft-2026-07-21\build.ps1
```

The build audits the evidence ledger, compiles `main.tex` with Tectonic and writes `main.pdf`.
`publication_ready` remains false. Re-activating this manuscript requires a new explicit evidence
boundary and is outside the current repository roadmap.
