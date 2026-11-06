from datetime import date
from pathlib import Path

import pytest
import yaml

from vip.core.audit import CHECK_CATALOGUE, AuditFinding, FindingOrigin, Severity, can_declare_validated
from vip.packs.loader import combine, load_pack, load_pack_dir
from vip.params.schema import ParameterRecord
from vip.params.store import ParameterStore, UnverifiedParameterError


def test_repo_packs_load(backend_dir: Path) -> None:
    packs = load_pack_dir(backend_dir / "packs")
    assert "toll_road_concession" in packs
    combine(list(packs.values()))


def test_pack_rejects_unknown_formula_input(tmp_path: Path, backend_dir: Path) -> None:
    raw = yaml.safe_load((backend_dir / "packs" / "toll_road_concession.yaml").read_text())
    raw["variables"][3]["formula"] = {"expression": "nonexistent * 2", "inputs": ["nonexistent"]}
    p = tmp_path / "bad.yaml"
    p.write_text(yaml.safe_dump(raw))
    with pytest.raises(ValueError):
        load_pack(p)


def test_combining_packs_detects_collisions(backend_dir: Path) -> None:
    pack = load_pack(backend_dir / "packs" / "toll_road_concession.yaml")
    with pytest.raises(ValueError):
        combine([pack, pack])


def test_repo_parameters_load_and_are_unverified(backend_dir: Path) -> None:
    store = ParameterStore.load_dir(backend_dir / "parameters")
    assert store.keys()
    for r in store.unverified():
        assert r.value is None
    with pytest.raises(UnverifiedParameterError):
        store.get("br.tax.lc214.cbs_rate", date(2027, 6, 30))
    assert store.get("br.tax.lc214.cbs_rate", date(2027, 6, 30), allow_unverified=True).id == "br.tax.lc214.cbs_rate@2027"


SRC_FAILED = {
    "url": "https://example.gov/x",
    "title": "t",
    "issuer": "i",
    "is_official": True,
    "retrieval_status": "failed",
    "attempted_at": "2026-11-06T00:00:00Z",
}
SRC_OK = {
    "url": "https://example.gov/x",
    "title": "t",
    "issuer": "i",
    "is_official": True,
    "retrieval_status": "ok",
    "retrieved_at": "2026-11-06T00:00:00Z",
    "content_sha256": "0" * 64,
}


def _rec(**kw: object) -> ParameterRecord:
    base: dict[str, object] = {
        "id": "k@1",
        "key": "k",
        "jurisdiction": "XX",
        "description": "d",
        "value_type": "rate",
        "status": "needs_verification",
        "sources": [SRC_FAILED],
    }
    base.update(kw)
    return ParameterRecord.model_validate(base)


def test_unverified_record_cannot_hold_value() -> None:
    with pytest.raises(ValueError):
        _rec(value="0.15")


def test_verified_record_requirements() -> None:
    with pytest.raises(ValueError):  # no successful retrieval
        _rec(status="verified", value="0.15", verified_by="x", verified_at="2026-11-06T00:00:00Z", valid_from="2026-01-01")
    r = _rec(
        status="verified", value="0.15", verified_by="x", verified_at="2026-11-06T00:00:00Z", valid_from="2026-01-01", sources=[SRC_OK]
    )
    assert ParameterStore([r]).get("k", date(2026, 6, 1)).value is not None


def test_overlapping_validity_rejected() -> None:
    a = _rec(id="k@1", valid_from="2026-01-01", valid_to="2026-12-31")
    b = _rec(id="k@2", valid_from="2026-06-01", valid_to="2027-12-31")
    with pytest.raises(ValueError):
        ParameterStore([a, b])


def test_validation_blocked_by_open_critical_or_unrun_critical_check() -> None:
    crit = next(c for c in CHECK_CATALOGUE if c.severity == Severity.CRITICAL)
    f = AuditFinding(check_id=crit.id, severity=Severity.CRITICAL, origin=FindingOrigin.DETERMINISTIC, location="x", explanation="e")
    assert not can_declare_validated([f], [])
    assert not can_declare_validated([], [crit.id])
    assert can_declare_validated([], [])
