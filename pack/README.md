# Premortem Pro

Find the failure points in a web application before they cause incidents.

Premortem detects every external entity your code depends on — databases, caches, HTTP APIs, queues, storage, auth, config, and user input — applies a catalog of known failure modes for each, checks for handling evidence, and reports what is unhandled, ranked by risk.

- **Offline.** No network access, no telemetry.
- **Standard library only.** No pip install required.
- **Read-only.** Never edits your source files.
- **Git used only** by `premortem-pr` for diffing branches.

## Skills

| Skill | Purpose |
|-------|---------|
| premortem-scan | Build the failure tree and FAILURES.md report |
| premortem-query | What-if, blast radius, silent, critical, SPOF queries |
| premortem-pr | New and newly unhandled failure modes between two git refs |
| premortem-harden | Fix suggestions, failure-mocking test skeletons, runbook stubs |
| premortem-design | Pre-mortem from a design doc before code exists |
