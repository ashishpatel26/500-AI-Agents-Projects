# Agriculture & Food

## Overview
Growers, insurers, food manufacturers and importers spend effort on traceability, safety plans, labeling, certifications and supply-chain due diligence. Manual work concentrates in reconciling supplier documents, lot codes and field records across ERP, email and paper, then assembling evidence for regulators or certifiers. Errors lead to recalls, denied claims or market-access loss.

## Systems of record, regulations, public datasets
- Systems: ERP (SAP, Oracle), QMS/LIMS, WMS/TMS, supplier portals, PLM/formulation systems, label artwork systems, farm management software, RMA/insurer claims systems, GIS/satellite platforms.
- Regulations: FSMA 204 Food Traceability Rule (2022); FSMA Preventive Controls (21 CFR 117) and FSVP (21 CFR 1 Subpart L); FALCPA 2004 and FASTER Act 2021; USDA National Organic Program (7 CFR 205; Strengthening Organic Enforcement rule, 2023); EU Deforestation Regulation 2023/1115; FIFRA; USDA RMA Loss Adjustment Manual.
- Datasets: FDA recalls https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts ; FDA inspection citations https://www.accessdata.fda.gov/scripts/inspsearch ; USDA RMA data https://www.rma.usda.gov/data ; USDA Organic Integrity Database https://organic.ams.usda.gov/integrity ; PlantVillage images; Global Forest Watch https://www.globalforestwatch.org ; CDC outbreak notices.

## Use cases

### 1. Crop insurance claim adjustment and loss verification
- **Tier:** A | Enterprise: pass
- **Enterprise check:** Buyer: approved insurance providers; systems: claims system, policy admin, weather/NDVI feeds, farmer records; RMA Loss Adjustment Manual, fraud oversight; licensed adjuster signs.
- **Problem and today's workflow:** Adjusters inspect fields, reconcile planting records, yield history and weather, compute indemnities in worksheets.
- **Evidence:** USDA RMA 2023 Accomplishment report (PDF text extracted): "$19.8 billion in losses paid for 2022 crop year." https://rma.usda.gov/sites/default/files/2024-05/RMA%202023%20Accomplishment%20Text.pdf [Verified]
- **Agent design:** Pull policy terms and satellite/weather data, draft loss worksheet, flag anomalies for SIU; adjuster signs, no automated denial.
- **Open source today:** none found (gh search repos "crop insurance claims", stars>=20, not archived: no hits).
- **Demo path:** RMA public cause-of-loss data plus Sentinel-2 NDVI and synthetic claims.
- **Verification:** 2026-11-06, Verified, repos checked: none listed, search run

### 2. FSMA 204 traceability recordkeeping and trace-back
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: food processors/distributors/retailers; systems: ERP, WMS, supplier EDI/email; FDA Food Traceability Rule; food safety lead signs.
- **Problem and today's workflow:** Key data elements at critical tracking events are scattered; during outbreaks staff manually build spreadsheets.
- **Evidence:** FDA page opened: records "must be made available to the FDA within 24 hours after a request is made"; original compliance date 20 Jan 2026; FDA proposed 20 Jul 2028 ("extend the compliance date for the rule by 30 months") and Congress directed no enforcement before that date. https://www.fda.gov/food/food-safety-modernization-act-fsma/fsma-final-rule-requirements-additional-traceability-records-certain-foods [Verified]
- **Agent design:** Reconcile lot codes across partners, find missing KDEs, chase suppliers, assemble sortable spreadsheet; lead approves submission.
- **Open source today:** none found for FSMA 204 (gh search repos "FSMA traceability", stars>=20: no hits). Adjacent only: FoodPrintLabs/foodprint (65 stars, MIT, not archived, last push 2025-11-01; README read: yes) - Algorand blockchain traceability for smallholder farmers, not FSMA 204 recordkeeping.
- **Demo path:** Synthetic lot/shipment graph for leafy greens; FDA Food Traceability List.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 3. Pesticide-label-compliant scouting and treatment advisory
- **Tier:** B | Enterprise: pass
- **Enterprise check:** Buyer: ag retailers and agronomy service firms; systems: farm management software, spray records, label database, weather; FIFRA label is law; certified crop adviser signs.
- **Problem and today's workflow:** Agronomists combine scouting photos, weather and spray history to recommend treatments within label restrictions.
- **Evidence:** IPPC press briefing: "Plant pests destroy up to 40 percent of agricultural crops, including food crops each year", costing "approximately USD 220 billion annually in global trade losses" (the $220B is stated as trade losses, not as a disease cost as first written). https://ippc.int/en/news/geneva-press-briefing-update-on-global-plant-pests-and-their-devastating-impact-on-food-security/ [Corrected]
- **Agent design:** Image classifier (model does core), agent checks label, interval, MRL and buffer rules, drafts recommendation; adviser signs.
- **Open source today:** No label-aware advisory agent found. Adjacent only, classifiers/datasets: spMohanty/PlantVillage-Dataset (1,028 stars, no licence, last push 2026-02-05; README read: yes - 54,306 leaf images dataset); imskr/Plant_Disease_Detection (366 stars, GPL-3.0, last push 2023-02-14; README read: yes - plant disease detector web app, stale).
- **Demo path:** PlantVillage images plus synthetic label rules.
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 4. Allergen and label compliance on formulation or ingredient change
- **Tier:** A | Enterprise: pass
- **Enterprise check:** Buyer: food manufacturers; systems: PLM/spec system, ERP BOM, artwork system, changeover schedules; FALCPA/FASTER Act; QA manager approves.
- **Problem and today's workflow:** Each ingredient or line change requires re-check of specs, cross-contact controls and labels by hand.
- **Evidence:** Statista chart page: "This accounted for nearly four in ten cases (38.8 percent) of all food recalls." The extract did not show the subject of the sentence, so attribution to undeclared allergens (PIRG data) is probable but not confirmed. https://www.statista.com/chart/36281/fda-and-usda-food-recalls-in-the-united-states/ [Verified]
- **Agent design:** Diff BOM, read supplier specs, compare to label declaration, flag changeover risks, route to QA; QA approves.
- **Open source today:** none found (gh search repos "allergen labeling", stars>=20: no hits). Adjacent only: dmsl/foodscanner (35 stars, no licence, not archived, last push 2016-06-02, stale; README read: yes) - consumer smartphone nutrition/allergen analyzer.
- **Demo path:** Synthetic recipes with FDA recall notices as labelled errors.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 5. EU Deforestation Regulation due-diligence and plot geolocation verification
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: importers/traders of cocoa, coffee, soy, palm; systems: supplier portals, ERP, GIS; EUDR 2023/1115, EU TRACES filing; compliance officer signs.
- **Problem and today's workflow:** Staff collect plot polygons, validate legality and chase smallholder suppliers.
- **Evidence:** European Commission page opened: large and medium operators apply "from 30 December 2026"; micro and small operators 30 Dec 2026 for EUTR-annex products and 30 June 2027 for other EUDR products. https://trade.ec.europa.eu/access-to-markets/en/news/delay-until-december-2026-and-other-developments-implementation-eudr-regulation [Verified]
- **Agent design:** Validate polygons against forest-cover layers, score risk, chase missing records, draft statements; officer signs.
- **Open source today:** none found (gh search repos "EUDR deforestation", stars>=20, not archived: no hits).
- **Demo path:** Global Forest Watch data with synthetic supplier plots.
- **Verification:** 2026-11-06, Verified, repos checked: none listed, search run

### 6. FSVP importer supplier verification
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: US food importers; systems: ERP, supplier QMS, audit reports; 21 CFR Part 1 Subpart L; FDA inspections; qualified individual approves.
- **Problem and today's workflow:** Importers evaluate each foreign supplier's hazards, audits and inspection history manually.
- **Evidence:** FDA "about 15% of the US food supply is imported" could not be confirmed: the FSVP page and the FDA importing-food page both returned HTTP 404. Number removed. Reference, not confirmed: https://www.fda.gov/food/importing-food-products-united-states/foreign-supplier-verification-program-fsvp [Unconfirmed]
- **Agent design:** Pull supplier audits, check FDA import alerts and recalls, draft evaluation and verification plan; qualified individual signs.
- **Open source today:** none found (gh search repos "FSVP", stars>=20, not archived: no hits).
- **Demo path:** FDA import alert and inspection data with synthetic suppliers.
- **Verification:** 2026-11-06, Unconfirmed, repos checked: none listed, search run

### 7. Organic certification review and inspection follow-up
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: accredited certifiers and large handlers; systems: certification database, organic system plans, mass-balance records; NOP 7 CFR 205 and Strengthening Organic Enforcement rule; certifier reviewer approves.
- **Problem and today's workflow:** Reviewers compare organic system plans with inspection reports and trace-back audits by hand.
- **Evidence:** no reliable figure found (reference, not confirmed: https://www.ams.usda.gov/rules-regulations/organic/enforcement). [Unconfirmed]
- **Agent design:** Extract plan details, reconcile purchases and sales (mass balance), draft noncompliance notices; reviewer decides.
- **Open source today:** none found (gh search repos "organic certification", stars>=20, not archived: no hits).
- **Demo path:** Organic Integrity Database plus synthetic transaction records.
- **Verification:** 2026-11-06, Unconfirmed, repos checked: none listed, search run

### 8. Environmental monitoring program (Listeria) corrective action
- **Tier:** B | Enterprise: needs figure
- **Enterprise check:** Buyer: RTE food plants; systems: LIMS, QMS, sanitation records; 21 CFR 117 corrective actions; FDA inspections; QA director approves.
- **Problem and today's workflow:** QA staff track positive swabs, investigate root cause and verify follow-up sampling.
- **Evidence:** CDC Listeria page opened: "CDC estimates that each year in the United States, 1,250 people are infected with Listeria, and 172 people die from the infection." The earlier 1,600 illnesses and 260 deaths do not match the current page. https://www.cdc.gov/listeria/about/index.html [Corrected]
- **Agent design:** Detect positive trends by zone, assemble sanitation/maintenance history, draft corrective action and sampling plan; QA approves.
- **Open source today:** none found (gh search repos "Listeria environmental monitoring", stars>=20, not archived: no hits).
- **Demo path:** Synthetic swab data with zones.
- **Verification:** 2026-11-06, Corrected, repos checked: none listed, search run

### 9. Recall execution and effectiveness checks
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: manufacturers/retailers; systems: ERP, customer/distributor lists, recall notices; 21 CFR 7 recall guidance; recall coordinator and legal approve.
- **Problem and today's workflow:** Teams identify affected lots, notify customers, collect responses and report effectiveness.
- **Evidence:** no reliable figure found (reference, not confirmed: https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts ; 21 CFR 7 not opened). [Unconfirmed]
- **Agent design:** Map lots to shipments, draft notices, track acknowledgments, escalate non-responders; coordinator approves.
- **Open source today:** none found (gh search repos "food recall", stars>=20, not archived: no hits).
- **Demo path:** Synthetic distribution graph.
- **Verification:** 2026-11-06, Unconfirmed, repos checked: none listed, search run

### 10. FDA Form 483 and warning-letter response drafting
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: food manufacturers; systems: QMS/CAPA, inspection reports, SOPs; FDA response timeline not confirmed; quality head and counsel sign.
- **Problem and today's workflow:** Quality teams gather evidence per observation and draft CAPA commitments.
- **Evidence:** no reliable figure found (the FDA 483 page returned HTTP 404 and the inspection-observations page has no response deadline, so the "15 business days" expectation is removed; reference, not confirmed: https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/inspection-references/fda-inspection-observations). [Unconfirmed]
- **Agent design:** Parse observations, find related records, draft response and CAPA timeline; head approves.
- **Open source today:** none found (gh search repos "FDA 483", stars>=20, not archived: no hits).
- **Demo path:** Public FDA 483 documents from FDA reading room.
- **Verification:** 2026-11-06, Unconfirmed, repos checked: none listed, search run

## Sources
- https://www.fda.gov/food/food-safety-modernization-act-fsma/fsma-final-rule-requirements-additional-traceability-records-certain-foods
- https://rma.usda.gov/sites/default/files/2024-05/RMA%202023%20Accomplishment%20Text.pdf
- https://ippc.int/en/news/geneva-press-briefing-update-on-global-plant-pests-and-their-devastating-impact-on-food-security/
- https://www.statista.com/chart/36281/fda-and-usda-food-recalls-in-the-united-states/
- https://trade.ec.europa.eu/access-to-markets/en/news/delay-until-december-2026-and-other-developments-implementation-eudr-regulation
- https://www.fda.gov/food/importing-food-products-united-states/foreign-supplier-verification-program-fsvp
- https://www.ams.usda.gov/rules-regulations/organic/enforcement
- https://www.cdc.gov/listeria/about/index.html
- https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts
- https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/inspection-references/fda-inspection-observations
- https://www.globalforestwatch.org ; https://organic.ams.usda.gov/integrity ; https://www.rma.usda.gov/data
