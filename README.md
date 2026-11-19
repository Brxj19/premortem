# Premortem

Find the failure points in a web application before they cause incidents.

Premortem is a Claude Code skill pack that detects every external entity your code depends on — databases, caches, HTTP APIs, queues, storage, auth, config, and user input — applies a catalog of known failure modes for each, checks the code for handling evidence, and reports what is unhandled, ranked by risk.

## How it works

1. **Detect** — scans Python and TypeScript/JavaScript code for entity call sites and evidence of error handling
2. **Score** — assigns each unhandled failure mode an FMEA Risk Priority Number (severity × likelihood × detectability)
3. **Report** — produces a ranked failure tree, Markdown report and Mermaid fault-tree diagrams
4. **Query** — answers what-if, blast-radius and SPOF questions from the failure tree
5. **Diff** — compares two versions of the code and reports new or worsened failure modes

## Skills

| Skill | Purpose | Tier |
|-------|---------|------|
| `premortem-scan` | Build the failure tree and FAILURES.md report | Lite + Pro |
| `premortem-query` | What-if, blast radius, silent, critical, SPOF queries | Lite + Pro |
| `premortem-pr` | New and newly unhandled failure modes between git refs | Pro |
| `premortem-harden` | Fix suggestions, test skeletons, runbook stubs | Pro |
| `premortem-design` | Pre-mortem from a design doc before code exists | Pro |

## Entity catalog (v1)

| Entity | Examples |
|--------|----------|
| Database | SQLAlchemy, Prisma, Django ORM, TypeORM, Drizzle |
| Cache | Redis, Memcache, node-cache |
| HTTP API | requests, httpx, fetch, axios, Stripe, OpenAI |
| Queue | Celery, BullMQ, SQS, Kafka |
| Storage | S3, GCS, multer, file uploads |
| Auth | JWT, Passport, NextAuth, Clerk |
| Config | os.environ, process.env |
| User Input | Route handlers (FastAPI, Express, Next.js) |

## Constraints

- **Python 3.10+, standard library only** — no pip install, no requirements.txt for runtime
- **No network access** — fully offline, no telemetry
- **Read-only** — never edits your source files; output goes to `premortem-out/`
- **Git used only** by `premortem-pr` for diffing branches

## Development

### Prerequisites

- Python 3.10+
- Node.js 22+ (for TypeScript fixture validation only)

### Setup

```bash
git clone https://github.com/Brxj19/premortem.git
cd premortem
npm install          # dev dependencies only (TypeScript)
```

### Commands

```bash
make test            # run all unit tests
make eval            # evaluate detection against fixture answer keys
make check-fixtures  # verify fixture files parse correctly
make package-lite    # build dist/premortem-lite-<version>.zip
make package-pro     # build dist/premortem-pro-<version>.zip
make clean           # remove output and cache files
```

### Repository layout

```
premortem/
├── pack/                      everything that ships
│   ├── shared/
│   │   ├── catalog/           one JSON + MD per entity type
│   │   ├── scripts/           detect, validate, render, query, diff
│   │   │   └── lib/           shared modules
│   │   ├── schema.md          data format docs
│   │   ├── scoring.md         FMEA scoring rules
│   │   └── resilience.md      team mitigations format
│   └── skills/                SKILL.md for each skill
├── fixtures/                  test apps with planted failures
│   ├── py-shop/               FastAPI app (~15 files)
│   └── ts-shop/               Express app (~15 files)
├── tests/                     unittest suites
├── tools/                     eval.py, package.py
├── docs/                      spec and build plan
└── Makefile
```

### Build phases

| Phase | What | Ships |
|-------|------|-------|
| 0 | Repo setup, fixtures, answer key | — |
| 1 | Entity failure catalog (8 types) | — |
| 2 | detect.py + parsers | — |
| 3 | premortem-scan (score, validate, render) | — |
| 4 | premortem-query | Lite |
| 5 | premortem-pr (diff) | Pro |
| 6 | premortem-harden | Pro |
| 7 | premortem-design | Pro |

## License

All rights reserved.
