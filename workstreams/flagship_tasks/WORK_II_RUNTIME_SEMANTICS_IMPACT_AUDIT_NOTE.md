# Work II runtime-semantics static impact audit

This audit asks which existing Work II evidence blocks may depend on two corrected runtime
semantics: destructive instruments observing post-withdrawal state, and catalyst category modifying
reaction rates without a positive catalyst charge.

The audit is outcome-blind in its classification logic. JSON containers may contain historical
outcomes, but classification uses only artifact bindings, hash kinds, task identifiers, execution
denominators and operation metadata; it does not inspect, compare or reinterpret scores, scientific
effects, arm contrasts or participant recommendations. A committed or planned destructive measurement is `affected`. A reaction operation
without a preceding positive catalyst charge is `affected`. Missing, unreadable or hash-drifted action
bindings are `unknown`. Only fully inspectable trigger-free execution evidence, or non-execution
administrative artifacts, can be `unaffected`.

Planned denominators and planned cells are not execution evidence. Administrative and release
artifacts propagate `affected` or `unknown` fail-closed only when a recursively bound artifact contains
a trigger, a binding is missing or hash-inconsistent, or an actual completed/attempted/committed
execution summary has no recoverable action trace. Each report row records this distinction in
`classification_basis` and lists the concrete `execution_evidence_sources`.

The machine report must remain `pending_requalification` whenever any report is `affected` or
`unknown`. It cannot authorize formal execution or mark requalification complete. This audit does not
run a provider, replay an experiment, or create a new scientific outcome.

The independent validator checks the embedded self-hash, summary and per-artifact denominators,
summary status, fixed outcome-blind/provider/formal fields, and every classification-to-required-action
and classification-basis mapping.

Default discovery covers both current `work-ii-*.json` reports and the two retained Work II evidence
blocks whose historical filenames begin with `static-s0-`: the three-arm material-information result
and the five-task postqualification development result.
