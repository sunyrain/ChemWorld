# Experimental Intelligence in Executable Chemical Worlds: display items

Status: `provisional_awaiting_g2_v0_5`.
Derived-data SHA-256: `f05b99f287fd51d8d0c42d0b36727e77d4a318286b39c22cf73c364418005ba4`.

Every number in the tables below is rendered from the self-hashed arXiv derived-data
object. This file is intended for direct inclusion during manuscript typesetting.

## Main tables

### Table 1 | Qualified environment surface and formal evidence scope

| Quantity | Count | Evidence level |
| --- | --- | --- |
| registered task designs | 15 | release surface |
| typed operation types | 28 | release surface |
| instrument types | 5 | release surface |
| deterministic complete-experiment cases | 415 | design qualification |
| declared endpoints bound to evaluators | 62 | design qualification |
| tasks with formal compiled-agent results | 2 | paper evidence |
| tasks with autonomous-agent results | 1 | paper evidence |

Counts for the environment surface are design qualifications, not claims of agent
competence. Formal paper evidence covers fewer tasks than the registered surface.

### Table 2 | Compiled-experiment capability profiles

| Task | Information arm | Worlds | Final score | Held-out accuracy | Brier | Structure F1 | Mechanism F1 | Unsupported claims |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| electrochemical-conversion | opaque | 10 | 0.715 | 0.744 | 0.186 | 0.389 | 0.190 | 0.611 |
| electrochemical-conversion | nominal | 10 | 0.787 | 0.778 | 0.149 | not measured | not measured | not measured |
| electrochemical-conversion | misindexed | 10 | 0.685 | 0.711 | 0.209 | not measured | not measured | not measured |
| reaction-to-crystallization | opaque | 10 | 0.535 | 0.478 | 0.298 | 0.275 | 0.144 | 0.714 |
| reaction-to-crystallization | nominal | 10 | 0.562 | 0.433 | 0.316 | not measured | not measured | not measured |
| reaction-to-crystallization | misindexed | 10 | 0.584 | 0.433 | 0.316 | not measured | not measured | not measured |

Scores are means across ten physical worlds. Dashes indicate endpoints that were not
defined for that information arm; they are not zeroes. No composite score is formed.

### Table 3 | Autonomous development trajectories (G2 v0.4)

| Arm | Cells | Completion | Operations | Best score | Batch AUC | Realized-op AUC | Fixed-budget AUC | Discovery fraction | Retention | Max drawdown | Terminal / best | Recovery |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| opaque | 5 | 1.000 | 82.600 | 0.631 | 0.617 | 0.520 | 0.563 | 0.320 | 0.520 | 0.333 | 0.671 | 0.500 |
| nominal | 5 | 1.000 | 80.400 | 0.709 | 0.589 | 0.501 | 0.591 | 0.800 | 0.720 | 0.092 | 0.941 | 0.800 |

Each arm contains five physical-world cells and six completed vessels per cell.
Operations are mean submitted primitive attempts per cell. These development data select
the worlds and endpoints for G2 v0.5 and are excluded from its replication estimand.

### Table 4 | Fresh-trajectory replication (G2 v0.5)

G2 v0.5 is not terminal. The preregistered 20-cell matrix remains absent from the
paper data object, so no interim replication values are rendered here.

Deltas are nominal minus opaque within the same physical world and replicate block.
The two deliberately selected worlds are not pooled into a population-level estimate.

## Figure legends

**Figure 1 | ChemWorld is a controlled apparatus for experimental intelligence.**
**A,** Closed-loop interaction between a hidden chemical world, one typed agent action,
the resulting state transition and a public measurement. **B,** Physical world, prior
information, agent authority, evidence access and resources are independently controlled
experimental axes. **C,** The auditable transition spine binds typed state, atomic
transaction, resource receipt, immutable trace and exact replay; invalid actions and
failures remain evidence. **D,** Qualified release surface. Counts establish declared
reachability and evaluator binding, not agent performance across all registered tasks.

**Figure 2 | One complete agent-directed experiment and its campaign ledger.**
**A,** The first vessel from the opaque world-0 development campaign: the agent selected
reagent and solvent addition, potential setting, electrolysis, a UV-visible measurement,
termination and final assay in seven primitive operations. This example illustrates the
interface and is excluded from prior-effect inference. **B,** Independently debited
campaign resources reconstructed from the immutable trajectory; physical inventory and
instrument use are not collapsed into a scalar token budget.

**Figure 3 | Endpoint summaries conceal distinct experimental trajectories.**
Final-assay sequences for opaque and anonymous nominal-information agents in development
worlds 0, 2 and 4. Open circles identify the first campaign maximum. The examples expose
early discovery followed by abandonment, gradual improvement, drawdown and terminal
recovery that a best-score endpoint alone cannot distinguish.

**Figure 4 | Prior interventions reshape behavior without guaranteeing recovery.**
**A,** Paired nominal-minus-opaque effects on compiled-experiment final score with
familywise 97.5% world-bootstrap intervals. **B,** Early and late shares of
actions aligned with deliberately misindexed material information. **C,** Separate
preregistered checks
for manipulation, differential action correction, performance restoration and their joint
recovery rule. **D,** Nominal-minus-opaque autonomous development effects across five
physical worlds; points are worlds and horizontal bars are descriptive means. Positive
drawdown differences indicate larger drawdown under nominal information.

**Figure 5 | Fresh trajectories test within-world repeatability.**
Nominal-minus-opaque paired differences for best score, online incumbent retention,
maximum absolute drawdown and terminal-to-best ratio across five fresh replicates in each
of selected physical worlds 1 and 3. This legend becomes active only after the terminal G2 v0.5 audit is incorporated.
Selection used the prior development matrix; those trajectories are excluded. Effects are
reported within world, with no pooled population-level test.

**Figure 6 | Experimental intelligence is a profile, not a scalar.**
**A,** Compiled-experiment endpoint score, held-out directional accuracy, Brier score and
unsupported-claim rate for the opaque participant in two chemical tasks.
**B,** Autonomous
completion, retention, recovery and terminal-to-best summaries by information arm. Metric
directions differ and no composite score is computed; the panel demonstrates the need to
retain a capability profile rather than rank systems on these bars.
