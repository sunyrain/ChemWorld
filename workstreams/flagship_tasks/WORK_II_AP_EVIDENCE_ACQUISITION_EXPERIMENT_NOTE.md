# Work II A-P controlled evidence-acquisition experiment

Status: frozen before provider-free packet construction or participant execution; reviewer-requested
causal follow-up independent of the completed Study B result.

## Question

Under an otherwise identical two-turn prediction protocol, does a participant with a wrong
parametric prior select diagnostic evidence when it is available, and does forced delivery of that
evidence separate acquisition failure from updating failure?

## Units and frozen coverage

- A-P electrochemical matched-prior task in the five registered public worlds.
- Initial-model arms `aligned_nominal` and `misindexed_nominal` only. Evidence conditions are
  `active_choice`, `forced_diagnostic`, and `forced_low_information`, producing 30 fresh two-turn
  sessions. Opaque is excluded because the causal estimand concerns selection and correction of an
  explicit directional prior.
- Turn 1 uses the same schema in every condition. It commits pre-evidence predictions and chooses one
  of three equal-size, label-blinded evidence bundles. Turn 2 returns the condition-assigned bundle
  and requests post-evidence predictions.
- Diagnostic and low-information bundles are frozen provider-free from development worlds. They are
  matched in row count, fields, numerical precision, ordering, and prompt length. Public truth and
  scoring queries are disjoint from evidence rows.

## Measurements

- Diagnostic-bundle selection rate by initial-model arm in `active_choice`.
- Pre/post prediction error and post-error convergence in all six arm-condition cells per world.
- Forced-diagnostic minus forced-low-information effect on final error.
- Active-choice shortfall relative to forced diagnostic, with the selected bundle retained.
- Public rejection or retention of the supplied parameter direction as a secondary typed outcome.

## Pass, failure and stop rules

- Provider-free qualification must show that the diagnostic bundle separates the registered
  directions and the low-information bundles do not, in all five development worlds.
- All bundles and scoring rosters are frozen before public truth or participant execution.
- Canary uses one world across all six cells and checks schema, bundle blindness, assignment, two-turn
  continuity, and denominators only. Canary outcomes are excluded.
- All 30 formal sessions are retained. Scientific/schema failures are never outcome-replaced.
- The experiment supports an acquisition bottleneck only if forced diagnostic reliably corrects the
  misindexed direction while active choice selects diagnostic evidence less often or leaves a larger
  post-error. Otherwise the acquisition claim is narrowed or rejected.

## Expected outputs

- Frozen bundle roster, provider-free qualification/public truth, 30 cell results, machine summary,
  Chinese report, and revised Paper 2 mechanism wording.

