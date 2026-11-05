# HR & Workforce

## Overview
HR and payroll teams spend effort on compliance-driven reconciliation: hiring records, work-authorization paperwork, pay calculations, leave and injury logs, and responses to regulators. Manual work concentrates in cross-checking HRIS, ATS, payroll and timekeeping data, and in documenting decisions for audits. Hiring and employee-decision use cases carry fairness and legal exposure, so every agent here keeps a human decision-maker.

## Systems of record, regulations, public datasets
- **Systems:** HRIS (Workday, SAP SuccessFactors, UKG), ATS (Greenhouse, USAJOBS/Workday Recruiting), payroll and timekeeping (ADP, UKG), E-Verify/I-9 platforms, leave administrators, EHS/incident systems, case management for ER.
- **Regulation/standards:** Title VII and the EEOC four-fifths guidance; NYC Local Law 144 (2023); EU AI Act (employment is high-risk); FLSA and state wage laws; 8 CFR 274a (I-9); OSHA 29 CFR 1904 recordkeeping; FMLA and ADA; EU Pay Transparency Directive 2023/970; FCRA.
- **Public datasets:** EEOC EEO-1 aggregates https://www.eeoc.gov/data ; BLS SOII https://www.bls.gov/iif/ ; DOL WHD enforcement data https://enforcedata.dol.gov/ ; OSHA injury data https://www.osha.gov/Establishment-Specific-Injury-and-Illness-Data ; OPM FedScope https://www.opm.gov/data/ ; NYC AEDT audit postings (employer sites).

## Use cases

### 1. Hiring-decision bias monitoring across the applicant funnel
- **Tier:** B (statistics do the core; agent gathers data, writes findings, routes remediation) Enterprise: needs figure (research result, no volume or dollar figure)
- **Enterprise check:** Buyer: employer TA / legal. Systems: ATS, HRIS demographics, requisition data. Regulation: Title VII adverse impact, NYC LL144, EU AI Act. Human gate: recruiter/legal decide changes; no autonomous rejections.
- **Problem and today's workflow:** Analysts export stage-by-stage funnel data and compute adverse-impact ratios occasionally; screening tools themselves are rarely audited.
- **Evidence:** Wilson and Caliskan (UW, 2024): in tests of three open-source embedding models, white-associated names were preferred 85% of the time versus 9% for Black-associated names (UW news summary quoted in search excerpts; resumes ranked against 500+ real job listings). The cited GeekWire page returned 403 and the UW page was not opened. https://www.geekwire.com/2024/ai-overwhelmingly-prefers-white-and-male-job-candidates-in-new-test-of-resume-screening-bias/ [Search-excerpt] (search excerpt only)
- **Agent design:** Pulls funnel data per requisition, computes selection-rate ratios, drafts audit memo, opens remediation tickets. Legal approves findings.
- **Open source today:** jbarach2012/AIBF_API (195 stars, Apache-2.0, not archived, last push 2026-07-07; README read: yes, a plug-in layer that intercepts ATS scoring decisions and flags biased ones for human review; adjacent only, per-decision not funnel adverse-impact reporting); yakew7/Fair-Code (55 stars, MIT, not archived, last push 2026-11-05; README read: yes, notebooks auditing bias across several domains; adjacent only).
- **Demo path:** Synthetic applicant funnel with injected disparity; public UCI Adult dataset for ratio tests.
- **Verification:** 2026-11-06, Verified (search excerpt), repos checked yes

### 2. Automated employment decision tool (AEDT) compliance monitoring
- **Tier:** A Enterprise: needs figure
- **Enterprise check:** Buyer: employer compliance, or city enforcement agency. Systems: career sites, vendor audit reports, ATS config. Regulation: NYC LL144. Human gate: counsel signs notices and findings.
- **Problem and today's workflow:** Compliance staff manually find AEDT use, check for posted bias audits and candidate notices.
- **Evidence:** The NY State Comptroller audit (Dec 2025) of DCWP enforcement of Local Law 144 exists and called enforcement ineffective (search excerpts); the page returned 403. The "32 employers, one likely violation" figure is not confirmed: one secondary source gives it, another reports 17 instances of potential non-compliance in the same group, so the number is removed. Reference, not confirmed: https://www.osc.ny.gov/state-agencies/audits/2025/12/02/enforcement-local-law-144-automated-employment-decision-tools [Unconfirmed]
- **Agent design:** Crawl careers pages, inventory tools, compare to audit postings, draft notice gap report. Counsel approves.
- **Open source today:** aclu-national/tracking-ll144-bias-audits (20 stars, no licence declared, not archived, last push 2026-09-23; README read: yes, crowd-sourced tracker of LL144 bias-audit postings; adjacent only, a data tracker not a compliance agent).
- **Demo path:** Mock careers pages with and without audit links.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 3. Public-sector time-to-hire orchestration
- **Tier:** A Enterprise: needs figure (days, no dollar figure)
- **Enterprise check:** Buyer: agency HR. Systems: USAJOBS/ATS, calendars, background-check and clearance systems. Regulation: merit system principles, veterans' preference, Section 508. Human gate: HR specialist certifies candidates.
- **Problem and today's workflow:** Specialists classify positions, screen against qualifications, schedule panels and chase clearances by email.
- **Evidence:** GAO OIG-26-1 (opened): "GAO's hiring of MCO employees took about 103 days on average" in FY2024 (mission-critical occupations), against "OPM's goal of 80 days for executive branch agencies". The government-wide 101.2 days for FY2023 is not on that page; only a trade-press search excerpt gives it, so it is removed. https://www.gao.gov/products/oig-26-1 [Corrected]
- **Agent design:** Tracks each requisition stage, drafts qualification crosswalks, schedules panels, escalates stalls. Specialist certifies.
- **Open source today:** none found (gh search "federal hiring time to hire", stars>=20, not archived: no relevant hit).
- **Demo path:** OPM FedScope plus synthetic requisition timeline.
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 4. Form I-9 audit and remediation
- **Tier:** A Enterprise: needs figure (per-form penalty only)
- **Enterprise check:** Buyer: HR/legal. Systems: I-9 platform/paper scans, HRIS, E-Verify. Regulation: 8 CFR 274a; anti-discrimination (IER) limits on over-documentation. Human gate: HR/counsel approve corrections.
- **Problem and today's workflow:** Reviewers check form completeness, document types and reverification dates across thousands of employees.
- **Evidence:** The cited Quarles page (opened, dated 30 Oct 2019) does not contain the $288-$2,861 range. Search excerpts of several law-firm summaries give $288 to $2,861 per form for paperwork violations under the DHS inflation adjustment published 2 Jan 2025 (Federal Register 2024-31204); the 8 CFR 274a.10 citation was not named in them, and a newer adjustment may exist in 2026. https://www.quarles.com/newsroom/publications/employers-beware-how-little-i-9-mistakes-can-add-up-to-big-fines [Corrected] (2025 amounts via search excerpts, not opened)
- **Agent design:** Extract fields, compute 3-day/expiry dates, cross-check HRIS, queue corrections. Remediation never backdates; HR approves.
- **Open source today:** none found (gh search "I-9 audit", stars>=20, not archived: no relevant hit).
- **Demo path:** Synthetic I-9 PDFs with seeded errors.
- **Verification:** 2026-11-06, Corrected (search excerpts), repos checked yes

### 5. Payroll and wage-and-hour error auditing
- **Tier:** A Enterprise: pass
- **Enterprise check:** Buyer: payroll/HR. Systems: timekeeping, payroll, scheduling. Regulation: FLSA, state wage laws. Human gate: payroll manager approves corrections.
- **Problem and today's workflow:** Auditors sample pay periods for overtime, rounding, meal-break and deduction errors.
- **Evidence:** The DOL WHD data page (opened) shows FY2025 results ("more than $259 million in back wages for 176,957 employees") and not FY2024. Search excerpts of DOL's FLSA release give FY2024 FLSA back wages of $149.9M for 125,301 employees, while DOL's broader page figure for FY2024 is about $273M for nearly 152,000 workers (different scope). https://www.dol.gov/agencies/whd/data [Corrected] (FY2024 figures via search excerpts)
- **Agent design:** Reconciles punches, schedules, rules and pay stubs; flags errors with computed back-pay. Manager approves.
- **Open source today:** none found (gh search "wage hour payroll audit", stars>=20, not archived: no relevant hit).
- **Demo path:** Synthetic punches with injected rounding and OT misclassification.
- **Verification:** 2026-11-06, Corrected (search excerpts), repos checked yes

### 6. Pay-equity analysis and EU Pay Transparency reporting
- **Tier:** A Enterprise: needs figure (regulatory deadline, no volume or dollar figure)
- **Enterprise check:** Buyer: reward/legal. Systems: HRIS, payroll, job architecture. Regulation: Directive (EU) 2023/970 (transposition due 7 June 2026; 250+ employers report annually from 2027; 150-249 first report 7 June 2027). Human gate: compensation committee and works councils.
- **Problem and today's workflow:** Analysts build job-level pay comparisons in spreadsheets across countries.
- **Evidence:** Legal500 copy of the Mondaq article (opened): "EU member states have until June 7, 2026, to implement the EU pay transparency directive"; first reporting begins in 2027 for employers with 150 or more employees on 2026 pay data. The page does not give separate dates for 250+ and 150-249 employers, so those split dates are unconfirmed and removed (check Directive 2023/970 text). https://www.mondaq.com/uk/employee-benefits-compensation/1689558/the-june-2026-eu-pay-transparency-directive-implementation-deadline-looms [Corrected]
- **Agent design:** Maps jobs to "equal value" groups, computes gaps, drafts explanations. Committee approves remediation budgets.
- **Open source today:** none found (gh search "pay equity analysis", stars>=20, not archived: no relevant hit).
- **Demo path:** Synthetic payroll with seeded gap; public UK gender-pay-gap service data https://gender-pay-gap.service.gov.uk/
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 7. Discrimination charge response and workplace investigation case management
- **Tier:** A Enterprise: pass
- **Enterprise check:** Buyer: employee-relations/legal. Systems: HRIS, email/chat archives, case management, EEOC portal. Regulation: Title VII/ADA/ADEA, litigation holds. Human gate: counsel approves position statements.
- **Problem and today's workflow:** Staff collect personnel files and communications and draft position statements under tight deadlines.
- **Evidence:** CWC page (opened): "The EEOC received 81,055 discrimination charges in FY 2023, a 10% increase from the year before". The page gives $440.5 million in monetary benefits for charging parties, not $665M; search excerpts of the EEOC annual performance report say $665 million total, comprising $440.5M (private and state/local) plus $202M (federal employees), not opened. https://cwc.org/CWC/Updates/2024/EEOCs-Final-FY-2023-Enforcement-Statistics-Show-10-Increase-in-Charges-Filed.aspx [Corrected]
- **Agent design:** Builds evidence index, timelines, draft statement with record citations; privilege screening. Counsel signs.
- **Open source today:** none found (gh search "EEOC charge response", stars>=20, not archived: no relevant hit).
- **Demo path:** Synthetic personnel files and complaint narratives.
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 8. OSHA injury recordkeeping and electronic submission
- **Tier:** B Enterprise: pass
- **Enterprise check:** Buyer: EHS/HR. Systems: incident reports, workers' comp claims, HRIS. Regulation: 29 CFR 1904 (Forms 300/300A/301). Human gate: EHS manager certifies logs.
- **Problem and today's workflow:** Staff decide recordability (medical treatment, restricted work) and maintain logs.
- **Evidence:** BLS release (opened): "Private industry employers reported 2.6 million nonfatal workplace injuries and illnesses in 2023"; Tables 1 and 2 list 2,569.0 thousand total recordable cases. https://www.bls.gov/news.release/archives/osh_11082024.htm [Verified]
- **Agent design:** Classifies cases against 1904 rules with citations, populates forms, flags late entries. Manager certifies.
- **Open source today:** none found (gh search "OSHA recordkeeping", stars>=20, not archived: no relevant hit).
- **Demo path:** OSHA public injury data; synthetic incident narratives.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 9. Worker-classification (contractor vs employee) review
- **Tier:** A Enterprise: needs figure (a contested rate, no dollar figure)
- **Enterprise check:** Buyer: HR/legal/procurement. Systems: AP/vendor master, contracts, engagement records. Regulation: FLSA economic-reality test (DOL rule status in flux), IRS common-law, state ABC tests. Human gate: counsel decides.
- **Problem and today's workflow:** Reviewers examine contractors one by one against multi-factor tests.
- **Evidence:** Mercatus comment (opened) quotes the DOL proposed rule, which cites a National Employment Law Project literature review: "the share of employers misclassifying workers ranges from 10 to 30 percent". It is second-hand and measures employers, not workers. https://www.mercatus.org/research/public-interest-comments/getting-worker-classification-right-evidence-tradeoffs-and-future [Verified]
- **Agent design:** Scores engagement facts per factor with contract citations; triage list. Counsel decides.
- **Open source today:** none found (gh search "worker misclassification", stars>=20, not archived: no relevant hit).
- **Demo path:** Synthetic contractor contracts and invoices.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 10. Leave (FMLA) and ADA accommodation case administration
- **Tier:** A Enterprise: needs figure
- **Enterprise check:** Buyer: leave/benefits team. Systems: HRIS, leave vendor, medical certification docs. Regulation: FMLA, ADA, state paid-leave. Human gate: leave specialist approves.
- **Problem and today's workflow:** Specialists track eligibility, certifications, intermittent-leave usage and notice deadlines.
- **Evidence:** no reliable figure found; nothing to verify. [Unconfirmed]
- **Agent design:** Eligibility calc, deadline notices, certification gap letters, usage reconciliation; no medical inference.
- **Open source today:** none found (gh search "FMLA leave", stars>=20, not archived: no relevant hit).
- **Demo path:** Synthetic leave cases with intermittent usage logs.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

## Sources
- https://www.geekwire.com/2024/ai-overwhelmingly-prefers-white-and-male-job-candidates-in-new-test-of-resume-screening-bias/
- https://www.osc.ny.gov/state-agencies/audits/2025/12/02/enforcement-local-law-144-automated-employment-decision-tools
- https://www.gao.gov/products/oig-26-1
- https://www.quarles.com/newsroom/publications/employers-beware-how-little-i-9-mistakes-can-add-up-to-big-fines
- https://www.dol.gov/agencies/whd/data
- https://www.mondaq.com/uk/employee-benefits-compensation/1689558/the-june-2026-eu-pay-transparency-directive-implementation-deadline-looms
- https://cwc.org/CWC/Updates/2024/EEOCs-Final-FY-2023-Enforcement-Statistics-Show-10-Increase-in-Charges-Filed.aspx
- https://www.bls.gov/news.release/archives/osh_11082024.htm
- https://www.mercatus.org/research/public-interest-comments/getting-worker-classification-right-evidence-tradeoffs-and-future
- Dataset URLs listed above
