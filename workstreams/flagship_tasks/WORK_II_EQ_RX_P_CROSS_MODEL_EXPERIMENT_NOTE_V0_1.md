# Work II EQ-P / RX-P cross-model experiment note v0.1

Date: 2026-09-22  
Status: authorized prospective execution

## Question

Holding the qualified EQ-P and RX-P scientific contracts fixed, how robust are autonomous
experimentation, sealed mechanism reporting, blind prediction, retrospective calibration, and
recommendation behavior to the Codex model and reasoning-effort condition?

## Frozen comparison units

Five provider conditions are declared before any ChemWorld source session:

1. GPT-5.6 Sol / medium (concurrent anchor);
2. GPT-5.6 Sol / xhigh;
3. GPT-5.5 / medium;
4. GPT-5.6 Terra / medium;
5. GPT-5.6 Luna / medium.

The originally considered GPT-5.5 dated snapshot, GPT-5.4 alias/snapshot, and GPT-5.3 Codex alias
were tested only with minimal provider-availability prompts before any ChemWorld session. The
current ChatGPT cached-login provider rejected them as unsupported, while the GPT-5.5 alias and
the two listed GPT-5.6 variants passed. These availability exclusions are infrastructure facts,
not experimental failures or outcome-based model selection. The exact resolved model IDs are
sealed in the run design.

Each condition receives 45 independent participant sessions:

- EQ-P: 5 physical worlds x Opaque/Aligned/MisIndexed x 1 characterization task = 15 sessions;
- RX-P: 5 physical worlds x Opaque/Aligned/MisIndexed x mechanism-discovery/optimization = 30
  sessions.

Every session has 12 autonomous source batches followed in the same provider thread by its frozen
K1, Q, and K2 chain. EQ retains its already frozen EQ-specific supplement because that supplement
is part of the completed EQ-P contract. The total prospective denominator is therefore 225 source
sessions, 2,700 source batches, and 675 shared K1/Q/K2 posttests (plus 75 frozen EQ supplements).

## Invariants and measurements

Only provider model ID and reasoning effort vary. Worlds, world seeds, keyed observation-noise
coordinates, O/A/M information arms, task goals, source budget, instruments, prompts, query banks,
reference truth, scoring, recommendation retest semantics, and exact-replay checks remain those of
the qualified source protocols. Noise namespaces deliberately omit model identity so equal action
histories are paired across provider conditions. Reference truth is provider-free, shared across
conditions, hidden until every required participant posttest is sealed, and generated only once.

Recorded outputs include the complete source trajectory, all failed and committed operations,
provider/resource receipts, recommendation, K1/Q/K2 (and EQ supplement), validation, exact replay,
blind-prediction metrics, recommendation retest, per-condition summaries, and a cross-condition
manifest. Credentials, raw authentication material, and unhashed provider thread identifiers stay
outside Git.

## Launch, pass, and failure rules

The existing qualified provider-free EQ-P and RX-P gates are reused by immutable hash binding;
changing the language model cannot change their deterministic physical result. Before scientific
execution, each provider condition must pass one minimal login/model compatibility probe that has
no ChemWorld tools or observations.

The formal W01 canary contains 45 sessions (nine per provider condition). A condition passes only
if all nine sessions finish 12 source batches, exact replay, and the complete sealed posttest chain.
No W02-W05 session starts until all five canary conditions pass. Scientific/schema failures are
retained and stop expansion; transport/infrastructure repair must be recorded separately and may
not erase or replace the failed attempt based on outcome.

After a passing canary, the remaining 180 sessions run from a single block-balanced global queue.
The maximum previously qualified shared-provider concurrency is eight isolated subprocesses. The
queue keeps all five provider conditions interleaved; it does not allocate eight workers per
condition. This prevents shared global-provider state, directory collisions, and avoidable rate
limit confounding while using the validated concurrency ceiling. Provider traffic uses a dedicated
Mac-to-Materials reverse proxy listener on remote port 7898 with SSH keepalives; it is independent
of the pre-existing shared listener on port 7897.

No result-dependent extra samples, model-specific prompt changes, or model-specific tool budgets
are allowed. Completion requires 225/225 conforming source chains, 2,700/2,700 source batches,
exact replay, all sealed posttests, shared provider-free truth/evaluation, and retained accounting
for every failure and repair.

## Pre-action recovery 1

The first detached controller created no trajectory, result, completed batch, or scientific model
response. Its children failed during agent construction because the non-login controller PATH did
not contain the already installed Codex executable; GPT-5.5 additionally passed the live provider
probe but was absent from the local adapter's static allowlist. The controller was stopped while
the canary was still pre-action. The entire original namespace and logs are retained. Before a
fresh namespace is launched, recovery 1 adds an explicit executable/PATH preflight, adds only the
provider-verified GPT-5.5 alias to the adapter allowlist, and validates every frozen condition
before creating any source directory. No prompt, world, arm, task, budget, seed, query, metric,
model condition, or scientific stopping rule changes.

The recovery preflight additionally caught that the shared virtual environment uses an editable
installation pointing at the collaborator's working checkout. No recovery run directory or model
call had started. The detached recovery controller therefore prepends the frozen archive's `src/`
and repository root to `PYTHONPATH`; the recorded import path and source commit must resolve inside
that archive. This is execution isolation only and does not change the scientific environment.
