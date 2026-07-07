# Task Cards

Task cards are the publishable benchmark contract for each registered task.
They are generated from `TaskSpec` so task metadata, CLI output, and
documentation do not drift.

Inspect one card:

```bash
chemworld tasks card reaction-optimization-standard
```

Each card contains:

- task id;
- scientific motivation;
- world law id and scenario id;
- allowed operations and instruments;
- budget and public/private seed policy;
- online reward and leaderboard metric;
- observation and termination policies;
- success metrics;
- baseline reference score slots;
- failure modes;
- recommended use.

Baseline reference scores are currently explicit `null` placeholders. They
should be filled by the official baseline suite before a benchmark release.

## Release Rule

A task should not be treated as release-ready until its card has:

- fixed public seeds;
- a private-eval policy;
- at least random, LHS, scripted, GP BO, and safe GP BO reference rows where
  applicable;
- known failure modes;
- a short note on intended use: teaching, benchmark, LLM-agent, BO, or RL.
