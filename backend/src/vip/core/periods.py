"""Periods and timelines (spec 16): fiscal year ends, annual/quarterly/stub,
actual vs forecast, and the discounting convention (spec 31, Medium)."""

from datetime import date
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PeriodType(StrEnum):
    ANNUAL = "annual"
    QUARTER = "quarter"
    STUB = "stub"  # partial period between valuation date and next period end


class PeriodKind(StrEnum):
    ACTUAL = "actual"
    FORECAST = "forecast"


class DiscountingConvention(StrEnum):
    END_OF_PERIOD = "end_of_period"
    MID_PERIOD = "mid_period"


class FinancialPeriod(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str = Field(pattern=r"^[A-Za-z0-9_.-]+$")  # e.g. "FY2025", "2026Q1"
    start: date
    end: date  # inclusive
    period_type: PeriodType
    kind: PeriodKind
    label: str | None = None  # display label, e.g. "1T26"

    @model_validator(mode="after")
    def _check(self) -> Self:
        if self.end <= self.start:
            raise ValueError(f"period {self.id}: end must be after start")
        return self


class Timeline(BaseModel):
    """Ordered, contiguous periods. Actuals precede forecasts."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    fiscal_year_end_month: int = Field(ge=1, le=12)
    periods: tuple[FinancialPeriod, ...]
    convention: DiscountingConvention = DiscountingConvention.END_OF_PERIOD

    @model_validator(mode="after")
    def _check(self) -> Self:
        ids = [p.id for p in self.periods]
        if len(set(ids)) != len(ids):
            raise ValueError("duplicate period ids")
        for a, b in zip(self.periods, self.periods[1:], strict=False):
            if (b.start - a.end).days != 1:
                raise ValueError(f"periods {a.id} and {b.id} are not contiguous")
            if a.kind == PeriodKind.FORECAST and b.kind == PeriodKind.ACTUAL:
                raise ValueError("actual periods must precede forecast periods")
        return self

    @property
    def forecast(self) -> tuple[FinancialPeriod, ...]:
        return tuple(p for p in self.periods if p.kind == PeriodKind.FORECAST)

    @property
    def actuals(self) -> tuple[FinancialPeriod, ...]:
        return tuple(p for p in self.periods if p.kind == PeriodKind.ACTUAL)
