# CLAUDE.md

## Specification

The full product specification lives in `docs/spec/`:

- `docs/spec/01-24-master-prompt.md` — Sections 1–24 (master prompt).
- `docs/spec/25-34-addendum-sector-packs-brazil-pf.md` — Sections 25–34 (sector packs, Brazil, project finance, lessons learned).

**Read both files before doing any work in this repository.**

**Precedence:** where Sections 25–34 are more specific than Sections 1–24, Sections 25–34 prevail.

## Working documents

- `docs/architecture.md` — system architecture, environment audit, risks.
- `docs/schemas.md` — core schemas, sector-pack interface, valuation archetypes, database design.
- `docs/parameter-store.md` — dated, sourced tax/market parameter store.
- `docs/implementation-plan.md` — roadmap, current status, open decisions.

## Backend

- Python package `vip` in `backend/` (uv). Run: `cd backend && uv sync && uv run ruff check src tests && uv run mypy src && uv run pytest`.
- No sector names in `backend/src/vip/core/` (spec 25.1). `tests/test_core_is_sector_agnostic.py` enforces this.
- Legal/tax/market values live in `backend/parameters/` as dated, sourced records. Never put them in code as constants. Never fill them from memory.
