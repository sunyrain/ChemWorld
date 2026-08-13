# Research findings

This page interprets the evidence without maintaining another result ledger.
See [Flagship experiments](flagship_experiments.en.md) for exact numbers and the
[authoritative current-status page](https://sunyrain.github.io/ChemWorld/benchmark_release/)
for release boundaries.

## Central narrative

ChemWorld does not ask only whether a model can optimize a black-box score. It asks:

> When an experimental world is partially observed, material identity is
> anonymous, priors may be right or wrong, and constitutive laws may change
> during a campaign, can an Agent form testable judgments from a limited
> experiment budget and update later actions when evidence disagrees?

Current evidence covers the first half of this chain: static optimization,
correct-information value, behavioral effects of a targeted wrong prior, and
environment-level mechanism identifiability. It does not yet establish complete
Participant detection, attribution, and recovery after an online law change.

## 1. Correct information can help, but its value is task-dependent

The anonymous-material three-arm experiment confirms positive information value
for electrochemistry while leaving crystallization inconclusive. This rejects
both “material information is always useless” and “correct attributes improve
every task.”

Information value depends on whether the attributes connect to controllable
variables, observations, budget, and the final decision. Future analyses should
therefore remain task-stratified rather than relying on one pooled mean.

## 2. Behavioral influence is not evidence of understanding

The wrong dossier changed early actions in both tasks, so the manipulation
entered the decision process. Yet both tasks failed the joint recovery rule for
different reasons:

- electrochemistry showed later action correction without practical performance
  recovery to the no-information arm;
- crystallization retained—and in these sampled worlds improved—performance,
  but lacked preregistered differential action correction.

Being influenced, avoiding a score loss, and identifying an error are distinct
claims. Recovery needs evidence that the manipulation mattered, behavior
corrected, and performance recovered.

## 3. No-information results need information-matched controls

Without a dossier, the Participant is above every information-matched classical
baseline in electrochemistry, but the comparison with privileged descriptor
calibration is unstable. In crystallization it is below simple LHS. Methods with
different information access do not belong in one undifferentiated leaderboard.

The results are formal descriptive evidence because the execution is complete
and auditable, while superiority thresholds and multiplicity were not
preregistered.

## 4. Environment identifiability is not Participant adaptation

Historical RC28 Gate A showed that candidate law families were identifiable
under controlled budgets and that a frozen reference policy could establish a
baseline, detect a change, and attribute it. That is an environment certificate,
not an Agent result.

The current-source binding is stale. Even after it is renewed, Participant Gates
B–E are required to test whether a model detects a change, distinguishes its
family, updates experiments, restores performance, and transfers to held-out
conditions.

## 5. Strict rules preserve informative failures

Earlier Safe-GP diagnostics improved objective, safety, and cost on several tasks
but failed a joint claim when one preregistered practical-effect threshold was
missed. Earlier RL diagnostics exposed action-coverage, reward, and workflow
completion problems rather than a reliable scaling law.

Those results are not current rankings. Their methodological value is that a
failure remains attached to a named criterion instead of disappearing through a
metric swap, task removal, or post-hoc threshold change.

## 6. One autonomous scaffold is not a cross-task constant

The five-task development campaign holds the neutral prompt, model, and budget
fixed. Codex is above the best classical method mean in electrochemistry and the
new reaction–distillation task, clearly below it in crystallization and
continuous flow, and close but below the frozen threshold in partition. A single
flagship score therefore cannot represent general autonomous experimental
optimization.

In continuous flow, the best explored conditions were already weak, so the
failure is not merely a final-synthesis selection error. A useful next
Participant should test access to generic numerical-search tools rather than
receive task-specific hidden hints.

## Supported and unsupported claims

Supported:

- ChemWorld can execute and audit multi-world experiments with anonymous
  materials, finite budgets, blind validation, and exact replay.
- Two flagship tasks have formal descriptive Participant results.
- A five-task development comparison is complete and shows strong task
  heterogeneity for one shared Codex strategy.
- Correct material information has positive value in electrochemistry, with
  clear task heterogeneity.
- A targeted wrong prior affects behavior, but general recovery is not shown.

Unsupported:

- broad SOTA for Codex or any provider;
- pooling task-specific absolute scores into one cross-task ranking;
- Participant mechanism discovery or online mechanism adaptation;
- interpreting the crystallization wrong-dossier benefit as error discovery;
- transfer from the simulator to real chemical systems.

## Highest-value next evidence

The next phase should stabilize the Participant method, execution, and
statistical contracts with focused development checks. Once that surface is
stable and release freeze is explicitly authorized, rebuild Gate A's
current-source binding once and execute Gates B–E without further design
changes. That closes the missing feedback-correction and online-recovery
segment of the narrative instead of adding more static score tables or
rebuilding source certificates after every development edit.
