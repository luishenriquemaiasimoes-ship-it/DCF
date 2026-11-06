"""Variable Registry (spec 4) — the industry-neutral representation that lets packs
introduce new operating variables without schema changes (spec 16)."""

from enum import StrEnum
from typing import Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from vip.core.formula import IDENT, FormulaSpec
from vip.core.provenance import Confidence, ValueOrigin
from vip.core.statements import BridgeItemKind, EbitdaTreatment, StatementLine
from vip.core.units import Unit


class Materiality(StrEnum):
    CRITICAL = "critical"
    MATERIAL = "material"
    SECONDARY = "secondary"
    NON_MATERIAL = "non_material"


class VariableCategory(StrEnum):
    OPERATIONAL = "operational"
    FINANCIAL = "financial"
    MACROECONOMIC = "macroeconomic"
    REGULATORY = "regulatory"
    NON_RECURRING = "non_recurring"
    VALUATION = "valuation"


class VariableRole(StrEnum):
    INPUT = "input"  # assumption or historical datum
    CALCULATED = "calculated"  # defined by a formula


class VariableDefinition(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str = Field(pattern=rf"^{IDENT}$")  # namespaced ids allowed: "pack.var"
    name: str
    description: str
    category: VariableCategory
    unit: Unit
    role: VariableRole
    formula: FormulaSpec | None = None
    materiality: Materiality
    statement_line: StatementLine | None = None  # rolls up into a universal line
    bridge_item: BridgeItemKind | None = None  # EV-to-equity bridge classification
    ebitda_treatment: EbitdaTreatment = EbitdaTreatment.INCLUDED
    segment_id: str | None = None
    pack_id: str | None = None
    excluded: bool = False
    exclusion_reason: str | None = None  # spec 4.10: explain excluded variables

    @model_validator(mode="after")
    def _check(self) -> Self:
        if self.role == VariableRole.CALCULATED and self.formula is None:
            raise ValueError(f"{self.id}: calculated variable requires a formula")
        if self.role == VariableRole.INPUT and self.formula is not None:
            raise ValueError(f"{self.id}: input variable cannot have a formula")
        if self.excluded != bool(self.exclusion_reason):
            raise ValueError(f"{self.id}: excluded variables need exclusion_reason (and only they)")
        if self.ebitda_treatment != EbitdaTreatment.INCLUDED and self.statement_line not in (
            StatementLine.REVENUE,
            StatementLine.COGS,
            StatementLine.OTHER_OPEX,
            None,
        ):
            raise ValueError(f"{self.id}: ebitda_treatment applies only to revenue/cost lines")
        return self


class VariableValue(BaseModel):
    """One value of one variable, in one period, in one scenario. Historical values
    are stored with origin=REPORTED and never overwritten by normalized ones (spec 5.1):
    normalization creates a separate variable or adjustment."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    variable_id: str
    period_id: str
    scenario_id: str | None = None  # None for actuals (shared across scenarios)
    value: float | None
    origin: ValueOrigin
    source_ids: tuple[UUID, ...] = ()
    confidence: Confidence | None = None

    @model_validator(mode="after")
    def _check(self) -> Self:
        if self.origin == ValueOrigin.REPORTED and not self.source_ids:
            raise ValueError("reported values require at least one source (spec 2.5, 3)")
        return self
