"""Valuation method specification and the cash-flow / discount-rate pairing rules
(spec 6.2: never FCFF at Ke or FCFE at WACC; spec 31 Critical)."""

from datetime import date
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, model_validator

from vip.core.periods import DiscountingConvention


class ValuationMethod(StrEnum):
    DCF_FCFF = "dcf_fcff"
    DCF_FCFE = "dcf_fcfe"
    APV = "apv"
    DDM = "ddm"
    RESIDUAL_INCOME = "residual_income"
    EXCESS_RETURN = "excess_return"
    PROJECT_DCF = "project_dcf"  # project/SPE: unlevered and levered IRR, NPV, coverage ratios
    NAV = "nav"
    RESIDUAL_VALUE = "residual_value"  # value of an input asset = value of output − costs − required margin
    TRADING_COMPARABLES = "trading_comparables"
    PRECEDENT_TRANSACTIONS = "precedent_transactions"
    SUM_OF_THE_PARTS = "sum_of_the_parts"
    LBO = "lbo"


class CashFlowBasis(StrEnum):
    FCFF = "fcff"
    FCFE = "fcfe"
    DIVIDENDS = "dividends"
    RESIDUAL_INCOME = "residual_income"  # net income − Ke × book equity
    PROJECT_UNLEVERED = "project_unlevered"
    PROJECT_EQUITY = "project_equity"
    NONE = "none"  # multiples, NAV marks


class DiscountRateKind(StrEnum):
    WACC = "wacc"
    COST_OF_EQUITY = "cost_of_equity"
    UNLEVERED_COST_OF_CAPITAL = "unlevered_cost_of_capital"  # APV / Ku
    NONE = "none"


COMPATIBLE_RATES: dict[CashFlowBasis, frozenset[DiscountRateKind]] = {
    CashFlowBasis.FCFF: frozenset({DiscountRateKind.WACC, DiscountRateKind.UNLEVERED_COST_OF_CAPITAL}),
    CashFlowBasis.FCFE: frozenset({DiscountRateKind.COST_OF_EQUITY}),
    CashFlowBasis.DIVIDENDS: frozenset({DiscountRateKind.COST_OF_EQUITY}),
    CashFlowBasis.RESIDUAL_INCOME: frozenset({DiscountRateKind.COST_OF_EQUITY}),
    CashFlowBasis.PROJECT_UNLEVERED: frozenset({DiscountRateKind.WACC, DiscountRateKind.UNLEVERED_COST_OF_CAPITAL}),
    CashFlowBasis.PROJECT_EQUITY: frozenset({DiscountRateKind.COST_OF_EQUITY}),
    CashFlowBasis.NONE: frozenset({DiscountRateKind.NONE}),
}

METHOD_CASH_FLOWS: dict[ValuationMethod, frozenset[CashFlowBasis]] = {
    ValuationMethod.DCF_FCFF: frozenset({CashFlowBasis.FCFF}),
    ValuationMethod.DCF_FCFE: frozenset({CashFlowBasis.FCFE}),
    ValuationMethod.APV: frozenset({CashFlowBasis.FCFF}),
    ValuationMethod.DDM: frozenset({CashFlowBasis.DIVIDENDS}),
    ValuationMethod.RESIDUAL_INCOME: frozenset({CashFlowBasis.RESIDUAL_INCOME}),
    ValuationMethod.EXCESS_RETURN: frozenset({CashFlowBasis.RESIDUAL_INCOME}),
    ValuationMethod.PROJECT_DCF: frozenset({CashFlowBasis.PROJECT_UNLEVERED, CashFlowBasis.PROJECT_EQUITY}),
    ValuationMethod.NAV: frozenset({CashFlowBasis.NONE}),
    ValuationMethod.RESIDUAL_VALUE: frozenset({CashFlowBasis.NONE, CashFlowBasis.PROJECT_UNLEVERED, CashFlowBasis.PROJECT_EQUITY}),
    ValuationMethod.TRADING_COMPARABLES: frozenset({CashFlowBasis.NONE}),
    ValuationMethod.PRECEDENT_TRANSACTIONS: frozenset({CashFlowBasis.NONE}),
    ValuationMethod.SUM_OF_THE_PARTS: frozenset({CashFlowBasis.NONE}),
    ValuationMethod.LBO: frozenset({CashFlowBasis.FCFE, CashFlowBasis.PROJECT_EQUITY}),
}


class TerminalKind(StrEnum):
    GORDON = "gordon"
    EXIT_MULTIPLE = "exit_multiple"
    END_OF_LIFE_ITEMS = "end_of_life_items"  # indemnity, salvage, closure costs (spec 27.1)
    FUTURE_ASSETS_NOT_SECURED = "future_assets_not_secured"  # separately labeled, default zero (spec 27.1)
    NONE = "none"


class TerminalSpec(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: TerminalKind
    justification: str | None = None  # required where an archetype discourages this kind


class ValuationSpec(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    method: ValuationMethod
    cash_flow_basis: CashFlowBasis
    discount_rate: DiscountRateKind
    terminal: tuple[TerminalSpec, ...] = ()
    valuation_date: date
    convention: DiscountingConvention = DiscountingConvention.END_OF_PERIOD

    @model_validator(mode="after")
    def _check(self) -> Self:
        if self.cash_flow_basis not in METHOD_CASH_FLOWS[self.method]:
            raise ValueError(f"{self.method} cannot use {self.cash_flow_basis} cash flows")
        if self.discount_rate not in COMPATIBLE_RATES[self.cash_flow_basis]:
            raise ValueError(
                f"{self.cash_flow_basis} cash flows cannot be discounted at {self.discount_rate} "
                "(spec 6.2 / 31: FCFF at WACC or Ku; FCFE, dividends, residual income at Ke)"
            )
        kinds = [t.kind for t in self.terminal]
        if TerminalKind.GORDON in kinds and TerminalKind.EXIT_MULTIPLE in kinds:
            raise ValueError("choose one perpetuity method per valuation; run the other as a separate spec")
        return self
