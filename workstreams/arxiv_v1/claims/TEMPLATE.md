# Work I Task Claim

```yaml
task_id: W1-X00
title: ""
status: CLAIMED

owner: ""
collaborators: []
claimed_at_utc: YYYY-MM-DDTHH:MM:SSZ
lease_expires_at_utc: YYYY-MM-DDTHH:MM:SSZ
heartbeat_at_utc: YYYY-MM-DDTHH:MM:SSZ

base_commit: ""
branch: work1/w1-x00-short-slug
worktree: ../ChemWorld-W1-X00
supersedes: null

declared_write_set:
  - path/or/glob
shared_hot_file_requests: []

deliverables:
  - path/or/artifact
validation:
  - command or review criterion

completed_since_last_heartbeat: []
current_validation: ""
files_touched: []
blockers: []
blocked_by: null
unblock_condition: null
next_check_at_utc: null
next_24h: ""
handoff_eta: YYYY-MM-DDTHH:MM:SSZ

final_commit: null
reviewer: null
review_result: null
notes: ""
```

删除示例值后再提交。时间统一使用 UTC；列表为空时保留 `[]`，不要省略关键字段。
