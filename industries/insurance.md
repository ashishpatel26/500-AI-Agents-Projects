# Insurance

## Overview
Property and casualty, life and health insurers spend most operating effort on moving documents and decisions between intake, underwriting, claims and finance. Manual work concentrates in claims handling (first notice, investigation, recovery), commercial underwriting submissions, reinsurance reporting, and regulatory filings. Decisions are regulated by unfair-claims-practices law, so agents should prepare and recommend while licensed adjusters and underwriters decide.

Verification note (2026-11-06): only the figures tagged below were checked against pages. Regulation names and dates in this file (NAIC bulletin, Colorado SB21-169, EU AI Act, Solvency II etc.) were not re-checked against official text and should be read as unconfirmed.

## Systems of record, regulations, public datasets
- **Systems:** policy administration (Guidewire PolicyCenter, Duck Creek), claims system (Guidewire ClaimCenter), billing, underwriting workbench, broker email inboxes, reinsurance/treaty system, SIU case management, ISO ClaimSearch and CLUE, document management, payments/ERP, SERFF filing system.
- **Regulations / standards:** state Unfair Claims Settlement Practices laws based on the NAIC model act; NAIC Model Bulletin on the Use of AI Systems by Insurers (2023); NAIC annual statement and Schedule P; state anti-fraud reporting laws; Colorado SB21-169 on external data and algorithms (2021); EU Solvency II and IDD; EU AI Act (2024) high-risk classification for life/health pricing and underwriting; ACORD data standards; GDPR/CCPA.
- **Public datasets:** OpenFEMA NFIP claims https://www.fema.gov/openfema-data-page/fima-nfip-claims ; NOAA Storm Events https://www.ncei.noaa.gov/stormevents/ ; NOAA billion-dollar disasters https://www.ncei.noaa.gov/access/billions/ ; NAIC public consumer complaint data https://content.naic.org/consumer/data ; SERFF public filing access https://filingaccess.serff.com ; synthetic claims datasets on Kaggle/Hugging Face (pick one with a licence you can use).

## Use cases

### 1. Claims fraud (SIU) investigation support
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is an insurer SIU. Systems: claims system, ISO ClaimSearch, SIU case management, public records, repair/medical invoices. Regulated by state fraud-reporting statutes, unfair claims practices, bad-faith liability, NAIC AI bulletin. Human gate: SIU investigator decides referral and adjuster decides on denial.
- **Problem and today's workflow:** Investigators cross-check documents, invoices, prior-claim networks and public records and assemble a referral file by hand.
- **Evidence:** Coalition Against Insurance Fraud / CSU report (opened, text extracted): "Insurance Fraud Costs the U.S. $308.6 Billion Annually"; the report's tables show a $45 billion property-casualty line. The figure is disputed: the Rutgers Center for Risk and Responsibility paper (opened) says the report's figure "is based on faulty research methodology". https://insurancefraud.org/wp-content/uploads/The-Impact-of-Insurance-Fraud-on-the-U.S.-Economy-Report-2022-8.26.2022.pdf and https://crr.rutgers.edu/wp-content/uploads/sites/22/Misinformation-About-Insurance-Fraud-11-2024.pdf [Verified] (treat as a contested estimate)
- **Agent design:** Tools: claim reader, ISO/public-records lookups, document forensics (metadata, duplicate image check), link-analysis query, referral-pack writer. Steps: score indicators, gather corroboration, write explainable referral reasons. Humans decide; no auto-denial.
- **Open source today:** AvinashSingh786/Fraud-Analysis (56 stars, MIT, not archived, last push 2024-01-10, README read: yes; README says "not maintained often"; classical ML fraud analysis on synthetic data - adjacent only); rh-aiservices-bu/insurance-claim-processing (43 stars, MIT, not archived, last push 2024-08-20, README read: yes; README carries a deprecation warning, workshop lab - adjacent only).
- **Demo path:** Public insurance fraud claims CSV from Kaggle plus synthetic invoices with duplicated images.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 2. Claims first notice of loss (FNOL) intake and triage
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer is an insurer claims operation. Systems: policy admin (coverage check), claims system, telematics/photos, call or email inbox. Regulated by state acknowledgement and fault-assignment deadlines, privacy law. Human gate: adjuster confirms coverage position and assignment.
- **Problem and today's workflow:** Intake staff collect loss facts by phone, email or portal, verify the policy, create the claim, set reserves and route to a handler.
- **Evidence:** no reliable figure found. [Unconfirmed]
- **Agent design:** Tools: policy lookup, claims create API, photo and document extractor, duplicate-claim search. Steps: structure the loss, check coverage in force, flag severity and fraud indicators, propose routing and reserve range. Adjuster approves.
- **Open source today:** microsoft/claims-processing-hack (36 stars, MIT, ARCHIVED, last push 2026-07-22, README read: yes; Microsoft Foundry agents claims-processing hackathon - addresses the use case as a teaching sample only, archived).
- **Demo path:** Synthetic loss narratives and photos with a mock policy table.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 3. Subrogation identification and recovery
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer is an insurer recovery unit. Systems: claims notes, payments, police reports, adverse carrier portals, Arbitration Forums. Regulated by statutes of limitation, state made-whole rules, inter-company arbitration rules. Human gate: recovery specialist approves demand letters and settlement.
- **Problem and today's workflow:** Adjusters often close claims without noticing third-party liability; recovery staff read notes, collect evidence, send demands and chase payment.
- **Evidence:** A National Subrogation article (opened) attributes a subrogation leakage cost to an NAIC study, but gives no study details and the NAIC study was not found, so the dollar figure is not used here. Reference, not confirmed: https://www.nationalsubrogation.com/author/pweilcozen-com/ [Unconfirmed]
- **Agent design:** Tools: claim-note reader, liability-signal extractor, evidence retriever, demand-letter drafter, deadline tracker. Steps: screen closed and open claims, assemble case, draft demand, track limitation dates. Specialist approves.
- **Open source today:** none found (gh search "subrogation", stars>=20: 0 hits).
- **Demo path:** Synthetic auto claim notes with seeded third-party fault statements.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 4. Reinsurance bordereaux preparation and reconciliation
- **Tier:** B (data transformation core; agent handles exceptions and reconciliation). Enterprise: needs figure
- **Enterprise check:** Buyer is a cedent, MGA or reinsurer. Systems: policy admin, claims, treaty/reinsurance system, finance ledger, Lloyd's/market bordereaux templates. Regulated by treaty reporting terms, Solvency II / NAIC credit-for-reinsurance rules, audit. Human gate: reinsurance accountant approves each bordereau before release.
- **Problem and today's workflow:** Analysts compile premium and loss bordereaux from several systems, map to each treaty's format, and reconcile differences by spreadsheet.
- **Evidence:** no reliable figure found. The US Treasury TRIP instructions PDF could not be opened (connection reset), so its relevance as a format reference is unconfirmed: https://home.treasury.gov/system/files/311/TRIP02C-Instructions.pdf [Unconfirmed]
- **Agent design:** Tools: warehouse queries, schema mapper, validation rules, reconciliation to ledger, exception reporter. Steps: map and validate fields, explain breaks, draft the file. Accountant approves release.
- **Open source today:** none found (gh search "reinsurance bordereaux", stars>=20: 0 hits).
- **Demo path:** Synthetic policy and claim tables with two treaty templates.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 5. Commercial underwriting submission intake and triage
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer is a commercial insurer or MGA. Systems: broker email, underwriting workbench, policy admin, exposure data (COPE), third-party data and loss runs. Regulated by state filed rates and rules, NAIC AI bulletin, anti-discrimination law. Human gate: underwriter quotes and binds.
- **Problem and today's workflow:** Underwriting assistants open emails and attachments (ACORD forms, SOVs, loss runs), re-key data, check appetite, and prioritise submissions.
- **Evidence:** no reliable figure found. [Unconfirmed]
- **Agent design:** Tools: email and attachment parser, ACORD/SOV extractor, appetite rules, geocoder, workbench API. Steps: extract, validate, enrich, check appetite, present a summary and gaps list. Underwriter decides.
- **Open source today:** none found for insurance (gh search "underwriting submission", stars>=20: one hit, aws-solutions-library-samples/guidance-for-intelligent-document-processing-agents-on-aws, 27 stars, Apache-2.0, last push 2025-09-08, README read: yes; loan-application document processing, not insurance submissions - adjacent only).
- **Demo path:** Synthetic ACORD-style forms and a property schedule spreadsheet.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 6. Catastrophe claim surge handling
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer is a P&C insurer or TPA. Systems: claims system, policy admin, imagery/aerial providers, adjuster dispatch, payments. Regulated by state catastrophe claim deadlines and emergency orders. Human gate: adjuster approves coverage decisions and payments.
- **Problem and today's workflow:** After a hurricane or hail event, claim volumes spike; staff triage by hand, dispatch field adjusters and approve advance payments from partial information.
- **Evidence:** The earlier "27 billion-dollar disasters in 2024, about $182.7B" claim could not be confirmed (climate.gov fetch failed with connection reset; the NOAA NCEI page opened but showed no figures). Number removed. It was in any case an economic-loss figure, not insured loss. Reference, not confirmed: https://climate.gov/news-features/blogs/beyond-data/2024-active-year-us-billion-dollar-weather-and-climate-disasters [Unconfirmed]
- **Agent design:** Tools: event footprint overlay, policy geocode lookup, imagery damage scoring, dispatch scheduler, payment API. Steps: match claims to affected policies, prioritise severity, propose fast-track payments within limits. Adjuster approves.
- **Open source today:** none found (gh search "catastrophe claims", stars>=20: 0 hits).
- **Demo path:** NOAA Storm Events plus OpenFEMA NFIP claims with synthetic policies.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 7. Bodily-injury claim demand-package review
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer is an insurer's liability claims unit. Systems: claims system, medical records and bills, demand letters, legal hold. Regulated by time-limit demand rules, bad-faith exposure, state fair claims law. Human gate: adjuster and counsel set evaluation and respond.
- **Problem and today's workflow:** Adjusters read hundreds of pages of medical records and bills to build chronologies and evaluate demands against policy limits.
- **Evidence:** no reliable figure found. [Unconfirmed]
- **Agent design:** Tools: document OCR, medical chronology builder, bill-to-record matcher, policy limit lookup, deadline tracker. Steps: summarise treatment, flag unrelated or duplicate charges, draft evaluation memo. Adjuster decides.
- **Open source today:** none found (gh search "demand letter medical", stars>=20: 0 hits).
- **Demo path:** Synthetic medical records from Synthea with generated bills.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 8. Rate and form filing preparation (SERFF)
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer is an insurer's product/compliance team. Systems: actuarial rate models, form library, SERFF, state requirement databases. Regulated by state prior-approval or file-and-use laws. Human gate: compliance and actuarial approve filings.
- **Problem and today's workflow:** Analysts assemble state-specific filings, check each state's rules and objections, and respond to regulator questions.
- **Evidence:** no reliable figure found. [Unconfirmed]
- **Agent design:** Tools: state rule retriever, form diff, exhibit generator, SERFF data exporter, objection-response drafter. Steps: build per-state checklist, populate exhibits, draft responses. Compliance and actuaries approve.
- **Open source today:** none found (gh search "SERFF", stars>=20: 0 hits).
- **Demo path:** Public filings from SERFF Filing Access for one line of business.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 9. Commercial premium audit
- **Tier:** B. Enterprise: needs figure
- **Enterprise check:** Buyer is a workers' compensation / general liability carrier. Systems: policy admin, insured payroll and records, audit workflow tools, classification code manuals. Regulated by state class code rules and audit contract terms. Human gate: auditor finalises and signs the audit.
- **Problem and today's workflow:** Auditors request payroll records, compare to estimates, reclassify exposure and compute final premium.
- **Evidence:** no reliable figure found. [Unconfirmed]
- **Agent design:** Tools: records request, payroll extractor, class code lookup, premium calculator. Steps: reconcile payroll to ledger, flag misclassification, draft audit worksheet. Auditor approves.
- **Open source today:** none found (gh search "premium audit": one hit, AnalytixAudit/Solidity, 26 stars, a smart-contract audit repo, unrelated).
- **Demo path:** Synthetic payroll registers and class code table.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 10. Coverage verification and reservation-of-rights drafting
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer is an insurer's complex claims unit. Systems: policy admin (policy forms and endorsements), claims, legal matter system. Regulated by unfair claims practices, state notice requirements. Human gate: coverage counsel approves letters.
- **Problem and today's workflow:** Adjusters read policy forms and endorsements against loss facts and ask counsel to draft coverage position letters.
- **Evidence:** no reliable figure found. [Unconfirmed]
- **Agent design:** Tools: policy and endorsement retriever, loss-facts extractor, clause matcher, letter template. Steps: map facts to exclusions and conditions, draft position with quotes, track response deadlines. Counsel approves.
- **Open source today:** none found (gh search "reservation rights", stars>=20: 0 hits).
- **Demo path:** Public sample ISO-style policy wording with synthetic claim facts.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

## Sources
- https://insurancefraud.org/wp-content/uploads/The-Impact-of-Insurance-Fraud-on-the-U.S.-Economy-Report-2022-8.26.2022.pdf (opened, text extracted)
- https://crr.rutgers.edu/wp-content/uploads/sites/22/Misinformation-About-Insurance-Fraud-11-2024.pdf (opened, text extracted)
- https://www.nationalsubrogation.com/author/pweilcozen-com/ (opened; claim unsupported)
- https://home.treasury.gov/system/files/311/TRIP02C-Instructions.pdf (not opened)
- https://climate.gov/news-features/blogs/beyond-data/2024-active-year-us-billion-dollar-weather-and-climate-disasters (not opened)
- https://www.fema.gov/openfema-data-page/fima-nfip-claims
- https://www.ncei.noaa.gov/stormevents/
- https://www.ncei.noaa.gov/access/billions/
- https://content.naic.org/consumer/data
- https://filingaccess.serff.com
