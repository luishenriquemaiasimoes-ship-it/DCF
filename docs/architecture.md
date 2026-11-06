# Architecture — Valuation Intelligence Platform

Status: Phase 0 deliverable, waiting for review. Spec: `docs/spec/` (Sections 25–34 take precedence where they are more specific).

## 1. Environment audit (spec 21, Phase 0)

Checked on 2026-11-06 in the build container:

| Item | Found | Use |
|---|---|---|
| Repository | Empty before this work (spec files only) | Greenfield, so the spec 15 stack applies |
| Python | 3.13.18, `uv` | Backend, engine |
| Node | 22.23.4 | Next.js frontend (Phase 4) |
| PostgreSQL | 16 (client and server binaries) | Primary store (Phase 2) |
| Redis | `redis-server` available | Job queue broker (Phase 2/3) |
| LibreOffice | `soffice` available | Headless recalculation of exported workbooks so Excel formulas can be checked against the engine (spec 11.2) |
| Docker | Client only, no daemon | Dev uses local services; Docker Compose is optional and comes later |
| Network | Proxy allowlist. `planalto.gov.br` and `legislacao.presidencia.gov.br` are **blocked** | Legal parameters could not be verified (see `parameter-store.md` §6) |

## 2. Guiding split

AI thinks, users control, models calculate, auditors verify (spec, preamble). This maps onto five layers. A layer may depend only on the layers below it.

```
 ┌──────────────────────────────────────────────────────────────────────┐
 │ web (Next.js)          workspace, grids, scenario manager, audit UI   │  Phase 4
 ├──────────────────────────────────────────────────────────────────────┤
 │ api (FastAPI)          REST + job endpoints, auth, tenancy            │  Phase 2–6
 ├───────────────┬───────────────┬───────────────┬──────────────────────┤
 │ agents        │ data          │ excel/report  │ audit                │
 │ (Claude,      │ (providers,   │ (openpyxl,    │ (deterministic       │
 │  structured   │  ingestion,   │  import/sync, │  checks + AI         │
 │  outputs)     │  normalizing) │  reports)     │  auditor)            │
 │ Phase 3       │ Phase 2       │ Phase 5       │ Phase 1 (det.), 3    │
 ├───────────────┴───────────────┴───────────────┴──────────────────────┤
 │ engine        formula evaluator, dependency graph, statements,        │  Phase 1
 │               discounting, FCFF/FCFE/DDM/RI/project, WACC, terminal,  │
 │               scenarios, sensitivities, goal seek                     │
 ├──────────────────────────────────────────────────────────────────────┤
 │ core          schemas: units, periods, provenance, variables,         │  Phase 0 ✔
 │               assumptions, archetypes, framework, valuation specs,    │
 │               model versions, audit catalogue                         │
 ├──────────────────────┬───────────────────────────────────────────────┤
 │ packs (interface)    │ params (dated, sourced parameter store)        │  Phase 0 ✔
 │ + packs/*.yaml data  │ + parameters/**/*.yaml data                    │
 └──────────────────────┴───────────────────────────────────────────────┘
```

### Hard boundaries

1. **Core and engine know no sectors** (spec 25.1). `tests/test_core_is_sector_agnostic.py` runs the grep check the spec asks for. Phase 1 extends it to `engine/`.
2. **The AI never computes outputs** (spec 2.4, 19). Agents return structured proposals (assumptions, variable registries, pack selections, `ValuationSpec`s), and the engine evaluates them. Goal seek, for example the minimum tariff for a target IRR (spec 28.4), runs in the engine.
3. **Law and market values are data, not code** (spec 26.5, 29). The engine reads them from the parameter store by key and date. Every model version pins the exact parameter records and pack versions it used, which keeps it reproducible.
4. **Packs are data** (YAML validated by `SectorPack`). A new sector means a new YAML file, with no code change.
5. **Audit is independent** of the agent that built the model (spec 13). Deterministic checks are pure functions of a `ModelVersion` plus engine results.

## 3. Repository layout

```
CLAUDE.md
docs/
  spec/                       full specification (verbatim)
  architecture.md             this file
  schemas.md                  core schemas, pack interface, archetypes, database design
  parameter-store.md          dated/sourced parameters
  implementation-plan.md      roadmap, Phase 1 detail, risks, open decisions
backend/
  pyproject.toml, uv.lock     Python 3.13, pydantic 2, pyyaml; dev: pytest, ruff, mypy --strict
  src/vip/
    core/                     Phase 0: schemas (no sector names)
    packs/                    pack schema + loader
    params/                   parameter schema + store
    engine/                   Phase 1
    audit/                    Phase 1 (deterministic checks)
    data/, agents/, excel/, api/   Phases 2–5
  packs/*.yaml                sector-pack data
  parameters/<jurisdiction>/*.yaml   parameter data
  tests/
frontend/                     Phase 4
```

## 4. Key technical decisions

| Decision | Choice | Why |
|---|---|---|
| Numeric type in engine | `float64` | Excel computes in IEEE double. Exported workbooks have to reconcile with engine results to tight tolerances (spec 11.2), and that is easiest with the same arithmetic. Sensitivity grids also need it for speed. |
| Numeric type in parameter store | `Decimal` (string in YAML) | Statutory rates must round-trip exactly. They are converted to float at engine input. |
| Rates | Stored as fractions (0.15 = 15%) | One convention everywhere. The UI and Excel format them for display. |
| Formula language | Small grammar (`vip.core.formula`) with a hand-written evaluator in Phase 1, never `eval` | Safe, inspectable, and translatable to native Excel formulas (spec 11) |
| Schema library | Pydantic v2, frozen models | Validation at the boundary. Immutability makes versions and history simple. |
| Persistence | PostgreSQL + SQLAlchemy 2 + Alembic (Phase 2) | Spec 15. Phase 0/1 run in memory and from YAML, so the engine can be tested without a database (spec 21, Phase 1). |
| Variable storage | Narrow `variable_value` table + JSONB metadata | Packs add variables without migrations (spec 16) |
| Job queue | Redis-backed (RQ or Arq, decided in Phase 2) | Spec 15: persistent status, retry, cancel, progress |
| AI | Anthropic API behind a `LLMProvider` interface. Model ids are configuration, never hardcoded. | Spec 7, 15 |
| Excel check | LibreOffice headless recalculation of exported workbooks, compared against engine outputs | Spec 11.2 ("test workbook formulas using a compatible spreadsheet calculation engine") |
| Locale | ISO dates and `.` decimal internally. pt-BR formats only at presentation. English function names in openpyxl formulas. | Spec 34 |

## 5. Data flow for one valuation

1. **Identify** (data, Phase 2): ticker → `Company`, `Security`. Raw filings are stored with a hash and a retrieval timestamp (`SourceRecord`).
2. **Understand** (agents, Phase 3): the Company and Industry Analysts produce a report, choose the **archetype per segment**, and select or combine **packs**. The Variable Completeness Protocol produces the variable registry (pack templates plus first-principles additions, with exclusions explained).
3. **Propose**: agents produce `Assumption`s holding `AISuggestion`s, a `DiscountFramework`, and `ValuationSpec`s. The schemas reject invalid combinations at construction time: FCFF at Ke, FCFF on a bank, Gordon on a finite-life asset without justification, Framework C without CRP.
4. **Control** (workspace, Phase 4): the user edits. User-approved values cannot be overwritten by the AI (`Assumption.with_ai_suggestion`).
5. **Calculate** (engine, Phase 1): a `ModelVersion` plus a scenario id go in. The engine resolves the dependency graph, builds the statements, discounts, and returns results with a full trace.
6. **Verify** (audit): the deterministic catalogue (`vip.core.audit.CHECK_CATALOGUE`) plus pack checks plus the AI auditor. `can_declare_validated` refuses while any Critical finding is open **or any Critical check has not run**.
7. **Deliver** (Phase 5): Excel with native formulas, and reports (PT-BR default for Brazil, spec 34). The cover shows valuation date, data cut-off and framework.

## 6. Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Legal sources blocked by the network | Tax parameters cannot be verified, so models depending on them cannot be validated | Records are kept as `needs_verification` with no value. The `unverified_parameters` audit check blocks validation. The environment needs `planalto.gov.br` allowlisted. |
| Data licensing (B3, ANBIMA, market data) | Commercial use may be prohibited | Spec 3, 26.5, 33: a provider registry with a licensing status per provider, and no provider goes live without a recorded review |
| Engine shaped by one sector | Rework later | Spec 25.3: Phase 1 tests cover three archetypes from the first test, plus the grep check on the core |
| Formula grammar too weak for real models (circularity from interest on average debt, sculpted repayment) | Engine can't express needed logic | Phase 1 adds explicit iterative solving for declared circular blocks, with convergence reporting. Sculpting is an engine primitive, not a formula. |
| Excel/engine divergence | Users distrust outputs | Every exported workbook is recalculated with LibreOffice in tests and compared with the engine |
| Benchmark fixtures need real sourced data and independent hand calculations (spec 32) | Can't be fabricated | Phase 1 uses **synthetic** fixtures clearly labeled illustrative and checked by an independent hand calculation (closed-form or a separate spreadsheet). Real-company benchmarks come in Phase 2 once ingestion exists. |
| LLM cost and latency | Unviable product | Spec 19: the engine handles edits with no AI call. Agents run in background jobs with caching. Usage is accounted per valuation. |
