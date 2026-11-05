# Construction & Engineering

## Overview
Owners, general contractors and engineering firms spend effort on permits, document control (RFIs, submittals, change orders), cost control, payment compliance and safety. Manual work concentrates in reading drawings and specs against codes and contracts, and in compiling evidence for payment, claims and closeout. Most outputs carry legal or contractual consequences, so a licensed or accountable human approves.

## Systems of record, regulations, public datasets
- Systems: project management (Procore, Autodesk Construction Cloud), scheduling (Primavera P6 XER, MS Project), ERP/job cost (Viewpoint, Sage, Oracle), BIM/IFC, permit systems (Accela, Tyler EnerGov), certified-payroll and compliance tools, insurance tracking.
- Regulations/standards: International Building Code and local amendments; OSHA 29 CFR 1926; Davis-Bacon Act (40 U.S.C. 3141 et seq.) and certified payroll (WH-347); AIA A201/G702-G703 payment forms; state lien and prompt-payment statutes; ISO 19650 (BIM information management); NFPA 70.
- Public datasets: DataSF building permits https://data.sfgov.org/Housing-and-Buildings/Building-Permits/i98e-djp9 ; buildingSMART IFC sample files https://github.com/buildingSMART/Sample-Test-Files ; OSHA severe injury reports https://www.osha.gov/severe-injury-reports ; OSHA enforcement https://enforcedata.dol.gov ; SAM.gov wage determinations https://sam.gov/wage-determinations ; BLS CFOI https://www.bls.gov/iif/fatal-injuries-tables.htm .

## Use cases

### 1. Building permit plan-check and resubmittal cycles
- **Tier:** A | Enterprise: pass
- **Enterprise check:** Buyer: city permit department or architect/applicant firms. Systems: permit system, PDF/BIM drawings, code libraries. Regulation: adopted building/fire/zoning codes. Human gate: licensed plans examiner issues corrections and approval.
- **Problem and today's workflow:** Reviewers check sheets against code by hand across departments; applicants cycle through correction rounds.
- **Evidence:** News report of the SF Budget and Legislative Analyst study: SF housing permit processing "a median of 280 days"; Austin 91 days; Seattle "averaged about 133 days" (not 185 as first written, and an average not a median); most projects had "at least three rounds of review". The BLA PDF itself returned an empty page. https://www.yahoo.com/news/articles/f-lagged-behind-other-big-050305002.html [Corrected]
- **Agent design:** Tools: drawing/BIM parser, jurisdiction code search, checklist generator, permit-system comment writer. Steps: extract sheet data, test each code item, draft comment letter with citations. Examiner approves.
- **Open source today:** none found for jurisdiction code plan-check. Adjacent only: jeremylongshore/cad-ai-agent (55 stars, Apache-2.0, not archived, last push 2026-11-03; README read: yes) - DXF/PDF drawing analysis with compliance reports, takeoffs and RFIs; does not check against a jurisdiction adopted code.
- **Demo path:** DataSF permit records plus public IFC samples.
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 2. RFI and submittal triage across drawings, specs and contracts
- **Tier:** A | Enterprise: pass
- **Enterprise check:** Buyer: general contractor. Systems: Procore/ACC, drawings, specs, schedule. Regulation: contractual notice and response clauses. Human gate: project engineer approves RFI/submittal action; engineer of record answers.
- **Problem and today's workflow:** Engineers hunt for conflicts across documents, write RFIs, route and track responses.
- **Evidence:** Construction Dive on the Autodesk/FMI study: bad data "may have caused $1.8 trillion in losses worldwide" and "may be responsible for 14% of avoidable rework, which amounts to $88 billion". The earlier $88.69B is not on the page (it says $88 billion). Vendor survey; not RFI-specific. https://www.constructiondive.com/news/contractors-lost-18-trillion-globally-in-2020-due-to-bad-data-new-report/606939/ [Corrected]
- **Agent design:** Tools: spec/drawing search, prior-RFI lookup, project-system routing. Steps: detect conflict, draft RFI with references, route, track schedule impact. Engineer approves.
- **Open source today:** ibuilder/massing (133 stars, MIT, not archived, last push 2026-11-02; README read: yes) - IFC-native AEC platform with a GC portal incl. RFIs; workflow tooling, adjacent only (no spec/drawing conflict detection). A-SHOJAEI/ConstructDrawingAI (45 stars, NOASSERTION, last push 2026-07-14; README read: yes) mentions RFI drafts from drawings, partial.
- **Demo path:** Public spec sets and drawings with injected conflicts.
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 3. Delay and entitlement analysis for construction claims
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: contractors, owners, claims consultants. Systems: P6/XER schedules, daily logs, correspondence, change orders. Regulation: contract notice provisions; expert admissibility. Human gate: expert/attorney signs.
- **Problem and today's workflow:** Consultants reconstruct schedule updates and assign delay responsibility across thousands of documents.
- **Evidence:** Arcadis dispute-value and duration figures could not be confirmed: ENR returned HTTP 403 and search results for Arcadis editions gave conflicting values. Numbers removed. Reference, not confirmed: https://enr.com/articles/2165-report-international-disputes-lasting-longer-costing-more . [Unconfirmed]
- **Agent design:** Tools: XER parser, document search, timeline builder. Steps: compare schedule updates, link events to evidence, draft windows analysis with citations. Expert reviews every citation.
- **Open source today:** none found (gh search repos "construction delay analysis schedule", stars>=20, not archived: no hits).
- **Demo path:** Synthetic XER pairs and correspondence.
- **Verification:** 2026-11-06, Unconfirmed, repos checked: none listed, search run

### 4. Site safety observation and incident triage
- **Tier:** B | Enterprise: pass
- **Enterprise check:** Buyer: contractor EHS. Systems: inspection apps, photos, incident logs, schedule. Regulation: OSHA 29 CFR 1926 (Subpart M); recordkeeping 1904. Human gate: competent person signs corrective actions.
- **Problem and today's workflow:** Safety managers review photos and reports, write JHAs and track actions.
- **Evidence:** BLS CFOI release (covers 2024, published 19 Feb 2026): "Construction and extraction workers experienced 1,032 fatalities in 2024"; fatal falls, slips and trips among these workers "decreased 7.5 percent to 370 in 2024 from 400 in 2023". The earlier 2023 figures (1,075; 421; 39.2%) are not on the current page. https://www.bls.gov/news.release/cfoi.htm [Corrected]
- **Agent design:** Tools: vision detector, OSHA rule lookup, task assignment. Steps: classify hazards, cite rule, assign action, follow up. Competent person approves.
- **Open source today:** snehilsanyal/Construction-Site-Safety-PPE-Detection (212 stars, no licence, last push 2024-08-18; README read: yes - YOLOv8 PPE detection notebook) and VoxDroid/Construction-Site-Safety-PPE-Detection (29 stars, MIT, last push 2025-12-16; README read: yes - same plus Flask dashboard). Detectors only; adjacent.
- **Demo path:** OSHA severe-injury reports plus public PPE image datasets.
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 5. Quantity takeoff and bid estimate from drawings
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: contractor estimating. Systems: drawings/BIM, cost databases, vendor quotes. Regulation: bid is binding. Human gate: senior estimator signs bid.
- **Problem and today's workflow:** Estimators measure quantities manually and price from quotes.
- **Evidence:** McKinsey 98%/77% megaproject figures could not be confirmed: the PDF and the article page both timed out. Numbers removed. Reference, not confirmed: https://www.mckinsey.com/~/media/McKinsey/Industries/Capital%20Projects%20and%20Infrastructure/Our%20Insights/The%20construction%20productivity%20imperative/The%20construction%20productivity%20imperative.pdf [Unconfirmed]
- **Agent design:** Tools: drawing parser, unit-cost DB, quote lookup, risk simulation. Steps: extract quantities, price, flag assumptions. Estimator approves.
- **Open source today:** A-SHOJAEI/ConstructDrawingAI (45 stars, NOASSERTION licence, not archived, last push 2026-07-14; README read: yes) - turns 2D drawings into detected components and quantity takeoff; covers the takeoff step, not pricing or bid risk.
- **Demo path:** Public sample plan sets.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 6. Pay application and lien-waiver compliance review
- **Tier:** A | Enterprise: pass
- **Enterprise check:** Buyer: GC finance / owner. Systems: ERP job cost, project management, schedule of values, subcontract ledger. Regulation: state prompt-payment and lien statutes; AIA G702/G703. Human gate: project manager and accountant approve payment.
- **Problem and today's workflow:** Staff reconcile subs' billings to SOV, stored materials, change orders and waivers before releasing payment.
- **Evidence:** Siteline blog: "Fifty-nine percent of subs say they wait 46 days or longer to get paid" (vendor survey). The Rabbet/Procore ~$64B claim could not be confirmed and was removed. https://www.siteline.com/blog/youre-not-behind-the-whole-industry-is-built-this-way [Verified]
- **Agent design:** Tools: ERP/subcontract ledger, pay-app parser, waiver validator. Steps: check percent complete vs schedule, retainage, waiver status, draft approval memo. PM approves.
- **Open source today:** none found (gh search repos "pay application lien waiver", stars>=20, not archived: no hits).
- **Demo path:** Synthetic pay apps with seeded math errors.
- **Verification:** 2026-11-06, Verified, repos checked: none listed, search run

### 7. Davis-Bacon certified payroll review
- **Tier:** B | Enterprise: pass
- **Enterprise check:** Buyer: contractors and agencies on federal work. Systems: payroll, SAM.gov wage determinations, WH-347. Regulation: Davis-Bacon Act; 2023 final rule. Human gate: compliance officer signs payroll statements.
- **Problem and today's workflow:** Staff match worker classifications and hours to wage determinations and fringe benefits weekly.
- **Evidence:** HR Dive: "In fiscal year 2023, the DOL recovered over $35.5 million in back wages for construction workers across 2,134 cases" (all WHD construction cases, not Davis-Bacon only). The earlier $32.9M (buildermuse, HTTP 404) was not found. The Davis-Bacon 2023 final rule named in the Enterprise check was not opened. https://www.hrdive.com/news/dol-back-wages-contractors-california/711658/ [Corrected]
- **Agent design:** Tools: payroll export, wage-determination lookup, WH-347 generator. Steps: classify, compare rates, flag shortfalls, draft statement. Officer signs.
- **Open source today:** none found (gh search repos "Davis-Bacon", stars>=20, not archived: no hits).
- **Demo path:** SAM.gov wage determinations plus synthetic payroll.
- **Verification:** 2026-11-06, Corrected, repos checked: none listed, search run

### 8. Change-order pricing and entitlement review
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: GC and owner. Systems: project management, contracts, cost ledger, schedule. Regulation: contract change clauses. Human gate: PM and owner approve.
- **Problem and today's workflow:** Staff verify scope, notice timing, markup and time impact of proposed changes.
- **Evidence:** ASEE paper text: "Contract modifications that increase the contract value from 5 to 10% are expected in most construction projects" (the paper cites another source for this). https://peer.asee.org/change-orders-impact-on-project-cost.pdf [Verified]
- **Agent design:** Tools: contract clause search, pricing database, schedule. Steps: check notice, scope link, markup, draft recommendation. Humans approve.
- **Open source today:** none found (gh search repos "change order construction", stars>=20, not archived: no hits).
- **Demo path:** Synthetic contracts and change logs.
- **Verification:** 2026-11-06, Verified, repos checked: none listed, search run

### 9. Closeout, as-built and O&M documentation turnover
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: GC and owner. Systems: document control, commissioning records, submittal log, warranty tracker. Regulation: contract closeout requirements; permit sign-offs. Human gate: owner's representative accepts.
- **Problem and today's workflow:** Teams assemble warranties, manuals, as-builts and test records against spec requirements before final payment.
- **Evidence:** no reliable figure found. [Unconfirmed]
- **Agent design:** Tools: spec closeout section parser, submittal log, file search. Steps: build required-document list, match files, chase missing, draft turnover package. Owner rep accepts.
- **Open source today:** none found (gh search repos "closeout documents construction", stars>=20, not archived: no hits).
- **Demo path:** Public spec sections and synthetic document folders.
- **Verification:** 2026-11-06, Unconfirmed, repos checked: none listed, search run

## Sources
- https://sfbos.org/sites/default/files/BLA_Post_Entitlement_Permitting_030526.pdf
- https://www.constructiondive.com/news/contractors-lost-18-trillion-globally-in-2020-due-to-bad-data-new-report/606939/
- https://enr.com/articles/2165-report-international-disputes-lasting-longer-costing-more
- https://www.bls.gov/news.release/cfoi.htm
- https://www.mckinsey.com/~/media/McKinsey/Industries/Capital%20Projects%20and%20Infrastructure/Our%20Insights/The%20construction%20productivity%20imperative/The%20construction%20productivity%20imperative.pdf
- https://www.siteline.com/blog/youre-not-behind-the-whole-industry-is-built-this-way
- https://buildermuse.com/labor-wages/davis-bacon-prevailing-wage-federal-construction-bids/
- https://peer.asee.org/change-orders-impact-on-project-cost.pdf
- Dataset links listed in section 2.
