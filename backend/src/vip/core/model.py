"""Company, segments, scenarios and the versioned model (spec 9, 16, 25)."""

from datetime import UTC, date, datetime
from enum import StrEnum
from typing import Self
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, model_validator

from vip.core.archetypes import ARCHETYPE_PROFILES, Archetype
from vip.core.assumptions import Assumption
from vip.core.framework import DiscountFramework
from vip.core.periods import Timeline
from vip.core.valuation import ValuationSpec
from vip.core.variables import VariableDefinition


class AccountingStandard(StrEnum):
    IFRS = "ifrs"
    US_GAAP = "us_gaap"
    LOCAL_GAAP = "local_gaap"  # jurisdiction given by Company.country; e.g. CPC pronouncements


class Security(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    ticker: str
    exchange: str
    isin: str | None = None
    share_class: str | None = None
    currency: str


class Company(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID = Field(default_factory=uuid4)
    name: str
    country: str  # ISO 3166-1 alpha-2
    reporting_currency: str
    fiscal_year_end_month: int = Field(ge=1, le=12)
    accounting_standard: AccountingStandard
    securities: tuple[Security, ...] = ()


class Segment(BaseModel):
    """A valuation unit. Each segment has one archetype and zero or more sector packs.
    SOTP segments aggregate children (spec 25.2, 27.8)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str
    name: str
    archetype: Archetype
    pack_ids: tuple[str, ...] = ()
    parent_id: str | None = None
    ownership_share: float = Field(default=1.0, gt=0, le=1)
    end_of_life: date | None = None  # contractual/economic end for finite-life archetypes
    end_of_life_source: str | None = None
    valuation_specs: tuple[ValuationSpec, ...] = ()

    @model_validator(mode="after")
    def _check(self) -> Self:
        profile = ARCHETYPE_PROFILES[self.archetype]
        if profile.requires_end_of_life and not self.end_of_life:
            raise ValueError(f"segment {self.id}: {self.archetype} requires end_of_life (spec 27.1)")
        for spec in self.valuation_specs:
            if spec.method not in profile.allowed_methods:
                raise ValueError(f"segment {self.id}: {spec.method} not allowed for {self.archetype}")
            for t in spec.terminal:
                if t.kind not in profile.allowed_terminals:
                    raise ValueError(f"segment {self.id}: terminal {t.kind} not allowed for {self.archetype}")
                if t.kind in profile.terminals_requiring_justification and not t.justification:
                    raise ValueError(
                        f"segment {self.id}: terminal {t.kind} requires explicit justification for {self.archetype} (spec 27.1)"
                    )
        return self


class Scenario(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str
    name: str
    probability: float | None = Field(default=None, ge=0, le=1)
    derived_from: str | None = None
    narrative: str | None = None


class ModelVersion(BaseModel):
    """Immutable snapshot of everything needed to reproduce a valuation (spec 2.4)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID = Field(default_factory=uuid4)
    model_id: UUID
    version: int = Field(ge=1)
    parent_version_id: UUID | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    created_by: str
    company: Company
    framework: DiscountFramework
    timeline: Timeline
    segments: tuple[Segment, ...]
    scenarios: tuple[Scenario, ...]
    variables: tuple[VariableDefinition, ...]
    assumptions: tuple[Assumption, ...] = ()
    parameter_snapshot: dict[str, str] = {}  # parameter key -> record id used (docs/parameter-store.md)
    pack_versions: dict[str, str] = {}  # pack id -> pack version used
    data_cutoff: date | None = None

    @model_validator(mode="after")
    def _check(self) -> Self:
        seg_ids = {s.id for s in self.segments}
        if len(seg_ids) != len(self.segments):
            raise ValueError("duplicate segment ids")
        for s in self.segments:
            if s.parent_id and s.parent_id not in seg_ids:
                raise ValueError(f"segment {s.id}: unknown parent {s.parent_id}")
            children = [c for c in self.segments if c.parent_id == s.id]
            if ARCHETYPE_PROFILES[s.archetype].requires_components and not children:
                raise ValueError(f"segment {s.id}: sum-of-the-parts requires component segments")
            missing = set(s.pack_ids) - set(self.pack_versions)
            if missing:
                raise ValueError(f"segment {s.id}: pack versions not pinned for {sorted(missing)}")
        scen_ids = {s.id for s in self.scenarios}
        probs = [s.probability for s in self.scenarios]
        if any(p is not None for p in probs):
            if any(p is None for p in probs) or abs(sum(p or 0 for p in probs) - 1) > 1e-9:
                raise ValueError("scenario probabilities must be all set and sum to 1, or all unset")
        var_ids = [v.id for v in self.variables]
        if len(set(var_ids)) != len(var_ids):
            raise ValueError("duplicate variable ids")
        known = set(var_ids)
        for v in self.variables:
            if v.formula and not v.formula.inputs <= known:
                raise ValueError(f"{v.id}: formula references unknown variables {sorted(v.formula.inputs - known)}")
        period_ids = {p.id for p in self.timeline.periods}
        for a in self.assumptions:
            if a.variable_id not in known:
                raise ValueError(f"assumption for unknown variable {a.variable_id}")
            if a.scenario_id not in scen_ids:
                raise ValueError(f"assumption for unknown scenario {a.scenario_id}")
            if a.period_id and a.period_id not in period_ids:
                raise ValueError(f"assumption for unknown period {a.period_id}")
        return self
