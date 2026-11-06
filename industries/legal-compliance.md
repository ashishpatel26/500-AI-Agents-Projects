# Legal & Compliance

## Overview
Corporate legal, privacy and compliance teams spend most effort on document-heavy review (contracts, e-discovery, vendor paper), deadline-driven obligations (DSARs, holds, regulator responses, IP renewals) and tracking regulatory change. Manual work concentrates where facts sit in many systems (email, DMS, CLM, HR, ERP) and a lawyer must still sign. All ten cases below keep a lawyer or DPO as the approver; none gives the agent legal judgement.

Verification note: GitHub search was rate-limited (HTTP 403) during the run, so "Open source today" entries for new cases say "not searched". Seeded entries are carried from earlier research and were not re-read by me.

## Systems of record, regulations, public datasets
- **Systems:** CLM (Ironclad, Icertis, DocuSign CLM), document management (iManage, SharePoint, NetDocuments), e-discovery platforms (Relativity, Everlaw), legal hold tools, matter/e-billing (CounselLink, Mitratech), IP docketing (Anaqua, CPA), GRC/TPRM platforms, HRIS, ERP/AP, M365/Google Workspace, ticketing.
- **Regulations and rules:** GDPR (2016/679) Arts. 12, 15, 28; DORA (2022/2554); US Federal Rules of Civil Procedure 26 and 37(e) (2015 amendment); Federal Rule of Evidence 502; USPTO trademark and patent maintenance rules; ABA Model Rule 1.6 and 5.3 (confidentiality, supervision of nonlawyer assistance).
- **Public datasets for demos:**
  - CUAD, 510 commercial contracts with 41 clause types: https://www.atticusprojectai.org/cuad
  - SEC EDGAR material contracts (Exhibit 10): https://www.sec.gov/edgar
  - Enron email corpus (EDRM version): https://edrm.net/resources/data-sets/edrm-enron-email-data-set/
  - EUR-Lex / Federal Register APIs for regulatory change: https://eur-lex.europa.eu , https://www.federalregister.gov/developers
  - USPTO bulk data: https://data.uspto.gov

## Use cases

### 1. GDPR data subject access request (DSAR) fulfilment
- **Tier:** A | Enterprise: pass
- **Enterprise check:** Buyer: privacy office/DPO at any EU-exposed enterprise. Systems: CRM, HRIS, ticketing, email, data warehouse, DMS. Regulation: GDPR Arts. 12 and 15, one-month deadline. Human: DPO approves exemptions and final release.
- **Problem and today's workflow:** Privacy analysts email system owners, search each store by name and identifiers, redact third-party data and compile the response by hand within a month.
- **Evidence:** IAPP: EDPB 2024 coordinated enforcement on right of access involved "30 EU data protection authorities" exploring "1,185 data controllers". https://iapp.org/news/a/edpb-s-2024-coordinated-enforcement-offers-window-into-right-of-access [Verified]
- **Agent design:** Verify identity, fan out search connectors, entity-match records, propose redactions and exemptions with citations, assemble the package. DPO reviews redactions and approves release.
- **Open source today:** none found (gh search 'dsar gdpr' returned no hits).
- **Demo path:** Synthetic customer across a mock CRM, ticket and email set (Enron corpus as email noise); score recall of planted records and leaked third-party data.
- **Verification:** 2026-11-06, Verified, search done yes

### 2. Post-signature contract obligation tracking and value leakage
- **Tier:** A | Enterprise: pass
- **Enterprise check:** Buyer: legal ops/commercial finance. Systems: CLM, ERP/billing, procurement. Regulation: contractual and revenue-recognition audit trail. Human: counsel approves any notice or claim.
- **Problem and today's workflow:** Obligations (rebates, SLA credits, renewal notice windows, price indexation) sit in PDFs; staff rarely reconcile them with invoices.
- **Evidence:** WorldCC: "average value erosion now estimated at 8.6%" (9.2% in 2014); top performers "slightly over 3%"; worst performers "exceeding 20%", not 15%. https://news.worldcc.com/news-from-worldcc/are-organizations-unlocking-their-full-financial-potential [Corrected]
- **Agent design:** Extract obligations into a register, join with ERP billing and SLA data, flag shortfalls, draft claim or notice letters. Counsel approves before sending.
- **Open source today:** none found (gh search 'contract obligations' returned only unrelated terms-of-service repos).
- **Demo path:** CUAD contracts plus synthetic invoice and SLA-report CSVs with planted rebate misses.
- **Verification:** 2026-11-06, Corrected, search done yes

### 3. Privilege review in e-discovery
- **Tier:** B (classification is model work; agent runs QC loops and privilege log) | Enterprise: needs figure
- **Enterprise check:** Buyer: litigation counsel/corporate legal. Systems: e-discovery platform, DMS, email archive. Regulation: FRCP 26, FRE 502 (waiver). Human: attorney decides every privilege call.
- **Problem and today's workflow:** Contract reviewers read millions of documents for responsiveness and privilege; senior lawyers QC samples and write the log.
- **Evidence:** RAND press release (April 2012) could not be opened (connection reset), so the claim that review is the largest e-discovery cost component and the 57-case/eight-corporation study are unconfirmed. No percentage claimed. Reference, not confirmed: https://www.rand.org/news/press/2012/04/11.html [Unconfirmed]
- **Agent design:** Pre-classify, sample for precision/recall, draft log entries with basis, route low-confidence items to reviewers. Attorney signs off validation protocol and log.
- **Open source today:** shmsoft/FreeEed (154 stars, Apache-2.0, not archived, last push 2026-10-30; README read: yes; adjacent only: self-hosted eDiscovery processing, search and AI Q&A, no privilege-log workflow shown); FreeDiscovery/FreeDiscovery (79 stars, licence NOASSERTION, not archived, last push 2022-06-21; README read: partly, badges only; adjacent only, stale).
- **Demo path:** EDRM Enron set with synthetic privilege labels (lawyer names list).
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 4. Regulatory change management and obligation mapping
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: compliance function at a regulated firm. Systems: regulator feeds, policy library, GRC control register, Jira/ServiceNow. Regulation: whichever regime applies; audit trail of versioned citations. Human: compliance owner approves applicability and control changes.
- **Problem and today's workflow:** Analysts read regulator publications, decide applicability, map to policies and raise remediation tickets in spreadsheets.
- **Evidence:** Thomson Reuters 234 alerts/day, 1,374 regulators, 190 countries not found on the cited Waters Technology page (a 2016 article saying feeds cover "more than 750 global regulators"). Figures removed. Reference, not confirmed: https://www.waterstechnology.com/inside-reference-data/news/2479485/thomson-reuters-consolidates-regulatory-feeds [Unconfirmed]
- **Agent design:** Monitor feeds, diff versions, score applicability against the business profile, map to controls, open tickets. Owner approves each mapping.
- **Open source today:** aws-samples/sample-compliance-assistant-with-agents (37 stars, MIT-0, not archived, last push 2025-04-15; README read: yes; partly addresses: Bedrock + CrewAI multi-agent compliance automation sample).
- **Demo path:** Federal Register API plus a synthetic policy/control register.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 5. Third-party / vendor privacy and security due diligence (GDPR Art. 28, DORA)
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: procurement, privacy, security. Systems: TPRM/GRC platform, contract repository, vendor portal, DORA register of information. Regulation: GDPR Art. 28; DORA third-party provisions. Human: risk owner approves; no automated approval of high-risk vendors.
- **Problem and today's workflow:** Staff read questionnaires, SOC 2 reports and DPAs, compare against requirements, chase follow-ups.
- **Evidence:** Verizon DBIR third-party involvement doubling 15% to 30%: the executive-summary PDF returned 503 and the second source opened did not state it. Number removed. Reference, not confirmed: https://www.verizongov.com/resources/reports/2025-dbir-executive-summary.pdf [Unconfirmed]
- **Agent design:** Ingest documents, map to control checklist, identify gaps, send follow-up questions, update register, recommend risk tier. Risk owner decides.
- **Open source today:** LeeMangold/OpenGRC (160 stars, licence NOASSERTION, not archived, last push 2026-10-08; README read: yes; adjacent only: self-hosted GRC platform); grcengineering/gigachad-grc (167 stars, NOASSERTION, not archived, last push 2026-10-26; README read: yes; adjacent only: GRC platform).
- **Demo path:** Public SOC 2/ISO summaries and CSA CAIQ answers (https://cloudsecurityalliance.org/artifacts/consensus-assessments-initiative-questionnaire-v4) with a synthetic requirement list.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 6. Contract review against a negotiation playbook
- **Tier:** A | Enterprise: pass
- **Enterprise check:** Buyer: in-house legal/sales ops. Systems: CLM, DMS, CRM (Salesforce), e-signature. Regulation: audit trail of approved deviations, delegation-of-authority policy. Human: attorney approves redlines and any fallback beyond delegated authority.
- **Problem and today's workflow:** Lawyers read inbound third-party paper, compare each clause to the playbook, redline and escalate, often with a backlog before quarter end.
- **Evidence:** No review-time savings figure found. Related value-at-stake: WorldCC "average value erosion now estimated at 8.6%" of contract value (earlier 9.2%), corrected from 9%. https://news.worldcc.com/news-from-worldcc/are-organizations-unlocking-their-full-financial-potential [Corrected]
- **Agent design:** Parse, segment clauses, classify against playbook positions, propose fallback redlines, check the CRM deal data (value, region) for approval tier, route escalations, log deviations. Attorney approves.
- **Open source today:** Vaquill-AI/ms-word-addin (78 stars, Apache-2.0, not archived, last push 2026-10-01; README read: yes; addresses partly: Word add-in for contract review, grounded redlining and drafting).
- **Demo path:** CUAD contracts with a hand-written 15-clause playbook; measure clause recall and redline acceptance.
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 7. Litigation hold issuance and preservation tracking
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: general counsel. Systems: legal hold tool, HRIS (custodians), M365/Google Vault, Slack/Teams, backup/retention systems, matter management. Regulation: FRCP 37(e); duty arising once litigation is reasonably anticipated (Zubulake line of cases). Human: counsel approves custodian list, scope and release.
- **Problem and today's workflow:** Paralegals identify custodians from org charts and interviews, send notices, chase acknowledgements, ask IT to suspend auto-deletion and re-issue as scope changes.
- **Evidence:** Rule 37(e) intent-to-deprive background not confirmed: ABA page returned 403. No sanction-frequency figure. Reference, not confirmed: https://www.americanbar.org/groups/litigation/resources/newsletters/pretrial-practice-discovery/spoliation-sanctions-how-avoid-them/ [Unconfirmed]
- **Agent design:** From the matter facts propose custodians and data sources, draft notices, apply preservation holds through admin APIs, track acknowledgements and reminders, flag departing employees. Counsel approves each step that touches systems.
- **Open source today:** none found (gh search 'litigation hold' returned only unrelated terms-of-service repos).
- **Demo path:** Synthetic org chart and mock M365 tenant (Graph API sandbox) with a matter description.
- **Verification:** 2026-11-06, Unconfirmed, search done yes

### 8. Trademark and patent prosecution docketing and deadline management
- **Tier:** B (deadline rules are deterministic; agent handles office actions and intake) | Enterprise: needs figure
- **Enterprise check:** Buyer: IP department or firm. Systems: IP management system (Anaqua, CPA), USPTO Patent Center / TSDR, WIPO, correspondence email. Regulation: statutory response and maintenance deadlines; missed deadlines can abandon rights. Human: attorney approves every filing and instruction.
- **Problem and today's workflow:** Docketers read office actions and notices, calculate deadlines, enter them, and prepare instruction emails to outside counsel across jurisdictions.
- **Evidence:** USPTO FY2024 application and grant counts not confirmed: the Commerce OIG report was too large to fetch and a GAO-relayed 527,000/365,000 figure was seen only in search excerpts. Numbers removed. Reference, not confirmed: https://www.oig.doc.gov/wp-content/OIGPublications/USPTO-FY-2024-Agency-Financial-Report.pdf [Unconfirmed]
- **Agent design:** Pull TSDR/Patent Center status, parse office actions, compute deadlines and fee amounts, update the docket, draft client/associate reports. Attorney reviews before anything is filed.
- **Open source today:** jjdejong/phpip (55 stars, GPL-3.0, not archived, last push 2026-09-25; README read: yes; adjacent only: IP portfolio and docketing manager, not an agent).
- **Demo path:** USPTO bulk data (TSDR/Patent File Wrapper) for real office actions; synthetic docket database.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 9. Regulatory examination and subpoena response assembly
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: compliance/legal at a regulated firm (bank, broker-dealer, insurer). Systems: document request tracker, DMS, email archive, core systems for reports, GRC. Regulation: examiner requests carry deadlines; production must be complete and consistent. Human: counsel reviews privilege and approves every submission.
- **Problem and today's workflow:** A request list with dozens of items is split across business owners; staff collect documents, reconcile answers across items and format responses.
- **Evidence:** No reliable figure found. [Unconfirmed]
- **Agent design:** Parse the request letter into items, assign owners, search repositories for candidate documents, cross-check answers for inconsistency, draft the cover narrative. Counsel signs off privilege and consistency before submission.
- **Open source today:** none found (gh search 'subpoena' returned only unrelated repos).
- **Demo path:** Public SEC exam document-request-list examples with a synthetic firm document set.
- **Verification:** 2026-11-06, Unconfirmed, search done yes

### 10. Outside counsel invoice review against billing guidelines
- **Tier:** B (rules engines already flag; agent adds reasoning and dispute drafting) | Enterprise: pass
- **Enterprise check:** Buyer: legal operations. Systems: e-billing (LEDES), matter management, ERP AP. Regulation: audit trail for spend approval. Human: matter manager approves reductions and disputes.
- **Problem and today's workflow:** Reviewers read time entries for block billing, duplicate work, unapproved staffing and rate breaches, then negotiate cuts.
- **Evidence:** Mitratech (vendor): AI invoice review "driving 5-10% annual reductions in outside counsel spend"; e-billing "consistently realize a 5-10% reduction". Original 3-10% range not on page. Vendor source, not independent. https://mitratech.com/en-gb/resource-hub/blog/5-ways-reduce-legal-spend-outside-counsel/ [Corrected]
- **Agent design:** Parse LEDES invoices, check entries against guidelines and matter budget, explain each flag, draft adjustment letters, learn from accepted reductions. Matter manager approves.
- **Open source today:** none found (gh search 'legal billing' returned only unrelated repos).
- **Demo path:** Synthetic LEDES 1998B files with planted guideline breaches.
- **Verification:** 2026-11-06, Corrected, search done yes

## Sources
- https://www.atticusprojectai.org/cuad
- https://www.sec.gov/edgar
- https://edrm.net/resources/data-sets/edrm-enron-email-data-set/
- https://www.federalregister.gov/developers
- https://data.uspto.gov
- https://cloudsecurityalliance.org/artifacts/consensus-assessments-initiative-questionnaire-v4
- https://iapp.org/news/a/edpb-s-2024-coordinated-enforcement-offers-window-into-right-of-access
- https://news.worldcc.com/news-from-worldcc/are-organizations-unlocking-their-full-financial-potential
- https://www.rand.org/news/press/2012/04/11.html
- https://www.waterstechnology.com/inside-reference-data/news/2479485/thomson-reuters-consolidates-regulatory-feeds
- https://www.verizongov.com/resources/reports/2025-dbir-executive-summary.pdf
- https://www.americanbar.org/groups/litigation/resources/newsletters/pretrial-practice-discovery/spoliation-sanctions-how-avoid-them/
- https://www.oig.doc.gov/wp-content/OIGPublications/USPTO-FY-2024-Agency-Financial-Report.pdf
- https://mitratech.com/en-gb/resource-hub/blog/5-ways-reduce-legal-spend-outside-counsel/
