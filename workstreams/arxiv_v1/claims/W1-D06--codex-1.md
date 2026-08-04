# Work I Task Claim

```yaml
task_id: W1-D06
title: "Record first-paper authors and affiliation metadata"
status: BLOCKED

owner: "codex-1"
collaborators: []
claimed_at_utc: 2026-08-03T14:02:52Z
lease_expires_at_utc: 2026-08-05T14:02:52Z
heartbeat_at_utc: 2026-08-04T04:59:38Z

base_commit: "969f4cd66b79857dbcd82c66cba2574cad1eef45"
branch: main
worktree: "D:/Projects/ChemWorld"
supersedes: null

declared_write_set:
  - workstreams/arxiv_v1/claims/W1-D06--codex-1.md
  - paper/experimental_intelligence_v1_manuscript.md
  - paper/arxiv/template.tex
  - paper/arxiv/main.tex
  - paper/exports/experimental-intelligence-v1-arxiv/**
shared_hot_file_requests:
  - "paper/arxiv/main.tex: coordinator reservation granted by the user's 2026-08-03 author-metadata instruction"
  - "paper/arxiv/template.tex: coordinator reservation granted by the user's 2026-08-04 author-layout correction instruction"
  - "paper/exports/experimental-intelligence-v1-arxiv/**: coordinator reservation granted for synchronized manuscript artifacts"

deliverables:
  - "Canonical manuscript records Jiangjie Qiu and Yijun Li in that order"
  - "Both authors share the supplied Tsinghua University affiliation"
  - "Current arXiv source artifacts carry the same author and affiliation block"
validation:
  - "Run the task-local arXiv build once"
  - "Confirm placeholder author text is absent from current manuscript artifacts"
  - "git diff --check"

completed_since_last_heartbeat:
  - "Recorded Jiangjie Qiu and Yijun Li in the supplied order"
  - "Assigned both authors to the supplied Tsinghua University affiliation"
  - "Rebuilt the PDF and ZIP/TAR arXiv artifacts once"
  - "Constrained the long affiliation to a centered 0.92-textwidth paragraph box so the author block no longer overflows"
  - "Rebuilt the arXiv PDF/source archives once and visually confirmed the corrected first page"
current_validation: "PASS: one standard arXiv build; 17-page PDF; first-page visual inspection shows both author names and the three-line affiliation fully inside the page; git diff --check"
files_touched:
  - workstreams/arxiv_v1/claims/W1-D06--codex-1.md
  - paper/experimental_intelligence_v1_manuscript.md
  - paper/arxiv/template.tex
  - paper/arxiv/main.tex
  - paper/exports/experimental-intelligence-v1-arxiv/**
blockers:
  - "Corresponding author, public email, and ORCID metadata have not been supplied"
blocked_by: "project owner metadata input for the remaining W1-D06 fields"
unblock_condition: "Receive corresponding-author designation/email and any ORCID values"
next_check_at_utc: 2026-08-04T14:04:32Z
next_24h: "Stop under the project owner's instruction; await corresponding-author metadata only if the release is resumed"
handoff_eta: 2026-08-03T14:04:32Z

final_commit: "e04c58dff741b4d22543eb583d6e2c0dab5f213e"
reviewer: null
review_result: null
notes: "The external 17.7 GB archive is explicitly out of scope for this claim. Main is used because the coordinator requested a visible main-branch claim and directly assigned this shared manuscript metadata update. The 2026-08-04 write-set expansion covers only the user-requested title-page author/affiliation overflow repair."
```
