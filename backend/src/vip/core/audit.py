"""Audit findings and the deterministic check catalogue (spec 13, 31).

Phase 0 registers every check with its severity and spec reference. Phase 1 implements
them; an unimplemented check is reported as such, never as passed."""

from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class Severity(StrEnum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"


class FindingStatus(StrEnum):
    OPEN = "open"
    RESOLVED = "resolved"
    ACCEPTED_WITH_JUSTIFICATION = "accepted_with_justification"
    FALSE_POSITIVE = "false_positive"


class FindingOrigin(StrEnum):
    DETERMINISTIC = "deterministic"
    AI_AUDITOR = "ai_auditor"
    PACK_CHECK = "pack_check"


class AuditCheck(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str
    severity: Severity
    spec_ref: str
    description: str


class AuditFinding(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID = Field(default_factory=uuid4)
    check_id: str
    severity: Severity
    origin: FindingOrigin
    location: str  # e.g. "segment:main/variable:revenue/period:FY2027"
    explanation: str
    expected_correction: str | None = None
    suggested_resolution: str | None = None
    status: FindingStatus = FindingStatus.OPEN
    justification: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


def can_declare_validated(findings: list[AuditFinding], checks_not_run: list[str]) -> bool:
    """Spec 13: never 'validated' while critical errors remain open — or while any critical
    check could not be run."""
    critical_ids = {c.id for c in CHECK_CATALOGUE if c.severity == Severity.CRITICAL}
    if critical_ids & set(checks_not_run):
        return False
    return not any(f.severity == Severity.CRITICAL and f.status == FindingStatus.OPEN for f in findings)


def _c(id: str, sev: Severity, ref: str, desc: str) -> AuditCheck:
    return AuditCheck(id=id, severity=sev, spec_ref=ref, description=desc)


C, H, Md = Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM

CHECK_CATALOGUE: tuple[AuditCheck, ...] = (
    _c("real_nominal_mismatch", C, "26.1, 31", "Discount rate, cash flows and terminal growth share one price basis."),
    _c(
        "country_risk_count",
        C,
        "26.1, 31",
        "Country risk premium appears exactly once (Framework C) and is not double counted (Framework A).",
    ),
    _c("cash_flow_rate_pairing", C, "6.2, 31", "FCFF at WACC/Ku; FCFE, dividends, residual income at Ke."),
    _c("wacc_market_weights", C, "26.3, 31", "WACC equity weight at diluted market value."),
    _c("wacc_weights_vs_relever", C, "26.3, 31", "D/(D+E) in WACC consistent with D/E used to relever beta."),
    _c("finite_life_perpetuity", C, "27.1, 31", "No Gordon terminal value on a finite-life asset without justification."),
    _c("pass_through_in_ebitda", C, "27.2, 31", "Pass-through or non-cash revenue excluded from EBITDA used for margins/multiples."),
    _c(
        "bridge_completeness",
        C,
        "17, 27.2, 31",
        "Debt-like items present in the EV-to-equity bridge, consistent with IFRS 16 EBITDA basis.",
    ),
    _c("fcff_on_financial_institution", C, "25.2, 31", "No FCFF/WACC on a financial institution."),
    _c("balance_sheet_balances", C, "5.2, 13", "Assets = liabilities + equity in every period."),
    _c("cash_flow_reconciles", C, "5.2, 13", "Change in cash equals cash flow statement total."),
    _c("growth_below_wacc", C, "6.4", "Perpetual growth strictly below discount rate."),
    _c("unit_currency_consistency", C, "13, 16", "No arithmetic across incompatible units, currencies or price bases."),
    _c("growth_vs_gdp", H, "31", "Perpetual growth below long-term GDP growth of the currency (nominal or real per framework)."),
    _c("terminal_share_of_ev", H, "6.4, 31", "Terminal value share of EV above threshold (default 75%) requires explanation."),
    _c("terminal_roic_consistency", H, "6.4, 31", "g = reinvestment rate × ROIC in the terminal year."),
    _c("base_year_reconciliation", H, "31", "Base-year figures reconcile to reported actuals within tolerance."),
    _c("diluted_shares", H, "6.1, 31", "Diluted shares used; treasury shares excluded."),
    _c("minorities_at_market", H, "27.8, 31", "Minority interests at market/intrinsic value where available."),
    _c("tax_shield_negative_ebt", H, "26.4, 31", "No tax shield in years with negative EBT or unusable losses."),
    _c("beta_low_r2", Md, "26.2, 31", "Regression beta with low R² is flagged."),
    _c("timing_convention", Md, "31", "Stub period and discounting convention explicit and appropriate."),
    _c("risk_free_duration", Md, "26.1, 31", "Risk-free maturity matched to cash-flow duration."),
    _c("unverified_parameters", H, "29", "No parameter with status needs_verification feeds a valuation output."),
    _c("consensus_divergence", Severity.INFORMATIONAL, "31", "Divergence from consensus and peer multiples explained."),
)
