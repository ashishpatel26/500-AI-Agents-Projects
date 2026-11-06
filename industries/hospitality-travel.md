# Hospitality & Travel

## Overview
Airlines, hotels, tour operators and corporate travel managers spend effort on irregular operations, passenger-rights claims, settlement and reconciliation between carriers, agencies and platforms, and compliance reporting. Manual work concentrates in cross-system case handling (PSS, PMS, GDS, payments) where rules differ by jurisdiction and every payout or rejection must be explainable.

## Systems of record, regulations, public datasets
- **Systems:** Airline PSS/DCS (Amadeus Altea, Sabre), operations control (crew/aircraft), WorldTracer, GDS/NDC, IATA BSPlink, hotel PMS (Opera), channel managers/OTA extranets, payment processors, TMC/expense tools (Concur).
- **Regulation/standards:** EU Regulation 261/2004 and UK261; US DOT refund rule (2024); Montreal Convention; Regulation (EU) 2024/1028 (short-term rentals, applies 20 May 2026); IATA Resolution 850m (ADMs); EU ETS aviation and CORSIA MRV; PCI-DSS and card-network dispute rules; FDA Food Code; GDPR.
- **Public datasets:** BTS on-time/cancellation data https://www.transtats.bts.gov/ ; DOT Air Travel Consumer Report https://www.transportation.gov/airconsumer ; Eurocontrol Aviation Intelligence data https://ansperformance.eu/ ; Inside Airbnb listings https://insideairbnb.com/get-the-data/ ; FDA/state restaurant inspection open data (e.g., NYC https://data.cityofnewyork.us/ ).

## Use cases

### 1. Airline irregular operations (IROPS) passenger rebooking
- **Tier:** A Enterprise: pass
- **Enterprise check:** Buyer: airline OCC/customer ops. Systems: PSS, crew/aircraft recovery, partner inventory, hotel/meal vouchers. Regulation: DOT refund rule, EU261 care duties, crew duty limits. Human gate: duty manager approves policy exceptions and mass rebook plans.
- **Problem and today's workflow:** After cancellations, agents and controllers rebook thousands of passengers across flights, partners and hotels under fare and entitlement rules.
- **Evidence:** Checkbook (opened): "1.2 percent of the 16.3 million scheduled flights departing from U.S. airports - about 195,600 flights - were canceled" in 2023 per DOT; automatic refunds "beginning Oct. 28" (2024, article dated 30 Oct 2024). Vendor cost estimates not checked. https://www.checkbook.org/national/consumers-notebook/articles/Here-Is-What-Airlines-Must-Do-If-Your-Flight-Is-Canceled-or-Delayed-7739 [Verified]
- **Agent design:** Reads disruption feed and PNRs, calls rebook-options and entitlement tools, drafts offers and notifications. Manager approves exceptions; crew legality stays in recovery system.
- **Open source today:** none found (gh search "flight rebooking disruption", stars>=20, not archived: no relevant hit).
- **Demo path:** BTS cancellation data plus synthetic PNRs.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 2. EU261/UK261 and DOT compensation claim adjudication
- **Tier:** A Enterprise: needs figure (dated enforcement event, no claim volume or dollar figure)
- **Enterprise check:** Buyer: airline customer relations. Systems: flight ops logs, weather/maintenance records, CRM. Regulation: EU261, UK CAA enforcement, GDPR. Human gate: reviewer approves every rejection.
- **Problem and today's workflow:** Handlers establish arrival delay, distance band and "extraordinary circumstances" evidence, then pay or reject with reasons.
- **Evidence:** ch-aviation (opened, 24 Feb 2017): UK CAA announced enforcement action against five carriers (American Airlines, Emirates, Etihad, Singapore Airlines, Turkish Airlines) "for denying passengers compensation for delayed flights which originated in the European Union". The EUR 250/400/600 tiers are not on this page and were not checked against Regulation 261/2004, so they are unconfirmed. https://www.ch-aviation.com/news/53601-uks-caa-sanctions-five-carriers-for-pax-rights-violations [Corrected]
- **Agent design:** Pulls actual times, applies tiers and exceptions, drafts decision letters with citations. Human signs rejections.
- **Open source today:** none found (gh search "EU261 compensation", stars>=20, not archived: no relevant hit).
- **Demo path:** BTS/Eurocontrol delays with synthetic claims.
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 3. Short-term rental registration compliance (EU 2024/1028)
- **Tier:** B Enterprise: needs figure
- **Enterprise check:** Buyer: platform, property manager or tourism authority. Systems: national registers, listing databases. Regulation: Regulation (EU) 2024/1028 from 20 May 2026. Human gate: review before suspension.
- **Problem and today's workflow:** Staff match listings to registration numbers and flag invalid ones across jurisdictions.
- **Evidence:** Austrian ministry page (opened): the regulation applies from 20 May 2026 (Austria will initially not implement it in any federal province); each unit gets a registration number shown in listings; platforms transmit booking data to authorities monthly. The page does not mention random validity checks, so that claim is unconfirmed; the date is also confirmed by EP Legislative Observatory search excerpts. https://www.bmwet.gv.at/en/Topics/tourism/tourism-service-and-contacts/str_regulation.html [Corrected]
- **Agent design:** Entity-resolve addresses, validate numbers against registers, draft host notices. Reviewer approves delisting.
- **Open source today:** none found (gh search "short-term rental registration", stars>=20, not archived: no relevant hit).
- **Demo path:** Inside Airbnb listings with synthetic register.
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 4. Baggage irregularity tracing and claims (WorldTracer)
- **Tier:** A Enterprise: pass
- **Enterprise check:** Buyer: airline/handler baggage services. Systems: WorldTracer, DCS bag tags, claims/finance. Regulation: Montreal Convention liability limits. Human gate: claims handler approves payments.
- **Problem and today's workflow:** Agents match files, contact passengers, authorize delivery and settle claims.
- **Evidence:** Travel Weekly (opened, 12 Jun 2025, citing SITA): "The total number of mishandled bags fell to 33.4 million"; rate "dropped to 6.3 bags per 1,000 passengers"; mishandling "cost the aviation industry an estimated $5 billion". https://travelweekly.co.uk/news/mishandled-bags-cost-airlines-5bn-in-2024 [Verified]
- **Agent design:** Matches tracing files to scans, drafts delivery orders and claim assessments. Handler approves.
- **Open source today:** none found (gh search "baggage claims airline", stars>=20, not archived: no relevant hit).
- **Demo path:** Synthetic WorldTracer-style records.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 5. BSP settlement and agency debit memo (ADM) dispute handling
- **Tier:** A Enterprise: needs figure
- **Enterprise check:** Buyer: airline revenue accounting or travel agency. Systems: BSPlink, ticketing/PSS, GDS. Regulation: IATA Resolution 850m. Human gate: accountant approves disputes/acceptances.
- **Problem and today's workflow:** Staff examine ADMs against fare rules and tickets and file disputes within short windows.
- **Evidence:** The Cathay agents policy page timed out twice, so the 60-day response window is unconfirmed and removed. No BSP volume figure was found. Reference, not confirmed: https://www.cxagents.com/content/cathay-agents/worldwide/en_DE/policies/reservation-ticketing/adm-acm-policy.html . [Unconfirmed]
- **Agent design:** Retrieves ticket/fare data, tests ADM reason, drafts dispute. Accountant files.
- **Open source today:** none found (gh search "BSP ADM airline", stars>=20, not archived: no relevant hit).
- **Demo path:** Synthetic tickets and ADMs.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 6. Aviation emissions MRV (EU ETS / CORSIA)
- **Tier:** B Enterprise: needs figure
- **Enterprise check:** Buyer: airline sustainability/finance. Systems: flight ops fuel data, registries. Regulation: EU ETS MRV, CORSIA (19-month MRV cycle). Human gate: verifier and compliance lead sign.
- **Problem and today's workflow:** Analysts reconcile fuel uplift and flight lists into annual emissions reports.
- **Evidence:** ICAO's April 2025 CORSIA newsletter (search excerpt; the cited ICAO PDF returned 403): aeroplane operators and verification bodies were to submit verified 2024 emissions reports to States by 30 April 2025. The "19-month MRV cycle" wording (also in the Enterprise check line above) was not found and is unconfirmed. No dollar impact found. https://www.icao.int/sites/default/files/APAC/Meetings/2025/2025%20CORSIASAP/Presentations/CORSIA_Agenda-Item-2_CORSIA-Implementation-Elements.pdf [Corrected]
- **Agent design:** Reconciles fuel records to flights, flags gaps, drafts report. Verifier signs.
- **Open source today:** none found (gh search "emissions MRV aviation", stars>=20, not archived: no relevant hit).
- **Demo path:** Synthetic flight/fuel logs.
- **Verification:** 2026-11-06, Corrected (search excerpt), repos checked yes

### 7. Multi-site food-safety compliance and inspection remediation
- **Tier:** B Enterprise: needs figure (public-health counts, no operator-level dollar figure)
- **Enterprise check:** Buyer: hotel/restaurant group. Systems: temperature sensors, inspection reports, QA tools. Regulation: FDA Food Code, HACCP. Human gate: food-safety manager closes actions.
- **Problem and today's workflow:** Managers track logs and inspection findings across sites.
- **Evidence:** CDC page (opened) does not contain the 48 million / 128,000 figures. It says the most common foodborne pathogens cause "an estimated 9.9 million illnesses, 53,000 hospitalizations, and 931 deaths" yearly and that "More than half of all U.S. foodborne outbreaks are associated with restaurants". https://www.cdc.gov/restaurant-food-safety [Corrected]
- **Agent design:** Ingests logs and inspections, ranks risks, drafts corrective-action plans. Manager closes.
- **Open source today:** none found (gh search "food safety HACCP", stars>=20, not archived: no relevant hit).
- **Demo path:** NYC restaurant inspection open data.
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 8. Corporate travel policy compliance and expense reconciliation
- **Tier:** B Enterprise: needs figure (survey percentages, no dollar figure)
- **Enterprise check:** Buyer: corporate travel manager. Systems: TMC booking data, expense (Concur), card feeds. Regulation: audit, duty of care, tax. Human gate: manager approves exceptions.
- **Problem and today's workflow:** Staff match bookings to receipts and chase out-of-policy trips.
- **Evidence:** The GBTA research page (opened) only says booking outside required channels and out-of-policy hotel stays are "the leading compliance challenges", with no percentages. Search excerpts of the GBTA/ALTOUR release (168 travel managers, US and Canada) report 35% for booking outside channels and 28% for out-of-policy hotels; not opened. https://gbta.org/research/corporate-travel-policy-research-2026/ [Search-excerpt] (search excerpt only)
- **Agent design:** Reconciles bookings vs expenses, flags leakage, drafts traveler queries. Manager approves.
- **Open source today:** KXHXK/fieldpilot (21 stars, no licence declared, not archived, last push 2026-08-11; README read: partly, text mostly garbled; description says policy-aware field mission orchestration with travel and expense constraints; adjacent only).
- **Demo path:** Synthetic bookings and receipts.
- **Verification:** 2026-11-06, Verified (search excerpt), repos checked yes

### 9. OTA virtual-card chargeback and dispute response for hotels
- **Tier:** A Enterprise: needs figure
- **Enterprise check:** Buyer: hotel finance. Systems: PMS, payments, OTA extranet. Regulation: PCI-DSS, card-network rules. Human gate: finance approves responses.
- **Problem and today's workflow:** Staff gather folios and no-show proof per network deadline.
- **Evidence:** The cited Hospitality Net piece (opened) is a contributed opinion article by the CEO of TTI Technologies, which sells an ID-scanning product, and gives no chargeback figures (only an anecdote: "their chargeback issue has essentially disappeared"). No independent figure found. https://www.hospitalitynet.org/news/4131125/the-hidden-cost-of-otas-chargebacks-hotels-didnt-sign-up-for [Unconfirmed]
- **Agent design:** Assembles evidence, maps reason codes, drafts rebuttal. Finance submits; never fabricates evidence.
- **Open source today:** none found (gh search "hotel chargeback", stars>=20, not archived: no relevant hit).
- **Demo path:** Synthetic folios and disputes.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 10. Border-system disruption planning (EU Entry/Exit System)
- **Tier:** B Enterprise: needs figure
- **Enterprise check:** Buyer: airport, airline, tour operator. Systems: queue feeds, flight/booking data. Regulation: passenger-rights duty of care, GDPR. Human gate: ops manager approves re-timings.
- **Problem and today's workflow:** Teams forecast queues and rebook connections with patchy data.
- **Evidence:** Gulf News (opened): IATA's Rafael Schvartzman said expected EES waits had risen to "three, four, five, six hours", above earlier industry warnings of up to four hours. The page does not mention ACI Europe or a "2-6 hour" range (search excerpts show ACI Europe, A4E and IATA letters citing 4+ hours). https://gulfnews.com/business/aviation/europe-airport-queues-may-worsen-this-summer-warns-iata-over-ees-system-1.500565844 [Corrected]
- **Agent design:** Combines feeds, proposes re-timings and notices. Manager approves.
- **Open source today:** none found (gh search "EES border queue", stars>=20, not archived: no relevant hit).
- **Demo path:** Synthetic queue and itinerary data.
- **Verification:** 2026-11-06, Corrected, repos checked no (no EES-specific query run)

## Sources
- https://www.checkbook.org/national/consumers-notebook/articles/Here-Is-What-Airlines-Must-Do-If-Your-Flight-Is-Canceled-or-Delayed-7739
- https://www.ch-aviation.com/news/53601-uks-caa-sanctions-five-carriers-for-pax-rights-violations
- https://www.bmwet.gv.at/en/Topics/tourism/tourism-service-and-contacts/str_regulation.html
- https://travelweekly.co.uk/news/mishandled-bags-cost-airlines-5bn-in-2024
- https://www.cxagents.com/content/cathay-agents/worldwide/en_DE/policies/reservation-ticketing/adm-acm-policy.html
- https://www.icao.int/sites/default/files/APAC/Meetings/2025/2025%20CORSIASAP/Presentations/CORSIA_Agenda-Item-2_CORSIA-Implementation-Elements.pdf
- https://www.cdc.gov/restaurant-food-safety
- https://gbta.org/research/corporate-travel-policy-research-2026/
- https://www.hospitalitynet.org/news/4131125/the-hidden-cost-of-otas-chargebacks-hotels-didnt-sign-up-for
- https://gulfnews.com/business/aviation/europe-airport-queues-may-worsen-this-summer-warns-iata-over-ees-system-1.500565844
