# ICLR 2027 submission checklist

Updated: 2026-09-03. Recheck the official
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
| W2-58 runner-derived-status B3 | Terminal DeepSeek interface canary 0/3; GPT unstarted | Three rc=0 post payloads reused the pre shape despite the required post schema; no scientific or cross-model denominator |
| W2-59 main-evidence completion | Terminal block-specific coverage | A-P/B2 complete matched DeepSeek + GPT formal; GPT C2 and W2-50 stop after in-denominator triplets; B3 formal 0/30 per provider |
| W2-60 DeepSeek low reasoning | B2 formal 15/15; A-P platform-defective partial | Same-harness B2 robustness: all 15 low error, misindexed exact law 0/5, contrast -0.0405; low is not reasoning-off |
| W2-61 four-condition action successor | Terminal dual-model failure-aware surface | Four conditions and 180 scheduled slots per model; autonomous value is directional, portable-law benefit is unstable, and yoked failures preclude a pure experiment-selection effect |
| W2-62 Codex C2 full-cohort successor | Terminal 135-cell scheduled surface | Completes dual-model C2 coverage; Codex has lower law/compression error but neither model has blind action gain or passes selective correction |
| W2-63 DeepSeek B3 full-cohort successor | Terminal 30-cell failure-aware surface | Completes dual-model B3 coverage; retain 13 DeepSeek schema failures and do not infer a model ranking |

W2-51 and W2-52 are terminal results, not unfinished submission blockers. Their original
five-condition participant cohort remains unexecuted and must not be reconstructed retrospectively.
The independent W2-61 successor removes the oracle arm and supplies four-condition action readouts.
Every participant-bearing main evidence block now has a DeepSeek and GPT-5.6-sol/Codex scheduled
surface: A-P and A-S B2 have complete matched formal denominators; C2 has 135 scheduled cells per
model, B3 has 30 per model, and W2-61 has 180 condition slots per model. Failures remain in the
denominators, so this is dual-model coverage rather than all-cell completion or a model leaderboard.
W2-58 is terminal rather than pending paper evidence: DeepSeek produced six completed provider turns,
but all three sessions failed the frozen post-action schema; GPT and both formal blocks remained
unstarted. It must not appear in figures, effect estimates or model comparisons.
W2-60 adds one complete structural matched-evidence denominator, bringing valid matched formal
sessions to 75. Its A-P low block remains 0/15 formal and is reported only as a platform boundary.

## Nine-page integration target

| Section | Target pages | Required content |
|---|---:|---|
| Introduction | 1.0 | Endpoint ambiguity, five-stage capability chain, contributions |
| Environment and evaluation | 1.5 | Persistent loop, interventions, prediction/law/action readouts |
| Experimental programme | 1.0 | Independent units, denominators, failure and stop rules |
| Prior-conditioned discovery | 1.5 | Task heterogeneity, within-session learning, law fidelity |
| Evidence to laws | 1.0 | Matched evidence and structural-recovery boundary |
| Laws to actions | 1.0 | W2-50 selection, W2-61 four-condition contrasts and law--action separation |
| Evaluator alignment | 0.8 | W2-51/W2-52 qualification and W2-53 diagnostic |
| Related work | 0.6 | Scientific agents, active experimentation and evaluation |
| Limitations and conclusion | 0.6 | Two fixed systems, differential failures, simulated chemistry, no oracle-arm participant estimate |

## Main display budget

1. Figure 1: endpoint ambiguity and the evidence-to-action chain.
2. Figure 2: intervention logic, loci and frozen denominators.
3. Figure 3: prior uptake, numerical learning and failed selective correction.
4. Figure 4: matched-evidence numerical convergence plus dual-model B3 structural/action control.
5. Figure 5: dual-model C2 selective correction, executable compression and blind action.
6. Figure 6: W2-61 four-condition action contrasts, W2-50 law--action relation and W2-53 evaluator alignment.
7. Table 1: exact denominators, evidence role and claim boundary.

The integrated action/evaluator figure uses W2-61 for participant-bearing four-condition readouts and
W2-53 for evaluator validity. W2-51/W2-52 qualification funnels and per-unit details remain in the
supplement. Never draw a participant-effect panel for the original five-condition cohort that was not
executed.

## Submission work

- [ ] Confirm the title, author list, author order and all OpenReview profiles before the abstract
  deadline.
- [ ] Confirm reciprocal-review eligibility and any author exemptions.
- [x] Import the official ICLR 2027 LaTeX style and establish an anonymous nine-page build.
- [x] Convert the current Markdown evidence narrative into the ICLR section budget above.
- [x] Build the six main figures and Table 1 from source data, with exact denominators and failures.
- [ ] Complete related work and citation verification.
- [x] Draft limitations, reproducibility, ethics and the mandatory AI-use statement.
- [x] Re-run claims-to-evidence, anonymity, page-count and rendered-PDF checks after W2-61/62/63 integration.
- [ ] Complete citation-source verification.

Current anonymous build: nine main-text pages and 15 pages total in anonymous review mode. The
W2-61/62/63 integration and dual-model Figure 5 pass stable-cross-reference, undefined-citation,
overfull-box, identifying-string and rendered-page checks. The complete-ranking table and Spearman
displacement explanation remain in the appendix. Citation-source verification remains open.

The canonical manuscript, story, display plan and evidence map are respectively
`paper/prior_discovery_manuscript.md`, `paper/prior_discovery_story_zh.md`,
`paper/prior_discovery_display_items.md` and `paper/prior_discovery_evidence_map.md`.
