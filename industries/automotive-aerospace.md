# Automotive & Aerospace

## Overview
OEMs, suppliers and MRO shops spend effort on field quality, certification evidence, supplier quality gates and maintenance-record integrity. Manual work concentrates where regulated documents must be cross-checked against standards and history: warranty and recall analysis, airworthiness records, nonconformance dispositions, type-approval dossiers and PPAP packages. Errors carry regulator action (recalls, certificate revocation), so every use case ends with a qualified human signature.

## Systems of record, regulations, public datasets
- Systems: PLM (Teamcenter, Windchill, CATIA), ERP (SAP), warranty/claims systems, QMS, MRO/CAMO software (AMOS, TRAX, Ramco), dealer DMS, requirements tools (DOORS, Polarion), supplier portals (Covisint-style, OEM portals).
- Regulations/standards: AS9100D (IAQG, 2016); AS9102 FAI; AS5553 counterfeit parts; IATF 16949:2016; AIAG PPAP 4th ed.; 49 CFR Part 573 (defect reports) and TREAD Act early warning reporting (49 CFR 579); 14 CFR Parts 43, 91.417, 145 (records, repair stations); EASA Part-145/CAMO; EU Regulation 2018/858 (type approval); UN Regulations R155 (cyber) and R156 (software updates); RTCA DO-178C (2011) and DO-254.
- Public datasets: NHTSA complaints/recalls/investigations https://www.nhtsa.gov/nhtsa-datasets-and-apis ; NHTSA recalls API https://api.nhtsa.gov ; FAA Service Difficulty Reports https://av-info.faa.gov/sdrx/ ; FAA Dynamic Regulatory System (ADs) https://drs.faa.gov ; EASA ADs https://ad.easa.europa.eu ; Federal Register API https://www.federalregister.gov/developers/documentation/api/v1 ; NTSB CAROL https://data.ntsb.gov/carol-main-public/basic-search ; NASA C-MAPSS turbofan data via https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/ .

## Use cases

### 1. Warranty claim analysis, fraud screening and supplier recovery
- **Tier:** A | Enterprise: pass
- **Enterprise check:** Buyer: OEM/tier-1 warranty and quality org. Systems: dealer claims system, DMS repair orders, ERP/supplier contracts, PLM. Regulation/audit: contractual warranty terms, SOX accruals, EWR input. Human gate: warranty administrator approves denials and supplier chargebacks.
- **Problem and today's workflow:** Analysts read technician comments, match claims to part/lot, detect abuse, and compile supplier recovery packages manually.
- **Evidence:** Warranty Week: "Ford, General Motors, and Tesla spent a collective $10 billion in warranty claims during 2023" (Ford $4.78B, GM $4.01B, Tesla $1.23B). The earlier figures (about $10.5B for all US car and cycle makers, about $51B global) are not on the page and were removed. https://www.warrantyweek.com/archive/ww20240208.html [Corrected]
- **Agent design:** Tools: claims DB, repair-order text, part genealogy, contract terms lookup. Steps: cluster failure narratives, link to supplier lots, test claim validity, draft recovery packet. Administrator approves.
- **Open source today:** none found (gh search repos "warranty claims analysis", stars>=20, not archived: no hits).
- **Demo path:** NHTSA consumer complaints as free-text proxy plus synthetic claims table.
- **Verification:** 2026-11-06, Corrected, repos checked: none listed, search run

### 2. Recall root-cause investigation and Part 573 report drafting
- **Tier:** A | Enterprise: pass
- **Enterprise check:** Buyer: OEM product safety office. Systems: warranty, NHTSA complaints, field-data, PLM, supplier quality. Regulation: 49 CFR Part 573 (report within 5 working days of defect determination), 49 CFR 579. Human gate: safety committee decides recall and signs filing.
- **Problem and today's workflow:** Engineers assemble complaints, warranty trends and test data, draft the defect chronology and population by hand under deadline.
- **Evidence:** NHTSA 2023: "There were 894 vehicle recalls affecting 34,862,036 vehicles in 2023." https://www.repairerdrivennews.com/2024/03/06/nhtsa-about-4m-more-vehicles-recalled-last-year/ (trade report of NHTSA data; NHTSA annual report not opened). 49 CFR 573.6 text opened: report due "not more than 5 working days" after the defect determination (working days, not business days). https://www.law.cornell.edu/cfr/text/49/573.6 [Verified]
- **Agent design:** Tools: NHTSA complaint/investigation search, warranty and VIN-build queries, population calculator, report template. Steps: detect signal, correlate to build dates/suppliers, draft chronology and population, list evidence gaps. Committee and legal approve.
- **Open source today:** none found (gh search repos "NHTSA recall complaints", stars>=20, not archived: no hits).
- **Demo path:** NHTSA complaints and recall flat files; replay a historical recall.
- **Verification:** 2026-11-06, Verified, repos checked: none listed, search run

### 3. Aircraft maintenance records (MRO) compliance review
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: airline, lessor, repair station. Systems: MRO/CAMO software, scanned logbooks, parts stores, FAA/EASA AD databases. Regulation: 14 CFR 43.9, 145.219; EASA Part-M/CAMO. Human gate: licensed inspector/certifying staff signs release.
- **Problem and today's workflow:** Records reviewers read scanned logbooks and work packages to confirm AD/life-limited-part compliance and spot gaps before delivery or return-to-service.
- **Evidence:** No reliable aggregate figure found. The earlier claim of an FAA emergency revocation of a Part 145 certificate in Feb 2026 could not be confirmed and was removed; 14 CFR 145.12 could not be confirmed as a falsification rule and was dropped from the regulation list. Reference, not confirmed: https://www.faa.gov/media/12486 . 14 CFR 145.219 (records) is cited from Cornell LII, text not re-read. [Unconfirmed]
- **Agent design:** Tools: OCR, MRO system, AD database, parts back-to-birth. Steps: extract entries, build compliance matrix, flag missing signatures or gaps, draft discrepancy list. Certifying staff decide.
- **Open source today:** PalestyHR/AMRA (0 stars, no licence, not archived, last push 2026-10-31; README read: yes) - README describes an AI-driven assistant that screens maintenance records with source quotations, local checks and human review; addresses the screening step, demo-stage. Second: none found.
- **Demo path:** FAA SDR data and synthetic scanned logbook pages.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 4. AS9100 nonconformance and MRB disposition support
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: aerospace manufacturer/supplier quality. Systems: QMS NCR, ERP, PLM drawings, FAI records. Regulation: AS9100D s.8.7; customer flow-downs. Human gate: Material Review Board (engineering, quality, customer rep) signs disposition.
- **Problem and today's workflow:** Quality engineers pull drawings, measurements and past similar NCRs to propose use-as-is/repair/scrap, and check customer approval needs.
- **Evidence:** no reliable figure found. [Unconfirmed]
- **Agent design:** Tools: NCR, CMM data, drawing tolerance lookup, prior-NCR search. Steps: quantify deviation, find precedent dispositions, check approval thresholds, draft MRB package. MRB decides.
- **Open source today:** none found (gh search repos "nonconformance NCR", stars>=20, not archived: no hits).
- **Demo path:** Synthetic NCRs and inspection tables.
- **Verification:** 2026-11-06, Unconfirmed, repos checked: none listed, search run

### 5. Type-approval and homologation dossier assembly (EU 2018/858, UNECE)
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: OEM homologation team. Systems: PLM, test-lab reports, requirements tools, approval-authority portals. Regulation: Reg. (EU) 2018/858; UNECE regulations. Human gate: homologation manager submits to technical service.
- **Problem and today's workflow:** Staff map each regulation clause to test evidence and variant data for every market and update dossiers when rules change.
- **Evidence:** no reliable figure found (a vendor claim of "60+ countries" for UN R155/R156 could not be confirmed and is not used; Reg. (EU) 2018/858 text not re-opened). [Unconfirmed]
- **Agent design:** Tools: regulation text search, test-report parser, variant matrix, document generator. Steps: track amendments, map clauses to evidence, list gaps, draft information document. Manager approves.
- **Open source today:** none found (gh search repos "type approval homologation", stars>=20, not archived: no hits).
- **Demo path:** UNECE regulation texts plus synthetic test reports.
- **Verification:** 2026-11-06, Unconfirmed, repos checked: none listed, search run

### 6. Supplier PPAP package review
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: OEM/tier-1 supplier quality. Systems: supplier portal, QMS, PLM, ERP. Standard: AIAG PPAP 4th ed., IATF 16949. Human gate: SQE approves/rejects PSW.
- **Problem and today's workflow:** SQEs check 18 PPAP elements (control plans, PFMEA, MSA, capability) for consistency and completeness, then chase fixes.
- **Evidence:** no reliable figure found. [Unconfirmed]
- **Agent design:** Tools: portal documents, drawing read, Cpk calculation, PFMEA/control-plan cross-check. Steps: completeness check, consistency check, recompute capability, draft deficiency letter. SQE decides.
- **Open source today:** No PPAP review agent found. Adjacent only: jherrodthomas/automotive-skills-suite (3,334 stars, MIT, last push 2026-10-16; README read: yes - 152 Claude skills incl. AIAG-VDA quality and IATF 16949 knowledge, not a package-review workflow); RBraga01/Quality-Engineering-Skills (43 stars, MIT, last push 2026-10-30; README read: yes - 23 quality skills incl. PPAP, skill prompts not an agent over supplier portals).
- **Demo path:** Synthetic PPAP packages with seeded inconsistencies.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 7. Airworthiness directive and service bulletin applicability
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: airline/operator engineering. Systems: fleet configuration database, MRO planning, FAA/EASA AD feeds, OEM service bulletins. Regulation: 14 CFR Part 39. Human gate: continuing-airworthiness engineer approves applicability and compliance plan.
- **Problem and today's workflow:** Engineers read each new AD, match serial/part effectivity to the as-built fleet configuration and schedule work.
- **Evidence:** no reliable figure found. [Unconfirmed]
- **Agent design:** Tools: Federal Register/DRS/EASA feed, configuration DB, task-card generator. Steps: parse effectivity, match to aircraft, propose compliance method and due date, draft work packages. Engineer approves.
- **Open source today:** none found (gh search repos "airworthiness directive", stars>=20, not archived: no hits).
- **Demo path:** Federal Register AD documents plus synthetic fleet configuration.
- **Verification:** 2026-11-06, Unconfirmed, repos checked: none listed, search run

### 8. First Article Inspection (AS9102) review
- **Tier:** B | Enterprise: needs figure
- **Enterprise check:** Buyer: aerospace supplier and prime. Systems: PLM/ballooned drawings, CMM, QMS. Standard: AS9102. Human gate: quality engineer signs FAI forms.
- **Problem and today's workflow:** Inspectors balloon drawings and transcribe measurements into Forms 1-3, then reviewers check completeness.
- **Evidence:** no reliable figure found. [Unconfirmed]
- **Agent design:** Tools: drawing parser, CMM data import, form generator. Steps: extract characteristics, match measurements, flag out-of-tolerance or missing items. Engineer signs.
- **Open source today:** none found (gh search repos "first article inspection", stars>=20, not archived: no hits).
- **Demo path:** Public sample drawings plus synthetic CMM export.
- **Verification:** 2026-11-06, Unconfirmed, repos checked: none listed, search run

### 9. Parts traceability and suspect-unapproved-parts screening
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: MRO, airline, distributor. Systems: stores/ERP, supplier certs, MRO system. Regulation: 14 CFR 21/43, AS5553. Human gate: receiving inspector/quality releases part.
- **Problem and today's workflow:** Staff check 8130-3/EASA Form 1 certificates, back-to-birth trace and supplier status by hand.
- **Evidence:** no reliable figure found. [Unconfirmed]
- **Agent design:** Tools: certificate OCR, supplier approval list, trace-history query. Steps: validate certificate fields, trace chain, flag anomalies. Quality decides quarantine.
- **Open source today:** none found (gh search repos "counterfeit parts traceability", stars>=20, not archived: no hits).
- **Demo path:** Synthetic certificates with seeded forgeries.
- **Verification:** 2026-11-06, Unconfirmed, repos checked: none listed, search run

### 10. Software certification evidence review (DO-178C traceability)
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: avionics developer. Systems: DOORS/Polarion, code repo, test tools, configuration management. Standard: DO-178C. Human gate: software quality assurance and DER/designee sign.
- **Problem and today's workflow:** Engineers cross-check requirement-to-code-to-test trace links and coverage evidence manually before audits.
- **Evidence:** no reliable figure found. [Unconfirmed]
- **Agent design:** Tools: requirements export, repo query, coverage reports. Steps: build trace matrix, find orphan requirements, draft discrepancy list. SQA approves.
- **Open source today:** none found (gh search repos "DO-178C traceability", stars>=20, not archived: no hits).
- **Demo path:** Open-source flight software requirements with synthetic test links.
- **Verification:** 2026-11-06, Unconfirmed, repos checked: none listed, search run

## Sources
- https://www.warrantyweek.com/archive/ww20240208.html
- https://www.repairerdrivennews.com/2024/03/06/nhtsa-about-4m-more-vehicles-recalled-last-year/
- https://www.faa.gov/media/12486
- https://www.law.cornell.edu/cfr/text/14/145.219
- Dataset links listed in section 2.
