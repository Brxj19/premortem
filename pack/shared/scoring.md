# Scoring Rules

Every non-handled finding gets an FMEA Risk Priority Number:

    RPN = severity × likelihood × detectability

Each factor is 1–5, so RPN ranges from 1 to 125. Scores are computed only by `lib/score.py`.

## Severity (from impact.kind)

| impact.kind                                    | Severity |
|------------------------------------------------|----------|
| data_loss, silent_loss, double_action, security | 5        |
| wrong_data                                      | 4        |
| error_500, hang, stale_data                     | 3        |
| degraded                                        | 2        |
| none                                            | 1        |

An optional `severity_override` (value 1–5 with a reason of ≥10 chars) takes precedence.

## Likelihood

Start from the mode's `default_likelihood`, then adjust (clamped to 1–5):
- `partial` status: −1
- `mitigated_by_infra` status: −2
- Call site inside a loop or per-request path of an http_route entry point: +1

## Detectability (higher = harder to notice)

| Situation                                                        | Score |
|------------------------------------------------------------------|-------|
| Swallowed and not logged, or no handling and caller discards     | 5     |
| No handling; error propagates to generic framework handler only  | 4     |
| Surfaced to user but not logged                                  | 3     |
| Logged (logger.*, console.error, print to stderr)                | 2     |
| Logged AND reported to error tracking/metrics                    | 1     |

## Bands

| Band     | Rule (first match wins)                    |
|----------|--------------------------------------------|
| critical | severity 5 AND RPN ≥ 40, or RPN ≥ 80      |
| high     | RPN 40–79                                  |
| medium   | RPN 15–39                                  |
| low      | RPN < 15                                   |

## Single Point of Failure (SPOF)

The entity whose non-handled findings touch the most distinct workflows. Ties go to the higher summed RPN.
