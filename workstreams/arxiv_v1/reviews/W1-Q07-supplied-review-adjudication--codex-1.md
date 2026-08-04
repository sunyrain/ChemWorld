# W1-Q07 supplied-review adjudication and closure matrix

> **Internal/editor master. Not reviewer-facing.**

- Owner: `codex-1`
- Decision in supplied report: **Major Revision**
- Task mode: manuscript revision plus internal adjudication
- Reviewed baseline: `23d333754cd1e86bc5e70b74adcefc48d050fd42`
- Supplied report SHA-256: `b7996be0ea7d3947429ad195446ab3d731805a44b7bdcd629f08e6913d387e89`
- Revised surface: `paper/experimental_intelligence_v1_manuscript.md`
- Paper I posture: programmable-world scientific-instrument release
- Paper II posture: causal, mechanistic and adaptation study of agent behavior
- Package readiness: **first-paper text ready after one package rebuild; the broader Major-Revision evidence programme remains incomplete**

## Adjudication principle

The review correctly identifies that the strongest current evidence concerns instrument
semantics, observability, accounting and replay. The revision therefore does not defend a
broad latent construct of agency or expand selected examples into a population survey.
It narrows the title and measured object to an operational experimental-process profile,
discloses complete-system prompt and interface confounding, treats the 6/36 latent result
as an unqualified module, and makes task, protocol, statistical, chemistry and
reproducibility boundaries directly auditable.

New crossed-agent experiments, independent construct validation, broad primitive-control
coverage and physical bridging are scientifically valuable. They answer explanatory or
external-validity questions beyond the first instrument release. They are not represented
as completed in this revision.

## Major-comment closure matrix

| ID | Reviewer concern | Classification | Action | Work status and verification | Residual issue | Blocks Paper I? |
| --- | --- | --- | --- | --- | --- | --- |
| R1.1 | The deterministic policies are self-confirming and do not establish broad construct validity for “experimental agency”. | evidence / interpretation, major | `SOFTEN_CLAIM` + `ACCEPT_TEXT` | `VERIFIED_DONE`. Title, Abstract, Introduction, Section 4, Discussion, Methods 10.3, Conclusion and Appendix C now use experimental-process profile as the measured object. Section 4 states that the policies qualify logging and metric computation, not a universal construct. | Independent policy authors, blind expert ratings, adversarial endpoint-matched policies and stochastic test-retest remain future validity studies. | No, after claim narrowing. Yes for any broad agency-validity claim. |
| R1.2 | The two complete systems confound model, scaffold, prompt, interface, session and retry behavior. Assay and discard may be asymmetric. | methodological, major | `PARTIAL` + `SOFTEN_CLAIM` | `VERIFIED_DONE`. Sections 5 and 10.5 now list matched and unmatched fields, disclose the different prompt surfaces, state the terminal-action asymmetry, and deny model-preference or causal-backend inference. | Same-model crossed-scaffold, same-scaffold crossed-model and prompt/menu ablations were not run. These belong to Work II if causal attribution is pursued. | No for an instrument capability demonstration. Yes for a model or scaffold effect claim. |
| R1.3 | Formal empirical coverage is narrow relative to 15 registered tasks. | evidence / scope, major | `ACCEPT_TEXT` + `PARTIAL` | `VERIFIED_DONE`. Appendix D now gives a 15-task coverage matrix distinguishing boundary qualification, forks, known policies, compiled campaigns, primitive control, replay and Work I statistics. Introduction and Discussion keep the formal subset explicit. | Primitive-control complete-system evidence remains limited to electrochemical conversion. Broader randomly sampled task families are future generalization evidence. | No for the registered instrument surface. Yes for cross-task prevalence or universality. |
| R1.4 | The 6/36 latent audit is an instrument defect, not merely a rigor demonstration. | methodological / integrity, major | `SOFTEN_CLAIM` + `ACCEPT_TEXT` | `VERIFIED_DONE`. Sections 5, 9.2 and 10.6 call the counterfactual module unqualified, explain that 36/36 preflight executed no replacement assay, list 11 prefix, 18 resource and one precondition failures, and require a new cohort after repair. | The module is not repaired or rerun. The frozen failure remains historical evidence. | No because no latent-quality point claim remains. Yes for counterfactual-terminal capability. |
| R1.5 | Preregistration, commit freeze and post-launch outcome-blind decisions are conflated. The launcher restart and extension stop require a timeline. | protocol / reporting, major | `ACCEPT_TEXT` | `VERIFIED_DONE`. Methods 10.13 defines repository preregistration, commit freeze and outcome-blind analysis freeze, denies third-party trusted registration, and records the restart, visible data, source commits, deviation and owner scope stop. | Repository timestamps are public version-control evidence, not a registered-report service. | No after explicit terminology and deviation disclosure. |
| R1.6 | Bootstrap interval meaning is unclear for ten fixed worlds, and censoring may relate to trajectory complexity. | statistical, major | `ACCEPT_TEXT` + `CLARIFY_EXISTING` | `VERIFIED_DONE`. Section 6 makes all ten paired differences primary. Methods 10.4 defines bootstrap output as finite-set resampling sensitivity, not a confidence interval. Sections 8 and 10.8 deny missing-at-random censoring and retain incomplete pairs. | No superpopulation inference or high-powered selected-world conclusion is available. Exact sign summaries and leave-one-world-out ranges remain in the public sensitivity artifact. | No for finite-world descriptive claims. |
| R1.7 | Chemistry-domain validity is weaker than software semantics and needs model-type and validity boundaries. | domain validity / scope, major | `CLARIFY_EXISTING` + `ACCEPT_TEXT` | `VERIFIED_DONE`. Discussion 9.2 now identifies equation-based and reference-checked runtime families, explains maturity labels and preserves model-card, synthetic-instrument and no-physical-calibration boundaries. | Wet-lab, high-fidelity simulator comparison and independent physical-domain review remain future bridge studies. | No for a virtual instrument. Yes for physical predictive or deployment validity. |
| R1.8 | Reproducibility is incomplete without raw-byte archive access, provider bodies and immutable model versions. | data / code, major | `PARTIAL` + `ACCEPT_TEXT` | `VERIFIED_DONE` for disclosure. Section 11 separates numeric/figure regeneration, environment replay and stochastic decision reproducibility, and states exactly what a third party can and cannot verify. | The 17.7-GB roots have no durable identifier; unrestricted provider bodies and hidden identities remain excluded; alias drift remains possible. | No for the scoped arXiv instrument release. Yes for full raw-provider independent audit. |

## Minor-comment closure matrix

| ID | Reviewer concern | Action | Work status and verification |
| --- | --- | --- | --- |
| R1.m1 | Abstract is count-heavy and obscures the main line. | `ACCEPT_TEXT` | `VERIFIED_DONE`. Abstract now states one problem, the instrument contribution, representative qualification and failure results, then the claim boundary. |
| R1.m2 | Qualification and freeze vocabulary is repetitive. | `ACCEPT_TEXT` | `VERIFIED_DONE`. Table 1 carries the recurring evidence-layer boundary; prose now uses the specific term only where timing or gate status matters. |
| R1.m3 | All 19 profile metrics need definitions and ranges. | `ACCEPT_TEXT` | `VERIFIED_DONE`. Appendix C gives every metric, denominator, range and null rule and binds the authoritative contract hash. |
| R1.m4 | G0 and G2 lack intuitive definitions. | `ACCEPT_TEXT` | `VERIFIED_DONE`. Methods 10.4 and Data Availability define compiled-control (`G0`) and primitive-control (`G2`) on first use. Current display-item headings do the same. |
| R1.m5 | Some figure annotations are too small. | `CLARIFY_EXISTING` | `VERIFIED_DONE` against the accepted P09 figure repair and the current arXiv package. No new figure rendering was required by this adjudication. |
| R1.m6 | The title overstates agency measurement. | `ACCEPT_TEXT` | `VERIFIED_DONE`. New title is “ChemWorld: A Programmable Virtual Instrument for Measuring Experimental Process Profiles”. |

## Direct answers to the reviewer's six questions

1. **Same model under different scaffolds.** This experiment was not run, so no
   significance claim exists. The all-assay pattern cannot be separated from prompt and
   scaffold effects in Paper I. A crossed design is a Work II requirement if the authors
   want causal attribution.
2. **Why 36/36 preflight became 6/36 formal.** Preflight reconstructed identities and
   ledgers but executed zero replacement assays. The formal evaluator added terminal-
   replacement and resource-entry integration, where 11 prefix, 18 resource and one
   precondition failure appeared. Thus the narrow preflight passed and the integrated
   module failed.
3. **Which of 15 tasks received agents.** Appendix D gives the complete matrix. Five tasks
   have audited compiled-participant campaigns, two contribute formal compiled statistics,
   and only electrochemical conversion has primitive-control complete-system evidence.
4. **Was preregistration publicly timestamped.** Relevant protocols and hashes were pushed
   before their stated formal outcomes, but no third-party preregistration or trusted-
   timestamp service is claimed. The post-launch trajectory rule is now labelled an
   outcome-blind analysis freeze.
5. **What can be verified without 17.7 GB and provider bodies.** A third party can regenerate
   paper numbers and figures from tracked derived data, inspect the contracts and hashes,
   and exactly replay released simulator trajectories and resource ledgers. It cannot
   independently inspect every raw provider response, reconstruct hidden evaluator bytes,
   or recompute the four raw-root hashes without the raw bytes.
6. **What chemistry correctness was tested.** The backend uses scoped equation-based and
   reference-checked runtime modules with units, invariants, diagnostics, maturity metadata
   and model-card failure domains. This supports virtual chemical semantics within those
   domains. It does not establish universal predictive accuracy, wet-lab calibration or
   deployment safety.

## What should happen next

### Close in Paper I

- Keep the new instrument title and experimental-process terminology.
- Keep the complete-system runs as capability demonstrations only.
- Keep the 6/36 counterfactual result as a failed qualification with no latent point claim.
- Keep Appendix C, Appendix D, the timeline and the three reproducibility levels.
- Rebuild the arXiv package once and inspect only pages affected by the new tables.

### Move to Paper II

- Cross model, scaffold, prompt and interface while holding the other factors fixed.
- Test why assay, discard, evidence acquisition and continuation policies change.
- Use additional worlds and complete systems to estimate heterogeneity and adaptation.
- Add independent or adversarial profile-validity evidence if the broader agency construct
  becomes a central claim.

### Future instrument validation, only if the stronger claims are desired

- Repair the discarded-state evaluator and run it on a new registered cohort.
- Add primitive-control coverage across additional task families.
- Add calibrated high-fidelity or physical bridges for claims about real chemistry.
- Deposit raw roots under a durable identifier if full raw-byte external audit becomes a
  publication requirement.

## Chinese author check

- 第一篇现在只承诺“世界和仪器能让完整智能体自主运行、被观测、被记账和被重放”。
- 第一篇不再承诺已验证普适的“实验能动性”构念，也不解释两个系统为何产生不同终止行为。
- `6/36` 被定性为模块资格失败。保留它是为了公开失败边界，不把它包装成能力成果。
- 如果投稿目标要求模型归因、跨任务普适性或物理化学真实性，必须补新实验；这些不是改文字能关闭的问题。
