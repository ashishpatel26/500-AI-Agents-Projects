# Real Estate

## Overview
Real estate work is document-heavy and transaction-driven: leases, title chains, loan files, appraisals, plan sets and draw packages are read, cross-checked and re-keyed by people before money moves or a filing is accepted. Manual effort concentrates at the handoffs between systems (lease admin to ERP, title plant to underwriter, LOS to investor, plan portal to code library). Errors are costly because they become financial-reporting misstatements, defective loans, fair-housing liability, or stolen closing funds.

## Systems of record, regulations, public datasets
- **Systems:** lease administration / ERP (Yardi, MRI, SAP RE-FX, Oracle), property management (AppFolio, RealPage), loan origination systems (Encompass), title production software (SoftPro, Qualia, RamQuest), county recorder and assessor systems, municipal permit portals (Accela, Tyler EnerGov), CMBS servicer platforms, appraisal management systems, MLS.
- **Regulations/standards:** IFRS 16 (2016) and ASC 842 (2016) lease accounting (IFRS 16 publication of January 2016 confirmed on ifrs.org); TRID/RESPA/TILA (CFPB, 2015 rule); ECOA and Fair Housing Act (1968); FCRA (1970; CFPB advisory on name-only matching confirmed on consumerfinance.gov); GLBA Safeguards Rule; ALTA Best Practices; UCDP/UAD appraisal standards (FHFA, GSEs; FHFA ROV policy announced 1 May 2024, confirmed on fhfa.gov); local building and zoning codes (IBC/IRC adoptions). Not individually confirmed against official text: ASC 842, TRID/RESPA/TILA 2015 rule, ECOA, GLBA Safeguards, ALTA Best Practices, UAD.
- **Public datasets for demos:** HUD Fair Market Rents and open data https://www.huduser.gov/portal/datasets/fmr.html ; HMDA loan-level data https://ffiec.cfpb.gov/data-browser/ ; NYC DOB permit data https://data.cityofnewyork.us/ ; SEC EDGAR lease exhibits (10-K Exhibit 10 leases) https://www.sec.gov/edgar ; CMBS 15-E / EDGAR ABS-EE filings https://www.sec.gov/edgar ; CourtListener eviction opinions https://www.courtlistener.com/ .

## Use cases

### 1. Commercial lease abstraction and lease-accounting data
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is a REIT, corporate real-estate or property manager; systems are lease admin/ERP and document repositories; IFRS 16/ASC 842 audit trail; lease accountant approves abstract before posting.
- **Problem and today's workflow:** Lease administrators read the base lease plus every amendment to extract rent steps, options, CAM caps and critical dates, then key them into the lease system. Accountants re-check against payment history for the lease liability schedule.
- **Evidence:** IFRS Foundation: "Listed companies using IFRS Standards or US GAAP are estimated to have around US$3.3 trillion of lease commitments", "over 85 per cent of which do not appear on their balance sheets". https://www.ifrs.org/news-and-events/news/2016/01/iasb-shines-light-on-leases-by-bringing-them-onto-the-balance-sheet/ . Per-lease abstraction hours: no reliable independent figure found. [Verified]
- **Agent design:** Tools: PDF/OCR parser, lease-system API, payment-ledger query. Steps: order amendments, resolve supersession, extract fields with page citations, reconcile with ledger, flag conflicts. Human gate: lease accountant approves each abstract before posting.
- **Open source today:** none found (gh search repos "lease abstraction", stars >= 20, not archived: no results).
- **Demo path:** Public 10-K lease exhibits from SEC EDGAR plus synthetic amendments; score field-level accuracy against hand-labelled abstracts.
- **Verification:** 2026-11-06, Verified, repos checked yes (search only)

### 2. Closing wire-fraud and payoff verification
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is a title/escrow company or settlement attorney; systems are title production software, bank portal, email; GLBA and funds-transfer liability; escrow officer releases the wire.
- **Problem and today's workflow:** Escrow officers verify wiring instructions and lender payoff letters, which fraudsters spoof via email, using callbacks and spot checks.
- **Evidence:** HousingWire: "In 2023, the FBI received 21,489 complaints about business email compromise", with losses of "$2.9 billion"; the article says BEC is how most real estate fraud is carried out and reports $145.243 million in real-estate-related cybercrime losses overall. https://www.housingwire.com/articles/cybercrime-losses-hit-record-high-in-2023/ (secondary reporting of FBI IC3; the IC3 report itself was not opened). [Verified]
- **Agent design:** Tools: email header analysis, domain-age/WHOIS lookup, payoff-letter parser, prior-instruction comparison, callback task queue. Steps: score each instruction change, require callback to a known number. Human gate: officer releases funds; agent never sends wires.
- **Open source today:** none found (gh search repos "escrow wire fraud", stars >= 20, not archived: no results).
- **Demo path:** Synthetic escrow files with injected altered account numbers and lookalike domains; measure detection and false-block rate.
- **Verification:** 2026-11-06, Verified, repos checked yes (search only)

### 3. Municipal building-permit plan review
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is a city building department; systems are the permit portal and code library; public-record and life-safety obligations; licensed plan reviewer signs off.
- **Problem and today's workflow:** Reviewers check drawings against zoning and building codes over multiple correction rounds; applicants resubmit.
- **Evidence:** Denver auditor: "Between 2020 and the first part of 2023, average wait times for residential project permits grew by 75 percent, or 113 days". https://businessden.com/residential-permit-delays-caused-in-part-by-review-errors-unreliable-data-auditor-says/ [Verified]
- **Agent design:** Tools: plan-set parser, code-section retriever (adopted code edition), zoning GIS, comment-letter generator. Steps: extract dimensions/occupancy, test against code, cite sections. Human gate: reviewer approves or edits every correction comment.
- **Open source today:** mikeOnBreeze/cc-crossbeam (298 stars, MIT, not archived, last push 2026-10-30; README read: yes). README describes AI plan check for cities and counties (intake screening, plan review, corrections letters, backchecks); it truly addresses the use case. inosca/ebau (26 stars, EUPL-1.2, last push 2026-09-16; README not read, description only) is a Swiss building-permit application system; adjacent only.
- **Demo path:** Open residential plan sets from city permit portals with the adopted IRC text; seed known violations.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 4. Tenant screening accuracy and FCRA dispute handling
- **Tier:** B. Enterprise: pass
- **Enterprise check:** Buyer is a screening agency or property manager; systems are court-record feeds, credit bureaus, property management software; FCRA and Fair Housing Act; human decides adverse action.
- **Problem and today's workflow:** Analysts match applicants to eviction/criminal records and investigate disputes within statutory time limits.
- **Evidence:** CFPB page: "matching consumer records solely through the matching of names is illegal under the Fair Credit Reporting Act" (advisory opinion on false identifications). https://www.consumerfinance.gov/about-us/newsroom/cfpb-reports-highlight-problems-with-tenant-background-checks . TransUnion and its rental-screening subsidiary settled with the CFPB and FTC for $15 million over inaccurate tenant screening reports (headline of a law-firm post, October 2023): https://www.consumerfinancialserviceslawmonitor.com/2023/10/trans-union-settles-for-15-million-with-cfpb-and-ftc-over-tenant-screening-reports/ . Corrected: the $15M is not on the CFPB page, and the "Nov 2022" date for the CFPB report was not confirmed. [Corrected]
- **Agent design:** Tools: record-source queries, identity-matching with confidence, dispute tracker with deadline clock. Steps: re-verify matches against primary court records, draft dispute response. Human gate: investigator signs corrections and adverse-action notices.
- **Open source today:** none found for screening disputes (gh search repos "tenant screening", stars >= 20, not archived). yakew7/Fair-Code (55 stars, MIT, not archived, last push 2026-11-05; README read: yes) is a bias-audit educational project covering several domains including tenant screening; adjacent only.
- **Demo path:** Synthetic applicants with ambiguous names against public court-docket samples (CourtListener).
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 5. Mortgage loan file assembly and condition clearing
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is a lender or mortgage servicer; systems are the LOS, income/asset verification services, appraisal portal; ECOA, TRID, GLBA, repurchase risk; underwriter decides.
- **Problem and today's workflow:** Processors collect income, asset and appraisal documents, reconcile discrepancies and clear underwriting conditions against agency guidelines.
- **Evidence:** MBA letter to the CFPB (PDF text read): "for the consumer direct channel, fulfillment costs reached $4,077 per loan originated in 2023" (retail $3,483). This is fulfillment cost only (underwriting, closing, other fulfillment), not total production cost. https://newslink.mba.org/wp-content/uploads/2024/08/8-2-24-CFPB-Closing-Cost-RFI.pdf [Verified]
- **Agent design:** Tools: document classifier, LOS API, Fannie/Freddie guideline retriever, borrower-request drafts. Steps: map documents to conditions, cross-check figures. Human gate: underwriter clears conditions and makes the credit decision.
- **Open source today:** none found (gh search repos "mortgage loan underwriting document", stars >= 20, not archived: no results).
- **Demo path:** HMDA data for realistic loan attributes plus synthetic paystubs/bank statements.
- **Verification:** 2026-11-06, Verified, repos checked yes (search only)

### 6. Title examination and curative-item tracking
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is a title insurer or agency; systems are title plant, county recorder images, title production software; state insurance regulation and ALTA Best Practices; licensed examiner/underwriter signs the commitment.
- **Problem and today's workflow:** Examiners trace the chain of title through recorded deeds, mortgages, liens and judgments, list exceptions, then chase curative documents.
- **Evidence:** ALTA release: "the title insurance industry generated $15.1 billion in title insurance premiums during 2023"; "In 2023, the industry paid more than $638 million in claims." https://alta.org/news-and-publications/press-release/Title-Insurance-Premium-Volume-Decreased-31-in-2023-ALTA-Reports (the earlier PDF link was also read via text extraction and matches). [Verified]
- **Agent design:** Tools: recorder-image OCR, legal-description parser, lien/judgment search, curative-letter drafter. Steps: build chain, flag gaps/liens, track cures. Human gate: examiner approves schedule B exceptions.
- **Open source today:** none found (gh search repos "title examination", stars >= 20, not archived: no results).
- **Demo path:** Open county recorder samples (e.g., public deed indexes) with synthetic chain breaks.
- **Verification:** 2026-11-06, Verified, repos checked yes (search only)

### 7. Fair-housing compliance review of listings and ad campaigns
- **Tier:** B. Enterprise: pass
- **Enterprise check:** Buyer is a brokerage, portal or property manager; systems are MLS, CRM, ad platforms; Fair Housing Act (1968), HUD guidance; compliance officer approves.
- **Problem and today's workflow:** Compliance staff manually spot-check listing text, targeting settings and photos for discriminatory content or steering.
- **Evidence:** NFHA: "There were 34,150 fair housing complaints received in 2023, compared to 33,007 complaints received in 2022". https://nationalfairhousing.org/housing-discrimination-complaints-continue-to-trend-upward/ . Corrected: the DOJ 2022 Meta settlement civil penalty of $115,054 could not be confirmed (the DOJ page fetched empty; a search extract only), so it is removed from the evidence; the original NFHA PDF link returned HTTP 404. [Corrected]
- **Agent design:** Tools: listing/ad API pulls, phrase and image checks, targeting-setting audit. Steps: score, propose compliant rewrites, log decision. Human gate: compliance officer approves publish or edit.
- **Open source today:** none found (gh search repos "fair housing listing", stars >= 20, not archived: no results).
- **Demo path:** Synthetic listings with seeded discriminatory phrases; public HUD advertising guidance as rubric.
- **Verification:** 2026-11-06, Corrected, repos checked yes (search only)

### 8. Appraisal review and reconsideration-of-value handling
- **Tier:** B. Enterprise: needs figure
- **Enterprise check:** Buyer is a lender or appraisal management company; systems are LOS, UCDP/EAD submission, AMC platform; ECOA/Fair Housing, FHFA ROV policies (2024); review appraiser decides.
- **Problem and today's workflow:** Reviewers check appraisal reports for comparable selection, UAD errors and prohibited language and handle borrower ROV requests.
- **Evidence:** FHFA: on May 1, 2024 it announced that Fannie Mae and Freddie Mac published new reconsideration-of-value policies; lenders must disclose the ROV process, standardize communication with appraisers and meet response timelines. https://www.fhfa.gov/news/news-release/fhfa-announces-enterprise-reconsideration-of-value-policies . Corrected: the Freddie Mac "12.5% of Black-tract properties appraised below contract" figure was never traced to a primary source and is removed. [Corrected]
- **Agent design:** Tools: report parser, MLS comp search, AVM, UCDP edit rules. Steps: recompute adjustments, draft ROV letter. Human gate: staff appraiser approves the review.
- **Open source today:** none found (gh search repos "appraisal review", stars >= 20, not archived: no results).
- **Demo path:** Synthetic appraisal XML (MISMO) with injected comp errors.
- **Verification:** 2026-11-06, Corrected, repos checked yes (search only)

### 9. CRE rent-roll and T-12 underwriting plus covenant monitoring
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is a CRE lender, special servicer or fund; systems are servicer platforms, property accounting, loan data tapes; SEC ABS reporting/CREFC IRP standards; credit officer approves.
- **Problem and today's workflow:** Analysts normalize borrower rent rolls and operating statements, tie them to leases, and flag DSCR and occupancy covenant breaches.
- **Evidence:** MBA NewsLink summary of Trepp: the overall CMBS delinquency rate for December 2025 "grew in December, up four basis points to 7.3%". https://newslink.mba.org/servicing-tag/cmbs . Corrected: the "office 11.68% in November" figure sat on a GlobeSt page that returned HTTP 403 and the opened page gave no office rate (a search extract suggests December office was 11.31% and 11.68% was November), so the office number is removed. [Corrected]
- **Agent design:** Tools: spreadsheet parser, lease abstracts, servicer API, covenant calculator. Steps: normalize, reconcile, flag. Human gate: credit officer signs the watchlist/risk rating.
- **Open source today:** none found (gh search repos "rent roll underwriting", stars >= 20, not archived: no results).
- **Demo path:** SEC EDGAR ABS-EE property-level CMBS data.
- **Verification:** 2026-11-06, Corrected, repos checked yes (search only)

### 10. Construction-loan draw package review
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer is a construction lender or title/draw administrator; systems are loan servicing, inspection reports, lien-waiver trackers; state lien law and bank regulatory exam; loan administrator releases funds.
- **Problem and today's workflow:** Staff match draw requests, invoices, lien waivers and inspector percent-complete reports before each disbursement.
- **Evidence:** no reliable national figure found. Case example only: "the indictment says $188,000 was advanced for subcontractor work that was never performed" (Muncie contractor, fake lien waivers). https://colemanreport.com/fraud-friday-9-fake-lien-waivers-zero-work-muncie-contractor-indicted-on-188000-construction-loan-draw-fraud/ [Verified]
- **Agent design:** Tools: invoice/waiver parser, budget ledger, photo-inspection comparison. Steps: tie waivers to invoices, check prior-draw releases. Human gate: administrator approves disbursement.
- **Open source today:** none found (gh search repos "construction draw lien waiver", stars >= 20, not archived: no results).
- **Demo path:** Synthetic G702/G703 draw packages with inflated waivers.
- **Verification:** 2026-11-06, Verified (case example only), repos checked yes (search only)

## Sources
- https://www.ifrs.org/news-and-events/news/2016/01/iasb-shines-light-on-leases-by-bringing-them-onto-the-balance-sheet/
- https://www.housingwire.com/articles/cybercrime-losses-hit-record-high-in-2023/
- https://businessden.com/residential-permit-delays-caused-in-part-by-review-errors-unreliable-data-auditor-says/
- https://www.consumerfinance.gov/about-us/newsroom/cfpb-reports-highlight-problems-with-tenant-background-checks
- https://www.consumerfinancialserviceslawmonitor.com/2023/10/trans-union-settles-for-15-million-with-cfpb-and-ftc-over-tenant-screening-reports/
- https://newslink.mba.org/wp-content/uploads/2024/08/8-2-24-CFPB-Closing-Cost-RFI.pdf
- https://alta.org/news-and-publications/press-release/Title-Insurance-Premium-Volume-Decreased-31-in-2023-ALTA-Reports
- https://nationalfairhousing.org/housing-discrimination-complaints-continue-to-trend-upward/
- https://www.justice.gov/archives/opa/pr/justice-department-secures-groundbreaking-settlement-agreement-meta-platforms-formerly-known (reference, not confirmed)
- https://www.fhfa.gov/news/news-release/fhfa-announces-enterprise-reconsideration-of-value-policies
- https://newslink.mba.org/servicing-tag/cmbs ; https://www.globest.com/amp/2025/12/23/market-at-an-inflection-point-as-cmbs-strength-masks-rising-stress/ (reference, not confirmed)
- https://colemanreport.com/fraud-friday-9-fake-lien-waivers-zero-work-muncie-contractor-indicted-on-188000-construction-loan-draw-fraud/
- https://www.huduser.gov/portal/datasets/fmr.html ; https://ffiec.cfpb.gov/data-browser/ ; https://data.cityofnewyork.us/ ; https://www.sec.gov/edgar ; https://www.courtlistener.com/
