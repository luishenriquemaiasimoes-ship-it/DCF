"""The seven valuation archetypes (spec 25.2) as data the engine and audit consult.

Archetypes describe economic shape, not sectors: a finite-life profile applies equally
to any asset with a contractual or economic end date."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict

from vip.core.valuation import TerminalKind
from vip.core.valuation import ValuationMethod as M


class Archetype(StrEnum):
    PERPETUAL_GOING_CONCERN = "perpetual_going_concern"
    FINITE_LIFE_ASSET = "finite_life_asset"
    FINANCIAL_INSTITUTION = "financial_institution"
    PROJECT_FINANCE_SPE = "project_finance_spe"
    ASSET_BASED_NAV = "asset_based_nav"
    EARLY_STAGE = "early_stage"
    SUM_OF_THE_PARTS = "sum_of_the_parts"


class ReinvestmentConstraint(StrEnum):
    NET_OPERATING_ASSETS = "net_operating_assets"  # CAPEX + ΔNWC drive growth
    REGULATORY_CAPITAL = "regulatory_capital"  # retained equity must meet capital ratios
    CONTRACTUAL_PROGRAM = "contractual_program"  # investment set by contract/plan
    NONE = "none"
    PER_COMPONENT = "per_component"


class ArchetypeProfile(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    archetype: Archetype
    allowed_methods: frozenset[M]
    default_method: M
    allowed_terminals: frozenset[TerminalKind]
    terminals_requiring_justification: frozenset[TerminalKind] = frozenset()
    reinvestment_constraint: ReinvestmentConstraint
    requires_end_of_life: bool = False
    supports_survival_probability: bool = False
    requires_components: bool = False
    notes: str


_COMPARABLES = frozenset({M.TRADING_COMPARABLES, M.PRECEDENT_TRANSACTIONS})
T = TerminalKind

ARCHETYPE_PROFILES: dict[Archetype, ArchetypeProfile] = {
    Archetype.PERPETUAL_GOING_CONCERN: ArchetypeProfile(
        archetype=Archetype.PERPETUAL_GOING_CONCERN,
        allowed_methods=frozenset({M.DCF_FCFF, M.DCF_FCFE, M.APV, M.DDM, M.RESIDUAL_INCOME, M.LBO}) | _COMPARABLES,
        default_method=M.DCF_FCFF,
        allowed_terminals=frozenset({T.GORDON, T.EXIT_MULTIPLE}),
        reinvestment_constraint=ReinvestmentConstraint.NET_OPERATING_ASSETS,
        notes="Perpetual life; terminal growth must be consistent with reinvestment and ROIC (spec 6.4, 31).",
    ),
    Archetype.FINITE_LIFE_ASSET: ArchetypeProfile(
        archetype=Archetype.FINITE_LIFE_ASSET,
        allowed_methods=frozenset({M.DCF_FCFF, M.DCF_FCFE, M.APV, M.PROJECT_DCF}) | _COMPARABLES,
        default_method=M.DCF_FCFF,
        allowed_terminals=frozenset({T.END_OF_LIFE_ITEMS, T.NONE, T.FUTURE_ASSETS_NOT_SECURED, T.GORDON}),
        terminals_requiring_justification=frozenset({T.GORDON, T.FUTURE_ASSETS_NOT_SECURED}),
        reinvestment_constraint=ReinvestmentConstraint.CONTRACTUAL_PROGRAM,
        requires_end_of_life=True,
        notes="Value to end of contractual/economic life plus end-of-life items; no perpetuity by default (spec 27.1).",
    ),
    Archetype.FINANCIAL_INSTITUTION: ArchetypeProfile(
        archetype=Archetype.FINANCIAL_INSTITUTION,
        allowed_methods=frozenset({M.DCF_FCFE, M.DDM, M.EXCESS_RETURN, M.RESIDUAL_INCOME}) | _COMPARABLES,
        default_method=M.DCF_FCFE,
        allowed_terminals=frozenset({T.GORDON, T.EXIT_MULTIPLE}),
        reinvestment_constraint=ReinvestmentConstraint.REGULATORY_CAPITAL,
        notes="Equity-based only; debt is raw material, not capital. FCFF/WACC forbidden (spec 25.2, 31).",
    ),
    Archetype.PROJECT_FINANCE_SPE: ArchetypeProfile(
        archetype=Archetype.PROJECT_FINANCE_SPE,
        allowed_methods=frozenset({M.PROJECT_DCF, M.DCF_FCFF, M.DCF_FCFE, M.APV}),
        default_method=M.PROJECT_DCF,
        allowed_terminals=frozenset({T.END_OF_LIFE_ITEMS, T.NONE}),
        reinvestment_constraint=ReinvestmentConstraint.CONTRACTUAL_PROGRAM,
        requires_end_of_life=True,
        notes="Debt sized by coverage ratios; levered vs unlevered IRR; reserve accounts (spec 28).",
    ),
    Archetype.ASSET_BASED_NAV: ArchetypeProfile(
        archetype=Archetype.ASSET_BASED_NAV,
        allowed_methods=frozenset({M.NAV, M.RESIDUAL_VALUE, M.PROJECT_DCF}) | _COMPARABLES,
        default_method=M.NAV,
        allowed_terminals=frozenset({T.NONE, T.END_OF_LIFE_ITEMS}),
        reinvestment_constraint=ReinvestmentConstraint.NONE,
        notes="Value of assets less liabilities; residual method for input assets (spec 30).",
    ),
    Archetype.EARLY_STAGE: ArchetypeProfile(
        archetype=Archetype.EARLY_STAGE,
        allowed_methods=frozenset({M.DCF_FCFF, M.DCF_FCFE}) | _COMPARABLES,
        default_method=M.DCF_FCFF,
        allowed_terminals=frozenset({T.GORDON, T.EXIT_MULTIPLE}),
        reinvestment_constraint=ReinvestmentConstraint.NET_OPERATING_ASSETS,
        supports_survival_probability=True,
        notes="Long explicit period to steady state; survival probability; dilution (spec 25.2).",
    ),
    Archetype.SUM_OF_THE_PARTS: ArchetypeProfile(
        archetype=Archetype.SUM_OF_THE_PARTS,
        allowed_methods=frozenset({M.SUM_OF_THE_PARTS}),
        default_method=M.SUM_OF_THE_PARTS,
        allowed_terminals=frozenset({T.NONE}),
        reinvestment_constraint=ReinvestmentConstraint.PER_COMPONENT,
        requires_components=True,
        notes="Each component valued under its own archetype × stake, less holding costs and holding net debt (spec 27.8).",
    ),
}
