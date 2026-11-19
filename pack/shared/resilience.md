# Team Mitigations (resilience.json)

Teams can declare infrastructure mitigations that live outside the code — service mesh timeouts, connection pools, retry policies — in `.premortem/resilience.json` at the repo root.

## Format

```json
{
  "schema_version": "1",
  "mitigations": [
    {
      "entity": "http_api:*",
      "mode": "timeout",
      "by": "Envoy sidecar, 5s outbound timeout",
      "owner": "platform"
    }
  ],
  "ignore": [
    {
      "finding": "f:9f1c2a7b3e:rate_limited",
      "reason": "Internal API, no rate limit",
      "until": "2027-03-01"
    }
  ]
}
```

## Rules

- `entity` is `<type>:<name>` with `*` wildcards.
- `paths` (optional) is a list of glob patterns that limit the mitigation to matching call-site files.
- `by` is required and printed in FAILURES.md beside the finding.
- `ignore` entries require a `reason`. Expired `until` dates are ignored and the finding comes back with a warning.
- Matching findings get status `mitigated_by_infra` instead of `unhandled_in_code`.
