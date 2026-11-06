from datetime import date
from uuid import uuid4

import pytest

from vip.core.archetypes import Archetype
from vip.core.assumptions import AISuggestion, Assumption, AssumptionStatus
from vip.core.formula import FormulaSpec, referenced_identifiers
from vip.core.framework import CountryRiskTreatment, DiscountFramework, FrameworkKind
from vip.core.model import AccountingStandard, Company, ModelVersion, Scenario, Segment
from vip.core.periods import FinancialPeriod, PeriodKind, PeriodType, Timeline
from vip.core.provenance import Confidence, ValueOrigin
from vip.core.units import PERCENT, PriceBasis, money
from vip.core.valuation import CashFlowBasis as CF
from vip.core.valuation import DiscountRateKind as DR
from vip.core.valuation import TerminalKind, TerminalSpec, ValuationSpec
from vip.core.valuation import ValuationMethod as M
from vip.core.variables import Materiality, VariableCategory, VariableDefinition, VariableRole, VariableValue

D = date(2026, 11, 6)


def test_formula_validation() -> None:
    assert referenced_identifiers("prev(debt) * (1 + rate) - max(0, x)") == {"debt", "rate", "x"}
    with pytest.raises(ValueError):
        FormulaSpec(expression="a * b", inputs=frozenset({"a"}))
    with pytest.raises(ValueError):
        referenced_identifiers("__import__(os)")
    with pytest.raises(ValueError):
        referenced_identifiers("(a + b")


def test_reported_value_requires_source() -> None:
    with pytest.raises(ValueError):
        VariableValue(variable_id="revenue", period_id="FY2025", value=1.0, origin=ValueOrigin.REPORTED)


def _sugg(v: float) -> AISuggestion:
    return AISuggestion(value=v, reasoning="r", methodology="m", confidence=Confidence.MEDIUM)


def test_ai_never_overwrites_user_approved_value() -> None:
    a = Assumption(variable_id="g", scenario_id="base", unit=PERCENT, ai_suggestion=_sugg(0.05), status=AssumptionStatus.AI_SUGGESTED)
    assert a.active_value == 0.05
    u = a.with_user_value(0.03, by="user1")
    assert u.active_value == 0.03 and u.original_value == 0.05 and u.status == AssumptionStatus.USER_MODIFIED
    after_ai = u.with_ai_suggestion(_sugg(0.07), agent="forecast")
    assert after_ai.active_value == 0.03 and after_ai.ai_suggestion and after_ai.ai_suggestion.value == 0.07
    authorized = u.with_ai_suggestion(_sugg(0.07), agent="forecast", authorized_by_user=True)
    assert authorized.active_value == 0.07
    assert u.reset_to_ai(by="user1").active_value == 0.05
    assert len(u.history) == 1


def _var(i: str, formula: FormulaSpec | None = None) -> VariableDefinition:
    return VariableDefinition(
        id=i,
        name=i,
        description=i,
        category=VariableCategory.FINANCIAL,
        unit=money("BRL"),
        role=VariableRole.CALCULATED if formula else VariableRole.INPUT,
        formula=formula,
        materiality=Materiality.CRITICAL,
    )


def _mv(segments: tuple[Segment, ...], **kw: object) -> ModelVersion:
    tl = Timeline(
        fiscal_year_end_month=12,
        periods=(
            FinancialPeriod(
                id="FY2027", start=date(2027, 1, 1), end=date(2027, 12, 31), period_type=PeriodType.ANNUAL, kind=PeriodKind.FORECAST
            ),
        ),
    )
    fw = DiscountFramework(
        kind=FrameworkKind.LOCAL_NOMINAL,
        valuation_currency="BRL",
        price_basis=PriceBasis.NOMINAL,
        risk_free_reference="x",
        country_risk=CountryRiskTreatment.EMBEDDED_IN_LOCAL_RISK_FREE,
    )
    co = Company(name="Test", country="BR", reporting_currency="BRL", fiscal_year_end_month=12, accounting_standard=AccountingStandard.IFRS)
    base = dict(
        model_id=uuid4(),
        version=1,
        created_by="t",
        company=co,
        framework=fw,
        timeline=tl,
        segments=segments,
        scenarios=(Scenario(id="base", name="Base"),),
        variables=(_var("a"), _var("b", FormulaSpec(expression="a * 2", inputs=frozenset({"a"})))),
    )
    base.update(kw)
    return ModelVersion.model_validate(base)


FCFF = ValuationSpec(
    method=M.DCF_FCFF, cash_flow_basis=CF.FCFF, discount_rate=DR.WACC, valuation_date=D, terminal=(TerminalSpec(kind=TerminalKind.GORDON),)
)


def test_three_phase1_archetypes_construct() -> None:
    fcfe = ValuationSpec(
        method=M.DCF_FCFE,
        cash_flow_basis=CF.FCFE,
        discount_rate=DR.COST_OF_EQUITY,
        valuation_date=D,
        terminal=(TerminalSpec(kind=TerminalKind.GORDON),),
    )
    finite = ValuationSpec(
        method=M.DCF_FCFF,
        cash_flow_basis=CF.FCFF,
        discount_rate=DR.WACC,
        valuation_date=D,
        terminal=(TerminalSpec(kind=TerminalKind.END_OF_LIFE_ITEMS),),
    )
    _mv((Segment(id="gc", name="GC", archetype=Archetype.PERPETUAL_GOING_CONCERN, valuation_specs=(FCFF,)),))
    _mv((Segment(id="fl", name="FL", archetype=Archetype.FINITE_LIFE_ASSET, end_of_life=date(2045, 12, 31), valuation_specs=(finite,)),))
    _mv((Segment(id="fi", name="FI", archetype=Archetype.FINANCIAL_INSTITUTION, valuation_specs=(fcfe,)),))


def test_archetype_rules_enforced_on_segments() -> None:
    with pytest.raises(ValueError):  # FCFF on a financial institution
        Segment(id="fi", name="FI", archetype=Archetype.FINANCIAL_INSTITUTION, valuation_specs=(FCFF,))
    with pytest.raises(ValueError):  # finite life needs end date
        Segment(id="fl", name="FL", archetype=Archetype.FINITE_LIFE_ASSET)
    with pytest.raises(ValueError):  # Gordon on finite life without justification
        Segment(id="fl", name="FL", archetype=Archetype.FINITE_LIFE_ASSET, end_of_life=date(2045, 12, 31), valuation_specs=(FCFF,))


def test_model_version_integrity() -> None:
    with pytest.raises(ValueError):  # SOTP without components
        _mv((Segment(id="h", name="H", archetype=Archetype.SUM_OF_THE_PARTS),))
    with pytest.raises(ValueError):  # unpinned pack version
        _mv((Segment(id="gc", name="GC", archetype=Archetype.PERPETUAL_GOING_CONCERN, pack_ids=("p",)),))
    with pytest.raises(ValueError):  # probabilities must sum to 1
        _mv(
            (Segment(id="gc", name="GC", archetype=Archetype.PERPETUAL_GOING_CONCERN),),
            scenarios=(Scenario(id="base", name="Base", probability=0.5), Scenario(id="bear", name="Bear", probability=0.3)),
        )
