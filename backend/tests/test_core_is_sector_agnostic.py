"""Spec 25.1 audit check: grep the core for sector names; any hit is a design violation."""

import re
from pathlib import Path

CORE = Path(__file__).resolve().parents[1] / "src" / "vip" / "core"

SECTOR_TERMS = [
    "mining",
    "mine",
    "mines",
    "ore",
    "oil",
    "gas",
    "petroleum",
    "saas",
    "software",
    "subscription",
    "retail",
    "retailer",
    "same-store",
    "bank",
    "banks",
    "banking",
    "insurer",
    "insurance",
    "toll",
    "tolls",
    "highway",
    "road",
    "roads",
    "traffic",
    "concession",
    "concessions",
    "sanitation",
    "water",
    "airport",
    "airports",
    "seaport",
    "telecom",
    "utility",
    "utilities",
    "hotel",
    "hospitality",
    "real estate",
    "land",
    "biotech",
    "pharma",
    "drug",
    "energy",
    "transmission",
    "agribusiness",
]
PATTERN = re.compile(r"\b(" + "|".join(re.escape(t) for t in SECTOR_TERMS) + r")\b", re.IGNORECASE)


def test_core_has_no_sector_names() -> None:
    hits = []
    for path in CORE.rglob("*.py"):
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for m in PATTERN.finditer(line):
                hits.append(f"{path.name}:{n}: {m.group(0)!r} in {line.strip()}")
    assert not hits, "sector names in core (spec 25.1):\n" + "\n".join(hits)
