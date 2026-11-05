# Logistics & Supply Chain

## Overview
Logistics spends most of its manual effort on documents that must agree with each other (commercial invoice, packing list, bill of lading, carrier invoice, customs entry) and on rules that change often (tariff actions, sanctions lists, carrier tariffs, FMC and FMCSA rules). Work concentrates in customs brokerage, trade-compliance teams, freight audit and payment, claims desks and carrier-management teams. Most decisions carry a statutory liability (penalties, bond claims, loss of refund rights), so a human sign-off is normal.

## Systems of record, regulations, public datasets
- **Systems:** TMS (e.g. Oracle OTM, SAP TM, Blue Yonder), WMS, ERP (SAP, Oracle, NetSuite) AP and purchasing, customs brokerage/ABI platforms (ACE filing), global trade management (GTM), freight-audit-and-pay platforms, EDI (204/210/214/856), carrier portals, container-status feeds, restricted-party screening tools, document stores.
- **Regulations and standards:** 19 USC 1484 and 1592 (reasonable care, penalties); 19 CFR Part 149 (Importer Security Filing); Uyghur Forced Labor Prevention Act (2021); FMC detention and demurrage billing rule (final rule, Feb 2024; most provisions effective May 28, 2024, confirmed on fmc.gov); 49 USC 14706 (Carmack) and 49 CFR Part 370 (claims; Part 370 text confirmed on law.cornell.edu); 31 CFR Part 560 and OFAC regimes, Export Administration Regulations (15 CFR 730-774); 49 CFR Parts 171-180 (hazmat) and IATA Dangerous Goods Regulations; 19 USC 1313 (drawback, as amended by TFTEA 2015); FMCSA registration rules (49 CFR Parts 365, 387). Regulations not individually confirmed against official text: 19 USC 1484/1592, 19 CFR 149, 31 CFR 560, EAR, 49 CFR 171-180, 19 USC 1313, 49 CFR 365/387.
- **Public datasets:**
  - USITC HTS: https://hts.usitc.gov/ ; CBP CROSS rulings: https://rulings.cbp.gov/
  - DHS UFLPA Entity List: https://www.dhs.gov/uflpa-entity-list
  - Treasury Consolidated Screening List: https://www.trade.gov/consolidated-screening-list
  - FMCSA carrier registration/safety data: https://data.transportation.gov (search "FMCSA")
  - PHMSA hazmat incident data: https://www.phmsa.dot.gov/hazmat-program-management-data-and-statistics/data-operations/incident-statistics
  - CBP IPR seizure statistics: https://catalog.data.gov/dataset/cbp-intellectual-property-rights-ipr-annual-seizure-statistics

## Use cases

### 1. Customs tariff (HTS) classification for import entries
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer is a customs broker or importer trade-compliance team. Systems: ERP item master, GTM/broker platform, ACE entry filing, CBP CROSS rulings. Regulated under 19 USC 1484/1592 (reasonable care); a licensed broker or importer signs off. Per-SKU rationale is retained for audit.
- **Problem and today's workflow:** A classifier reads product specs, applies the General Rules of Interpretation, searches CROSS rulings and section/chapter notes, then checks overlays such as Section 301 or 232 actions. Backlogs build when new SKUs or tariff actions arrive; errors flow into duty underpayment and penalties.
- **Evidence:** The CBP FY2023 trade fact sheet (entry volume and import value) could not be opened (HTTP 403) and the secondary pages opened did not show the entry count, so the earlier entry/dollar figure is removed. No reliable per-error cost figure found. Reference, not confirmed: https://cbp.gov/sites/default/files/2024-06/cbp_fy_2023_trade_fact_sheet_06.2024.pdf [Unconfirmed]
- **Agent design:** Tools: item-master lookup, HTS search, CROSS search, tariff-action overlay table, prior-classification memory. Steps: extract attributes, propose 2-3 candidate codes with GRI reasoning and ruling citations, check overlays, flag low-confidence SKUs. A licensed broker approves each new classification before filing; changes are logged with the rationale.
- **Open source today:** none found (gh search repos "HTS classification" and "customs tariff classification", stars >= 20, not archived: no results).
- **Demo path:** Use the USITC HTS CSV and CROSS ruling texts as the corpus; build 50 synthetic product descriptions from rulings and score top-3 candidate agreement against the ruling's code.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes (search only, no repos listed)

### 2. Freight invoice audit and accessorial-charge dispute
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer is a shipper's logistics/AP team or a third-party freight-audit provider. Systems: TMS, ERP AP, EDI 210 carrier invoices, contract rate tables, BOL/POD images, carrier portals. Needs an audit trail for payment and claims; an analyst approves each dispute before it goes to the carrier.
- **Problem and today's workflow:** Auditors match carrier invoices (LTL, parcel, truckload) to contract rates, accessorial rules, BOL weights and proof of delivery, then email carriers to dispute wrong detention, liftgate, reweigh or duplicate charges. Dispute deadlines are carrier-specific and many small variances are never chased.
- **Evidence:** The cited vendor page (opened) contains no invoice error-rate statistic, so the earlier "5-10% of invoices" figure is removed; no primary source traced. Reference, not confirmed: https://gingercontrol.com/blog/freight-invoice-audit-guide [Unconfirmed]
- **Agent design:** Tools: contract/tariff retrieval, TMS shipment lookup, POD/BOL reader, carrier-portal dispute submission. Steps: match invoice to shipment and rate, classify variance, assemble evidence, draft dispute. Analyst approves any dispute above a value threshold; the agent never files without evidence attached.
- **Open source today:** none found for audit agents. Mohaby/freight-invoice-audit (1 star, no licence, last push 2025-10-10, not archived; README read: yes) is a Flask dashboard that detects duplicates and rate mismatches; adjacent only, a student demo.
- **Demo path:** Generate synthetic invoices from a public LTL class/rate table with injected errors (duplicate, wrong accessorial, weight bump) and measure recall of injected errors.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 3. UFLPA supply-chain tracing for detained shipments
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is an importer's compliance/legal team. Systems: ERP purchasing and BOM, supplier portals, customs broker platform, CBP detention notices, DHS UFLPA Entity List. Rebuttable presumption of forced labor under UFLPA (2021) puts the burden on the importer; counsel signs the submission.
- **Problem and today's workflow:** After a detention, analysts chase POs, mill and farm records, transport documents and mass-balance data across supplier tiers and languages, then assemble a binder for CBP within tight windows.
- **Evidence:** "a total of 8,142 shipments at an estimated value of US$3.17 billion have been detained or denied entry under the act" (June 2022 to March 2024, attributed to CBP data). https://www.visualcompliance.com/blog/escalation-in-forced-labor-enforcement-how-to-comply-with-the-uflpa-entity-list/ . Corrected: the STR article originally cited covers April-June 2023 (1,182 stopped shipments, $586M) and does not support the earlier "about 1,500 shipments / $830M in Q1 2024" figure, which is removed. CBP's own dashboard was not opened; the cumulative figure is a secondary-source quote. [Corrected]
- **Agent design:** Tools: BOM/PO retrieval, supplier-document inbox with translation, Entity List matcher, mass-balance calculator. Steps: build tier map, flag gaps, request documents, reconcile quantities, draft the response. Counsel approves; any unsupported provenance claim is blocked from the draft.
- **Open source today:** none found (gh search repos "UFLPA forced labor", stars >= 20, not archived: no results).
- **Demo path:** Synthetic BOM for a solar-module or cotton-apparel product with 3 tiers; plant a supplier name that fuzzy-matches an Entity List entry and test that the agent escalates instead of clearing it.
- **Verification:** 2026-11-06, Corrected, repos checked yes (search only)

### 4. Ocean demurrage and detention (D&D) invoice validation and dispute
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer is a shipper, NVOCC or forwarder. Systems: TMS/visibility feeds, carrier and terminal invoices, container events (gate-out, return), contracts. FMC billing rule makes defective invoices non-payable; a billing specialist approves disputes.
- **Problem and today's workflow:** Staff compare invoice dates to free time, port closures, empty-return availability and gate events, then request waivers or refunds inside short windows.
- **Evidence:** FMC final rule: invoices "can only be issued to either" the contracting party or the consignee, "within 30 calendar days from when charges were last incurred"; an invoice omitting required information "eliminates any obligation of the billed party to pay"; billed parties have "at least 30 calendar days" for mitigation, refund or waiver requests; most of the rule takes effect May 28, 2024 (the invoice-contents section has a separate date after OMB approval). https://www.fmc.gov/fmc-publishes-final-rule-on-detention-and-demurrage-billing-practices/ . Industry-wide charge volume not found. [Verified]
- **Agent design:** Tools: invoice parser, event-timeline API, contract free-time calculator, FMC rule checker. Steps: recompute chargeable days, check timeliness and required fields, draft dispute with event evidence. Specialist approves every dispute before sending.
- **Open source today:** none found (gh search repos "demurrage detention", stars >= 20, not archived: no results).
- **Demo path:** Synthetic container-event timelines plus invoices; inject late invoices, wrong billed party, and closed-terminal days; score detection.
- **Verification:** 2026-11-06, Verified, repos checked yes (search only)

### 5. Freight cargo loss-and-damage claims handling
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer is a shipper claims desk or a carrier's claims department. Systems: TMS, claims system, BOL/POD/inspection photos, carrier liability terms, insurer portal. Regulated by 49 USC 14706 (Carmack) and 49 CFR Part 370; claims have an audit trail and a claims manager approves payment or denial.
- **Problem and today's workflow:** Claims staff gather BOL notations, photos, invoices and repair quotes, compute value, file with the carrier, and track acknowledgement and payment clocks by hand.
- **Evidence:** 49 CFR 370.5: carrier must acknowledge a claim "within 30 days after the date of its receipt"; 370.9: pay, decline or make a firm compromise offer within 120 days, then written status notices at the end of "each succeeding 60-day period". The 60-day figure that conflicted in the earlier note is the status-update interval, not the acknowledgement period. Corrected: the 9-month minimum filing period is in 49 USC 14706(e) ("a period of less than 9 months for filing a claim"), not Part 370, which defers to the bill of lading (370.3). Sources: https://www.law.cornell.edu/cfr/text/49/370.5 ; https://www.law.cornell.edu/cfr/text/49/370.9 ; https://www.law.cornell.edu/uscode/text/49/14706 . No reliable claims-dollar figure found. [Corrected]
- **Agent design:** Tools: TMS shipment and POD retrieval, photo analysis, carrier-terms lookup, claim form generator, deadline tracker. Steps: validate claim completeness, compute damages, file, chase on clock. Claims manager approves filing and any settlement.
- **Open source today:** none found (gh search repos "freight claims", stars >= 20, not archived: no results).
- **Demo path:** Synthetic claim packets (BOL with exceptions, photos from a public damaged-goods image set, invoices) and a deadline simulator.
- **Verification:** 2026-11-06, Corrected, repos checked yes (search only)

### 6. Importer Security Filing (ISF) and entry document reconciliation
- **Tier:** B (extraction and rules do the core; agent resolves mismatches). Enterprise: pass
- **Enterprise check:** Buyer is a broker or NVOCC. Systems: broker platform (ACE/ISF filing), supplier commercial invoices, packing lists, booking/BOL, ERP POs. 19 CFR Part 149 requires 10 importer data elements 24h before loading; broker or importer signs off.
- **Problem and today's workflow:** Clerks re-key and compare invoice, packing list, PO and BOL data, chase suppliers for missing HTS, manufacturer and consolidator details, and fix late or mismatching filings.
- **Evidence:** "Failure to comply with the ISF requirements can result in liquidated damages of $5,000 per violation." https://www.ghy.com/trade-talk/us-importer-security-filing-isf/ (broker commentary; controlling text is 19 CFR Parts 149 and 113, not opened). The earlier note of a conflicting $10,000 figure was not reproduced on the page opened and is dropped. [Verified]
- **Agent design:** Tools: document OCR/extraction, PO match, supplier-contact email, ISF/ACE submission API. Steps: extract, cross-check 10+2 fields, request fixes, prepare filing. Broker reviews exceptions and approves submission.
- **Open source today:** none found (gh search repos "importer security filing", stars >= 20, not archived: only unrelated hits).
- **Demo path:** Synthetic invoice/packing-list/BOL PDFs with deliberate mismatches (quantity, country of origin, consignee).
- **Verification:** 2026-11-06, Verified, repos checked yes (search only)

### 7. Restricted-party and export-control screening alert adjudication
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is a forwarder, exporter or logistics provider. Systems: GTM/screening engine, ERP customer/vendor masters, TMS, ownership data. OFAC and BIS rules (31 CFR, EAR) require documented decisions; a compliance officer approves releases and blocks.
- **Problem and today's workflow:** Screening produces large volumes of fuzzy-name hits; analysts check addresses, ownership percentages and end use to clear or escalate, logging reasons.
- **Evidence:** The Federal Register 2025 inflation-adjustment table lists $377,700 as the IEEPA maximum civil penalty (up from $368,136), effective January 15, 2025 (50 U.S.C. 1705). https://www.govinfo.gov/content/pkg/FR-2025-01-15/html/2025-00786.htm . Corrected: the "or twice the transaction value" wording is not on that page and is removed. [Corrected]
- **Agent design:** Tools: screening-list lookup, corporate-registry and ownership search, shipment history, 50%-rule calculator. Steps: gather identifiers, compare, write disposition. Compliance officer approves every release; the agent may not auto-clear on weak matches.
- **Open source today:** Divine16/Sanctions-screening-benchmark (33 stars, MIT, not archived, last push 2026-08-13; README read: yes). It is a reproducible benchmark of name-screening recall across 18 name-variation classes; adjacent only, not an adjudication agent.
- **Demo path:** Treasury Consolidated Screening List plus synthetic shipment parties with perturbed names; measure false-clear rate.
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 8. Dangerous goods shipping-document compliance check
- **Tier:** B. Enterprise: needs figure
- **Enterprise check:** Buyer is a forwarder, 3PL or shipper. Systems: TMS/WMS, SDS repository, booking systems, carrier DG acceptance portals. 49 CFR Parts 171-180 and IATA DGR require correct class, packing group, marking and declaration; a certified DG specialist signs the declaration.
- **Problem and today's workflow:** Specialists compare SDS data to the shipper's declaration, UN number, packing instruction and carrier limits, and reject or correct bookings.
- **Evidence:** no reliable figure found. The PHMSA incident-statistics page returned HTTP 403, so no national damage total could be checked. Reference, not confirmed: https://www.phmsa.dot.gov/hazmat-program-management-data-and-statistics/data-operations/incident-statistics [Unconfirmed]
- **Agent design:** Tools: SDS parser, UN/hazmat table lookup, carrier DG rules, booking system. Steps: extract section 14 data, validate declaration, list defects. DG specialist approves; agent cannot sign declarations.
- **Open source today:** none found (gh search repos "dangerous goods shipping", stars >= 20, not archived: no results).
- **Demo path:** Public SDS PDFs with synthetic declarations containing seeded errors (wrong packing group, missing technical name).
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes (search only)

### 9. Carrier onboarding and fraud vetting
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is a broker or shipper carrier-management team. Systems: TMS carrier master, FMCSA registration data, insurance certificates, bank details, load boards. Duty of care under broker-registration and insurance rules (49 CFR Parts 365, 387); a carrier-management lead approves.
- **Problem and today's workflow:** Staff check MC/DOT authority, insurance, address, phone and bank-change requests by hand to spot identity-theft carriers and double brokering.
- **Evidence:** Verisk CargoNet figures as quoted by Risk & Insurance: "cargo theft incidents rose to 3,625 in 2024, up from 2,852 in 2023"; estimated loss value rose "to $454.9 million in 2024"; average value per theft "$202,364". https://riskandinsurance.com/cargo-theft-losses-hit-record-455m-in-2024/ . The Verisk release page itself did not render the figures. This is cargo theft in general, not specifically carrier-identity fraud. [Verified]
- **Agent design:** Tools: FMCSA lookup, insurer verification, domain/phone checks, TMS history. Steps: verify identity, compare against prior records, score red flags, hold the carrier. Lead approves onboarding and any bank-detail change.
- **Open source today:** none found (gh search repos "freight broker fraud", stars >= 20, not archived: no results).
- **Demo path:** FMCSA public registration data with synthetic cloned-carrier records.
- **Verification:** 2026-11-06, Verified, repos checked yes (search only)

### 10. Duty drawback claim preparation
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is an importer/exporter finance or trade team. Systems: ERP inventory and export records, ACE import entries, bonded records. 19 USC 1313 as amended; CBP audits; a broker or trade lead certifies the claim.
- **Problem and today's workflow:** Analysts match imports to later exports or destruction by part number, quantity and date across years, then compile claims within a five-year window.
- **Evidence:** GAO: the drawback program refunds "about $1 billion a year"; CBP's August 2023 estimate was that over four years it "denied $163,370,381" in improper refunds. https://www.gao.gov/products/gao-20-182 . [Verified]
- **Agent design:** Tools: ACE entry export, ERP export history, matching engine. Steps: match, validate eligibility, build claim packages. Trade lead approves; unmatched lines stay out of the claim.
- **Open source today:** none found (gh search repos "duty drawback", stars >= 20, not archived: no results).
- **Demo path:** Synthetic import and export ledgers with partial overlaps and scrap/destruction events.
- **Verification:** 2026-11-06, Verified, repos checked yes (search only)

## Sources
- https://cbp.gov/sites/default/files/2024-06/cbp_fy_2023_trade_fact_sheet_06.2024.pdf (reference, not confirmed)
- https://gingercontrol.com/blog/freight-invoice-audit-guide (opened; no figure)
- https://www.visualcompliance.com/blog/escalation-in-forced-labor-enforcement-how-to-comply-with-the-uflpa-entity-list/
- https://www.fmc.gov/fmc-publishes-final-rule-on-detention-and-demurrage-billing-practices/
- https://www.law.cornell.edu/cfr/text/49/370.5 ; https://www.law.cornell.edu/cfr/text/49/370.9 ; https://www.law.cornell.edu/uscode/text/49/14706
- https://www.ghy.com/trade-talk/us-importer-security-filing-isf/
- https://www.govinfo.gov/content/pkg/FR-2025-01-15/html/2025-00786.htm
- https://riskandinsurance.com/cargo-theft-losses-hit-record-455m-in-2024/
- https://www.gao.gov/products/gao-20-182
- https://hts.usitc.gov/ ; https://rulings.cbp.gov/ ; https://www.dhs.gov/uflpa-entity-list ; https://www.trade.gov/consolidated-screening-list ; https://data.transportation.gov
- https://www.phmsa.dot.gov/hazmat-program-management-data-and-statistics/data-operations/incident-statistics (reference, not confirmed)
- https://catalog.data.gov/dataset/cbp-intellectual-property-rights-ipr-annual-seizure-statistics
