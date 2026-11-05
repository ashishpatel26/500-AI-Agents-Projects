# Banking & Lending

## Overview
Banks spend most of their operating effort on financial-crime compliance (AML, sanctions, KYC), credit origination and monitoring, payments operations (disputes, trade documents) and recurring regulatory reporting. Manual work concentrates where an analyst must pull evidence from several systems, apply a policy or rulebook, and write a defensible narrative: alert dispositions, file review, memos, discrepancy notices. Every decision needs an audit trail and a named human approver.

Verification note (2026-11-06): only the figures tagged below were checked against pages. Regulation names and dates in this file were not re-checked against official text, except the FinCEN 13 Feb 2026 exceptive relief order FIN-2026-R001, which is confirmed in the FinCEN consolidated CDD FAQ text. Treat the rest (including the CFPB 15/60-day complaint timelines and the 10-business-day OFAC reporting window) as unconfirmed.

## Systems of record, regulations, public datasets
- **Systems:** core banking (Fiserv, FIS, Temenos, Jack Henry class), loan origination system (LOS) and servicing platform, document management/ECM, transaction-monitoring and sanctions-screening engines, KYC/CLM platform, case management, GL/regulatory reporting warehouse, card/payment processors, trade-finance platforms, credit-bureau and registry feeds.
- **Regulations/standards:** Bank Secrecy Act and FinCEN CDD Rule (2016, amended by exceptive relief 2026); OFAC sanctions regulations (31 CFR 500s); FATF Recommendations (2012, updated); Fed/OCC SR 11-7 model risk guidance (2011); ECOA/Reg B and Fair Housing Act; TILA/Reg Z and EFTA/Reg E (error resolution); Fannie Mae/Freddie Mac Selling Guides; ICC UCP 600 (2007) and ISBP 745 (2013); Basel III; FFIEC call report and FR Y-14/Y-9C instructions; GLBA.
- **Public datasets (demo use; URLs not opened unless noted in Sources):**
  - CFPB Consumer Complaint Database: https://www.consumerfinance.gov/data-research/consumer-complaints/
  - HMDA loan-level data: https://ffiec.cfpb.gov/data-browser/
  - OFAC SDN/consolidated lists: https://sanctionslist.ofac.treas.gov/ ; OpenSanctions: https://www.opensanctions.org/datasets/
  - IBM synthetic AML transactions (Kaggle): https://www.kaggle.com/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml
  - UK Companies House PSC bulk data: https://download.companieshouse.gov.uk/en_pscdata.html ; GLEIF Golden Copy: https://www.gleif.org/en/lei-data/gleif-golden-copy
  - SEC EDGAR / Financial Statement Data Sets: https://www.sec.gov/dera/data/financial-statement-data-sets
  - FFIEC call report bulk data: https://cdr.ffiec.gov/public/

Open-source note: GitHub repository search (stars>=20, not archived, keyword queries, 2026-11-06) is a limited, noisy search; "none found" means no relevant hit in that query, not that none exist.

## Use cases

### 1. AML transaction-monitoring alert investigation and SAR narrative drafting
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer: bank financial-crime unit. Systems: transaction-monitoring engine, KYC/CLM, core banking, case management, FinCEN BSA E-Filing. Regulation: BSA/AML, SAR confidentiality (no tipping-off), SR 11-7; every rationale logged. Human: analyst closes or escalates; BSA officer approves SAR filing.
- **Problem and today's workflow:** Analysts open each alert, pull customer profile, account history, counterparties and adverse media from separate tools, decide on escalation and hand-write the SAR narrative. Most effort goes into evidence gathering and repetitive narrative writing.
- **Evidence:** BPI report (opened): in 2017 survey participants "reviewed approximately 16 million alerts" and "filed over 640,000 suspicious activity reports"; among institutions that tracked it, a median 4% of SARs drew law-enforcement follow-up. https://bpi.com/getting-to-effectiveness-report-on-u-s-financial-institution-resources-devoted-to-bsa-aml-sanctions-compliance/ FinCEN infographic (opened, text extracted): approximate total of 4.6M SARs for FY23. https://fincen.gov/sites/default/files/shared/FinCEN_Infographic_Public_508FINAL_2024_June_7.pdf [Verified]
- **Agent design:** Tools: case-management read/write, KYC lookup, transaction query, counterparty/entity resolution, adverse-media search, typology library. Steps: assemble evidence pack, score against typologies, propose disposition, draft cited narrative. Gate: analyst decision plus BSA officer SAR approval; agent cannot file.
- **Open source today:** IBM/Multi-GNN (127 stars, Apache-2.0, not archived, last push 2025-09-18, README read: yes; GNN models for AML detection - adjacent only, upstream detection not triage). No alert-triage agent found.
- **Demo path:** IBM synthetic AML transaction dataset on Kaggle; generate synthetic alerts from labelled laundering patterns and have the agent produce a narrative scored against ground truth.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 2. Sanctions screening alert disposition (name-match adjudication)
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer: bank sanctions compliance. Systems: screening engine (payments and customer batch), SDN/consolidated lists, KYC data, payment messages (SWIFT MT/MX), case management. Regulation: OFAC strict-liability regime and 31 CFR 501 Appendix A enforcement guidelines (not re-checked); blocking/reject reports to OFAC within 10 business days (not re-checked). Human: sanctions analyst/officer approves release or block.
- **Problem and today's workflow:** Fuzzy name matching creates large alert volumes. Analysts compare list entry attributes (DOB, nationality, address, vessel IMO) against payment and KYC data and document why a hit is a false match.
- **Evidence:** No regulator-published false-positive rate was found. The earlier vendor-commentary range was not confirmed (ACAMS page returned HTTP 403 on fetch) and the numbers are removed. Reference, not confirmed: https://www.acamstoday.org/?p=22901 [Unconfirmed]
- **Agent design:** Tools: list-entry fetch, payment message parser, KYC lookup, secondary-identifier comparison, prior-decision memory (good-guy list). Steps: compare attributes, check prior dispositions, propose discount/escalate with evidence, write rationale. Gate: analyst approves discounts above a risk threshold; true-match candidates always go to a human; payment release is a separate human action.
- **Open source today:** Divine16/Sanctions-screening-benchmark (33 stars, MIT, not archived, last push 2026-08-13, README read: yes (start); benchmark of name-screening recall under name perturbations - adjacent only, an evaluation harness not a disposition agent). OpenSanctions data/matching library not re-checked (README read: no).
- **Demo path:** OFAC SDN list plus OpenSanctions data; synthesise payments with perturbed names and a few true hits.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 3. Beneficial-ownership and KYC refresh for legal-entity customers
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer: bank onboarding/KYC ops. Systems: CLM platform, corporate registries, GLEIF/LEI, document store, sanctions screening. Regulation: FinCEN CDD Rule (25% owners plus control person); FATF R.24/25. Human: KYC analyst and compliance approve risk rating and owner determination.
- **Problem and today's workflow:** Analysts trace ownership chains across registries and filings in many jurisdictions, reconcile with customer certifications, and re-do this at periodic or trigger-based review.
- **Evidence:** FinCEN consolidated CDD FAQs (opened, text extracted) re-issue the FAQs "to align with the exceptive relief order FinCEN issued on February 13, 2026 (FIN-2026-R001)". https://www.fincen.gov/system/files/2026-05/CDD-Rule-Consolidated-FAQs.pdf [Verified] No cost/time figure found.
- **Agent design:** Tools: registry APIs (Companies House PSC, GLEIF), document OCR, entity resolution, sanctions/PEP screen, CLM write. Steps: build ownership graph, compute effective ownership, flag gaps/triggers, draft determination memo. Gate: analyst approves; unresolved chains escalated.
- **Open source today:** StephenAbbott/opencheck (21 stars, licence NOASSERTION, not archived, last push 2026-11-05, README read: yes (start); LEI/GLEIF-based customer due diligence checks using open data and BODS - partially addresses the use case, closest); openownership/data-standard (82 stars, NOASSERTION, not archived, last push 2026-09-02, README read: yes (start); Beneficial Ownership Data Standard - adjacent only, a data schema). OpenKYC (ID/face verification) is a different problem.
- **Demo path:** UK PSC bulk data plus GLEIF relationship data; ask the agent to compute 25% owners for sampled companies and compare to registry-declared PSCs.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 4. Mortgage loan file underwriting and condition clearing
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer: mortgage lender/servicer. Systems: LOS (Encompass-class), DU/LPA findings, income/asset docs, appraisal, title, credit. Regulation: ECOA/Reg B, TRID, GSE Selling Guide reps and warranties, GLBA. Human: underwriter makes the credit decision and issues adverse action.
- **Problem and today's workflow:** Processors and underwriters verify income, assets and property documents against guidelines, issue conditions and chase borrowers for missing or conflicting documents.
- **Evidence:** Freddie Mac 2024 Cost to Originate study page (opened): "loan origination costs have risen 35%, or $3,000" over three years; lenders making heavy use of LPA digital capabilities originate loans that cost "$1,500 less". Corrected: the earlier "record $9,300 per loan" and "$2,200 lower, 5 days faster" were not on the opened page and are removed (a search summary suggested $9,300 comes from an earlier study, not opened). https://sf.freddiemac.com/articles/insights/2024-cost-to-originate-study [Corrected]
- **Agent design:** Tools: document classifier/extractor, LOS API, guideline lookup (Selling Guide), calculators (DTI, reserves), borrower messaging drafts. Steps: reconcile docs to 1003, find discrepancies, propose conditions with guide citations. Gate: underwriter approves decision; agent never issues approvals or adverse action.
- **Open source today:** confluentinc/workshop-mortgage-underwriting-agentic-system (40 stars, Apache-2.0, not archived, last push 2026-10-29, README read: yes (start); Confluent Cloud streaming multi-agent mortgage underwriting workshop - addresses the workflow as a vendor demo, not a production tool).
- **Demo path:** HMDA data for realistic loan attributes plus synthetic pay stubs/bank statements with injected discrepancies.
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 5. Commercial credit memo and financial-spreading preparation
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer: commercial bank credit department. Systems: spreading software, loan origination, core banking, financial statement PDFs, external data (bureaus, news). Regulation: SR 11-7 model governance, interagency credit risk guidance, fair lending for small business (ECOA, Section 1071). Human: analyst owns the memo; credit officer/committee approves.
- **Problem and today's workflow:** Analysts re-key borrower financials from PDFs into spreading tools, compute ratios, research industry and news and draft the memo for committee.
- **Evidence:** The Moody's case-study page (opened) refers to an unnamed "leading financial institution in the Asia-Pacific region" and gives no hours before/after. The earlier Taishin Bank "20 hours to 4" claim is not on the page and is removed. Reference, not confirmed: https://www.moodys.com/web/en/us/insights/lending/case-study-new-approach-corporate-credit-speed-flexibility-consistency.html [Unconfirmed]
- **Agent design:** Tools: table extraction, spreading template write, ratio engine, news/filing search, memo template. Steps: extract, tie out to totals, calculate, draft sections with cell-level citations. Gate: analyst reviews every figure; credit officer approval.
- **Open source today:** none found (gh search "credit memo", stars>=20: only unrelated Magento/RL hits).
- **Demo path:** SEC EDGAR Financial Statement Data Sets as borrower financials (mid-cap issuers), compare agent spreads to XBRL values.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 6. Loan covenant compliance monitoring
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer: commercial/CRE lender, agent bank. Systems: loan servicing system, credit agreements (PDF), borrower compliance certificates and financials, covenant tracking sheet, risk-rating system. Regulation: interagency credit-risk and CRE monitoring expectations; internal risk-rating policy. Human: relationship manager/credit officer decides waiver, reservation of rights or downgrade.
- **Problem and today's workflow:** Staff read credit agreements to find financial covenant definitions, recompute ratios from quarterly financials, compare with certificates, and track reporting deadlines in spreadsheets.
- **Evidence:** Penn State repository page (opened): abstract states "monitoring is positively related to future covenant violations and loan renegotiations" (Journal of Financial Economics, 2021). https://pure.psu.edu/en/publications/bank-monitoring-evidence-from-syndicated-loans/ [Verified] Academic support only; no dollar or time figure for manual covenant testing.
- **Agent design:** Tools: contract clause extraction, financial statement extraction, ratio recomputation using agreement-specific definitions, deadline calendar, draft notice letters. Gate: credit officer approves any breach notice, waiver or rating change.
- **Open source today:** 100xopensource/100x-credit-monitoring (25 stars, Apache-2.0, not archived, last push 2026-11-03, README read: yes (start only); AI-assisted private-credit monitoring plugin built around borrower reporting and loan documents - partially addresses the use case; coverage of covenant definitions not confirmed).
- **Demo path:** Public credit agreements filed as EDGAR exhibits (EX-10) with the same borrower's 10-Q financials; agent recomputes leverage/coverage tests.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 7. Trade finance documentary-credit examination (letters of credit)
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer: bank trade-services operations. Systems: trade-finance platform, SWIFT MT700/MX messages, scanned presentations (invoice, bill of lading, insurance, certificates), sanctions/vessel screening. Regulation: ICC UCP 600, ISBP 745, sanctions and dual-use controls. Human: documentary examiner decides compliance; officer approves refusal notice within the 5 banking days limit (UCP 600 timing not re-checked).
- **Problem and today's workflow:** Examiners check each presented document against LC terms and rules, list discrepancies and send refusal or acceptance advice. Highly manual and multilingual.
- **Evidence:** ICC Technical Advisory Briefing No. 3 (2022, opened, text extracted): "the global percentage of documents refused on first presentation under documentary credits ranges between 65-80%". Corrected: the earlier "about 70% in the UCP 600 foreword" was not checked and is dropped. https://library.iccwbo.org//content//tfb//BRIEFINGS//20220627_TA_Briefing_No3_reducing_discrepancy_rates.pdf [Corrected]
- **Agent design:** Tools: document OCR/extraction, LC terms parser, UCP/ISBP rule checks, vessel/party sanctions screening, discrepancy notice template. Gate: examiner confirms discrepancies; officer signs off refusal and payment.
- **Open source today:** HyperledgerHandsOn/trade-finance-logistics (193 stars, Apache-2.0, not archived, last push 2026-03-29, README read: yes (start); blockchain letter-of-credit/shipment demo - adjacent only, not document examination). No examination agent found.
- **Demo path:** Synthetic LC and document set generated from templates with injected discrepancies (date, quantity, port, description mismatch).
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 8. Regulatory reporting data reconciliation and submission review (call report, FR Y-9C/Y-14)
- **Tier:** B. Enterprise: pass
- **Enterprise check:** Buyer: bank finance/regulatory reporting. Systems: GL, subledgers, regulatory reporting warehouse, call-report/FR Y software, data lineage tools. Regulation: FFIEC 031/041 call report, FR Y-9C, FR Y-14 instructions; attestation by officers. Human: controller and CFO certify.
- **Problem and today's workflow:** Teams reconcile GL balances to report schedules, investigate edit-check failures and quarter-over-quarter variances, and write variance explanations before filing.
- **Evidence:** Federal Register notice of 2 Oct 2024 (opened, text extracted): "Total estimated annual burden hours: 115,283" appears in the FR Y-9 family section, just before the FR Y-14 paragraph. Corrected: this is not clearly a total across all Board collections as previously stated, and no FR Y-14 total was found. https://govinfo.gov/content/pkg/FR-2024-10-02/pdf/2024-22634.pdf [Corrected]
- **Agent design:** Tools: warehouse SQL, edit-check results, lineage lookup, prior-period comparison, commentary drafting. Rules perform core validation; agent triages failures, traces to source, drafts explanations. Gate: reporting manager and controller approve before filing.
- **Open source today:** chosak/fdic-call-reports (31 stars, MIT, not archived, last push 2022-12-01, README read: yes (start); call report downloader and analysis web app - adjacent only, not a reconciliation agent).
- **Demo path:** FFIEC bulk call report data; mask a set of values and have the agent flag and explain inconsistencies between schedules.
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 9. Card and deposit dispute / chargeback handling (Reg E and Reg Z)
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer: issuer bank disputes operations. Systems: card processor, network dispute platforms (Visa/Mastercard), core banking, fraud system, customer comms. Regulation: EFTA/Reg E and TILA/Reg Z error-resolution timelines (10 business days provisional credit, 45-90 day investigations - not re-checked). Human: disputes analyst approves final determination; compliance reviews adverse outcomes.
- **Problem and today's workflow:** Analysts classify disputes, pull transaction and merchant evidence, apply network reason-code rules, send letters and track statutory clocks.
- **Evidence:** The cited Consumer Compliance Outlook URL returned a 404 page, so the claim that Reg E error resolution was among the most-cited 2024 violations is unconfirmed. Reference, not confirmed: https://www.consumercomplianceoutlook.org/2026/first-issue/top-federal-reserve-system-resolution-in-2024 [Unconfirmed] No volume or cost figure found.
- **Agent design:** Tools: transaction history, merchant evidence lookup, network rules library, letter generator, deadline tracker. Gate: analyst approves deny/uphold; provisional-credit and clock rules enforced by workflow, not the model.
- **Open source today:** none found (gh search "chargeback dispute", stars>=20: 0 hits).
- **Demo path:** Synthetic disputes using CFPB complaint narratives (card/ACH categories) as customer text.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 10. Customer complaint triage and root-cause analysis (CFPB / UDAAP)
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer: bank complaint management/compliance. Systems: complaint management system, CFPB Company Portal, CRM, call transcripts, core banking. Regulation: UDAAP (Dodd-Frank 2010), CFPB response expectations (15 days to respond, 60 days to close for portal complaints - unverified), fair lending. Human: complaint specialist approves response; compliance reviews systemic issues.
- **Problem and today's workflow:** Staff read complaints, classify product/issue, locate the account facts, draft a response and tag root cause for trend reporting.
- **Evidence:** No reliable figure verified; the CFPB Consumer Complaint Database page was not opened. Reference, not confirmed: https://www.consumerfinance.gov/data-research/consumer-complaints/ [Unconfirmed]
- **Agent design:** Tools: CMS read/write, account lookup, policy KB, response template, theme clustering. Gate: specialist approves response; remediation (refunds) approved by authority holder.
- **Open source today:** none found (gh search "CFPB complaints", stars>=20: 0 hits).
- **Demo path:** CFPB Consumer Complaint Database narratives; evaluate classification and root-cause clustering against labelled issue fields.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

## Sources
- https://bpi.com/getting-to-effectiveness-report-on-u-s-financial-institution-resources-devoted-to-bsa-aml-sanctions-compliance/ (opened)
- https://fincen.gov/sites/default/files/shared/FinCEN_Infographic_Public_508FINAL_2024_June_7.pdf (opened, text extracted)
- https://www.fincen.gov/system/files/2026-05/CDD-Rule-Consolidated-FAQs.pdf (opened, text extracted)
- https://www.acamstoday.org/?p=22901 (HTTP 403, not confirmed)
- https://sf.freddiemac.com/articles/insights/2024-cost-to-originate-study (opened)
- https://www.moodys.com/web/en/us/insights/lending/case-study-new-approach-corporate-credit-speed-flexibility-consistency.html (opened; claim not found)
- https://pure.psu.edu/en/publications/bank-monitoring-evidence-from-syndicated-loans/ (opened)
- https://library.iccwbo.org//content//tfb//BRIEFINGS//20220627_TA_Briefing_No3_reducing_discrepancy_rates.pdf (opened, text extracted)
- https://govinfo.gov/content/pkg/FR-2024-10-02/pdf/2024-22634.pdf (opened, text extracted)
- https://www.consumercomplianceoutlook.org/2026/first-issue/top-federal-reserve-system-resolution-in-2024 (404, not confirmed)
- Dataset URLs listed in the datasets section (not opened).
