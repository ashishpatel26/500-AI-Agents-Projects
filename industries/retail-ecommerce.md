# Retail & E-commerce

## Overview
Retailers and marketplaces spend manual effort on exceptions: returns that may be fraudulent, disputed card payments, supplier deductions, product-safety and chemical rules, seller verification and recalls. Work concentrates in loss prevention, payments/dispute operations, vendor compliance, trust-and-safety and regulatory-affairs teams. Each case needs evidence pulled from several systems (order, carrier, payment, catalog, ERP), and many have regulatory clocks or financial penalties.

## Systems of record, regulations, public datasets
- **Systems:** OMS, POS, ERP (SAP/Oracle), WMS, product information management (PIM), payment gateway and acquirer portals, card-network dispute portals (Visa/Mastercard), CRM/case management, EDI (850/856/810, retailer vendor portals), marketplace seller-onboarding and listing platforms, supplier/QA document stores.
- **Regulations and standards:** Card-network dispute rules and PCI DSS; EU General Product Safety Regulation (EU) 2023/988 (applies 13 Dec 2024, confirmed on osborneclarke.com) and Digital Services Act (2022); US INFORM Consumers Act (effective 27 June 2023; thresholds and penalty confirmed on ftc.gov); Consumer Product Safety Act (CPSC recalls); California Proposition 65 (Health and Safety Code 25249.5); FSMA Section 204 Food Traceability Rule (2022; 24-hour records confirmed on fda.gov); Lanham Act / DMCA notice-and-takedown; state consumer-protection and biometric privacy laws. Items not individually confirmed against official text: PCI DSS, DSA, Prop 65 code section, Lanham/DMCA, the 27 June 2023 effective date.
- **Public datasets:**
  - Olist Brazilian e-commerce orders: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
  - IEEE-CIS fraud detection (transactions): https://www.kaggle.com/c/ieee-fraud-detection
  - CPSC recalls API: https://www.saferproducts.gov/RestWebServices
  - EU Safety Gate alerts: https://ec.europa.eu/safety-gate-alerts
  - openFDA food enforcement: https://open.fda.gov/apis/food/enforcement/
  - CBP IPR seizure statistics: https://catalog.data.gov/dataset/cbp-intellectual-property-rights-ipr-annual-seizure-statistics

## Use cases

### 1. Returns processing and returns-fraud adjudication
- **Tier:** B (fraud scoring is a model; agent assembles evidence and routes borderline cases). Enterprise: pass
- **Enterprise check:** Buyer is a retailer's returns/loss-prevention team. Systems: OMS, POS receipts, carrier scans, WMS inspection, CRM. Consumer-protection and anti-discrimination law require explainable denials; a reviewer approves denials and account actions.
- **Problem and today's workflow:** Analysts check receipts, serial numbers, return history and condition photos to separate wardrobing, receipt fraud and bracketing from legitimate returns, and decide refund, restock or deny.
- **Evidence:** NRF/Happy Returns: "total returns projected to reach $890 billion in 2024"; "16.9% of their annual sales in 2024 will be returned"; "(93%) of retailers said retail fraud and other exploitive behavior is a significant issue". https://nrf.com/media-center/press-releases/nrf-and-happy-returns-report-2024-retail-returns-total-890-billion . Corrected: the "$101B lost to returns fraud" figure is not on this release; search results attribute it to the earlier NRF/Appriss report on 2023 returns, which was not opened, so it is removed. [Corrected]
- **Agent design:** Tools: OMS/POS lookup, carrier-scan check, image comparison, customer-history query, policy engine. Steps: gather signals, compare returned item to sold item, recommend action with reasons. Human approves any denial or account restriction.
- **Open source today:** none found (gh search repos "returns fraud", stars >= 20, not archived: no results).
- **Demo path:** Olist orders plus synthetic return events with injected mismatches (wrong serial, empty-box).
- **Verification:** 2026-11-06, Corrected, repos checked yes (search only)

### 2. Card-payment chargeback representment
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is a merchant's dispute team or PSP. Systems: OMS, carrier tracking, payment gateway (3DS/AVS logs), CRM, network dispute portals. Card-scheme rules set reason codes and deadlines; PCI DSS governs data; analyst approves high-value submissions.
- **Problem and today's workflow:** Analysts map each reason code to required evidence, pull delivery proof, device/IP data and customer messages, and upload a packet before the response window closes.
- **Evidence:** Vendor blog relaying the Mastercard report: "global chargeback volumes will reach 261 million in 2025"; "By 2028... 324 million"; "Merchants win in 20% of cases" (the same page notes many surveyed merchants report winning over 50% of contested chargebacks, likely larger merchants). https://www.chargebackgurus.com/blog/chargeback-stats-and-insights-from-mastercards-state-of-chargebacks-report . The primary Mastercard/Datos report was not opened, so treat as vendor-relayed. [Verified]
- **Agent design:** Tools: reason-code rulebook, OMS, carrier API, gateway logs, document builder, portal upload. Steps: classify dispute, collect evidence, draft rebuttal, submit. Analyst approves above a value threshold; the agent must never invent evidence and drops disputes it cannot support.
- **Open source today:** none found (gh search repos "chargeback dispute", stars >= 20, not archived: no results).
- **Demo path:** IEEE-CIS transactions with synthetic order and delivery records and a reason-code table.
- **Verification:** 2026-11-06, Verified, repos checked yes (search only)

### 3. EU GPSR marketplace product-safety compliance
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer is a marketplace trust-and-safety/compliance team. Systems: listing database, Safety Gate feed, seller records, case management. Regulation (EU) 2023/988 and DSA notice-and-action; compliance officer approves takedowns.
- **Problem and today's workflow:** Staff monitor Safety Gate alerts, search for matching or identical listings, request missing trader and safety data, and respond to authority orders.
- **Evidence:** The GPSR "is applicable from 13 December this year" (article dated 18 July 2024); orders from market surveillance authorities "must be complied with within two working days from receipt". https://www.osborneclarke.com/insights/navigating-eus-new-gpsr-obligations-are-introduced-online-marketplaces . Corrected: the page does not say marketplaces must register on Safety Gate (it says only that Safety Gate will be made interoperable), so the registration claim is removed. Listing volumes not found. [Corrected]
- **Agent design:** Tools: Safety Gate API, listing search with image match, seller messaging, takedown API. Steps: match alert to listings, draft notices, queue removals. Compliance officer approves removals and seller notices.
- **Open source today:** none found (gh search repos "GPSR product safety", stars >= 20, not archived: no results).
- **Demo path:** Safety Gate alert export plus a synthetic listing catalog with near-duplicate products.
- **Verification:** 2026-11-06, Corrected, repos checked yes (search only)

### 4. Store inventory shrink and record-accuracy investigation
- **Tier:** B. Enterprise: pass
- **Enterprise check:** Buyer is a retailer's loss-prevention/inventory-control team. Systems: POS, ERP inventory, receiving, cycle counts, CCTV/case management. Employment and biometric/CCTV privacy law (e.g. BIPA) apply; HR/legal approve action.
- **Problem and today's workflow:** Analysts trace shrink to theft, process errors, vendor fraud or record errors by joining POS voids, receiving and counts.
- **Evidence:** NRF: "shrink accounted for $112.1 billion in losses" in FY2022, rate 1.6%; "internal and external theft accounted for nearly two-thirds (65%) of retailers' shrink." https://nrf.com/media-center/press-releases/shrink-accounted-over-112-billion-industry-losses-2022-according-nrf . Corrected: the page does not give the separate shares (external 36.15%, internal 28.85%, process errors 27.29%), so those are removed. [Corrected]
- **Agent design:** Tools: anomaly detector output, POS/receiving queries, case-file builder. Steps: pick top variances, drill down, separate record errors from loss, write case file. Humans decide any HR or legal step.
- **Open source today:** none found (gh search repos "shrink loss prevention retail", stars >= 20, not archived: no results).
- **Demo path:** Synthetic store ledger from Olist-style orders with injected receiving errors and void patterns.
- **Verification:** 2026-11-06, Corrected, repos checked yes (search only)

### 5. Counterfeit and IP notice-and-takedown handling for marketplaces
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer is a marketplace IP/trust team or a brand-protection team. Systems: listing platform, rights-holder portals, seller records, case management. DMCA/Lanham Act and DSA procedures with due-process steps; counsel approves repeat-infringer actions.
- **Problem and today's workflow:** Analysts validate rights-holder claims, match listings, remove or reject, and handle counter-notices.
- **Evidence:** The CBP FY2023 IPR fact sheet and the CBP IPR page both returned HTTP 403; a search extract attributed 19,724 seizures, nearly 23M items and over $2.7B MSRP to the fact sheet, but the page was not opened, so the figures are removed. Reference, not confirmed: https://www.cbp.gov/sites/default/files/2024-05/IPR%20FACT%20SHEET%20FISCAL%20YEAR%202023%20PBRB%20APPROVED%20%28508%29_5.29.pdf [Unconfirmed]
- **Agent design:** Tools: claim parser, image/text match, seller history, takedown API, notice drafter. Steps: validate, match, propose action, log. Counsel approves repeat-infringer termination and disputed notices.
- **Open source today:** none found for takedown handling. gokulkumaran03-tbg/Logalyze (52 stars, no licence, not archived, last push 2026-02-02; README not read, description only) is a logo-impersonation detector; adjacent only.
- **Demo path:** Synthetic brand-claim notices matched against a product listing set.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes (description and metadata only for Logalyze)

### 6. Vendor deduction and OTIF fine dispute
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is a consumer-goods supplier's order-to-cash team. Systems: ERP/AR, EDI (856 ASN, 810), retailer vendor portals, carrier PODs. Retailer compliance programs and contracts set fines and dispute windows; finance approves disputes and write-offs.
- **Problem and today's workflow:** Analysts reconcile deductions to POs, ASNs and delivery receipts, and file disputes inside portal deadlines.
- **Evidence:** "Walmart suppliers have been told that on-time and in-full (OTIF) shipments must be 98% complete effective Sept. 15" and "Suppliers not meeting the new guidance will be fined 3% of the cost of goods" (article dated Sept 3, 2020). https://talkbusiness.net/2020/09/walmart-demands-all-suppliers-comply-with-98-on-time-in-full-shipment-rule/ . This is the 2020 announcement; current rules were not checked. [Verified]
- **Agent design:** Tools: AR deduction feed, EDI history, carrier POD lookup, portal upload. Steps: match deduction, test validity, assemble proof, file. Finance approves each dispute.
- **Open source today:** none found (gh search repos "vendor deduction", stars >= 20, not archived: no results).
- **Demo path:** Synthetic PO/ASN/POD set with late and short shipments and a deduction ledger.
- **Verification:** 2026-11-06, Verified, repos checked yes (search only)

### 7. Product recall execution and effectiveness tracking
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is a retailer's quality/regulatory team. Systems: POS, loyalty/CRM, ERP lot data, supplier portals, regulator portals. CPSC and FDA obligations require notices and records; recall coordinator approves communications.
- **Problem and today's workflow:** Teams map recalled SKUs and lots to stores and customers, block sales at POS, send notices and track returns and regulator reports.
- **Evidence:** CPSC commissioner statement: "announced more than 300 recalls in fiscal year 2023, a 20 percent increase over the previous year"; its table lists 312 recalls for FY2023 versus 260 for FY2022. https://www.cpsc.gov/About-CPSC/Commissioner/Peter-A-Feldman/Statement/Statement-of-Commissioner-Peter-A-Feldman-Record-Recall-Numbers-Reflect-Return-on-Investment-for-American-Consumers . [Verified]
- **Agent design:** Tools: recall feed, lot-to-store mapping, POS block API, customer notice generator, return tracker. Steps: scope, block, notify, report progress. Coordinator approves notices and regulator submissions.
- **Open source today:** none found (gh search repos "product recall", stars >= 20, not archived: only an unrelated playlist repo).
- **Demo path:** CPSC recall API joined to synthetic sales by SKU and lot.
- **Verification:** 2026-11-06, Verified, repos checked yes (search only)

### 8. High-volume seller verification (INFORM Consumers Act)
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is an online marketplace compliance team. Systems: seller onboarding, payments/payout, KYC providers, tax-ID checks. INFORM Act (2023) with FTC and state enforcement; compliance lead approves suspensions.
- **Problem and today's workflow:** Analysts detect sellers crossing 200 sales / $5,000 revenue, collect bank, tax and contact data, verify it, require annual certification and suspend non-responders.
- **Evidence:** FTC: high-volume seller means "200 or more separate sales or transactions of new or unused consumer products" and $5,000 or more in gross revenues in a 12-month period within 24 months; the marketplace has 10 days to collect and 10 days to verify; civil penalties of "$53,088 per violation" (updated January 2025). https://www.ftc.gov/INFORMAct . The earlier "Temu $2M (Sept 2025)" enforcement note could not be confirmed on any page opened and is removed. [Verified]
- **Agent design:** Tools: sales-threshold monitor, KYC/tax APIs, seller messaging, suspension API. Steps: detect, request, verify, certify, escalate. Compliance lead approves suspensions and mismatch decisions.
- **Open source today:** none found (gh search repos "INFORM Consumers Act", stars >= 20, not archived: no results).
- **Demo path:** Synthetic seller transaction ledger with sellers crossing thresholds and bad tax IDs.
- **Verification:** 2026-11-06, Verified, repos checked yes (search only)

### 9. Product chemical-restriction and Prop 65 compliance
- **Tier:** B. Enterprise: needs figure
- **Enterprise check:** Buyer is a retailer's regulatory/product-compliance team. Systems: PIM, supplier test reports, ERP, labeling systems. Prop 65 warning duty and 60-day notice litigation; compliance lead approves warnings and product holds.
- **Problem and today's workflow:** Analysts read supplier lab reports, compare substances to Prop 65 and other restricted lists, add warnings and respond to notices.
- **Evidence:** The cited Sheppard Mullin page returned HTTP 429 on every attempt. A search extract suggested different counts than the earlier note (e.g. 4,142 notices in 2023 and 5,398 in 2024) but no page was opened, so no number is kept. The earlier "3,170 in 2022 / record in 2023" claim is not supported by anything seen. Reference, not confirmed: https://www.sheppard.com/insights/blogs/proposition-65-2023-in-review [Unconfirmed]
- **Agent design:** Tools: lab-report extractor, list matcher, PIM warning field update, notice response drafter. Steps: extract, compare, recommend warning or hold. Compliance lead approves every warning change.
- **Open source today:** none found (gh search repos "Prop 65", stars >= 20, not archived: no results).
- **Demo path:** Prop 65 chemical list with synthetic lab reports.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes (search only)

### 10. FSMA 204 food traceability record assembly
- **Tier:** B. Enterprise: needs figure
- **Enterprise check:** Buyer is a grocery retailer or food distributor. Systems: WMS/ERP lot data, supplier EDI/portals, receiving logs. FDA Food Traceability Rule requires key data elements and records within 24 hours; QA lead approves submissions.
- **Problem and today's workflow:** Staff chase suppliers for lot and location data and build trace records during outbreaks.
- **Evidence:** FDA rule page: records "must be made available to the FDA within 24 hours after a request is made" (with an exception for "within a reasonable time to which the FDA has agreed"). Corrected: the page says FDA proposed a 30-month extension "to July 20, 2028" (original date January 20, 2026) and that Congress directed FDA not to enforce the rule before that date; the page itself is internally inconsistent and I did not confirm a finalised extension, so "compliance date moved to July 20, 2028" is softened. https://www.fda.gov/food/food-safety-modernization-act-fsma/fsma-final-rule-requirements-additional-traceability-records-certain-foods [Corrected]
- **Agent design:** Tools: lot/receiving query, supplier data requests, KDE validator, record packager. Steps: trace forward/back, find gaps, request data, package. QA lead approves what goes to FDA.
- **Open source today:** none found (gh search repos "FSMA 204 traceability", stars >= 20, not archived: no results).
- **Demo path:** openFDA food enforcement data with synthetic shipping events.
- **Verification:** 2026-11-06, Corrected, repos checked yes (search only)

## Sources
- https://nrf.com/media-center/press-releases/nrf-and-happy-returns-report-2024-retail-returns-total-890-billion
- https://www.chargebackgurus.com/blog/chargeback-stats-and-insights-from-mastercards-state-of-chargebacks-report
- https://www.osborneclarke.com/insights/navigating-eus-new-gpsr-obligations-are-introduced-online-marketplaces
- https://nrf.com/media-center/press-releases/shrink-accounted-over-112-billion-industry-losses-2022-according-nrf
- https://www.cbp.gov/sites/default/files/2024-05/IPR%20FACT%20SHEET%20FISCAL%20YEAR%202023%20PBRB%20APPROVED%20%28508%29_5.29.pdf (reference, not confirmed)
- https://talkbusiness.net/2020/09/walmart-demands-all-suppliers-comply-with-98-on-time-in-full-shipment-rule/
- https://www.cpsc.gov/About-CPSC/Commissioner/Peter-A-Feldman/Statement/Statement-of-Commissioner-Peter-A-Feldman-Record-Recall-Numbers-Reflect-Return-on-Investment-for-American-Consumers
- https://www.ftc.gov/INFORMAct
- https://www.sheppard.com/insights/blogs/proposition-65-2023-in-review (reference, not confirmed)
- https://www.fda.gov/food/food-safety-modernization-act-fsma/fsma-final-rule-requirements-additional-traceability-records-certain-foods
- Datasets: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce ; https://www.kaggle.com/c/ieee-fraud-detection ; https://www.saferproducts.gov/RestWebServices ; https://ec.europa.eu/safety-gate-alerts ; https://open.fda.gov/apis/food/enforcement/ ; https://catalog.data.gov/dataset/cbp-intellectual-property-rights-ipr-annual-seizure-statistics
