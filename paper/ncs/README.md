# Nature Computational Science working manuscript

This directory contains the living ChemWorld manuscript targeted as a **Nature Computational
Science Article**. It is separate from the earlier `paper/main.tex` author-review snapshot because
that snapshot is bound to an older evidence boundary.

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

From the repository root on Windows:

```powershell
.\paper\ncs\build.ps1
```

The build audits the evidence ledger, compiles `main.tex` with Tectonic and writes `main.pdf`.
`publication_ready` remains false until all required result slots and submission metadata are closed.

