# Manufacturing & Industrial

## Overview
Plants spend effort on uptime, quality records, supplier management, product-compliance paperwork and safety/environmental reporting. Manual work concentrates where one engineer must join evidence from many systems (CMMS, QMS, ERP, PLM, historian) and write a signed record: CAPA files, supplier corrective actions, change-impact reviews, material declarations and regulatory filings. Most of these end in a human signature, which is why agents (retrieve, cross-check, draft, route for approval) fit better than a single model call.

## Systems of record, regulations, public datasets
- Systems: ERP (SAP, Oracle, Infor), MES, CMMS/EAM (Maximo, SAP PM), historian/SCADA (OSIsoft PI, Ignition), QMS (MasterControl, ETQ, Veeva), PLM (Teamcenter, Windchill), supplier portals, customs/GTS systems.
- Regulations/standards: ISO 9001:2015; ISO 13485:2016; 21 CFR Part 820 (QMSR, effective Feb 2026); 21 CFR Part 11; OSHA 29 CFR 1910.147 (lockout/tagout) and 1910.119 (PSM); ISO 12100:2010; EU CBAM Regulation (EU) 2023/956; EU REACH (1907/2006) and RoHS Directive 2011/65/EU; Waste Framework Directive (EU) 2018/851 (SCIP); EPCRA s.313 / 40 CFR 372 (TRI); 19 U.S.C. 1592 (customs penalties).
- Public datasets: NASA PCoE prognostics repository https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/ ; FDA warning letters https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters ; USITC HTS https://hts.usitc.gov ; CBP CROSS rulings https://rulings.cbp.gov ; ECHA Candidate List https://echa.europa.eu/candidate-list-table ; EPA TRI basic data files https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-data-files-calendar-years-1987-present ; OSHA enforcement data https://enforcedata.dol.gov .

## Use cases

### 1. Maintenance troubleshooting and work-order drafting from manuals, CMMS history and sensor data
- **Tier:** A | Enterprise: pass
- **Enterprise check:** Buyer: plant operations / reliability. Systems: CMMS (Maximo), historian, OEM manuals, ERP spare-parts stock. Regulation/audit: LOTO (1910.147), ISO 12100; every recommendation logged. Human gate: maintenance planner approves the work order; agent never actuates equipment.
- **Problem and today's workflow:** When a line stops, technicians search PDF manuals, old work orders and trends by hand, then request parts. Knowledge leaves with retiring technicians.
- **Evidence:** Siemens True Cost of Downtime 2024, via AEMT summary page: the 500 biggest companies "lose approximately $1.4 trillion annually due to unplanned downtime", "equivalent to 11% of their total revenues"; automotive line up to "$2.3 million per hour". Siemens PDF itself failed to load (connection reset); vendor-commissioned survey. https://www.theaemt.com/resource/the-true-cost-of-downtime-2024-a-comprehensive-analysis.html [Verified]
- **Agent design:** Tools: CMMS search, manual RAG, historian query, ERP stock check, work-order create (draft). Steps: classify fault code, retrieve similar past failures, pull 24h trends, rank causes with citations, draft work order and parts reservation. Planner approves; safety steps are copied from the approved LOTO procedure, never generated.
- **Open source today:** LGDiMaggio/predictive-maintenance-mcp (109 stars, MIT, not archived, last push 2026-11-05; README read: yes; addresses partly: vibration-diagnostics MCP for condition monitoring, no work-order drafting). Second: none found.
- **Demo path:** NASA PCoE bearing/turbofan data plus synthetic CMMS work orders and a public equipment manual.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 2. CAPA investigation and effectiveness checks (regulated plants)
- **Tier:** A | Enterprise: pass
- **Enterprise check:** Buyer: quality/regulatory head at device or pharma plant. Systems: QMS, complaint system, ERP batch/lot, audit tracker. Regulation: 21 CFR 820 / ISO 13485, Part 11 audit trail. Human gate: quality head signs CAPA closure.
- **Problem and today's workflow:** Quality engineers gather complaints, NCRs, batch records and audit findings, run root-cause analysis, write the CAPA and schedule effectiveness checks by hand.
- **Evidence:** Emergo by UL: "50% or more of warning letters for 2023 include" CAPA and complaint-procedure concerns; CAPA insufficient in 13 of 24 device warning letters (54%), complaints in 12 (50%). https://www.emergobyul.com/news/us-fda-cdrh-warning-letters-review-2023 [Verified]
- **Agent design:** Tools: QMS read/draft, ERP lot genealogy, complaint query, trend stats. Steps: cluster related records, propose 5-Why/fishbone hypotheses with evidence links, draft CAPA plan and effectiveness criteria, schedule checks. Human edits and signs; all drafts versioned.
- **Open source today:** none found for QMS/CAPA (gh search 'capa quality' returned no hits). salesforce/PyRCA (572 stars, BSD-3-Clause, not archived, last push 2026-06-02; README read: yes, intro only; adjacent only: root-cause library for IT metrics).
- **Demo path:** FDA warning letters text plus synthetic NCR/complaint tables.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 3. Supplier embedded-emissions data collection for EU CBAM declarations
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: importers/EU manufacturers of steel, aluminium, cement, fertiliser. Systems: ERP purchasing, customs declarations, supplier portals, CBAM registry. Regulation: Reg. (EU) 2023/956 (definitive period from 1 Jan 2026). Human gate: compliance officer signs declaration.
- **Problem and today's workflow:** Teams chase non-EU suppliers by email for installation-level emissions, check them against default values and CN codes in spreadsheets.
- **Evidence:** European Commission: "As of 1 January 2026, CBAM is applicable under its definitive regime." The default-values vs verified-data point was not on that page and is not asserted; check the regulation and implementing acts. https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism_en [Verified]
- **Agent design:** Tools: ERP import lines, CN-code lookup, email/portal requests, emission-report parser, default-value table. Steps: map imports to CN codes, request data, validate and flag gaps, compute embedded emissions, draft declaration. Officer approves submission.
- **Open source today:** none found (gh search 'cbam' returned only unrelated attention-module repos). cloud-carbon-footprint/cloud-carbon-footprint (1,055 stars, Apache-2.0, not archived, last push 2026-04-23; README read: yes; unrelated: cloud energy estimation).
- **Demo path:** Synthetic import lines plus Commission default-value tables and sample supplier reports.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 4. Electronic component obsolescence and last-time-buy decisions
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: sustainment/procurement in defence, avionics, medical, industrial. Systems: PLM/BOM, ERP, distributor APIs, PCN feeds. Regulation: RoHS, DFARS/AS5553 counterfeit avoidance, configuration control. Human gate: engineering and procurement sign buy/redesign plan.
- **Problem and today's workflow:** Engineers track EOL notices by hand, hunt form-fit-function alternates and decide last-time-buy quantities across thousands of BOM lines.
- **Evidence:** US Army AMRDEC obsolescence team chief: "70 percent of electronics are obsolete prior to system fielding" (single figure; the 70-80% range was wrong). https://www.army.mil/article/167937/Managing_obsolete_products_could_save_government_millions [Corrected]
- **Agent design:** Tools: BOM read, distributor stock/lifecycle APIs, datasheet parser, RoHS check. Steps: flag at-risk parts, find alternates, rate requalification effort, forecast demand, draft LTB or redesign proposal. Humans approve.
- **Open source today:** none found for obsolescence (gh search 'obsolescence bom' returned no hits). oaslananka/kicad-mcp-pro (181 stars, MIT, not archived, last push 2026-11-05; README read: yes; adjacent only: KiCad design and DFM MCP).
- **Demo path:** Open hardware KiCad BOMs plus a synthetic PCN/EOL feed.
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 5. Tariff classification (HS code) and origin determination
- **Tier:** B (classification model does core; agent assembles evidence and routes) | Enterprise: pass
- **Enterprise check:** Buyer: trade-compliance at manufacturers/importers. Systems: ERP/GTS item master, PLM specs, customs broker portal. Regulation: 19 U.S.C. 1592, reasonable care. Human gate: licensed broker/compliance lead signs.
- **Problem and today's workflow:** Analysts classify thousands of parts from specs and drawings, search rulings and apply duty programs.
- **Evidence:** Purolator International blog on Canada's Auditor General audit: "roughly 20 percent of shipments entering Canada have the wrong tariff classification code"; government "missing out on $21 million annually" (not $42M+). Carrier blog; primary audit not opened. https://www.purolatorinternational.com/the-high-price-of-tariff-classification-mistakes [Corrected]
- **Agent design:** Tools: item-master read, HTS lookup, CROSS ruling search, spec/drawing reader. Steps: extract attributes, shortlist codes with ruling citations, draft rationale, flag low-confidence. Broker approves.
- **Open source today:** none found (gh search 'hs code' returned only unrelated repos).
- **Demo path:** USITC HTS plus CBP CROSS rulings against synthetic part descriptions.
- **Verification:** 2026-11-06, Corrected, search done yes

### 6. Supplier corrective action (SCAR / 8D) review and escalation
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: supplier quality. Systems: QMS NCR module, ERP receiving/inspection, supplier portal. Regulation/audit: ISO 9001 s.8.4, IATF 16949 where automotive. Human gate: supplier quality engineer accepts or rejects 8D.
- **Problem and today's workflow:** Engineers read supplier 8D PDFs, judge whether root cause and containment are credible, chase late responses and update scorecards.
- **Evidence:** No reliable figure found. [Unconfirmed]
- **Agent design:** Tools: NCR read, receiving-inspection history, portal messaging, 8D template checker. Steps: check completeness and root-cause logic, compare against prior repeats, request clarification, propose accept/reject. Engineer decides.
- **Open source today:** none found (gh search '8d supplier' returned no hits).
- **Demo path:** Synthetic NCRs and generated 8D reports with seeded weaknesses.
- **Verification:** 2026-11-06, Unconfirmed, search done yes

### 7. Product material compliance (REACH SVHC, RoHS, SCIP) across supplier declarations
- **Tier:** A | Enterprise: pass
- **Enterprise check:** Buyer: product compliance at electronics/industrial OEMs. Systems: PLM BOM, supplier material declarations (IPC-1752), ECHA SCIP. Regulation: REACH Art. 33, RoHS 2011/65/EU, WFD 2018/851. Human gate: compliance manager approves declarations and SCIP submissions.
- **Problem and today's workflow:** Each Candidate List update (twice a year) requires re-checking every BOM item against supplier declarations by email and spreadsheet.
- **Evidence:** CIRS Group report on ECHA's September 2021 SCIP publication: "The SCIP database now displays more than four million article notifications", including duplicates (ECHA's own page returned 403). https://www.cirs-group.com/en/chemicals/scip-database-has-officially-been-published [Verified]
- **Agent design:** Tools: BOM read, Candidate List diff, declaration parser, supplier email, SCIP file builder. Steps: diff list, find affected parts, request updated declarations, compute >0.1% w/w status, draft notifications. Manager approves.
- **Open source today:** none found (gh search 'reach rohs' returned no hits).
- **Demo path:** ECHA Candidate List plus synthetic BOM and declarations.
- **Verification:** 2026-11-06, Verified, search done yes

### 8. Engineering change order (ECO) impact analysis across BOM, inventory and compliance
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: engineering/ops. Systems: PLM, ERP (inventory, open POs, work orders), QMS, regulatory files. Regulation: design-change control (21 CFR 820, AS9100 s.8.5.6). Human gate: change control board approves.
- **Problem and today's workflow:** Engineers manually trace where-used, open orders, validation, labelling and certification impacts before a change board meets.
- **Evidence:** No reliable figure found. [Unconfirmed]
- **Agent design:** Tools: PLM where-used, ERP stock and PO queries, doc search. Steps: build impact list, estimate scrap/rework cost, flag affected regulatory filings, draft ECO package. CCB approves.
- **Open source today:** none found (gh search 'engineering change order' returned only unrelated repos).
- **Demo path:** Synthetic multi-level BOM and ERP snapshot.
- **Verification:** 2026-11-06, Unconfirmed, search done yes

### 9. Process safety management of change (MOC) and PHA action tracking
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: chemical/process plants. Systems: MOC workflow, P&IDs, PHA database, CMMS. Regulation: OSHA 29 CFR 1910.119 (l) MOC, (e) PHA. Human gate: process safety lead and operations sign MOC and pre-startup review.
- **Problem and today's workflow:** Engineers check each proposed change against P&IDs, prior PHAs and operating procedures, then chase open recommendations.
- **Evidence:** OSHA 1910.119 citation and penalty totals (344/87/$3.13M) not confirmed: the safteng page is member-only and a second search excerpt gave conflicting totals. Numbers removed. Reference, not confirmed: https://safteng.net/oshas-data-on-1910-119-october-2023-through-september-2024/ [Unconfirmed]
- **Agent design:** Tools: MOC system, document search, PHA register, CMMS. Steps: identify affected procedures and PHA nodes, draft hazard checklist, list required updates, track closure. Humans decide risk acceptance.
- **Open source today:** none found (gh search 'process safety' returned only unrelated repos).
- **Demo path:** Synthetic MOC requests plus public CSB investigation reports.
- **Verification:** 2026-11-06, Unconfirmed, search done yes

### 10. Environmental release reporting (TRI Form R / EPCRA) data assembly and QA
- **Tier:** B | Enterprise: pass
- **Enterprise check:** Buyer: EHS at manufacturing sites. Systems: ERP purchasing, chemical inventory, air permits, waste manifests. Regulation: EPCRA s.313 (40 CFR 372). Human gate: certifying official signs.
- **Problem and today's workflow:** EHS staff compile thresholds, releases and waste-management quantities from multiple systems each year and reconcile against prior reports.
- **Evidence:** EPA 2022 TRI National Analysis: "For calendar year 2022, more than 21,000 facilities reported to the TRI Program"; 28.6 billion lb of TRI chemicals managed as waste, 12% released or disposed of. The 21,752 and 3.3 billion lb figures were not on the page. https://19january2025snapshot.epa.gov/trinationalanalysis/introduction-2022-tri-national-analysis [Corrected]
- **Agent design:** Tools: purchasing and inventory queries, TRI chemical list, prior-year compare. Steps: threshold determination, estimate releases, flag year-over-year anomalies, draft Form R. Official certifies.
- **Open source today:** not checked (GitHub search rate-limited).
- **Demo path:** EPA TRI basic data files as prior-year baseline plus synthetic purchasing data.
- **Verification:** 2026-11-06, Corrected, repos not checked

## Sources
- https://assets.new.siemens.com/siemens/assets/api/uuid:1b43afb5-2d07-47f7-9eb7-893fe7d0bc59/TCOD-2024_original.pdf
- https://www.emergobyul.com/news/us-fda-cdrh-warning-letters-review-2023
- https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism_en
- https://www.army.mil/article/167937/Managing_obsolete_products_could_save_government_millions
- https://www.purolatorinternational.com/the-high-price-of-tariff-classification-mistakes
- https://echa.europa.eu/-/scip-duty-kicks-in-5-million-notifications-received-for-harmful-chemicals-in-products
- https://safteng.net/oshas-data-on-1910-119-october-2023-through-september-2024/
- https://19january2025snapshot.epa.gov/trinationalanalysis/introduction-2022-tri-national-analysis
- Dataset links listed in section 2.
