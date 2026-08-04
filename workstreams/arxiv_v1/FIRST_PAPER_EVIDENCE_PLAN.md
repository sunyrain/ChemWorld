# First-paper evidence expansion plan

Status: **ACTIVE**  
Replaces: the task-driven Work I master TODO  
Scope: first paper only

## Paper contract

ChemWorld is a programmable virtual experimental instrument that lets complete agent
systems act autonomously in executable chemical worlds while their operations, evidence,
resources, failures and lifecycle decisions are observed and replayed. The first paper
qualifies this instrument and illustrates its measurements. It does not explain why an
agent produced a trajectory, attribute behavior to a model mechanism, or establish
physical-laboratory validity.

## Reader-facing terminology

| Canonical term | Meaning in the first paper | Do not use as a synonym |
| --- | --- | --- |
| programmable virtual instrument | the complete world, transaction, observation, resource and replay apparatus | benchmark alone; agent evaluator alone |
| experimental-process profile | the 19 separate operational measurements | intelligence score; universal agency construct |
| complete agent system | model, scaffold, prompt, tools and decision transport as deployed | model backend alone |
| compiled control | a complete experiment proposed in one structured submission | internal release labels |
| primitive control | stepwise typed operation selection inside a lifecycle | internal release labels |
| exact replay | deterministic reconstruction of simulator transitions and public records | reproduction of stochastic model tokens or a physical batch |

The manuscript and its figures must not expose repository filenames, hashes, commit IDs,
run IDs, internal task IDs, release labels, manifests or build-pipeline vocabulary. Those
remain available in internal evidence and release records.

## Evidence expansion decision

The best next revision is **comprehensive instrument qualification plus two targeted
validation experiments**. A broad agent-behavior study is not the priority for Paper I.

### 1. Cross-world infrastructure qualification — primary

Question: does the instrument preserve its declared semantics across the full registered
chemical-world surface?

- Exercise every registered task at valid midpoint and boundary conditions.
- Pair valid operations with invalid, resource-exhausted and precondition-failing probes.
- Verify units, mass/charge/energy constraints where applicable, transaction atomicity,
  resource reconciliation, lifecycle closure, public/private separation and exact replay.
- Report a task-by-property coverage matrix, exact tested denominators and every failure.
- Treat the task/world configuration as the independent unit. Operations and replay events
  are repeated observations within that unit, not independent samples.
- Use descriptive pass counts and failure classes; do not manufacture significance tests
  for deterministic contract checks.

This is the highest-value addition because it directly supports the paper's instrument
claim and answers the concern that formal evidence is narrow relative to the registered
surface.

### 2. Independent profile validation — primary

Question: can the experimental-process profile distinguish prespecified process
organization without relying only on policies designed around the metrics?

- Define policy behaviors independently of the metric implementation and freeze their
  expected qualitative signatures before decoding results.
- Include endpoint-matched policy pairs that reach similar final outcomes through
  different evidence-acquisition, continuation, resource-use or termination paths.
- Include at least one adversarial policy whose endpoint is strong but process record is
  deliberately sparse, and one whose process is evidence-rich without guaranteed endpoint
  superiority.
- Repeat across independent world seeds and retain campaign, not lifecycle or operation,
  as the analysis unit.
- Report signature recovery, effect sizes across worlds, test–retest agreement and failures;
  keep all 19 coordinates separate.

This converts the existing positive control into a more independent measurement-validity
study without turning the paper into a claim about general intelligence.

### 3. Repair and requalify the discarded-state evaluator — primary

Question: can the evaluator resolve every registered counterfactual terminal state without
mutating the original trajectory or resource record?

- Repair the identity-prefix, resource-entry and assay-precondition integration failures.
- Qualify the repaired path on disjoint synthetic cases, then freeze a new protocol.
- Run a fresh discard cohort; do not substitute repaired outputs into the historical failed
  cohort.
- Require complete registered coverage for point estimation. Otherwise retain a failed
  qualification and report bounds only.

The historical 6-of-36 failure remains visible as a prior instrument defect; it is never
rewritten into a favorable result.

### 4. Crossed interface sensitivity — secondary

Question: how much of the observed terminal profile depends on the interaction surface?

- Minimum identifiable design: run the same model through both interaction surfaces with
  harmonized terminal-action descriptions and matched world/resource identities.
- Preferred design: two models crossed with two interfaces, with prompt content and retry
  policy explicitly controlled.
- Pair comparisons by world campaign. Estimate within-model interface effects first;
  treat model-by-interface interaction as descriptive unless the number of independent
  worlds supports a planned inferential model.

This is a sensitivity control for Paper I. Mechanistic explanation of model behavior,
adaptation and law learning remains Paper II.

### 5. Physical bridge — later, not required for the virtual-instrument release

Use calibrated high-fidelity simulators, reference datasets or laboratory experiments only
when the paper is asked to claim physical predictive validity. Do not add a token wet-lab
example that cannot validate the full instrument contract.

## Recommended execution order

1. Run the cross-world infrastructure qualification.
2. Repair and freshly qualify the discarded-state evaluator.
3. Run independent endpoint-matched profile validation.
4. Add the crossed-interface sensitivity experiment if feasible within the first-paper
   schedule; otherwise state it as the first Paper II experiment.
5. Rebuild the manuscript around the new evidence once, without exposing internal audit
   plumbing.

## Statistical contract for new evidence

- Define one independent unit before launch for every experiment class.
- Preserve paired or blocked world structure in analysis.
- Report effect sizes and the complete vector of independent-unit contrasts.
- Use uncertainty intervals only when their target population and sampling interpretation
  are explicit.
- Define censoring and failure handling before launch; no complete-case substitution.
- Separate deterministic qualification counts from stochastic agent experiments.
- Freeze primary comparisons before viewing formal outcomes and label exploratory analyses.

## Stop rule for the first paper

Paper I is ready for a new external review when the full infrastructure matrix is complete,
the repaired evaluator has either passed a fresh cohort or remains explicitly failed, and
the profile has at least one independent endpoint-matched validation. Crossed-interface
sensitivity strengthens the paper but does not become a causal behavior claim. Physical
validation and mechanistic explanation are not required for this virtual-instrument paper.
