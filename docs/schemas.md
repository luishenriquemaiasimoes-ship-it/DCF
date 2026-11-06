# Core schemas, sector-pack interface, archetypes, database design

Status: Phase 0, waiting for review. Code: `backend/src/vip/`. Each rule below is enforced by a validator and covered by a test in `backend/tests/`.

## 1. Core schemas (`vip.core`)

| Module | Entities (spec 16 name → code) | Rules enforced at construction |
|---|---|---|
| `units` | `Unit`, `Dimension`, `Scale`, `PriceBasis` | Money needs an ISO currency **and** a nominal/real basis. Real needs a base year. Percent/ratio can't carry a currency. Physical dimensions need a pack-defined `physical_unit`. Only identical units can be added (`addable_with`). |
| `periods` | FinancialPeriod/ForecastPeriod → `FinancialPeriod` (`kind` = actual/forecast); `Timeline`; `DiscountingConvention` | Periods are contiguous with unique ids, actuals come before forecasts, stub periods are supported, and the convention (end/mid) is explicit (spec 31, Medium) |
| `provenance` | SourceRecord → `SourceRecord`; `ValueOrigin`; `Confidence` | The seven value kinds of spec 2.3, plus `parameter` |
| `statements` | FinancialStatement/FinancialMetric → `StatementLine`; `BridgeItemKind`; `EbitdaTreatment` | Universal lines that packs map onto. EV-to-equity bridge vocabulary (spec 17, 31). Pass-through/non-cash flags for EBITDA (spec 31, Critical). |
| `formula` | FinancialFormula/FormulaDependency → `FormulaSpec` | Whitelisted grammar and functions (`prev`, `min`, `max`, `abs`, `if_positive`). Declared inputs must equal the referenced identifiers. No `eval`. |
| `variables` | VariableDefinition, VariableValue, OperatingDriver (= a variable with `category=operational`) | Calculated ⇔ has a formula. Excluded ⇔ has a reason (spec 4.10). Reported values need a source. Actuals are never overwritten by normalized values; normalization is a separate variable (spec 5.1). |
| `assumptions` | Assumption, AssumptionVersion, AssumptionSource (= `source_ids` → `SourceRecord`), `AISuggestion` | Spec 8.2: AI value / user value / active / original. **An AI suggestion never displaces a user-approved value without `authorized_by_user=True`.** Reset-to-AI is supported. Append-only history. A value-less assumption must be `needs_review`. |
| `archetypes` | `Archetype` (7), `ArchetypeProfile` | See §2 |
| `framework` | `DiscountFramework` (spec 26.1 A/B/C) | B ⇒ real. A, C ⇒ nominal. C ⇒ foreign base currency and CRP included once (or excluded with justification). A/B with CRP added ⇒ justification required (double count). CRP ⇒ one declared source. |
| `valuation` | ValuationMethod, `CashFlowBasis`, `DiscountRateKind`, `TerminalSpec`, `ValuationSpec` | Method ↔ cash-flow basis ↔ rate pairing: FCFF at WACC/Ku only; FCFE, dividends and RI at Ke only (spec 6.2, 31). At most one perpetuity method per spec. |
| `model` | Company, Security, Segment, Scenario, Model/ModelVersion | Each segment's archetype must allow its methods and terminals. Finite-life and project archetypes need `end_of_life`. SOTP needs component segments. Pack versions must be pinned. Scenario probabilities are all unset, or all set and summing to 1. Formula inputs must exist. Assumptions must point to known variables, scenarios and periods. |
| `audit` | AuditFinding, `AuditCheck`, `CHECK_CATALOGUE` | Every check from spec 13 and 31 is registered with severity and spec reference. `can_declare_validated` is false while a Critical finding is open or a Critical check has not run. |

Not yet modeled (by phase): ValuationResult and SensitivityTable (Phase 1 engine outputs), ResearchDocument (Phase 2/3), ExcelArtifact (Phase 5), Industry (Phase 3; packs cover the analytical side).

## 2. The seven archetypes (spec 25.2) — `vip.core.archetypes.ARCHETYPE_PROFILES`

| Archetype | Allowed methods (plus comparables unless noted) | Default | Terminal | Reinvestment constraint | Special |
|---|---|---|---|---|---|
| Perpetual going concern | FCFF, FCFE, APV, DDM, RI, LBO | FCFF | Gordon or exit multiple | Net operating assets | Terminal ROIC/g consistency (Phase 1 audit) |
| Finite-life asset | FCFF, FCFE, APV, project DCF | FCFF | End-of-life items or none. Gordon and "future assets not yet secured" only **with justification**. | Contractual programme | `end_of_life` required (spec 27.1) |
| Financial institution | FCFE, DDM, excess return, RI | FCFE | Gordon or exit multiple | **Regulatory capital** | No FCFF/APV (spec 25.2, 31) |
| Project finance / SPE | Project DCF, FCFF, FCFE, APV (no comparables) | Project DCF | End-of-life items or none | Contractual programme | `end_of_life` required. Coverage-sized debt (spec 28). |
| Asset-based / NAV | NAV, residual value, project DCF | NAV | None or end-of-life | None | Residual method (spec 30) |
| Early stage | FCFF, FCFE | FCFF | Gordon or exit multiple | Net operating assets | Survival probability, dilution |
| Sum of the parts | SOTP only (no comparables) | SOTP | None (components carry their own) | Per component | Child segments required, `ownership_share` per component (spec 27.8) |

## 3. Sector-pack interface (`vip.packs.schema.SectorPack`)

A pack is a YAML file validated into:

- `id`, `version`, `name`, `description`
- `applicable_archetypes`, and `preferred_methods` per archetype (each must be applicable)
- `variables`: full `VariableDefinition`s with `pack_id` set. Formulas may reference pack variables, universal `StatementLine`s, or declared `external_inputs`.
- `kpis`: ids of pack variables
- `accounting_notes`: standard references and treatment text
- `audit_checks`: pack checks written in the formula grammar (`rule ≥ 0` means pass), resolved against pack variables
- `data_sources`: with `licensing_verified` (spec 3, 33)
- `benchmarks`: low/high range **with a mandatory source title and date** (spec 25.1)

Combining packs for a segment (`vip.packs.loader.combine`) fails on any variable-id collision. Shared concepts go through `external_inputs` or core statement lines, so multi-segment companies stay unambiguous.

Example: `backend/packs/toll_road_concession.yaml` is a structural illustration of spec 27.2/27.3. It has traffic × tariff, construction revenue/cost flagged `excluded_pass_through`, and a pack check that construction margin is near zero. It has **no benchmark numbers**, because they would need dated sources.

## 4. Database design (implemented in Phase 2; Phase 0/1 run in memory)

PostgreSQL 16. Every table has `id uuid pk`, `created_at`, and `tenant_id` where it holds user data (row-level security, spec 18). Model content is **immutable per version**: edits create a new `model_version` row with `parent_version_id`.

```
tenant(id, name)                                   user(id, tenant_id, email, role)
company(id, name, country, reporting_currency, fye_month, accounting_standard)
security(id, company_id, ticker, exchange, isin, share_class, currency)
source_record(id, tenant_id?, title, publisher, url, document_date, retrieved_at, locator, sha256, storage_uri)
model(id, tenant_id, company_id, name, owner_id)
model_version(id, model_id, version, parent_version_id, created_by, created_at,
              framework jsonb, timeline jsonb, data_cutoff, notes)               -- ModelVersion header
segment(id, model_version_id, key, name, archetype, parent_key, ownership_share, end_of_life, end_of_life_source)
valuation_spec(id, segment_id, method, cash_flow_basis, discount_rate, terminal jsonb, valuation_date, convention)
scenario(id, model_version_id, key, name, probability, derived_from, narrative)
variable_definition(id, model_version_id, key, name, description, category, unit jsonb, role,
                    formula_expr, formula_inputs text[], materiality, statement_line, bridge_item,
                    ebitda_treatment, segment_key, pack_id, excluded, exclusion_reason)
variable_value(model_version_id, variable_key, period_id, scenario_key null, value double precision,
               origin, confidence, source_ids uuid[])        PK(model_version_id, variable_key, period_id, scenario_key)
assumption(id, model_version_id, variable_key, scenario_key, period_id, unit jsonb, ai_suggestion jsonb,
           user_value, original_value, status, user_approved, explanation, source_ids uuid[])
assumption_version(id, assumption_lineage_id, version, value, origin, changed_by, changed_at, reason)  -- append-only
model_version_parameter(model_version_id, parameter_record_id)   -- pins parameters used
model_version_pack(model_version_id, pack_id, pack_version)       -- pins packs used
sector_pack(id, version, body jsonb, sha256, published_at)        -- immutable per version
parameter_record(id, key, jurisdiction, description, value_type, value text, valid_from, valid_to,
                 applies_to, status, verified_by, verified_at, spec_reference, open_questions text[], supersedes)
parameter_source(id, parameter_record_id, url, title, issuer, is_official, locator,
                 retrieval_status, attempted_at, retrieved_at, sha256, retrieval_note)
valuation_result(id, model_version_id, segment_key, scenario_key, spec_id, outputs jsonb, trace_uri, engine_version)
sensitivity_table(id, model_version_id, x_var, y_var, x_values float8[], y_values float8[], output, grid float8[][])
audit_run(id, model_version_id, engine_version, checks_run text[], checks_not_run text[], validated bool)
audit_finding(id, audit_run_id, check_id, severity, origin, location, explanation, expected_correction,
              suggested_resolution, status, justification)
research_document(id, tenant_id, model_version_id, kind, body jsonb, sources uuid[])  -- Phase 3
excel_artifact(id, model_version_id, storage_uri, sha256, generated_at, recalc_check_passed)  -- Phase 5
job(id, tenant_id, kind, status, progress, error, created_at, finished_at)
ai_usage(id, tenant_id, model_version_id, agent, model_name, input_tokens, output_tokens, cost_estimate)
```

How this meets spec 16's "new operating variables without changing the entire database architecture": pack variables are rows in `variable_definition` and `variable_value`, never new columns.
