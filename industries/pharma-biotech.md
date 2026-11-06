# Pharma, Biotech & Life Sciences

## Overview
Drug and device developers spend most non-laboratory effort on documents and compliance: safety case processing, trial operations, regulatory dossiers and quality records. Work concentrates in pharmacovigilance, clinical operations, regulatory affairs and quality assurance, where every step must be traceable and validated. Fixed regulatory clocks (for example expedited safety reports) and very expensive failures (the FY2027 PDUFA application fee with clinical data is $4,600,753, confirmed on RAPS) make errors costly, so agents must keep humans in the approval loop.

Verification note (2026-11-06): only the figures tagged below were checked against pages. Regulation names and dates in this file (ICH, GVP, 21 CFR, EU CTR etc.) were not re-checked against official text and should be read as unconfirmed.

## Systems of record, regulations, public datasets
- **Systems:** safety database (Oracle Argus, ArisGlobal LifeSphere), CTMS (Veeva Vault CTMS), EDC (Medidata Rave, Veeva EDC), eTMF, RIM (Veeva Vault RIM), QMS (TrackWise, Veeva QMS), LIMS, MES/batch records, literature databases (PubMed, Embase), ClinicalTrials.gov.
- **Regulations / standards:** 21 CFR Part 11 (electronic records); 21 CFR Parts 211 and 312/314 (GMP, IND/NDA); ICH E2A/E2B(R3) (ICSRs), ICH E6(R3) GCP (2025), ICH M4 CTD/eCTD; EMA GVP Modules VI and VII; EU CTR 536/2014; EU GMP Annex 11; GAMP 5; FDA PDUFA user fee program; MedDRA coding.
- **Public datasets:** FAERS https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html ; openFDA https://open.fda.gov ; ClinicalTrials.gov API https://clinicaltrials.gov/data-api/api ; DailyMed labels https://dailymed.nlm.nih.gov ; PubMed E-utilities https://www.ncbi.nlm.nih.gov/books/NBK25497/ ; FDA inspection citations dataset https://datadashboard.fda.gov ; Synthea for patient-level data.

## Use cases

### 1. Pharmacovigilance adverse-event case intake and triage
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is a drug-safety department. Systems: safety database, MedDRA, source email/call-centre/literature, partner exchange. Regulated by ICH E2B(R3), GVP VI, 21 CFR 314.80/600.80, Part 11. Human gate: medical reviewer approves seriousness, causality and submission.
- **Problem and today's workflow:** Case processors read unstructured reports, code terms to MedDRA, search for duplicates, write narratives and prepare expedited reports under 15-day clocks.
- **Evidence:** FAERS table (opened): 2014 had 828,368 domestic and 375,347 foreign reports (about 1.2M); the table's last row is 2015 Q1, so it is dated. https://www.fda.gov/drugs/fda-adverse-event-monitoring-system-aems/faers-domestic-and-foreign-reports-year [Verified]
- **Agent design:** Tools: document extractor, MedDRA coder, duplicate search, narrative drafter, safety DB API. Steps: extract the four minimum criteria, code, de-duplicate, draft narrative, route. Seriousness is never downgraded by the agent; medical reviewer signs.
- **Open source today:** KarelDO/BioDEX (67 stars, MIT, not archived, last push 2024-01-29, README read: yes; adverse-drug-event extraction dataset and benchmark - adjacent only); jihyechoi77/malade (30 stars, no licence in API though README badge says MIT, not archived, last push 2025-02-19, README read: yes; multi-agent ADE extraction research code - adjacent, closest to the use case).
- **Demo path:** FAERS quarterly files; convert rows to synthetic free-text reports and score extraction and coding.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 2. Clinical-trial eligibility screening against free-text records
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer is a sponsor, CRO or academic medical centre. Systems: EHR, CTMS, ClinicalTrials.gov protocol criteria. Regulated by ICH E6 GCP, IRB/consent, HIPAA. Human gate: coordinator and PI confirm eligibility before any outreach.
- **Problem and today's workflow:** Coordinators read charts against long inclusion/exclusion lists to find candidates; slow recruitment delays trials.
- **Evidence:** The earlier cited study (PMC9857498, surgical RCTs registered on ClinicalTrials.gov 2010-2014, JAMA Netw Open 2023) could not be opened (PMC returned a captcha page; PubMed and a university listing did not show the results). Numbers removed. Reference, not confirmed: https://pmc.ncbi.nlm.nih.gov/articles/PMC9857498/ [Unconfirmed]
- **Agent design:** Tools: criteria parser, EHR query (structured and notes), terminology mapper, evidence cite-back. Steps: decompose criteria, evaluate per patient with evidence spans, rank, queue for review. Human approves candidates.
- **Open source today:** cbib/TrialMatchAI (41 stars, licence NOASSERTION, not archived, last push 2026-10-23, README read: yes; CLI for patient-to-trial retrieval and criterion-level eligibility review - addresses the use case); dfci/matchminer (54 stars, no licence listed, not archived, last push 2026-10-28, README read: yes; Dana-Farber trial-matching suite incl. MatchMiner-AI - addresses the use case, genomics-oriented).
- **Demo path:** ClinicalTrials.gov criteria text plus Synthea patients; measure per-criterion accuracy.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 3. Regulatory submission (eCTD) assembly and consistency check
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is a regulatory affairs department. Systems: RIM, document management (Veeva Vault), eCTD publishing tool, CSR/CMC source documents. Regulated by ICH M4, FDA eCTD requirements, PDUFA. Human gate: regulatory lead approves content and the publishing sign-off.
- **Problem and today's workflow:** Teams cross-check module 2 summaries against modules 3-5, verify numbers, hyperlinks and cross-references, and prepare responses to agency questions.
- **Evidence:** RAPS (opened): FY2027 PDUFA fee for applications requiring clinical data is $4,600,753, down 1.7% from $4,682,003 in FY2026. https://www.raps.org/resource/fda-unveils-fy-2027-user-fee-rates.html [Verified] Fee shows the stakes, not labour cost.
- **Agent design:** Tools: document retriever, table/number extractor, cross-reference checker, eCTD validator, question-response drafter. Steps: compare claims across modules, flag inconsistencies, draft agency responses with citations. Regulatory lead approves.
- **Open source today:** RConsortium/submissions-pilot1-to-fda (92 stars; description "eCTD package for pilot1 submission to FDA", README read: no; sample R submission package, adjacent only). No consistency-check agent found (gh search "ectd submission").
- **Demo path:** Public FDA approval packages on Drugs@FDA https://www.accessdata.fda.gov/scripts/cder/daf/ ; seed inconsistencies between summary and review sections.
- **Verification:** 2026-11-06, Verified, repos checked partly (stars/description only for pilot1)

### 4. Clinical trial site feasibility and selection
- **Tier:** B (scoring is analytic; agent gathers and reconciles evidence). Enterprise: needs figure
- **Enterprise check:** Buyer is a sponsor or CRO. Systems: CTMS, site performance history, ClinicalTrials.gov, investigator databases, feasibility questionnaires. Regulated by ICH E6 GCP site-qualification expectations; audit trail of selection rationale. Human gate: clinical operations lead approves the site list.
- **Problem and today's workflow:** Feasibility managers send questionnaires, collect answers by email, compare with past performance, and compile a ranked list.
- **Evidence:** no reliable figure found. [Unconfirmed]
- **Agent design:** Tools: ClinicalTrials.gov search, investigator history lookup, questionnaire parser, CTMS read, ranking sheet writer. Steps: build candidate list, extract site answers, reconcile with competing trials, propose ranking with reasons. Ops lead approves.
- **Open source today:** none found (gh search "clinical trial feasibility", stars>=20: 0 hits).
- **Demo path:** ClinicalTrials.gov API for site and competing-trial density by condition and region.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 5. GxP deviation investigation and CAPA drafting
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer is a manufacturer's quality unit. Systems: QMS, batch records (MES), LIMS, equipment logs, SOPs. Regulated by 21 CFR 211.192 and 211.100, EU GMP, Part 11. Human gate: QA approves root cause, impact assessment and CAPA closure.
- **Problem and today's workflow:** QA investigators collect batch, equipment and training records, find similar past deviations, run root-cause analysis and write reports within site timelines.
- **Evidence:** no reliable figure found for deviation volume. FDA inspection data page not opened; reference, not confirmed: https://datadashboard.fda.gov [Unconfirmed]
- **Agent design:** Tools: QMS search, MES/LIMS reads, SOP retriever, similarity search, report drafter. Steps: assemble timeline, retrieve precedent, propose root-cause hypotheses with evidence, draft CAPA. QA owns conclusions.
- **Open source today:** none found (gh search "GxP deviation", stars>=20: 0 hits).
- **Demo path:** Synthetic deviation records modelled on public FDA Form 483 / warning letter text https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters .
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 6. Safety literature surveillance
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer is a marketing authorisation holder. Systems: PubMed/Embase, safety database, literature tracking tool. Regulated by GVP Module VI (literature screening) and ICH E2D. Human gate: PV scientist confirms every potential ICSR and its validity.
- **Problem and today's workflow:** Scientists run saved searches weekly, read abstracts and full texts, identify case reports, and log screening decisions for audit.
- **Evidence:** no reliable figure found. [Unconfirmed]
- **Agent design:** Tools: PubMed search, full-text fetch, case-criteria checker, dedup against database, screening log. Steps: screen, extract minimum case data, draft ICSR intake, record rationale. Scientist decides.
- **Open source today:** none found (gh search "pharmacovigilance literature", stars>=20: only a generic literature-search CLI, pryndor/Lixplore_cli, 33 stars, description-only, not relevant to ICSR screening).
- **Demo path:** PubMed queries for a marketed drug name plus adverse-event terms; compare to scientist labels.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 7. Clinical protocol authoring and amendment impact analysis
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is a sponsor. Systems: protocol repository, CTMS, EDC build specs, informed consent forms, registry entries. Regulated by ICH E6/E8, 21 CFR 312.30, EU CTR. Human gate: medical monitor and regulatory sign-off.
- **Problem and today's workflow:** A protocol change must be traced to the schedule of assessments, ICF, EDC forms, site contracts and registry records, mostly manually.
- **Evidence:** Tufts CSDD via PharmaVoice (opened, 2016): median direct cost of a substantial amendment $141,000 (Phase II) and $535,000 (Phase III). Corrected: the page says sponsors implement at least one substantial global amendment for "almost 60%" of protocols, not 57%. https://www.pharmavoice.com/news/2016-03-clinical-trial-amendments/613018/ [Corrected]
- **Agent design:** Tools: document diff, cross-document retriever, EDC spec reader, ICF drafter. Steps: identify changed sections, list downstream artefacts affected, draft redlines. Medical monitor and regulatory approve.
- **Open source today:** none found (gh search "protocol amendment", stars>=20: only unrelated terms-of-service hits).
- **Demo path:** Public protocols posted on ClinicalTrials.gov (document attachments); create synthetic amendments.
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 8. Clinical data review and query management
- **Tier:** B. Enterprise: needs figure
- **Enterprise check:** Buyer is a sponsor or CRO data management group. Systems: EDC, data listings, lab feeds, medical coding. Regulated by ICH E6, 21 CFR Part 11, CDISC SDTM. Human gate: data manager approves query issuance and data lock.
- **Problem and today's workflow:** Data managers run edit checks, review listings, and write queries to sites that must be tracked to closure.
- **Evidence:** no reliable figure found. [Unconfirmed]
- **Agent design:** Tools: EDC API, listing generator, protocol retriever, query drafter. Steps: detect inconsistencies, draft site queries with cited protocol rules, track answers. Data manager approves queries.
- **Open source today:** none found (gh search "clinical data query", stars>=20: only OHDSI/UMLS utilities, not query management).
- **Demo path:** CDISC pilot SDTM dataset https://github.com/cdisc-org/sdtm-adam-pilot-project with injected errors.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 9. Promotional material medical-legal-regulatory (MLR) review
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer is a commercial / medical affairs department. Systems: promo review system (Veeva PromoMats), approved label, reference library. Regulated by FDA 21 CFR 202.1, OPDP Form 2253 submission, PhRMA code. Human gate: medical, legal and regulatory reviewers approve.
- **Problem and today's workflow:** Reviewers check every claim against the label and cited references, then annotate rounds of comments.
- **Evidence:** no reliable figure found. [Unconfirmed]
- **Agent design:** Tools: claim extractor, label and reference retriever, fair-balance checker, annotation writer. Steps: match claims to support, flag unsupported or off-label statements, propose edits. Reviewers decide.
- **Open source today:** none found (gh search "promotional review MLR", stars>=20: 0 hits).
- **Demo path:** DailyMed labels as the approved basis; synthetic marketing copy with seeded errors.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 10. Global regulatory change control and label variation tracking
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer is a regulatory/CMC group. Systems: RIM registrations, change control in QMS, country requirement databases. Regulated by EU variation regulation 1234/2008, FDA CBE/PAS rules, ICH Q12. Human gate: regulatory affairs approves strategy and filings.
- **Problem and today's workflow:** Each manufacturing or label change must be assessed per country, classified, and tracked to approval and implementation across markets.
- **Evidence:** no reliable figure found. [Unconfirmed]
- **Agent design:** Tools: RIM read, change-control read, regulation retriever, impact matrix writer. Steps: classify change per market, list required filings, draft filing plan. Regulatory approves.
- **Open source today:** none found (gh search "regulatory affairs variation", stars>=20: 0 hits).
- **Demo path:** Synthetic product registrations plus public EU variation classification guideline text.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

## Sources
- https://www.fda.gov/drugs/fda-adverse-event-monitoring-system-aems/faers-domestic-and-foreign-reports-year (opened)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC9857498/ (reference, not confirmed)
- https://www.raps.org/resource/fda-unveils-fy-2027-user-fee-rates.html (opened)
- https://www.pharmavoice.com/news/2016-03-clinical-trial-amendments/613018/ (opened)
- https://datadashboard.fda.gov (reference, not opened)
- https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html
- https://open.fda.gov
- https://clinicaltrials.gov/data-api/api
- https://dailymed.nlm.nih.gov
- https://www.ncbi.nlm.nih.gov/books/NBK25497/
- https://www.accessdata.fda.gov/scripts/cder/daf/
- https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters
- https://github.com/cdisc-org/sdtm-adam-pilot-project
