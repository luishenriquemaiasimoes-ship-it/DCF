"""Load and combine sector packs (spec 25.1: multi-segment companies combine packs)."""

from pathlib import Path

import yaml

from vip.packs.schema import SectorPack


def load_pack(path: Path) -> SectorPack:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    for v in raw.get("variables", []):
        v.setdefault("pack_id", raw["id"])
    return SectorPack.model_validate(raw)


def load_pack_dir(directory: Path) -> dict[str, SectorPack]:
    packs: dict[str, SectorPack] = {}
    for p in sorted(directory.glob("*.yaml")):
        pack = load_pack(p)
        if pack.id in packs:
            raise ValueError(f"duplicate pack id {pack.id}")
        packs[pack.id] = pack
    return packs


def combine(packs: list[SectorPack]) -> dict[str, str]:
    """Return variable id -> pack id for a segment using several packs; collisions are errors
    (packs must namespace shared concepts or declare them as external_inputs)."""
    owner: dict[str, str] = {}
    for pack in packs:
        for v in pack.variables:
            if v.id in owner:
                raise ValueError(f"variable {v.id} defined by both {owner[v.id]} and {pack.id}")
            owner[v.id] = pack.id
    return owner
