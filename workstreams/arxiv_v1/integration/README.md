# Work I integration staging

`work-i-integration-queue-v0.1.json` is the coordinator-owned staging authority for
unfinished Work I tasks. It is a frozen queue snapshot, not a replacement for
`WORK_I_TODOLIST.md` or the claim contract.

## Rules

1. `codex-1` is the sole coordinator and planned owner for the remaining first-paper
   work. A task still needs its own committed claim before substantive writes.
2. Only one queue entry may be `in_progress`. Downstream entries stay `waiting` until
   their listed dependencies are accepted on `main`.
3. A non-null `handoff_head` is immutable. A null value means no accepted handoff existed
   at the frozen queue baseline; it is not permission to infer completion from a branch.
4. Shared hot files are edited only during their named reservation window. S03 and S08
   produce isolated story inputs; S10 alone integrates them into the manuscript.
5. Each handoff is pushed promptly. Coordinator acceptance updates the master TODO once,
   after focused task validation and `git diff --check`.
6. W1-D02 remains explicitly deferred by the project owner. W1-D06 remains externally
   blocked on corresponding-author metadata. Neither blocker reopens completed science.

Run the provider-free audit from the repository root:

```powershell
python scripts/audit_work_i_integration_queue.py --check
python -m pytest -o addopts="" tests/test_work_i_integration_queue.py -q
```

The audit reads the TODO and claims at the queue's frozen `baseline_commit`, so later
coordinator status transitions do not silently rewrite the historical staging receipt.
