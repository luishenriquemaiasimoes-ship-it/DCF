# Parameter store data

Dated, sourced legal/tax/market parameters. Schema: `src/vip/params/schema.py`. Design: `docs/parameter-store.md`.

Rules:
- A record carries a `value` only when `status: verified`, backed by a successfully retrieved official source (`retrieved_at` + `content_sha256`) and a named verifier.
- Records with `status: needs_verification` have `value: null`. Figures stated in the spec are kept in `spec_reference` as text, not as values.
- Never fill a value from memory. Retrieval attempts that failed are logged with `attempted_at` and `retrieval_note`.
