# Data Schema

Two JSON files carry everything Premortem produces.

## candidates.json

Raw output from `detect.py`. Contains:
- `schema_version`: always `"1"`
- `root`: the scanned root path
- `generated_at`: ISO 8601 timestamp
- `files_scanned`: `{python: N, typescript: N}`
- `entities`: detected dependencies
- `entry_points`: HTTP routes, jobs, CLI commands, consumers
- `call_sites`: each call to an entity with evidence of handling
- `call_graph`: `[caller, callee]` pairs as `file::function`
- `silent_handlers`: bare except/catch blocks that swallow errors
- `warnings`: parser warnings

## failure-tree.json

The reviewed, scored tree that every other skill reads. Contains everything in candidates.json plus:
- `scope`: which paths and entry points were scanned
- `workflows`: named groups of entry points and entities
- `findings`: each (call site × failure mode) with status, evidence, impact, score, and fix
- `summary`: counts per band, handled, silent, SPOF

See the spec (section 4) for full field definitions and allowed values.
