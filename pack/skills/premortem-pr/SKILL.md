---
name: premortem-pr
description: Detect new and newly unhandled failure modes between two git refs. Use on PRs or before merging a branch.
summary: Diffs failure modes between two versions of the code and reports new, resolved and worsened findings.
version: 0.1.0
tags: [reliability, sre, code-review, pr-review, resilience]
keywords: [pr review, diff, new failures, regression, branch compare]
use_cases:
  - Review a PR for new failure points
  - Compare failure modes between branches
  - CI gate on new unhandled failures
---

# premortem-pr

<!-- Implementation in phase 5 -->
