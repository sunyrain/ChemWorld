# Work II DeepSeek development evaluator confirmation

Date: 2026-08-10. Status: frozen post-hoc development evaluation; not formal or private evidence.

Question: Do the retained 75 DeepSeek development trajectories improve registered held-out
predictions, produce executable final law summaries, and commit recommendations that survive
outcome-blind replay?

Coverage: retain the exact five tasks x five world seeds x three prior arms already bound by
`work_ii_deepseek_five_task_development_complete_analysis_sources_20260810.json`. Execute four
evaluator-held queries for each of the 25 task x seed clusters (100 zero-provider truth
experiments). For every participant cell that already completed and passed its frozen runner
qualification, replay the observed incumbent and committed final recommendation three times each
under paired evaluator noise. Failed participant cells remain failed and receive no blind replay.
No participant session is rerun or replaced.

Measurements: checkpoint prediction error, pre-to-final improvement, executable-law error and
consistency, task x seed H1/H2/H3 descriptive contrasts, blind recommendation gain, evaluator
failures, exact replay, operation denominators and provider-call count.

Pass/failure: all 25 truth clusters and their 100 queries must reach terminal exact-replay records;
all blind executions scheduled from the frozen qualified-cell denominator must reach terminal
exact-replay records; evaluator provider calls and participant-ledger impact must remain zero. A
missing or invalid participant prediction, law summary or recommendation is retained as a model or
method outcome, not repaired. No formal hypothesis test or transfer claim is authorized.

Expected outputs: an ignored raw evaluator root under `runs/development/`, progress events during
execution, and one tracked JSON plus Markdown report with exact denominators, source hashes and all
failures.

Infrastructure amendment before the accepted block: the first zero-provider evaluator attempt
completed 100/100 truth queries but created 0/414 blind trajectories because the full participant
cell ID was used as a Windows directory name and exceeded the filesystem path limit. The raw failed
root and its denominators are retained. The blind evaluator now keeps the complete execution ID in
the receipt while using a deterministic short-hash directory. Because this is a platform defect,
the entire evaluator block is rerun from the first truth cluster; no participant trajectory is
rerun and no scientific result is selected or replaced.
