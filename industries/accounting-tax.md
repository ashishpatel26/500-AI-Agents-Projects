# Accounting & Tax

## Overview
Finance, audit and tax teams spend effort on period close, reconciliations, payables control, audit evidence, and multi-jurisdiction tax compliance. Manual work concentrates in matching documents to ledger entries, reading contracts and notices, and compiling evidence for reviewers. Everything is subject to internal controls and auditor or tax-authority scrutiny.

## Systems of record, regulations, public datasets
- **Systems:** ERP (SAP, Oracle, NetSuite, Dynamics class), GL and subledgers, AP/procurement and e-invoicing, consolidation tools, contract repositories, tax engines, audit workpaper software, IRS transcripts and e-services, ESG data platforms.
- **Regulations/standards:** SOX 302/404 (2002); PCAOB AS 2110, AS 2201, AS 2401; AICPA SAS; ASC 606 / IFRS 15; OECD Pillar Two GloBE Model Rules (2021); OECD BEPS Action 13 transfer pricing documentation; IRC 7216 and Circular 230; CSRD (2022) with Omnibus revisions (adopted Dec 2025) and ESRS; ISSA 5000 / ISAE 3000 assurance.
- **Public datasets (URLs not opened):**
  - SEC Financial Statement Data Sets: https://www.sec.gov/dera/data/financial-statement-data-sets
  - IRS statistics of income and Taxpayer Advocate reports: https://www.irs.gov/statistics ; https://www.taxpayeradvocate.irs.gov/
  - Synthetic JE/AP data (generate); Kaggle invoice/receipt datasets
  - EDGAR contract exhibits (EX-10/EX-99): https://www.sec.gov/edgar
  - EFRAG ESRS drafts: https://www.efrag.org/

Open-source note: GitHub search was rate-limited during this run, so "Open source today" is limited.

## Use cases

### 1. Audit testing of journal entries and estimates
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: audit firms and internal audit. Systems: client ERP/GL extracts, audit workpaper platform, support documents. Regulation: PCAOB AS 2401, AS 2110, AICPA AU-C 240. Human: senior and engagement partner review and sign.
- **Problem and today's workflow:** Auditors sample entries, trace them to support, test estimates and document conclusions. Regulators repeatedly find insufficient evidence.
- **Evidence:** PCAOB inspection results for 2024 show a lower share of audits with Part I.A deficiencies (insufficient audit evidence) than 2023, and a lower Big Four rate. Exact percentages removed: the PCAOB PDF returned unreadable binary and the Deloitte DART page returned no text; only search-tool excerpts were seen. Reference, not confirmed: https://assets.pcaobus.org/pcaob-dev/docs/default-source/documents/staff-update-2024-inspection-activities-spotlight.pdf [Unconfirmed]
- **Agent design:** Tools: GL extract analytics, document retrieval, tie-out checks, workpaper writer. Steps: scan full population for risk criteria, trace selected entries, draft conclusions with evidence links. Gate: auditor judgement and partner review; agent output is not audit evidence by itself.
- **Open source today:** AICPA-AuditDataAnalytics2018/ADS---Python-Example- (50 stars, Apache-2.0, not archived, last push 2021-04-30; README read: yes; adjacent only: Jupyter notebooks for journal-entry audit procedures, not an agent).
- **Demo path:** Synthetic GL with injected anomalies (weekend, round-sum, manual-to-revenue entries).
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 2. Pillar Two (GloBE) data collection and top-up tax computation
- **Tier:** A | Enterprise: pass
- **Enterprise check:** Buyer: multinational group tax department. Systems: ERPs across countries, consolidation system, tax provision tool, GIR templates. Regulation: OECD GloBE Model Rules, local QDMTT/IIR laws, safe-harbour guidance. Human: tax director signs.
- **Problem and today's workflow:** Teams extract entity-level data, apply GloBE adjustments, test safe harbours and prepare the GloBE Information Return.
- **Evidence:** ZEW abstract: "total one-off costs of about EUR 1.2 billion (up to EUR 2.0 billion)" and "total recurring costs of EUR 517 million EUR p.a." (EU-headquartered groups only). https://www.zew.de/PU95713 [Verified]
- **Agent design:** Tools: ERP/consolidation queries, rule lookup per jurisdiction, adjustment calculator, reconciliation to financial statements. Gate: tax director approves positions and filings.
- **Open source today:** none found (one gh search, 'globe pillar', returned no hits).
- **Demo path:** Synthetic multi-entity group data using EDGAR segment/country disclosures.
- **Verification:** 2026-11-06, Verified, search done yes

### 3. IRS notice triage and response preparation
- **Tier:** A | Enterprise: pass
- **Enterprise check:** Buyer: tax practices and corporate tax departments. Systems: practice management, IRS e-Services transcripts, tax software. Regulation: Circular 230, IRC 7216 consent, statutory response deadlines. Human: CPA/EA reviews and signs.
- **Problem and today's workflow:** Staff read the notice, match to the return and transcripts, determine action and deadline and draft a reply.
- **Evidence:** National Taxpayer Advocate: "backlog of unprocessed amended returns stood at 0.5 million, but increased almost fourfold to 1.9 million" (0.5M at end of 2019; 1.9M as of late October 2023, so not January 2024). Opened via https://nysscpa.org/news/1046768-national-taxpayer-advocate-notes-progress-in-phone-service-and-reduced-backlog-but-says-challenges-remain-2024-01-11 ; NTA PDF itself unreadable. The 45-day correspondence figure was not found and is removed. [Corrected]
- **Agent design:** Tools: notice classifier, transcript retrieval, computation check, template drafting, deadline tracker. Gate: CPA/EA review; agent never sends.
- **Open source today:** none found (one gh search, 'IRS notice', returned no hits).
- **Demo path:** Synthetic notices (CP2000-style) with synthetic returns and transcripts.
- **Verification:** 2026-11-06, Corrected, search done yes

### 4. Month-end close and intercompany reconciliation
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: controller organizations. Systems: ERP/GL, intercompany module, bank feeds, consolidation. Regulation: SOX ICFR, segregation of duties. Human: controller approves journal entries.
- **Problem and today's workflow:** Accountants match intercompany balances, bank items and subledger differences, chase counterparties and book adjusting entries.
- **Evidence:** Close-time benchmarks in circulation come from vendor or secondary sources and are inconsistent; no figure confirmed. Reference, not confirmed: https://www.sfmagazine.com/articles/2023/september/the-financial-close-process-insights-from-europe (not opened). [Unconfirmed]
- **Agent design:** Tools: GL queries, matching rules, FX lookup, JE proposal. Gate: preparer-reviewer approval in ERP workflow; agent drafts only.
- **Open source today:** none found for close automation (gh search 'intercompany reconciliation': no hits). vas3k/TaxHacker (6,800 stars, MIT, not archived, last push 2026-10-31; README read: yes; adjacent only: self-hosted AI receipt/accounting app).
- **Demo path:** Synthetic multi-entity ledgers with injected FX and timing differences.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 5. US sales-tax exemption-certificate and nexus compliance
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: corporate indirect-tax teams. Systems: ERP/billing, tax engine, certificate repository, state portals. Regulation: state sales-tax law, Wayfair (2018) economic nexus thresholds. Human: tax manager approves.
- **Problem and today's workflow:** Staff collect and validate certificates per state and monitor nexus thresholds.
- **Evidence:** Number of US sales-tax jurisdictions: the cited Tax Foundation page failed to load twice (connection reset), so the earlier 11,000+ figure is removed. Reference, not confirmed: https://taxfoundation.org/data/all/state/state-sales-tax-jurisdictions-in-the-us-2020/ [Unconfirmed]
- **Agent design:** Tools: certificate OCR, state rule lookup, customer master query, threshold monitor. Gate: tax manager approves acceptance and registrations.
- **Open source today:** commerceguys/tax (287 stars, MIT, not archived, last push 2026-10-14; README read: yes; adjacent only: PHP tax-rate resolver library). Also adjacent rate calculators from search: valeriansaliou/node-sales-tax (339 stars), txcrb/tax_cloud (71 stars); READMEs not read.
- **Demo path:** Synthetic certificates and sales data with state thresholds.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 6. Accounts payable invoice exception handling (three-way match)
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: finance shared services. Systems: ERP AP module, PO/receiving, vendor master, invoice capture, payment run. Regulation: SOX controls, sales/VAT rules, sanctions on payments. Human: AP supervisor approves payment of exceptions.
- **Problem and today's workflow:** Clerks research price/quantity mismatches, missing PO or receipts, duplicate and suspicious invoices, and request approvals by email.
- **Evidence:** AP cost and exception-rate benchmarks: APQC page returned 403 and the 2026 Ardent and ACFE 2024 figures were not opened; search turned up only an SMB research site repeating a cross-industry median. All numbers removed. Reference, not confirmed: https://www.apqc.org/resource-library/resource-listing/accounts-payable-key-benchmarks-cross-industry [Unconfirmed]
- **Agent design:** Tools: ERP match queries, vendor history, duplicate detection, approver messaging. Gate: approver and AP supervisor; payment release remains in ERP workflow.
- **Open source today:** datpham0412/invoice-processor 'MatchFlow' (41 stars, MIT, not archived, last push 2025-07-03; README read: yes; adjacent only: invoice-to-PO matching web app, not an exception-handling agent).
- **Demo path:** Synthetic POs/receipts/invoices with injected mismatches and duplicates.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 7. Revenue-recognition contract review (ASC 606 / IFRS 15)
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: technical accounting teams. Systems: contract repository/CLM, CRM, billing, revenue subledger. Regulation: ASC 606, auditor review. Human: revenue accountant and controller approve accounting memo.
- **Problem and today's workflow:** Accountants read nonstandard contracts to identify performance obligations, variable consideration, and modifications, then draft memos and schedules.
- **Evidence:** Claim that revenue is among the most common audit-deficiency areas could not be confirmed: the PCAOB PDF was unreadable and no readable second source was opened. Reference, not confirmed: https://assets.pcaobus.org/pcaob-dev/docs/default-source/documents/staff-update-2024-inspection-activities-spotlight.pdf [Unconfirmed]
- **Agent design:** Tools: clause extraction, five-step checklist, schedule generator, precedent search. Gate: controller approves.
- **Open source today:** not checked (GitHub search rate-limited).
- **Demo path:** EDGAR EX-10 software/licensing agreements.
- **Verification:** 2026-11-06, Unconfirmed, repos not checked

### 8. Transfer pricing documentation (master file, local file, intercompany agreements)
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: multinational tax departments. Systems: ERP intercompany data, benchmarking databases, CbCR data, contract repository. Regulation: OECD BEPS Action 13 and local rules. Human: tax director approves positions.
- **Problem and today's workflow:** Teams compile functional analyses, intercompany transaction data and benchmarking for each jurisdiction's local file each year.
- **Evidence:** No quantified compliance-cost study found; the cited tpguidelines page was not opened. Reference, not confirmed: http://tpguidelines.com/category/transfer-pricing-guidelines/oecd-transfer-pricing-guidelines-2017/chapter-v-documentation/c-a-three-tiered-approach-to-transfer-pricing-documentation/ [Unconfirmed]
- **Agent design:** Tools: ERP data pulls, prior-year docs, local rule thresholds, drafting. Gate: tax director and advisor review.
- **Open source today:** none found (gh search 'transfer pricing' returned only unrelated repos).
- **Demo path:** Synthetic intercompany ledger and public company segment data.
- **Verification:** 2026-11-06, Unconfirmed, search done yes

### 9. ESG / CSRD sustainability data assurance
- **Tier:** B | Enterprise: needs figure
- **Enterprise check:** Buyer: sustainability reporting teams and assurance providers. Systems: ESG data platform, ERP/HR/energy data, supplier data, report drafts. Regulation: CSRD/ESRS, limited assurance. Human: sustainability controller and assurer sign.
- **Problem and today's workflow:** Teams collect data points from many sources, trace to evidence and reconcile with narrative disclosures.
- **Evidence:** CSRD scope and limited-assurance cost figures could not be confirmed: the Proskauer PDF was unreadable in fetch. Numbers (50 thousand entities; 15-30% cost) removed, as is the Omnibus adoption date, which is not confirmed. Reference, not confirmed: https://www.proskauer.com/insights/get-pdf/29494 [Unconfirmed]
- **Agent design:** Tools: data-point mapping, source tracing, consistency checks, evidence pack builder. Gate: assurer judgement.
- **Open source today:** climateandtech/report-analyst 'Open Sustainability Analyst' (41 stars, no licence declared, not archived, last push 2026-11-05; README read: yes; adjacent only: AI analysis of sustainability reports, not assurance).
- **Demo path:** Public sustainability reports with synthetic source data.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 10. SOX 404 control testing evidence collection
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: internal audit / SOX PMO. Systems: GRC tool, ERP, ticketing, access logs. Regulation: SOX 404, PCAOB AS 2201. Human: control owner and audit manager conclude.
- **Problem and today's workflow:** Testers request evidence from control owners, check against attributes and document exceptions.
- **Evidence:** PCAOB statement that ICFR deficiencies remain common not confirmed (PDF unreadable). Reference, not confirmed: https://assets.pcaobus.org/pcaob-dev/docs/default-source/documents/staff-update-2024-inspection-activities-spotlight.pdf [Unconfirmed]
- **Agent design:** Tools: ERP/access log queries, sampling, evidence request emails, workpaper writing. Gate: audit manager signs deficiencies.
- **Open source today:** none found (gh search 'sox compliance agent' returned no hits).
- **Demo path:** Synthetic user-access and approval logs.
- **Verification:** 2026-11-06, Unconfirmed, search done yes

## Sources
- https://assets.pcaobus.org/pcaob-dev/docs/default-source/documents/staff-update-2024-inspection-activities-spotlight.pdf
- https://www.zew.de/PU95713
- https://www.taxpayeradvocate.irs.gov/wp-content/uploads/2024/01/IR-2024-07.pdf
- https://www.sfmagazine.com/articles/2023/september/the-financial-close-process-insights-from-europe
- https://taxfoundation.org/data/all/state/state-sales-tax-jurisdictions-in-the-us-2020/
- https://www.apqc.org/resource-library/resource-listing/accounts-payable-key-benchmarks-cross-industry
- http://tpguidelines.com/category/transfer-pricing-guidelines/oecd-transfer-pricing-guidelines-2017/chapter-v-documentation/c-a-three-tiered-approach-to-transfer-pricing-documentation/
- https://www.proskauer.com/insights/get-pdf/29494
