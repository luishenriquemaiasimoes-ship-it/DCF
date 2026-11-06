"""Valuation Intelligence Platform — backend package.

Layout (see docs/architecture.md):
- vip.core   : universal finance schemas. Must contain no sector names (spec 25.1).
- vip.packs  : sector-pack interface and loader. Pack *content* lives in backend/packs/.
- vip.params : dated, sourced parameter store. Parameter *content* lives in backend/parameters/.
"""

__version__ = "0.0.1"
