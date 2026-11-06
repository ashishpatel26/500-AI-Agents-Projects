# Government & Public Safety

## Overview
Government agencies spend effort on adjudicating claims and benefits, producing records and rulemaking files, and proving compliance. Manual work concentrates in reading evidence, applying statute or policy to each case, redacting records, and documenting decisions for appeal or audit. Every outcome is reviewable (appeals, litigation, IG audits), so agents must assist officials who keep decision authority. Safety-critical real-time functions (for example 911 dispatch) are deliberately excluded.

## Systems of record, regulations, public datasets
- **Systems:** case management (Salesforce Gov, Pega, ServiceNow), state eligibility systems, VBMS (VA claims), eMASS/GRC tools (ATO packages), e-discovery/FOIA platforms (FOIAXpress, Relativity), Regulations.gov / FDMS, digital evidence management (Axon Evidence), USASpending/SAM.gov, wage-record databases.
- **Regulations/standards:** FOIA (1966, amended 2016; 20-working-day processing requirement confirmed in the GAO-24-106535 highlights); Privacy Act (1974); Administrative Procedure Act (1946); NEPA (1969); NIST SP 800-37 RMF (Rev. 2, 2018) and FedRAMP; IRS Pub. 1075 (FTI); PIIA improper-payment law (2019); 42 CFR 435.916 Medicaid renewals; CJIS Security Policy. Only the FOIA 20-day rule was confirmed against a source; the other citations were not individually checked against official text.
- **Public datasets for demos:** FOIA.gov annual report data https://www.foia.gov/data.html ; Regulations.gov API and bulk comments https://www.regulations.gov/ ; USASpending https://www.usaspending.gov/ ; Paymentaccuracy.gov https://www.paymentaccuracy.gov/ ; CEQ EIS database https://eplanning.blm.gov/ and EPA EIS database https://cdxapps.epa.gov/cdx-enepa-II/public/action/eis/search ; USDA SNAP QC data https://www.fns.usda.gov/snap/qc/data .

## Use cases

### 1. FOIA / public-records request processing and redaction
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is a federal or state agency; systems are email/records stores and FOIA case system; FOIA exemptions, Privacy Act, 20-working-day clock, litigable; FOIA officer signs release.
- **Problem and today's workflow:** FOIA staff search multiple repositories, review each page for exemptions (b)(5)/(b)(6), redact by hand and track deadlines.
- **Evidence:** E&E News on GAO-24-106535 (March 2024): "22 percent of requests were backlogged in fiscal 2022, compared to 14 percent in fiscal 2013". https://www.eenews.net/articles/watchdog-foia-backlog-undermines-open-government-goals/ . The GAO highlights page opened confirms the backlog "has risen over the last decade" but shows the percentages only in an image chart, so the percentages are confirmed through the secondary source. [Verified]
- **Agent design:** Tools: records search, document de-duplication, exemption classifier with rationale, redaction engine, case-system API. Human gate: FOIA officer approves every withholding and release.
- **Open source today:** none found (gh search repos "FOIA redaction", stars >= 20, not archived: no results).
- **Demo path:** Public released FOIA reading-room documents with synthetic PII injected.
- **Verification:** 2026-11-06, Verified, repos checked yes (search only)

### 2. SNAP eligibility casework and payment-error prevention
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is a state human-services agency; systems are state eligibility system, wage databases, paystub uploads; federal QC sanctions, due-process notices; caseworker approves each determination.
- **Problem and today's workflow:** Caseworkers verify income and household composition from paystubs and data matches under state-specific rules.
- **Evidence:** USDA FNS: "The national payment error rate for fiscal year (FY) 2024 is 10.93%." https://fns-prod.azureedge.us/node/22999 (the fns.usda.gov page originally cited returned HTTP 403 to fetch; this is the same release on an FNS-hosted address). [Verified]
- **Agent design:** Tools: document extraction, wage-match query, state-rule engine, case notes. Human gate: caseworker certifies the budget before notice.
- **Open source today:** DSACMS/iv-cbv-payroll (28 stars, CC0-1.0, not archived, last push 2026-11-05; README read: yes) is CMS's "Emmy" income verification via payroll providers for benefit applicants; the README frames it for Medicaid eligibility, so it addresses income verification but is adjacent for SNAP. navapbc/oscer (26 stars, Apache-2.0, not archived, last push 2026-11-03; README read: yes) is Medicaid community-engagement reporting; adjacent only.
- **Demo path:** USDA SNAP QC public-use data and synthetic paystubs.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 3. Unemployment-insurance fraud and improper-payment triage
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is a state workforce agency; systems are UI claims system, wage records, bank/IP data, NASWA IDH; due process on benefit stoppage; adjudicator signs.
- **Problem and today's workflow:** Investigators work cross-match hits for identity theft, multistate claims and deceased claimants, then adjudicate and recover.
- **Evidence:** GAO-23-106696 estimated pandemic-era unemployment insurance fraud was "between $100 billion and $135 billion", roughly 11 to 15 percent of benefits paid (April 2020 to May 2023). https://gao.gov/products/gao-23-106696 [Verified]
- **Agent design:** Tools: link analysis, ID-verification vendor APIs, wage lookup, case writeup. Human gate: adjudicator decides stoppage; claimant notice and appeal preserved.
- **Open source today:** none found (gh search repos "unemployment insurance fraud", stars >= 20, not archived: no results).
- **Demo path:** Synthetic claim graphs (shared bank accounts/IPs) with seeded rings.
- **Verification:** 2026-11-06, Verified, repos checked yes (search only)

### 4. NEPA environmental-review document preparation
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is a federal agency or contractor; systems are EIS repository, GIS, comment databases; APA litigation over the record; agency NEPA lead signs.
- **Problem and today's workflow:** Staff compile scoping, comment responses and cross-reference studies.
- **Evidence:** CEQ report (PDF text read): "based on 1,276 EISs for which a notice of availability of a final EIS was published between January 1, 2010, and December 31, 2018"; average EIS completion time from NOI to ROD "was 4.5 years, unchanged from the 2018 report". https://nepa.gov/sites/default/files/documents/CEQ_EIS_Timeline_Report_2020-6-12.pdf (2010-2018 data, dated). [Verified]
- **Agent design:** Tools: prior-EIS retrieval, GIS/environmental data pulls, comment clustering, citation checker. Human gate: NEPA lead owns the record.
- **Open source today:** pnnl/nepa-mcp (22 stars, BSD-3-Clause, not archived, last push 2026-11-04; README read: yes). README: MCP servers for federal environmental data, regulatory research and geospatial screening to support AI-assisted NEPA workflows; it covers the data-retrieval tools, not full document preparation (partial fit).
- **Demo path:** EPA EIS database documents and public comment sets.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 5. VA disability claims evidence review
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is VBA or a state veterans agency; systems are VBMS, service treatment records, exam reports; 38 CFR rating schedule, appeal rights; rating specialist decides.
- **Problem and today's workflow:** Rating staff read hundreds of pages of medical evidence, identify claimed conditions and match to diagnostic codes.
- **Evidence:** Nextgov (Aug 2025): VA "processed a record 2,524,115 disability compensation and pension claims in fiscal 2025" (with six weeks left in the fiscal year); officials say the backlog fell by more than 37% since January 20, 2025; the backlog peaked above 600,000 in March 2013. https://www.nextgov.com/digital-government/2025/08/veterans-affairs-reduces-claims-backlog-record-rate/407429/ . Corrected: the earlier figures (3,001,734 claims, backlog 112,353 from 264,717) are not on that page and are removed. VA-sourced, no independent audit. [Corrected]
- **Agent design:** Tools: record OCR, condition extractor, rating-schedule retriever, summary generator. Human gate: rating specialist makes all decisions.
- **Open source today:** none found (gh search repos "VA disability claims", stars >= 20, not archived: no results).
- **Demo path:** Synthetic medical records; public 38 CFR Part 4.
- **Verification:** 2026-11-06, Corrected, repos checked yes (search only)

### 6. Body-worn-camera footage review and redaction for public-records release
- **Tier:** B. Enterprise: pass
- **Enterprise check:** Buyer is a police department or records unit; systems are digital evidence management (Axon, Motorola) and records requests portal; state public-records laws, CJIS; records custodian approves.
- **Problem and today's workflow:** Staff scrub video and audio to blur faces, plates, minors and victims.
- **Evidence:** Dodge County (Wisconsin) Sheriff Dale Schmidt, as reported by Fox6: "For every hour of video, on average, it takes an hour-and-a-half to go through and redact it." https://www.fox6now.com/news/wisconsin-body-camera-video-cost . Corrected: this is a sheriff's estimate in news coverage; the Wisconsin legislative testimony PDF originally cited returned HTTP 403 and was not read. A search extract attributes a similar ratio to the state FOP president, so treat it as an agency estimate, not a measured rate. [Corrected]
- **Agent design:** Tools: face/plate/audio-PII detectors, evidence-system API, redaction log. Human gate: custodian reviews every output before release.
- **Open source today:** none found (gh search repos "body camera redaction", stars >= 20, not archived: no results).
- **Demo path:** Public-domain body-cam style video; Mapillary/OpenImages faces for detector testing.
- **Verification:** 2026-11-06, Corrected, repos checked yes (search only)

### 7. Rulemaking public-comment analysis
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer is a regulatory agency; systems are Regulations.gov/FDMS; APA requires responding to significant comments; rule-writer attests to the record.
- **Problem and today's workflow:** Staff read, de-duplicate and categorize comments (including mass campaigns) and draft responses.
- **Evidence:** The ACUS draft report returned HTTP 403 and the ACUS project page also returned 403; search extracts did not show the "hundreds of thousands to millions" or "over 90% mass-campaign" statements, so both figures are removed. Plain-language problem stands: mass, computer-generated and falsely attributed comments are the subject of ACUS Recommendation 2021-1. Reference, not confirmed: https://www.ACUS.GOV/sites/default/files/documents/Draft%20Report_Mass%2C%20Computer-Generated%2C%20and%20Fraudulent%20Comments_04022021.pdf [Unconfirmed]
- **Agent design:** Tools: Regulations.gov API, near-duplicate clustering, issue taxonomy, response drafter with comment citations. Human gate: rule team approves each response.
- **Open source today:** none found (gh search repos "public comment analysis rulemaking", stars >= 20, not archived: no results).
- **Demo path:** Regulations.gov bulk comments for a past rulemaking.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes (search only)

### 8. Authorization-to-operate (RMF/FedRAMP) package preparation
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer is an agency CISO or vendor; systems are eMASS/GRC, scanners, CMDB; NIST 800-37/800-53, FedRAMP; authorizing official signs.
- **Problem and today's workflow:** ISSOs write control narratives, collect evidence and track POA&Ms by hand.
- **Evidence:** GSA statement to House Oversight (July 2019, PDF text read): "Agency authorization timelines have also decreased in FY2018, averaging approximately 8 months compared to roughly 15 months in FY 2015." https://docs.house.gov/meetings/GO/GO24/20190717/109809/HHRG-116-GO24-Wstate-CheriyanA-20190717.pdf (dated 2019; current timelines not checked). The cost ranges previously attributed to GAO-24-106591 were not verified and are dropped. Authorization time is a duration, not a dollar figure. [Verified]
- **Agent design:** Tools: scanner/CMDB queries, OSCAL generator, control-narrative drafter, POA&M tracker. Human gate: ISSO reviews; AO decides.
- **Open source today:** none found (gh search repos "FedRAMP OSCAL ATO", stars >= 20, not archived: no results).
- **Demo path:** NIST OSCAL sample SSPs https://github.com/usnistgov/oscal-content .
- **Verification:** 2026-11-06, Verified, repos checked yes (search only)

### 9. Personnel-vetting investigation preparation
- **Tier:** B. Enterprise: pass
- **Enterprise check:** Buyer is DCSA / federal security office; systems are DISS/NBIS, investigative databases; Executive Orders and SEAD 4 adjudicative guidelines; adjudicator decides.
- **Problem and today's workflow:** Staff compile and reconcile SF-86 data, records checks and interviews.
- **Evidence:** ClearedJobs blog: "DCSA's case inventory ended FY2026 Q2 at 100,696, down from roughly 259,000 in FY2024 Q4", with the caveat that "the historical inventory series was restated downward between the two most recent quarterly reports with no published explanation". https://blog.clearedjobs.net/what-dcsa-does/ (secondary blog; DoD quarterly report not opened). The earlier "GAO 86%-inaccurate timeliness" item was never traced and is dropped. [Verified]
- **Agent design:** Tools: SF-86 parser, records-check queues, discrepancy flagger. Human gate: adjudicator makes all determinations.
- **Open source today:** none found (gh search repos "security clearance investigation", stars >= 20, not archived: no results).
- **Demo path:** Synthetic SF-86-like forms.
- **Verification:** 2026-11-06, Verified, repos checked yes (search only)

### 10. Medicaid renewal (ex parte) and procedural-denial prevention
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is a state Medicaid agency; systems are eligibility system, data hubs, mailed-notice vendors; 42 CFR 435.916 ex parte renewal rule; caseworker approves terminations.
- **Problem and today's workflow:** Caseworkers try data-based renewals, then send forms and chase responses.
- **Evidence:** KFF tracker: "at least 25,198,000 Medicaid enrollees had been disenrolled" as of September 12, 2024, and "69% of all people disenrolled had their coverage terminated for procedural reasons". https://www.kff.org/medicaid/issue-brief/medicaid-enrollment-and-unwinding-tracker/ (archived page; the rate varies with the denominator used). [Verified]
- **Agent design:** Tools: data-source matching, notice generator, outreach scheduler. Human gate: caseworker approves any termination.
- **Open source today:** none found for renewals (gh search repos "Medicaid renewal", stars >= 20, not archived: no results). navapbc/oscer (26 stars, Apache-2.0, last push 2026-11-03; README read: yes) is for work-requirement reporting; adjacent only.
- **Demo path:** KFF/CMS public unwinding data with synthetic cases.
- **Verification:** 2026-11-06, Verified, repos checked yes

## Sources
- https://www.eenews.net/articles/watchdog-foia-backlog-undermines-open-government-goals/ ; https://www.gao.gov/products/gao-24-106535 (opened, chart only)
- https://fns-prod.azureedge.us/node/22999
- https://gao.gov/products/gao-23-106696
- https://nepa.gov/sites/default/files/documents/CEQ_EIS_Timeline_Report_2020-6-12.pdf
- https://www.nextgov.com/digital-government/2025/08/veterans-affairs-reduces-claims-backlog-record-rate/407429/
- https://www.fox6now.com/news/wisconsin-body-camera-video-cost
- https://www.ACUS.GOV/sites/default/files/documents/Draft%20Report_Mass%2C%20Computer-Generated%2C%20and%20Fraudulent%20Comments_04022021.pdf (reference, not confirmed)
- https://docs.house.gov/meetings/GO/GO24/20190717/109809/HHRG-116-GO24-Wstate-CheriyanA-20190717.pdf
- https://blog.clearedjobs.net/what-dcsa-does/
- https://www.kff.org/medicaid/issue-brief/medicaid-enrollment-and-unwinding-tracker/
- https://www.gao.gov/products/gao-25-107753 (context: GAO FY2024 improper payments about $162B across 68 programs; not re-opened in this pass)
- https://www.foia.gov/data.html ; https://www.regulations.gov/ ; https://www.usaspending.gov/ ; https://www.paymentaccuracy.gov/ ; https://www.fns.usda.gov/snap/qc/data ; https://github.com/usnistgov/oscal-content
