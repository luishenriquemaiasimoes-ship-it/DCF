"""In-memory parameter store loaded from YAML files under backend/parameters/.

Phase 2 moves records into PostgreSQL (docs/schemas.md); the API stays the same."""

from datetime import date
from pathlib import Path

import yaml

from vip.params.schema import ParameterRecord, ParamStatus


class UnverifiedParameterError(LookupError):
    pass


class ParameterNotFound(LookupError):
    pass


class ParameterStore:
    def __init__(self, records: list[ParameterRecord]):
        ids = [r.id for r in records]
        if len(set(ids)) != len(ids):
            raise ValueError("duplicate parameter record ids")
        self._by_key: dict[str, list[ParameterRecord]] = {}
        for r in records:
            self._by_key.setdefault(r.key, []).append(r)
        for key, recs in self._by_key.items():
            live = sorted((r for r in recs if r.status != ParamStatus.SUPERSEDED and r.valid_from), key=lambda r: r.valid_from or date.min)
            for a, b in zip(live, live[1:], strict=False):
                if a.valid_to is None or (b.valid_from and a.valid_to >= b.valid_from):
                    raise ValueError(f"{key}: overlapping validity between {a.id} and {b.id}")

    @classmethod
    def load_dir(cls, directory: Path) -> "ParameterStore":
        records: list[ParameterRecord] = []
        for path in sorted(directory.rglob("*.yaml")):
            doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            for raw in doc.get("records", []):
                records.append(ParameterRecord.model_validate(raw))
        return cls(records)

    def keys(self) -> list[str]:
        return sorted(self._by_key)

    def records(self, key: str) -> list[ParameterRecord]:
        return list(self._by_key.get(key, []))

    def get(self, key: str, as_of: date, *, allow_unverified: bool = False) -> ParameterRecord:
        recs = [r for r in self._by_key.get(key, []) if r.status != ParamStatus.SUPERSEDED]
        if not recs:
            raise ParameterNotFound(key)
        dated = [r for r in recs if r.valid_from and r.valid_from <= as_of and (r.valid_to is None or as_of <= r.valid_to)]
        if dated:
            rec = dated[0]
        else:
            undated = [r for r in recs if r.valid_from is None]
            if not undated:
                raise ParameterNotFound(f"{key} as of {as_of}")
            rec = undated[0]
        if rec.status != ParamStatus.VERIFIED and not allow_unverified:
            raise UnverifiedParameterError(f"{rec.id} is {rec.status}; verify it against its official source before use")
        return rec

    def unverified(self) -> list[ParameterRecord]:
        return [r for recs in self._by_key.values() for r in recs if r.status == ParamStatus.NEEDS_VERIFICATION]
