"""Unit and currency system (spec 16). Prevents invalid arithmetic such as
adding BRL to USD, nominal to real money, or percentages to money."""

from enum import IntEnum, StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, model_validator

CurrencyCode = str  # ISO 4217, validated in Unit


class Dimension(StrEnum):
    MONEY = "money"
    PERCENT = "percent"  # stored as a fraction: 0.095 == 9.5%
    RATIO = "ratio"  # dimensionless ratio that is not a rate (e.g., D/E, DSCR)
    MULTIPLE = "multiple"  # e.g., EV/EBITDA
    COUNT = "count"  # shares, customers, units
    DAYS = "days"
    YEARS = "years"
    PHYSICAL = "physical"  # volume in a pack-defined physical unit
    MONEY_PER_PHYSICAL = "money_per_physical"  # price per pack-defined physical unit
    MONEY_PER_COUNT = "money_per_count"  # e.g., price per share, ARPU
    DIMENSIONLESS = "dimensionless"  # factors, indices


class Scale(IntEnum):
    UNITS = 0
    THOUSANDS = 3
    MILLIONS = 6
    BILLIONS = 9


class PriceBasis(StrEnum):
    NOMINAL = "nominal"
    REAL = "real"  # constant prices of `real_base_year`


_MONEY_DIMS = {Dimension.MONEY, Dimension.MONEY_PER_PHYSICAL, Dimension.MONEY_PER_COUNT}
_PHYSICAL_DIMS = {Dimension.PHYSICAL, Dimension.MONEY_PER_PHYSICAL}


class Unit(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    dimension: Dimension
    currency: CurrencyCode | None = None
    scale: Scale = Scale.UNITS
    price_basis: PriceBasis | None = None
    real_base_year: int | None = None
    physical_unit: str | None = None  # free text, defined by a sector pack (e.g., "t", "MWh")

    @model_validator(mode="after")
    def _check(self) -> Self:
        money = self.dimension in _MONEY_DIMS
        if money:
            if not self.currency or len(self.currency) != 3 or not self.currency.isupper():
                raise ValueError("monetary unit requires an ISO 4217 currency code")
            if self.price_basis is None:
                raise ValueError("monetary unit requires price_basis (nominal or real)")
        elif self.currency or self.price_basis:
            raise ValueError(f"{self.dimension} unit cannot carry currency or price_basis")
        if self.price_basis == PriceBasis.REAL and self.real_base_year is None:
            raise ValueError("real price basis requires real_base_year")
        if self.price_basis != PriceBasis.REAL and self.real_base_year is not None:
            raise ValueError("real_base_year only applies to real price basis")
        if (self.dimension in _PHYSICAL_DIMS) != bool(self.physical_unit):
            raise ValueError("physical_unit is required for, and only for, physical dimensions")
        if not money and self.dimension is not Dimension.COUNT and self.dimension not in _PHYSICAL_DIMS and self.scale != Scale.UNITS:
            raise ValueError(f"{self.dimension} unit cannot be scaled")
        return self

    def addable_with(self, other: "Unit") -> bool:
        """Two quantities can be added/subtracted only if units are identical."""
        return self == other

    def label(self) -> str:
        scale = {Scale.UNITS: "", Scale.THOUSANDS: " thousands", Scale.MILLIONS: " millions", Scale.BILLIONS: " billions"}[self.scale]
        if self.dimension == Dimension.MONEY:
            basis = "" if self.price_basis == PriceBasis.NOMINAL else f" real {self.real_base_year}"
            return f"{self.currency}{scale}{basis}"
        if self.dimension == Dimension.PERCENT:
            return "%"
        if self.physical_unit:
            base = self.physical_unit if self.dimension == Dimension.PHYSICAL else f"{self.currency}/{self.physical_unit}"
            return f"{base}{scale}"
        return self.dimension.value


def money(
    currency: CurrencyCode, scale: Scale = Scale.MILLIONS, basis: PriceBasis = PriceBasis.NOMINAL, real_base_year: int | None = None
) -> Unit:
    return Unit(dimension=Dimension.MONEY, currency=currency, scale=scale, price_basis=basis, real_base_year=real_base_year)


PERCENT = Unit(dimension=Dimension.PERCENT)
RATIO = Unit(dimension=Dimension.RATIO)
MULTIPLE = Unit(dimension=Dimension.MULTIPLE)
DAYS = Unit(dimension=Dimension.DAYS)
YEARS = Unit(dimension=Dimension.YEARS)
