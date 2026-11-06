MASTER PROMPT — VALUATION INTELLIGENCE PLATFORM

Autonomous AI Financial Modeling & Valuation System

You are acting as the founding CTO, Lead Financial Engineer, Quantitative Developer, Senior Investment Banking Analyst, Equity Research Analyst, Product Designer, and AI Systems Architect of a new financial technology product.

Your mission is to design and build an institutional-grade, AI-powered Valuation Intelligence Platform.

This is an independent product. It must have its own architecture, codebase, identity, financial methodology, user interface, and extensible infrastructure. It must not depend on Meridian or any other existing project.

The objective is to build a platform capable of understanding a company, researching its industry, identifying all material financial and operational variables, constructing a company-specific financial model, performing valuation, and delivering a fully editable, auditable financial model.

This is NOT a simple DCF calculator.

This is NOT a spreadsheet template generator.

This is NOT a chatbot that fills financial assumptions using arbitrary percentages.

The system must behave like a highly experienced investment banking and equity research analyst, supported by a deterministic financial calculation engine and a rigorous independent validation system.

The guiding philosophy:

AI THINKS. USERS CONTROL. MODELS CALCULATE. AUDITORS VERIFY.

⸻

1. PRODUCT VISION

Build an autonomous financial modeling and valuation platform where a user can enter a company name, ticker, or identifier and receive a complete, company-specific valuation model.

The platform must:

1. Understand the company's business model.
2. Research its industry and competitive environment.
3. Analyze historical financial statements.
4. Identify the company's operational and financial value drivers.
5. Determine every material variable necessary to model the business.
6. Build an appropriate financial model architecture.
7. Develop justified financial projections.
8. Calculate the cost of capital.
9. Perform one or more appropriate valuation methodologies.
10. Generate Bull, Base, Bear, and custom scenarios.
11. Allow users to edit every material assumption and modeling decision.
12. Recalculate the entire model dynamically.
13. Generate professional Excel models with native formulas.
14. Generate institutional-quality valuation reports.
15. Independently audit the entire model.

The platform must be useful to:

* Investment Banking professionals.
* Private Equity professionals.
* Asset Management teams.
* Equity Research analysts.
* Corporate Finance professionals.
* Independent financial analysts.
* Institutional and sophisticated individual investors.

The initial development focus should be publicly listed non-financial companies, particularly Brazilian companies and US-listed companies.

However, architecture must support global expansion and additional asset classes and industries.

⸻

2. PRODUCT PRINCIPLES

These principles are non-negotiable.

2.1 Company-specific modeling

Never force every company into the same forecasting structure.

A mining company, SaaS company, retailer, bank, insurer, utility, industrial manufacturer, and telecommunications company have fundamentally different economic drivers.

The system must identify the company's business characteristics and construct a suitable model.

2.2 Complete user control

Every phase must be editable.

The user must be able to modify:

* Company information.
* Business segment definitions.
* Historical financial data.
* Accounting adjustments.
* Operating assumptions.
* Revenue assumptions.
* Cost assumptions.
* Margin assumptions.
* Working capital assumptions.
* CAPEX.
* Depreciation.
* Tax assumptions.
* Capital structure.
* Beta.
* ERP.
* Country risk premium.
* Cost of debt.
* WACC.
* Terminal value.
* Valuation methodology.
* Scenario assumptions.
* Model structure and relevant variables.

No important assumption may be hidden or inaccessible.

2.3 AI recommendations are not facts

Every AI-generated assumption must be distinguishable from:

* Reported historical data.
* Management guidance.
* External market data.
* Analyst estimates.
* User-entered assumptions.
* AI-generated estimates.
* Calculated outputs.

The platform must never present an unsupported estimate as an observed fact.

2.4 Deterministic financial calculations

The AI must NOT be responsible for calculating financial model outputs through free-form reasoning.

Use a deterministic calculation engine.

The AI proposes assumptions and model structures. The calculation engine executes formulas. The audit engine verifies the outputs.

All calculations must be reproducible.

2.5 Full transparency

Every material assumption must have:

* Value.
* Unit.
* Currency, where applicable.
* Forecast period.
* Source.
* Source date.
* Methodology.
* Explanation.
* Confidence level.
* Status.
* User modification history.

2.6 No fake functionality

Never create buttons, workflows, integrations, data sources, or features that appear functional but are not implemented.

If a feature is unavailable, communicate that limitation clearly.

Never invent financial data, sources, citations, or model results.

⸻

3. CORE PRODUCT ARCHITECTURE

Design the application around independent, modular engines.

ENGINE A — DATA INTELLIGENCE ENGINE

Responsible for collecting, validating, normalizing, and organizing company information.

Required capabilities:

* Company identification.
* Ticker resolution.
* Exchange identification.
* Currency identification.
* Financial statement extraction.
* Annual reports.
* Quarterly reports.
* Regulatory filings.
* Investor presentations.
* Management guidance.
* Earnings call transcripts, where available.
* Segment disclosures.
* Market capitalization.
* Enterprise value.
* Debt information.
* Cash and equivalents.
* Shares outstanding.
* Historical market prices.
* Relevant macroeconomic indicators.
* Industry-specific operating statistics.

Initial source priorities:

Brazil:

* CVM.
* B3.
* Company investor relations websites.
* Public financial statements.
* Official company filings.
* Banco Central do Brasil.
* IBGE.
* ANEEL and other relevant regulators.

United States:

* SEC EDGAR.
* Company 10-K and 10-Q filings.
* Company investor relations websites.
* Official earnings releases.
* FRED and other authoritative macroeconomic sources.

International:

* Relevant securities regulators.
* Company annual reports.
* Official company disclosures.
* Appropriate market data providers.

Design a provider abstraction layer so new data sources can be added without rewriting the platform.

Every retrieved data point must preserve its source and retrieval date.

Implement source prioritization and conflict resolution.

When two sources disagree, flag the discrepancy instead of silently choosing one.

Do not assume that an API is free, available, or licensed for commercial use. Clearly document data provider costs, usage restrictions, rate limits, and commercial licensing requirements.

ENGINE B — COMPANY INTELLIGENCE ENGINE

The AI must deeply understand each company before building the financial model.

Required analytical tasks:

1. Business model analysis.
2. Revenue stream identification.
3. Segment analysis.
4. Geographic exposure.
5. Customer concentration.
6. Supplier dependencies.
7. Pricing power.
8. Competitive advantages.
9. Competitive positioning.
10. Industry structure.
11. Regulatory exposure.
12. Cyclicality.
13. Seasonality.
14. Capital intensity.
15. Management strategy.
16. Historical acquisitions and divestitures.
17. Operational risks.
18. Growth opportunities.
19. Structural industry trends.
20. Relevant macroeconomic dependencies.

Produce a structured Company Intelligence Report.

The report must contain:

* Business overview.
* Segment descriptions.
* Revenue composition.
* Competitive landscape.
* Industry outlook.
* Historical performance.
* Growth drivers.
* Key risks.
* Management strategy.
* Critical valuation considerations.

All important statements must have sources or be explicitly identified as analytical interpretations.

The user must be able to edit the report, correct the AI, add information, and request a new analysis based on those corrections.

ENGINE C — INDUSTRY INTELLIGENCE ENGINE

Build an industry classification and analytical framework.

The system must identify the appropriate sector and industry-specific variables.

Examples:

MINING:

* Production volume.
* Commodity prices.
* Realized prices.
* Product quality.
* Ore grades.
* Recovery rates.
* Production costs.
* C1 costs.
* Freight.
* Royalties.
* Sustaining CAPEX.
* Expansion CAPEX.
* Reserves.
* Mine life.
* Depletion.
* Commodity price sensitivities.

SAAS / SOFTWARE:

* ARR.
* MRR.
* New customer acquisition.
* Customer churn.
* Net revenue retention.
* Gross revenue retention.
* ARPU.
* CAC.
* LTV.
* Subscription growth.
* Gross margins.
* Hosting costs.
* R&D expenditure.
* Sales and marketing expenditure.
* Rule of 40.
* Customer concentration.

RETAIL:

* Same-store sales growth.
* Store openings.
* Store closures.
* Sales per square meter.
* Average ticket.
* Transaction volume.
* Average selling price.
* Inventory turnover.
* Gross margin.
* Rent.
* Store-level EBITDA.
* Working capital.

UTILITIES:

* Regulated asset base.
* Allowed returns.
* Regulatory WACC.
* Tariff adjustments.
* Energy volumes.
* Capacity.
* Utilization.
* Contracted revenue.
* Regulatory review cycles.
* Maintenance CAPEX.
* Expansion CAPEX.

INDUSTRIAL MANUFACTURING:

* Production capacity.
* Utilization rate.
* Sales volume.
* Average selling price.
* Product mix.
* Raw material costs.
* Labor costs.
* Energy costs.
* Manufacturing efficiency.
* Backlog.
* CAPEX.
* R&D.

OIL AND GAS:

* Production volume.
* Reserves.
* Realized oil and gas prices.
* Lifting costs.
* Decline rates.
* Drilling CAPEX.
* Development CAPEX.
* Royalties.
* Decommissioning obligations.
* Commodity sensitivities.

TELECOMMUNICATIONS:

* Subscribers.
* ARPU.
* Churn.
* Data consumption.
* Network utilization.
* Spectrum costs.
* Infrastructure CAPEX.
* EBITDA margins.

CONSTRUCTION AND REAL ESTATE:

* Land bank.
* Launches.
* Sales velocity.
* Average selling price.
* Construction costs.
* Gross margin.
* Inventory.
* Delivery schedule.
* Net debt.
* Development pipeline.

BANKS AND FINANCIAL INSTITUTIONS:

* Loan portfolio.
* Net interest income.
* Net interest margin.
* Cost of risk.
* Non-performing loans.
* Deposits.
* Capital adequacy.
* Regulatory capital.
* Fee income.
* Efficiency ratio.
* Return on equity.

INSURANCE:

* Premiums.
* Claims.
* Loss ratio.
* Expense ratio.
* Combined ratio.
* Underwriting profitability.
* Investment income.
* Solvency capital.

These are examples, not exhaustive templates.

The system must discover additional variables whenever the specific company requires them.

It must support multi-segment businesses and different operational models within the same company.

⸻

4. VARIABLE COMPLETENESS PROTOCOL

This is one of the most important components of the entire platform.

Before generating a financial model, the AI must perform a comprehensive variable discovery process.

For every company:

1. Identify all potentially relevant operational variables.
2. Identify all relevant financial variables.
3. Identify relevant macroeconomic variables.
4. Identify regulatory variables.
5. Identify extraordinary and non-recurring variables.
6. Identify relationships between variables.
7. Determine materiality.
8. Determine whether each variable can be quantified.
9. Determine the source or estimation methodology.
10. Explain which variables are excluded and why.

Build a Variable Registry.

Each variable must contain:

* Variable ID.
* Name.
* Description.
* Category.
* Unit.
* Historical values.
* Forecast values.
* Source.
* Formula, if applicable.
* Dependency relationships.
* Materiality classification.
* Confidence level.
* User override status.

Classify variables as:

* Critical.
* Material.
* Secondary.
* Non-material.

The system must not add unnecessary complexity merely to make the model appear sophisticated.

The objective is to capture every material economic driver without introducing irrelevant variables.

Implement a dependency graph that links operating variables to financial statements and valuation outputs.

Example:

Production volume × Realized selling price = Revenue.

Revenue × Gross margin = Gross profit.

Gross profit − Operating expenses = EBITDA.

EBITDA − D&A = EBIT.

EBIT × (1 − Tax rate) = NOPAT, subject to appropriate tax adjustments.

NOPAT + D&A − CAPEX − Change in NWC = FCFF, with appropriate treatment of other operating items.

The system must dynamically generate these relationships based on the company's business model.

⸻

5. FINANCIAL MODELING ENGINE

Build a flexible model generator.

The system must not depend on one universal template.

It must generate the required financial structure based on the company and the selected valuation methodology.

5.1 Historical financial analysis

Collect and organize preferably 5–10 years of historical information, depending on availability and relevance.

Support:

* Income statement.
* Balance sheet.
* Cash flow statement.
* Segment information.
* Operating KPIs.
* Debt schedules.
* Share count.
* Capital structure.

Analyze:

* Revenue growth.
* Gross profit.
* EBITDA.
* EBIT.
* Net income.
* Margins.
* ROIC.
* ROE.
* ROA.
* Working capital.
* CAPEX.
* D&A.
* FCF conversion.
* Leverage.
* Liquidity.
* Cash conversion.

Identify accounting inconsistencies, extraordinary items, impairments, restructuring, acquisitions, disposals, and other relevant adjustments.

Distinguish reported and normalized financials.

Never overwrite reported financial statements with adjusted values.

5.2 Three-statement model

Implement an integrated three-statement model where applicable.

Income Statement:

* Revenue.
* COGS.
* Gross profit.
* SG&A.
* R&D.
* Other operating expenses.
* EBITDA.
* D&A.
* EBIT.
* Financial income and expenses.
* EBT.
* Taxes.
* Net income.

Balance Sheet:

* Cash.
* Accounts receivable.
* Inventory.
* Other current assets.
* PP&E.
* Intangible assets.
* Goodwill.
* Accounts payable.
* Debt.
* Other liabilities.
* Equity.

Cash Flow Statement:

* Net income.
* D&A.
* Non-cash adjustments.
* Changes in working capital.
* Operating cash flow.
* CAPEX.
* Acquisitions and disposals.
* Financing activities.
* Debt issuance and repayment.
* Dividends.
* Change in cash.

All statements must be connected through formulas.

Implement balance sheet checks and cash flow reconciliations.

5.3 Revenue forecasting

The AI must determine the appropriate revenue forecasting methodology.

Possible approaches:

* Price × Volume.
* Segment-level projections.
* Customer × ARPU.
* ARR-based forecasting.
* Same-store sales.
* Production-based forecasting.
* Capacity × Utilization × Price.
* Contracted revenue.
* Backlog conversion.
* Geographic forecasting.
* Organic growth plus acquisitions.

Use the methodology best suited to the company.

Avoid mechanically extrapolating historical growth.

5.4 Cost and margin forecasting

Identify the appropriate cost drivers.

Model:

* COGS.
* SG&A.
* R&D.
* Personnel.
* Raw materials.
* Energy.
* Logistics.
* Rent.
* Other operating expenses.

Support fixed, variable, semi-variable, and step-function costs.

Use segment-level margin assumptions where appropriate.

5.5 Working capital

Support individual assumptions for:

* DSO.
* DIO.
* DPO.
* Other receivables.
* Other payables.
* Deferred revenue.
* Contract assets.
* Contract liabilities.

Calculate working capital consistently with the business model.

Avoid double-counting and inappropriate treatment of cash, debt, and financing-related balances.

5.6 CAPEX and depreciation

Distinguish:

* Maintenance CAPEX.
* Expansion CAPEX.
* Regulatory CAPEX.
* Growth CAPEX.
* Replacement CAPEX.
* Acquisition-related investments.

Model PP&E and depreciation using appropriate schedules when data permits.

Support asset lives, depreciation methods, commissioning dates, and asset categories.

5.7 Taxation

Model effective tax rates, statutory rates, deferred taxes, tax losses, tax incentives, and relevant jurisdiction-specific items where applicable.

The platform must distinguish accounting taxes from cash taxes.

Do not apply a simplistic tax percentage when the company's circumstances require a more detailed treatment.

⸻

6. VALUATION ENGINE

The initial priority is DCF, but the architecture must support other valuation methods.

6.1 DCF — FCFF

Build a complete unlevered DCF model.

Include:

* Revenue.
* EBITDA.
* EBIT.
* Taxes on operating income.
* NOPAT.
* D&A.
* CAPEX.
* Change in NWC.
* Other relevant operating cash flow adjustments.
* FCFF.
* Discount factors.
* Present value of forecast cash flows.
* Terminal value.
* Enterprise value.
* Net debt and other relevant adjustments.
* Equity value.
* Diluted shares outstanding.
* Implied share price.

All calculations must be formula-driven.

6.2 DCF — FCFE

Support levered free cash flow valuation where appropriate.

Include:

* Net income.
* D&A.
* CAPEX.
* Working capital.
* Net borrowing.
* Equity cash flows.
* Cost of equity.
* Terminal value.
* Equity value.

Prevent mixing FCFF with cost of equity or FCFE with WACC.

6.3 WACC ENGINE

Build a detailed cost of capital module.

Cost of Equity:

* Risk-free rate.
* Beta.
* Equity Risk Premium.
* Country Risk Premium, when applicable.
* Additional risk adjustments, where justified.
* Cost of equity.

CAPM and justified extensions must be supported.

Beta methodologies:

* Historical regression beta.
* Levered beta.
* Unlevered beta.
* Peer-derived beta.
* Relevered beta.

Peer selection must be transparent.

Cost of Debt:

* Existing debt cost.
* Market borrowing rates.
* Credit spreads.
* Synthetic ratings where justified.
* Tax shield.
* Pre-tax and after-tax cost of debt.

Capital Structure:

* Market-value equity.
* Debt.
* Preferred stock, if applicable.
* Appropriate weights.
* WACC.

Support different currencies, inflation assumptions, and nominal versus real valuation consistency.

For Brazil, support:

* NTN-F and NTN-B reference rates.
* Relevant Brazilian market risk data.
* Country risk premium methodologies.
* EMBI+ or other appropriate country-risk references.

Never mechanically add country risk to a discount rate without examining the methodology and avoiding double-counting.

All WACC assumptions must have explicit sources and dates.

6.4 TERMINAL VALUE

Support:

* Gordon Growth Model.
* Exit EBITDA Multiple.
* Other appropriate terminal methodologies.

Implement checks for:

* WACC versus perpetual growth.
* Terminal growth consistency.
* Terminal-year margins.
* Reinvestment requirements.
* Terminal ROIC.
* Implied terminal multiples.
* Terminal value contribution to enterprise value.

Flag unrealistic assumptions.

6.5 OTHER VALUATION METHODS

Design extensible modules for:

* Trading Comparables.
* Precedent Transactions.
* Sum-of-the-Parts.
* Dividend Discount Model.
* NAV.
* Residual Income.
* LBO valuation.

These methods can be implemented progressively, but the architecture must accommodate them.

Do not force DCF on businesses for which another valuation methodology is more appropriate.

For financial institutions, support sector-appropriate equity valuation methods rather than automatically applying an industrial FCFF model.

⸻

7. AUTONOMOUS AI ANALYST

The AI is the intellectual core of the product.

It must be capable of researching, reasoning, proposing, explaining, and challenging assumptions.

Use Claude through the Anthropic API, with a configurable model abstraction so that other AI providers can eventually be integrated.

Implement an orchestration system with specialized analytical roles.

Suggested agents:

1. Company Analyst.
2. Industry Analyst.
3. Accounting Analyst.
4. Operating Driver Analyst.
5. Forecast Analyst.
6. WACC Analyst.
7. Valuation Analyst.
8. Scenario Analyst.
9. Independent Audit Analyst.

These agents should produce structured outputs, not merely conversational text.

The orchestration layer must coordinate their work and resolve contradictions.

Do not assume that every task requires a separate AI call. Use structured workflows, context management, caching, and model selection to control latency and costs.

7.1 AI assumption generation

For each assumption, the AI must provide:

* Suggested value.
* Historical reference.
* Industry benchmark, if relevant.
* Management guidance, if available.
* External evidence.
* Reasoning.
* Methodology.
* Confidence.
* Key risks.
* Alternative assumptions.

Example:

Revenue growth, Year 1:

* AI suggestion: 9.5%.
* Historical growth: 8.2%.
* Management guidance: 8–10%.
* Industry expectation: 7.5%.
* Rationale: segment expansion and pricing.
* Confidence: Medium.

The example is illustrative.

7.2 Analytical reasoning

The AI must challenge its own conclusions.

Examples:

* Is revenue growth consistent with market growth?
* Is projected market share achievable?
* Does CAPEX support the forecast production capacity?
* Are margins consistent with historical performance?
* Does the model adequately reflect operating leverage?
* Is working capital consistent with revenue growth?
* Are depreciation assumptions consistent with the asset base?
* Does terminal growth exceed reasonable long-term economic assumptions?
* Is the implied valuation consistent with peer multiples?
* Are assumptions internally consistent?

7.3 No fabricated certainty

If the AI lacks sufficient information, it must:

1. Identify the missing information.
2. Explain why it matters.
3. Provide a reasonable estimation methodology, if possible.
4. Flag the uncertainty.
5. Ask the user for input when necessary.

It must never silently fill missing information with invented historical data.

⸻

8. FULLY EDITABLE USER WORKSPACE

This is a fundamental product requirement.

The user must be able to edit every stage of the valuation process.

Build a professional financial modeling interface.

Required sections:

1. Company Overview.
2. Business Analysis.
3. Industry Analysis.
4. Historical Financials.
5. Accounting Adjustments.
6. Variable Registry.
7. Operating Assumptions.
8. Revenue Forecast.
9. Cost Forecast.
10. Working Capital.
11. CAPEX and D&A.
12. Tax.
13. Three-Statement Model.
14. WACC.
15. DCF.
16. Terminal Value.
17. Scenario Manager.
18. Sensitivity Analysis.
19. Valuation Summary.
20. Audit and Validation.
21. Excel Export.
22. AI Research Report.

Every section must allow editing, subject to appropriate data validation and user permissions.

8.1 Editable assumptions

Every assumption must support:

* Direct numeric input.
* Textual explanation.
* Source attachment or URL.
* Unit selection.
* Forecast period selection.
* AI suggestion.
* User override.
* Reset to AI suggestion.
* Historical comparison.
* Version history.

Support percentage, currency, absolute values, per-unit values, multiples, days, volume, and other appropriate units.

8.2 AI Suggested vs. User Assumptions

For each assumption, maintain:

* AI Suggested Value.
* User Assumption.
* Active Value.
* Original Value.
* Source.
* Explanation.
* Modification timestamp.

The user must be able to accept, reject, or modify the AI suggestion.

An AI-generated value must never overwrite a user-approved assumption without explicit authorization.

8.3 Assumption status

Use clear visual indicators:

* AI Suggested.
* User Modified.
* Source Verified.
* Historical Actual.
* Calculated.
* Needs Review.
* Unverified.

Do not use visual indicators as a substitute for explaining the underlying status.

8.4 AI-assisted editing

Allow natural-language instructions such as:

"Assume revenue grows 12% annually for the next three years."

"Reduce gross margin by 150 basis points in 2028."

"Assume a 100 bps increase in WACC."

"Model a 20% increase in CAPEX due to the new production facility."

The AI must translate the instruction into structured assumption changes.

Before committing a change, show exactly which assumptions and model components will be affected.

Support preview, approval, rejection, and undo.

⸻

9. SCENARIO MANAGER

Build a fully editable scenario system.

Default scenarios:

* Bull Case.
* Base Case.
* Bear Case.

Each scenario must have its own assumptions.

The user must be able to:

* Edit all assumptions independently.
* Duplicate scenarios.
* Create custom scenarios.
* Rename scenarios.
* Compare outcomes.
* Set scenario probabilities.
* Calculate weighted valuation.
* Save and restore scenario versions.

Support scenario narratives such as:

* Market expansion.
* New product launch.
* Acquisition.
* Recession.
* Commodity price shock.
* Regulatory change.
* Margin compression.
* New production capacity.
* Currency depreciation.

The AI should translate the event into a set of interconnected assumptions.

Example:

"Model a recession in Brazil."

The system should consider the company's specific exposure to:

* Domestic demand.
* Interest rates.
* FX.
* Inflation.
* Credit conditions.
* Customer activity.
* Pricing power.
* Operating leverage.

It must not apply identical macroeconomic impacts to every company.

⸻

10. SENSITIVITY ANALYSIS

Build interactive sensitivity tools.

At minimum:

* WACC versus perpetual growth.
* WACC versus Exit EBITDA Multiple.
* Revenue growth versus EBITDA margin.
* Revenue growth versus WACC.
* CAPEX versus revenue growth.
* Other company-specific sensitivities.

Allow users to choose the variables and ranges.

Display:

* Enterprise Value.
* Equity Value.
* Implied Share Price.
* Upside/Downside.
* Key assumptions.

Support tornado charts, scenario comparisons, and dynamic valuation tables.

The sensitivity engine must recalculate using the actual underlying model.

Do not generate sensitivities using approximate or disconnected calculations.

⸻

11. EXCEL GENERATION AND SYNCHRONIZATION

This is a major product feature.

Generate professional, institutional-quality Excel models.

Excel must be a genuine financial model, not a static export of values.

Required characteristics:

* Native Excel formulas.
* Linked worksheets.
* Clear formatting.
* Professional number formats.
* Consistent currency and units.
* Historical and forecast periods.
* Formula-driven calculations.
* Assumption highlighting.
* Source comments or references.
* Error checks.
* Model integrity checks.
* Sensitivity tables.
* Scenario support.

Suggested worksheets:

1. Cover.
2. Company Overview.
3. Historical Financials.
4. Operating Assumptions.
5. Revenue Build.
6. Cost Build.
7. Working Capital.
8. CAPEX & D&A.
9. Three Statements.
10. WACC.
11. DCF.
12. Sensitivities.
13. Scenarios.
14. Valuation Summary.
15. Sources & Assumptions.

The exact workbook structure must be adaptable to the company.

11.1 Excel synchronization

The user should be able to edit assumptions inside the platform and export an updated workbook.

Design a robust synchronization architecture so that changes made in Excel can also be imported into the platform.

Preserve:

* Formula integrity.
* Assumption metadata.
* Source references.
* Scenario definitions.
* Model versions.

Do not claim real-time two-way synchronization unless it is actually implemented and tested.

If external Excel editing creates conflicts, provide a clear reconciliation workflow.

Never allow a spreadsheet import to silently overwrite approved platform assumptions.

11.2 Excel quality

Use a recognizable financial modeling convention:

* Blue font: hardcoded inputs.
* Black font: formulas within the workbook.
* Green font: links to other worksheets.
* Appropriate negative-number formatting.
* Zero values displayed consistently.
* Clear section headers.
* Units in headers.
* Forecast periods clearly differentiated.

Make formatting configurable.

All formulas must be inspectable.

Where possible, test workbook formulas using a compatible spreadsheet calculation engine and validate outputs against the platform's calculation engine.

⸻

12. VALUATION REPORT GENERATOR

Generate professional valuation reports.

Required content:

1. Executive Summary.
2. Company Overview.
3. Industry Overview.
4. Historical Financial Performance.
5. Key Operating Drivers.
6. Forecast Methodology.
7. Main Assumptions.
8. WACC Methodology.
9. DCF Valuation.
10. Terminal Value.
11. Sensitivity Analysis.
12. Scenario Analysis.
13. Comparable Companies, where relevant.
14. Key Risks.
15. Valuation Conclusion.
16. Sources and Disclosures.

Every material conclusion must be supported by data or identified as an analytical judgment.

Allow the user to choose report language and detail.

Support Portuguese and English initially.

⸻

13. INDEPENDENT AUDIT ENGINE

Build a separate validation layer.

The audit engine must examine the financial model independently of the AI agent that constructed it.

It should identify:

* Broken formulas.
* Missing data.
* Incorrect signs.
* Inconsistent currencies.
* Unit mismatches.
* Incorrect tax treatment.
* Inconsistent forecast periods.
* Incorrect debt treatment.
* FCFF and FCFE inconsistencies.
* WACC calculation errors.
* Terminal value errors.
* Incorrect discount factors.
* Balance sheet imbalances.
* Cash flow reconciliation errors.
* Double-counted adjustments.
* Unexplained assumptions.
* Unsupported projections.
* Implausible margins.
* Unrealistic terminal growth.
* Excessive terminal value contribution.
* Inconsistent implied valuation multiples.

Implement deterministic checks wherever possible.

The AI audit agent may also identify conceptual and economic inconsistencies.

Produce an Audit Report with:

* Error.
* Severity.
* Location.
* Explanation.
* Expected correction.
* Suggested resolution.
* Resolution status.

Classify findings as:

* Critical.
* High.
* Medium.
* Low.
* Informational.

The system must never declare a model fully validated while critical errors remain unresolved.

⸻

14. USER EXPERIENCE AND DESIGN

Build a premium, institutional financial software interface.

Design inspiration:

* Bloomberg Terminal.
* Capital IQ.
* FactSet.
* Modern investment banking financial modeling software.
* Professional equity research platforms.

However, create an original visual identity.

Design principles:

* Sophisticated.
* Minimalist.
* Dense but readable.
* Professional.
* Fast.
* Data-oriented.
* Responsive.
* Easy to navigate.

Avoid excessive animations, oversized cards, decorative elements, and consumer-finance aesthetics.

The user should be able to navigate large models efficiently.

Required interface elements:

* Sidebar navigation.
* Company search.
* Model workspace.
* Assumption tables.
* Editable financial grids.
* Charts.
* Scenario manager.
* AI assistant panel.
* Audit panel.
* Source panel.
* Export controls.
* Version history.

Use clear visual distinctions between:

* Actuals.
* Forecasts.
* AI suggestions.
* User assumptions.
* Calculated outputs.

Support dark and light modes.

The platform must be usable on desktop first, with responsive support for smaller screens.

⸻

15. TECHNICAL ARCHITECTURE

Inspect the current development environment before choosing the final architecture.

If the repository is empty, use the following preferred stack unless a strong technical reason justifies a change.

Frontend:

* Next.js.
* React.
* TypeScript.
* Professional component system.
* Interactive financial tables and charts.

Backend:

* Python.
* FastAPI.
* Pydantic.
* Modular service architecture.

Database:

* PostgreSQL.
* SQLAlchemy or an equivalent ORM.
* Database migrations.

Calculation Engine:

* Python.
* Explicit financial formulas.
* Dependency graph.
* Versioned model inputs.
* Deterministic calculations.

AI:

* Anthropic Claude API.
* Configurable model selection.
* Structured outputs.
* Tool calling.
* Context management.
* Retry and error handling.
* Token and cost monitoring.

Excel:

* openpyxl or an appropriate workbook-generation library.
* Formula-based workbook architecture.
* Import/export validation.

Background Processing:

* Appropriate job queue for research and model-generation tasks.
* Persistent job status.
* Retry policies.
* Cancellation.
* Progress tracking.

Data Storage:

* Raw source records.
* Normalized financial data.
* Assumption metadata.
* Model versions.
* Audit logs.
* Generated workbooks and reports.

Infrastructure:

* Environment variables.
* Secure API key handling.
* Structured logging.
* Error monitoring.
* Automated testing.

Do not expose API keys in frontend code.

Do not hardcode secrets.

Use migrations and reproducible development environments.

Keep external data providers replaceable through interfaces.

⸻

16. FINANCIAL DATA MODEL AND INTERNAL SCHEMAS

Create a structured internal representation of the financial model.

At minimum, define entities for:

* Company.
* Security.
* Industry.
* Segment.
* FinancialStatement.
* FinancialPeriod.
* FinancialMetric.
* OperatingDriver.
* VariableDefinition.
* VariableValue.
* Assumption.
* AssumptionSource.
* AssumptionVersion.
* Model.
* ModelVersion.
* ForecastPeriod.
* FinancialFormula.
* FormulaDependency.
* Scenario.
* ScenarioAssumption.
* ValuationMethod.
* ValuationResult.
* SensitivityTable.
* AuditFinding.
* ResearchDocument.
* SourceRecord.
* ExcelArtifact.

All entities must have appropriate identifiers, timestamps, and version relationships.

Use a schema that allows different industries to introduce new operating variables without changing the entire database architecture.

The financial calculation engine must support:

* Different currencies.
* Different fiscal year ends.
* Annual and quarterly periods.
* Actual and forecast periods.
* Multiple reporting standards.
* Different units.
* Historical restatements.
* Consolidated and segment-level financials.

Define a robust unit and currency system to prevent invalid calculations.

⸻

17. ACCOUNTING AND FINANCIAL MODELING STANDARDS

Implement appropriate support for:

* IFRS.
* US GAAP.
* Brazilian accounting standards.
* IFRS 16.
* Lease accounting.
* Minority interests.
* Goodwill.
* Impairments.
* Deferred taxes.
* Pension liabilities.
* Non-controlling interests.
* Diluted shares.
* Stock-based compensation.
* Exceptional items.
* Acquisitions and divestitures.

Avoid treating different accounting standards as identical.

Implement explicit normalization rules and document their assumptions.

The platform must distinguish Enterprise Value from Equity Value correctly.

It must handle cash, debt, leases, minority interests, investments, and other non-operating adjustments consistently with the chosen valuation framework.

⸻

18. SECURITY, USERS AND PROJECT MANAGEMENT

Build a foundation for commercial SaaS deployment.

Support:

* User authentication.
* Individual workspaces.
* Multiple valuation projects.
* Project duplication.
* Model version history.
* User permissions.
* Secure document storage.
* API key protection.
* Audit logs.

Prepare for future team collaboration and role-based access control.

Users must not access other users' financial models or documents without authorization.

Implement tenant isolation and appropriate security controls.

⸻

19. PERFORMANCE AND COST CONTROL

The product must be economically viable.

Implement:

* AI response caching where appropriate.
* Research caching.
* Financial data caching.
* Structured AI context.
* Selective model invocation.
* Background processing.
* Rate-limit management.
* Token monitoring.
* AI usage accounting.
* Cost estimates per valuation.

Do not send the entire financial history and research corpus to Claude for every small calculation.

The deterministic calculation engine should handle ordinary user edits without unnecessary AI calls.

The AI should be invoked for reasoning-intensive tasks, not arithmetic that can be performed reliably in code.

⸻

20. QUALITY ASSURANCE AND TESTING

Testing is mandatory.

Create automated tests for:

Financial formulas:

* Revenue calculations.
* EBITDA.
* EBIT.
* NOPAT.
* FCFF.
* FCFE.
* Working capital.
* CAPEX.
* D&A.
* WACC.
* Discount factors.
* Terminal value.
* Enterprise value.
* Equity value.
* Implied share price.

Model integrity:

* Balance sheet balancing.
* Cash flow reconciliation.
* Formula dependency consistency.
* Scenario independence.
* Assumption overrides.
* Currency consistency.
* Unit consistency.

Excel:

* Workbook generation.
* Formula references.
* Worksheet integrity.
* Input formatting.
* Formula consistency.
* Export/import behavior.

AI:

* Structured output validation.
* Source verification.
* Missing data handling.
* Conflicting evidence.
* Invalid assumptions.
* Tool errors.
* Hallucination-resistant workflows.

Create at least three comprehensive demonstration cases:

1. A mining company.
2. A SaaS/software company.
3. A retail or industrial company.

Use documented historical data and clearly identified illustrative forecast assumptions.

Do not use fabricated historical financial statements as real data.

Build benchmark cases with independently calculated expected financial outputs.

⸻

21. DEVELOPMENT ROADMAP

Build this product progressively.

Do not attempt to implement the entire vision in one uncontrolled coding operation.

PHASE 0 — REPOSITORY AND ARCHITECTURE AUDIT

* Inspect the existing repository.
* Understand the development environment.
* Identify installed dependencies.
* Create the technical architecture.
* Identify risks.
* Create the implementation plan.
* Establish coding standards.
* Define the core financial data schemas.

Deliver:

* Architecture documentation.
* Database design.
* Technical roadmap.
* Development environment.

PHASE 1 — CORE FINANCIAL ENGINE

Build:

* Financial data structures.
* Financial formulas.
* Dependency graph.
* DCF FCFF.
* DCF FCFE.
* WACC.
* Terminal value.
* Sensitivities.
* Scenario calculations.
* Validation framework.

The financial calculation engine must be testable independently of the UI and AI.

PHASE 2 — DATA INTELLIGENCE

Build:

* Company identification.
* Financial statement ingestion.
* Data normalization.
* Source management.
* Historical analysis.
* Financial data validation.

Start with Brazilian and US public companies.

PHASE 3 — AI INTELLIGENCE

Build:

* Company Analyst.
* Industry Analyst.
* Driver Analyst.
* Forecast Analyst.
* WACC Analyst.
* Valuation Analyst.
* Audit Analyst.

Implement the Variable Completeness Protocol.

PHASE 4 — EDITABLE WORKSPACE

Build the entire interactive modeling environment.

All material assumptions must be editable.

Implement:

* AI Suggested vs. User Assumptions.
* Scenario Manager.
* Version history.
* Natural-language editing.
* Live deterministic recalculation.

PHASE 5 — EXCEL AND REPORTING

Build:

* Excel generation.
* Excel import.
* Synchronization and conflict resolution.
* Valuation reports.
* Sources and assumptions reports.

PHASE 6 — COMMERCIAL FOUNDATION

Build:

* Authentication.
* Workspaces.
* Project management.
* Permissions.
* Usage monitoring.
* SaaS-ready architecture.

Do not prioritize billing or marketing pages before the financial product works correctly.

⸻

22. FIRST MVP ACCEPTANCE CRITERIA

The MVP is not complete until a user can:

1. Enter a publicly listed company ticker.
2. Retrieve and validate available historical financial information.
3. Receive an AI-generated business and industry analysis.
4. See the complete material variable registry.
5. Review the proposed model structure.
6. Review and edit all material assumptions.
7. Generate company-specific forecasts.
8. Calculate a complete FCFF DCF.
9. Inspect and modify the WACC.
10. Create and modify Bull, Base, and Bear cases.
11. See sensitivities recalculate from the underlying model.
12. Change any assumption and immediately see the valuation update.
13. Ask Claude to explain the impact of an assumption change.
14. Export a formula-driven Excel workbook.
15. Run an independent model audit.
16. Review the source and methodology behind every important assumption.

A valuation must never be presented as institutionally reliable merely because the system successfully generated a workbook.

The quality of the underlying data, assumptions, model integrity, and independent validation determines the reliability of the result.

⸻

23. HOW YOU SHOULD WORK AS CLAUDE CODE

You are not being asked to simply generate a proposal or a mockup.

You are being asked to build a functioning product.

Follow these instructions:

1. Inspect the repository before modifying anything.
2. Do not destroy existing files or overwrite useful code without understanding it.
3. Create an implementation plan.
4. Establish the core architecture.
5. Implement the project incrementally.
6. Run tests after each major implementation.
7. Fix errors before proceeding.
8. Keep documentation updated.
9. Use modular, maintainable code.
10. Avoid unnecessary abstraction.
11. Never create fake data integrations.
12. Never claim that an incomplete feature works.
13. Do not skip financial formula validation.
14. Do not use AI for deterministic arithmetic.
15. Do not hardcode company-specific logic into a supposedly universal engine.
16. Do not build a universal DCF template and call it autonomous valuation.
17. Preserve full user control over assumptions.
18. Keep financial calculations reproducible.
19. Track the provenance of every material input.
20. Make reasonable technical decisions independently instead of repeatedly asking for permission on minor implementation details.

When encountering an ambiguous financial modeling decision, document the issue, implement a defensible default where possible, and expose the choice to the user.

When encountering missing external credentials or paid data providers, build the provider interface and clearly report the missing configuration. Never simulate a successful live connection.

Do not stop after producing an attractive frontend.

The core financial engine, data structures, AI orchestration, editable workspace, and model validation are the actual product.

⸻

24. FINAL PRODUCT STANDARD

The final product should feel like a combination of:

* A senior investment banking analyst.
* An equity research analyst.
* A financial modeling specialist.
* An industry research analyst.
* A quantitative financial engineer.
* An independent model auditor.

The AI must understand that valuation is not about choosing a discount rate and applying a growth percentage.

Valuation requires understanding the economics of a business, its competitive position, capital requirements, financial structure, reinvestment needs, risk profile, and long-term ability to generate cash flows.

Every company deserves an appropriately designed model.

Every important assumption must be explainable.

Every user must retain control.

Every financial output must be reproducible.

Every model must be auditable.

The ultimate objective: build the most intelligent, transparent, flexible, and analytically rigorous AI-powered valuation platform possible.

Start with Phase 0, inspect the environment, and then execute the roadmap systematically.

Do not compromise financial rigor for visual appearance or speed of implementation.
