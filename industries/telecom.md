# Telecom & Networks

## Overview
Telecom operators spend manual effort on network operations (alarm triage, change control, energy), subscriber protection (SIM-swap, fraud, robocalls) and regulatory work (outage reporting, broadband maps, legal demands, pole attachments). Work concentrates in NOCs, fraud and revenue-assurance teams, regulatory and legal departments, and network engineering. Networks are safety-relevant, so almost every automated action needs change control and a human approval gate.

## Systems of record, regulations, public datasets
- **Systems:** OSS/BSS, alarm and fault managers, topology/inventory (CMDB, GIS), PM/KPI stores, ticketing (ServiceNow, Remedy), CRM and billing, CDR/mediation and fraud-management systems, number-portability gateways, network automation/NCM tools, pole-attachment and permitting portals, legal-process (subpoena) intake systems.
- **Regulations and standards:** FCC SIM-swap/port-out rules (FCC 23-95, adopted 15 Nov 2023, WC Docket 21-341; confirmed in the Federal Register text of 8 Dec 2023); CPNI rules (47 CFR 64.2001 et seq.); TRACED Act (2019) and STIR/SHAKEN call authentication; FCC Robocall Mitigation Database rules; FCC outage reporting (47 CFR Part 4, NORS); CALEA and Stored Communications Act for legal demands; FCC pole attachment rules (47 CFR 1.1411 and 2018/2025 orders); broadband data collection and map challenge process; 3GPP and TM Forum standards for network automation. Not individually confirmed against official text: CPNI section numbers, TRACED Act, 47 CFR Part 4, CALEA/SCA, 47 CFR 1.1411.
- **Public datasets:**
  - FCC National Broadband Map data: https://broadbandmap.fcc.gov/data-download
  - TN-AutoRCA benchmark (530 scenarios; the paper names it TN-RCA530): https://arxiv.org/abs/2507.18190
  - Ericsson multi-agent troubleshooting paper: https://arxiv.org/abs/2511.00651
  - CRTC/Xona Rogers outage review: https://crtc.gc.ca/eng/publications/reports/xona2024.htm
  - Verizon transparency reports: https://www.verizon.com/about/investors/transparency-report
  - Synthetic CDRs and alarm logs generated with open generators (no public operator CDR dataset used).

## Use cases

### 1. Network fault root-cause analysis from alarm storms
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer is an operator NOC. Systems: alarm manager, topology/inventory, KPI store, ticketing, change records. Service-level and outage-reporting obligations apply; engineers approve any remediation.
- **Problem and today's workflow:** NOC engineers triage thousands of correlated RAN, transport and core alarms by hand to find the failing element or recent change.
- **Evidence:** TN-AutoRCA paper (PDF text read): "TN-RCA530, the inaugural real-world, publicly accessible benchmark for root cause analysis (RCA) of telecommunication network alarms, comprising 530 fault scenarios constructed from expert-validated Knowledge Graphs". Ericsson paper abstract: a multi-agent system applying "across both Radio Access Network (RAN) and Core network domains". https://arxiv.org/pdf/2507.18190 ; https://arxiv.org/abs/2511.00651 . No operator cost figure verified. [Verified]
- **Agent design:** Tools: topology query, alarm/KPI retrieval, change-log search, runbook retrieval. Steps: cluster alarms, hypothesize causes, test with queries, propose remediation. Engineer approves any config change.
- **Open source today:** none found for RCA agents (gh search repos "alarm root cause telecom", stars >= 20, not archived: no results). LiaoWenzhe/Aiops-Learning-Resources (214 stars, AGPL-3.0, not archived, last push 2023-01-08; README read: yes) is a personal collection of AIOps learning resources; adjacent only, and stale.
- **Demo path:** Use the TN-AutoRCA scenarios or generate alarm storms from a synthetic topology graph.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 2. SIM-swap and port-out fraud authentication
- **Tier:** A. Enterprise: needs figure
- **Enterprise check:** Buyer is a carrier's retail/care and fraud team. Systems: CRM, SIM/eSIM provisioning, number-portability gateway, device/risk data. FCC 23-95 requires secure authentication and notifications; CPNI privacy rules apply; a fraud supervisor approves exceptions.
- **Problem and today's workflow:** Agents verify callers before SIM changes or ports; fraudsters social-engineer them. Step-up checks vary by channel.
- **Evidence:** Federal Register: the FCC "adopted this Report and Order on November 15, 2023" (FCC 23-95); before a SIM change or port providers must use "secure methods to authenticate a customer" and give "immediate notification to customers of any requests for a SIM change". Compliance is the later of six months after the effective date or OMB completing review; the 5 July 2024 Wireline Competition Bureau waiver postponed compliance until OMB review completes ("will not be required until OMB completes review"), per a law-firm summary. https://www.govinfo.gov/content/pkg/FR-2023-12-08/html/2023-26338.htm ; https://www.tlp.law/2024/07/08/fcc-amends-sim-swapping-port-out-fraud-compliance-date/ . Loss totals not verified. Current compliance status after July 2024 not checked. [Verified]
- **Agent design:** Tools: CRM history, device-change signals, step-up verification, account-hold API. Steps: score request, choose verification, hold or release. Supervisor approves exceptions; denials explained.
- **Open source today:** none found (gh search repos "SIM swap fraud", stars >= 20, not archived: no results).
- **Demo path:** Synthetic account events with injected takeover patterns.
- **Verification:** 2026-11-06, Verified, repos checked yes (search only)

### 3. Telecom fraud and revenue-assurance investigation (IRSF, Wangiri, bypass)
- **Tier:** B. Enterprise: needs figure
- **Enterprise check:** Buyer is a carrier fraud-management team. Systems: CDR/mediation, signalling probes, billing, interconnect contracts. GDPR/CPNI apply; analyst approves blocks and partner disputes.
- **Problem and today's workflow:** Analysts review anomaly alerts, check number ranges, block routes and negotiate disputes.
- **Evidence:** The CFCA page (opened) describes the survey only and carries no loss figure; the Subex write-up of the survey returned HTTP 403. Search extracts attributed about $39.89B (2.22% of revenue) to the 2021 survey but no page showing it was opened, so the number is removed. Reference, not confirmed: https://cfca.org/fraud-loss-survey-2021/ [Unconfirmed]
- **Agent design:** Tools: CDR query, number-range intelligence, block-route API, dispute drafter. Steps: confirm anomaly, size loss, propose block, draft dispute. Analyst approves blocks.
- **Open source today:** none found (gh search repos "telecom fraud CDR", stars >= 20, not archived: no results).
- **Demo path:** Synthetic CDRs with premium-rate destination bursts.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes (search only)

### 4. Broadband availability map challenge adjudication
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is an ISP or state broadband office. Systems: GIS, subscriber/billing records, propagation models, FCC BDC portal. False certification carries FCC penalties; an engineer certifies.
- **Problem and today's workflow:** Staff review location-level challenges and assemble engineering evidence or concede.
- **Evidence:** "According to FCC figures cited by NTCA, 2.2 million of 3.7 million fixed availability challenges were conceded by providers." https://www.benton.org/headlines/significant-errors-plague-fccs-broadband-map-says-isp-alliance . A search extract says later FCC figures (map version 2) differ (about 2.1M conceded at a later stage); not opened. [Verified]
- **Agent design:** Tools: address geocoder, network-plant GIS, subscriber lookup, response drafter. Steps: test serviceability, gather proof, draft reply. Engineer approves each submission.
- **Open source today:** none found (gh search repos "broadband map challenge", stars >= 20, not archived: no results).
- **Demo path:** FCC National Broadband Map extracts with synthetic challenges.
- **Verification:** 2026-11-06, Verified, repos checked yes (search only)

### 5. Robocall mitigation filing and traceback response
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is a voice provider compliance team. Systems: Robocall Mitigation Database filings, SBC/CDR logs, traceback portal (ITG), customer KYC. TRACED Act and FCC rules; compliance officer approves filings and blocks.
- **Problem and today's workflow:** Staff keep RMD filings accurate, answer traceback requests and vet upstream customers.
- **Evidence:** Wiley: in December 2024 the FCC Enforcement Bureau issued a Show Cause Order "directing 2,411 providers to either cure their deficient RMD filings" or explain; on August 25, 2025 its Final Removal Order removed "over 1,200 voice service providers' certifications". https://www.wiley.law/alert-FCC-Enforcement-Action-Removes-Over-1200-Providers-from-Robocall-Mitigation-Database . A fetched FCC press release of 25 Aug 2025 carries the same figures. The telecompetitor URL originally cited returned HTTP 403. [Verified]
- **Agent design:** Tools: RMD checker, CDR trace, customer-KYC lookup, filing drafter. Steps: trace call path, identify source customer, draft response. Compliance officer approves.
- **Open source today:** none found for compliance (gh search repos "robocall mitigation", stars >= 20, not archived: no results; callattendant-style repos are consumer call blockers).
- **Demo path:** Synthetic CDRs with spoofed-origin bursts and a mock traceback request.
- **Verification:** 2026-11-06, Verified, repos checked yes (search only)

### 6. Legal-demand (subpoena and warrant) response processing
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is a carrier legal-compliance team. Systems: intake queue, CRM/billing, CDR archive, case management. Stored Communications Act and CALEA; counsel approves each release.
- **Problem and today's workflow:** Analysts validate legal process, scope the data, pull records, redact and respond within deadlines.
- **Evidence:** Verizon US Transparency Report (2nd half 2023), table row "Subpoenas" lists 61,120 for 2H 2023 (the same report notes 8,182 of the subpoenas in civil cases). https://www.verizon.com/about/sites/default/files/US-Transparency-Report-2H-2023.pdf (text extracted from the fetched PDF; the original espanol.verizon.com URL redirects here). [Verified]
- **Agent design:** Tools: document validity checks, record query, redaction, response drafter. Steps: validate, scope, collect, draft. Counsel approves every release.
- **Open source today:** none found for response handling (gh search repos "subpoena telecom", stars >= 20, not archived: no results). OpenLI-NZ/openli (127 stars, GPL-3.0, not archived, last push 2026-10-29; README read: yes) is ETSI-compliant lawful-intercept software; adjacent only.
- **Demo path:** Synthetic subpoenas and a mock subscriber database.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 7. Network change-request validation
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is operator network operations. Systems: change-management tool, NCM, topology, lab. Outage-reporting duties follow failures; change board approves.
- **Problem and today's workflow:** Engineers assess change risk, review method-of-procedure steps and set rollback plans manually.
- **Evidence:** MobileSyrup on the CRTC/Xona review: the outage came from "an error in configuring distribution routers" (a policy filter was removed); Rogers' algorithm lowered the upgrade's risk rating after five successful phases so lab testing was not required; staff "could not pinpoint the root cause for about 14 hours". https://mobilesyrup.com/2024/07/05/july-2022-rogers-outage-report-crtc/ . The CRTC page itself returned HTTP 403. [Verified]
- **Agent design:** Tools: config diff, topology blast-radius, past-incident search. Steps: score risk, require pre/post checks, flag mis-rated changes. Change board approves.
- **Open source today:** none found for risk validation (gh search repos "network change risk", stars >= 20, not archived: only unrelated hits). rconfig/rconfig (224 stars, GPL-3.0, not archived, last push 2026-11-01; README read: yes) is network configuration management with change detection; adjacent only.
- **Demo path:** Router configs from a lab emulator with injected filter removal.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 8. Pole-attachment and make-ready application management
- **Tier:** B. Enterprise: needs figure
- **Enterprise check:** Buyer is a fiber builder or utility. Systems: pole-attachment portal, GIS, permitting, contractor management. FCC timelines apply; engineer approves.
- **Problem and today's workflow:** Teams track applications, surveys, estimates and make-ready steps manually.
- **Evidence:** The cited Sheppard Mullin page returned HTTP 429 on both attempts, so the earlier timelines (about 10 business days completeness review, about 45 days merits response) are unverified and removed. Third-party benefit estimates not verified. Reference, not confirmed: https://www.sheppard.com/insights/blogs/fcc-adopts-new-pole-attachment-rules-to-streamline-broadband-deployment [Unconfirmed]
- **Agent design:** Tools: portal queries, GIS, deadline tracker, response drafter. Steps: check completeness, track clocks, escalate overruns. Engineer approves submissions.
- **Open source today:** none found (gh search repos "pole attachment", stars >= 20, not archived: no results).
- **Demo path:** Synthetic application queue with deadline breaches.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes (search only)

### 9. Outage-reporting (NORS) determination and filing
- **Tier:** A. Enterprise: pass
- **Enterprise check:** Buyer is operator regulatory affairs. Systems: ticketing, monitoring, NORS portal. 47 CFR Part 4 sets reporting triggers; regulatory lead approves each filing.
- **Problem and today's workflow:** Staff decide whether an incident meets thresholds and compile notifications and final reports.
- **Evidence:** Benton summary of the FCC action: total $17.4 million ($16 million CenturyLink, $1.4 million Intrado) for the April 2014 multi-state 911 outage, which lasted over six hours, with more than 6,600 911 calls unanswered. https://www.benton.org/headlines/fcc-fines-centurylink-and-intrado-174-million-multi-state-911-outage . Corrected: the earlier "65-minute outage left over 460,000 calls undelivered" is wrong for this case and is removed; the fcc.gov pages returned HTTP 403. The fine concerns a 911 outage, not a NORS filing failure as such. [Corrected]
- **Agent design:** Tools: incident timeline, customer-impact calculator, rule checker, report drafter. Steps: assess, draft, track deadlines. Regulatory lead approves filings.
- **Open source today:** none found (gh search repos "NORS outage", stars >= 20, not archived: only an unrelated hit).
- **Demo path:** Synthetic incident tickets with impact data.
- **Verification:** 2026-11-06, Corrected, repos checked yes (search only)

## Sources
- https://arxiv.org/pdf/2507.18190 ; https://arxiv.org/abs/2511.00651
- https://www.govinfo.gov/content/pkg/FR-2023-12-08/html/2023-26338.htm ; https://www.tlp.law/2024/07/08/fcc-amends-sim-swapping-port-out-fraud-compliance-date/
- https://cfca.org/fraud-loss-survey-2021/ (reference, not confirmed)
- https://www.benton.org/headlines/significant-errors-plague-fccs-broadband-map-says-isp-alliance
- https://www.lightreading.com/network-operators-focus-on-energy-savings-as-costs-soar/d/d-id/781453
- https://www.wiley.law/alert-FCC-Enforcement-Action-Removes-Over-1200-Providers-from-Robocall-Mitigation-Database
- https://www.verizon.com/about/sites/default/files/US-Transparency-Report-2H-2023.pdf
- https://mobilesyrup.com/2024/07/05/july-2022-rogers-outage-report-crtc/ (CRTC original https://crtc.gc.ca/eng/publications/reports/xona2024.htm returned 403)
- https://www.sheppard.com/insights/blogs/fcc-adopts-new-pole-attachment-rules-to-streamline-broadband-deployment (reference, not confirmed)
- https://www.benton.org/headlines/fcc-fines-centurylink-and-intrado-174-million-multi-state-911-outage
- https://broadbandmap.fcc.gov/data-download ; https://www.verizon.com/about/investors/transparency-report
