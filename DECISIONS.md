# Decisions

Decisions taken where the spec is silent, with reasons.

| # | Decision | Reason | Date |
|---|----------|--------|------|
| 1 | Dev dependencies use npm (typescript@5.6.3, @types/node@22.9.0, @types/express@5.0.0). These are NOT runtime deps — the pack itself is stdlib-only Python. | Need `tsc --noEmit` to validate TS fixtures per phase 0 acceptance criteria. | 2026-11-19 |
| 2 | TS fixtures use `.js` with JSDoc types so `node --check` works without compilation. `tsc --noEmit` validates the `.ts` files separately. | Simplest approach: fixtures only need to parse, not run. | 2026-11-19 |
