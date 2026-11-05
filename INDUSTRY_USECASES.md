# Industry-wise Agent Use Cases

A catalogue of **245 real, enterprise-grade problems** across **25 industries** where multi-step, tool-using AI agents fit. Each problem is a workflow people do by hand today, with systems of record, a regulatory or audit angle, and a human approval step. Layout follows [Real-time-ML-Project](https://github.com/ashishpatel26/Real-time-ML-Project).

**How to read the tags**

- Tier A: an agent is the right tool. Tier B: a model or rules do the core, the agent assists.
- Evidence: Verified (source page opened, figure confirmed), Corrected (original figure was wrong, fixed), Search-excerpt (figure seen only in a search excerpt), Unconfirmed (number removed, problem description kept).
- Open gap: no matching open-source agent was found in a keyword search. That is not proof none exists.

**Contribute:** build or find an open-source agent for any item, then open a PR following [CONTRIBUTION.md](CONTRIBUTION.md). A listed project should be removed if its owner marks it unmaintained or it has had no commits for about two years.

| <!-- --> | <!-- --> | <!-- --> |
| --- | --- | --- |
| [Accounting & Tax](#accounting--tax) | [Agriculture & Food](#agriculture--food) | [Automotive & Aerospace](#automotive--aerospace) |
| [Banking & Lending](#banking--lending) | [Capital Markets & Asset Management](#capital-markets--asset-management) | [Construction & Engineering](#construction--engineering) |
| [Cybersecurity](#cybersecurity) | [Education & Research](#education--research) | [Energy & Utilities](#energy--utilities) |
| [Government & Public Safety](#government--public-safety) | [Healthcare Providers & Payers](#healthcare-providers--payers) | [Hospitality & Travel](#hospitality--travel) |
| [HR & Workforce](#hr--workforce) | [Insurance](#insurance) | [Legal & Compliance](#legal--compliance) |
| [Logistics & Supply Chain](#logistics--supply-chain) | [Manufacturing & Industrial](#manufacturing--industrial) | [Media, Entertainment & Gaming](#media-entertainment--gaming) |
| [Nonprofit & Social Impact](#nonprofit--social-impact) | [Oil, Gas & Mining](#oil-gas--mining) | [Pharma, Biotech & Life Sciences](#pharma-biotech--life-sciences) |
| [Real Estate](#real-estate) | [Retail & E-commerce](#retail--e-commerce) | [Software Development & DevOps](#software-development--devops) |
| [Telecom & Networks](#telecom--networks) |  |  |

## Table of Contents

- [Accounting & Tax](#accounting--tax)
  - [Audit testing of journal entries and estimates](#accounting--tax)
  - [Pillar Two (GloBE) data collection and top-up tax computation](#accounting--tax)
  - [IRS notice triage and response preparation](#accounting--tax)
  - [Month-end close and intercompany reconciliation](#accounting--tax)
  - [US sales-tax exemption-certificate and nexus compliance](#accounting--tax)
  - [Accounts payable invoice exception handling (three-way match)](#accounting--tax)
  - [Revenue-recognition contract review (ASC 606 / IFRS 15)](#accounting--tax)
  - [Transfer pricing documentation (master file, local file, intercompany agreements)](#accounting--tax)
  - [ESG / CSRD sustainability data assurance](#accounting--tax)
  - [SOX 404 control testing evidence collection](#accounting--tax)
- [Agriculture & Food](#agriculture--food)
  - [Crop insurance claim adjustment and loss verification](#agriculture--food)
  - [FSMA 204 traceability recordkeeping and trace-back](#agriculture--food)
  - [Pesticide-label-compliant scouting and treatment advisory](#agriculture--food)
  - [Allergen and label compliance on formulation or ingredient change](#agriculture--food)
  - [EU Deforestation Regulation due-diligence and plot geolocation verification](#agriculture--food)
  - [FSVP importer supplier verification](#agriculture--food)
  - [Organic certification review and inspection follow-up](#agriculture--food)
  - [Environmental monitoring program (Listeria) corrective action](#agriculture--food)
  - [Recall execution and effectiveness checks](#agriculture--food)
  - [FDA Form 483 and warning-letter response drafting](#agriculture--food)
- [Automotive & Aerospace](#automotive--aerospace)
  - [Warranty claim analysis, fraud screening and supplier recovery](#automotive--aerospace)
  - [Recall root-cause investigation and Part 573 report drafting](#automotive--aerospace)
  - [Aircraft maintenance records (MRO) compliance review](#automotive--aerospace)
  - [AS9100 nonconformance and MRB disposition support](#automotive--aerospace)
  - [Type-approval and homologation dossier assembly (EU 2018/858, UNECE)](#automotive--aerospace)
  - [Supplier PPAP package review](#automotive--aerospace)
  - [Airworthiness directive and service bulletin applicability](#automotive--aerospace)
  - [First Article Inspection (AS9102) review](#automotive--aerospace)
  - [Parts traceability and suspect-unapproved-parts screening](#automotive--aerospace)
  - [Software certification evidence review (DO-178C traceability)](#automotive--aerospace)
- [Banking & Lending](#banking--lending)
  - [AML transaction-monitoring alert investigation and SAR narrative drafting](#banking--lending)
  - [Sanctions screening alert disposition (name-match adjudication)](#banking--lending)
  - [Beneficial-ownership and KYC refresh for legal-entity customers](#banking--lending)
  - [Mortgage loan file underwriting and condition clearing](#banking--lending)
  - [Commercial credit memo and financial-spreading preparation](#banking--lending)
  - [Loan covenant compliance monitoring](#banking--lending)
  - [Trade finance documentary-credit examination (letters of credit)](#banking--lending)
  - [Regulatory reporting data reconciliation and submission review (call report, FR Y-9C/Y-14)](#banking--lending)
  - [Card and deposit dispute / chargeback handling (Reg E and Reg Z)](#banking--lending)
  - [Customer complaint triage and root-cause analysis (CFPB / UDAAP)](#banking--lending)
- [Capital Markets & Asset Management](#capital-markets--asset-management)
  - [Trade break and settlement-fail resolution](#capital-markets--asset-management)
  - [Fund NAV reconciliation and pricing-exception review](#capital-markets--asset-management)
  - [Institutional counterparty and fund KYC onboarding](#capital-markets--asset-management)
  - [Fund shareholder-report and prospectus compliance review](#capital-markets--asset-management)
  - [Best-execution review and TCA exception analysis](#capital-markets--asset-management)
  - [Trade and communications surveillance alert review](#capital-markets--asset-management)
  - [Transaction-reporting break remediation (EMIR REFIT / MiFIR)](#capital-markets--asset-management)
  - [Collateral and margin dispute resolution (UMR/VM)](#capital-markets--asset-management)
  - [Corporate actions event processing and entitlement checks](#capital-markets--asset-management)
- [Construction & Engineering](#construction--engineering)
  - [Building permit plan-check and resubmittal cycles](#construction--engineering)
  - [RFI and submittal triage across drawings, specs and contracts](#construction--engineering)
  - [Delay and entitlement analysis for construction claims](#construction--engineering)
  - [Site safety observation and incident triage](#construction--engineering)
  - [Quantity takeoff and bid estimate from drawings](#construction--engineering)
  - [Pay application and lien-waiver compliance review](#construction--engineering)
  - [Davis-Bacon certified payroll review](#construction--engineering)
  - [Change-order pricing and entitlement review](#construction--engineering)
  - [Closeout, as-built and O&M documentation turnover](#construction--engineering)
- [Cybersecurity](#cybersecurity)
  - [SOC alert triage and investigation](#cybersecurity)
  - [Edge-device and exploited-CVE patch prioritisation](#cybersecurity)
  - [Multi-regime regulatory incident reporting (DORA / NIS2 / SEC)](#cybersecurity)
  - [Detection engineering: threat intel to working SIEM rules](#cybersecurity)
  - [SBOM/VEX exploitability triage](#cybersecurity)
  - [User-reported phishing triage](#cybersecurity)
  - [Cloud misconfiguration (CSPM) finding remediation](#cybersecurity)
  - [Access recertification (user entitlement reviews)](#cybersecurity)
  - [Threat-intel-driven threat hunting](#cybersecurity)
  - [Customer security questionnaire and due-diligence response](#cybersecurity)
- [Education & Research](#education--research)
  - [Systematic-review screening and data extraction](#education--research)
  - [Research-integrity screening (paper mills, image/data manipulation)](#education--research)
  - [Special-education IEP drafting and compliance tracking](#education--research)
  - [Federal student-aid verification and improper-payment detection](#education--research)
  - [Grant peer-review logistics (reviewer matching, conflicts)](#education--research)
  - [Transfer-credit evaluation and articulation](#education--research)
  - [Clery Act annual security report compilation](#education--research)
  - [IRB protocol pre-review and completeness checks](#education--research)
  - [Sponsored-research proposal and post-award compliance checks](#education--research)
  - [Accreditation self-study evidence compilation](#education--research)
- [Energy & Utilities](#energy--utilities)
  - [Generator interconnection study screening and queue management](#energy--utilities)
  - [NEPA environmental review drafting and consistency checking for energy infrastructure](#energy--utilities)
  - [Lead service line inventory resolution and replacement planning](#energy--utilities)
  - [Utility wildfire mitigation plan evidence assembly](#energy--utilities)
  - [NERC CIP compliance evidence collection and gap review](#energy--utilities)
  - [Rate case filing support and regulatory data-request response](#energy--utilities)
  - [Distributed energy resource (DER) interconnection application review](#energy--utilities)
  - [Nuclear corrective action program condition-report screening](#energy--utilities)
  - [Power plant emissions (CEMS) data validation and Part 75 quarterly reporting](#energy--utilities)
  - [Transmission and pipeline right-of-way permit and easement tracking](#energy--utilities)
- [Government & Public Safety](#government--public-safety)
  - [FOIA / public-records request processing and redaction](#government--public-safety)
  - [SNAP eligibility casework and payment-error prevention](#government--public-safety)
  - [Unemployment-insurance fraud and improper-payment triage](#government--public-safety)
  - [NEPA environmental-review document preparation](#government--public-safety)
  - [VA disability claims evidence review](#government--public-safety)
  - [Body-worn-camera footage review and redaction for public-records release](#government--public-safety)
  - [Rulemaking public-comment analysis](#government--public-safety)
  - [Authorization-to-operate (RMF/FedRAMP) package preparation](#government--public-safety)
  - [Personnel-vetting investigation preparation](#government--public-safety)
  - [Medicaid renewal (ex parte) and procedural-denial prevention](#government--public-safety)
- [Healthcare Providers & Payers](#healthcare-providers--payers)
  - [Provider-side prior-authorization packet assembly and submission](#healthcare-providers--payers)
  - [Hospital claim-denial analysis and appeal drafting](#healthcare-providers--payers)
  - [Discharge medication reconciliation](#healthcare-providers--payers)
  - [Payer utilization-management case review assist](#healthcare-providers--payers)
  - [Coding and clinical documentation integrity (CDI) audit](#healthcare-providers--payers)
  - [Provider credentialing and payer enrollment](#healthcare-providers--payers)
  - [Provider directory validation](#healthcare-providers--payers)
  - [HEDIS / quality measure chart abstraction and gap closure](#healthcare-providers--payers)
  - [Claims payment integrity and pre-payment review](#healthcare-providers--payers)
  - [Medicare Advantage appeals and grievances case handling](#healthcare-providers--payers)
- [Hospitality & Travel](#hospitality--travel)
  - [Airline irregular operations (IROPS) passenger rebooking](#hospitality--travel)
  - [EU261/UK261 and DOT compensation claim adjudication](#hospitality--travel)
  - [Short-term rental registration compliance (EU 2024/1028)](#hospitality--travel)
  - [Baggage irregularity tracing and claims (WorldTracer)](#hospitality--travel)
  - [BSP settlement and agency debit memo (ADM) dispute handling](#hospitality--travel)
  - [Aviation emissions MRV (EU ETS / CORSIA)](#hospitality--travel)
  - [Multi-site food-safety compliance and inspection remediation](#hospitality--travel)
  - [Corporate travel policy compliance and expense reconciliation](#hospitality--travel)
  - [OTA virtual-card chargeback and dispute response for hotels](#hospitality--travel)
  - [Border-system disruption planning (EU Entry/Exit System)](#hospitality--travel)
- [HR & Workforce](#hr--workforce)
  - [Hiring-decision bias monitoring across the applicant funnel](#hr--workforce)
  - [Automated employment decision tool (AEDT) compliance monitoring](#hr--workforce)
  - [Public-sector time-to-hire orchestration](#hr--workforce)
  - [Form I-9 audit and remediation](#hr--workforce)
  - [Payroll and wage-and-hour error auditing](#hr--workforce)
  - [Pay-equity analysis and EU Pay Transparency reporting](#hr--workforce)
  - [Discrimination charge response and workplace investigation case management](#hr--workforce)
  - [OSHA injury recordkeeping and electronic submission](#hr--workforce)
  - [Worker-classification (contractor vs employee) review](#hr--workforce)
  - [Leave (FMLA) and ADA accommodation case administration](#hr--workforce)
- [Insurance](#insurance)
  - [Claims fraud (SIU) investigation support](#insurance)
  - [Claims first notice of loss (FNOL) intake and triage](#insurance)
  - [Subrogation identification and recovery](#insurance)
  - [Reinsurance bordereaux preparation and reconciliation](#insurance)
  - [Commercial underwriting submission intake and triage](#insurance)
  - [Catastrophe claim surge handling](#insurance)
  - [Bodily-injury claim demand-package review](#insurance)
  - [Rate and form filing preparation (SERFF)](#insurance)
  - [Commercial premium audit](#insurance)
  - [Coverage verification and reservation-of-rights drafting](#insurance)
- [Legal & Compliance](#legal--compliance)
  - [GDPR data subject access request (DSAR) fulfilment](#legal--compliance)
  - [Post-signature contract obligation tracking and value leakage](#legal--compliance)
  - [Privilege review in e-discovery](#legal--compliance)
  - [Regulatory change management and obligation mapping](#legal--compliance)
  - [Third-party / vendor privacy and security due diligence (GDPR Art. 28, DORA)](#legal--compliance)
  - [Contract review against a negotiation playbook](#legal--compliance)
  - [Litigation hold issuance and preservation tracking](#legal--compliance)
  - [Trademark and patent prosecution docketing and deadline management](#legal--compliance)
  - [Regulatory examination and subpoena response assembly](#legal--compliance)
  - [Outside counsel invoice review against billing guidelines](#legal--compliance)
- [Logistics & Supply Chain](#logistics--supply-chain)
  - [Customs tariff (HTS) classification for import entries](#logistics--supply-chain)
  - [Freight invoice audit and accessorial-charge dispute](#logistics--supply-chain)
  - [UFLPA supply-chain tracing for detained shipments](#logistics--supply-chain)
  - [Ocean demurrage and detention (D&D) invoice validation and dispute](#logistics--supply-chain)
  - [Freight cargo loss-and-damage claims handling](#logistics--supply-chain)
  - [Importer Security Filing (ISF) and entry document reconciliation](#logistics--supply-chain)
  - [Restricted-party and export-control screening alert adjudication](#logistics--supply-chain)
  - [Dangerous goods shipping-document compliance check](#logistics--supply-chain)
  - [Carrier onboarding and fraud vetting](#logistics--supply-chain)
  - [Duty drawback claim preparation](#logistics--supply-chain)
- [Manufacturing & Industrial](#manufacturing--industrial)
  - [Maintenance troubleshooting and work-order drafting from manuals, CMMS history and sensor data](#manufacturing--industrial)
  - [CAPA investigation and effectiveness checks (regulated plants)](#manufacturing--industrial)
  - [Supplier embedded-emissions data collection for EU CBAM declarations](#manufacturing--industrial)
  - [Electronic component obsolescence and last-time-buy decisions](#manufacturing--industrial)
  - [Tariff classification (HS code) and origin determination](#manufacturing--industrial)
  - [Supplier corrective action (SCAR / 8D) review and escalation](#manufacturing--industrial)
  - [Product material compliance (REACH SVHC, RoHS, SCIP) across supplier declarations](#manufacturing--industrial)
  - [Engineering change order (ECO) impact analysis across BOM, inventory and compliance](#manufacturing--industrial)
  - [Process safety management of change (MOC) and PHA action tracking](#manufacturing--industrial)
  - [Environmental release reporting (TRI Form R / EPCRA) data assembly and QA](#manufacturing--industrial)
- [Media, Entertainment & Gaming](#media-entertainment--gaming)
  - [Music sync rights clearance](#media-entertainment--gaming)
  - [Royalty statement reconciliation and audit](#media-entertainment--gaming)
  - [DSA statements-of-reasons and moderation case handling](#media-entertainment--gaming)
  - [Online game harassment report triage](#media-entertainment--gaming)
  - [Live-sports piracy detection and takedown](#media-entertainment--gaming)
  - [Subtitle and dubbing localization QC](#media-entertainment--gaming)
  - [Ad campaign delivery reconciliation and invoice dispute](#media-entertainment--gaming)
  - [Guild residuals and production payment compliance](#media-entertainment--gaming)
  - [Online gambling AML and responsible-gambling interventions](#media-entertainment--gaming)
  - [Accessibility compliance for video services (EAA)](#media-entertainment--gaming)
- [Nonprofit & Social Impact](#nonprofit--social-impact)
  - [Legal-aid intake, triage and referral](#nonprofit--social-impact)
  - [Humanitarian needs assessment and appeal prioritization](#nonprofit--social-impact)
  - [Homelessness coordinated entry and housing placement](#nonprofit--social-impact)
  - [Federal-grant compliance and Single Audit readiness](#nonprofit--social-impact)
  - [Funder reporting and outcomes consolidation](#nonprofit--social-impact)
  - [Cash-assistance registration, deduplication and payment reconciliation](#nonprofit--social-impact)
  - [Form 990 preparation and multi-state charity registration](#nonprofit--social-impact)
  - [UK Gift Aid claim preparation and donor-declaration audit](#nonprofit--social-impact)
  - [Partner and vendor due diligence with sanctions screening for international NGOs](#nonprofit--social-impact)
  - [Foundation cross-border grant due diligence (equivalency determination)](#nonprofit--social-impact)
- [Oil, Gas & Mining](#oil-gas--mining)
  - [Methane leak detection (LDAR) and super-emitter response](#oil-gas--mining)
  - [HSE incident investigation and trend analysis](#oil-gas--mining)
  - [Well integrity review](#oil-gas--mining)
  - [Mineral reserve and resource reporting (S-K 1300 / JORC / NI 43-101)](#oil-gas--mining)
  - [Drilling and mining permit application assembly](#oil-gas--mining)
  - [Environmental compliance monitoring and exceedance reporting](#oil-gas--mining)
  - [Royalty and production regulatory reporting reconciliation](#oil-gas--mining)
  - [Pipeline integrity: in-line inspection anomaly dig prioritization](#oil-gas--mining)
  - [Process safety: management of change (MOC) and PHA review](#oil-gas--mining)
  - [Orphan, idle well and asset-retirement obligation tracking](#oil-gas--mining)
- [Pharma, Biotech & Life Sciences](#pharma-biotech--life-sciences)
  - [Pharmacovigilance adverse-event case intake and triage](#pharma-biotech--life-sciences)
  - [Clinical-trial eligibility screening against free-text records](#pharma-biotech--life-sciences)
  - [Regulatory submission (eCTD) assembly and consistency check](#pharma-biotech--life-sciences)
  - [Clinical trial site feasibility and selection](#pharma-biotech--life-sciences)
  - [GxP deviation investigation and CAPA drafting](#pharma-biotech--life-sciences)
  - [Safety literature surveillance](#pharma-biotech--life-sciences)
  - [Clinical protocol authoring and amendment impact analysis](#pharma-biotech--life-sciences)
  - [Clinical data review and query management](#pharma-biotech--life-sciences)
  - [Promotional material medical-legal-regulatory (MLR) review](#pharma-biotech--life-sciences)
  - [Global regulatory change control and label variation tracking](#pharma-biotech--life-sciences)
- [Real Estate](#real-estate)
  - [Commercial lease abstraction and lease-accounting data](#real-estate)
  - [Closing wire-fraud and payoff verification](#real-estate)
  - [Municipal building-permit plan review](#real-estate)
  - [Tenant screening accuracy and FCRA dispute handling](#real-estate)
  - [Mortgage loan file assembly and condition clearing](#real-estate)
  - [Title examination and curative-item tracking](#real-estate)
  - [Fair-housing compliance review of listings and ad campaigns](#real-estate)
  - [Appraisal review and reconsideration-of-value handling](#real-estate)
  - [CRE rent-roll and T-12 underwriting plus covenant monitoring](#real-estate)
  - [Construction-loan draw package review](#real-estate)
- [Retail & E-commerce](#retail--e-commerce)
  - [Returns processing and returns-fraud adjudication](#retail--e-commerce)
  - [Card-payment chargeback representment](#retail--e-commerce)
  - [EU GPSR marketplace product-safety compliance](#retail--e-commerce)
  - [Store inventory shrink and record-accuracy investigation](#retail--e-commerce)
  - [Counterfeit and IP notice-and-takedown handling for marketplaces](#retail--e-commerce)
  - [Vendor deduction and OTIF fine dispute](#retail--e-commerce)
  - [Product recall execution and effectiveness tracking](#retail--e-commerce)
  - [High-volume seller verification (INFORM Consumers Act)](#retail--e-commerce)
  - [Product chemical-restriction and Prop 65 compliance](#retail--e-commerce)
  - [FSMA 204 food traceability record assembly](#retail--e-commerce)
- [Software Development & DevOps](#software-development--devops)
  - [Legacy COBOL/mainframe migration](#software-development--devops)
  - [Incident root-cause analysis and postmortem drafting](#software-development--devops)
  - [Vulnerable-dependency / CVE remediation pull requests across a repo estate](#software-development--devops)
  - [Cloud cost (FinOps) anomaly investigation and rightsizing](#software-development--devops)
  - [Language and framework upgrade migration (e.g. Java 8 to 17)](#software-development--devops)
  - [Change-request risk review and audit evidence assembly](#software-development--devops)
  - [Static-analysis (SAST) finding auto-remediation](#software-development--devops)
  - [Policy-aware pull-request review at scale](#software-development--devops)
- [Telecom & Networks](#telecom--networks)
  - [Network fault root-cause analysis from alarm storms](#telecom--networks)
  - [SIM-swap and port-out fraud authentication](#telecom--networks)
  - [Telecom fraud and revenue-assurance investigation (IRSF, Wangiri, bypass)](#telecom--networks)
  - [Broadband availability map challenge adjudication](#telecom--networks)
  - [Robocall mitigation filing and traceback response](#telecom--networks)
  - [Legal-demand (subpoena and warrant) response processing](#telecom--networks)
  - [Network change-request validation](#telecom--networks)
  - [Pole-attachment and make-ready application management](#telecom--networks)
  - [Outage-reporting (NORS) determination and filing](#telecom--networks)

<a name="accounting--tax"></a>
## Accounting & Tax

Finance, audit and tax teams spend effort on period close, reconciliations, payables control, audit evidence, and multi-jurisdiction tax compliance. Manual work concentrates in matching documents to ledger entries, reading contracts and notices, and compiling evidence for reviewers. Everything is subject to internal controls and auditor or tax-authority scrutiny.

Full write-up with sources: [industries/accounting-tax.md](industries/accounting-tax.md)

**Enterprise problem statements**

- [Audit testing of journal entries and estimates](industries/accounting-tax.md#1-audit-testing-of-journal-entries-and-estimates) - Auditors sample entries, trace them to support, test estimates and document conclusions. (Tier A; Unconfirmed; enterprise: needs figure)
- [Pillar Two (GloBE) data collection and top-up tax computation](industries/accounting-tax.md#2-pillar-two-globe-data-collection-and-top-up-tax-computation) - Teams extract entity-level data, apply GloBE adjustments, test safe harbours and prepare the GloBE Information Return. (Tier A; Verified; enterprise: pass)
- [IRS notice triage and response preparation](industries/accounting-tax.md#3-irs-notice-triage-and-response-preparation) - Staff read the notice, match to the return and transcripts, determine action and deadline and draft a reply. (Tier A; Corrected; enterprise: pass)
- [Month-end close and intercompany reconciliation](industries/accounting-tax.md#4-month-end-close-and-intercompany-reconciliation) - Accountants match intercompany balances, bank items and subledger differences, chase counterparties and book adjusting entries. (Tier A; Unconfirmed; enterprise: needs figure)
- [US sales-tax exemption-certificate and nexus compliance](industries/accounting-tax.md#5-us-sales-tax-exemption-certificate-and-nexus-compliance) - Staff collect and validate certificates per state and monitor nexus thresholds. (Tier A; Unconfirmed; enterprise: needs figure)
- [Accounts payable invoice exception handling (three-way match)](industries/accounting-tax.md#6-accounts-payable-invoice-exception-handling-three-way-match) - Clerks research price/quantity mismatches, missing PO or receipts, duplicate and suspicious invoices, and request approvals by email. (Tier A; Unconfirmed; enterprise: needs figure)
- [Revenue-recognition contract review (ASC 606 / IFRS 15)](industries/accounting-tax.md#7-revenue-recognition-contract-review-asc-606--ifrs-15) - Accountants read nonstandard contracts to identify performance obligations, variable consideration, and modifications, then draft memos and schedules. (Tier A; Unconfirmed; enterprise: needs figure)
- [Transfer pricing documentation (master file, local file, intercompany agreements)](industries/accounting-tax.md#8-transfer-pricing-documentation-master-file-local-file-intercompany-agreements) - Teams compile functional analyses, intercompany transaction data and benchmarking for each jurisdiction's local file each year. (Tier A; Unconfirmed; enterprise: needs figure)
- [ESG / CSRD sustainability data assurance](industries/accounting-tax.md#9-esg--csrd-sustainability-data-assurance) - Teams collect data points from many sources, trace to evidence and reconcile with narrative disclosures. (Tier B; Unconfirmed; enterprise: needs figure)
- [SOX 404 control testing evidence collection](industries/accounting-tax.md#10-sox-404-control-testing-evidence-collection) - Testers request evidence from control owners, check against attributes and document exceptions. (Tier A; Unconfirmed; enterprise: needs figure)

**Open gaps (no matching open-source agent found)**

- Pillar Two (GloBE) data collection and top-up tax computation
- IRS notice triage and response preparation
- Month-end close and intercompany reconciliation
- Transfer pricing documentation (master file, local file, intercompany agreements)
- SOX 404 control testing evidence collection

<a name="agriculture--food"></a>
## Agriculture & Food

Growers, insurers, food manufacturers and importers spend effort on traceability, safety plans, labeling, certifications and supply-chain due diligence. Manual work concentrates in reconciling supplier documents, lot codes and field records across ERP, email and paper, then assembling evidence for regulators or certifiers. Errors lead to recalls, denied claims or market-access loss.

Full write-up with sources: [industries/agriculture-food.md](industries/agriculture-food.md)

**Enterprise problem statements**

- [Crop insurance claim adjustment and loss verification](industries/agriculture-food.md#1-crop-insurance-claim-adjustment-and-loss-verification) - Adjusters inspect fields, reconcile planting records, yield history and weather, compute indemnities in worksheets. (Tier A; Verified; enterprise: pass)
- [FSMA 204 traceability recordkeeping and trace-back](industries/agriculture-food.md#2-fsma-204-traceability-recordkeeping-and-trace-back) - Key data elements at critical tracking events are scattered; during outbreaks staff manually build spreadsheets. (Tier A; Verified; enterprise: needs figure)
- [Pesticide-label-compliant scouting and treatment advisory](industries/agriculture-food.md#3-pesticide-label-compliant-scouting-and-treatment-advisory) - Agronomists combine scouting photos, weather and spray history to recommend treatments within label restrictions. (Tier B; Corrected; enterprise: pass)
- [Allergen and label compliance on formulation or ingredient change](industries/agriculture-food.md#4-allergen-and-label-compliance-on-formulation-or-ingredient-change) - Each ingredient or line change requires re-check of specs, cross-contact controls and labels by hand. (Tier A; Verified; enterprise: pass)
- [EU Deforestation Regulation due-diligence and plot geolocation verification](industries/agriculture-food.md#5-eu-deforestation-regulation-due-diligence-and-plot-geolocation-verification) - Staff collect plot polygons, validate legality and chase smallholder suppliers. (Tier A; Verified; enterprise: needs figure)
- [FSVP importer supplier verification](industries/agriculture-food.md#6-fsvp-importer-supplier-verification) - Importers evaluate each foreign supplier's hazards, audits and inspection history manually. (Tier A; Unconfirmed; enterprise: needs figure)
- [Organic certification review and inspection follow-up](industries/agriculture-food.md#7-organic-certification-review-and-inspection-follow-up) - Reviewers compare organic system plans with inspection reports and trace-back audits by hand. (Tier A; Unconfirmed; enterprise: needs figure)
- [Environmental monitoring program (Listeria) corrective action](industries/agriculture-food.md#8-environmental-monitoring-program-listeria-corrective-action) - QA staff track positive swabs, investigate root cause and verify follow-up sampling. (Tier B; Corrected; enterprise: needs figure)
- [Recall execution and effectiveness checks](industries/agriculture-food.md#9-recall-execution-and-effectiveness-checks) - Teams identify affected lots, notify customers, collect responses and report effectiveness. (Tier A; Unconfirmed; enterprise: needs figure)
- [FDA Form 483 and warning-letter response drafting](industries/agriculture-food.md#10-fda-form-483-and-warning-letter-response-drafting) - Quality teams gather evidence per observation and draft CAPA commitments. (Tier A; Unconfirmed; enterprise: needs figure)

**Open gaps (no matching open-source agent found)**

- Crop insurance claim adjustment and loss verification
- FSMA 204 traceability recordkeeping and trace-back
- Allergen and label compliance on formulation or ingredient change
- EU Deforestation Regulation due-diligence and plot geolocation verification
- FSVP importer supplier verification
- Organic certification review and inspection follow-up
- Environmental monitoring program (Listeria) corrective action
- Recall execution and effectiveness checks
- FDA Form 483 and warning-letter response drafting

<a name="automotive--aerospace"></a>
## Automotive & Aerospace

OEMs, suppliers and MRO shops spend effort on field quality, certification evidence, supplier quality gates and maintenance-record integrity. Manual work concentrates where regulated documents must be cross-checked against standards and history: warranty and recall analysis, airworthiness records, nonconformance dispositions, type-approval dossiers and PPAP packages. Errors carry regulator action (recalls, certificate revocation), so every use case ends with a qualified human signature.

Full write-up with sources: [industries/automotive-aerospace.md](industries/automotive-aerospace.md)

**Enterprise problem statements**

- [Warranty claim analysis, fraud screening and supplier recovery](industries/automotive-aerospace.md#1-warranty-claim-analysis-fraud-screening-and-supplier-recovery) - Analysts read technician comments, match claims to part/lot, detect abuse, and compile supplier recovery packages manually. (Tier A; Corrected; enterprise: pass)
- [Recall root-cause investigation and Part 573 report drafting](industries/automotive-aerospace.md#2-recall-root-cause-investigation-and-part-573-report-drafting) - Engineers assemble complaints, warranty trends and test data, draft the defect chronology and population by hand under deadline. (Tier A; Verified; enterprise: pass)
- [Aircraft maintenance records (MRO) compliance review](industries/automotive-aerospace.md#3-aircraft-maintenance-records-mro-compliance-review) - Records reviewers read scanned logbooks and work packages to confirm AD/life-limited-part compliance and spot gaps before delivery or return-to-service. (Tier A; Unconfirmed; enterprise: needs figure)
- [AS9100 nonconformance and MRB disposition support](industries/automotive-aerospace.md#4-as9100-nonconformance-and-mrb-disposition-support) - Quality engineers pull drawings, measurements and past similar NCRs to propose use-as-is/repair/scrap, and check customer approval needs. (Tier A; Unconfirmed; enterprise: needs figure)
- [Type-approval and homologation dossier assembly (EU 2018/858, UNECE)](industries/automotive-aerospace.md#5-type-approval-and-homologation-dossier-assembly-eu-2018858-unece) - Staff map each regulation clause to test evidence and variant data for every market and update dossiers when rules change. (Tier A; Unconfirmed; enterprise: needs figure)
- [Supplier PPAP package review](industries/automotive-aerospace.md#6-supplier-ppap-package-review) - SQEs check 18 PPAP elements (control plans, PFMEA, MSA, capability) for consistency and completeness, then chase fixes. (Tier A; Unconfirmed; enterprise: needs figure)
- [Airworthiness directive and service bulletin applicability](industries/automotive-aerospace.md#7-airworthiness-directive-and-service-bulletin-applicability) - Engineers read each new AD, match serial/part effectivity to the as-built fleet configuration and schedule work. (Tier A; Unconfirmed; enterprise: needs figure)
- [First Article Inspection (AS9102) review](industries/automotive-aerospace.md#8-first-article-inspection-as9102-review) - Inspectors balloon drawings and transcribe measurements into Forms 1-3, then reviewers check completeness. (Tier B; Unconfirmed; enterprise: needs figure)
- [Parts traceability and suspect-unapproved-parts screening](industries/automotive-aerospace.md#9-parts-traceability-and-suspect-unapproved-parts-screening) - Staff check 8130-3/EASA Form 1 certificates, back-to-birth trace and supplier status by hand. (Tier A; Unconfirmed; enterprise: needs figure)
- [Software certification evidence review (DO-178C traceability)](industries/automotive-aerospace.md#10-software-certification-evidence-review-do-178c-traceability) - Engineers cross-check requirement-to-code-to-test trace links and coverage evidence manually before audits. (Tier A; Unconfirmed; enterprise: needs figure)

**Open gaps (no matching open-source agent found)**

- Warranty claim analysis, fraud screening and supplier recovery
- Recall root-cause investigation and Part 573 report drafting
- AS9100 nonconformance and MRB disposition support
- Type-approval and homologation dossier assembly (EU 2018/858, UNECE)
- Airworthiness directive and service bulletin applicability
- First Article Inspection (AS9102) review
- Parts traceability and suspect-unapproved-parts screening
- Software certification evidence review (DO-178C traceability)

<a name="banking--lending"></a>
## Banking & Lending

Banks spend most of their operating effort on financial-crime compliance (AML, sanctions, KYC), credit origination and monitoring, payments operations (disputes, trade documents) and recurring regulatory reporting. Manual work concentrates where an analyst must pull evidence from several systems, apply a policy or rulebook, and write a defensible narrative: alert dispositions, file review, memos, discrepancy notices. Every decision needs an audit trail and a named human approver.

Full write-up with sources: [industries/banking-lending.md](industries/banking-lending.md)

**Enterprise problem statements**

- [AML transaction-monitoring alert investigation and SAR narrative drafting](industries/banking-lending.md#1-aml-transaction-monitoring-alert-investigation-and-sar-narrative-drafting) - Analysts open each alert, pull customer profile, account history, counterparties and adverse media from separate tools, decide on escalation and hand-write the SAR narrative. (Tier A; Verified; enterprise: pass)
- [Sanctions screening alert disposition (name-match adjudication)](industries/banking-lending.md#2-sanctions-screening-alert-disposition-name-match-adjudication) - Fuzzy name matching creates large alert volumes. (Tier A; Unconfirmed; enterprise: needs figure)
- [Beneficial-ownership and KYC refresh for legal-entity customers](industries/banking-lending.md#3-beneficial-ownership-and-kyc-refresh-for-legal-entity-customers) - Analysts trace ownership chains across registries and filings in many jurisdictions, reconcile with customer certifications, and re-do this at periodic or trigger-based review. (Tier A; Verified; enterprise: needs figure)
- [Mortgage loan file underwriting and condition clearing](industries/banking-lending.md#4-mortgage-loan-file-underwriting-and-condition-clearing) - Processors and underwriters verify income, assets and property documents against guidelines, issue conditions and chase borrowers for missing or conflicting documents. (Tier A; Corrected; enterprise: pass)
- [Commercial credit memo and financial-spreading preparation](industries/banking-lending.md#5-commercial-credit-memo-and-financial-spreading-preparation) - Analysts re-key borrower financials from PDFs into spreading tools, compute ratios, research industry and news and draft the memo for committee. (Tier A; Unconfirmed; enterprise: needs figure)
- [Loan covenant compliance monitoring](industries/banking-lending.md#6-loan-covenant-compliance-monitoring) - Staff read credit agreements to find financial covenant definitions, recompute ratios from quarterly financials, compare with certificates, and track reporting deadlines in spreadsheets. (Tier A; Verified; enterprise: needs figure)
- [Trade finance documentary-credit examination (letters of credit)](industries/banking-lending.md#7-trade-finance-documentary-credit-examination-letters-of-credit) - Examiners check each presented document against LC terms and rules, list discrepancies and send refusal or acceptance advice. (Tier A; Corrected; enterprise: pass)
- [Regulatory reporting data reconciliation and submission review (call report, FR Y-9C/Y-14)](industries/banking-lending.md#8-regulatory-reporting-data-reconciliation-and-submission-review-call-report-fr-y-9cy-14) - Teams reconcile GL balances to report schedules, investigate edit-check failures and quarter-over-quarter variances, and write variance explanations before filing. (Tier B; Corrected; enterprise: pass)
- [Card and deposit dispute / chargeback handling (Reg E and Reg Z)](industries/banking-lending.md#9-card-and-deposit-dispute--chargeback-handling-reg-e-and-reg-z) - Analysts classify disputes, pull transaction and merchant evidence, apply network reason-code rules, send letters and track statutory clocks. (Tier A; Unconfirmed; enterprise: needs figure)
- [Customer complaint triage and root-cause analysis (CFPB / UDAAP)](industries/banking-lending.md#10-customer-complaint-triage-and-root-cause-analysis-cfpb--udaap) - Staff read complaints, classify product/issue, locate the account facts, draft a response and tag root cause for trend reporting. (Tier A; Unconfirmed; enterprise: needs figure)

**Open gaps (no matching open-source agent found)**

- Commercial credit memo and financial-spreading preparation
- Card and deposit dispute / chargeback handling (Reg E and Reg Z)
- Customer complaint triage and root-cause analysis (CFPB / UDAAP)

<a name="capital-markets--asset-management"></a>
## Capital Markets & Asset Management

Broker-dealers, banks' markets divisions, custodians and asset managers spend effort on post-trade operations (matching, settlement, collateral, corporate actions), fund accounting and NAV control, regulatory reporting and surveillance. Manual work concentrates in exception queues: a trade or position does not agree across two systems or counterparties, and an operations analyst must find out why, contact the counterparty and fix the record before a deadline.

Full write-up with sources: [industries/capital-markets-asset-management.md](industries/capital-markets-asset-management.md)

**Enterprise problem statements**

- [Trade break and settlement-fail resolution](industries/capital-markets-asset-management.md#1-trade-break-and-settlement-fail-resolution) - Analysts compare internal trades to counterparty/custodian data, identify the cause (price, quantity, SSI, allocation, missing instruction), contact counterparties and amend before the settlement cutoff, now one day shorter under T+1. (Tier A; Verified; enterprise: pass)
- [Fund NAV reconciliation and pricing-exception review](industries/capital-markets-asset-management.md#2-fund-nav-reconciliation-and-pricing-exception-review) - Daily, accountants reconcile positions and cash to custodian, review price tolerance breaches and stale prices, and decide whether an override is needed before striking the NAV. (Tier A; Unconfirmed; enterprise: needs figure)
- [Institutional counterparty and fund KYC onboarding](industries/capital-markets-asset-management.md#3-institutional-counterparty-and-fund-kyc-onboarding) - Analysts collect constitutional documents, identify the manager, GP, investors and controllers of funds, screen them and resolve missing documents across email chains. (Tier A; Verified; enterprise: needs figure)
- [Fund shareholder-report and prospectus compliance review](industries/capital-markets-asset-management.md#4-fund-shareholder-report-and-prospectus-compliance-review) - Teams assemble per-share-class reports, check fees, performance and holdings data against source systems and prior filings, and reconcile narrative against disclosures. (Tier A; Corrected; enterprise: pass)
- [Best-execution review and TCA exception analysis](industries/capital-markets-asset-management.md#5-best-execution-review-and-tca-exception-analysis) - Analysts run periodic execution quality statistics, pick outliers, collect the order context and write the rationale for exceptions. (Tier B; Corrected; enterprise: needs figure)
- [Trade and communications surveillance alert review](industries/capital-markets-asset-management.md#6-trade-and-communications-surveillance-alert-review) - Analysts review alerts (spoofing, front-running, wash trades), pull orders, chat and news, and write closure rationale. (Tier A; Corrected; enterprise: pass)
- [Transaction-reporting break remediation (EMIR REFIT / MiFIR)](industries/capital-markets-asset-management.md#7-transaction-reporting-break-remediation-emir-refit--mifir) - Teams reconcile rejects and mismatches from repositories, correct fields (UTI, LEI, valuation) and file correction reports. (Tier B; Unconfirmed; enterprise: needs figure)
- [Collateral and margin dispute resolution (UMR/VM)](industries/capital-markets-asset-management.md#8-collateral-and-margin-dispute-resolution-umrvm) - When margin calls differ from counterparty figures, analysts trace to trade-level valuation, CSA terms (thresholds, eligible collateral) and exchange breaks by email. (Tier A; Verified; enterprise: needs figure)
- [Corporate actions event processing and entitlement checks](industries/capital-markets-asset-management.md#9-corporate-actions-event-processing-and-entitlement-checks) - Staff reconcile conflicting event notices from several sources, determine terms, calculate entitlements and instruct elections before deadlines. (Tier A; Unconfirmed; enterprise: needs figure)

**Open gaps (no matching open-source agent found)**

- Trade break and settlement-fail resolution
- Fund shareholder-report and prospectus compliance review
- Best-execution review and TCA exception analysis
- Trade and communications surveillance alert review
- Transaction-reporting break remediation (EMIR REFIT / MiFIR)
- Collateral and margin dispute resolution (UMR/VM)
- Corporate actions event processing and entitlement checks

<a name="construction--engineering"></a>
## Construction & Engineering

Owners, general contractors and engineering firms spend effort on permits, document control (RFIs, submittals, change orders), cost control, payment compliance and safety. Manual work concentrates in reading drawings and specs against codes and contracts, and in compiling evidence for payment, claims and closeout. Most outputs carry legal or contractual consequences, so a licensed or accountable human approves.

Full write-up with sources: [industries/construction-engineering.md](industries/construction-engineering.md)

**Enterprise problem statements**

- [Building permit plan-check and resubmittal cycles](industries/construction-engineering.md#1-building-permit-plan-check-and-resubmittal-cycles) - Reviewers check sheets against code by hand across departments; applicants cycle through correction rounds. (Tier A; Corrected; enterprise: pass)
- [RFI and submittal triage across drawings, specs and contracts](industries/construction-engineering.md#2-rfi-and-submittal-triage-across-drawings-specs-and-contracts) - Engineers hunt for conflicts across documents, write RFIs, route and track responses. (Tier A; Corrected; enterprise: pass)
- [Delay and entitlement analysis for construction claims](industries/construction-engineering.md#3-delay-and-entitlement-analysis-for-construction-claims) - Consultants reconstruct schedule updates and assign delay responsibility across thousands of documents. (Tier A; Unconfirmed; enterprise: needs figure)
- [Site safety observation and incident triage](industries/construction-engineering.md#4-site-safety-observation-and-incident-triage) - Safety managers review photos and reports, write JHAs and track actions. (Tier B; Corrected; enterprise: pass)
- [Quantity takeoff and bid estimate from drawings](industries/construction-engineering.md#5-quantity-takeoff-and-bid-estimate-from-drawings) - Estimators measure quantities manually and price from quotes. (Tier A; Unconfirmed; enterprise: needs figure)
- [Pay application and lien-waiver compliance review](industries/construction-engineering.md#6-pay-application-and-lien-waiver-compliance-review) - Staff reconcile subs' billings to SOV, stored materials, change orders and waivers before releasing payment. (Tier A; Verified; enterprise: pass)
- [Davis-Bacon certified payroll review](industries/construction-engineering.md#7-davis-bacon-certified-payroll-review) - Staff match worker classifications and hours to wage determinations and fringe benefits weekly. (Tier B; Corrected; enterprise: pass)
- [Change-order pricing and entitlement review](industries/construction-engineering.md#8-change-order-pricing-and-entitlement-review) - Staff verify scope, notice timing, markup and time impact of proposed changes. (Tier A; Verified; enterprise: needs figure)
- [Closeout, as-built and O&M documentation turnover](industries/construction-engineering.md#9-closeout-as-built-and-om-documentation-turnover) - Teams assemble warranties, manuals, as-builts and test records against spec requirements before final payment. (Tier A; Unconfirmed; enterprise: needs figure)

**Open gaps (no matching open-source agent found)**

- Building permit plan-check and resubmittal cycles
- Delay and entitlement analysis for construction claims
- Pay application and lien-waiver compliance review
- Davis-Bacon certified payroll review
- Change-order pricing and entitlement review
- Closeout, as-built and O&M documentation turnover

<a name="cybersecurity"></a>
## Cybersecurity

Security operations teams spend effort on alert triage, vulnerability prioritisation, detection upkeep, identity hygiene and regulator/customer-facing evidence. Manual work concentrates where an analyst pivots across five or six consoles per decision and then writes it up. Every case keeps a human approving any containment, patch, filing or access change. Alert content is attacker-controlled, so prompt-injection resistance and least-privilege tool scopes apply to all.

Full write-up with sources: [industries/cybersecurity.md](industries/cybersecurity.md)

**Enterprise problem statements**

- [SOC alert triage and investigation](industries/cybersecurity.md#1-soc-alert-triage-and-investigation) - Tier-1/2 analysts pivot across consoles to decide true vs false positive, then write the case. (Tier A; Verified; enterprise: pass)
- [Edge-device and exploited-CVE patch prioritisation](industries/cybersecurity.md#2-edge-device-and-exploited-cve-patch-prioritisation) - Analysts reconcile scanner output with KEV, asset criticality and owners, then chase tickets and exceptions. (Tier A; Corrected; enterprise: pass)
- [Multi-regime regulatory incident reporting (DORA / NIS2 / SEC)](industries/cybersecurity.md#3-multi-regime-regulatory-incident-reporting-dora--nis2--sec) - Staff classify severity and hand-draft staged notices to several regulators while facts change. (Tier A; Verified; enterprise: needs figure)
- [Detection engineering: threat intel to working SIEM rules](industries/cybersecurity.md#4-detection-engineering-threat-intel-to-working-siem-rules) - Engineers read reports, map to ATT&CK, write and translate rules, test, and repair rules that silently stop firing. (Tier A; Verified; enterprise: pass)
- [SBOM/VEX exploitability triage](industries/cybersecurity.md#5-sbomvex-exploitability-triage) - Teams decide per product whether each dependency CVE is reachable, then write VEX statements. (Tier A; Corrected; enterprise: pass)
- [User-reported phishing triage](industries/cybersecurity.md#6-user-reported-phishing-triage) - Analysts open each reported mail, detonate links, check who clicked, search for the campaign across mailboxes and write the outcome back to the reporter. (Tier A; Unconfirmed; enterprise: needs figure)
- [Cloud misconfiguration (CSPM) finding remediation](industries/cybersecurity.md#7-cloud-misconfiguration-cspm-finding-remediation) - Analysts triage thousands of findings, find owners, and write Terraform fixes or chase teams. (Tier A; Unconfirmed; enterprise: needs figure)
- [Access recertification (user entitlement reviews)](industries/cybersecurity.md#8-access-recertification-user-entitlement-reviews) - Reviewers get spreadsheets with thousands of entitlements and rubber-stamp them. (Tier B; Verified; enterprise: pass)
- [Threat-intel-driven threat hunting](industries/cybersecurity.md#9-threat-intel-driven-threat-hunting) - Hunters turn a fresh report into hypotheses, write queries, review results and document findings, mostly ad hoc. (Tier A; Verified; enterprise: needs figure)
- [Customer security questionnaire and due-diligence response](industries/cybersecurity.md#10-customer-security-questionnaire-and-due-diligence-response) - Sales engineers and security staff answer repeated 100-300 question forms by searching old responses. (Tier A; Verified; enterprise: pass)

**Open gaps (no matching open-source agent found)**

- Multi-regime regulatory incident reporting (DORA / NIS2 / SEC)
- User-reported phishing triage

<a name="education--research"></a>
## Education & Research

Education institutions and research enterprises spend effort on compliance-bound administration: aid verification, special-education documentation, accreditation, sponsored-research compliance and review logistics. Manual work concentrates in reading student or research records across systems, matching them to federal rules, and producing documentation that auditors, regulators or courts may later examine. Student-facing tutoring and consumer study apps are out of scope.

Full write-up with sources: [industries/education-research.md](industries/education-research.md)

**Enterprise problem statements**

- [Systematic-review screening and data extraction](industries/education-research.md#1-systematic-review-screening-and-data-extraction) - Teams screen thousands of abstracts in duplicate, then extract data and assess bias. (Tier A; Verified; enterprise: needs figure)
- [Research-integrity screening (paper mills, image/data manipulation)](industries/education-research.md#2-research-integrity-screening-paper-mills-imagedata-manipulation) - Integrity staff check submissions for tortured phrases, fabricated authors and reused images. (Tier A; Unconfirmed; enterprise: needs figure)
- [Special-education IEP drafting and compliance tracking](industries/education-research.md#3-special-education-iep-drafting-and-compliance-tracking) - Case managers draft present levels and goals and track service minutes and legal timelines. (Tier B; Verified; enterprise: needs figure)
- [Federal student-aid verification and improper-payment detection](industries/education-research.md#4-federal-student-aid-verification-and-improper-payment-detection) - Staff verify FAFSA data and collect documents for flagged applications. (Tier A; Search-excerpt; enterprise: needs figure)
- [Grant peer-review logistics (reviewer matching, conflicts)](industries/education-research.md#5-grant-peer-review-logistics-reviewer-matching-conflicts) - Review officers match applications to reviewers and screen conflicts. (Tier B; Verified; enterprise: needs figure)
- [Transfer-credit evaluation and articulation](industries/education-research.md#6-transfer-credit-evaluation-and-articulation) - Evaluators compare outside syllabi and descriptions to local courses and set equivalencies. (Tier A; Verified; enterprise: needs figure)
- [Clery Act annual security report compilation](industries/education-research.md#7-clery-act-annual-security-report-compilation) - Staff collect crime reports from many sources, classify by geography and category and publish by Oct 1. (Tier B; Corrected; enterprise: needs figure)
- [IRB protocol pre-review and completeness checks](industries/education-research.md#8-irb-protocol-pre-review-and-completeness-checks) - Analysts check submissions against checklists, flag consent issues and route by review category. (Tier A; Corrected; enterprise: needs figure)
- [Sponsored-research proposal and post-award compliance checks](industries/education-research.md#9-sponsored-research-proposal-and-post-award-compliance-checks) - Staff check proposals against solicitations, review budgets and costs allowability. (Tier A; Unconfirmed; enterprise: needs figure)
- [Accreditation self-study evidence compilation](industries/education-research.md#10-accreditation-self-study-evidence-compilation) - Staff map evidence to standards across departments. (Tier B; Unconfirmed; enterprise: needs figure)

**Open gaps (no matching open-source agent found)**

- Research-integrity screening (paper mills, image/data manipulation)
- Special-education IEP drafting and compliance tracking
- Federal student-aid verification and improper-payment detection
- Grant peer-review logistics (reviewer matching, conflicts)
- Transfer-credit evaluation and articulation
- Clery Act annual security report compilation
- IRB protocol pre-review and completeness checks
- Sponsored-research proposal and post-award compliance checks
- Accreditation self-study evidence compilation

<a name="energy--utilities"></a>
## Energy & Utilities

Electric, gas and water utilities and the developers who connect to them spend most effort on regulatory filings, interconnection and permitting studies, asset-inspection records, and compliance evidence for auditors. Manual work concentrates where engineers move data between studies, GIS/asset systems and PDF filings (spreadsheets, shared drives, email), then a licensed or accountable person signs. Timelines are set by tariffs, statutes and regulator data requests, so delay has a direct cost.

Full write-up with sources: [industries/energy-utilities.md](industries/energy-utilities.md)

**Enterprise problem statements**

- [Generator interconnection study screening and queue management](industries/energy-utilities.md#1-generator-interconnection-study-screening-and-queue-management) - Planners and developers run cluster studies, allocate network-upgrade costs and re-study after withdrawals, mostly with spreadsheets and PDF reports. (Tier A; Verified; enterprise: pass)
- [NEPA environmental review drafting and consistency checking for energy infrastructure](industries/energy-utilities.md#2-nepa-environmental-review-drafting-and-consistency-checking-for-energy-infrastructure) - Staff assemble EIS text from specialist studies and prior documents, and match thousands of public comments to consistent responses. (Tier A; Unconfirmed; enterprise: needs figure)
- [Lead service line inventory resolution and replacement planning](industries/energy-utilities.md#3-lead-service-line-inventory-resolution-and-replacement-planning) - Engineers classify "unknown" material service lines using records, historical permits and field verification, then schedule excavations. (Tier A; Unconfirmed; enterprise: needs figure)
- [Utility wildfire mitigation plan evidence assembly](industries/energy-utilities.md#4-utility-wildfire-mitigation-plan-evidence-assembly) - Teams compile annual plan updates from risk models, inspection results and progress metrics, then answer regulator data requests. (Tier A; Corrected; enterprise: needs figure)
- [NERC CIP compliance evidence collection and gap review](industries/energy-utilities.md#5-nerc-cip-compliance-evidence-collection-and-gap-review) - Analysts hand-collect screenshots, logs and tickets to prove patch evaluation, access reviews and baseline changes across thousands of cyber assets. (Tier A; Unconfirmed; enterprise: needs figure)
- [Rate case filing support and regulatory data-request response](industries/energy-utilities.md#6-rate-case-filing-support-and-regulatory-data-request-response) - Hundreds of data requests per case require analysts to locate prior responses, pull ledger data and keep answers consistent with testimony. (Tier A; Unconfirmed; enterprise: needs figure)
- [Distributed energy resource (DER) interconnection application review](industries/energy-utilities.md#7-distributed-energy-resource-der-interconnection-application-review) - Engineers check completeness of solar/storage applications, run supplemental screens against feeder models and request corrections by email. (Tier A; Unconfirmed; enterprise: needs figure)
- [Nuclear corrective action program condition-report screening](industries/energy-utilities.md#8-nuclear-corrective-action-program-condition-report-screening) - Staff screen thousands of condition reports per year for significance, duplicates and trending. (Tier B; Unconfirmed; enterprise: needs figure)
- [Power plant emissions (CEMS) data validation and Part 75 quarterly reporting](industries/energy-utilities.md#9-power-plant-emissions-cems-data-validation-and-part-75-quarterly-reporting) - Environmental staff review hourly data, substitute missing data per rules, reconcile QA tests and submit quarterly files. (Tier A; Unconfirmed; enterprise: needs figure)
- [Transmission and pipeline right-of-way permit and easement tracking](industries/energy-utilities.md#10-transmission-and-pipeline-right-of-way-permit-and-easement-tracking) - Land agents track expiring easements, encroachments and permit conditions across PDFs and county records. (Tier B; Unconfirmed; enterprise: needs figure)

**Open gaps (no matching open-source agent found)**

- Generator interconnection study screening and queue management
- NEPA environmental review drafting and consistency checking for energy infrastructure
- Lead service line inventory resolution and replacement planning
- Utility wildfire mitigation plan evidence assembly
- NERC CIP compliance evidence collection and gap review
- Rate case filing support and regulatory data-request response
- Distributed energy resource (DER) interconnection application review
- Nuclear corrective action program condition-report screening
- Power plant emissions (CEMS) data validation and Part 75 quarterly reporting
- Transmission and pipeline right-of-way permit and easement tracking

<a name="government--public-safety"></a>
## Government & Public Safety

Government agencies spend effort on adjudicating claims and benefits, producing records and rulemaking files, and proving compliance. Manual work concentrates in reading evidence, applying statute or policy to each case, redacting records, and documenting decisions for appeal or audit. Every outcome is reviewable (appeals, litigation, IG audits), so agents must assist officials who keep decision authority. Safety-critical real-time functions (for example 911 dispatch) are deliberately excluded.

Full write-up with sources: [industries/government-public-safety.md](industries/government-public-safety.md)

**Enterprise problem statements**

- [FOIA / public-records request processing and redaction](industries/government-public-safety.md#1-foia--public-records-request-processing-and-redaction) - FOIA staff search multiple repositories, review each page for exemptions (b)(5)/(b)(6), redact by hand and track deadlines. (Tier A; Verified; enterprise: pass)
- [SNAP eligibility casework and payment-error prevention](industries/government-public-safety.md#2-snap-eligibility-casework-and-payment-error-prevention) - Caseworkers verify income and household composition from paystubs and data matches under state-specific rules. (Tier A; Verified; enterprise: pass)
- [Unemployment-insurance fraud and improper-payment triage](industries/government-public-safety.md#3-unemployment-insurance-fraud-and-improper-payment-triage) - Investigators work cross-match hits for identity theft, multistate claims and deceased claimants, then adjudicate and recover. (Tier A; Verified; enterprise: pass)
- [NEPA environmental-review document preparation](industries/government-public-safety.md#4-nepa-environmental-review-document-preparation) - Staff compile scoping, comment responses and cross-reference studies. (Tier A; Verified; enterprise: pass)
- [VA disability claims evidence review](industries/government-public-safety.md#5-va-disability-claims-evidence-review) - Rating staff read hundreds of pages of medical evidence, identify claimed conditions and match to diagnostic codes. (Tier A; Corrected; enterprise: pass)
- [Body-worn-camera footage review and redaction for public-records release](industries/government-public-safety.md#6-body-worn-camera-footage-review-and-redaction-for-public-records-release) - Staff scrub video and audio to blur faces, plates, minors and victims. (Tier B; Corrected; enterprise: pass)
- [Rulemaking public-comment analysis](industries/government-public-safety.md#7-rulemaking-public-comment-analysis) - Staff read, de-duplicate and categorize comments (including mass campaigns) and draft responses. (Tier A; Unconfirmed; enterprise: needs figure)
- [Authorization-to-operate (RMF/FedRAMP) package preparation](industries/government-public-safety.md#8-authorization-to-operate-rmffedramp-package-preparation) - ISSOs write control narratives, collect evidence and track POA&Ms by hand. (Tier A; Verified; enterprise: needs figure)
- [Personnel-vetting investigation preparation](industries/government-public-safety.md#9-personnel-vetting-investigation-preparation) - Staff compile and reconcile SF-86 data, records checks and interviews. (Tier B; Verified; enterprise: pass)
- [Medicaid renewal (ex parte) and procedural-denial prevention](industries/government-public-safety.md#10-medicaid-renewal-ex-parte-and-procedural-denial-prevention) - Caseworkers try data-based renewals, then send forms and chase responses. (Tier A; Verified; enterprise: pass)

**Open gaps (no matching open-source agent found)**

- FOIA / public-records request processing and redaction
- Unemployment-insurance fraud and improper-payment triage
- VA disability claims evidence review
- Body-worn-camera footage review and redaction for public-records release
- Rulemaking public-comment analysis
- Authorization-to-operate (RMF/FedRAMP) package preparation
- Personnel-vetting investigation preparation
- Medicaid renewal (ex parte) and procedural-denial prevention

<a name="healthcare-providers--payers"></a>
## Healthcare Providers & Payers

Hospitals, physician groups and health plans spend a large share of staff time on administrative work that sits between the clinical record and the payment: prior authorization, coding, claims denials, credentialing, quality reporting and directory upkeep. The work is manual because it needs unstructured clinical text, payer-specific rules and portal or fax submission, and each step has regulatory clocks. Manual effort concentrates in revenue cycle, utilization management and quality/compliance teams. CAQH 2023 Index (opened, PDF): medical-industry administrative spend $82.7B and $16.4B of savings available from full electronic processing [Verified, https://www.caqh.org/hubfs/drupal/2024-01/CAQH_IndexReport_2023_FINAL.pdf].

Full write-up with sources: [industries/healthcare-providers-payers.md](industries/healthcare-providers-payers.md)

**Enterprise problem statements**

- [Provider-side prior-authorization packet assembly and submission](industries/healthcare-providers-payers.md#1-provider-side-prior-authorization-packet-assembly-and-submission) - PA coordinators look up each payer's policy, pull notes, imaging and labs from the chart, fill payer-specific forms or portals, then chase status by phone or fax and handle appeals. (Tier A; Verified; enterprise: pass)
- [Hospital claim-denial analysis and appeal drafting](industries/healthcare-providers-payers.md#2-hospital-claim-denial-analysis-and-appeal-drafting) - Staff read denial codes, pull the documentation and contract language, and write appeal letters per claim, tracking deadlines in spreadsheets. (Tier A; Corrected; enterprise: pass)
- [Discharge medication reconciliation](industries/healthcare-providers-payers.md#3-discharge-medication-reconciliation) - Pharmacists and nurses compare home meds, inpatient orders, fill history and discharge instructions across screens, often under time pressure. (Tier B; Verified; enterprise: pass)
- [Payer utilization-management case review assist](industries/healthcare-providers-payers.md#4-payer-utilization-management-case-review-assist) - Nurse reviewers read submitted records against InterQual/MCG or plan policy, check eligibility and history, and write determination rationale under SLA clocks. (Tier A; Verified; enterprise: needs figure)
- [Coding and clinical documentation integrity (CDI) audit](industries/healthcare-providers-payers.md#5-coding-and-clinical-documentation-integrity-cdi-audit) - Coders and CDI specialists read entire charts to assign codes, spot missing specificity, and send physician queries; pre-bill audits sample only a fraction of charts. (Tier A; Unconfirmed; enterprise: needs figure)
- [Provider credentialing and payer enrollment](industries/healthcare-providers-payers.md#6-provider-credentialing-and-payer-enrollment) - Staff perform primary-source verification of licenses, board certifications, sanctions and work history across dozens of sites, then re-key data into payer enrollment forms. (Tier A; Unconfirmed; enterprise: needs figure)
- [Provider directory validation](industries/healthcare-providers-payers.md#7-provider-directory-validation) - Plans mail or call providers to confirm addresses, panels and phone numbers and reconcile conflicting sources. (Tier B; Unconfirmed; enterprise: needs figure)
- [HEDIS / quality measure chart abstraction and gap closure](industries/healthcare-providers-payers.md#8-hedis--quality-measure-chart-abstraction-and-gap-closure) - Nurses retrieve charts from provider offices during the annual hybrid-measure season and abstract results by hand for unresolved care gaps. (Tier A; Unconfirmed; enterprise: needs figure)
- [Claims payment integrity and pre-payment review](industries/healthcare-providers-payers.md#9-claims-payment-integrity-and-pre-payment-review) - Auditors review flagged claims, request records, compare to contract and coding rules, and write findings to providers. (Tier B; Corrected; enterprise: needs figure)
- [Medicare Advantage appeals and grievances case handling](industries/healthcare-providers-payers.md#10-medicare-advantage-appeals-and-grievances-case-handling) - Appeals staff gather the case file, check timeliness and jurisdiction, re-review against policy, and draft decision letters with required language. (Tier A; Unconfirmed; enterprise: needs figure)

**Open gaps (no matching open-source agent found)**

- Hospital claim-denial analysis and appeal drafting
- Payer utilization-management case review assist
- Coding and clinical documentation integrity (CDI) audit
- Provider credentialing and payer enrollment
- Provider directory validation
- Claims payment integrity and pre-payment review
- Medicare Advantage appeals and grievances case handling

<a name="hospitality--travel"></a>
## Hospitality & Travel

Airlines, hotels, tour operators and corporate travel managers spend effort on irregular operations, passenger-rights claims, settlement and reconciliation between carriers, agencies and platforms, and compliance reporting. Manual work concentrates in cross-system case handling (PSS, PMS, GDS, payments) where rules differ by jurisdiction and every payout or rejection must be explainable.

Full write-up with sources: [industries/hospitality-travel.md](industries/hospitality-travel.md)

**Enterprise problem statements**

- [Airline irregular operations (IROPS) passenger rebooking](industries/hospitality-travel.md#1-airline-irregular-operations-irops-passenger-rebooking) - After cancellations, agents and controllers rebook thousands of passengers across flights, partners and hotels under fare and entitlement rules. (Tier A; Verified; enterprise: pass)
- [EU261/UK261 and DOT compensation claim adjudication](industries/hospitality-travel.md#2-eu261uk261-and-dot-compensation-claim-adjudication) - Handlers establish arrival delay, distance band and "extraordinary circumstances" evidence, then pay or reject with reasons. (Tier A; Corrected; enterprise: needs figure)
- [Short-term rental registration compliance (EU 2024/1028)](industries/hospitality-travel.md#3-short-term-rental-registration-compliance-eu-20241028) - Staff match listings to registration numbers and flag invalid ones across jurisdictions. (Tier B; Corrected; enterprise: needs figure)
- [Baggage irregularity tracing and claims (WorldTracer)](industries/hospitality-travel.md#4-baggage-irregularity-tracing-and-claims-worldtracer) - Agents match files, contact passengers, authorize delivery and settle claims. (Tier A; Verified; enterprise: pass)
- [BSP settlement and agency debit memo (ADM) dispute handling](industries/hospitality-travel.md#5-bsp-settlement-and-agency-debit-memo-adm-dispute-handling) - Staff examine ADMs against fare rules and tickets and file disputes within short windows. (Tier A; Unconfirmed; enterprise: needs figure)
- [Aviation emissions MRV (EU ETS / CORSIA)](industries/hospitality-travel.md#6-aviation-emissions-mrv-eu-ets--corsia) - Analysts reconcile fuel uplift and flight lists into annual emissions reports. (Tier B; Corrected; enterprise: needs figure)
- [Multi-site food-safety compliance and inspection remediation](industries/hospitality-travel.md#7-multi-site-food-safety-compliance-and-inspection-remediation) - Managers track logs and inspection findings across sites. (Tier B; Corrected; enterprise: needs figure)
- [Corporate travel policy compliance and expense reconciliation](industries/hospitality-travel.md#8-corporate-travel-policy-compliance-and-expense-reconciliation) - Staff match bookings to receipts and chase out-of-policy trips. (Tier B; Search-excerpt; enterprise: needs figure)
- [OTA virtual-card chargeback and dispute response for hotels](industries/hospitality-travel.md#9-ota-virtual-card-chargeback-and-dispute-response-for-hotels) - Staff gather folios and no-show proof per network deadline. (Tier A; Unconfirmed; enterprise: needs figure)
- [Border-system disruption planning (EU Entry/Exit System)](industries/hospitality-travel.md#10-border-system-disruption-planning-eu-entryexit-system) - Teams forecast queues and rebook connections with patchy data. (Tier B; Corrected; enterprise: needs figure)

**Open gaps (no matching open-source agent found)**

- Airline irregular operations (IROPS) passenger rebooking
- EU261/UK261 and DOT compensation claim adjudication
- Short-term rental registration compliance (EU 2024/1028)
- Baggage irregularity tracing and claims (WorldTracer)
- BSP settlement and agency debit memo (ADM) dispute handling
- Aviation emissions MRV (EU ETS / CORSIA)
- Multi-site food-safety compliance and inspection remediation
- OTA virtual-card chargeback and dispute response for hotels
- Border-system disruption planning (EU Entry/Exit System)

<a name="hr--workforce"></a>
## HR & Workforce

HR and payroll teams spend effort on compliance-driven reconciliation: hiring records, work-authorization paperwork, pay calculations, leave and injury logs, and responses to regulators. Manual work concentrates in cross-checking HRIS, ATS, payroll and timekeeping data, and in documenting decisions for audits. Hiring and employee-decision use cases carry fairness and legal exposure, so every agent here keeps a human decision-maker.

Full write-up with sources: [industries/hr-workforce.md](industries/hr-workforce.md)

**Enterprise problem statements**

- [Hiring-decision bias monitoring across the applicant funnel](industries/hr-workforce.md#1-hiring-decision-bias-monitoring-across-the-applicant-funnel) - Analysts export stage-by-stage funnel data and compute adverse-impact ratios occasionally; screening tools themselves are rarely audited. (Tier B; Search-excerpt; enterprise: needs figure)
- [Automated employment decision tool (AEDT) compliance monitoring](industries/hr-workforce.md#2-automated-employment-decision-tool-aedt-compliance-monitoring) - Compliance staff manually find AEDT use, check for posted bias audits and candidate notices. (Tier A; Unconfirmed; enterprise: needs figure)
- [Public-sector time-to-hire orchestration](industries/hr-workforce.md#3-public-sector-time-to-hire-orchestration) - Specialists classify positions, screen against qualifications, schedule panels and chase clearances by email. (Tier A; Corrected; enterprise: needs figure)
- [Form I-9 audit and remediation](industries/hr-workforce.md#4-form-i-9-audit-and-remediation) - Reviewers check form completeness, document types and reverification dates across thousands of employees. (Tier A; Corrected; enterprise: needs figure)
- [Payroll and wage-and-hour error auditing](industries/hr-workforce.md#5-payroll-and-wage-and-hour-error-auditing) - Auditors sample pay periods for overtime, rounding, meal-break and deduction errors. (Tier A; Corrected; enterprise: pass)
- [Pay-equity analysis and EU Pay Transparency reporting](industries/hr-workforce.md#6-pay-equity-analysis-and-eu-pay-transparency-reporting) - Analysts build job-level pay comparisons in spreadsheets across countries. (Tier A; Corrected; enterprise: needs figure)
- [Discrimination charge response and workplace investigation case management](industries/hr-workforce.md#7-discrimination-charge-response-and-workplace-investigation-case-management) - Staff collect personnel files and communications and draft position statements under tight deadlines. (Tier A; Corrected; enterprise: pass)
- [OSHA injury recordkeeping and electronic submission](industries/hr-workforce.md#8-osha-injury-recordkeeping-and-electronic-submission) - Staff decide recordability (medical treatment, restricted work) and maintain logs. (Tier B; Verified; enterprise: pass)
- [Worker-classification (contractor vs employee) review](industries/hr-workforce.md#9-worker-classification-contractor-vs-employee-review) - Reviewers examine contractors one by one against multi-factor tests. (Tier A; Verified; enterprise: needs figure)
- [Leave (FMLA) and ADA accommodation case administration](industries/hr-workforce.md#10-leave-fmla-and-ada-accommodation-case-administration) - Specialists track eligibility, certifications, intermittent-leave usage and notice deadlines. (Tier A; Unconfirmed; enterprise: needs figure)

**Open gaps (no matching open-source agent found)**

- Public-sector time-to-hire orchestration
- Form I-9 audit and remediation
- Payroll and wage-and-hour error auditing
- Pay-equity analysis and EU Pay Transparency reporting
- Discrimination charge response and workplace investigation case management
- OSHA injury recordkeeping and electronic submission
- Worker-classification (contractor vs employee) review
- Leave (FMLA) and ADA accommodation case administration

<a name="insurance"></a>
## Insurance

Property and casualty, life and health insurers spend most operating effort on moving documents and decisions between intake, underwriting, claims and finance. Manual work concentrates in claims handling (first notice, investigation, recovery), commercial underwriting submissions, reinsurance reporting, and regulatory filings. Decisions are regulated by unfair-claims-practices law, so agents should prepare and recommend while licensed adjusters and underwriters decide.

Full write-up with sources: [industries/insurance.md](industries/insurance.md)

**Enterprise problem statements**

- [Claims fraud (SIU) investigation support](industries/insurance.md#1-claims-fraud-siu-investigation-support) - Investigators cross-check documents, invoices, prior-claim networks and public records and assemble a referral file by hand. (Tier A; Verified; enterprise: pass)
- [Claims first notice of loss (FNOL) intake and triage](industries/insurance.md#2-claims-first-notice-of-loss-fnol-intake-and-triage) - Intake staff collect loss facts by phone, email or portal, verify the policy, create the claim, set reserves and route to a handler. (Tier A; Unconfirmed; enterprise: needs figure)
- [Subrogation identification and recovery](industries/insurance.md#3-subrogation-identification-and-recovery) - Adjusters often close claims without noticing third-party liability; recovery staff read notes, collect evidence, send demands and chase payment. (Tier A; Unconfirmed; enterprise: needs figure)
- [Reinsurance bordereaux preparation and reconciliation](industries/insurance.md#4-reinsurance-bordereaux-preparation-and-reconciliation) - Analysts compile premium and loss bordereaux from several systems, map to each treaty's format, and reconcile differences by spreadsheet. (Tier B; Unconfirmed; enterprise: needs figure)
- [Commercial underwriting submission intake and triage](industries/insurance.md#5-commercial-underwriting-submission-intake-and-triage) - Underwriting assistants open emails and attachments (ACORD forms, SOVs, loss runs), re-key data, check appetite, and prioritise submissions. (Tier A; Unconfirmed; enterprise: needs figure)
- [Catastrophe claim surge handling](industries/insurance.md#6-catastrophe-claim-surge-handling) - After a hurricane or hail event, claim volumes spike; staff triage by hand, dispatch field adjusters and approve advance payments from partial information. (Tier A; Unconfirmed; enterprise: needs figure)
- [Bodily-injury claim demand-package review](industries/insurance.md#7-bodily-injury-claim-demand-package-review) - Adjusters read hundreds of pages of medical records and bills to build chronologies and evaluate demands against policy limits. (Tier A; Unconfirmed; enterprise: needs figure)
- [Rate and form filing preparation (SERFF)](industries/insurance.md#8-rate-and-form-filing-preparation-serff) - Analysts assemble state-specific filings, check each state's rules and objections, and respond to regulator questions. (Tier A; Unconfirmed; enterprise: needs figure)
- [Commercial premium audit](industries/insurance.md#9-commercial-premium-audit) - Auditors request payroll records, compare to estimates, reclassify exposure and compute final premium. (Tier B; Unconfirmed; enterprise: needs figure)
- [Coverage verification and reservation-of-rights drafting](industries/insurance.md#10-coverage-verification-and-reservation-of-rights-drafting) - Adjusters read policy forms and endorsements against loss facts and ask counsel to draft coverage position letters. (Tier A; Unconfirmed; enterprise: needs figure)

**Open gaps (no matching open-source agent found)**

- Subrogation identification and recovery
- Reinsurance bordereaux preparation and reconciliation
- Commercial underwriting submission intake and triage
- Catastrophe claim surge handling
- Bodily-injury claim demand-package review
- Rate and form filing preparation (SERFF)
- Commercial premium audit
- Coverage verification and reservation-of-rights drafting

<a name="legal--compliance"></a>
## Legal & Compliance

Corporate legal, privacy and compliance teams spend most effort on document-heavy review (contracts, e-discovery, vendor paper), deadline-driven obligations (DSARs, holds, regulator responses, IP renewals) and tracking regulatory change. Manual work concentrates where facts sit in many systems (email, DMS, CLM, HR, ERP) and a lawyer must still sign. All ten cases below keep a lawyer or DPO as the approver; none gives the agent legal judgement.

Full write-up with sources: [industries/legal-compliance.md](industries/legal-compliance.md)

**Enterprise problem statements**

- [GDPR data subject access request (DSAR) fulfilment](industries/legal-compliance.md#1-gdpr-data-subject-access-request-dsar-fulfilment) - Privacy analysts email system owners, search each store by name and identifiers, redact third-party data and compile the response by hand within a month. (Tier A; Verified; enterprise: pass)
- [Post-signature contract obligation tracking and value leakage](industries/legal-compliance.md#2-post-signature-contract-obligation-tracking-and-value-leakage) - Obligations (rebates, SLA credits, renewal notice windows, price indexation) sit in PDFs; staff rarely reconcile them with invoices. (Tier A; Corrected; enterprise: pass)
- [Privilege review in e-discovery](industries/legal-compliance.md#3-privilege-review-in-e-discovery) - Contract reviewers read millions of documents for responsiveness and privilege; senior lawyers QC samples and write the log. (Tier B; Unconfirmed; enterprise: needs figure)
- [Regulatory change management and obligation mapping](industries/legal-compliance.md#4-regulatory-change-management-and-obligation-mapping) - Analysts read regulator publications, decide applicability, map to policies and raise remediation tickets in spreadsheets. (Tier A; Unconfirmed; enterprise: needs figure)
- [Third-party / vendor privacy and security due diligence (GDPR Art. 28, DORA)](industries/legal-compliance.md#5-third-party--vendor-privacy-and-security-due-diligence-gdpr-art-28-dora) - Staff read questionnaires, SOC 2 reports and DPAs, compare against requirements, chase follow-ups. (Tier A; Unconfirmed; enterprise: needs figure)
- [Contract review against a negotiation playbook](industries/legal-compliance.md#6-contract-review-against-a-negotiation-playbook) - Lawyers read inbound third-party paper, compare each clause to the playbook, redline and escalate, often with a backlog before quarter end. (Tier A; Corrected; enterprise: pass)
- [Litigation hold issuance and preservation tracking](industries/legal-compliance.md#7-litigation-hold-issuance-and-preservation-tracking) - Paralegals identify custodians from org charts and interviews, send notices, chase acknowledgements, ask IT to suspend auto-deletion and re-issue as scope changes. (Tier A; Unconfirmed; enterprise: needs figure)
- [Trademark and patent prosecution docketing and deadline management](industries/legal-compliance.md#8-trademark-and-patent-prosecution-docketing-and-deadline-management) - Docketers read office actions and notices, calculate deadlines, enter them, and prepare instruction emails to outside counsel across jurisdictions. (Tier B; Unconfirmed; enterprise: needs figure)
- [Regulatory examination and subpoena response assembly](industries/legal-compliance.md#9-regulatory-examination-and-subpoena-response-assembly) - A request list with dozens of items is split across business owners; staff collect documents, reconcile answers across items and format responses. (Tier A; Unconfirmed; enterprise: needs figure)
- [Outside counsel invoice review against billing guidelines](industries/legal-compliance.md#10-outside-counsel-invoice-review-against-billing-guidelines) - Reviewers read time entries for block billing, duplicate work, unapproved staffing and rate breaches, then negotiate cuts. (Tier B; Corrected; enterprise: pass)

**Open gaps (no matching open-source agent found)**

- GDPR data subject access request (DSAR) fulfilment
- Post-signature contract obligation tracking and value leakage
- Litigation hold issuance and preservation tracking
- Regulatory examination and subpoena response assembly
- Outside counsel invoice review against billing guidelines

<a name="logistics--supply-chain"></a>
## Logistics & Supply Chain

Logistics spends most of its manual effort on documents that must agree with each other (commercial invoice, packing list, bill of lading, carrier invoice, customs entry) and on rules that change often (tariff actions, sanctions lists, carrier tariffs, FMC and FMCSA rules). Work concentrates in customs brokerage, trade-compliance teams, freight audit and payment, claims desks and carrier-management teams. Most decisions carry a statutory liability (penalties, bond claims, loss of refund rights), so a human sign-off is normal.

Full write-up with sources: [industries/logistics-supply-chain.md](industries/logistics-supply-chain.md)

**Enterprise problem statements**

- [Customs tariff (HTS) classification for import entries](industries/logistics-supply-chain.md#1-customs-tariff-hts-classification-for-import-entries) - A classifier reads product specs, applies the General Rules of Interpretation, searches CROSS rulings and section/chapter notes, then checks overlays such as Section 301 or 232 actions. (Tier A; Unconfirmed; enterprise: needs figure)
- [Freight invoice audit and accessorial-charge dispute](industries/logistics-supply-chain.md#2-freight-invoice-audit-and-accessorial-charge-dispute) - Auditors match carrier invoices (LTL, parcel, truckload) to contract rates, accessorial rules, BOL weights and proof of delivery, then email carriers to dispute wrong detention, liftgate, reweigh or duplicate charges. (Tier A; Unconfirmed; enterprise: needs figure)
- [UFLPA supply-chain tracing for detained shipments](industries/logistics-supply-chain.md#3-uflpa-supply-chain-tracing-for-detained-shipments) - After a detention, analysts chase POs, mill and farm records, transport documents and mass-balance data across supplier tiers and languages, then assemble a binder for CBP within tight windows. (Tier A; Corrected; enterprise: pass)
- [Ocean demurrage and detention (D&D) invoice validation and dispute](industries/logistics-supply-chain.md#4-ocean-demurrage-and-detention-dd-invoice-validation-and-dispute) - Staff compare invoice dates to free time, port closures, empty-return availability and gate events, then request waivers or refunds inside short windows. (Tier A; Verified; enterprise: needs figure)
- [Freight cargo loss-and-damage claims handling](industries/logistics-supply-chain.md#5-freight-cargo-loss-and-damage-claims-handling) - Claims staff gather BOL notations, photos, invoices and repair quotes, compute value, file with the carrier, and track acknowledgement and payment clocks by hand. (Tier A; Corrected; enterprise: needs figure)
- [Importer Security Filing (ISF) and entry document reconciliation](industries/logistics-supply-chain.md#6-importer-security-filing-isf-and-entry-document-reconciliation) - Clerks re-key and compare invoice, packing list, PO and BOL data, chase suppliers for missing HTS, manufacturer and consolidator details, and fix late or mismatching filings. (Tier B; Verified; enterprise: pass)
- [Restricted-party and export-control screening alert adjudication](industries/logistics-supply-chain.md#7-restricted-party-and-export-control-screening-alert-adjudication) - Screening produces large volumes of fuzzy-name hits; analysts check addresses, ownership percentages and end use to clear or escalate, logging reasons. (Tier A; Corrected; enterprise: pass)
- [Dangerous goods shipping-document compliance check](industries/logistics-supply-chain.md#8-dangerous-goods-shipping-document-compliance-check) - Specialists compare SDS data to the shipper's declaration, UN number, packing instruction and carrier limits, and reject or correct bookings. (Tier B; Unconfirmed; enterprise: needs figure)
- [Carrier onboarding and fraud vetting](industries/logistics-supply-chain.md#9-carrier-onboarding-and-fraud-vetting) - Staff check MC/DOT authority, insurance, address, phone and bank-change requests by hand to spot identity-theft carriers and double brokering. (Tier A; Verified; enterprise: pass)
- [Duty drawback claim preparation](industries/logistics-supply-chain.md#10-duty-drawback-claim-preparation) - Analysts match imports to later exports or destruction by part number, quantity and date across years, then compile claims within a five-year window. (Tier A; Verified; enterprise: pass)

**Open gaps (no matching open-source agent found)**

- Customs tariff (HTS) classification for import entries
- Freight invoice audit and accessorial-charge dispute
- UFLPA supply-chain tracing for detained shipments
- Ocean demurrage and detention (D&D) invoice validation and dispute
- Freight cargo loss-and-damage claims handling
- Importer Security Filing (ISF) and entry document reconciliation
- Dangerous goods shipping-document compliance check
- Carrier onboarding and fraud vetting
- Duty drawback claim preparation

<a name="manufacturing--industrial"></a>
## Manufacturing & Industrial

Plants spend effort on uptime, quality records, supplier management, product-compliance paperwork and safety/environmental reporting. Manual work concentrates where one engineer must join evidence from many systems (CMMS, QMS, ERP, PLM, historian) and write a signed record: CAPA files, supplier corrective actions, change-impact reviews, material declarations and regulatory filings. Most of these end in a human signature, which is why agents (retrieve, cross-check, draft, route for approval) fit better than a single model call.

Full write-up with sources: [industries/manufacturing.md](industries/manufacturing.md)

**Enterprise problem statements**

- [Maintenance troubleshooting and work-order drafting from manuals, CMMS history and sensor data](industries/manufacturing.md#1-maintenance-troubleshooting-and-work-order-drafting-from-manuals-cmms-history-and-sensor-data) - When a line stops, technicians search PDF manuals, old work orders and trends by hand, then request parts. (Tier A; Verified; enterprise: pass)
- [CAPA investigation and effectiveness checks (regulated plants)](industries/manufacturing.md#2-capa-investigation-and-effectiveness-checks-regulated-plants) - Quality engineers gather complaints, NCRs, batch records and audit findings, run root-cause analysis, write the CAPA and schedule effectiveness checks by hand. (Tier A; Verified; enterprise: pass)
- [Supplier embedded-emissions data collection for EU CBAM declarations](industries/manufacturing.md#3-supplier-embedded-emissions-data-collection-for-eu-cbam-declarations) - Teams chase non-EU suppliers by email for installation-level emissions, check them against default values and CN codes in spreadsheets. (Tier A; Verified; enterprise: needs figure)
- [Electronic component obsolescence and last-time-buy decisions](industries/manufacturing.md#4-electronic-component-obsolescence-and-last-time-buy-decisions) - Engineers track EOL notices by hand, hunt form-fit-function alternates and decide last-time-buy quantities across thousands of BOM lines. (Tier A; Corrected; enterprise: needs figure)
- [Tariff classification (HS code) and origin determination](industries/manufacturing.md#5-tariff-classification-hs-code-and-origin-determination) - Analysts classify thousands of parts from specs and drawings, search rulings and apply duty programs. (Tier B; Corrected; enterprise: pass)
- [Supplier corrective action (SCAR / 8D) review and escalation](industries/manufacturing.md#6-supplier-corrective-action-scar--8d-review-and-escalation) - Engineers read supplier 8D PDFs, judge whether root cause and containment are credible, chase late responses and update scorecards. (Tier A; Unconfirmed; enterprise: needs figure)
- [Product material compliance (REACH SVHC, RoHS, SCIP) across supplier declarations](industries/manufacturing.md#7-product-material-compliance-reach-svhc-rohs-scip-across-supplier-declarations) - Each Candidate List update (twice a year) requires re-checking every BOM item against supplier declarations by email and spreadsheet. (Tier A; Verified; enterprise: pass)
- [Engineering change order (ECO) impact analysis across BOM, inventory and compliance](industries/manufacturing.md#8-engineering-change-order-eco-impact-analysis-across-bom-inventory-and-compliance) - Engineers manually trace where-used, open orders, validation, labelling and certification impacts before a change board meets. (Tier A; Unconfirmed; enterprise: needs figure)
- [Process safety management of change (MOC) and PHA action tracking](industries/manufacturing.md#9-process-safety-management-of-change-moc-and-pha-action-tracking) - Engineers check each proposed change against P&IDs, prior PHAs and operating procedures, then chase open recommendations. (Tier A; Unconfirmed; enterprise: needs figure)
- [Environmental release reporting (TRI Form R / EPCRA) data assembly and QA](industries/manufacturing.md#10-environmental-release-reporting-tri-form-r--epcra-data-assembly-and-qa) - EHS staff compile thresholds, releases and waste-management quantities from multiple systems each year and reconcile against prior reports. (Tier B; Corrected; enterprise: pass)

**Open gaps (no matching open-source agent found)**

- CAPA investigation and effectiveness checks (regulated plants)
- Supplier embedded-emissions data collection for EU CBAM declarations
- Electronic component obsolescence and last-time-buy decisions
- Tariff classification (HS code) and origin determination
- Supplier corrective action (SCAR / 8D) review and escalation
- Product material compliance (REACH SVHC, RoHS, SCIP) across supplier declarations
- Engineering change order (ECO) impact analysis across BOM, inventory and compliance
- Process safety management of change (MOC) and PHA action tracking

<a name="media-entertainment--gaming"></a>
## Media, Entertainment & Gaming

Studios, labels, platforms, broadcasters and game publishers spend effort on rights and royalty accounting, content-policy enforcement, localization and compliance. Manual work concentrates in matching usage to rights holders across fragmented databases, per-decision reasoning for moderation and takedowns, and reconciling money flows between partners.

Full write-up with sources: [industries/media-entertainment-gaming.md](industries/media-entertainment-gaming.md)

**Enterprise problem statements**

- [Music sync rights clearance](industries/media-entertainment-gaming.md#1-music-sync-rights-clearance) - Coordinators identify each composition and master, trace splits, request quotes and track status. (Tier A; Unconfirmed; enterprise: needs figure)
- [Royalty statement reconciliation and audit](industries/media-entertainment-gaming.md#2-royalty-statement-reconciliation-and-audit) - Accountants match DSP lines to catalog, chase unmatched usage and reconcile payments. (Tier A; Verified; enterprise: pass)
- [DSA statements-of-reasons and moderation case handling](industries/media-entertainment-gaming.md#3-dsa-statements-of-reasons-and-moderation-case-handling) - Reviewers decide on flagged content and write a statement of reasons. (Tier A; Verified; enterprise: pass)
- [Online game harassment report triage](industries/media-entertainment-gaming.md#4-online-game-harassment-report-triage) - Moderators read report context and apply graduated sanctions. (Tier B; Verified; enterprise: needs figure)
- [Live-sports piracy detection and takedown](industries/media-entertainment-gaming.md#5-live-sports-piracy-detection-and-takedown) - Teams find streams during matches, verify rights and send notices in minutes. (Tier A; Search-excerpt; enterprise: needs figure)
- [Subtitle and dubbing localization QC](industries/media-entertainment-gaming.md#6-subtitle-and-dubbing-localization-qc) - Linguists check timing, terminology and style per language. (Tier B; Corrected; enterprise: needs figure)
- [Ad campaign delivery reconciliation and invoice dispute](industries/media-entertainment-gaming.md#7-ad-campaign-delivery-reconciliation-and-invoice-dispute) - Teams compare insertion orders to delivery and invoices. (Tier A; Verified; enterprise: pass)
- [Guild residuals and production payment compliance](industries/media-entertainment-gaming.md#8-guild-residuals-and-production-payment-compliance) - Staff compute residuals from contract tiers and exhibition data. (Tier A; Corrected; enterprise: needs figure)
- [Online gambling AML and responsible-gambling interventions](industries/media-entertainment-gaming.md#9-online-gambling-aml-and-responsible-gambling-interventions) - Analysts review alerts and affordability. (Tier A; Search-excerpt; enterprise: pass)
- [Accessibility compliance for video services (EAA)](industries/media-entertainment-gaming.md#10-accessibility-compliance-for-video-services-eaa) - Staff audit catalogs for captions and audio description. (Tier B; Search-excerpt; enterprise: needs figure)

**Open gaps (no matching open-source agent found)**

- Music sync rights clearance
- Royalty statement reconciliation and audit
- Live-sports piracy detection and takedown
- Ad campaign delivery reconciliation and invoice dispute
- Guild residuals and production payment compliance
- Accessibility compliance for video services (EAA)

<a name="nonprofit--social-impact"></a>
## Nonprofit & Social Impact

Nonprofits and NGOs spend a large share of staff time on funder-driven compliance (grant reporting, audits, registrations), casework intake, and reconciling data between field systems and finance. Manual work concentrates in eligibility screening, document chasing, and turning program data into regulator- or funder-ready reports. Consumer-facing benefits navigation was deliberately excluded; every use case below has an organizational buyer (legal-aid org, CoC lead agency, international NGO, foundation, charity finance team).

Full write-up with sources: [industries/nonprofit.md](industries/nonprofit.md)

**Enterprise problem statements**

- [Legal-aid intake, triage and referral](industries/nonprofit.md#1-legal-aid-intake-triage-and-referral) - Intake staff phone-screen callers for income eligibility, issue type and conflicts, then manually compute deadlines (e.g., eviction answer dates) and refer. (Tier A; Verified; enterprise: pass)
- [Humanitarian needs assessment and appeal prioritization](industries/nonprofit.md#2-humanitarian-needs-assessment-and-appeal-prioritization) - Analysts consolidate heterogeneous assessments, displacement figures and 3W data into severity tables and funding appeals, largely in spreadsheets, under tight annual cycle deadlines. (Tier A; Corrected; enterprise: pass)
- [Homelessness coordinated entry and housing placement](industries/nonprofit.md#3-homelessness-coordinated-entry-and-housing-placement) - Staff assess households, track documents (ID, income, disability verification), prioritize by vulnerability and phone landlords, in HMIS plus spreadsheets. (Tier B; Search-excerpt; enterprise: needs figure)
- [Federal-grant compliance and Single Audit readiness](industries/nonprofit.md#4-federal-grant-compliance-and-single-audit-readiness) - Finance staff match ledger entries to award terms and supporting documents (time allocations, procurement files) and compile schedules of expenditures of federal awards by hand before audit. (Tier A; Unconfirmed; enterprise: needs figure)
- [Funder reporting and outcomes consolidation](industries/nonprofit.md#5-funder-reporting-and-outcomes-consolidation) - Each funder wants a different template; staff re-key program outputs and narratives from several systems quarterly. (Tier B; Verified; enterprise: needs figure)
- [Cash-assistance registration, deduplication and payment reconciliation](industries/nonprofit.md#6-cash-assistance-registration-deduplication-and-payment-reconciliation) - Overlapping partners register the same households; staff dedupe lists in Excel and reconcile FSP payment files against targeted lists. (Tier A; Corrected; enterprise: pass)
- [Form 990 preparation and multi-state charity registration](industries/nonprofit.md#7-form-990-preparation-and-multi-state-charity-registration) - Staff rebuild 990 schedules from the ledger and file state registrations/renewals with differing forms and due dates. (Tier A; Verified; enterprise: needs figure)
- [UK Gift Aid claim preparation and donor-declaration audit](industries/nonprofit.md#8-uk-gift-aid-claim-preparation-and-donor-declaration-audit) - Teams match donations to valid declarations, fix address/name mismatches and submit claims; errors cause clawback. (Tier B; Verified; enterprise: pass)
- [Partner and vendor due diligence with sanctions screening for international NGOs](industries/nonprofit.md#9-partner-and-vendor-due-diligence-with-sanctions-screening-for-international-ngos) - Staff screen sub-recipients and vendors by name against lists, research ownership, and document the decision for donors. (Tier A; Unconfirmed; enterprise: needs figure)
- [Foundation cross-border grant due diligence (equivalency determination)](industries/nonprofit.md#10-foundation-cross-border-grant-due-diligence-equivalency-determination) - Staff collect foreign charity documents, compare governance and charitable-purpose requirements to US equivalents, and draft a determination memo. (Tier A; Verified; enterprise: needs figure)

**Open gaps (no matching open-source agent found)**

- Legal-aid intake, triage and referral
- Humanitarian needs assessment and appeal prioritization
- Federal-grant compliance and Single Audit readiness
- Funder reporting and outcomes consolidation
- Cash-assistance registration, deduplication and payment reconciliation
- Foundation cross-border grant due diligence (equivalency determination)

<a name="oil-gas--mining"></a>
## Oil, Gas & Mining

Operators in upstream oil and gas, pipelines and mining spend heavy effort on safety and environmental compliance, permits, and reserve/regulatory reporting. Manual work concentrates in reading inspection and incident narratives, assembling filings from field and geoscience systems, and tracking regulator deadlines. Errors carry criminal or large civil exposure, so humans sign.

Full write-up with sources: [industries/oil-gas-mining.md](industries/oil-gas-mining.md)

**Enterprise problem statements**

- [Methane leak detection (LDAR) and super-emitter response](industries/oil-gas-mining.md#1-methane-leak-detection-ldar-and-super-emitter-response) - Staff correlate OGI surveys, continuous monitors and third-party alerts with assets, dispatch crews, track repair deadlines and write reports. (Tier A; Corrected; enterprise: pass)
- [HSE incident investigation and trend analysis](industries/oil-gas-mining.md#2-hse-incident-investigation-and-trend-analysis) - Investigators read narratives, pull permits and maintenance history, assign causes and corrective actions; trending across sites is manual. (Tier A; Unconfirmed; enterprise: needs figure)
- [Well integrity review](industries/oil-gas-mining.md#3-well-integrity-review) - Engineers review sustained casing pressure, logs and test results to decide on remediation, a mostly document-driven judgment. (Tier A; Unconfirmed; enterprise: needs figure)
- [Mineral reserve and resource reporting (S-K 1300 / JORC / NI 43-101)](industries/oil-gas-mining.md#4-mineral-reserve-and-resource-reporting-s-k-1300--jorc--ni-43-101) - Geologists/engineers reconcile models, price assumptions and cost data into technical reports and check consistency with prior filings. (Tier B; Verified; enterprise: needs figure)
- [Drilling and mining permit application assembly](industries/oil-gas-mining.md#5-drilling-and-mining-permit-application-assembly) - Land and regulatory staff assemble APD/plan-of-operations packages from surveys, lease maps, environmental studies and prior permits. (Tier A; Unconfirmed; enterprise: needs figure)
- [Environmental compliance monitoring and exceedance reporting](industries/oil-gas-mining.md#6-environmental-compliance-monitoring-and-exceedance-reporting) - Staff compare lab and monitor results against permit limits, investigate exceedances and prepare agency reports. (Tier A; Unconfirmed; enterprise: needs figure)
- [Royalty and production regulatory reporting reconciliation](industries/oil-gas-mining.md#7-royalty-and-production-regulatory-reporting-reconciliation) - Accountants reconcile volumes, prices and allowances across systems and fix report rejections. (Tier B; Unconfirmed; enterprise: needs figure)
- [Pipeline integrity: in-line inspection anomaly dig prioritization](industries/oil-gas-mining.md#8-pipeline-integrity-in-line-inspection-anomaly-dig-prioritization) - Engineers align ILI runs, apply remaining-strength calcs and decide which anomalies to excavate within regulatory deadlines. (Tier B; Unconfirmed; enterprise: needs figure)
- [Process safety: management of change (MOC) and PHA review](industries/oil-gas-mining.md#9-process-safety-management-of-change-moc-and-pha-review) - Engineers check each change against PHA, P&IDs and procedures, manually updating affected documents. (Tier A; Verified; enterprise: needs figure)
- [Orphan, idle well and asset-retirement obligation tracking](industries/oil-gas-mining.md#10-orphan-idle-well-and-asset-retirement-obligation-tracking) - Staff reconcile idle wells, plugging cost estimates and bonds across state records and ERP. (Tier B; Unconfirmed; enterprise: needs figure)

**Open gaps (no matching open-source agent found)**

- HSE incident investigation and trend analysis
- Well integrity review
- Mineral reserve and resource reporting (S-K 1300 / JORC / NI 43-101)
- Drilling and mining permit application assembly
- Environmental compliance monitoring and exceedance reporting
- Royalty and production regulatory reporting reconciliation
- Pipeline integrity: in-line inspection anomaly dig prioritization
- Process safety: management of change (MOC) and PHA review
- Orphan, idle well and asset-retirement obligation tracking

<a name="pharma-biotech--life-sciences"></a>
## Pharma, Biotech & Life Sciences

Drug and device developers spend most non-laboratory effort on documents and compliance: safety case processing, trial operations, regulatory dossiers and quality records. Work concentrates in pharmacovigilance, clinical operations, regulatory affairs and quality assurance, where every step must be traceable and validated. Fixed regulatory clocks (for example expedited safety reports) and very expensive failures (the FY2027 PDUFA application fee with clinical data is $4,600,753, confirmed on RAPS) make errors costly, so agents must keep humans in the approval loop.

Full write-up with sources: [industries/pharma-biotech.md](industries/pharma-biotech.md)

**Enterprise problem statements**

- [Pharmacovigilance adverse-event case intake and triage](industries/pharma-biotech.md#1-pharmacovigilance-adverse-event-case-intake-and-triage) - Case processors read unstructured reports, code terms to MedDRA, search for duplicates, write narratives and prepare expedited reports under 15-day clocks. (Tier A; Verified; enterprise: pass)
- [Clinical-trial eligibility screening against free-text records](industries/pharma-biotech.md#2-clinical-trial-eligibility-screening-against-free-text-records) - Coordinators read charts against long inclusion/exclusion lists to find candidates; slow recruitment delays trials. (Tier A; Unconfirmed; enterprise: needs figure)
- [Regulatory submission (eCTD) assembly and consistency check](industries/pharma-biotech.md#3-regulatory-submission-ectd-assembly-and-consistency-check) - Teams cross-check module 2 summaries against modules 3-5, verify numbers, hyperlinks and cross-references, and prepare responses to agency questions. (Tier A; Verified; enterprise: pass)
- [Clinical trial site feasibility and selection](industries/pharma-biotech.md#4-clinical-trial-site-feasibility-and-selection) - Feasibility managers send questionnaires, collect answers by email, compare with past performance, and compile a ranked list. (Tier B; Unconfirmed; enterprise: needs figure)
- [GxP deviation investigation and CAPA drafting](industries/pharma-biotech.md#5-gxp-deviation-investigation-and-capa-drafting) - QA investigators collect batch, equipment and training records, find similar past deviations, run root-cause analysis and write reports within site timelines. (Tier A; Unconfirmed; enterprise: needs figure)
- [Safety literature surveillance](industries/pharma-biotech.md#6-safety-literature-surveillance) - Scientists run saved searches weekly, read abstracts and full texts, identify case reports, and log screening decisions for audit. (Tier A; Unconfirmed; enterprise: needs figure)
- [Clinical protocol authoring and amendment impact analysis](industries/pharma-biotech.md#7-clinical-protocol-authoring-and-amendment-impact-analysis) - A protocol change must be traced to the schedule of assessments, ICF, EDC forms, site contracts and registry records, mostly manually. (Tier A; Corrected; enterprise: pass)
- [Clinical data review and query management](industries/pharma-biotech.md#8-clinical-data-review-and-query-management) - Data managers run edit checks, review listings, and write queries to sites that must be tracked to closure. (Tier B; Unconfirmed; enterprise: needs figure)
- [Promotional material medical-legal-regulatory (MLR) review](industries/pharma-biotech.md#9-promotional-material-medical-legal-regulatory-mlr-review) - Reviewers check every claim against the label and cited references, then annotate rounds of comments. (Tier A; Unconfirmed; enterprise: needs figure)
- [Global regulatory change control and label variation tracking](industries/pharma-biotech.md#10-global-regulatory-change-control-and-label-variation-tracking) - Each manufacturing or label change must be assessed per country, classified, and tracked to approval and implementation across markets. (Tier A; Unconfirmed; enterprise: needs figure)

**Open gaps (no matching open-source agent found)**

- Clinical trial site feasibility and selection
- GxP deviation investigation and CAPA drafting
- Safety literature surveillance
- Clinical protocol authoring and amendment impact analysis
- Clinical data review and query management
- Promotional material medical-legal-regulatory (MLR) review
- Global regulatory change control and label variation tracking

<a name="real-estate"></a>
## Real Estate

Real estate work is document-heavy and transaction-driven: leases, title chains, loan files, appraisals, plan sets and draw packages are read, cross-checked and re-keyed by people before money moves or a filing is accepted. Manual effort concentrates at the handoffs between systems (lease admin to ERP, title plant to underwriter, LOS to investor, plan portal to code library). Errors are costly because they become financial-reporting misstatements, defective loans, fair-housing liability, or stolen closing funds.

Full write-up with sources: [industries/real-estate.md](industries/real-estate.md)

**Enterprise problem statements**

- [Commercial lease abstraction and lease-accounting data](industries/real-estate.md#1-commercial-lease-abstraction-and-lease-accounting-data) - Lease administrators read the base lease plus every amendment to extract rent steps, options, CAM caps and critical dates, then key them into the lease system. (Tier A; Verified; enterprise: pass)
- [Closing wire-fraud and payoff verification](industries/real-estate.md#2-closing-wire-fraud-and-payoff-verification) - Escrow officers verify wiring instructions and lender payoff letters, which fraudsters spoof via email, using callbacks and spot checks. (Tier A; Verified; enterprise: pass)
- [Municipal building-permit plan review](industries/real-estate.md#3-municipal-building-permit-plan-review) - Reviewers check drawings against zoning and building codes over multiple correction rounds; applicants resubmit. (Tier A; Verified; enterprise: pass)
- [Tenant screening accuracy and FCRA dispute handling](industries/real-estate.md#4-tenant-screening-accuracy-and-fcra-dispute-handling) - Analysts match applicants to eviction/criminal records and investigate disputes within statutory time limits. (Tier B; Corrected; enterprise: pass)
- [Mortgage loan file assembly and condition clearing](industries/real-estate.md#5-mortgage-loan-file-assembly-and-condition-clearing) - Processors collect income, asset and appraisal documents, reconcile discrepancies and clear underwriting conditions against agency guidelines. (Tier A; Verified; enterprise: pass)
- [Title examination and curative-item tracking](industries/real-estate.md#6-title-examination-and-curative-item-tracking) - Examiners trace the chain of title through recorded deeds, mortgages, liens and judgments, list exceptions, then chase curative documents. (Tier A; Verified; enterprise: pass)
- [Fair-housing compliance review of listings and ad campaigns](industries/real-estate.md#7-fair-housing-compliance-review-of-listings-and-ad-campaigns) - Compliance staff manually spot-check listing text, targeting settings and photos for discriminatory content or steering. (Tier B; Corrected; enterprise: pass)
- [Appraisal review and reconsideration-of-value handling](industries/real-estate.md#8-appraisal-review-and-reconsideration-of-value-handling) - Reviewers check appraisal reports for comparable selection, UAD errors and prohibited language and handle borrower ROV requests. (Tier B; Corrected; enterprise: needs figure)
- [CRE rent-roll and T-12 underwriting plus covenant monitoring](industries/real-estate.md#9-cre-rent-roll-and-t-12-underwriting-plus-covenant-monitoring) - Analysts normalize borrower rent rolls and operating statements, tie them to leases, and flag DSCR and occupancy covenant breaches. (Tier A; Corrected; enterprise: pass)
- [Construction-loan draw package review](industries/real-estate.md#10-construction-loan-draw-package-review) - Staff match draw requests, invoices, lien waivers and inspector percent-complete reports before each disbursement. (Tier A; Verified; enterprise: needs figure)

**Open gaps (no matching open-source agent found)**

- Commercial lease abstraction and lease-accounting data
- Closing wire-fraud and payoff verification
- Tenant screening accuracy and FCRA dispute handling
- Mortgage loan file assembly and condition clearing
- Title examination and curative-item tracking
- Fair-housing compliance review of listings and ad campaigns
- Appraisal review and reconsideration-of-value handling
- CRE rent-roll and T-12 underwriting plus covenant monitoring
- Construction-loan draw package review

<a name="retail--e-commerce"></a>
## Retail & E-commerce

Retailers and marketplaces spend manual effort on exceptions: returns that may be fraudulent, disputed card payments, supplier deductions, product-safety and chemical rules, seller verification and recalls. Work concentrates in loss prevention, payments/dispute operations, vendor compliance, trust-and-safety and regulatory-affairs teams. Each case needs evidence pulled from several systems (order, carrier, payment, catalog, ERP), and many have regulatory clocks or financial penalties.

Full write-up with sources: [industries/retail-ecommerce.md](industries/retail-ecommerce.md)

**Enterprise problem statements**

- [Returns processing and returns-fraud adjudication](industries/retail-ecommerce.md#1-returns-processing-and-returns-fraud-adjudication) - Analysts check receipts, serial numbers, return history and condition photos to separate wardrobing, receipt fraud and bracketing from legitimate returns, and decide refund, restock or deny. (Tier B; Corrected; enterprise: pass)
- [Card-payment chargeback representment](industries/retail-ecommerce.md#2-card-payment-chargeback-representment) - Analysts map each reason code to required evidence, pull delivery proof, device/IP data and customer messages, and upload a packet before the response window closes. (Tier A; Verified; enterprise: pass)
- [EU GPSR marketplace product-safety compliance](industries/retail-ecommerce.md#3-eu-gpsr-marketplace-product-safety-compliance) - Staff monitor Safety Gate alerts, search for matching or identical listings, request missing trader and safety data, and respond to authority orders. (Tier A; Corrected; enterprise: needs figure)
- [Store inventory shrink and record-accuracy investigation](industries/retail-ecommerce.md#4-store-inventory-shrink-and-record-accuracy-investigation) - Analysts trace shrink to theft, process errors, vendor fraud or record errors by joining POS voids, receiving and counts. (Tier B; Corrected; enterprise: pass)
- [Counterfeit and IP notice-and-takedown handling for marketplaces](industries/retail-ecommerce.md#5-counterfeit-and-ip-notice-and-takedown-handling-for-marketplaces) - Analysts validate rights-holder claims, match listings, remove or reject, and handle counter-notices. (Tier A; Unconfirmed; enterprise: needs figure)
- [Vendor deduction and OTIF fine dispute](industries/retail-ecommerce.md#6-vendor-deduction-and-otif-fine-dispute) - Analysts reconcile deductions to POs, ASNs and delivery receipts, and file disputes inside portal deadlines. (Tier A; Verified; enterprise: pass)
- [Product recall execution and effectiveness tracking](industries/retail-ecommerce.md#7-product-recall-execution-and-effectiveness-tracking) - Teams map recalled SKUs and lots to stores and customers, block sales at POS, send notices and track returns and regulator reports. (Tier A; Verified; enterprise: pass)
- [High-volume seller verification (INFORM Consumers Act)](industries/retail-ecommerce.md#8-high-volume-seller-verification-inform-consumers-act) - Analysts detect sellers crossing 200 sales / $5,000 revenue, collect bank, tax and contact data, verify it, require annual certification and suspend non-responders. (Tier A; Verified; enterprise: pass)
- [Product chemical-restriction and Prop 65 compliance](industries/retail-ecommerce.md#9-product-chemical-restriction-and-prop-65-compliance) - Analysts read supplier lab reports, compare substances to Prop 65 and other restricted lists, add warnings and respond to notices. (Tier B; Unconfirmed; enterprise: needs figure)
- [FSMA 204 food traceability record assembly](industries/retail-ecommerce.md#10-fsma-204-food-traceability-record-assembly) - Staff chase suppliers for lot and location data and build trace records during outbreaks. (Tier B; Corrected; enterprise: needs figure)

**Open gaps (no matching open-source agent found)**

- Returns processing and returns-fraud adjudication
- Card-payment chargeback representment
- EU GPSR marketplace product-safety compliance
- Store inventory shrink and record-accuracy investigation
- Counterfeit and IP notice-and-takedown handling for marketplaces
- Vendor deduction and OTIF fine dispute
- Product recall execution and effectiveness tracking
- High-volume seller verification (INFORM Consumers Act)
- Product chemical-restriction and Prop 65 compliance
- FSMA 204 food traceability record assembly

<a name="software-development--devops"></a>
## Software Development & DevOps

Large engineering organisations spend effort on keeping a huge estate current (dependencies, language versions, legacy code), keeping production up (incidents, CI health), and proving control (change approval, code review). Manual work concentrates in repetitive, multi-repo changes and in evidence gathering across CI/CD, ITSM and observability tools. In all ten cases an engineer or change board approves merges, deploys or deletions.

Full write-up with sources: [industries/software-devops.md](industries/software-devops.md)

**Enterprise problem statements**

- [Legacy COBOL/mainframe migration](industries/software-devops.md#1-legacy-cobolmainframe-migration) - Scarce engineers reverse-engineer undocumented logic, rewrite it and prove equivalence by manual comparison. (Tier A; Verified; enterprise: pass)
- [Incident root-cause analysis and postmortem drafting](industries/software-devops.md#2-incident-root-cause-analysis-and-postmortem-drafting) - On-call engineers correlate metrics, logs, traces and recent deploys, then spend hours reconstructing a timeline. (Tier A; Corrected; enterprise: pass)
- [Vulnerable-dependency / CVE remediation pull requests across a repo estate](industries/software-devops.md#3-vulnerable-dependency--cve-remediation-pull-requests-across-a-repo-estate) - Teams get thousands of alerts; someone picks safe versions, fixes breaking API changes and runs tests. (Tier A; Verified; enterprise: pass)
- [Cloud cost (FinOps) anomaly investigation and rightsizing](industries/software-devops.md#4-cloud-cost-finops-anomaly-investigation-and-rightsizing) - Engineers trace spikes to teams and judge whether resources are safe to remove. (Tier A; Verified; enterprise: pass)
- [Language and framework upgrade migration (e.g. Java 8 to 17)](industries/software-devops.md#5-language-and-framework-upgrade-migration-eg-java-8-to-17) - Teams upgrade each service by hand: build fixes, API replacements, dependency bumps. (Tier A; Verified; enterprise: pass)
- [Change-request risk review and audit evidence assembly](industries/software-devops.md#6-change-request-risk-review-and-audit-evidence-assembly) - Change managers manually link tickets to PRs, test evidence and approvals, and judge risk. (Tier B; Unconfirmed; enterprise: needs figure)
- [Static-analysis (SAST) finding auto-remediation](industries/software-devops.md#7-static-analysis-sast-finding-auto-remediation) - Developers triage scanner alerts and hand-fix common vulnerability classes. (Tier A; Verified; enterprise: pass)
- [Policy-aware pull-request review at scale](industries/software-devops.md#8-policy-aware-pull-request-review-at-scale) - Reviewers check style, security, licensing and ticket linkage manually; queues delay delivery. (Tier B; Unconfirmed; enterprise: needs figure)

**Open gaps (no matching open-source agent found)**

- Change-request risk review and audit evidence assembly

<a name="telecom--networks"></a>
## Telecom & Networks

Telecom operators spend manual effort on network operations (alarm triage, change control, energy), subscriber protection (SIM-swap, fraud, robocalls) and regulatory work (outage reporting, broadband maps, legal demands, pole attachments). Work concentrates in NOCs, fraud and revenue-assurance teams, regulatory and legal departments, and network engineering. Networks are safety-relevant, so almost every automated action needs change control and a human approval gate.

Full write-up with sources: [industries/telecom.md](industries/telecom.md)

**Enterprise problem statements**

- [Network fault root-cause analysis from alarm storms](industries/telecom.md#1-network-fault-root-cause-analysis-from-alarm-storms) - NOC engineers triage thousands of correlated RAN, transport and core alarms by hand to find the failing element or recent change. (Tier A; Verified; enterprise: needs figure)
- [SIM-swap and port-out fraud authentication](industries/telecom.md#2-sim-swap-and-port-out-fraud-authentication) - Agents verify callers before SIM changes or ports; fraudsters social-engineer them. (Tier A; Verified; enterprise: needs figure)
- [Telecom fraud and revenue-assurance investigation (IRSF, Wangiri, bypass)](industries/telecom.md#3-telecom-fraud-and-revenue-assurance-investigation-irsf-wangiri-bypass) - Analysts review anomaly alerts, check number ranges, block routes and negotiate disputes. (Tier B; Unconfirmed; enterprise: needs figure)
- [Broadband availability map challenge adjudication](industries/telecom.md#4-broadband-availability-map-challenge-adjudication) - Staff review location-level challenges and assemble engineering evidence or concede. (Tier A; Verified; enterprise: pass)
- [Robocall mitigation filing and traceback response](industries/telecom.md#5-robocall-mitigation-filing-and-traceback-response) - Staff keep RMD filings accurate, answer traceback requests and vet upstream customers. (Tier A; Verified; enterprise: pass)
- [Legal-demand (subpoena and warrant) response processing](industries/telecom.md#6-legal-demand-subpoena-and-warrant-response-processing) - Analysts validate legal process, scope the data, pull records, redact and respond within deadlines. (Tier A; Verified; enterprise: pass)
- [Network change-request validation](industries/telecom.md#7-network-change-request-validation) - Engineers assess change risk, review method-of-procedure steps and set rollback plans manually. (Tier A; Verified; enterprise: pass)
- [Pole-attachment and make-ready application management](industries/telecom.md#8-pole-attachment-and-make-ready-application-management) - Teams track applications, surveys, estimates and make-ready steps manually. (Tier B; Unconfirmed; enterprise: needs figure)
- [Outage-reporting (NORS) determination and filing](industries/telecom.md#9-outage-reporting-nors-determination-and-filing) - Staff decide whether an incident meets thresholds and compile notifications and final reports. (Tier A; Corrected; enterprise: pass)

**Open gaps (no matching open-source agent found)**

- Network fault root-cause analysis from alarm storms
- SIM-swap and port-out fraud authentication
- Telecom fraud and revenue-assurance investigation (IRSF, Wangiri, bypass)
- Broadband availability map challenge adjudication
- Robocall mitigation filing and traceback response
- Legal-demand (subpoena and warrant) response processing
- Network change-request validation
- Pole-attachment and make-ready application management
- Outage-reporting (NORS) determination and filing
