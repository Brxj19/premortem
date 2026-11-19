---
name: premortem-scan
description: Find failure points in a web app before they cause incidents. Use when the user asks what can break, wants a failure / resilience / reliability audit, a premortem, an FMEA, or asks which dependencies are unhandled in a repo, module, service or workflow.
summary: Maps every database, cache, API, queue, storage, auth and config dependency to its known failure modes and reports which are unhandled, ranked by risk.
version: 0.1.0
tags: [reliability, sre, code-review, resilience, fmea]
keywords: [failure modes, premortem, blast radius, unhandled errors, silent failures, timeouts, retries]
use_cases:
  - Audit a service for unhandled failure points before launch
  - Find silent failures that swallow errors
  - Identify the single point of failure in a workflow
---

# premortem-scan

<!-- Implementation in phase 3 -->
