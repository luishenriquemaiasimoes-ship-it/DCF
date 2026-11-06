# Parameter store — dated, sourced tax and market data

Status: Phase 0, waiting for review. Code: `backend/src/vip/params/`. Data: `backend/parameters/`.

## 1. Why

Spec 29: "All rates below must be stored as dated, sourced parameters (not constants in code), because the law changes." Spec 26.5: every WACC input carries source and date. Session rule: legal values are **never filled from memory**.

## 2. Record model (`ParameterRecord`)

| Field | Meaning |
|---|---|
| `id` | Unique record id, e.g. `br.tax.lc214.cbs_rate@2027` |
| `key` | Logical key, e.g. `br.tax.lc214.cbs_rate`. Several records can share a key across time. |
| `jurisdiction` | ISO country, or a sub-national code later |
| `value_type` / `value` | `rate` (fraction), `amount`, `boolean`, `text`. `Decimal` for numbers. |
| `valid_from` / `valid_to` | Effective dating (inclusive). Records for one key may not overlap. |
| `applies_to` | Condition text (regime, entity type, region) |
| `status` | `verified` · `needs_verification` · `superseded` |
| `sources[]` | `ParamSource`: URL, title, issuer, `is_official`, locator (article/§), `retrieval_status` (ok/failed/not_attempted), `attempted_at`, `retrieved_at`, `content_sha256`, `retrieval_note` |
| `verified_by` / `verified_at` | Who checked the value against the retrieved text, and when |
| `spec_reference` | What the spec says, as **text**. It is never used as a value. |
| `open_questions[]` | What the verifier must answer |
| `supersedes` | Previous record id when the law changes |

## 3. Invariants (validators + tests)

1. `needs_verification` ⇒ `value is null`.
2. `verified` ⇒ value present, `valid_from` present, `verified_by` and `verified_at` present, and **at least one official source with `retrieval_status = ok`, `retrieved_at` and `content_sha256`**.
3. A source counts as `ok` only if it has a timestamp and a hash. A `failed` source must log `attempted_at`.
4. No overlapping validity for live records of one key.
5. `ParameterStore.get(key, as_of)` raises `UnverifiedParameterError` unless the caller passes `allow_unverified=True`. The engine never passes it for valuation outputs. Previews may, but then the audit check `unverified_parameters` fires and validation is blocked.

## 4. Lifecycle

```
needs_verification ──(retrieve official text, hash it, read article, fill value, sign)──▶ verified
verified ──(law changes: new record with supersedes=old.id, old.valid_to set)──▶ superseded
```

Verification is done by a person (or by an agent whose output a person approves) working from the retrieved text. The hash proves which text was read. In Phase 2 a `LegalSourceProvider` fetches and stores the raw document as a `SourceRecord`, and verification becomes a reviewed workflow in the workspace.

## 5. Model reproducibility

`ModelVersion.parameter_snapshot` maps each key used to the record id used. Re-running an old version uses the same records even after the law changes. The audit report lists each parameter, its status and its source.

## 6. Current contents (2026-11-06)

All records are `needs_verification` with `value: null`.

| File | Keys | Source | Retrieval |
|---|---|---|---|
| `br/lei_14801_2024_infrastructure_debentures.yaml` | issuer interest treatment, eligibility | planalto.gov.br/.../l14801.htm | **failed**: host blocked by the session network proxy |
| `br/lei_15270_2025_dividends_jcp.yaml` | resident withholding rate, monthly threshold, effective date/transition, non-resident rate, minimum-tax schedule, JCP changes | planalto.gov.br/.../l15270.htm | **failed**: same |
| `br/lc_214_2025_ibs_cbs_transition.yaml` | CBS rate, IBS rate, PIS/COFINS status, ICMS/ISS reduction: one record per year 2026–2033 | planalto.gov.br/.../lcp214.htm | **failed**: same |
| `br/corporate_income_tax.yaml` | IRPJ base, surcharge rate, surcharge threshold, CSLL, loss-offset limit, combined marginal rate | Planalto consolidated laws | not attempted. Spec figures kept in `spec_reference` only. |

To unblock: allow `www.planalto.gov.br` in the environment's network settings, then run verification. `legislacao.presidencia.gov.br` is blocked too. The Diário Oficial (`www.in.gov.br`) was not tried.
