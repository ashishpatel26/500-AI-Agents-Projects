# Oil, Gas & Mining

## Overview
Operators in upstream oil and gas, pipelines and mining spend heavy effort on safety and environmental compliance, permits, and reserve/regulatory reporting. Manual work concentrates in reading inspection and incident narratives, assembling filings from field and geoscience systems, and tracking regulator deadlines. Errors carry criminal or large civil exposure, so humans sign.

## Systems of record, regulations, public datasets
- Systems: well/drilling databases (WellView, OpenWells), SCADA/historians (OSIsoft PI), EAM (SAP PM, Maximo), HSE platforms (Enablon, Intelex), LDAR software, GIS, mine planning (Deswik, Leapfrog), resource models, ERP, royalty/accounting systems.
- Regulations: EPA OOOOb/OOOOc methane rules (2024); OSHA PSM 29 CFR 1910.119; PHMSA 49 CFR 192/195; BSEE 30 CFR 250 Subpart Q/S; SEC S-K 1300 (2018, mining disclosure); JORC 2012; NI 43-101; MSHA 30 CFR; GISTM (2020); ONRR 30 CFR Parts 1200-1290.
- Datasets: BSEE incident data https://www.data.bsee.gov ; PHMSA incident data https://www.phmsa.dot.gov/data-and-statistics/pipeline/pipeline-incident-20-year-trends ; MSHA open data https://arlweb.msha.gov/OpenGovernmentData/OGIMSHA.asp ; EPA GHGRP FLIGHT https://ghgdata.epa.gov ; ONRR data https://revenuedata.doi.gov ; state well data (e.g. Texas RRC, Colorado ECMC); USGS orphan well data.

## Use cases

### 1. Methane leak detection (LDAR) and super-emitter response
- **Tier:** A | Enterprise: pass
- **Enterprise check:** Buyer: upstream/midstream operators; systems: LDAR database, asset register, work-order system, satellite/aerial alert feeds; EPA methane rule, Clean Air Act certification; EHS manager certifies.
- **Problem and today's workflow:** Staff correlate OGI surveys, continuous monitors and third-party alerts with assets, dispatch crews, track repair deadlines and write reports.
- **Evidence:** EPA super-emitter page opened: events have "an emission rate of 100 kilograms per hour of methane or greater"; operators must start an investigation "within five calendar days" of EPA notification and report findings within 15 days; implementation "extended until January 22, 2027". The "first repair attempts due within 30 days" claim is not on the page and is removed. https://www.epa.gov/compliance/super-emitter [Corrected]
- **Agent design:** Match alert coordinates to asset register, open work orders, track deadlines, draft investigation report; EHS manager certifies.
- **Open source today:** geoschem/integrated_methane_inversion (50 stars, MIT, not archived, last push 2026-11-04; README read: yes) - atmospheric emissions inversion workflow, adjacent only. UCSB-VRL/MethaneMapper-Spectral-Absorption-aware-Hyperspectral-Transformer-for-Methane-Detection (85 stars, NOASSERTION licence, last push 2024-02-16; README read: yes) - airborne hyperspectral detection model, adjacent only (repo was renamed from MethaneMapper). Neither handles compliance workflow; gh search "methane LDAR" found no others.
- **Demo path:** Synthetic asset register with simulated alert feed; public methane plume datasets.
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 2. HSE incident investigation and trend analysis
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: operators/drillers; systems: HSE incident system, IADC/BSEE reports, work permits, CMMS; BSEE incident reporting (30 CFR 250.188), OSHA recordkeeping; HSE manager approves root cause.
- **Problem and today's workflow:** Investigators read narratives, pull permits and maintenance history, assign causes and corrective actions; trending across sites is manual.
- **Evidence:** no reliable figure found (30 CFR 250.188 section opened on Cornell LII: it lists reportable incidents (deaths, well control failures, fires, injuries) with 15-day written follow-up; no volume figure. Reference, not confirmed: https://www.data.bsee.gov). [Unconfirmed]
- **Agent design:** Gather linked records, draft timeline and causal factors, check similar past incidents, propose actions; investigator and HSE manager approve.
- **Open source today:** none found (gh search repos "HSE incident investigation", stars>=20, not archived: no hits).
- **Demo path:** BSEE public incident and INC (enforcement) data.
- **Verification:** 2026-11-06, Unconfirmed, repos checked: none listed, search run

### 3. Well integrity review
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: operators; systems: well-file/WellView, annulus pressure logs, cement/casing logs; BSEE 30 CFR 250 and state rules; well integrity engineer signs barrier assessment.
- **Problem and today's workflow:** Engineers review sustained casing pressure, logs and test results to decide on remediation, a mostly document-driven judgment.
- **Evidence:** no reliable figure found (Davies et al. 2014 "2% to 75%" barrier failure range could not be confirmed: the DOI only redirects to Elsevier. Number removed; reference, not confirmed: https://doi.org/10.1016/j.marpetgeo.2014.07.011). [Unconfirmed]
- **Agent design:** Extract pressure trends and test results, compare to barrier envelope, flag anomalies, draft integrity assessment; engineer signs.
- **Open source today:** none found (gh search repos "well integrity", stars>=20, not archived: no hits).
- **Demo path:** Synthetic annulus-pressure time series plus public state well files.
- **Verification:** 2026-11-06, Unconfirmed, repos checked: none listed, search run

### 4. Mineral reserve and resource reporting (S-K 1300 / JORC / NI 43-101)
- **Tier:** B | Enterprise: needs figure
- **Enterprise check:** Buyer: mining issuers; systems: resource models, drill-hole databases, cost models, ERP; SEC S-K 1300 requires qualified-person-backed technical report summaries; Qualified Person signs.
- **Problem and today's workflow:** Geologists/engineers reconcile models, price assumptions and cost data into technical reports and check consistency with prior filings.
- **Evidence:** SEC final rule release 33-10570 (2018): "Registrants engaged in mining operations must comply with the final rule amendments for the first fiscal year beginning on or after January 1, 2021." https://www.sec.gov/files/rules/final/2018/33-10570.pdf (the s7-10-16 page returned HTTP 503). [Verified]
- **Agent design:** Compare model outputs to prior-year reserves, recalc cut-off grades, draft reconciliation and disclosure text; QP signs.
- **Open source today:** none found (gh search repos "mineral resource reporting JORC", stars>=20, not archived: no hits).
- **Demo path:** Public SEC technical report summaries (EDGAR) and synthetic block model.
- **Verification:** 2026-11-06, Verified, repos checked: none listed, search run

### 5. Drilling and mining permit application assembly
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: operators; systems: BLM/state permit portals (AFMSS), GIS, surveys, land records; permit conditions and NEPA; permitting manager signs.
- **Problem and today's workflow:** Land and regulatory staff assemble APD/plan-of-operations packages from surveys, lease maps, environmental studies and prior permits.
- **Evidence:** no reliable figure found (reference, not confirmed: https://www.blm.gov/programs/energy-and-minerals/oil-and-gas/operations-and-production/permitting). [Unconfirmed]
- **Agent design:** Check completeness against agency checklist, pull lease/GIS data, draft sections, respond to deficiency letters; permitting manager submits.
- **Open source today:** none found (gh search repos "drilling permit", stars>=20, not archived: no hits).
- **Demo path:** Public APD forms and state permit data with synthetic leases.
- **Verification:** 2026-11-06, Unconfirmed, repos checked: none listed, search run

### 6. Environmental compliance monitoring and exceedance reporting
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: operators and mines; systems: LIMS, discharge monitoring, air permits, EHS system; Clean Water Act NPDES, state permits; environmental manager certifies.
- **Problem and today's workflow:** Staff compare lab and monitor results against permit limits, investigate exceedances and prepare agency reports.
- **Evidence:** no reliable figure found (reference, not confirmed: https://echo.epa.gov). [Unconfirmed]
- **Agent design:** Ingest lab results, detect exceedances, pull context (flow, rainfall), draft notification and corrective plan; manager certifies.
- **Open source today:** none found (gh search repos "environmental exceedance", stars>=20, not archived: no hits).
- **Demo path:** EPA ECHO/DMR public discharge data.
- **Verification:** 2026-11-06, Unconfirmed, repos checked: none listed, search run

### 7. Royalty and production regulatory reporting reconciliation
- **Tier:** B | Enterprise: needs figure
- **Enterprise check:** Buyer: producers on federal/state leases; systems: production accounting, ERP, ONRR reporting; 30 CFR Parts 1210/1212; audit and penalty exposure; royalty accountant approves.
- **Problem and today's workflow:** Accountants reconcile volumes, prices and allowances across systems and fix report rejections.
- **Evidence:** no reliable figure found (reference, not confirmed: https://revenuedata.doi.gov ; 30 CFR 1210/1212 not opened). [Unconfirmed]
- **Agent design:** Compare production accounting to filings, explain variances, draft corrections; accountant approves.
- **Open source today:** none found (gh search repos "royalty", stars>=20: hits were NFT, loyalty-points and music-royalty software, unrelated).
- **Demo path:** Public ONRR revenue/production data.
- **Verification:** 2026-11-06, Unconfirmed, repos checked: none relevant, search run

### 8. Pipeline integrity: in-line inspection anomaly dig prioritization
- **Tier:** B | Enterprise: needs figure
- **Enterprise check:** Buyer: pipeline operators; systems: ILI vendor reports, GIS, integrity management database; PHMSA 49 CFR 192 Subpart O/195.452; integrity engineer approves digs.
- **Problem and today's workflow:** Engineers align ILI runs, apply remaining-strength calcs and decide which anomalies to excavate within regulatory deadlines.
- **Evidence:** no reliable figure found (reference, not confirmed: https://www.phmsa.dot.gov/data-and-statistics/pipeline/pipeline-incident-20-year-trends ; 49 CFR 192 Subpart O/195.452 not opened). [Unconfirmed]
- **Agent design:** Align runs, call strength-calc tools, rank anomalies by regulatory timeframe, draft dig list; engineer approves.
- **Open source today:** none found (gh search repos "pipeline in-line inspection", stars>=20, not archived: no hits).
- **Demo path:** Synthetic ILI anomaly lists with PHMSA incident data for context.
- **Verification:** 2026-11-06, Unconfirmed, repos checked: none listed, search run

### 9. Process safety: management of change (MOC) and PHA review
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: refiners/gas plants; systems: MOC system, P&IDs, PHA records, CMMS; OSHA PSM 1910.119 requires MOC and PHA revalidation every 5 years; process safety lead approves.
- **Problem and today's workflow:** Engineers check each change against PHA, P&IDs and procedures, manually updating affected documents.
- **Evidence:** OSHA 29 CFR 1910.119 opened: PHA must be "updated and revalidated" at least every five years; employers must "establish and implement written procedures to manage changes". No volume or dollar figure. https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.119 [Verified]
- **Agent design:** Find affected documents, flag PHA scenarios, draft MOC checklist, track closure; PSM lead approves.
- **Open source today:** none found (gh search repos "management of change PHA", stars>=20, not archived: no hits).
- **Demo path:** Synthetic MOC records and public CSB investigation reports (https://www.csb.gov).
- **Verification:** 2026-11-06, Verified, repos checked: none listed, search run

### 10. Orphan, idle well and asset-retirement obligation tracking
- **Tier:** B | Enterprise: needs figure
- **Enterprise check:** Buyer: operators, state regulators, acquirers; systems: well database, ARO accounting, bonding records; state plugging rules and financial assurance; manager approves.
- **Problem and today's workflow:** Staff reconcile idle wells, plugging cost estimates and bonds across state records and ERP.
- **Evidence:** The "$4.7 billion" IIJA orphan-well figure could not be confirmed: https://www.doi.gov/orphanwell returned HTTP 404 and no DOI page was opened. Number removed. Reference, not confirmed: https://www.doi.gov/orphanwell [Unconfirmed]
- **Agent design:** Match state records to internal registry, estimate plugging cost, flag bond shortfalls, draft plans; manager approves.
- **Open source today:** none found (gh search repos "orphan wells", stars>=20, not archived: no hits).
- **Demo path:** State public well-status datasets.
- **Verification:** 2026-11-06, Unconfirmed, repos checked: none listed, search run

## Sources
- https://epa.gov/compliance/super-emitter
- https://www.data.bsee.gov
- https://doi.org/10.1016/j.marpetgeo.2014.07.011
- https://www.sec.gov/rules-regulations/2018/10/s7-10-16
- https://www.blm.gov/programs/energy-and-minerals/oil-and-gas/operations-and-production/permitting
- https://echo.epa.gov
- https://revenuedata.doi.gov
- https://www.phmsa.dot.gov/data-and-statistics/pipeline/pipeline-incident-20-year-trends
- https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.119
- https://www.doi.gov/orphanwell
- https://www.csb.gov ; https://arlweb.msha.gov/OpenGovernmentData/OGIMSHA.asp ; https://ghgdata.epa.gov
