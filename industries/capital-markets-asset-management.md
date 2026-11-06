# Capital Markets & Asset Management

## Overview
Broker-dealers, banks' markets divisions, custodians and asset managers spend effort on post-trade operations (matching, settlement, collateral, corporate actions), fund accounting and NAV control, regulatory reporting and surveillance. Manual work concentrates in exception queues: a trade or position does not agree across two systems or counterparties, and an operations analyst must find out why, contact the counterparty and fix the record before a deadline.

Verification note (2026-11-06): only the figures tagged below were checked against pages. Regulation names and dates in this file (SEC rules, MiFID II, EMIR REFIT, MAR, UMR etc.) were not re-checked against official text and should be read as unconfirmed.

## Systems of record, regulations, public datasets
- **Systems:** order/execution management (OMS/EMS), portfolio accounting and fund-accounting platforms, custodian and prime-broker feeds, SWIFT, DTCC CTM/NSCC/DTC, trade repositories (DTCC, Regis-TR), collateral management, market-data/pricing vendors, surveillance platforms, KYC/onboarding systems, EDGAR filing agents.
- **Regulations/standards:** SEC Rule 22c-1 and Rule 2a-5 (fund pricing and fair value); Rule 30e-1 and Form N-1A tailored shareholder reports (2022 adopting release 33-11125); Reg NMS Rules 605/606; FINRA Rule 5310 best execution; MiFID II RTS 27/28 and MiFIR transaction reporting; EMIR REFIT (2024) derivative reporting; MAR (2014) STORs; UMR/BCBS-IOSCO margin rules (2015); SEC T+1 settlement (May 2024); CSDR settlement discipline; SEC Rule 17a-4 recordkeeping; AML/CIP rules for broker-dealers.
- **Public datasets (URLs not opened unless in Sources):**
  - SEC EDGAR full-text and bulk (N-PORT data sets): https://www.sec.gov/dera/data/form-n-port-data-sets
  - SEC Rule 605 execution quality data: https://www.sec.gov/data-research/sec-markets-data/rule-605-equity-market-center-statistics
  - DTCC equities statistics: https://www.dtcc.com/equity-trade-volume-insights
  - ESMA registers and data quality reports: https://www.esma.europa.eu/
  - GLEIF LEI data: https://www.gleif.org/en/lei-data/gleif-golden-copy
  - Synthetic trades/Kaggle stock datasets for price history; ISDA SIMM public docs: https://www.isda.org/

Open-source note: GitHub repository search (stars>=20, not archived, keyword queries, 2026-11-06) is a limited, noisy search; "none found" means no relevant hit in that query, not that none exist.

## Use cases

### 1. Trade break and settlement-fail resolution
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer: broker-dealer/asset-manager operations. Systems: OMS, DTCC CTM/SWIFT confirmations, custodian instruction feeds, SSI database, internal books. Regulation: SEC T+1 (2024), CSDR penalties in EU, Reg SHO close-out. Human: ops manager approves amendments/cancel-correct and counterparty outreach on material breaks.
- **Problem and today's workflow:** Analysts compare internal trades to counterparty/custodian data, identify the cause (price, quantity, SSI, allocation, missing instruction), contact counterparties and amend before the settlement cutoff, now one day shorter under T+1.
- **Evidence:** SIFMA/ICI/DTCC T+1 after-action report release (opened, 12 Sep 2024): nearly 95% of transactions met affirmation criteria by DTC's 9:00 PM ET trade-date cutoff, up from 73% at end of January 2024; July 2024 average CNS fail rate 2.12% and DTC non-CNS 3.31%. https://www.dtcc.com/news/2024/september/12/sifma-ici-and-dtcc-release-t1-after-action-report [Verified]
- **Agent design:** Tools: break feed query, SSI lookup, counterparty email/portal, SWIFT/CTM amend API, ticketing. Steps: classify break cause, propose fix, draft counterparty message, track to resolution. Gate: human approves amendments above a notional threshold and any cancel/rebook.
- **Open source today:** none found (gh search "trade break", stars>=20: only unrelated trading-bot hits).
- **Demo path:** Synthetic trade file plus counterparty file with injected breaks (price, quantity, SSI, date), scored on cause-classification accuracy.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 2. Fund NAV reconciliation and pricing-exception review
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer: fund administrator or asset manager middle office. Systems: fund-accounting platform, custodian positions/cash, pricing vendors (ICE, Bloomberg, Refinitiv class), corporate actions feed, trade blotter. Regulation: Rule 22c-1 (forward pricing), Rule 2a-5 (valuation designee), Board reporting of material pricing errors. Human: fund accountant and valuation committee approve overrides and NAV release.
- **Problem and today's workflow:** Daily, accountants reconcile positions and cash to custodian, review price tolerance breaches and stale prices, and decide whether an override is needed before striking the NAV.
- **Evidence:** The cited Seward & Kissel blog URL is an archive listing with no article text, so the earlier 0.5% NAV materiality and Nov 2022 SEC mismarking-case claims are not confirmed and are removed. Reference, not confirmed: https://40actblog.sewkis.com/blog/sec-seeks-special-master-in-case-involving-nav-mismarking-scheme [Unconfirmed] No industry cost figure found.
- **Agent design:** Tools: position/cash recon queries, vendor price comparison, corporate-action lookup, tolerance rules, issue log. Steps: investigate each break, propose resolution with evidence, compute NAV impact. Gate: accountant approves overrides; NAV sign-off remains human.
- **Open source today:** matthius-titanmarkets/daily-nav (0 stars, no licence, not archived, last push 2026-04-15, README read: yes; a one-line README "Build automated daily NAV reconciliation pipeline" - not a solution); elitraOS/nav-reconciliation (0 stars, no licence, not archived, last push 2026-03-30, README read: no README present). Both are hobby-level and adjacent only.
- **Demo path:** Synthetic fund with positions, prices, custodian file; inject stale prices and missed splits.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 3. Institutional counterparty and fund KYC onboarding
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer: prime brokerage, custodian, fund administrator onboarding. Systems: CLM/KYC platform, fund offering documents, registries, GLEIF, sanctions screening, CRM. Regulation: CIP/CDD rules, FATF, FinCEN investment adviser AML rule (as finalised/postponed; check current status - not verified). Human: onboarding/compliance approves risk rating and account opening.
- **Problem and today's workflow:** Analysts collect constitutional documents, identify the manager, GP, investors and controllers of funds, screen them and resolve missing documents across email chains.
- **Evidence:** No cost or time figure found. Background only: the FinCEN consolidated CDD FAQs (opened, text extracted) align with exceptive relief order FIN-2026-R001 of 13 Feb 2026. https://www.fincen.gov/system/files/2026-05/CDD-Rule-Consolidated-FAQs.pdf [Verified] (regulatory background, not a volume figure)
- **Agent design:** Tools: document extraction, registry/LEI lookup, screening, checklist engine, outreach drafts. Gate: compliance approves rating and exceptions.
- **Open source today:** StephenAbbott/opencheck (21 stars, NOASSERTION, not archived, last push 2026-11-05, README read: yes (start); LEI/GLEIF-based customer due diligence checks - adjacent, relevant to entity lookup only; see banking-lending use case 3).
- **Demo path:** GLEIF relationship records and SEC Form ADV/N-PORT filer data to build fund-structure scenarios.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 4. Fund shareholder-report and prospectus compliance review
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer: fund complex legal/compliance and financial reporting. Systems: fund accounting, document composition (EDGARization), EDGAR, Form N-1A/N-CSR/N-PORT preparation, performance data. Regulation: Rule 30e-1 tailored shareholder reports, Form N-1A, Marketing Rule. Human: fund counsel and CCO approve filing.
- **Problem and today's workflow:** Teams assemble per-share-class reports, check fees, performance and holdings data against source systems and prior filings, and reconcile narrative against disclosures.
- **Evidence:** PolicyRisk summary of the Federal Register notice (opened): open-end funds "average 107 hours each" under Rule 30e-1; the SEC's revised total annual burden estimate is "1,437,523 hours and $174,614,292 in (reported) costs". Corrected: the earlier "$62,060 per fund" does not appear on the page (it matches a division of figures, so it is derived, not stated) and is removed. The page itself notes the cost line items do not add up to the $174.6M total, so treat that dollar figure with caution. https://policyrisk.com/federal-register/2026-07777 [Corrected] (secondary aggregator, SEC PRA estimate)
- **Agent design:** Tools: EDGAR retrieval, data-vs-document comparison, XBRL/inline tag validator, redline. Steps: compare each number and statement to source, flag mismatches, draft changes. Gate: counsel approves every change; agent never files.
- **Open source today:** none found (gh search "shareholder report", stars>=20: only unrelated hits).
- **Demo path:** Public N-CSR/N-1A filings from EDGAR with N-PORT data sets; seed mismatches.
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 5. Best-execution review and TCA exception analysis
- **Tier:** B. Enterprise: needs figure
- **Enterprise check:** Buyer: broker-dealer and buy-side compliance/trading. Systems: OMS/EMS, venue/algo routing logs, market data, TCA. Regulation: FINRA Rule 5310, Reg NMS 605/606, MiFID II RTS 28 and best-execution policy. Human: Best Execution Committee signs reviews.
- **Problem and today's workflow:** Analysts run periodic execution quality statistics, pick outliers, collect the order context and write the rationale for exceptions.
- **Evidence:** FINRA 2019 exam findings report (opened): firms that do not review each order must run a "regular and rigorous" review at least quarterly by security and order type; reviews omitted factors such as speed of execution and price improvement. Corrected: Regulatory Notice 26-15 (July 2026) is not mentioned on that page and could not be confirmed, so it is removed. https://finra.org/rules-guidance/guidance/reports/2019-report-exam-findings-and-observations/best-execution [Corrected]
- **Agent design:** TCA models and rules identify outliers; agent assembles order timeline, routing logs and market state, drafts the review note. Gate: committee approves conclusions.
- **Open source today:** none found (gh search "best execution", stars>=20: only unrelated hits).
- **Demo path:** SEC Rule 605 public statistics plus simulated order flow.
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 6. Trade and communications surveillance alert review
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer: markets compliance. Systems: surveillance engine, order/trade data, e-comms and voice archives, HR/watch lists. Regulation: MAR (STORs), FINRA 5210/5270/5320-class rules, Rule 17a-4 retention. Human: compliance officer decides STOR/SAR escalation.
- **Problem and today's workflow:** Analysts review alerts (spoofing, front-running, wash trades), pull orders, chat and news, and write closure rationale.
- **Evidence:** ESMA STOR report of Dec 2025 (opened, text extracted): "NCAs received 5,981 STORs in 2024, a 8% decrease"; the UK accounted for 50% and 43% of all STORs received in 2017 and 2018, and the aggregate fell sharply after 2018 mainly due to Brexit. Corrected: the earlier counts of 10,653 (2017) and 11,130 (2018) were not found in the report and are removed. https://www.esma.europa.eu/sites/default/files/2025-12/ESMA74-268544963-1554_Report_on_Suspicious_Transaction_and_Order_Reports__STORs_.pdf [Corrected]
- **Agent design:** Tools: order-book reconstruction, comms search, news timeline, case management. Gate: officer closes or escalates; legal review for STOR filings.
- **Open source today:** none found (gh search "trade surveillance", stars>=20: only crypto-bot/whale-watcher hits, not market-abuse surveillance).
- **Demo path:** Public LOB data (LOBSTER sample) with injected spoofing patterns.
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 7. Transaction-reporting break remediation (EMIR REFIT / MiFIR)
- **Tier:** B. Enterprise: needs figure
- **Enterprise check:** Buyer: derivatives operations/regulatory reporting. Systems: trade capture, reporting engine, trade repository feeds, reference data (LEI, ISIN/UTI). Regulation: EMIR REFIT (Apr 2024), MiFIR Art. 26; data-quality scrutiny by ESMA/NCAs. Human: reporting manager approves resubmissions and error notifications.
- **Problem and today's workflow:** Teams reconcile rejects and mismatches from repositories, correct fields (UTI, LEI, valuation) and file correction reports.
- **Evidence:** The World Exchanges article (opened) says the ESMA 2024 data quality report notes "improvements in rejection rates" but does not contain the rejection figures (about 20%, 1-2.5%, 1.4%) cited earlier; those are removed. Reference, not confirmed: https://focus.world-exchanges.org/articles/esmas-2024-data-quality-report [Unconfirmed] (primary ESMA report not opened)
- **Agent design:** Tools: repository reject feeds, reference-data lookup, rule lookup, resubmission API. Gate: manager approves bulk corrections and regulator notifications.
- **Open source today:** none found (gh search "EMIR reporting", stars>=20: 0 hits).
- **Demo path:** Synthetic EMIR trade reports with injected field errors validated against ESMA validation rules.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 8. Collateral and margin dispute resolution (UMR/VM)
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer: collateral management teams. Systems: collateral platform (e.g., AcadiaSoft class), valuation/exposure engines, CSA/ISDA agreements, custodians. Regulation: BCBS-IOSCO uncleared margin rules, EMIR RTS, ISDA CSA terms. Human: collateral manager approves dispute positions and agreed amounts.
- **Problem and today's workflow:** When margin calls differ from counterparty figures, analysts trace to trade-level valuation, CSA terms (thresholds, eligible collateral) and exchange breaks by email.
- **Evidence:** Clarus FT (opened): "Total Uncleared IM has more than doubled in the three years from 2020 to 2023, from $218bn to $462bn." https://www.clarusft.com/?p=34021 [Verified] This is exposure growth, not dispute volume; no dispute-rate figure found.
- **Agent design:** Tools: portfolio recon, agreement term lookup, valuation comparison, email drafts. Gate: manager approves settlement of disputed amounts.
- **Open source today:** none found (gh search "collateral margin", stars>=20: only unrelated crypto hits).
- **Demo path:** Synthetic portfolios with valuation differences and CSA parameters.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 9. Corporate actions event processing and entitlement checks
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer: custodian/asset-manager ops. Systems: golden-source reference data, corporate-action vendor feeds, SWIFT ISO 15022 messages, position keeping, custodian notifications. Regulation: SEC/market practice standards (SMPG/ISO 20022), client mandate rules. Human: ops approves elections on voluntary events.
- **Problem and today's workflow:** Staff reconcile conflicting event notices from several sources, determine terms, calculate entitlements and instruct elections before deadlines.
- **Evidence:** No reliable figure found. [Unconfirmed]
- **Agent design:** Tools: notice parser, source comparison, entitlement calculator, election instruction writer. Gate: human approves elections and any golden-copy override.
- **Open source today:** none found (gh search "corporate actions", stars>=20: only unrelated hits).
- **Demo path:** EDGAR 8-K/merger documents as events; synthetic holdings.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

## Sources
- https://www.dtcc.com/news/2024/september/12/sifma-ici-and-dtcc-release-t1-after-action-report (opened)
- https://40actblog.sewkis.com/blog/sec-seeks-special-master-in-case-involving-nav-mismarking-scheme (opened; no article text)
- https://www.fincen.gov/system/files/2026-05/CDD-Rule-Consolidated-FAQs.pdf (opened, text extracted)
- https://policyrisk.com/federal-register/2026-07777 (opened)
- https://finra.org/rules-guidance/guidance/reports/2019-report-exam-findings-and-observations/best-execution (opened)
- https://www.esma.europa.eu/sites/default/files/2025-12/ESMA74-268544963-1554_Report_on_Suspicious_Transaction_and_Order_Reports__STORs_.pdf (opened, text extracted)
- https://focus.world-exchanges.org/articles/esmas-2024-data-quality-report (opened; figures not found)
- https://www.clarusft.com/?p=34021 (opened)
- Dataset URLs listed above (not opened).
