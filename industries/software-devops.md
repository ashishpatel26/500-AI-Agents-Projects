# Software Development & DevOps

## Overview
Large engineering organisations spend effort on keeping a huge estate current (dependencies, language versions, legacy code), keeping production up (incidents, CI health), and proving control (change approval, code review). Manual work concentrates in repetitive, multi-repo changes and in evidence gathering across CI/CD, ITSM and observability tools. In all ten cases an engineer or change board approves merges, deploys or deletions.

Verification note: GitHub search was rate-limited (HTTP 403) during the run, so cases 6-10 say "not searched". Seeded repos (cases 1-5) are carried from earlier research.

## Systems of record, regulations, public datasets
- **Systems:** Git hosting (GitHub, GitLab), CI/CD (Jenkins, GitHub Actions), artifact registries, observability (Datadog, Prometheus, Grafana), incident tools (PagerDuty), ITSM (ServiceNow change/CMDB), IaC (Terraform), cloud billing, issue trackers.
- **Regulations/standards:** SOX IT general controls (change management); PCI DSS v4.0 req 6 (secure development, code review); DORA (2022/2554) ICT change management; ISO/IEC 27001:2022 A.8.32; SOC 2 CC8.1; EU Cyber Resilience Act (2024).
- **Public datasets:** SWE-bench https://www.swebench.com ; GitHub Archive https://www.gharchive.org ; deps.dev https://deps.dev ; OSV https://osv.dev ; Defects4J https://github.com/rjust/defects4j ; GitHub Actions logs from open-source repos; Loghub https://github.com/logpai/loghub ; AWS Open Data cost samples; Google SRE postmortem collection https://github.com/danluu/post-mortems .

## Use cases

### 1. Legacy COBOL/mainframe migration
- **Tier:** A | Enterprise: pass
- **Enterprise check:** Buyer: banks, insurers, governments. Systems: mainframe (CICS, Db2, JCL), source control, test environments. Regulation: change control and model-risk expectations; payment correctness. Human: engineers sign behavioural equivalence.
- **Problem and today's workflow:** Scarce engineers reverse-engineer undocumented logic, rewrite it and prove equivalence by manual comparison.
- **Evidence:** BMC quoting Reuters: "220 billion lines of code still in production"; Commonwealth Bank "replaced its core COBOL platform in 2012, it took five years and cost $749.9 million". Secondary, 2017-2020 era. https://www.bmc.com/blogs/cobol-trends/ [Verified]
- **Agent design:** Parse and map dependencies, extract business rules, generate target code, generate characterisation tests against legacy output, iterate. Humans approve equivalence.
- **Open source today:** squid-protocol/gitgalaxy (63 stars, licence NOASSERTION, not archived, last push 2026-11-05; README read: yes; addresses partly: repo scanner feeding a CICS-to-Java translator); opensourcecobol/opensourcecobol4j (126 stars, GPL-3.0, not archived, last push 2026-10-29; README read: yes; adjacent only: deterministic COBOL-to-Java compiler).
- **Demo path:** GnuCOBOL test suite and public COBOL samples; compare outputs with the translated Java.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 2. Incident root-cause analysis and postmortem drafting
- **Tier:** A | Enterprise: pass
- **Enterprise check:** Buyer: SRE/platform org. Systems: observability, deploy history (CI/CD), PagerDuty, runbooks, ITSM. Regulation: DORA major-incident records, SLA credits, audit trail. Human: on-call approves any rollback or remediation.
- **Problem and today's workflow:** On-call engineers correlate metrics, logs, traces and recent deploys, then spend hours reconstructing a timeline.
- **Evidence:** Uptime Institute 2025 via Data Center Knowledge: "53% of operators reported an outage in the past three years"; "human error accounts for two-thirds to three-quarters of all outages". The 85% procedures figure was not on the page and is removed. https://www.datacenterknowledge.com/outages/data-center-outages-decline-for-fourth-straight-year-but-issues-persist [Corrected]
- **Agent design:** Hypothesis-test loop over read-only observability tools and change history; propose remediation; draft blameless postmortem. On-call approves actions.
- **Open source today:** Tommy-yw/RunbookHermes (510 stars, MIT, not archived, last push 2026-05-18; README read: yes; addresses: SRE incident-response agent with evidence-based RCA and approval-gated execution); aws/tools-for-devops-agent (137 stars, Apache-2.0, not archived, last push 2026-11-05; README read: yes; adjacent only: extensions for AWS DevOps Agent, vendor-tied).
- **Demo path:** OpenTelemetry Demo (https://github.com/open-telemetry/opentelemetry-demo) with fault injection flags.
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 3. Vulnerable-dependency / CVE remediation pull requests across a repo estate
- **Tier:** A | Enterprise: pass
- **Enterprise check:** Buyer: engineering and AppSec. Systems: GitHub/GitLab, Dependabot/Renovate, SCA scanner, CI, artifact registry. Regulation: PCI DSS 6.3.3, CRA, customer SLAs. Human: maintainers review and merge.
- **Problem and today's workflow:** Teams get thousands of alerts; someone picks safe versions, fixes breaking API changes and runs tests.
- **Evidence:** Sonatype 10th State of the Software Supply Chain: "95% of the time, when vulnerable components are consumed, a fixed version already exists"; "80% of application dependencies remain un-upgraded for over a year". Vendor report. https://www.sonatype.com/en/press-releases/sonatypes-10th-annual-state-of-the-software-supply-chain-report [Verified]
- **Agent design:** Choose a target version using changelogs and deps.dev, patch code, run tests, iterate, open PR with risk notes. Maintainer merges; no auto-merge.
- **Open source today:** wemake-services/kira-dependencies (109 stars, MIT, not archived, last push 2025-08-08; README read: yes; adjacent only: GitLab dependency-update bot, dependabot-script fork, not LLM).
- **Demo path:** Repos with known vulnerable pins (OWASP WebGoat, https://github.com/WebGoat/WebGoat) and OSV data.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 4. Cloud cost (FinOps) anomaly investigation and rightsizing
- **Tier:** A | Enterprise: pass
- **Enterprise check:** Buyer: FinOps/platform. Systems: cloud billing (CUR), tagging, monitoring, Terraform, CMDB. Regulation: financial controls, commitment approvals. Human: owner approves deletion or rightsizing.
- **Problem and today's workflow:** Engineers trace spikes to teams and judge whether resources are safe to remove.
- **Evidence:** Flexera State of the Cloud via tech-insider: "Wasted cloud spend rose to 29%, up two points from 27% in 2025" (2026 report). Secondary source; Flexera original not opened. https://tech-insider.org/cloud-waste-29-percent-finops-2026/ [Verified]
- **Agent design:** Join billing, tags, utilisation and IaC; propose Terraform changes; open tickets. Owner approves.
- **Open source today:** hystax/optscale (2,238 stars, Apache-2.0, not archived, last push 2026-10-26; README read: yes; addresses partly: FinOps platform with optimisation recommendations, not an agent); openops-cloud/openops (1,082 stars, NOASSERTION, not archived, last push 2026-11-05; README read: yes; addresses partly: no-code FinOps workflow automation).
- **Demo path:** FOCUS sample data (https://focus.finops.org) and AWS CUR samples.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 5. Language and framework upgrade migration (e.g. Java 8 to 17)
- **Tier:** A | Enterprise: pass
- **Enterprise check:** Buyer: large engineering orgs. Systems: VCS, build tools (Maven/Gradle), CI, dependency registry. Regulation: end-of-support risk for security patches; change records. Human: team reviews and approves each PR.
- **Problem and today's workflow:** Teams upgrade each service by hand: build fixes, API replacements, dependency bumps.
- **Evidence:** AWS blog (Aug 2024): "savings of over 4,500 years of development work for over a thousand developers" (https://aws.amazon.com/blogs/devops/amazon-q-developer-just-reached-a-260-million-dollar-milestone/). The Decoder: Amazon Q "cut the average time to upgrade an app to Java 17 from about 50 developer days to just a few hours"; "79 percent of Amazon Q's auto-generated code reviews" used without changes (https://the-decoder.com/amazons-ai-assistant-saves-4500-years-of-development-time-ceo-andy-jassy-says/). Amazon internal claims, not independent. [Verified]
- **Agent design:** Analyse build, apply deterministic recipes (OpenRewrite) first, use LLM for residual compile failures, run tests, open PR. Owners approve.
- **Open source today:** not checked (GitHub search rate-limited). OpenRewrite (https://github.com/openrewrite/rewrite) is a known rules-based tool, not checked here.
- **Demo path:** Public Java 8 Spring Boot sample projects.
- **Verification:** 2026-11-06, Verified, repos not checked

### 6. Change-request risk review and audit evidence assembly
- **Tier:** B | Enterprise: needs figure
- **Enterprise check:** Buyer: IT change management in regulated firms. Systems: ServiceNow change, CI/CD, VCS, test results, CMDB. Regulation: SOX ITGC, PCI DSS 6.5, DORA change management. Human: CAB approves.
- **Problem and today's workflow:** Change managers manually link tickets to PRs, test evidence and approvals, and judge risk.
- **Evidence:** No reliable figure found. [Unconfirmed]
- **Agent design:** Pull diff, test and deploy data, check segregation of duties, score risk, assemble evidence pack, recommend approve/hold. CAB decides.
- **Open source today:** none found (gh search 'change request risk review' returned no hits).
- **Demo path:** Synthetic change tickets linked to real OSS pull requests.
- **Verification:** 2026-11-06, Unconfirmed, search done yes

### 7. Static-analysis (SAST) finding auto-remediation
- **Tier:** A | Enterprise: pass
- **Enterprise check:** Buyer: AppSec plus engineering. Systems: CodeQL/SonarQube, VCS, CI, ticketing. Regulation: PCI DSS 6.2, secure-SDLC attestations. Human: developer approves fix PR.
- **Problem and today's workflow:** Developers triage scanner alerts and hand-fix common vulnerability classes.
- **Evidence:** GitHub blog: median time to commit a Copilot Autofix for a pull-request alert was 28 minutes "compared to 1.5 hours to resolve the same alerts manually" (public beta May-July 2024). Vendor-reported. https://github.blog/news-insights/product-news/secure-code-more-than-three-times-faster-with-copilot-autofix/ [Verified]
- **Agent design:** Read alert, locate code, patch, rebuild, rerun scanner and tests, open PR. Developer approves.
- **Open source today:** not checked (GitHub search rate-limited).
- **Demo path:** OWASP Juice Shop (https://github.com/juice-shop/juice-shop) with CodeQL.
- **Verification:** 2026-11-06, Verified, repos not checked

### 8. Policy-aware pull-request review at scale
- **Tier:** B | Enterprise: needs figure
- **Enterprise check:** Buyer: engineering governance. Systems: VCS, CI, policy-as-code, ticketing. Regulation: PCI DSS 6.2.3 and SOX four-eyes review. Human: human reviewer remains required approver.
- **Problem and today's workflow:** Reviewers check style, security, licensing and ticket linkage manually; queues delay delivery.
- **Evidence:** No reliable figure found. [Unconfirmed]
- **Agent design:** Review diff against policies, check ticket linkage and licences, comment, route to code owners. Human approves.
- **Open source today:** no confirmed hit. gh search 'pull request review agent' returned coldteadotai/pr-lens (2,356 stars), gmickel/flow-next (716), biheto/DevAgent-Studio (181); descriptions only, README read: no; adjacent only, none shown to be policy-aware review.
- **Demo path:** Closed pull requests from open-source repositories with human review labels.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

## Sources
- https://www.bmc.com/blogs/cobol-trends/
- https://www.datacenterknowledge.com/outages/data-center-outages-decline-for-fourth-straight-year-but-issues-persist
- https://www.sonatype.com/en/press-releases/sonatypes-10th-annual-state-of-the-software-supply-chain-report
- https://testing.googleblog.com/2016/05/
- https://tech-insider.org/cloud-waste-29-percent-finops-2026/
- https://arxiv.org/abs/2402.09171
- https://aws.amazon.com/blogs/devops/amazon-q-developer-just-reached-a-260-million-dollar-milestone/
- https://github.blog/news-insights/product-news/secure-code-more-than-three-times-faster-with-copilot-autofix/
- https://www.swebench.com
- https://www.gharchive.org
- https://deps.dev
- https://osv.dev
- https://github.com/rjust/defects4j
- https://github.com/logpai/loghub
- https://github.com/danluu/post-mortems
- https://github.com/open-telemetry/opentelemetry-demo
- https://github.com/WebGoat/WebGoat
- https://focus.finops.org
- https://github.com/juice-shop/juice-shop
