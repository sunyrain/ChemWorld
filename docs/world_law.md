# World Law

ChemWorld is organized around one shared physical-chemical law, not a set of
independent mini-games. The registered Gym environment is `ChemWorld`; each
benchmark task is a constrained slice of the same law.

## Law Contract

`WorldLawSpec` records:

- ontology registry: mechanism-owned substances plus shared phases, vessels,
  instruments, operations, and state variables;
- physical constitution: executable constraints for units, non-negativity,
  material conservation, safety, measurement cost, and action preconditions;
- operation registry: the common experimental language;
- transition kernel registry: reaction ODEs, phase partitioning, separation,
  crystallization, distillation, continuous-flow, electrochemistry, and
  instrument-cost updates;
- observation kernel registry: partial, noisy instrument observations.

Current law id:

```text
chemworld-physical-chemistry
```

## Shared Modules

Reaction behavior includes Arrhenius kinetics, catalyst and solvent effects,
product degradation, coupled impurities, catalyst deactivation, and a simplified
energy balance.

Concrete species are not global defaults. Each scenario compiles a mechanism
card into a substance registry, species ledger, observable mapping, and score
contract before runtime begins. The old seven-slot reaction fixture exists only
as an explicit reference case, not as the generic world ontology.

Phase and separation behavior includes aqueous/organic phase ledgers, product
partitioning, impurity carryover, settling, phase separation, washing, drying,
concentration, transfer loss, purity, recovery, and process mass-balance error.

Year 2 process behavior adds crystallization, distillation, continuous-flow,
and electrochemistry modules. These modules expose new operations and metrics,
but still share the same ontology, physical constitution, action validation,
instrument observation layer, and trajectory schema.

Observation behavior includes HPLC, GC, UV-vis, and final assay instruments.
Agents receive measured estimates, raw signal summaries, uncertainty metadata,
and public cost/risk ledgers, but not hidden species amounts or hidden rate
parameters.

## Design Rule

New benchmark tasks should first ask: which slice of the existing world law is
being exercised? Only add a new law module when the required physical process
cannot be represented by the current ontology, constitution, transition kernels,
or observation kernels.
