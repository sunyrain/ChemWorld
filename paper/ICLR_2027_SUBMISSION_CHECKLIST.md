# ICLR 2027 submission checklist

Updated: 2026-08-31. Recheck the official
[Call for Papers](https://iclr.cc/Conferences/2027/CallForPapers),
[Author Guidelines](https://iclr.cc/Conferences/2027/AuthorGuidelines),
[Dates](https://iclr.cc/Conferences/2027/Dates) and
[AI Policy for Authors](https://iclr.cc/Conferences/2027/AIPolicyForAuthors) before submission.

## Format contract

- Use the official ICLR 2027 style files and anonymous review mode.
- Limit the review manuscript to nine pages of main text; references and the appendix follow the
  current official rules.
- Keep author names, affiliations, acknowledgements and identifying repository links out of the
  anonymous PDF and supplementary material.
- Report internal task IDs, seeds, run roots, hashes and repository filenames only in evidence records,
  not in reader-facing prose or figures.
- Include the required AI-use statement and a reproducibility statement outside the main-text page
  budget when the official format permits.
- Keep code/data availability wording anonymous during review and replace it only for camera-ready.

## Current scientific status

| Evidence block | Status | Main-paper role |
|---|---|---|
| Public participant and evaluator | Complete | Prior-conditioned search, prediction and law fidelity |
| Matched evidence | Complete | Acquisition, numerical revision and structural identification |
| W2-50 fresh open action | Complete | Descriptive unseen-plan selection: 11/42 Top-1 |
| W2-51 96-query control | Terminal scientific rejection | No participant causal contrast; report the stop boundary |
| W2-52 320-query control | Construction pass; prospective rejection | Separate exposed repair from fresh generalization |
| W2-53 gate--action alignment | Complete diagnostic | Complete ranking and action validity are different estimands |
| W2-54 matched extension | Development-only, yoked right-censored | Do not use as a causal or arm-level result |
| W2-55 reviewer controls | Complete, zero provider calls | Schema capacity plus continuous and threshold-sensitive law--action analysis |
| W2-56 replicated B3 | DeepSeek canary rejected; GPT formal 30/30 complete | Provider-specific structural/action control; no cross-provider leaderboard |
| W2-57 shared-index B3 | Terminal DeepSeek canary 2/3; GPT unstarted | Retained interface failure, not a scientific or cross-model denominator |
| W2-58 runner-derived-status B3 | Terminal DeepSeek canary 0/3; GPT unstarted | Retained participant-schema rejection; no scientific or cross-model denominator |

W2-51 and W2-52 are terminal results, not unfinished submission blockers. The unexecuted
five-condition participant cohort remains a limitation. The paper contains DeepSeek and GPT-5.6-sol
evidence at programme level, but no evidence block has complete matched formal denominators for both;
the GPT B3 result remains provider-specific.
W2-58 is terminal rather than pending paper evidence: DeepSeek produced six completed provider turns,
but all three sessions failed the frozen post-action schema; GPT and both formal blocks remained
unstarted. It must not appear in figures, effect estimates or model comparisons.

## Nine-page integration target

| Section | Target pages | Required content |
|---|---:|---|
| Introduction | 1.0 | Endpoint ambiguity, five-stage capability chain, contributions |
| Environment and evaluation | 1.5 | Persistent loop, interventions, prediction/law/action readouts |
| Experimental programme | 1.0 | Independent units, denominators, failure and stop rules |
| Prior-conditioned discovery | 1.5 | Task heterogeneity, within-session learning, law fidelity |
| Evidence to laws | 1.0 | Matched evidence and structural-recovery boundary |
| Laws to actions | 1.0 | W2-50 selection and law--action separation |
| Evaluator alignment | 0.8 | W2-51/W2-52 qualification and W2-53 diagnostic |
| Related work | 0.6 | Scientific agents, active experimentation and evaluation |
| Limitations and conclusion | 0.6 | Single system, simulated chemistry, no five-condition estimate |

## Main display budget

1. Capability chain and study map.
2. Prior-conditioned discovery.
3. Phenomenological interpolation versus structural recovery.
4. Agent law--action decoupling and evaluator rank--action misalignment.
5. Table 1: exact denominators, evidence role and claim boundary.

The integrated action/evaluator figure uses the available main-text space for compact W2-51/W2-52
qualification funnels; per-unit details remain in the supplement. Never draw a participant-effect
panel for conditions that were not executed.

## Submission work

- [ ] Confirm the title, author list, author order and all OpenReview profiles before the abstract
  deadline.
- [ ] Confirm reciprocal-review eligibility and any author exemptions.
- [x] Import the official ICLR 2027 LaTeX style and establish an anonymous nine-page build.
- [x] Convert the current Markdown evidence narrative into the ICLR section budget above.
- [x] Build the four main figures and Table 1 from source data, with exact denominators and failures.
- [ ] Complete related work and citation verification.
- [x] Draft limitations, reproducibility, ethics and the mandatory AI-use statement.
- [x] Run claims-to-evidence, anonymity, page-count and rendered-PDF checks.
- [ ] Complete citation-source verification.

Current anonymous build: 9 pages of main text and 14 pages total in the official ICLR 2027 style,
with zero LaTeX errors, undefined citations, overfull boxes or direct identifying-string leaks. The
combined law/action/evaluator display is integrated from machine-readable W2-50--W2-55 sources. The
claims-to-evidence, anonymity, page-count and rendered-PDF passes are complete; citation-source
verification remains open.

The canonical manuscript, story, display plan and evidence map are respectively
`paper/prior_discovery_manuscript.md`, `paper/prior_discovery_story_zh.md`,
`paper/prior_discovery_display_items.md` and `paper/prior_discovery_evidence_map.md`.
