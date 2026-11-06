"""Discount-rate framework declaration (spec 26.1, 6.3).

Every model declares ONE framework. The validator enforces the structural rules;
the audit engine (Phase 1) checks cash flows and terminal growth against it."""

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, model_validator

from vip.core.units import PriceBasis


class FrameworkKind(StrEnum):
    LOCAL_NOMINAL = "local_nominal"  # spec 26.1 Framework A
    LOCAL_REAL = "local_real"  # spec 26.1 Framework B
    FOREIGN_CAPM_CONVERTED = "foreign_capm_converted"  # spec 26.1 Framework C


class CountryRiskTreatment(StrEnum):
    INCLUDED_ONCE = "included_once"
    EMBEDDED_IN_LOCAL_RISK_FREE = "embedded_in_local_risk_free"
    EXCLUDED_WITH_JUSTIFICATION = "excluded_with_justification"


class DiscountFramework(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: FrameworkKind
    valuation_currency: str
    price_basis: PriceBasis
    risk_free_reference: str  # instrument + maturity, e.g. a local bond series; sourced via the parameter store
    country_risk: CountryRiskTreatment
    country_risk_source: str | None = None
    justification: str | None = None
    base_currency: str | None = None  # Framework C: currency of the CAPM (e.g. USD)

    @model_validator(mode="after")
    def _check(self) -> Self:
        k, cr = self.kind, self.country_risk
        if k == FrameworkKind.LOCAL_REAL and self.price_basis != PriceBasis.REAL:
            raise ValueError("local real framework requires real cash flows (spec 26.1 B)")
        if k in (FrameworkKind.LOCAL_NOMINAL, FrameworkKind.FOREIGN_CAPM_CONVERTED) and self.price_basis != PriceBasis.NOMINAL:
            raise ValueError(f"{k} requires nominal cash flows (spec 26.1)")
        if k == FrameworkKind.FOREIGN_CAPM_CONVERTED:
            if not self.base_currency or self.base_currency == self.valuation_currency:
                raise ValueError("Framework C requires a base_currency different from valuation_currency")
            if cr == CountryRiskTreatment.EMBEDDED_IN_LOCAL_RISK_FREE:
                raise ValueError("Framework C uses a foreign risk-free; country risk cannot be embedded in it")
            if cr == CountryRiskTreatment.EXCLUDED_WITH_JUSTIFICATION and not self.justification:
                raise ValueError("missing country risk under Framework C requires justification (spec 26.1, Critical)")
        if (
            k in (FrameworkKind.LOCAL_NOMINAL, FrameworkKind.LOCAL_REAL)
            and cr == CountryRiskTreatment.INCLUDED_ONCE
            and not self.justification
        ):
            raise ValueError("adding country risk on a local risk-free requires documented justification (double count, spec 26.1 A)")
        if cr == CountryRiskTreatment.INCLUDED_ONCE and not self.country_risk_source:
            raise ValueError("country risk premium requires a single declared source")
        if cr == CountryRiskTreatment.EXCLUDED_WITH_JUSTIFICATION and not self.justification:
            raise ValueError("excluding country risk requires justification")
        return self
