# Work II EQ bounded-aqueous-equilibrium experiment note

Date: 2026-09-20. Status: v1.1 provider-free gate passed; v1.4 operational freeze prepared after the first complete source exposed a posttest-budget monitor mismatch. One coordinator may use isolated source workers after the canary. The scientific contract was fixed before the first scientific action and remains unchanged.

## Question and denominator

Can an autonomous Agent use twelve complete experiments to characterize the effective acidity/dissociation and concentration-or-dilution response of the bounded aqueous-equilibrium task, revise or reject a matched prior, and make calibrated predictions at twelve independent held-out conditions?

The block has one task only: bounded aqueous equilibrium characterization. It has five frozen worlds, three matched prior arms (Strict Opaque, Aligned, MisIndexed), fifteen independent source sessions, twelve complete batches per session, and same-thread K1 → Q → K2 posttests. The formal denominator is 15 sources, 180 source batches, and 45 posttests. Reference truth is shared by matching world and query, uses five independently frozen observation seeds per query, and therefore contains 300 reference executions rather than multiplying truth by arm.

## Worlds, measurements, and information boundary

All worlds use the same base seed and precipitation constant. Only the effective acid-base constant is shifted on the registered `equilibrium.acid-base-constants` axis, yielding five ordered effective pKa values from 4.6594 to 5.3794. The span is intended to be resolvable with the public 0.02-pH instrument noise without creating qualitatively different chemistry.

The source may vary legal solvent volume, reagent amount, staged additions, and allowed measurements. It receives twelve non-final measurements and twelve final assays. The scored prediction channels are `pH_normalized`, `acid_dissociation_fraction`, and `precipitation_signal`. `equilibrium_residual` is a numerical diagnostic. `equilibrium_confidence` is an environment-derived diagnostic and is never treated as Agent uncertainty or a task score.

Strict Opaque receives no instance pKa, center, interval, response direction, precipitation threshold, best point, reference recipe, or target-world-calibrated informative region. Aligned and MisIndexed use the same schema, anchor, wording, numerical precision, interval width, source class, and 80% confidence statement. Only the registered effective-acidity/dilution relationship changes; MisIndexed receives the pre-registered relationship of another frozen world. Legal operations, instruments, budgets, measurement definitions, and all non-locus background remain correct and identical.

## Provider-free pass/failure rules

Before any provider call, the versioned gate executes three independent keyed-noise repeats of all twelve frozen query paths in every world. It requires complete legal execution, exact replay, finite in-range values, the frozen arm schema and permissions, no Strict-Opaque leakage, Aligned coverage, public refutability of MisIndexed, at least 0.08 pH units between every adjacent world at a qualifying probe, at least 0.25 pH units and 0.015 on each other response across the tested design in every world, at least 3-sigma best-probe adjacent separation, non-trivial default and one-shot constant baselines, equivalent-path agreement within 0.01, and resource-window completion. Thresholds are not lowered after seeing results. A failed gate remains development evidence and any repair uses a new config and evidence namespace.

## Posttests and stopping

K1 is a complete self-contained English effective-mechanism/relationship report. Only after K1 is sealed is Q shown: twelve fixed independent new conditions, each requiring point estimates, 80% intervals, and English rationale. Q covers near-domain behavior, amount-versus-volume decoupling, staged order and accumulation, dissociation/precipitation competition, boundary extrapolation, equivalent explanations, and interval calibration. K2 uses the canonical seven themes, rewritten for EQ evidence and limitations. No truth or score is returned before K2 seals.

The first execution wave is EQ-W01 × three arms. It checks chain integrity, isolation, budgets, JSON, report export, and recovery only. If the scientific protocol, priors, worlds, or Q change, the old canary is development-only and W01 reruns in a new namespace. If unchanged and all gates pass, the canary remains part of the fifteen-cell matrix. Platform failures are retained and recovered from the latest legal boundary; retries never count as new scientific samples. Scientific failures remain in the denominator.

## Outputs

The ignored run directory contains frozen design bindings, raw trajectories, private provider recovery state, failures, progress, reference truth after embargo release, and evaluations. Safe repository reports contain no credential, token, provider thread identifier, raw provider stream, or private recovery state. Final delivery includes one English `EXPERIMENT_REPORT.md` and safe `RESULT.json` per cell, a world index, matrix summary, failure/recovery audit, exact denominators, and reproduction instructions.

## Frozen development gate result

The v1.1 provider-free run completed 15/15 keyed-noise campaigns, 180/180 batches, and 15/15 exact replays with zero provider calls. All twelve registered checks passed without changing thresholds: the best fixed probe had a 0.17246 minimum adjacent-world pH gap and 6.232 minimum adjacent separation in pooled-noise standard deviations; within-world pH spans were 1.0431--1.5382, acid-dissociation spans were 0.3831--0.6479, and precipitation-signal spans were 0.1530--0.1597. The failed v1 evidence remains retained; v1.1 changes only the Q coordinates under the repair protocol.

The recovery runner preserves every original cell and creates numbered write-once attempts. A complete, exactly replayed source resumes only missing or invalid same-thread K1/Q/K2 turns; a partial source may restart only in an independent recovery directory and is not counted as a new scientific sample. The final exporter selects one complete effective result per frozen cell, publishes the five-repeat truth and blind scores only after all K2 turns seal, and rejects private field names from public JSON.

The first remote canary launch failed before Agent construction because the detached shell did not expose the installed Codex executable. Recovery attempt 01 then failed before provider-process construction because the private source-output parent had not been created. Both attempts recorded zero operations, zero accepted model calls, zero provider-process attempts, and no scientific output. Protocol v1.2 fixes only those launch prerequisites by injecting the already-authorized executable path and pre-creating the private output parent; the original failures remain retained and the next recovery starts from batch 1.

Recovery attempt 02 started provider processes without the login-shell proxy and retained uniform pre-action network failures. Attempt 03 used the proxy but the three concurrent NFS-backed laboratory MCP processes exceeded the inherited 30-second startup handshake; all failed before a model response or scientific action. A provider-free timing check showed that even a serial laboratory-MCP module import could exceed 48 seconds. Protocol v1.3 therefore sets an EQ-specific 180-second MCP startup allowance and requires the canary arms to start serially. This changes only host startup tolerance, not any scientific or model budget.

Under v1.3, W01 Opaque completed 12/12 source batches with exact replay and no rollback. Its first K1 turn then exposed a previously inherited outer monitor limit of eight calculator attempts, despite the already frozen MCP calculator limit of 128. The original K1 failure is retained with no payload and no truth exposure. Protocol v1.4 passes the same 128-call, continue-answer budget to the outer monitor and makes recovery select the latest durable complete source rather than the initial zero-operation directory. Recovery therefore resumes K1 on the same source thread without rerunning any physical batch.
