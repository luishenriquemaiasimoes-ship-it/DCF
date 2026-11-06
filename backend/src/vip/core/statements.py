"""Universal statement lines and EV-to-equity bridge items (spec 5.2, 6.1, 17, 31).

Packs map their variables onto these lines; the core never needs to know the sector."""

from enum import StrEnum


class StatementLine(StrEnum):
    # Income statement
    REVENUE = "revenue"
    COGS = "cogs"
    GROSS_PROFIT = "gross_profit"
    SGA = "sga"
    RND = "rnd"
    OTHER_OPEX = "other_opex"
    EBITDA = "ebitda"
    DA = "da"
    EBIT = "ebit"
    NET_FINANCIAL_RESULT = "net_financial_result"
    EBT = "ebt"
    INCOME_TAX = "income_tax"
    NET_INCOME = "net_income"
    MINORITY_SHARE_OF_NET_INCOME = "minority_share_of_net_income"
    # Balance sheet
    CASH = "cash"
    RECEIVABLES = "receivables"
    INVENTORY = "inventory"
    OTHER_CURRENT_ASSETS = "other_current_assets"
    PPE = "ppe"
    INTANGIBLES = "intangibles"
    GOODWILL = "goodwill"
    PAYABLES = "payables"
    DEBT = "debt"
    OTHER_LIABILITIES = "other_liabilities"
    EQUITY = "equity"
    REGULATORY_CAPITAL = "regulatory_capital"  # reinvestment constraint for financial institutions
    # Cash flow
    CAPEX = "capex"
    CHANGE_IN_NWC = "change_in_nwc"
    ACQUISITIONS_DISPOSALS = "acquisitions_disposals"
    NET_BORROWING = "net_borrowing"
    DIVIDENDS = "dividends"


class EbitdaTreatment(StrEnum):
    """Spec 31 Critical: pass-through / non-cash revenue must not inflate EBITDA used for margins or multiples."""

    INCLUDED = "included"
    EXCLUDED_PASS_THROUGH = "excluded_pass_through"  # e.g., revenue recognized with matching cost and ~zero margin
    EXCLUDED_NON_CASH = "excluded_non_cash"  # e.g., fair-value gains


class BridgeItemKind(StrEnum):
    """EV-to-equity bridge items (spec 6.1, 17, 27.2, 31). Positive = deducted from EV."""

    GROSS_DEBT = "gross_debt"
    CASH_AND_EQUIVALENTS = "cash_and_equivalents"  # added back
    LEASE_LIABILITIES = "lease_liabilities"
    PENSION_DEFICIT = "pension_deficit"
    PROVISIONS_DEBT_LIKE = "provisions_debt_like"  # decommissioning, environmental, litigation, restoration
    REGULATORY_FEES_PAYABLE = "regulatory_fees_payable"
    DECLARED_UNPAID_DISTRIBUTIONS = "declared_unpaid_distributions"
    TAX_INSTALLMENT_PROGRAMS = "tax_installment_programs"
    SUPPLIER_FINANCE = "supplier_finance"
    MINORITY_INTERESTS = "minority_interests"
    NON_OPERATING_INVESTMENTS = "non_operating_investments"  # added back
    PREFERRED_EQUITY = "preferred_equity"
    OTHER_DEBT_LIKE = "other_debt_like"
    OTHER_CASH_LIKE = "other_cash_like"  # added back


ADDED_BACK = frozenset({BridgeItemKind.CASH_AND_EQUIVALENTS, BridgeItemKind.NON_OPERATING_INVESTMENTS, BridgeItemKind.OTHER_CASH_LIKE})
