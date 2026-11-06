# Implementation plan

Status: **Phase 0 complete, waiting for review. Phase 1 starts after approval.**

## Phase 0 — delivered

| Deliverable (spec 21) | Where |
|---|---|
| Repository & environment audit | `architecture.md` §1 |
| Technical architecture, risks | `architecture.md` |
| Core financial data schemas | `backend/src/vip/core/`, documented in `schemas.md` §1 |
| Sector-pack interface | `backend/src/vip/packs/`, `schemas.md` §3, example `backend/packs/toll_road_concession.yaml` |
| Seven archetypes (spec 25.2) | `vip.core.archetypes`, `schemas.md` §2 |
| Parameter store design and data | `backend/src/vip/params/`, `parameter-store.md`, `backend/parameters/br/` |
| Database design | `schemas.md` §4 |
| Coding standards | below |
| Development environment | `backend/` uv project. `cd backend && uv sync && uv run pytest`. 31 tests pass. ruff and mypy --strict are clean. |

## Coding standards

- Python 3.13, `uv`, `ruff` (E, F, I, B, UP; line length 140), `mypy --strict` with the pydantic plugin, `pytest`.
- Pydantic v2 frozen models for every schema. Invariants live in validators, and each one has a test.
- Rates are fractions. Money carries currency, scale and price basis. No bare floats cross module boundaries without a `Unit`.
- No sector names in `vip.core` or `vip.engine` (enforced by test). No law or market values in code (enforced by review and the parameter store).
- Every change runs `ruff check`, `mypy`, and `pytest` before commit. Docs are updated in the same commit as the behavior.
- Commit messages are imperative and reference spec sections where relevant.

## Phase 1 — core financial engine (next, after review)

Scope (spec 21 Phase 1 + 25.3): everything is testable without UI, AI or a database.

1. **Formula evaluator and dependency graph**: parse `FormulaSpec` into an AST, topologically sort per period, support `prev()`, detect cycles, and allow explicitly declared circular blocks (interest on average debt) solved iteratively with convergence reporting. Unit algebra checks money × percent and refuses incompatible additions. Physical-unit conversion factors are declared explicitly in packs.
2. **Statements**: income statement, balance sheet and cash flow built from `StatementLine` roll-ups, with balance and cash reconciliation checks.
3. **Discounting**: end-of-period and mid-period conventions, stub period from the valuation date, constant or per-period rates (needed for year-by-year Ke under declining leverage, spec 26.2).
4. **Cost of capital**: CAPM, Hamada unlever/relever, market-value weights, Framework C Fisher conversion (spec 26.1), and the after-tax cost of debt only where EBT can use the shield (spec 26.4). Inputs come from the parameter store or user assumptions, never constants.
5. **Valuation methods**: FCFF→EV→equity bridge (all `BridgeItemKind`s), FCFE, DDM / excess return for financial institutions with regulatory capital as the reinvestment constraint, Gordon and exit-multiple terminal values, and end-of-life items (indemnity, salvage, closure costs).
6. **Scenarios and sensitivities**: scenario overlay on assumptions, probability-weighted value, and 2-D grids that call the full engine (spec 10: no approximations).
7. **Deterministic audit**: implement the Critical and High checks of `CHECK_CATALOGUE` that apply to Phase 1 objects. Checks that need data not yet available are reported as *not run*, which blocks "validated".

**Phase 1 acceptance tests — three archetypes from the first test (spec 25.3):**

| Case | Archetype | What it proves |
|---|---|---|
| A | Perpetual going concern | FCFF at WACC + Gordon. EV→equity bridge with leases and minorities. Terminal g < WACC. g = reinvestment × ROIC check. TV share flag. |
| B | Finite-life concession, **no perpetuity** | Uses the toll-road pack. Cash flows stop at `end_of_life`. Contractual indemnity at end. Construction revenue excluded from EBITDA. A Gordon TV attempt fails without justification. Per-year Ke under amortizing debt (FCFE variant). |
| C | Bank on FCFE | FCFE = net income − Δ required regulatory capital. Discounted at Ke. FCFF construction refused. Excess-return cross-check equals FCFE value under consistent assumptions. |

Fixtures are **synthetic and labeled illustrative**: no real company data until Phase 2 ingestion exists (spec 20, 32). Expected outputs are computed independently of the engine, with closed-form results where possible and otherwise a separately built spreadsheet committed under `backend/tests/fixtures/` together with its LibreOffice recalculation. Real-company benchmarks (spec 32's list of 7) move to Phase 2.

## Phases 2–6

Unchanged from spec 21, with these additions from Sections 25–34:

- **Phase 2**: Brazilian providers (CVM Dados Abertos, BCB SGS/Focus, IBGE SIDRA, Tesouro), each with a licensing review recorded before activation (spec 33). `LegalSourceProvider` and the parameter verification workflow. PostgreSQL schema from `schemas.md` §4. Real-data benchmark cases.
- **Phase 3**: agents choose the archetype per segment and the packs. Variable Completeness Protocol. WACC Analyst enforces the spec 26 rules (the schema already rejects the structural errors).
- **Later packs**: bank, project finance (spec 28: DSCR sculpting, DSRA/MRA, LLCR/PLCR, goal seek), real estate/land (spec 30), Brazilian tax module (spec 29: Lucro Real/Presumido, loss carryforwards, SUDENE/SUDAM, CBS/IBS transition).

## Open decisions for the reviewer

1. **float64 in the engine** (for Excel parity) vs Decimal. Recommendation: float64.
2. **Phase 1 fixtures synthetic** rather than real companies (real ones need Phase 2 ingestion to meet spec 32's "real and sourced"). Recommendation: synthetic now, real in Phase 2.
3. **Network**: allow `www.planalto.gov.br` (and optionally `www.in.gov.br`) so legal parameters can be verified from official text.
4. **Default branch**: `main` exists on the remote with the spec, but the repository's default branch is still `claude/spec-addendum-25-34`. Switching it is a GitHub repository setting (Settings → General → Default branch) that this session cannot change.
