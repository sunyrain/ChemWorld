# Work II current-source Gate A requalification

Date: 2026-08-09. Status: frozen before execution; environment qualification only.

Question: Does the current ChemWorld executable source still satisfy the frozen RC28 A1 design,
A2 controlled matched identifiability and A3 online attainability contracts, without using any
participant-agent outcome or external provider call?

Coverage: retain the RC28 protocol, tasks, mechanism families, interventions, action library,
world cohorts, seed/noise namespaces, controlled budgets, online checkpoints, thresholds,
bootstrap, exclusions and stopping rules unchanged. Execute the complete A3 reference-policy
certificate and A2 controlled matched certificate from their first frozen units. Existing RC28
reports are immutable historical evidence; write all requalification reports and structural
receipts to new versioned paths.

Measurements: A1 design and semantics audit status; A2 completed trials, relation closure,
active-oracle and fixed-decoder controlled metrics at the frozen budgets; A3 completed trials,
reference sufficiency, detection, calibration, attribution and end-to-end metrics; trial-manifest
completeness; exact protocol/plan/report bindings; release qualification and public joint decision.

Pass/failure: pass only if current release qualification, design audit and semantics audit pass;
both A2 and A3 complete their exact frozen trial denominators and structural receipts; every frozen
gate threshold passes; the public decision binds the new reports and declares Gate A passed while
participant performance remains null. Any interruption or failed threshold is retained. No world,
budget, threshold or action may be changed in response to the result; an implementation repair
requires the affected requalification stage to restart from its first frozen unit.

Expected outputs: one A3 certificate and structural receipt, one compact A2/full-Gate-A report and
structural receipt, one release qualification, one public joint decision, resumable ignored trial
stores, a current-binding audit, and an updated `configs/current.json`. Raw trial stores remain
ignored; reader-facing records report exact denominators and all failures without private payloads.

Pre-execution design result (2026-08-09): the first RC28 current-source release qualification ran
123/123 focused tests and Ruff successfully and passed its source-commit check, but failed before
any A2/A3 trial because current task contracts changed the diagnostic relation graph content and
hash. The failed receipt is retained. RC29 therefore supersedes only the current-source bindings:
the scientific coverage, budgets, thresholds and stopping rules remain RC28-identical. Its
regenerated diagnostic graph contains three declared relations; sample-size, 25-check semantics and
full design audits pass with zero failures. A2/A3 remain unstarted until the RC29 preregistration and
release receipt bind a clean source commit.

RC30 amendment (2026-08-12): subsequent Work II runtime-semantics and formal-gate repairs changed
the executable source after RC29 certification. RC29 remains immutable historical evidence. RC30
retains the same scientific coverage, budgets, thresholds, stopping rules and zero-provider Gate A
question, but writes a fresh protocol composition, plan, audits, release qualification, A2/A3
reports, structural receipts and public decision. No RC29 artifact may be overwritten or relabelled.

Closeout (2026-08-14): RC30 stopped after seven zero-provider design/audit projections. It never
produced the required preregistration, release qualification, attainability certificate, A2/A3
receipts, public decision, provider data, or formal result, and it never became the current evidence
authority. Under the development-first/freeze-once workflow, these partial projections were retired
from the working tree and remain recoverable from Git. RC29 remains immutable historical evidence;
the stable final execution surface will receive one new qualification chain at release freeze rather
than continuing the RC30 audit treadmill.
