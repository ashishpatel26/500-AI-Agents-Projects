# Nonprofit & Social Impact

## Overview
Nonprofits and NGOs spend a large share of staff time on funder-driven compliance (grant reporting, audits, registrations), casework intake, and reconciling data between field systems and finance. Manual work concentrates in eligibility screening, document chasing, and turning program data into regulator- or funder-ready reports. Consumer-facing benefits navigation was deliberately excluded; every use case below has an organizational buyer (legal-aid org, CoC lead agency, international NGO, foundation, charity finance team).

## Systems of record, regulations, public datasets
- **Systems:** Salesforce Nonprofit Cloud / NPSP, Blackbaud Raiser's Edge, case management (LegalServer, Apricot), HMIS (Clarity, WellSky), ERP/GL (Sage Intacct, QuickBooks), grants management (Fluxx, Submittable), KoBo/ODK field data, UNHCR proGres / WFP SCOPE-type registries.
- **Regulation/standards:** 2 CFR 200 Uniform Guidance and Single Audit (revised 2024); HUD HMIS Data Standards and CoC Program rules; VAWA/FVPSA confidentiality; IRS Form 990 and state charitable solicitation statutes; OFAC sanctions; IRS expenditure responsibility / equivalency determination (IRC 4945); UK Gift Aid rules (Income Tax Act 2007, Part 8); UN Humanitarian Programme Cycle and IASC data-responsibility guidance; GDPR.
- **Public datasets:** HUD AHAR / PIT counts https://www.huduser.gov/portal/datasets/ahar.html ; Federal Audit Clearinghouse https://app.fac.gov/ ; OCHA HDX (HNO/3W data) https://data.humdata.org/ ; IRS Form 990 e-file data https://www.irs.gov/charities-non-profits/form-990-series-downloads ; USAspending grants https://www.usaspending.gov/ ; OFAC SDN list https://sanctionssearch.ofac.treas.gov/ ; HMRC charity tax relief stats https://www.gov.uk/government/statistics/uk-charity-tax-relief-statistics

## Use cases

### 1. Legal-aid intake, triage and referral
- **Tier:** A Enterprise: pass
- **Enterprise check:** Buyer: legal-aid org / LSC grantee. Systems: case management (LegalServer), conflicts DB, court e-filing calendars. Regulation: LSC eligibility rules (45 CFR 1611), attorney-client confidentiality, UPL limits. Human gate: attorney accepts or declines every matter.
- **Problem and today's workflow:** Intake staff phone-screen callers for income eligibility, issue type and conflicts, then manually compute deadlines (e.g., eviction answer dates) and refer. Most callers are turned away or under-served for lack of capacity.
- **Evidence:** LSC Justice Gap: "Low-income Americans did not receive any legal help or enough legal help for 92% of the problems" that substantially affected their lives; "LSC-funded organizations are unable to provide any or enough legal help for 71% of the civil legal problems brought to them" (about 1.4 million problems per year per the page). https://justicegap.lsc.gov/resource/section-1-introduction/ (opened). [Verified]
- **Agent design:** Multilingual intake, eligibility calculator, conflict search, deadline extraction from notices, draft referral and case summary into case management. Attorney reviews every decline and every deadline.
- **Open source today:** none found (gh search "legal aid intake", stars>=20: 0 hits).
- **Demo path:** Synthetic intake transcripts plus public court-rule deadline tables; LSC published eligibility guidelines.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 2. Humanitarian needs assessment and appeal prioritization
- **Tier:** A Enterprise: pass
- **Enterprise check:** Buyer: OCHA cluster lead / international NGO. Systems: KoBo/ODK, HDX, 3W databases, Financial Tracking Service. Regulation/audit: IASC data responsibility, donor reporting, do-no-harm. Human gate: humanitarian coordinator and cluster leads sign the HNRP.
- **Problem and today's workflow:** Analysts consolidate heterogeneous assessments, displacement figures and 3W data into severity tables and funding appeals, largely in spreadsheets, under tight annual cycle deadlines.
- **Evidence:** Search-tool excerpts of OCHA coverage confirm the GHO 2025 launch (4 Dec 2024) sought about $47 billion for about 305 million people in need. The cited humanitarianaction.info page returned 403, and no source I reached shows "under 17% funded by August 2025" or the "hyper-prioritized" wording, so those are removed. Funding history seen: 45% (2023) and 43% (2024) funded. Reference: https://humanitarianaction.info/article/inter-agency-coordinated-appeal-september-update [Corrected] (launch figures from search excerpt, page not opened)
- **Agent design:** Pulls HDX/3W/assessment files, harmonizes admin codes (P-codes), joins geospatially, drafts severity tables and scenario prioritizations with cited sources. Coordinators approve numbers and framing.
- **Open source today:** none found (gh search "humanitarian needs assessment", stars>=20: 0 hits).
- **Demo path:** HDX Humanitarian Needs Overview and 3W datasets for a single country.
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 3. Homelessness coordinated entry and housing placement
- **Tier:** B (matching rules are mostly deterministic; agent handles document chase and case follow-up) Enterprise: needs figure (headcount only; no cost-per-case or dollar figure)
- **Enterprise check:** Buyer: CoC lead agency. Systems: HMIS, housing-provider vacancy lists, ID/document stores. Regulation: HUD CoC/HMIS standards, VAWA confidentiality, consent. Human gate: case manager and CoC prioritization committee decide placement.
- **Problem and today's workflow:** Staff assess households, track documents (ID, income, disability verification), prioritize by vulnerability and phone landlords, in HMIS plus spreadsheets.
- **Evidence:** HUD 2024 AHAR Part 1: 771,480 people homeless on a single night in January 2024, up 18% from 2023, a record (confirmed in several search excerpts including HUD's release pr24-327; the AHAR PDF fetch returned empty, so the PDF itself was not read). https://www.huduser.gov/portal/sites/default/files/pdf/2024-AHAR-Part-1.pdf [Search-excerpt] (search excerpt only)
- **Agent design:** Reads HMIS (via export/API), flags missing documents, drafts outreach to households and landlords, schedules follow-ups. Never scores or ranks households autonomously, because vulnerability tools have documented racial bias; committee decides.
- **Open source today:** greenriver/boston-cas (27 stars, GPL-3.0, not archived, last push 2026-11-02; README read: yes, rule-based matching of homeless clients to housing vacancies alongside an HMIS warehouse; adjacent only, a matching system not a document-chase agent).
- **Demo path:** Synthetic HMIS CSV following the HUD data standard; AHAR PIT totals for scale.
- **Verification:** 2026-11-06, Verified (search excerpt), repos checked yes

### 4. Federal-grant compliance and Single Audit readiness
- **Tier:** A Enterprise: needs figure
- **Enterprise check:** Buyer: nonprofit finance/controller. Systems: GL/ERP, payroll and timekeeping, procurement, grants system. Regulation: 2 CFR 200, Single Audit at $1,000,000+ federal spend, False Claims Act. Human gate: controller and auditor sign-off.
- **Problem and today's workflow:** Finance staff match ledger entries to award terms and supporting documents (time allocations, procurement files) and compile schedules of expenditures of federal awards by hand before audit.
- **Evidence:** The cited Washington State Auditor page was opened and does not state the Single Audit threshold (it only says unallowable costs "that exceed $25,000" are reported as questioned costs). The $1,000,000 threshold claim was not confirmed on any page I could open (eCFR redirected), so it is removed. Reference, not confirmed: https://sao.wa.gov/node/2337 . [Unconfirmed]
- **Agent design:** Pulls GL lines by award, tests allowability, finds missing support, drafts SEFA and finding-style memos. Controller approves adjustments.
- **Open source today:** none found (gh search "single audit", stars>=20: only unrelated hits).
- **Demo path:** Federal Audit Clearinghouse public findings as examples; synthetic GL with seeded unallowable costs.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 5. Funder reporting and outcomes consolidation
- **Tier:** B Enterprise: needs figure (only an unsourced percentage)
- **Enterprise check:** Buyer: program/MEL team. Systems: case management, CRM, survey tools, funder portals. Regulation/audit: grant agreements, data-sharing and privacy terms. Human gate: program director certifies every report.
- **Problem and today's workflow:** Each funder wants a different template; staff re-key program outputs and narratives from several systems quarterly.
- **Evidence:** The 18F wiki says "Currently up to 40% of a grants budget can be spent on reporting on the grant" under Key Metrics, with no source cited, so it is an unsourced claim, not a measured figure. https://www.github.com/18F/federal-grant-reporting/wiki (opened). [Verified] (wording only; underlying figure unsourced)
- **Agent design:** Maps funder indicators to internal fields, queries systems, drafts narrative with data tables, flags gaps. Director approves submission.
- **Open source today:** none found (gh search "grant reporting", stars>=20: only unrelated hits).
- **Demo path:** Synthetic program dataset and two mock funder templates.
- **Verification:** 2026-11-06, Verified (unsourced claim), repos checked yes

### 6. Cash-assistance registration, deduplication and payment reconciliation
- **Tier:** A Enterprise: pass
- **Enterprise check:** Buyer: humanitarian agency / cash working group. Systems: beneficiary registries (SCOPE, proGres), mobile-money/FSP payment files, complaint hotlines. Regulation: donor audit, data-protection policies, sanctions. Human gate: programme officer approves payment lists and exclusions.
- **Problem and today's workflow:** Overlapping partners register the same households; staff dedupe lists in Excel and reconcile FSP payment files against targeted lists.
- **Evidence:** A search-tool excerpt says the Food Security Sector (Cox's Bazar) concept note reports that 27% of targeted beneficiaries were targeted by multiple partners after national-ID cross-checking; the PDF returned 403 and was not opened, and no independent confirmation was found. The "WFP cash-based transfer value ~$2.8B in 2023" is corrected: search excerpts of WFP documents give about $2.9B (cash-based transfers and commodity vouchers, down from $3.3B in 2022), also not opened. https://fscluster.org/sites/default/files/documents/fsl_deduplication_exercise_concept_note_v.1_as_of_22_september_1.pdf [Corrected]
- **Agent design:** Fuzzy household matching with explainable evidence, payment-file reconciliation, exception queue. Humans resolve ambiguous matches and approve payments; no biometric data to external LLMs.
- **Open source today:** none found (gh search "beneficiary deduplication", stars>=20: 0 hits).
- **Demo path:** Synthetic household registries with injected duplicates and transliteration variants.
- **Verification:** 2026-11-06, Corrected (search excerpts), repos checked yes

### 7. Form 990 preparation and multi-state charity registration
- **Tier:** A Enterprise: needs figure
- **Enterprise check:** Buyer: charity finance/compliance. Systems: GL, donor CRM (state-level solicitation data), registration portals. Regulation: IRS Form 990 series; state charitable solicitation statutes. Human gate: officer and CPA sign.
- **Problem and today's workflow:** Staff rebuild 990 schedules from the ledger and file state registrations/renewals with differing forms and due dates.
- **Evidence:** IRS page: "Most states have statutes that require charitable organizations that solicit contributions from the public to register"; many states also accept a copy of Form 990 in place of some financial paperwork. https://www.irs.gov/charities-non-profits/charitable-organizations/charitable-solicitation-periodic-state-reporting (opened). The dated "about 40 states" law-firm claim was not checked and is removed. [Verified]
- **Agent design:** Maps GL to 990 lines, pulls state requirements, assembles packets, tracks deadlines. CPA/officer review and sign.
- **Open source today:** jc2744-fintech/taxguard-xai (989 stars, MIT, not archived, last push 2026-08-05; README read: yes, interpretable review prioritization on public Form 990 filings; adjacent only, it screens filings and does not prepare them).
- **Demo path:** IRS 990 e-file public data as target format; synthetic GL.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 8. UK Gift Aid claim preparation and donor-declaration audit
- **Tier:** B Enterprise: pass
- **Enterprise check:** Buyer: UK charity. Systems: donor CRM, payment processors, HMRC Charities Online. Regulation: Gift Aid declaration rules; HMRC audit. Human gate: finance lead submits claim.
- **Problem and today's workflow:** Teams match donations to valid declarations, fix address/name mismatches and submit claims; errors cause clawback.
- **Evidence:** HMRC charity tax relief statistics: in the tax year to April 2024, Gift Aid paid to charities and CASCs was 1.6 billion pounds across 66,310 organisations (read from the page's Chart 2a/2b data, tax-year-ending-2024 row; the page's prose covers a later year). https://www.gov.uk/government/statistics/uk-charity-tax-relief-statistics/uk-charity-tax-relief-statistics-commentary (opened). [Verified]
- **Agent design:** Validates declarations, reconciles processor exports, drafts claim file and exception list. Finance lead approves.
- **Open source today:** JustinBusschau/hmrc-gift-aid (21 stars, GPL-3.0, not archived, last push 2021-09-10, stale; README read: yes, PHP library for submitting Gift Aid claims to HMRC; adjacent only, no declaration audit).
- **Demo path:** Synthetic donations with realistic declaration defects.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 9. Partner and vendor due diligence with sanctions screening for international NGOs
- **Tier:** A Enterprise: needs figure
- **Enterprise check:** Buyer: NGO compliance/finance. Systems: ERP vendor master, sub-award system, OFAC/UN/EU lists, adverse media. Regulation: OFAC, donor flow-down clauses, counter-terrorism financing rules. Human gate: compliance officer clears or rejects.
- **Problem and today's workflow:** Staff screen sub-recipients and vendors by name against lists, research ownership, and document the decision for donors.
- **Evidence:** no reliable figure found. Reference only; nothing to verify. [Unconfirmed]
- **Agent design:** Entity resolution against SDN and UN lists, ownership research, risk memo with sources. Officer decides and logs.
- **Open source today:** Divine16/Sanctions-screening-benchmark (33 stars, MIT, not archived, last push 2026-08-13; README read: yes, a benchmark for name-screening recall across name-variation classes; adjacent only, it tests engines rather than running vendor due diligence). Wallet-Risk-Scanner is crypto-specific and not relevant.
- **Demo path:** OFAC SDN list plus synthetic vendor master with fuzzy-name traps.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 10. Foundation cross-border grant due diligence (equivalency determination)
- **Tier:** A Enterprise: needs figure (no cross-border volume)
- **Enterprise check:** Buyer: private foundation / DAF sponsor. Systems: grants management, foreign-entity document store. Regulation: IRC 4945 expenditure responsibility, IRS equivalency rules, OFAC. Human gate: grants officer and counsel approve.
- **Problem and today's workflow:** Staff collect foreign charity documents, compare governance and charitable-purpose requirements to US equivalents, and draft a determination memo.
- **Evidence:** Give.org summary of Giving USA 2025: "Foundations - 19% - $109.81 billion" of 2024 giving. https://give.org/news/wise-giving-wednesday-total-2024-giving-shows-moderate-growth-over-previous-year (opened). Cross-border share: no reliable figure found. [Verified]
- **Agent design:** Document intake and translation, checklist-based gap analysis, draft memo with citations. Counsel signs.
- **Open source today:** none found (gh search "expenditure responsibility foundation grant", stars>=20: only an unrelated hit).
- **Demo path:** Synthetic foreign-NGO document bundles.
- **Verification:** 2026-11-06, Verified, repos checked yes

## Sources
- https://justicegap.lsc.gov/resource/section-1-introduction/
- https://humanitarianaction.info/article/inter-agency-coordinated-appeal-september-update
- https://www.huduser.gov/portal/sites/default/files/pdf/2024-AHAR-Part-1.pdf
- https://sao.wa.gov/node/2337
- https://www.github.com/18F/federal-grant-reporting/wiki
- https://fscluster.org/sites/default/files/documents/fsl_deduplication_exercise_concept_note_v.1_as_of_22_september_1.pdf
- https://www.irs.gov/charities-non-profits/charitable-organizations/charitable-solicitation-periodic-state-reporting
- https://www.gov.uk/government/statistics/uk-charity-tax-relief-statistics/uk-charity-tax-relief-statistics-commentary
- https://give.org/news/wise-giving-wednesday-total-2024-giving-shows-moderate-growth-over-previous-year
- Dataset URLs listed under "Systems of record" above
