# Healthcare Providers & Payers

## Overview
Hospitals, physician groups and health plans spend a large share of staff time on administrative work that sits between the clinical record and the payment: prior authorization, coding, claims denials, credentialing, quality reporting and directory upkeep. The work is manual because it needs unstructured clinical text, payer-specific rules and portal or fax submission, and each step has regulatory clocks. Manual effort concentrates in revenue cycle, utilization management and quality/compliance teams. CAQH 2023 Index (opened, PDF): medical-industry administrative spend $82.7B and $16.4B of savings available from full electronic processing [Verified, https://www.caqh.org/hubfs/drupal/2024-01/CAQH_IndexReport_2023_FINAL.pdf].

Verification note (2026-11-06): only CMS-0057-F was confirmed against the official CMS fact sheet. Other regulation names and dates below were not re-checked against official text and should be read as unconfirmed.

## Systems of record, regulations, public datasets
- **Systems:** EHR (Epic, Oracle Health, MEDITECH), practice management / revenue cycle (Epic Resolute, athenahealth), clearinghouse (EDI 837/835/278), payer core admin (Facets, QNXT), utilization management platform, credentialing database (CAQH ProView), pharmacy system, data warehouse, document repository, payer and state portals.
- **Regulations / standards:** HIPAA Privacy, Security and Transactions rules (45 CFR 160/164); CMS Interoperability and Prior Authorization Final Rule CMS-0057-F (2024; 72-hour/7-day decisions from 2026, FHIR APIs by 1 Jan 2027 - confirmed on CMS fact sheet); No Surprises Act provider directory provisions (2020/2021); Medicare Advantage rules at 42 CFR Part 422; False Claims Act; NCQA HEDIS and credentialing standards; HL7 FHIR R4 and Da Vinci implementation guides (CRD, DTR, PAS); ICD-10-CM/PCS, CPT, HCPCS code sets.
- **Public datasets:** Synthea synthetic patients https://synthetichealth.github.io/synthea/ ; MIMIC-IV (credentialed) https://physionet.org/content/mimiciv/ ; CMS DE-SynPUF synthetic Medicare claims https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-claims-synthetic-public-use-files ; NPPES NPI registry https://download.cms.gov/nppes/NPI_Files.html ; CMS Medicare coverage database (LCD/NCD) https://www.cms.gov/medicare-coverage-database ; HAPI FHIR public test server https://hapi.fhir.org .

## Use cases

### 1. Provider-side prior-authorization packet assembly and submission
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is a health system or physician group. Systems: EHR (FHIR reads), payer portals / X12 278, payer policy documents. Regulated by HIPAA and CMS-0057-F; PHI audit trail. Human gate: nurse or clinician reviews the packet before submission.
- **Problem and today's workflow:** PA coordinators look up each payer's policy, pull notes, imaging and labs from the chart, fill payer-specific forms or portals, then chase status by phone or fax and handle appeals.
- **Evidence:** AMA survey of 1,000 physicians (late 2024): "39 prior authorization requests per physician, per week", 13 hours of physician and staff time weekly, 40% of physicians have staff working exclusively on PA. https://www.ama-assn.org/practice-management/prior-authorization/fixing-prior-auth-40-plus-prior-authorizations-week-way-too [Verified]
- **Agent design:** Tools: FHIR/EHR reader, payer-policy retriever, form/portal filler, status poller. Steps: determine whether PA is required, map criteria to chart evidence with citations, assemble packet, submit after sign-off, poll and escalate denials. Human approves every submission and any peer-to-peer.
- **Open source today:** HL7-DaVinci/prior-auth (37 stars, Apache-2.0, not archived, last push 2026-07-22, README read: yes; Da Vinci PAS reference implementation, standards plumbing - adjacent only); Azure-Samples/autoauth-solution-accelerator (20 stars, MIT, not archived, last push 2026-11-03, README read: yes (start only); Azure prior-authorization accelerator, closest match but a deployment sample, not a production agent).
- **Demo path:** Synthea patients on the HAPI FHIR server, a handful of synthetic payer policy PDFs, and a mock portal; score evidence-to-criterion mapping.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 2. Hospital claim-denial analysis and appeal drafting
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is a hospital revenue-cycle department. Systems: EHR, patient accounting, 835 remittance data, payer contracts and policies. Regulated by HIPAA and False Claims Act exposure; appeal deadlines. Human gate: coder or physician advisor signs each appeal.
- **Problem and today's workflow:** Staff read denial codes, pull the documentation and contract language, and write appeal letters per claim, tracking deadlines in spreadsheets.
- **Evidence:** Premier survey of 516 hospitals in 36 states: "nearly 15 percent of all claims submitted to private payers ... are initially denied"; MA appeals cost $47.77 per claim in admin cost; 52.7% of MA denials were eventually overturned. Corrected: the earlier "$19.7B per year" and "50-60% of appealed denials overturned" were not on the page (the 52.7% is for MA claims only). https://www.hcinnovationgroup.com/population-health-management/payers-providers/news/53099677/premier-survey-15-percent-of-claims-to-private-payers-are-initially-denied [Corrected]
- **Agent design:** Tools: 835/CARC-RARC parser, chart retriever, contract/policy search, letter generator, work-queue API. Steps: classify denial, decide appealable, assemble evidence, draft letter citing only chart facts, track outcome. Human approves every letter.
- **Open source today:** none found (gh search "claim denial appeal", stars>=20, not archived: 0 hits, 2026-11-06).
- **Demo path:** CMS DE-SynPUF claims with synthetic denial codes injected, plus Synthea notes as the evidence base.
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 3. Discharge medication reconciliation
- **Tier:** B (matching and interaction checks are largely rules; agent gathers and explains). Enterprise: pass
- **Enterprise check:** Buyer is a hospital pharmacy / quality department. Systems: EHR medication orders, pharmacy fill history (Surescripts), interaction database. Regulated by Joint Commission NPSG.03.06.01 and FDA clinical decision support boundary (not re-checked); audit of discrepancies. Human gate: pharmacist resolves each flagged discrepancy.
- **Problem and today's workflow:** Pharmacists and nurses compare home meds, inpatient orders, fill history and discharge instructions across screens, often under time pressure.
- **Evidence:** Leapfrog 2026 fact sheet (PDF text extracted locally): "Medication discrepancies occur in up to 70% of patients". https://ratings.leapfroggroup.org/sites/default/files/2026-04/2026%20Med%20Rec%20Fact%20Sheet.pdf [Verified]
- **Agent design:** Tools: EHR med list reader, fill-history API, RxNorm normaliser, interaction checker. Steps: normalise lists, diff, classify intentional vs unintentional, draft pharmacist worklist with evidence. Pharmacist decides; agent never edits orders.
- **Open source today:** jherskovic/MedRec (30 stars, no licence, not archived, last push 2014-03-18, README read: yes; a two-list RxNorm reconciliation algorithm, dated - adjacent only).
- **Demo path:** MIMIC-IV prescriptions and admission/discharge tables; seed known discrepancies.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 4. Payer utilization-management case review assist
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer is a health plan or UM vendor. Systems: UM platform, claims/eligibility core admin, medical policy library, provider portal. Regulated by CMS-0057-F (72-hour expedited and 7-day standard decisions), state laws, URAC/NCQA UM standards. Human gate: licensed clinician makes every denial; agent only recommends approval or routing.
- **Problem and today's workflow:** Nurse reviewers read submitted records against InterQual/MCG or plan policy, check eligibility and history, and write determination rationale under SLA clocks.
- **Evidence:** CMS fact sheet: payers must "send prior authorization decisions within 72 hours for expedited" requests and seven calendar days for standard; from 2026 payers must give a specific denial reason; Prior Authorization API from 1 Jan 2027. https://www.cms.gov/newsroom/fact-sheets/cms-interoperability-prior-authorization-final-rule-cms-0057-f [Verified] (regulatory clock, not a volume or dollar figure)
- **Agent design:** Tools: record ingester, criteria/policy retriever, eligibility lookup, rationale drafter, SLA clock monitor. Steps: extract clinical facts, match to criteria with citations, propose approve-or-route-to-physician, draft letter. No autonomous denials; clinician signs.
- **Open source today:** none found (gh search "prior authorization agent", stars>=20: 0 hits; HL7 Da Vinci RI listed under use case 1 is adjacent).
- **Demo path:** Synthea records plus public CMS LCD/NCD criteria as the policy; evaluate criterion citation accuracy.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 5. Coding and clinical documentation integrity (CDI) audit
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer is hospital HIM / compliance. Systems: EHR notes, encoder/grouper (3M, Optum), claims scrubber. Regulated by ICD-10 guidelines, CMS DRG payment rules and False Claims Act (upcoding exposure). Human gate: certified coder accepts or rejects each suggestion and physician query.
- **Problem and today's workflow:** Coders and CDI specialists read entire charts to assign codes, spot missing specificity, and send physician queries; pre-bill audits sample only a fraction of charts.
- **Evidence:** no reliable figure found (vendor claims only; not cited). [Unconfirmed]
- **Agent design:** Tools: note retriever, code-set lookup, grouper API, query-template generator. Steps: propose codes with note-span evidence, flag documentation gaps, draft compliant (non-leading) physician queries, record accept/reject. Coder is final.
- **Open source today:** none found (gh search "icd-10 coding llm", stars>=20: 0 hits).
- **Demo path:** MIMIC-IV discharge notes with ICD codes as ground truth (credentialed access).
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 6. Provider credentialing and payer enrollment
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer is a health system medical staff office or health plan credentialing unit. Systems: CAQH ProView, NPPES, state license boards, OIG LEIE exclusion list, NPDB, payer enrollment portals. Regulated by NCQA credentialing standards, Joint Commission medical staff standards, CMS enrollment rules. Human gate: credentialing committee approves.
- **Problem and today's workflow:** Staff perform primary-source verification of licenses, board certifications, sanctions and work history across dozens of sites, then re-key data into payer enrollment forms.
- **Evidence:** no reliable figure found. [Unconfirmed]
- **Agent design:** Tools: license-board lookups, LEIE/SAM checks, CAQH reader, document extractor, enrollment form filler. Steps: verify each element, flag discrepancies, assemble file, track expirations. Committee decides; agent never grants privileges.
- **Open source today:** none found (gh search "provider credentialing", stars>=20: 0 hits).
- **Demo path:** NPPES file plus OIG LEIE downloadable list https://oig.hhs.gov/exclusions/exclusions_list.asp with synthetic applicant files.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 7. Provider directory validation
- **Tier:** B (verification rules; agent runs outreach and reconciliation). Enterprise: needs figure
- **Enterprise check:** Buyer is a health plan. Systems: provider data management system, claims data, NPPES, practice websites, outreach channels. Regulated by No Surprises Act directory accuracy and 90-day verification rules (not re-checked), state laws, MA network adequacy. Human gate: data steward approves record changes.
- **Problem and today's workflow:** Plans mail or call providers to confirm addresses, panels and phone numbers and reconcile conflicting sources.
- **Evidence:** The earlier recalled CMS finding about MA directory inaccuracy could not be located or opened; number removed. [Unconfirmed]
- **Agent design:** Tools: NPPES/claims comparison, web lookup, email/fax outreach, directory update API. Steps: score staleness, gather evidence, contact practice, propose updates. Steward approves writes.
- **Open source today:** none found (gh search "provider directory", stars>=20: only unrelated Active Directory / awesome-list hits).
- **Demo path:** NPPES records perturbed with synthetic moves and closures.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 8. HEDIS / quality measure chart abstraction and gap closure
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer is a health plan or provider group. Systems: claims warehouse, EHR/HIE feeds, supplemental data, NCQA-certified measure engine. Regulated by NCQA HEDIS audit (NCQA-certified auditor), CMS Star Ratings. Human gate: abstractor / auditor validates each numerator hit.
- **Problem and today's workflow:** Nurses retrieve charts from provider offices during the annual hybrid-measure season and abstract results by hand for unresolved care gaps.
- **Evidence:** no reliable figure found. [Unconfirmed]
- **Agent design:** Tools: gap-list reader, chart retriever, document extractor, measure-spec checker. Steps: find evidence of screenings or results, cite page, submit for abstractor sign-off, keep audit trail. Human validates.
- **Open source today:** cqframework/hedis-ig (30 stars, no licence, not archived, last push 2019-12-27, README read: yes; HEDIS FHIR implementation guide source, adjacent only). No chart-abstraction agent found.
- **Demo path:** Synthea clinical records with a simplified HEDIS-style measure (e.g. HbA1c testing).
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 9. Claims payment integrity and pre-payment review
- **Tier:** B (edits and models detect; agent assembles the review file). Enterprise: needs figure
- **Enterprise check:** Buyer is a payer's payment integrity unit. Systems: claims adjudication system, code edit engine, medical records, provider contracts. Regulated by CMS NCCI edits, state prompt-pay laws, False Claims Act. Human gate: clinical coder / auditor approves adjustments and recoupments.
- **Problem and today's workflow:** Auditors review flagged claims, request records, compare to contract and coding rules, and write findings to providers.
- **Evidence:** CAQH 2023 Index (opened PDF) shows $16.4B medical-industry savings from full electronic transactions (not a direct payment-integrity figure). Corrected: the earlier cited HCI article is about the 2022 Index ($25B total, $22.3B medical), a different edition. https://www.caqh.org/hubfs/drupal/2024-01/CAQH_IndexReport_2023_FINAL.pdf [Corrected] Direct payment-integrity figure: no reliable figure found.
- **Agent design:** Tools: claims query, edit/contract lookup, records request, finding writer. Steps: triage flagged claims, gather records, check rules, draft finding. Auditor signs adjustments.
- **Open source today:** none found (gh search "payment integrity claims", stars>=20: 0 hits).
- **Demo path:** DE-SynPUF claims with synthetic duplicate billing and unbundling patterns.
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 10. Medicare Advantage appeals and grievances case handling
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer is an MA plan. Systems: appeals/grievance case management, claims, UM records, member correspondence. Regulated by 42 CFR Part 422 Subpart M timelines, CMS audit protocols. Human gate: medical director or appeals specialist decides and signs the letter.
- **Problem and today's workflow:** Appeals staff gather the case file, check timeliness and jurisdiction, re-review against policy, and draft decision letters with required language.
- **Evidence:** no reliable figure found. [Unconfirmed]
- **Agent design:** Tools: case system API, claims/UM lookup, policy retriever, letter template engine, deadline tracker. Steps: classify case, build chronology, check clocks, draft determination for review. Human decides and signs.
- **Open source today:** none found (gh search "medicare advantage", stars>=20: 0 hits).
- **Demo path:** Synthetic appeal cases built from public CMS LCD policies and Synthea data.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

## Sources
- https://www.ama-assn.org/practice-management/prior-authorization/fixing-prior-auth-40-plus-prior-authorizations-week-way-too (opened)
- https://www.hcinnovationgroup.com/population-health-management/payers-providers/news/53099677/premier-survey-15-percent-of-claims-to-private-payers-are-initially-denied (opened)
- https://ratings.leapfroggroup.org/sites/default/files/2026-04/2026%20Med%20Rec%20Fact%20Sheet.pdf (opened, text extracted)
- https://www.cms.gov/newsroom/fact-sheets/cms-interoperability-prior-authorization-final-rule-cms-0057-f (opened)
- https://www.caqh.org/hubfs/drupal/2024-01/CAQH_IndexReport_2023_FINAL.pdf (opened, text extracted)
- https://www.hcinnovationgroup.com/finance-revenue-cycle/news/21294207/caqh-automating-more-transactions-could-save-25-billion (opened; 2022 Index)
- https://synthetichealth.github.io/synthea/
- https://physionet.org/content/mimiciv/
- https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-claims-synthetic-public-use-files
- https://download.cms.gov/nppes/NPI_Files.html
- https://www.cms.gov/medicare-coverage-database
- https://hapi.fhir.org
- https://oig.hhs.gov/exclusions/exclusions_list.asp
