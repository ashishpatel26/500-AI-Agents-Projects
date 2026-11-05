# Cybersecurity

## Overview
Security operations teams spend effort on alert triage, vulnerability prioritisation, detection upkeep, identity hygiene and regulator/customer-facing evidence. Manual work concentrates where an analyst pivots across five or six consoles per decision and then writes it up. Every case keeps a human approving any containment, patch, filing or access change. Alert content is attacker-controlled, so prompt-injection resistance and least-privilege tool scopes apply to all.

Verification note: GitHub search was rate-limited (HTTP 403) during the run, so entries for cases 6-10 say "not searched". Seeded repos (cases 1-5) are carried from earlier research; README status per seed.

## Systems of record, regulations, public datasets
- **Systems:** SIEM (Splunk, Sentinel, Wazuh), EDR (CrowdStrike, Defender), SOAR, identity (Okta, Entra ID, SailPoint), CMDB/asset inventory, vulnerability scanners (Tenable, Qualys), CSPM, ticketing (ServiceNow, Jira), email security gateway, GRC.
- **Regulations/standards:** DORA (2022/2554) incident reporting, NIS2 Art. 23 (2022), SEC Form 8-K Item 1.05 (2023), PCI DSS v4.0 (2022), ISO/IEC 27001:2022, NIST CSF 2.0 (2024), SOX 404, EU Cyber Resilience Act (2024).
- **Public datasets:** MITRE ATT&CK https://attack.mitre.org ; CISA KEV https://www.cisa.gov/known-exploited-vulnerabilities-catalog ; EPSS https://www.first.org/epss/ ; NVD API https://nvd.nist.gov/developers ; SigmaHQ rules https://github.com/SigmaHQ/sigma ; Mordor/OTRF security datasets https://github.com/OTRF/Security-Datasets ; Splunk Attack Data https://github.com/splunk/attack_data .

## Use cases

### 1. SOC alert triage and investigation
- **Tier:** A | Enterprise: pass
- **Enterprise check:** Buyer: SOC/MSSP. Systems: SIEM, EDR, identity, threat intel, ticketing. Regulation: breach-notification clocks, GDPR on log PII, audit trail. Human: analyst approves containment (isolate host, disable account).
- **Problem and today's workflow:** Tier-1/2 analysts pivot across consoles to decide true vs false positive, then write the case.
- **Evidence:** IBM Cost of a Data Breach 2025 via Infosecurity Magazine: "mean time organizations took to identify and contain a breach fell to 241 days"; extensive AI/automation users "saved an average $1.9m". https://www.infosecurity-magazine.com/news/data-breach-costs-fall/ [Verified]
- **Agent design:** Enrich alert, query SIEM/EDR/identity, correlate, assign verdict and confidence, draft case notes. Containment actions queue for analyst approval.
- **Open source today:** beenuar/AiSOC (7,264 stars, MIT, not archived, last push 2026-11-05; README read: yes; addresses: AI SOC with auditable agent investigation and human-approved responses); gensecaihq/Wazuh-Autopilot (62 stars, MIT, not archived, last push 2026-09-24; README read: yes; addresses: agentic SOC for Wazuh with human control).
- **Demo path:** Splunk attack_data / OTRF datasets replayed into a Wazuh or Elastic stack.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 2. Edge-device and exploited-CVE patch prioritisation
- **Tier:** A | Enterprise: pass
- **Enterprise check:** Buyer: vulnerability management. Systems: scanners, CMDB, KEV/EPSS, change management. Regulation: PCI DSS 6.3.3, DORA ICT risk, cyber-insurance attestations. Human: change board approves patch windows and exceptions.
- **Problem and today's workflow:** Analysts reconcile scanner output with KEV, asset criticality and owners, then chase tickets and exceptions.
- **Evidence:** Verizon DBIR 2025 via Infosecurity Magazine: exploitation is "20% of the overall data breaches" (not 20% of initial access as originally written); "only 54% were fully remediated within a median time frame of 32 days". https://www.infosecurity-magazine.com/news/verizon-dbir-jump-vulnerability/ [Corrected]
- **Agent design:** Join scanner, KEV, EPSS and CMDB; find owners; draft tickets with risk rationale; track SLAs. Change board approves.
- **Open source today:** echelongraph/echelongraph-mcp (20 stars, MIT, not archived, last push 2026-11-01; README read: yes; adjacent only: read-only CVE and exposure data MCP, not a prioritisation agent).
- **Demo path:** CISA KEV + EPSS + a synthetic asset inventory CSV.
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 3. Multi-regime regulatory incident reporting (DORA / NIS2 / SEC)
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: CISO plus legal. Systems: IR case timeline, CMDB, GRC, regulator portals. Regulation: DORA (4h after classification / 24h after awareness, 72h, one month), NIS2 Art. 23 (24h/72h/one month), SEC 8-K Item 1.05 (four business days after materiality). Human: lawyers sign every filing; materiality is a legal judgement.
- **Problem and today's workflow:** Staff classify severity and hand-draft staged notices to several regulators while facts change.
- **Evidence:** Opened and confirmed: NIS2 early warning within 24 hours, notification within 72 hours, final report within one month (https://www.ilr.lu/en/?p=37413); SEC Form 8-K due "within four business days after a company makes a determination that a cybersecurity incident is material" (https://www.hunton.com/insights/legal/sec-finalizes-cybersecurity-disclosure-requirements). DORA clocks not confirmed: FMA page returned 403; no DORA timings are asserted. [Verified]
- **Agent design:** Pull facts from the IR timeline, classify against each regime's criteria, fill templates, track deadlines, redraft on updates. Legal approves and files.
- **Open source today:** none found (gh search 'dora incident' returned no hits).
- **Demo path:** Synthetic incident timeline; compare drafts with published DORA/NIS2 templates.
- **Verification:** 2026-11-06, Verified, search done yes

### 4. Detection engineering: threat intel to working SIEM rules
- **Tier:** A | Enterprise: pass
- **Enterprise check:** Buyer: detection engineering. Systems: SIEM, Sigma repo, CTI platform, log pipeline, git. Regulation: PCI DSS 10, NIST CSF DE. Human: engineer reviews before deploy.
- **Problem and today's workflow:** Engineers read reports, map to ATT&CK, write and translate rules, test, and repair rules that silently stop firing.
- **Evidence:** CardinalOps 2025 via Help Net Security: SIEMs "have detection coverage for just 21% of adversary techniques"; on average 13% of rules are "non-functional and will never trigger". Vendor study. https://www.helpnetsecurity.com/2025/06/09/siem-detection-coverage/ [Verified]
- **Agent design:** Extract behaviours from a report, draft Sigma, convert, test against sample logs, measure false positives, open PR. Engineer approves merge.
- **Open source today:** AttackIQ/SigmAIQ (96 stars, LGPL-2.1, not archived, last push 2025-11-03; README read: yes; addresses partly: pySigma wrapper and utilities for converting Sigma rules); depalmar/ai-dfir-toolkit (149 stars, Apache-2.0, not archived, last push 2026-11-02; README read: yes; adjacent only: detection rules for AI/ML attacks).
- **Demo path:** SigmaHQ rules plus OTRF datasets as test logs.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 5. SBOM/VEX exploitability triage
- **Tier:** A | Enterprise: pass
- **Enterprise check:** Buyer: product security. Systems: SBOM store, scanners, source repos, build system, VEX publisher. Regulation: EU CRA vulnerability handling, US EO 14028 SBOM practice. Human: security engineer signs each "not affected" statement.
- **Problem and today's workflow:** Teams decide per product whether each dependency CVE is reachable, then write VEX statements.
- **Evidence:** Security Boulevard (May 2024): "more than 93% of the flaws added have not been analyzed or enhanced"; VulnCheck found 11,885 of 12,720 CVEs published 12 Feb-20 May 2024 unanalysed. The 72.4% (Sept 2024) figure is not on the page. https://securityboulevard.com/2024/05/nist-struggles-with-nvd-backlog-as-93-of-flaws-remain-unanalyzed [Corrected]
- **Agent design:** Read call graphs, run reachability tools, check config, draft VEX with justification. Engineer signs.
- **Open source today:** guacsec/guac (1,570 stars, Apache-2.0, not archived, last push 2026-11-02; README read: yes; adjacent only: software supply-chain metadata graph); owasp-dep-scan/dep-scan (1,327 stars, MIT, not archived, last push 2026-10-30; README read: yes; adjacent only: dependency risk scanner). Neither is an exploitability-triage agent.
- **Demo path:** CycloneDX SBOMs of open-source apps, NVD data and OSV (https://osv.dev).
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 6. User-reported phishing triage
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: SOC/awareness team. Systems: report-phish mailbox, email gateway (M365 Defender), URL sandbox, EDR, SIEM, ticketing. Regulation: employee-data privacy, incident records. Human: analyst approves mailbox-wide purge, domain blocks and account resets.
- **Problem and today's workflow:** Analysts open each reported mail, detonate links, check who clicked, search for the campaign across mailboxes and write the outcome back to the reporter.
- **Evidence:** Phishing share of initial access (16%/15%) not found on the cited SpyCloud page, which gives no standalone phishing percentage. Number removed. Reference, not confirmed: https://spycloud.com/blog/verizon-2025-data-breach-report-insights [Unconfirmed]
- **Agent design:** Parse headers/URLs/attachments, sandbox and reputation lookups, query click logs, classify, propose purge and blocks, reply to reporter. Analyst approves tenant-wide actions.
- **Open source today:** none found (gh search 'phishing triage' returned no hits).
- **Demo path:** Public phishing corpora (Nazario set, https://monkey.org/~jose/phishing/) plus synthetic click logs.
- **Verification:** 2026-11-06, Unconfirmed, search done yes

### 7. Cloud misconfiguration (CSPM) finding remediation
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: cloud security. Systems: CSPM, AWS/Azure/GCP, IaC repos, CMDB for owners, ticketing. Regulation: PCI DSS, SOC 2, ISO 27001 control evidence. Human: resource owner approves IaC pull request.
- **Problem and today's workflow:** Analysts triage thousands of findings, find owners, and write Terraform fixes or chase teams.
- **Evidence:** 68% delayed-remediation survey figure could not be confirmed (vmblog returned 403; sponsor and year unknown). Number removed. Reference, not confirmed: https://vmblog.com/?p=49504 ; context https://cloudsecurityalliance.org/articles/survey-report-cloud-security-posture-management-and-misconfiguration-risks [Unconfirmed]
- **Agent design:** Cluster findings by root cause, map to repo via tags/state, draft Terraform change, run plan and policy checks. Owner approves PR.
- **Open source today:** not checked (GitHub search rate-limited).
- **Demo path:** Prowler or Checkov scan of intentionally vulnerable Terraform (TerraGoat, https://github.com/bridgecrewio/terragoat).
- **Verification:** 2026-11-06, Unconfirmed, repos not checked

### 8. Access recertification (user entitlement reviews)
- **Tier:** B (risk scoring is rules; agent preps evidence and chases reviewers) | Enterprise: pass
- **Enterprise check:** Buyer: IAM/internal audit. Systems: IGA (SailPoint), Entra ID/Okta, HRIS, ERP and app roles, ticketing. Regulation: SOX 404, PCI DSS 4.0 req 7 periodic review, ISO 27001:2022 A.5.18. Human: application owner certifies or revokes.
- **Problem and today's workflow:** Reviewers get spreadsheets with thousands of entitlements and rubber-stamp them.
- **Evidence:** Verizon DBIR 2025 via SpyCloud: "stolen credentials were still the most common initial access vector - used in 22% of breaches". Secondary source. https://spycloud.com/blog/verizon-2025-data-breach-report-insights [Verified]
- **Agent design:** Pull entitlements and HR status, flag leavers, SoD conflicts, unused access, summarise per reviewer with reasons, create revoke tickets after approval.
- **Open source today:** not checked (GitHub search rate-limited).
- **Demo path:** Synthetic HR + entitlement CSVs with planted orphan and SoD cases.
- **Verification:** 2026-11-06, Verified, repos not checked

### 9. Threat-intel-driven threat hunting
- **Tier:** A | Enterprise: needs figure
- **Enterprise check:** Buyer: threat hunt/CTI team. Systems: SIEM/data lake, EDR telemetry, CTI platform (MISP), ATT&CK. Regulation: log privacy rules, audit trail of searches. Human: hunter approves hypotheses and escalations.
- **Problem and today's workflow:** Hunters turn a fresh report into hypotheses, write queries, review results and document findings, mostly ad hoc.
- **Evidence:** IBM 2025 via Infosecurity Magazine: "mean time organizations took to identify and contain a breach fell to 241 days" (breach-lifecycle proxy, not a hunting study). https://www.infosecurity-magazine.com/news/data-breach-costs-fall/ [Verified]
- **Agent design:** Generate hypotheses mapped to ATT&CK, run bounded read-only queries, summarise anomalies, open an incident if confirmed. Hunter approves escalation.
- **Open source today:** not checked (GitHub search rate-limited).
- **Demo path:** OTRF Security-Datasets with injected adversary behaviours.
- **Verification:** 2026-11-06, Verified, repos not checked

### 10. Customer security questionnaire and due-diligence response
- **Tier:** A | Enterprise: pass
- **Enterprise check:** Buyer: security/GRC at a vendor. Systems: GRC evidence store, policy library, trust center, CRM, past answers. Regulation: contractual representations; false answers create liability. Human: security owner approves answers before release.
- **Problem and today's workflow:** Sales engineers and security staff answer repeated 100-300 question forms by searching old responses.
- **Evidence:** Wolfia (vendor blog): a 200-question questionnaire "should take about 12 to 18 hours of focused work"; "20 to 40 hours" without an answer library. Vendor figures, not independent. https://cdn.wolfia.com/blog/how-long-complete-200-question-security-questionnaire [Verified]
- **Agent design:** Parse form, retrieve approved answers and evidence, flag gaps or stale controls, draft responses with citations. Owner approves.
- **Open source today:** not checked (GitHub search rate-limited).
- **Demo path:** CSA CAIQ v4 (https://cloudsecurityalliance.org/artifacts/consensus-assessments-initiative-questionnaire-v4) with a synthetic policy set.
- **Verification:** 2026-11-06, Verified, repos not checked

## Sources
- https://attack.mitre.org
- https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- https://www.first.org/epss/
- https://nvd.nist.gov/developers
- https://github.com/SigmaHQ/sigma
- https://github.com/OTRF/Security-Datasets
- https://github.com/splunk/attack_data
- https://osv.dev
- https://monkey.org/~jose/phishing/
- https://github.com/bridgecrewio/terragoat
- https://www.infosecurity-magazine.com/news/data-breach-costs-fall/
- https://uk.newsroom.ibm.com/2025-cost-of-data-breach-UK
- https://www.infosecurity-magazine.com/news/verizon-dbir-jump-vulnerability/
- https://www.tenable.com/blog/verizon-2025-dbir-tenable-research-collaboration
- https://www.fma.gv.at/en/dora-ict-related-incidents/
- https://www.ilr.lu/en/?p=37413
- https://www.hunton.com/insights/legal/sec-finalizes-cybersecurity-disclosure-requirements
- https://www.helpnetsecurity.com/2025/06/09/siem-detection-coverage/
- https://securityboulevard.com/2024/05/nist-struggles-with-nvd-backlog-as-93-of-flaws-remain-unanalyzed
- https://spycloud.com/blog/verizon-2025-data-breach-report-insights
- https://vmblog.com/?p=49504
- https://cloudsecurityalliance.org/articles/survey-report-cloud-security-posture-management-and-misconfiguration-risks
- https://cdn.wolfia.com/blog/how-long-complete-200-question-security-questionnaire
- https://cloudsecurityalliance.org/artifacts/consensus-assessments-initiative-questionnaire-v4
