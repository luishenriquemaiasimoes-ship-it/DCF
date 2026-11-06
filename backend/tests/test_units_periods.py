from datetime import date

import pytest

from vip.core.periods import FinancialPeriod, PeriodKind, PeriodType, Timeline
from vip.core.units import PERCENT, Dimension, PriceBasis, Unit, money


def test_money_requires_currency_and_basis() -> None:
    with pytest.raises(ValueError):
        Unit(dimension=Dimension.MONEY)
    with pytest.raises(ValueError):
        Unit(dimension=Dimension.MONEY, currency="BRL")


def test_percent_cannot_carry_currency() -> None:
    with pytest.raises(ValueError):
        Unit(dimension=Dimension.PERCENT, currency="BRL")


def test_real_requires_base_year() -> None:
    with pytest.raises(ValueError):
        money("BRL", basis=PriceBasis.REAL)
    assert money("BRL", basis=PriceBasis.REAL, real_base_year=2026).label() == "BRL millions real 2026"


def test_addability() -> None:
    assert money("BRL").addable_with(money("BRL"))
    assert not money("BRL").addable_with(money("USD"))
    assert not money("BRL").addable_with(money("BRL", basis=PriceBasis.REAL, real_base_year=2026))
    assert not money("BRL").addable_with(PERCENT)


def _p(i: str, s: date, e: date, kind: PeriodKind) -> FinancialPeriod:
    return FinancialPeriod(id=i, start=s, end=e, period_type=PeriodType.ANNUAL, kind=kind)


def test_timeline_contiguity_and_order() -> None:
    a = _p("FY2025", date(2025, 1, 1), date(2025, 12, 31), PeriodKind.ACTUAL)
    f = _p("FY2026", date(2026, 1, 1), date(2026, 12, 31), PeriodKind.FORECAST)
    t = Timeline(fiscal_year_end_month=12, periods=(a, f))
    assert t.forecast == (f,) and t.actuals == (a,)
    with pytest.raises(ValueError):
        Timeline(fiscal_year_end_month=12, periods=(f, a))
    gap = _p("FY2027", date(2027, 2, 1), date(2027, 12, 31), PeriodKind.FORECAST)
    with pytest.raises(ValueError):
        Timeline(fiscal_year_end_month=12, periods=(a, f, gap))
