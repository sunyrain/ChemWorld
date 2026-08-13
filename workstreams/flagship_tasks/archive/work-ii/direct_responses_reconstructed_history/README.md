# Archived Work II implementation — standalone Direct Responses calls

Status: **retired on 2026-08-07; historical development evidence only.**

This directory preserves the first Work II prior-discovery implementation and all tracked
qualification summaries produced from it. It is archived because its model-side execution unit
was easy to misread as one persistent Codex session per experimental cell.

The actual legacy execution contract was:

- one logical cell used four standalone belief-snapshot requests and two standalone autonomous
  decision requests;
- every request was a fresh WellAU `/responses` call;
- public history was compacted locally and inserted again into each request;
- no provider session/thread identity was resumed;
- MCP and model tools were disabled;
- `StaticOptimizationExperimentSession` was an environment executor object, not a Codex session.

The archived mock, three-arm and five-task reports remain valid only as transport, schema,
deterministic-executor, held-out/blind bookkeeping and failure-recovery qualifications for that
legacy architecture. They are not current participant-method evidence and must not support claims
about persistent-session scientific discovery, prior use, wrong-prior rejection or transfer.

The replacement implementation must satisfy all of the following before new provider data are
produced:

1. exactly one persistent Codex session identity per `task × prior arm × world seed` cell;
2. all evidence updates, experiment choices and final synthesis occur inside that same session;
3. each agent experiment choice compiles to one complete deterministic ChemWorld experiment;
4. held-out and blind validation remain sealed outside the agent session;
5. session resume never replays or overwrites a completed physical experiment;
6. reports distinguish session turns, provider attempts and physical experiments.

Git history remains the primary provenance record. The files here are intentionally not imported
by the current Work II runner.

The retired provider runners and their exclusive tests were removed from the working tree during
the 2026-08-14 control-debt cleanup. Their exact source remains recoverable from Git commit
`d9dbbc7a081c5a2abd56d7e4b8bb5b85d4c85949`. The preserved plans and reports document the legacy
execution contract and observed development results; they do not provide a supported rerun entrypoint.
