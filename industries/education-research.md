# Education & Research

## Overview
Education institutions and research enterprises spend effort on compliance-bound administration: aid verification, special-education documentation, accreditation, sponsored-research compliance and review logistics. Manual work concentrates in reading student or research records across systems, matching them to federal rules, and producing documentation that auditors, regulators or courts may later examine. Student-facing tutoring and consumer study apps are out of scope.

## Systems of record, regulations, public datasets
- **Systems:** student information systems (Banner, PeopleSoft Campus, Workday Student), FAFSA/COD/NSLDS, IEP systems (PowerSchool Special Programs, Frontline), research administration (Cayuse, Kuali, Huron), IRB systems (iRIS, Huron IRB), editorial systems (ScholarOne, Editorial Manager), NIH eRA Commons, Grants.gov, accreditation platforms.
- **Regulations/standards:** FERPA (1974); IDEA (2004); Title IV HEA and 34 CFR 668; Clery Act (1990); Uniform Guidance 2 CFR 200 (2024 revision); Common Rule 45 CFR 46 (2018); PRISMA 2020; COPE guidelines; Section 504 / ADA.
- **Public datasets for demos:** IPEDS https://nces.ed.gov/ipeds/use-the-data ; College Scorecard https://collegescorecard.ed.gov/data/ ; Federal Student Aid data center https://studentaid.gov/data-center ; PubMed/OpenAlex https://openalex.org/ ; Retraction Watch database via Crossref https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/ ; NIH RePORTER https://reporter.nih.gov/ ; PROSPERO https://www.crd.york.ac.uk/prospero/ ; NSF award search https://www.nsf.gov/awardsearch/ .

## Use cases

### 1. Systematic-review screening and data extraction
- **Tier:** A Enterprise: needs figure (a duration, no dollar or volume figure)
- **Enterprise check:** Buyer is a university, guideline body or HTA agency; systems are reference managers, PubMed/Embase, Covidence; PRISMA/Cochrane reproducibility; reviewers adjudicate.
- **Problem and today's workflow:** Teams screen thousands of abstracts in duplicate, then extract data and assess bias.
- **Evidence:** Borah et al., BMJ Open 2017: "The mean estimated time to complete the project and publish the review was 67.3 weeks (IQR=42)" across "195 registered and completed reviews". https://pubmed.ncbi.nlm.nih.gov/28242767/ (opened via NCBI E-utilities efetch text, since the PubMed page itself needs cookies). [Verified]
- **Agent design:** Tools: PubMed/OpenAlex search, PDF parser, screening classifier with rationale, extraction forms. Human gate: two reviewers resolve disagreements; recall audited.
- **Open source today:** ChaokunHong/MetaScreener (1339 stars, Apache-2.0, not archived, last push 2026-06-11; README read: yes, multi-LLM ensemble for systematic-review abstract/PDF screening, addresses the use case); htlin222/meta-pipe (151 stars, licence NOASSERTION with README badge academic/non-commercial, not archived, last push 2026-11-04; README read: yes, end-to-end meta-analysis pipeline, adjacent only).
- **Demo path:** Public Cochrane/PROSPERO review with known included-study list.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 2. Research-integrity screening (paper mills, image/data manipulation)
- **Tier:** A Enterprise: needs figure
- **Enterprise check:** Buyer is a publisher or institution research-integrity office; systems are manuscript systems, ORCID, image tools; COPE process, defamation risk; editor decides.
- **Problem and today's workflow:** Integrity staff check submissions for tortured phrases, fabricated authors and reused images.
- **Evidence:** Richardson, Byrne and Amaral, PNAS 2025 studied suspected paper-mill output. The cited Retraction Watch page was opened but does not contain the doubling-time or paper-count figures (it says output was "doubling more than twice as fast as corrective measures" and 28.7 percent retracted). PNAS returned 403, so the numbers are removed. Reference, not confirmed: https://retractionwatch.com/2025/08/04/fighting-coordinated-publication-fraud-is-like-emptying-an-overflowing-bathtub-with-a-spoon-study-coauthor-says/ . [Unconfirmed]
- **Agent design:** Tools: text forensics, image-duplication detectors, author-network lookup. Human gate: editor and integrity panel decide actions.
- **Open source today:** none found (gh search "paper mill detection", stars>=20: no relevant hit).
- **Demo path:** Retraction Watch database plus OpenAlex records.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 3. Special-education IEP drafting and compliance tracking
- **Tier:** B Enterprise: needs figure (hours per IEP only, dated)
- **Enterprise check:** Buyer is a school district; systems are IEP system and SIS; IDEA, FERPA, parental consent; IEP team approves.
- **Problem and today's workflow:** Case managers draft present levels and goals and track service minutes and legal timelines.
- **Evidence:** CRS report RS21226 (older paperwork analysis): "on average, 2 hours are spent on each IEP"; IEP meetings average about 1.5 hours (source text garbled as "1? hours"). https://www.everycrsreport.com/reports/RS21226.html (opened). [Verified]
- **Agent design:** Tools: assessment retrieval, goal-bank search, timeline checker. Human gate: IEP team and parents approve; the agent never finalizes.
- **Open source today:** none found (gh search "special education IEP", stars>=20: no hit).
- **Demo path:** Synthetic student profiles; public state goal banks.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 4. Federal student-aid verification and improper-payment detection
- **Tier:** A Enterprise: needs figure (no dollar volume confirmed)
- **Enterprise check:** Buyer is a college financial-aid office or FSA contractor; systems are COD, NSLDS, SIS, IRS data exchange; Title IV, FERPA, FTI; aid officer decides.
- **Problem and today's workflow:** Staff verify FAFSA data and collect documents for flagged applications.
- **Evidence:** Education OIG's FY2024 payment-integrity compliance audit (ED-OIG/A25DC0225, 27 May 2025) found the Pell and Direct Loan improper-payment estimates unreliable. The OIG page returned 406 and NASFAA 403, so this rests on a search-tool excerpt, not an opened page; no dollar figure confirmed. https://oig.ed.gov/reports/audit/us-department-educations-compliance-payment-integrity-information-reporting-1 [Search-excerpt] (search excerpt only)
- **Agent design:** Tools: ISIR parser, document checklists, conflicting-data detection, student outreach drafts. Human gate: aid officer resolves.
- **Open source today:** none found (gh search "FAFSA verification", stars>=20: no hit).
- **Demo path:** Synthetic ISIR records.
- **Verification:** 2026-11-06, Verified (search excerpt), repos checked yes

### 5. Grant peer-review logistics (reviewer matching, conflicts)
- **Tier:** B Enterprise: needs figure (volumes only, no cost figure for this task)
- **Enterprise check:** Buyer is a funding agency or foundation; systems are eRA/proposal system and publication databases; confidentiality rules; review officer assigns.
- **Problem and today's workflow:** Review officers match applications to reviewers and screen conflicts.
- **Evidence:** NIH CSR Advisory Council minutes, 29 Mar 2021: "In calendar year 2020, NIH received 85,000 applications"; "CSR reviewed ~65,000"; "approximately 250 SROs interacted with 18,000 different reviewers". https://public.csr.nih.gov/sites/default/files/2021-04/Minutes_CSRAC_March_2021_final.pdf (opened PDF). [Verified]
- **Agent design:** Tools: publication embedding search, coauthor/affiliation graph. Human gate: officer finalizes. Must run on-prem since applications are confidential.
- **Open source today:** none found (gh search "reviewer assignment grant", stars>=20: no hit).
- **Demo path:** NIH RePORTER abstracts plus OpenAlex authors.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 6. Transfer-credit evaluation and articulation
- **Tier:** A Enterprise: needs figure (43% is a rate, not dollars)
- **Enterprise check:** Buyer is a registrar or state higher-ed system; systems are SIS, degree-audit (Degree Works), catalogs; accreditation and Title IV satisfactory-progress rules; registrar/faculty approve.
- **Problem and today's workflow:** Evaluators compare outside syllabi and descriptions to local courses and set equivalencies.
- **Evidence:** GAO-17-574: "students who transferred from 2004 to 2009 lost, on average, an estimated 43 percent of their credits". https://www.gao.gov/products/GAO-17-574 (opened). [Verified]
- **Agent design:** Tools: transcript parser, catalog and syllabus retrieval, articulation database, degree-audit simulation. Human gate: registrar/department approves equivalencies.
- **Open source today:** none meaningful found (searched "transfer credit evaluation": only student hobby repos, 0 to 3 stars).
- **Demo path:** Public community-college course catalogs and state articulation tables.
- **Verification:** 2026-11-06, Verified, repos checked no (earlier search only, not re-run)

### 7. Clery Act annual security report compilation
- **Tier:** B Enterprise: needs figure (per-violation fine only)
- **Enterprise check:** Buyer is a campus safety/compliance office; systems are police logs, Title IX case system, campus-security-authority reports; Clery Act, fines per violation; compliance officer certifies.
- **Problem and today's workflow:** Staff collect crime reports from many sources, classify by geography and category and publish by Oct 1.
- **Evidence:** The cited Husch Blackwell page was opened and says "On April 20, 2017, ED issued a final rule that, among other things, raised the amount of Clery fines to $54,789 per violation". The claimed $69,733 (2024) was not found on any page (search showed $62,689 in 2022; the 2024 Federal Register rule 2024-01449 was not opened). The maximum is inflation-adjusted yearly. https://www.huschblackwell.com/newsandinsights/yes-clery-fines-increase-again-clery-blog-series-1 [Corrected] (removed $69,733; current figure not confirmed)
- **Agent design:** Tools: log parsers, geography mapper, classification, de-duplication. Human gate: compliance officer signs statistics.
- **Open source today:** none found (gh search "Clery Act", stars>=20: no hit).
- **Demo path:** Synthetic incident logs; ED Campus Safety and Security data https://ope.ed.gov/campussafety/ .
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 8. IRB protocol pre-review and completeness checks
- **Tier:** A Enterprise: needs figure (turnaround days only, second-hand)
- **Enterprise check:** Buyer is a university or hospital IRB office; systems are IRB system and sponsor protocol; Common Rule, FDA 21 CFR 56; IRB chair decides.
- **Problem and today's workflow:** Analysts check submissions against checklists, flag consent issues and route by review category.
- **Evidence:** SRA International blog (Liberale and Kovach case study): "the median time from submission to an approval/denial decision is 39 days", citing AAHRPP 2015 metrics. The page does not say "full board" (earlier wording removed) and the AAHRPP original was not opened. https://www.srainternational.org/blogs/martha-jack/2017/09/15/reducing-the-time-for-irb-reviews (opened). [Corrected]
- **Agent design:** Tools: protocol parser, consent-element checker, exempt-category logic, correspondence drafts. Human gate: IRB analyst/chair approves.
- **Open source today:** none found (gh search "IRB protocol", stars>=20: only an unrelated proxy repo).
- **Demo path:** ClinicalTrials.gov protocols plus sample consent forms.
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 9. Sponsored-research proposal and post-award compliance checks
- **Tier:** A Enterprise: needs figure
- **Enterprise check:** Buyer is a university research office; systems are proposal systems, ERP/grants accounting, effort reporting; 2 CFR 200, sponsor NOFO rules; sponsored-programs officer submits.
- **Problem and today's workflow:** Staff check proposals against solicitations, review budgets and costs allowability.
- **Evidence:** Faculty lose a large share of federally funded research time to administrative requirements. The claimed 44.3% (2018) figure was not found on any reachable page (a search summary showed the FDP 2012 survey at about 42%, not opened), so the number is removed. Reference, not confirmed: https://www.nationalacademies.org/event/docs/D596C25384270C32501352423259FC1F6E79D87966E6 . [Unconfirmed]
- **Agent design:** Tools: NOFO parser, budget spreadsheet checker, ERP queries. Human gate: officer approves submission.
- **Open source today:** none found (gh search "grant proposal compliance", stars>=20: no relevant hit).
- **Demo path:** NSF/NIH public solicitations and NSF award data.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 10. Accreditation self-study evidence compilation
- **Tier:** B Enterprise: needs figure
- **Enterprise check:** Buyer is a college or program; systems are SIS, LMS, assessment, document repositories; accreditor standards and Dept. of Education recognition; accreditation liaison signs.
- **Problem and today's workflow:** Staff map evidence to standards across departments.
- **Evidence:** The JMU slides URL returned 404 and NASFAA returned 403. A search summary reports the BCG/Vanderbilt 2015 study extrapolated about $27B per year, but sources disagree on the accreditation share ($3B regional vs $6B total accreditation); nothing was opened, so figures are removed. Reference, not confirmed: https://www.jmu.edu/audit/_files/Compliance/compliance-resources/Cost-of-Federal-Regulatory-Compliance-slides.pdf . [Unconfirmed]
- **Agent design:** Tools: standards crosswalk, document retrieval, data pulls from IPEDS. Human gate: liaison and committees approve narratives.
- **Open source today:** none found (gh search "accreditation evidence", stars>=20: only an unrelated domain-registrar repo).
- **Demo path:** Public accreditor standards plus IPEDS/College Scorecard data.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

## Sources
- https://pubmed.ncbi.nlm.nih.gov/28242767/
- https://retractionwatch.com/2025/08/04/fighting-coordinated-publication-fraud-is-like-emptying-an-overflowing-bathtub-with-a-spoon-study-coauthor-says/
- https://www.everycrsreport.com/reports/RS21226.html
- https://oig.ed.gov/reports/audit/us-department-educations-compliance-payment-integrity-information-reporting-1
- https://public.csr.nih.gov/sites/default/files/2021-04/Minutes_CSRAC_March_2021_final.pdf
- https://www.gao.gov/products/GAO-17-574
- https://www.huschblackwell.com/newsandinsights/yes-clery-fines-increase-again-clery-blog-series-1
- https://www.srainternational.org/blogs/martha-jack/2017/09/15/reducing-the-time-for-irb-reviews
- https://www.nationalacademies.org/event/docs/D596C25384270C32501352423259FC1F6E79D87966E6
- https://www.jmu.edu/audit/_files/Compliance/compliance-resources/Cost-of-Federal-Regulatory-Compliance-slides.pdf
- https://nces.ed.gov/ipeds/use-the-data ; https://collegescorecard.ed.gov/data/ ; https://studentaid.gov/data-center ; https://openalex.org/ ; https://reporter.nih.gov/ ; https://www.nsf.gov/awardsearch/ ; https://ope.ed.gov/campussafety/
