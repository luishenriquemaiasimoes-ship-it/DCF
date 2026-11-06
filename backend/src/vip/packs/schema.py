"""Sector-pack schema (spec 25.1).

A pack contributes, as data: variable templates and formulas, KPIs, accounting notes,
pack-level audit checks, preferred methods per archetype, data sources, and sourced
benchmark ranges. The core engine never branches on a pack id."""

from datetime import date
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from vip.core.archetypes import Archetype
from vip.core.audit import Severity
from vip.core.formula import IDENT, referenced_identifiers
from vip.core.statements import StatementLine
from vip.core.valuation import ValuationMethod
from vip.core.variables import VariableDefinition


class AccountingNote(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    standard_refs: tuple[str, ...]  # e.g. ("IFRIC 12", "ICPC 01")
    topic: str
    treatment: str


class PackAuditCheck(BaseModel):
    """A pack-specific deterministic check, expressed with the core formula grammar.
    `rule` must evaluate to >= 0 when the check passes (Phase 1 evaluator)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str = Field(pattern=rf"^{IDENT}$")
    severity: Severity
    description: str
    rule: str


class DataSourceRef(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str
    url: str | None = None
    covers: tuple[str, ...] = ()  # variable ids
    licensing_verified: bool = False
    notes: str | None = None


class Benchmark(BaseModel):
    """Benchmark ranges must cite a source (spec 25.1, 2.6)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    variable_id: str
    low: float
    high: float
    source_title: str
    source_url: str | None = None
    source_date: date
    context: str | None = None

    @model_validator(mode="after")
    def _check(self) -> Self:
        if self.low > self.high:
            raise ValueError(f"benchmark {self.variable_id}: low > high")
        return self


class SectorPack(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    version: str
    name: str
    description: str
    applicable_archetypes: frozenset[Archetype]
    preferred_methods: dict[Archetype, tuple[ValuationMethod, ...]] = {}
    variables: tuple[VariableDefinition, ...]
    kpis: tuple[str, ...] = ()
    accounting_notes: tuple[AccountingNote, ...] = ()
    audit_checks: tuple[PackAuditCheck, ...] = ()
    data_sources: tuple[DataSourceRef, ...] = ()
    benchmarks: tuple[Benchmark, ...] = ()
    external_inputs: frozenset[str] = frozenset()  # ids the pack expects from the core or other packs

    @model_validator(mode="after")
    def _check(self) -> Self:
        ids = [v.id for v in self.variables]
        if len(set(ids)) != len(ids):
            raise ValueError(f"pack {self.id}: duplicate variable ids")
        resolvable = set(ids) | set(self.external_inputs) | {s.value for s in StatementLine}
        for v in self.variables:
            if v.pack_id != self.id:
                raise ValueError(f"pack {self.id}: variable {v.id} must declare pack_id={self.id}")
            if v.formula and not v.formula.inputs <= resolvable:
                raise ValueError(f"pack {self.id}: {v.id} references unknown {sorted(v.formula.inputs - resolvable)}")
        for ref in (*self.kpis, *(b.variable_id for b in self.benchmarks)):
            if ref not in ids:
                raise ValueError(f"pack {self.id}: unknown variable {ref}")
        for chk in self.audit_checks:
            unknown = referenced_identifiers(chk.rule) - resolvable
            if unknown:
                raise ValueError(f"pack {self.id}: check {chk.id} references unknown {sorted(unknown)}")
        for arch in self.preferred_methods:
            if arch not in self.applicable_archetypes:
                raise ValueError(f"pack {self.id}: preferred methods for non-applicable archetype {arch}")
        return self
