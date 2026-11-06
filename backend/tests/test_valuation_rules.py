from datetime import date

import pytest

from vip.core.archetypes import ARCHETYPE_PROFILES, Archetype
from vip.core.framework import CountryRiskTreatment as CR
from vip.core.framework import DiscountFramework
from vip.core.framework import FrameworkKind as FK
from vip.core.units import PriceBasis
from vip.core.valuation import CashFlowBasis as CF
from vip.core.valuation import DiscountRateKind as DR
from vip.core.valuation import TerminalKind, TerminalSpec, ValuationSpec
from vip.core.valuation import ValuationMethod as M

D = date(2026, 11, 6)


def test_all_seven_archetypes_have_profiles() -> None:
    assert set(ARCHETYPE_PROFILES) == set(Archetype) and len(Archetype) == 7


def test_financial_institution_forbids_fcff() -> None:
    p = ARCHETYPE_PROFILES[Archetype.FINANCIAL_INSTITUTION]
    assert M.DCF_FCFF not in p.allowed_methods and M.APV not in p.allowed_methods


def test_finite_life_no_perpetuity_by_default() -> None:
    p = ARCHETYPE_PROFILES[Archetype.FINITE_LIFE_ASSET]
    assert p.requires_end_of_life and TerminalKind.GORDON in p.terminals_requiring_justification


@pytest.mark.parametrize("cf,dr", [(CF.FCFF, DR.COST_OF_EQUITY), (CF.FCFE, DR.WACC), (CF.DIVIDENDS, DR.WACC)])
def test_cash_flow_rate_mismatch_rejected(cf: CF, dr: DR) -> None:
    method = {CF.FCFF: M.DCF_FCFF, CF.FCFE: M.DCF_FCFE, CF.DIVIDENDS: M.DDM}[cf]
    with pytest.raises(ValueError):
        ValuationSpec(method=method, cash_flow_basis=cf, discount_rate=dr, valuation_date=D)


def test_valid_pairs_accepted() -> None:
    ValuationSpec(method=M.DCF_FCFF, cash_flow_basis=CF.FCFF, discount_rate=DR.WACC, valuation_date=D)
    ValuationSpec(method=M.DCF_FCFE, cash_flow_basis=CF.FCFE, discount_rate=DR.COST_OF_EQUITY, valuation_date=D)


def test_one_perpetuity_method_per_spec() -> None:
    with pytest.raises(ValueError):
        ValuationSpec(
            method=M.DCF_FCFF,
            cash_flow_basis=CF.FCFF,
            discount_rate=DR.WACC,
            valuation_date=D,
            terminal=(TerminalSpec(kind=TerminalKind.GORDON), TerminalSpec(kind=TerminalKind.EXIT_MULTIPLE)),
        )


def _fw(**kw: object) -> DiscountFramework:
    base: dict[str, object] = dict(
        kind=FK.LOCAL_NOMINAL,
        valuation_currency="BRL",
        price_basis=PriceBasis.NOMINAL,
        risk_free_reference="local fixed-rate sovereign, duration-matched",
        country_risk=CR.EMBEDDED_IN_LOCAL_RISK_FREE,
    )
    base.update(kw)
    return DiscountFramework.model_validate(base)


def test_framework_a_ok_and_crp_double_count_needs_justification() -> None:
    _fw()
    with pytest.raises(ValueError):
        _fw(country_risk=CR.INCLUDED_ONCE, country_risk_source="X")
    _fw(country_risk=CR.INCLUDED_ONCE, country_risk_source="X", justification="local rf minus default spread, arithmetic shown")


def test_framework_b_requires_real() -> None:
    with pytest.raises(ValueError):
        _fw(kind=FK.LOCAL_REAL)
    _fw(kind=FK.LOCAL_REAL, price_basis=PriceBasis.REAL)


def test_framework_c_requires_crp() -> None:
    with pytest.raises(ValueError):
        _fw(kind=FK.FOREIGN_CAPM_CONVERTED, base_currency="USD")
    with pytest.raises(ValueError):
        _fw(kind=FK.FOREIGN_CAPM_CONVERTED, base_currency="USD", country_risk=CR.EXCLUDED_WITH_JUSTIFICATION)
    _fw(kind=FK.FOREIGN_CAPM_CONVERTED, base_currency="USD", country_risk=CR.INCLUDED_ONCE, country_risk_source="one documented source")
