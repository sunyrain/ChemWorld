# Work II evidence-to-action causal decomposition

Status: development design; provider execution is not authorized.

## Question and fixed coverage

Does autonomous experimentation causally improve held-out prediction and terminal selection among
previously unseen complete ActionPlans, and where is value lost between evidence, a learned law and
action? The formal design is `3` task families x `5` fresh worlds x `3` initial-model arms x `5`
information conditions: `225` fresh sessions. The conditions are no evidence, yoked evidence,
autonomous exploration, learned-law-only context reset and oracle-law context reset. Only autonomous
sessions execute `12` physical experiments, for `540` participant experiments in total.

Each task-world-prior stratum has one autonomous donor. Its participant-visible action/observation
trace feeds the yoked session and its committed final typed law feeds the learned-law session. Donor
reasoning, hidden evaluator fields, candidate outcomes and ranks are never transferred. No-evidence
and oracle-law sessions are independent of the donor. Every condition receives the same initial
world-model arm, task contract, checkpoint queries and eight complete candidate ActionPlans. The
candidate packet is identical within a task-world-prior stratum, while its reveal time follows the
condition-specific gate below.

Candidate visibility follows the estimand rather than a universal artificial checkpoint. The
no-evidence session sees the packet at session start and ranks it immediately, with no preliminary
law-writing turn. Learned-law and oracle-law sessions receive their artifact together with the
candidate packet in one fresh-context terminal decision. Autonomous exploration sees the packet
only after experiment 12 and its final belief checkpoint; yoked evidence receives all 12 donor
experiments one by one, records matched belief checkpoints after experiments 3, 6, 9 and 12, and
then sees the packet. Candidate outcomes and evaluator ranks remain hidden in every condition.

The oracle condition uses a provider-free predictive law fitted on a registered grid disjoint from
the candidate packet. It shares the learned-law typed schema, feature/metric scope and fixed word
budget, but fitting may not read candidate outcomes. Development qualification requires candidate
rank correlation at least `0.80`; failure rejects the oracle design rather than revealing candidate
scores or silently substituting an outcome table.

## Measurements and estimands

All conditions submit one complete terminal ranking. Autonomous and yoked conditions additionally
submit the matched pre-evidence and after-experiment 3, 6, 9 and 12 belief checkpoints; direct and
artifact-only recipients do not receive extra self-deliberation turns before ranking. Primary
outcome is failure-aware normalized regret of the selected unseen ActionPlan. Secondary outcomes
are selected rank, Top-1, complete-ranking agreement, prediction error, executable-law error,
law-implied versus submitted ranking agreement, whether the law-implied Top-1 is followed,
resource/process failure and checkpoint completion. The law/action agreement measures are defined
for every condition with an executable final or supplied law and directly distinguish an artifact
that is wrong from an action module that fails to use an informative artifact. Pre-to-final
prediction change is defined only for the autonomous and yoked longitudinal conditions.

Because some valid candidate packets contain scientifically meaningful near-ties, Top-1 and exact
complete-ranking agreement are descriptive rather than gatekeeping endpoints. The registered
tie-aware readouts are selection within `0.01` raw score of the best and pairwise ordering agreement
computed only for truth pairs separated by at least `0.01`; continuous regret remains primary.

The prespecified contrasts are autonomous minus no-evidence (total value of exploration), yoked
minus no-evidence (value of acquired evidence), autonomous minus yoked (value of choosing the
experiments), learned law minus no-evidence (portable value of the submitted artifact), and oracle
law minus learned law (artifact-quality loss). Lower regret and error are better.

Each contrast is first paired within task-world-prior. The three prior arms share a physical world
and are therefore repeated factors, not independent replicates: primary estimates average the three
paired contrasts within each task-world and use the `15` task-world units as independent inference
clusters, with worlds resampled within task. Prior-specific contrasts are effect-modification
analyses and retain the same task-world clustering.

## Qualification, failure and stop rules

Provider-free qualification uses only development worlds `0..4`; formal worlds are fixed separately
and are never replaced for an unfavorable truth surface or participant result. Qualification checks
complete-plan executability, public/truth/executed identity, candidate-score spread, exact replay and
the ability of the oracle artifact to reproduce the relevant candidate ordering. Candidate Top-1
gap is reported but is not an inclusion threshold.

Autonomous donor failure is retained. Its yoked and learned-law descendants become
`not_started_due_to_missing_donor` and remain in the scheduled denominator; another donor may not be
substituted. A missing terminal ranking receives failure-aware regret `1` and Top-1 `0`, while rank
is missing. Provider or platform failures pause the affected dependency chain. A defect in
participant-visible semantics, evidence transfer, candidate disclosure or physics requires the
affected formal block to restart from its first unit after repair. Scientific failures never
authorize replacement.

The first frozen task-world cluster is the operational canary. It may stop provider expansion only
for platform, contamination, schema, binding or accounting defects, not for poor scientific
performance. Raw provider payloads and run records remain outside Git.

## Expected outputs

One machine-readable design manifest, provider-free qualification summary, all scheduled cell
records including donor-blocked descendants, sanitized public submissions, provider usage totals,
exact replay, and a readable result summary with the five prespecified contrasts and exact
denominators.

## Development qualification correction

The first provider-free electrochemical qualification unit showed that a within-packet normalized
regret count was not a stable design gate: one catastrophic candidate expanded the denominator and
made several raw score differences of `0.05--0.13` appear artificially small. Before any participant
call, the opportunity gate was therefore expressed on the registered task-score scale: the packet
must retain raw score range at least `0.15`, with at least four candidates at least `0.05` below the
best. Top-1 gap remains descriptive. The incomplete first qualification attempt is retained as
development output; qualification restarts in a new output block.

The completed hash-split development block retained all `240/240` truth/replay queries but passed
the action-opportunity gate in only `11/15` worlds: one crystallization and three reaction-safety
packets lost too much of the registered 16-query coverage. Before provider execution, candidate
selection was therefore changed to deterministic public-feature Gower maximin: eight dispersed
queries are candidates and the registered remainder is the prediction/oracle-fit set, fixed across
worlds within task and selected without truth. The minimum number of candidates at least `0.05`
below the best is three rather than four. This excludes nearly flat packets while allowing a valid
choice set with five scientifically near-optimal variants; continuous regret remains primary. The
old hash-split block is retained as development evidence and is not relabelled.

Reclassification of the retained 16-query truth under the maximin rule passes the candidate gate
in `15/15` development worlds without new provider or physics calls. Minimum candidate score range
is `0.598` for electrochemistry, `0.275` for crystallization and `0.195` for reaction safety. The
first disjoint-oracle attempt, fitted only on the eight remainder queries, is rejected: just `3/15`
worlds reach Spearman `rho >= 0.80` and only `1/15` recovers the true Top-1. These eight points are
therefore insufficient to operationalize a correct oracle. A denser registered provider-free grid,
still disjoint from terminal candidates and fitted without candidate outcomes, is required before
the oracle condition or any provider session is authorized.
