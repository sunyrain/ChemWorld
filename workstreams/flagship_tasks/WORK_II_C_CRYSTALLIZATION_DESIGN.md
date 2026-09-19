# Work II: crystallization research design

Status: user authorized the development pilot on 2026-09-19; execution is governed by the [concise pilot note](WORK_II_C_PILOT_NOTE.md). The [English report](reports/work-ii-c-sol-pilot-20260919/REPORT.md) distinguishes preparation and model sources. This develops the C entry in [the experiment matrix](WORK_II_EXPERIMENT_MATRIX.md), section 9.10, without changing historical qualification or EC/PA results.

## 1. Scientific question and primary task

Can an agent use a small experimental budget to identify how material choice and process history affect crystal recovery and quality, and use that knowledge to recommend and predict a process?

The proposed first task is **maximize seed-excluded product recovery subject to public purity and fines constraints**. The agent controls the reaction-to-crystallization process; mechanism explanation and predictions follow the same source campaign. Do not split the first pilot into separate discovery and optimization campaigns. Such a comparison would require its own later design; this pilot cannot establish the causal effect of the research goal.

This task makes history relevant: two batches with the same final temperature can have different particle populations because their seeding, cooling, holding and reheating histories differ. Upstream conversion and impurity content also influence what can be recovered downstream. These are hypotheses and capabilities to investigate, not assumed agent failures.

Proposed initial quality constraints are purity >= 0.80 and number fraction of fines below 20 micrometres <= 0.50. A seed-excluded recovery of 0.10 is the initial feasibility target, not a ceiling on optimization. These values come from the previous full-process development task and require a feasible reference under the exact new material/physics combination before the pilot starts. If that combination is infeasible, diagnose and revise the draft before any agent source; do not relax thresholds after observing agent outcomes.

Evaluate quality feasibility and net recovery separately. Among quality-feasible recommendations, higher net recovery is better; an infeasible recommendation retains its measured purity, recovery and fines and is reported as infeasible. Do not replace this objective with an unrelated native composite score or combine the mechanism grade with product quality.

## 2. Actual laboratory and accounting

Implementation bindings for the proposed pilot:

- Native task: `reaction-to-crystallization`.
- Full-process contract: `phase-resolved-process-v5`, retaining v4 particle-population continuity, thermal redissolution and seed provenance while allowing measurement allocation without compulsory pre-seed/pre-filter assays. The original v4 draft failed the actual execution check; v4 behavior remains available for historical consumers.
- Material family: `reaction-crystallization-latent-materials-v1`, explicitly selected rather than the legacy default.
- First world: the existing C-W01 reference setting, with fixed world residuals. The combined contract still needs a local feasibility check; older C-W01 results do not prove this new combination is qualified.

Within public operation bounds the agent can choose anonymous catalyst and solvent, charges, reaction conditions, quenching, seed addition, cooling stages and durations, holding, reheating/redissolution, recooling and filtration. No fixed upstream recipe, compulsory seed dose or prescribed sequence is supplied. The fixed recipes in old C qualification were reference interventions, not restrictions on an autonomous researcher.

| Observation | Meaning and cost |
| --- | --- |
| HPLC | Composition under the public sample-preparation contract; consumes sample. It does not measure particle size. |
| Online `particle_size` | Available after crystals exist under the full-process contract; nondestructive, 120 seconds, cost 0.04. Returns the noisy bounded size index min(number-weighted d50 / 250 micrometres, 1), CSD quality and fines fraction below 20 micrometres. |
| Final assay | Terminal batch outcomes, including crystal quality and recovery. It is distinct from an extra intermediate measurement. |

Solids and mother liquor form the declared representative analytical slurry group; the interface does not provide arbitrary independent sample bottles. d50 and fines must both be evaluated: a large median alone does not establish an acceptable fine-particle tail. Conditions without crystals require an explicit absence/undefined-size outcome, not a fabricated zero-size prediction.

The net-recovery numerator excludes retained material originating from purchased seed. Use the original reactant-charge denominator specified by the full-process public contract, preserving sample withdrawals and material provenance through dissolution, recooling and filtering. Record seed consumption and cost separately. Verify these definitions in actual final tool responses, rather than inferring them from a historical field name such as `crystal_yield`.

## 3. Three prior arms

All arms share physics, actual action-to-material mapping, world residuals, operations, instrument noise rules, budgets, task instructions and held-out questions. Only the supplied material dossier changes. Arm labels, real chemical identities, hidden constants and host paths are not participant inputs.

| Arm | Supplied information |
| --- | --- |
| Opaque | Anonymous catalyst C0-C3 and solvent S0-S3 catalogue plus common laboratory, measurement and task definitions; no instance property dossier. |
| Aligned | The same catalogue plus nominal catalyst reference-reaction properties and solvent reference-reaction, relative solubility, nucleation, growth and impurity-occlusion properties. |
| MisIndexed | The same kind and amount of information as Aligned, with the S1 and S3 dossier entries exchanged; catalyst entries remain unchanged. Actual materials and physical actions are not exchanged. |

The existing C-E solvent permutation is `[0, 3, 2, 1]`. Dossier values are family-level nominal properties before hidden, fixed world residuals. They are incomplete prior evidence, not an exact world equation or guaranteed ranking at every condition. A locally inaccurate nominal prediction does not by itself prove the agent has identified a label swap.

Start with E only. Old C-P numerical bands cannot be transplanted into a contract with a different recovery denominator, and the old C-S qualification did not establish the proposed structural distinction. Neither is needed to investigate this first C-E task.

## 4. Source and follow-up flow

Proposed first coverage: one world x one task x E x three arms, GPT-5.6 Sol / medium, one source attempt per arm. Participant prompts, questions and generated reports are English.

Each source receives **12 batch slots, 12 freely allocated extra instrument calls and 12 final assays**. The extra measurements are a shared HPLC/particle-size allowance, not 12 calls to each instrument and not a mandatory one-per-batch allocation. The agent may work sequentially or group experiments, inspect feedback and revise freely. No mandatory reflection after every batch and no advance batch-group plan are imposed. Scientific failures consume their attempted slots and remain in the ledger.

Operation capacity and stock must support multi-stage trajectories across all 12 batches. Before launch, set and disclose the concrete capacity using the longest reference trajectory as a check; do not confuse the native 72-operation limit with 12 complete experiments. Record process time rather than accidentally treating the historical single-batch 100-hour envelope as the entire campaign allowance. Provider wall time and token limits are separate, explicit execution resources.

1. **Source research:** perform up to the declared 12 batches and allocate the measurements autonomously. The broad later prediction domain is disclosed, but the exact held-out recipes and outcomes are withheld.
2. **K1, sealed before Q:** give a free mechanism account, evidence from particular batches, uncertainty and competing explanations. Select one completed batch as the recommended process. If no observed batch satisfies quality constraints, report that explicitly and still identify the best available candidate with its limitations. No equation template or candidate-mechanism menu is required.
3. **Q:** answer one fixed set of 12 complete held-out process conditions, with point estimates and 80% intervals for seed-excluded recovery, purity, d50 and fines where defined. Provide paired directions/decisions and a concise common rationale. No new laboratory access or truth feedback.
4. **K2:** answer the three retrospective questions below on the same thread. K1 and Q remain sealed.
5. **Host evaluation:** exact replay checks the retained trajectory. Independently replay the selected recorded process with a predeclared new observation-noise seed, including its sampling operations, and score its outcomes. Keep reference, replay and recommendation-retest costs separate from the 12 source batches. Replaying recorded actions does not validate a general feedback-dependent policy, and measurement-noise replication alone does not establish physical robustness.

K1, Q and K2 each use the repaired public calculator policy: **128 attempts per stage**, shared by scalar and array expressions; invalid expressions count. Every reply reports remaining attempts. At exhaustion the calculator rejects new computation but the agent can still submit an answer within the response deadline. Save and pass the same policy to both the calculator and launcher. The new EC/PA entries already support this; the C runner still needs integration.

This pilot comprises **3 source campaigns, 36 planned source batches and 9 follow-up stages**. The Q conditions are host reference experiments, not extra experiments available to the agent. They are shared across arms. Source replay and the 3 planned recommendation retests are additional physical work; unusable recommendations remain explicit missing retests rather than replacement candidates.

## 5. Proposed held-out contrasts

Use six paired contrasts, two complete recipes per pair. The following is a coverage proposal, not an already executable or frozen question set. Exact legal actions, values, units and interval definitions must be saved before agent outcomes. Prediction recipes must specify the full upstream history and sampling actions as well as downstream conditions.

| Pair | Contrast | Question tested |
| --- | --- | --- |
| 1 | S1 versus S3 with the same other conditions | Does the learned material account predict observed solvent effects beyond the supplied nominal dossier? |
| 2 | Lower versus higher seed dose, other conditions matched | Can the agent distinguish seed addition from newly recovered product and predict the particle/recovery tradeoff? |
| 3 | Slow cooling versus fast cooling plus a hold, same end temperature and total scheduled duration | Does it account for cooling history beyond final temperature? |
| 4 | Monotonic cooling versus reheating/recooling, matched final temperature and total scheduled duration | Does it retain the consequence of an earlier particle population and partial dissolution? |
| 5 | Filter at a specified state versus continue a specified growth stage and then filter | Can it predict the quality/recovery consequence of continuing? Explicitly report the extra time and cost; this pair need not have equal resource use. |
| 6 | A defined upstream composition/loading change versus its reference, matched downstream schedule | Does the downstream account generalize beyond one feed history? |

Report per-metric prediction error, interval coverage and width, and pairwise ordering/quality decisions. Keep true process outcomes separate from noisy instrument observations; specify which is the prediction target. Freeze any metric normalization with the reference design, not using the agent's errors. Pairs with effects below the declared measurement resolution are reported as indistinguishable rather than forced into a directional win/loss. These observational contrasts test predictive consequences; they need not uniquely identify a microscopic law.

The three K2 questions, in participant-facing form:

1. Which of your main claims are supported, contradicted, or still untested by your experiments? Cite the relevant batches and distinguish direct observations from interpretation.
2. If allowed one additional experiment, what would you do, which competing explanations would it distinguish, and what different outcomes would you expect?
3. Which observation did your final account use least effectively, and which of your held-out predictions is least reliable? Explain why without changing the sealed answers.

## 6. Interpretation and the small pre-launch check

Analyze three linked but separate outcomes: material-prior use and revision; history-dependent mechanism/prediction quality; and delivery of acceptable crystals. A high-quality product with weak predictions is a possible dissociation to inspect, not proof of information loss. Failure despite an attempted repair also differs from failure to acquire the relevant observation. Trace explicit actions, measurements and claims without pretending the transcript reveals all internal reasoning.

If a later LLM judge is used, ground each mechanism assessment in cited evidence and host-valid interventions, allow equivalent explanations and justified uncertainty, and calibrate the judge separately. Fluent prose is not a substitute for held-out prediction or delivery. A single-world, single-attempt pilot establishes execution and examples, not a systematic cross-world effect.

Before this pilot, answer only four practical questions:

- **Does the actual public interface match the brief?** Check material anonymity, dossier delivery, online particle measurement, units, sampling and final metrics with the chosen v4 + latent-material combination.
- **Is the task meaningful and feasible?** Run a small predeclared reference block containing a feasible process and the proposed contrasts, using the same physics. Existing full-process references include 4 feasible C candidates out of 24 tested, but do not establish feasibility under this new combined setting.
- **Do the arms differ only in information?** Compare actual public inputs and replay identical actions in O/A/M; do not alter the physical material mapping for MisIndexed.
- **Can the full chain finish and be scored?** Check the 12-batch resource card, saved questions, same-thread K1/Q/K2, calculator policy, recommendation extraction, replay and readable failure/accounting output.

The source/follow-up adapter and exact reference recipes are implemented in `scripts/run_work_ii_c_pilot.py`; the pilot note records startup, material-anonymity and measurement-order corrections before model launch. Reuse compatible functional evidence; no new global source hash, release certificate or duplicate audit package is required for this development pilot. Read current completion counts from the report rather than treating implementation completion as experimental completion.

## Implementation references

- [Full-process contracts](../../src/chemworld/runtime/full_process_contract.py) and [crystallization services](../../src/chemworld/runtime/crystallization_services.py).
- [Anonymous dossiers](../../src/chemworld/materials.py) and [material families](../../src/chemworld/world/crystallization_material_family.py).
- [Existing full-process iteration](reports/work-ii-full-process-iteration-20260915.md) and [seed-continuity evidence](reports/work-ii-crystal-seed-continuity-20260915.md), resolved through the current evidence bindings.
- [Historical C qualification](experiment_1/systems/C/QUALIFICATION_SPEC_V1_0_1.md), for provenance; its recipes and prior numeric bands do not govern this new agent task.
