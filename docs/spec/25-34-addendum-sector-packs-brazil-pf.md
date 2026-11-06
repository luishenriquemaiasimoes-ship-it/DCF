ADDENDUM — SECTOR PACKS, BRAZIL, PROJECT FINANCE & LESSONS LEARNED

Where this addendum is more specific than the sections above, this addendum prevails.

The platform is sector-agnostic. No sector is privileged in the core engine. The sector modules below (infrastructure, project finance, real estate) are EXAMPLES of how sector knowledge plugs in, written in more depth because the founder can validate them; they carry the same weight as mining, SaaS, retail, banks or any other sector.

⸻

25. SECTOR-AGNOSTIC CORE + SECTOR PACKS

25.1 Separation of concerns

* The CORE ENGINE knows only universal finance: periods, units, currencies, the dependency graph, three statements, FCFF/FCFE/DDM/RI, discounting, terminal value logic, debt schedules, scenarios, sensitivities, audit framework.
* SECTOR PACKS contain sector knowledge as data and configuration, not as branches in the core: variable templates, typical drivers and formulas, accounting peculiarities, sector KPIs, sector-specific audit checks, preferred valuation methods, typical data sources, and benchmark ranges with sources.
* The Company Intelligence and Industry Intelligence agents select, combine and adapt packs. A conglomerate or multi-segment company combines several packs (one per segment). When no pack fits, the AI builds the driver structure from first principles via the Variable Completeness Protocol and may propose a new pack.
* Adding a new sector must never require changing the core engine. Audit check: grep the core for sector names; any hit is a design violation.

25.2 Valuation archetypes

The core must natively support these economic archetypes, because they cut across sectors:

* Going concern with perpetual life (most industrials, retail, software, consumer).
* Finite-life assets (concessions, mines, oil & gas fields, patents and drug franchises, leases, contracted energy assets): value until the end of economic or contractual life, no perpetuity by default (Section 27.1).
* Financial institutions (banks, insurers, asset managers): equity-based valuation (FCFE/DDM/excess return/residual income), regulatory capital as the reinvestment constraint, no FCFF.
* Project-level / SPE valuation with project finance debt (Section 28), in any sector.
* Asset-based / NAV (real estate, holding companies, land, investment companies, reserves-based resources).
* Early-stage / negative cash flow businesses (high-growth tech, biotech): long explicit periods, path to steady-state margins, probability of survival/failure, dilution.
* Sum-of-the-parts for multi-segment and holding structures, mixing archetypes per segment.

25.3 Roadmap guardrail

Keep the original roadmap, but Phase 1 tests must cover at least three different archetypes from day one (e.g., a perpetual going concern, a finite-life asset, and a financial institution), so the engine is not unconsciously shaped around a single sector.

⸻

26. BRAZIL-SPECIFIC COST OF CAPITAL RULES

These rules exist because each of them was a real error in previous manual models. The WACC Analyst and the audit engine must enforce them.

26.1 Choose ONE coherent framework and declare it

Every model must state explicitly which framework it uses:

Framework A — Local nominal BRL:
* Risk-free = NTN-F (prefixado) yield, or the DI futures curve, matched to the duration of the cash flows.
* Cash flows in nominal BRL.
* The local yield already embeds Brazil sovereign risk. Do NOT add a full CRP on top without justification. If a CRP adjustment is applied (e.g., Damodaran's approach of local rf minus default spread, then adding CRP to equity), document it and show the arithmetic.

Framework B — Local real BRL:
* Risk-free = NTN-B (IPCA+) real yield, matched to duration.
* Cash flows in real BRL (constant prices), with no inflation in tariffs, costs or terminal growth.
* Typical for IPCA-indexed concession contracts.

Framework C — USD-based CAPM converted to BRL:
* Risk-free = US Treasury (10y or duration-matched).
* Add CRP (EMBI+ Brazil spread, CDS, or Damodaran CRP — choose and document; do not mix sources).
* Convert to nominal BRL via relative inflation (Fisher): (1 + Ke_USD) × (1 + π_BRL) / (1 + π_USD) − 1, using Focus/BCB expectations for π_BRL and a documented source for π_USD.

Hard rules:
* Never mix a real discount rate with nominal cash flows, or vice versa. The audit engine must check tariff indexation, cost inflation and terminal growth against the declared framework.
* Never use NTN-B with nominal cash flows (classic error).
* CRP appears exactly once, or zero times with explicit justification. Flag both "missing CRP under Framework C" and "double-counted CRP under Framework A" as Critical findings.

26.2 Beta

* Observed regression beta vs Ibovespa: show window (e.g., 2y weekly and 5y monthly), R², standard error, and number of observations. Low R² must be flagged.
* Bottom-up beta: unlever peer betas (Hamada: βu = βL / [1 + (1 − t) × D/E]) using each peer's market D/E and marginal tax rate, take median, relever at the target company's D/E.
* Brazilian marginal tax rate for relevering: 34% (IRPJ 25% + CSLL 9%) under Lucro Real, unless the entity has a different regime or incentive (Section 29).
* Show observed vs bottom-up side by side and let the user choose. Optional Blume adjustment, labeled.
* For concessions with declining leverage over the contract, support year-by-year relevered beta and Ke (or APV), instead of a single static WACC.

26.3 Weights

* Equity at MARKET value (shares outstanding × price on the valuation date, diluted).
* Debt at market value where observable, otherwise book; state which.
* Use the target or average-over-horizon capital structure for a going concern; for a single concession with amortizing project debt, use the contractual debt schedule.
* Weights must be consistent with the D/E used to relever beta. Audit check: D/(D+E) in WACC = D/E in Hamada, transformed.

26.4 Cost of debt

* Build from the actual debt stack: CDI + spread, IPCA + spread, prefixado, BNDES (TLP-based), foreign currency (with hedge treatment).
* Incentivized infrastructure debentures (Lei 12.431/2011 and later regime changes) price at lower coupons because of investor tax benefits; flag this when inferring market cost of debt from them.
* Convert all debt costs to the declared framework (nominal or real) before weighting.
* After-tax at the applicable marginal rate, only if the entity is profitable enough to use the tax shield (check projected EBT and loss carryforwards).

26.5 Sources and dates

Every WACC input carries source + date: Tesouro/ANBIMA curve (and the specific bond and maturity), B3 DI futures, BCB Focus, Damodaran datasets (ERP, CRP; note the update date), EMBI+, peer prices. Treat ANBIMA and B3 data licensing as something to verify before commercial use.

⸻

27. SECTOR PACK EXAMPLE — INFRASTRUCTURE CONCESSIONS

27.1 Finite-life rule (applies to every finite-life archetype, not only concessions)

* A finite-life asset (concession, mine, oil field, patent, contracted plant) is valued as the PV of cash flows until the end of its contractual or economic life, plus terminal items specific to the asset (contractual indemnity for non-amortized reversible assets, salvage value, or closure/decommissioning/abandonment costs, which are negative).
* Gordon Growth terminal value is NOT applied to a single finite-life asset. If the user wants a going-concern TV for the company that owns such assets, it must be explicitly modeled as "value of future assets not yet secured" (new concessions, reserves not yet discovered/certified, pipeline drugs), separately labeled, with its own assumptions (pipeline, expected return vs cost of capital). Default is zero.
* Life extensions (contract renewals, reserve additions, patent extensions) are scenarios, never base case without evidence.

27.2 Accounting (ICPC 01 / IFRIC 12, OCPC 05, IFRS 15)

* Distinguish intangible asset model vs financial asset model (and bifurcated).
* Construction revenue and construction cost (recognized with zero or near-zero margin) inflate reported revenue and EBITDA. Always compute "Adjusted EBITDA ex-construction" and use operating cash flows for valuation.
* Amortization of the concession intangible follows the curve of economic benefits (often traffic-based), not straight-line; model it explicitly because it drives taxes.
* Provisions for maintenance/restoration (provisão para manutenção) and concession fee payables (outorga a pagar) are debt-like items: include them in the EV-to-equity bridge, not in working capital.

27.3 Revenue — toll roads

* Traffic in equivalent vehicles (veículos equivalentes): light vs heavy, axle multipliers.
* Drivers: GDP, industrial production, agribusiness output (for freight corridors), fuel prices, regional development, competing routes; ramp-up curves for greenfield.
* Elasticities by vehicle type, sourced or estimated from historical regression, with R² shown.
* Tariff: base tariff × contractual readjustment (usually IPCA, with a specific anniversary date and formula), plus discounts/additions from performance factors (e.g., fator D, fator X, IDA-type indicators, depending on contract).
* Free flow: model evasion and collection losses.
* Accessory revenue separately.

27.4 Revenue — other infrastructure (support progressively)

* Sanitation: connections, volume billed, tariff by category, coverage targets of the regulatory framework, losses (perdas).
* Energy transmission: RAP (Receita Anual Permitida), readjustment index, periodic review, availability penalties (parcela variável).
* Airports: PAX, cargo, tariff per PAX, commercial revenue per PAX, variable concession fee.
* Ports and urban mobility: TEU/tonnage, passengers, contractual tariffs, demand risk sharing.

27.5 CAPEX

* Phased contractual CAPEX from the contract's investment program (e.g., PER for highways), including volume-triggered investments (gatilhos de investimento by traffic thresholds) that must be modeled dynamically as functions of the traffic forecast.
* Maintenance and restoration cycles (pavement, OAEs) as recurring schedules.
* Separate obligatory vs discretionary CAPEX.

27.6 OPEX

* Use audited data where available (e.g., independent auditor-verified cost reports), split fixed vs variable per km / per vehicle.
* Insurance, guarantees, regulatory fees, fixed and variable concession fees (outorga fixa / variável) as separate lines.

27.7 Regulatory economics

* Economic-financial rebalancing (reequilíbrio econômico-financeiro): model pending claims as scenarios with probability, never in base case without evidence.
* Marginal cash flow rate (taxa do fluxo de caixa marginal) for new investments added after signing: model new investments using the contractual or regulator-defined rate.
* Compare project IRR vs regulatory IRR vs WACC and show the spread.

27.8 Holding company (listed names)

* Sum-of-the-parts: each concession valued individually (FCFE at Ke with its own debt schedule, or FCFF at its WACC, consistently), times the company's stake.
* Minus PV of holding costs, holding-level net debt, and other debt-like items.
* Minority interests at their share of each asset's value, not at book.
* Show the contribution of each asset and its remaining contract life.

⸻

28. PROJECT FINANCE MODULE (ANY SECTOR) + PPP EXTENSION

Project finance is a cross-sector capability: energy plants, mines, real estate developments, infrastructure, industrial plants, data centers. Sections 28.3 and 28.4 apply to all of them. Sections 28.1 and 28.2 are the Brazilian PPP extension, which also lets the platform produce feasibility studies for municipalities and states.

28.1 Legal framework for PPPs and concessions (verify current versions before use)

* Lei 8.987/1995 (common concessions), Lei 11.079/2004 (PPPs: sponsored and administrative), Lei 14.133/2021 (procurement), sector frameworks (e.g., Lei 14.026/2020 sanitation).
* PPP fiscal limit: PPP expenses as a share of the entity's net current revenue (RCL), per Lei 11.079 — compute and display headroom.

28.2 SPE cash flow structure

* Revenues: user tariffs, contraprestação pecuniária (public payment), aporte de recursos (capital contribution during construction), accessory revenue.
* Performance-linked payments: availability and quality indicators reducing contraprestação.
* Guarantees: fundo garantidor, vinculação de receitas (e.g., FPM), escrow accounts — model their effect on credit risk qualitatively and in scenarios.

28.3 Debt sizing

* Size debt by DSCR (target minimum DSCR configurable; show typical lender ranges with source), tenor, grace period, repayment profile (constant, SAC, sculpted to target DSCR).
* Reserve accounts (DSRA, MRA), cash sweeps, distribution lock-up tests.
* Sources: BNDES, incentivized debentures, commercial banks, multilaterals.
* Show LLCR, PLCR, minimum and average DSCR.

28.4 Outputs

* Unlevered (project) IRR, levered (equity) IRR, NPV at WACC and at Ke, payback, maximum equity exposure.
* Minimum contraprestação or tariff that achieves a target equity IRR (goal seek done deterministically by the engine, not by the AI).
* Value for Money (Public Sector Comparator vs PPP), risk matrix (risk allocation between public and private parties) as structured outputs.
* Sensitivity: demand, CAPEX overrun, construction delay, interest rates, inflation, tariff readjustment lag.

⸻

29. BRAZILIAN TAX MODULE

All rates below must be stored as dated, sourced parameters (not constants in code), because the law changes. Verify current legislation before every release.

* Lucro Real: IRPJ 15% + 10% surcharge above the annual threshold + CSLL 9% (standard rate for non-financial companies).
* Lucro Presumido: presumed margins by activity; common in small SPEs. Model both when relevant and let the user choose.
* Tax loss carryforwards: offset limited to 30% of taxable income per year; no expiry. Track the balance.
* Regional incentives (SUDENE / SUDAM): reduction of IRPJ on operating profit for qualifying projects, with expiry date. Relevant for Northeast/North assets.
* JCP (juros sobre capital próprio): deductibility and limits depend on current law; model as a parameter with its own source.
* PIS/COFINS (cumulative vs non-cumulative) and ISS on services, until replaced.
* Consumption tax reform (EC 132/2023 and implementing laws): CBS/IBS transition schedule. Model the transition years explicitly for revenue-sensitive businesses; flag contract rebalancing implications for concessions.
* Cash tax vs accounting tax: deferred taxes from concession intangible amortization, construction margin, and provisions.

⸻

30. REAL ESTATE & LAND VALUATION MODULE

Support land and development valuation, including raw land (glebas).

30.1 Methods

* Comparative method (método comparativo direto de dados de mercado), following ABNT NBR 14653 concepts: sample of comparables, homogenization factors (area, location, topography, frontage, access), statistical treatment, valuation range.
* Residual land value method (método involutivo): GDV/VGV of the hypothetical development − construction cost − infrastructure − soft costs − sales costs − taxes − developer's required margin/IRR → maximum price a developer can pay for the land.
* Discounted cash flow of the development with sales absorption curve.

30.2 Variables

* Total area, buildable area (aproveitamento), zoning, environmental restrictions (APP, legal reserve, coastal restrictions), permitted density, number of units/lots, infrastructure needs.
* Unit prices per m² by product type, absorption pace, construction cost (CUB as a reference, plus regional premium), timeline for approvals.
* Taxes: RET for incorporação under patrimônio de afetação (rate stored as parameter), ITBI, capital gains for the seller.
* Deal structures: cash sale, permuta física (land for units), permuta financeira (land for % of VGV), earn-outs. Compare the seller's PV under each structure.

30.3 Hospitality

* Keys, ADR, occupancy, RevPAR, GOP margin, management fees, FF&E reserve, cost per key, stabilized yield/cap rate, ramp-up.
* For boutique hotel buyers, compute the maximum land price from the hotel's target IRR, analogous to the residual method.

⸻

31. ADDITIONAL AUDIT CHECKS (KNOWN ERROR CATALOGUE)

Add these deterministic checks to the audit engine. Each one is a past real error.

Critical:
* Real/nominal mismatch between discount rate, cash flows and terminal growth.
* CRP missing (Framework C) or double counted (Framework A).
* FCFF discounted at Ke, or FCFE discounted at WACC.
* WACC weights at book equity value instead of market value.
* WACC weights inconsistent with the D/E used to relever beta.
* Gordon TV applied to a finite-life asset without explicit going-concern justification.
* Pass-through or non-cash revenue included in EBITDA used for margins or multiples (e.g., construction revenue under IFRIC 12, gross vs net revenue in marketplaces/agents, fair-value gains in agribusiness or real estate).
* Debt-like items missing from the EV-to-equity bridge: IFRS 16 leases (consistently with whether EBITDA is pre- or post-IFRS 16), pensions, provisions for decommissioning/environmental/litigation where cash outflow is probable, concession fees payable, declared unpaid dividends/JCP, tax installment programs (parcelamentos), supplier finance (risco sacado / forfait) reclassified as debt.
* FCFF/WACC framework applied to a bank or insurer.

High:
* Perpetual growth ≥ long-term nominal GDP of the currency (or ≥ real GDP in a real framework).
* Terminal value > 75% of EV (configurable threshold) without explanation.
* Terminal ROIC inconsistent with reinvestment rate (g = reinvestment rate × ROIC).
* Base-year model figures not reconciling to reported actuals (tolerance configurable, e.g., ±1% on revenue, EBITDA, net debt).
* Basic instead of diluted shares; treasury shares not excluded.
* Minorities at book when market value is available.
* Tax shield applied in years with negative EBT.

Medium:
* Beta regression with low R² used without flag.
* Valuation date vs cash flow timing: no stub period, or end-of-year convention when mid-year is appropriate (make the convention explicit and selectable).
* Risk-free maturity not matched to cash flow duration.

Consensus check (informational, not a correctness test):
* Compare implied price to sell-side consensus range and to implied multiples (EV/EBITDA, P/E) of peers. If the result is outside the range, the system must explain which assumptions drive the gap. Matching consensus is NOT a goal; unexplained divergence is the problem.

⸻

32. BENCHMARK CASES — ONE PER ARCHETYPE

Expand Section 20's demo cases so the benchmark set covers every archetype in Section 25.2, mixing Brazilian and US companies. Suggested set (names are examples; swap for any company with good public data):

1. Perpetual going concern, Brazil: a retailer or consumer company (price × volume / same-store sales / store expansion build).
2. Perpetual going concern, US: a SaaS company (ARR, NRR, CAC, path to steady-state margins, SBC and dilution).
3. Commodity / finite reserves: a mining or oil & gas company (production × realized price, C1 costs, reserve life, decommissioning).
4. Finite-life contracted asset: a listed toll-road holding (e.g., ECOR3) valued by SOTP of concessions with no perpetuity.
5. Financial institution: a Brazilian bank (FCFE/excess return, Basel capital as reinvestment constraint, cost of risk).
6. Asset-based: a raw land parcel or real estate developer (residual land value, comparables, NAV).
7. Project finance: a single SPE (any sector) with DSCR-sized debt, levered vs unlevered IRR.

All historical data must be real and sourced. All forecast assumptions in benchmarks must be labeled illustrative. Expected outputs must be calculated independently (e.g., a separate hand-built spreadsheet) before being used as test fixtures.

⸻

33. BRAZILIAN DATA SOURCES (ADDITIONS TO ENGINE A)

Verify availability, terms and rate limits before integrating each:

* CVM Dados Abertos: DFP and ITR datasets, FRE (reference form), fatos relevantes.
* B3: prices, corporate actions, DI futures.
* Tesouro Nacional / ANBIMA: government bond yields and term structure (ETTJ).
* Banco Central: SGS time series API, Focus survey expectations.
* IBGE SIDRA: GDP, IPCA, industrial production, regional data.
* Sector regulators and statistics, loaded by the relevant sector pack: ANTT/ARTESP (roads), ANEEL (energy), ANP (oil & gas, fuels), ANM (mining), ANATEL (telecom), ANS (health insurance), SUSEP (insurance), BCB IF.data (banks), ANAC (airports), ANTAQ (ports), ANA (water), CONAB (agribusiness), ABRAS/IBGE PMC (retail), ABRAINC/SECOVI (real estate).
* Contract documents: concession contracts, PERs, bidding notices, amendments, rebalancing decisions.
* Damodaran Online datasets for ERP, CRP and industry betas (note the update date of each dataset).
* Municipal and state fiscal data (e.g., Siconfi) for RCL and PPP fiscal headroom.

⸻

34. OUTPUT CONVENTIONS FOR BRAZIL

* Default currency R$ millions; units in every header.
* Report language: Portuguese (PT-BR) by default for Brazilian companies and public-sector studies, English optional.
* Excel: formulas must work regardless of the user's locale (write formulas with openpyxl in English function names; Excel localizes on open). Number formats configurable to pt-BR (comma decimal) in display.
* Dates: DD/MM/YYYY in reports; ISO internally.
* Every output lists its valuation date, data cut-off date, and framework (Section 26.1) on the cover.
