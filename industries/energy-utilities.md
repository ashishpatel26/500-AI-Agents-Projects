# Energy & Utilities

## Overview
Electric, gas and water utilities and the developers who connect to them spend most effort on regulatory filings, interconnection and permitting studies, asset-inspection records, and compliance evidence for auditors. Manual work concentrates where engineers move data between studies, GIS/asset systems and PDF filings (spreadsheets, shared drives, email), then a licensed or accountable person signs. Timelines are set by tariffs, statutes and regulator data requests, so delay has a direct cost.

## Systems of record, regulations, public datasets
- Systems: SCADA/EMS/DMS, ADMS, GIS (Esri), EAM/CMMS (Maximo, SAP PM), CIS/billing (SAP IS-U), outage management (OMS), interconnection portals, regulatory document systems, LIMS (water), power-flow tools (PSS/E, pandapower).
- Regulations: FERC Order 2023 (2023, interconnection); NERC CIP standards (numbering range not confirmed); NEPA and CEQ rules; Safe Drinking Water Act Lead and Copper Rule Revisions/LCRI (2024); California Wildfire Mitigation Plans (SB 901, 2018); 10 CFR 50 Appendix B (NRC quality assurance); 40 CFR Part 75 (EPA CEMS); IEEE 1547-2018 and CPUC Rule 21.
- Datasets: LBNL Queued Up https://emp.lbl.gov/queues ; EPA CAMPD emissions https://campd.epa.gov ; EIA-860/923 https://www.eia.gov/electricity/data.php ; EPA lead service line data https://www.epa.gov/ground-water-and-drinking-water ; CEQ EIS database https://eplanning.blm.gov and https://cdxapps.epa.gov/cdx-enepa-II/public/action/eis/search ; NREL/IEEE test feeders https://www.nrel.gov/grid/ieee-test-feeders ; NRC LER search https://www.nrc.gov/reading-rm/doc-collections/event-status/.

## Use cases

### 1. Generator interconnection study screening and queue management
- **Tier:** A | Enterprise: pass
- **Enterprise check:** Buyer: transmission owners/ISOs and developers; systems: interconnection portal, PSS/E models, queue spreadsheets; FERC Order 2023 study deadlines, penalties for late studies; engineer certifies study results.
- **Problem and today's workflow:** Planners and developers run cluster studies, allocate network-upgrade costs and re-study after withdrawals, mostly with spreadsheets and PDF reports. Each withdrawal cascades into re-study.
- **Evidence:** Berkeley Lab Queued Up 2025 edition (primary PDF): "Roughly 2,290 gigawatts (GW) of capacity actively seeking interconnection"; "The typical project built in 2024 took 55 months from the interconnection request to commercial operations". https://emp.lbl.gov/sites/default/files/2025-12/Queued%20Up%202025%20Edition%20-%2012.15.2025.pdf [Verified]
- **Agent design:** Parse study reports and queue data, call power-flow tool for screening cases, recompute cost allocation after a withdrawal, draft deficiency letters. Engineer reviews and certifies before anything goes to developers.
- **Open source today:** none found (gh search repos "interconnection queue", stars>=20, not archived: no hits).
- **Demo path:** pandapower on IEEE test feeders plus synthetic queue of 50 requests; LBNL queue public dataset for realistic mix.
- **Verification:** 2026-11-06, Verified, repos checked: none listed, search run

### 2. NEPA environmental review drafting and consistency checking for energy infrastructure
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: federal agencies (FERC, DOE, BLM) and consultants for pipelines, transmission, solar; systems: EIS documents, GIS, species databases, comment-management tools; Administrative Procedure Act litigation exposure; agency decision-maker signs.
- **Problem and today's workflow:** Staff assemble EIS text from specialist studies and prior documents, and match thousands of public comments to consistent responses.
- **Evidence:** CEQ EIS timeline figure (4.5 years NOI to ROD) could not be confirmed: the CEQ PDF URL now redirects to nepa.gov and the report was not opened. Number removed. Reference, not confirmed: https://ceq.doe.gov/docs/nepa-practice/CEQ_EIS_Timeline_Report_2020-6-12.pdf [Unconfirmed]
- **Agent design:** Query GIS/species APIs, retrieve precedent EIS sections, draft sections with citations, cluster comments and propose responses, flag inconsistencies across chapters. Human authors own the record.
- **Open source today:** none found (gh search repos "NEPA environmental review", stars>=20, not archived: no hits).
- **Demo path:** EPA EIS database public documents plus a set of draft EIS chapters; evaluate cross-chapter consistency detection.
- **Verification:** 2026-11-06, Unconfirmed, repos checked: none listed, search run

### 3. Lead service line inventory resolution and replacement planning
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: water utilities; systems: GIS, CIS/billing, permit archives, work-order system; LCRI requires inventories and replacement plans, public notice; utility director and state agency approve.
- **Problem and today's workflow:** Engineers classify "unknown" material service lines using records, historical permits and field verification, then schedule excavations.
- **Evidence:** EPA LCRI page opened: final rule issued October 8 (2024) and requires systems to "identify and replace lead pipes within 10 years". The specific dates (inventory 16 Oct 2024; replacement plans 1 Nov 2027) were not on any page opened (the fact sheet PDF and Q&A page failed to load) and are removed. Reference, not confirmed: https://www.epa.gov/system/files/documents/2024-10/final_lcri_fact-sheet_statespws.pdf [Unconfirmed]
- **Agent design:** Reconcile records, call material-prediction model, rank verification digs, draft notices and state reporting. Model predictions never replace field verification where the rule demands it; director approves.
- **Open source today:** none found (gh search repos "lead service line", stars>=20, not archived: no hits).
- **Demo path:** Synthetic parcel/service-line table with build year and permit text; some public inventories published by cities.
- **Verification:** 2026-11-06, Unconfirmed, repos checked: none listed, search run

### 4. Utility wildfire mitigation plan evidence assembly
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: California electric utilities; systems: GIS, vegetation inspection database, LiDAR, weather data, EAM; Energy Safety review and data requests; safety officer signs.
- **Problem and today's workflow:** Teams compile annual plan updates from risk models, inspection results and progress metrics, then answer regulator data requests.
- **Evidence:** Energy Safety page opened: SDG&E 2025 WMP Update signed off with improvement areas; "The Bear Valley Electric Service 2025 WMP Update was approved on Oct. 21"; other decisions to follow. The earlier claim that PG&E and SCE were approved and PacifiCorp, Liberty and LS Power ordered to resubmit is not on this page and is removed. No quantitative figure. https://energysafety.ca.gov/news/2024/10/30/energy-safety-approves-2025-wildfire-mitigation-plan-update-for-san-diego-gas-and-electric/ [Corrected]
- **Agent design:** Pull metrics from inspection/asset systems, populate plan tables, track data-request deadlines, draft narrative with source links. Safety officer signs; PSPS decisions stay human.
- **Open source today:** none found for utility workflow (gh search repos "wildfire mitigation plan utility", stars>=20: no hits). Adjacent only: lautenberger/elmfire (74 stars, NOASSERTION licence, not archived, last push 2026-10-25; README read: yes) - wildland fire spread model, not a filing tool.
- **Demo path:** Energy Safety public WMP documents and data-request spreadsheets as inputs.
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 5. NERC CIP compliance evidence collection and gap review
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: bulk-electric-system owners/operators; systems: asset inventory/CMDB, patch tools, access-control and ticketing systems, SIEM; NERC CIP audits by regional entities with monetary penalties; compliance officer attests.
- **Problem and today's workflow:** Analysts hand-collect screenshots, logs and tickets to prove patch evaluation, access reviews and baseline changes across thousands of cyber assets.
- **Evidence:** no reliable figure found (the NERC standards page opened but does not list individual CIP standards, so the CIP-002 to CIP-015 range and the 35-day patch evaluation window mentioned in Agent design are not confirmed). [Unconfirmed]
- **Agent design:** Per requirement, query CMDB/patch/access systems, assemble evidence packets, flag missed 35-day patch evaluation windows and incomplete reviews. Compliance officer reviews each packet before audit submission.
- **Open source today:** none found for audit-evidence automation (gh search repos "NERC CIP", stars>=20: one generic OPA compliance-policy library, ynotbhatc/rego_policy_libraries, 23 stars, not NERC-specific; adjacent only, description read, README not read).
- **Demo path:** Synthetic asset inventory, patch feeds and access logs; check evidence completeness.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes (description only)

### 6. Rate case filing support and regulatory data-request response
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: investor-owned utilities; systems: general ledger/ERP, FERC Form 1 data, work management, regulator filing portals; commission proceedings with discovery deadlines; regulatory counsel signs testimony.
- **Problem and today's workflow:** Hundreds of data requests per case require analysts to locate prior responses, pull ledger data and keep answers consistent with testimony.
- **Evidence:** no reliable figure found (reference, not confirmed: https://www.ferc.gov/industries-data/electric/general-information/electric-industry-forms/form-1-electric-utility-annual). [Unconfirmed]
- **Agent design:** Retrieve prior responses/exhibits, query ERP for figures, draft answers and cross-check against testimony numbers, route to subject-matter experts for approval.
- **Open source today:** none found (gh search repos "rate case utility", stars>=20, not archived: no hits).
- **Demo path:** Public FERC Form 1 bulk data plus public commission data-request sets.
- **Verification:** 2026-11-06, Unconfirmed, repos checked: none listed, search run

### 7. Distributed energy resource (DER) interconnection application review
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: distribution utilities; systems: application portal, GIS/ADMS feeder model, hosting-capacity maps; IEEE 1547-2018 and state rules (CPUC Rule 21) with timelines; utility engineer approves.
- **Problem and today's workflow:** Engineers check completeness of solar/storage applications, run supplemental screens against feeder models and request corrections by email.
- **Evidence:** no reliable figure found (reference, not confirmed: https://standards.ieee.org/ieee/1547/5915/ ; IEEE 1547-2018 and CPUC Rule 21 not re-opened). [Unconfirmed]
- **Agent design:** Validate application against checklist, extract equipment specs from datasheets, run screen via power-flow tool, draft deficiency or approval; engineer signs off.
- **Open source today:** none found (gh search repos "DER interconnection", stars>=20, not archived: no hits).
- **Demo path:** NREL test feeders with synthetic applications.
- **Verification:** 2026-11-06, Unconfirmed, repos checked: none listed, search run

### 8. Nuclear corrective action program condition-report screening
- **Tier:** B | Enterprise: needs figure
- **Enterprise check:** Buyer: nuclear plant operators; systems: CAP database, work orders, procedures; 10 CFR 50 Appendix B requires corrective actions; NRC inspections; screening committee approves classification.
- **Problem and today's workflow:** Staff screen thousands of condition reports per year for significance, duplicates and trending.
- **Evidence:** no reliable figure found (10 CFR 50 Appendix B page not opened; reference, not confirmed: https://www.nrc.gov/reading-rm/doc-collections/cfr/part050/part050-appb.html). [Unconfirmed]
- **Agent design:** Classify, link duplicates/similar past events, propose significance level and cause codes; screening committee decides. Model does core classification, agent drafts and routes.
- **Open source today:** none found (gh search repos "nuclear corrective action", stars>=20, not archived: no hits).
- **Demo path:** NRC Licensee Event Reports as public text corpus.
- **Verification:** 2026-11-06, Unconfirmed, repos checked: none listed, search run

### 9. Power plant emissions (CEMS) data validation and Part 75 quarterly reporting
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: fossil generators; systems: DAHS/CEMS, EPA ECMPS, maintenance records; 40 CFR Part 75 e-reporting with certification by designated representative; false-statement liability.
- **Problem and today's workflow:** Environmental staff review hourly data, substitute missing data per rules, reconcile QA tests and submit quarterly files.
- **Evidence:** no reliable figure found (the EPA Part 75 page returned HTTP 404; reference, not confirmed: https://www.epa.gov/airmarkets/part-75-emissions-monitoring). [Unconfirmed]
- **Agent design:** Pull hourly data, detect gaps/invalid QA, apply missing-data routines, pre-validate against ECMPS checks, draft certification package; DR certifies.
- **Open source today:** none found (gh search repos "CEMS emissions", stars>=20, not archived: no hits).
- **Demo path:** EPA CAMPD hourly emissions downloads.
- **Verification:** 2026-11-06, Unconfirmed, repos checked: none listed, search run

### 10. Transmission and pipeline right-of-way permit and easement tracking
- **Tier:** B | Enterprise: needs figure
- **Enterprise check:** Buyer: transmission owners; systems: land-rights database, GIS, permit portals; state/federal permits, audit trail for easements; land agent and counsel approve.
- **Problem and today's workflow:** Land agents track expiring easements, encroachments and permit conditions across PDFs and county records.
- **Evidence:** no reliable figure found. [Unconfirmed]
- **Agent design:** Extract terms from easement scans, link to GIS parcels, flag expirations and conditions, draft notices; counsel approves.
- **Open source today:** none found (gh search repos "right-of-way easement", stars>=20, not archived: no hits).
- **Demo path:** Synthetic easement PDFs and public parcel data.
- **Verification:** 2026-11-06, Unconfirmed, repos checked: none listed, search run

## Sources
- https://emp.lbl.gov/queues
- https://ceq.doe.gov/docs/nepa-practice/CEQ_EIS_Timeline_Report_2020-6-12.pdf
- https://www.epa.gov/system/files/documents/2024-10/final_lcri_fact-sheet_statespws.pdf
- https://energysafety.ca.gov/news/2024/10/30/energy-safety-approves-2025-wildfire-mitigation-plan-update-for-san-diego-gas-and-electric/
- https://www.nerc.com/pa/Stand/Pages/CIPStandards.aspx
- https://www.ferc.gov/industries-data/electric/general-information/electric-industry-forms/form-1-electric-utility-annual
- https://standards.ieee.org/ieee/1547/5915/
- https://www.nrc.gov/reading-rm/doc-collections/cfr/part050/part050-appb.html
- https://www.epa.gov/airmarkets/part-75-emissions-monitoring
- https://campd.epa.gov ; https://www.eia.gov/electricity/data.php ; https://www.nrel.gov/grid/ieee-test-feeders
