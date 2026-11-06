# Media, Entertainment & Gaming

## Overview
Studios, labels, platforms, broadcasters and game publishers spend effort on rights and royalty accounting, content-policy enforcement, localization and compliance. Manual work concentrates in matching usage to rights holders across fragmented databases, per-decision reasoning for moderation and takedowns, and reconciling money flows between partners.

## Systems of record, regulations, public datasets
- **Systems:** Rights/royalty systems (publishing admin, label accounting), music databases (MLC, ISWC/ISRC), production accounting (Movie Magic, Entertainment Partners), media asset management, ad servers/DSPs, trust-and-safety case tools, moderation queues, DSA Transparency Database, casino platform and KYC/AML tools.
- **Regulation/standards:** EU Digital Services Act (2022); UK Online Safety Act 2023; DMCA 512; EU AI Act transparency; US MMA/MLC; SAG-AFTRA/WGA/DGA agreements; UK Gambling Act and LCCP; EU Accessibility Act (Directive 2019/882, applies 28 June 2025); COPPA.
- **Public datasets:** DSA Transparency Database https://transparency.dsa.ec.europa.eu/ ; MusicBrainz https://musicbrainz.org/doc/MusicBrainz_Database ; MLC public search https://www.themlc.com/ ; Jigsaw Civil Comments / Toxic Comment data https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge ; UKGC enforcement register https://www.gamblingcommission.gov.uk/ ; OpenSubtitles https://www.opensubtitles.org/

## Use cases

### 1. Music sync rights clearance
- **Tier:** A Enterprise: needs figure
- **Enterprise check:** Buyer: studio/streamer clearance dept. Systems: cue sheets, publisher/society databases, contract repository. Regulation: copyright, contractual confidentiality. Human gate: music supervisor and legal approve quotes and licences.
- **Problem and today's workflow:** Coordinators identify each composition and master, trace splits, request quotes and track status.
- **Evidence:** The Billboard URL redirected (307) and then returned 402, so the $424.4M unmatched-royalties transfer is unconfirmed and removed; the NYFA "$25,000 each" rule of thumb was not checked. Reference, not confirmed: https://www.billboard.com/?p=9526741 . [Unconfirmed]
- **Agent design:** Identify cues, look up ownership, draft quote requests, track replies. Humans negotiate and sign.
- **Open source today:** none found (gh search "music sync licensing", stars>=20, not archived: no relevant hit). (one hit, kauenet/nft-music-license, is an NFT licence template, not relevant).
- **Demo path:** MusicBrainz plus synthetic cue sheets.
- **Verification:** 2026-11-06, Unconfirmed, repos checked yes

### 2. Royalty statement reconciliation and audit
- **Tier:** A Enterprise: pass
- **Enterprise check:** Buyer: publisher/label/rights admin. Systems: DSP statements, royalty system, MLC portal, bank. Regulation: contractual audit rights, MMA. Human gate: royalty accountant approves claims and disputes.
- **Problem and today's workflow:** Accountants match DSP lines to catalog, chase unmatched usage and reconcile payments.
- **Evidence:** MLC newsletter (opened): "for the 12 monthly distributions in 2024, The MLC processed $1.05 billion" (total royalties distributed were $859.7M, so "processed" is the correct word). https://emails.themlc.com/february-2025-member-updates [Verified]
- **Agent design:** Ingest statements, match works, flag discrepancies, draft claims. Accountant approves.
- **Open source today:** none found (gh search "royalty statement reconciliation", stars>=20, not archived: no relevant hit).
- **Demo path:** Synthetic DSP statements over MusicBrainz works.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 3. DSA statements-of-reasons and moderation case handling
- **Tier:** A Enterprise: pass
- **Enterprise check:** Buyer: platform trust and safety. Systems: case tools, account history, DSA database API. Regulation: DSA. Human gate: humans own borderline and severe cases.
- **Problem and today's workflow:** Reviewers decide on flagged content and write a statement of reasons.
- **Evidence:** Kaushal et al. abstract (opened): "we analyze a representative sample of the Transparency Database (131m SoRs) submitted in November 2023". https://arxiv.org/abs/2404.02894 [Verified]
- **Agent design:** Policy lookup, context gathering, draft decision and notice; escalate high severity. Child-safety material never sent to general LLM APIs.
- **Open source today:** dengxianghua888-ops/preference-lab (50 stars, Apache-2.0, not archived, last push 2026-11-05; README read: yes, turns moderation policies into preference-pair training data; adjacent only, not a case-handling agent); kisugez/moderator (28 stars, MIT, not archived, last push 2026-06-12; README read: partly, opening is unreadable ANSI art, description is a BYOK moderation API with a 5-strike pipeline; adjacent only).
- **Demo path:** DSA Transparency Database dump plus Civil Comments.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 4. Online game harassment report triage
- **Tier:** B Enterprise: needs figure (survey percentage, no dollar figure)
- **Enterprise check:** Buyer: game publisher T&S. Systems: report queue, chat/voice logs, sanctions DB. Regulation: COPPA, UK OSA, DSA, recording consent. Human gate: humans review severe cases and appeals.
- **Problem and today's workflow:** Moderators read report context and apply graduated sanctions.
- **Evidence:** ADL (opened): "76 percent of adults experience harassment in games, down from 86 percent in 2022." https://www.adl.org/resources/report/hate-no-game-hate-and-harassment-online-games-2023 [Verified]
- **Agent design:** Gather history, assess context, propose sanction, route appeals.
- **Open source today:** yuanzhe-jia/toxic-language-detection (101 stars, MIT, not archived, last push 2026-09-29; README read: yes, token-tagging classifier for in-game chat toxicity; adjacent only, a classifier not a case agent).
- **Demo path:** Civil Comments plus synthetic report histories.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 5. Live-sports piracy detection and takedown
- **Tier:** A Enterprise: needs figure (usage rate, no dollar figure)
- **Enterprise check:** Buyer: rights holder. Systems: stream monitoring, rights calendar, notice systems. Regulation: DMCA 512(f), DSA notice rules. Human gate: lawyer approves bulk/contentious notices.
- **Problem and today's workflow:** Teams find streams during matches, verify rights and send notices in minutes.
- **Evidence:** The Broadband TV News page returned a 307 and was not opened. Search excerpts of the EUIPO 2023 study report live-sports piracy rising from 0.42 to 0.55 accesses per user per month between 2021 and 2022, about 30%, from MUSO traffic data. https://www.broadbandtvnews.com/2023/10/05/europeans-are-consuming-more-pirated-tv-shows-and-live-sports/ [Search-excerpt] (search excerpt only)
- **Agent design:** Discover, fingerprint match, check rights window, file notices.
- **Open source today:** none found (gh search "sports piracy takedown", stars>=20, not archived: no relevant hit).
- **Demo path:** Synthetic stream listings plus match schedule.
- **Verification:** 2026-11-06, Verified (search excerpt), repos checked yes

### 6. Subtitle and dubbing localization QC
- **Tier:** B Enterprise: needs figure (no dollar figure)
- **Enterprise check:** Buyer: streamer/studio localization. Systems: TMS, subtitle files, style guides. Regulation: performer consent, age-rating claims. Human gate: linguists approve flagged lines.
- **Problem and today's workflow:** Linguists check timing, terminology and style per language.
- **Evidence:** EGA survey coverage (opened): "nearly 65% of viewers in France, Italy, Germany and Spain have stopped watching a movie or TV show" in the past year because of poor localisation quality (15,000+ consumers surveyed). That is a viewer-abandonment figure, not an error-rate figure; no error rate found. https://csimagazine.com/csi/Poor-localisation-is-hurting-streamers-EGA.php [Corrected]
- **Agent design:** Auto-check against style guide, route flagged lines.
- **Open source today:** Huanshere/VideoLingo (19,085 stars, Apache-2.0, not archived, last push 2026-09-30; README read: yes, automated subtitle cutting, translation and dubbing pipeline; adjacent only, production not QC); liuzhao1225/YouDub-webui (5,802 stars, Apache-2.0, not archived, last push 2026-11-03; README read: partly, video localization and dubbing desktop tool; adjacent only).
- **Demo path:** OpenSubtitles parallel files.
- **Verification:** 2026-11-06, Corrected, repos checked yes

### 7. Ad campaign delivery reconciliation and invoice dispute
- **Tier:** A Enterprise: pass
- **Enterprise check:** Buyer: advertiser/agency/publisher. Systems: ad servers, DSP logs, billing. Regulation: contract audit, privacy. Human gate: media finance approves credits.
- **Problem and today's workflow:** Teams compare insertion orders to delivery and invoices.
- **Evidence:** ANA (opened): "Only 36 cents of every dollar that enters a demand-side platform (DSP) effectively reaches the consumer"; the December 2023 study covers log-level data of 21 major advertisers. https://ana.net/programmatic [Verified]
- **Agent design:** Reconcile delivery data, flag discrepancies, draft make-good requests.
- **Open source today:** none found (gh search "ad delivery reconciliation", stars>=20, not archived: no relevant hit).
- **Demo path:** Synthetic IOs and logs.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 8. Guild residuals and production payment compliance
- **Tier:** A Enterprise: needs figure (no residual volume)
- **Enterprise check:** Buyer: studio production accounting. Systems: payroll, distribution revenue, guild reporting. Regulation: SAG-AFTRA/WGA/DGA agreements. Human gate: accountant approves payments.
- **Problem and today's workflow:** Staff compute residuals from contract tiers and exhibition data.
- **Evidence:** The SAG-AFTRA page returned 403. Search excerpts quote the union as saying the gains are "expected to generate over $1 billion in new compensation and funding to the benefit plans", a projection (the exact phrase "just over $1 billion" was not found). Residual volume: no reliable figure found. https://sagaftra.org/sag-aftra-members-approve-2023-tvtheatrical-contracts-tentative-agreement [Corrected] (search excerpt only)
- **Agent design:** Parse contract rules, compute amounts, reconcile. Accountant approves.
- **Open source today:** none found (gh search "residuals guild", stars>=20, not archived: no relevant hit).
- **Demo path:** Synthetic episodes and rate tables.
- **Verification:** 2026-11-06, Corrected (search excerpt), repos checked yes

### 9. Online gambling AML and responsible-gambling interventions
- **Tier:** A Enterprise: pass
- **Enterprise check:** Buyer: licensed operator compliance. Systems: player account, payments, KYC. Regulation: UK Gambling Act, LCCP, MLR 2017. Human gate: MLRO decides SARs.
- **Problem and today's workflow:** Analysts review alerts and affordability.
- **Evidence:** Compliance Week (opened, 29 Mar 2023): the UK Gambling Commission imposed a "record fine of 19.2 million pounds (U.S. $23.7 million)" on William Hill. That page does not mention Gamesys; search excerpts of the Gambling Commission and trade press give Gamesys 6 million pounds on 10 Jan 2024 (6,071,292 pounds including a divestment amount), not opened. https://complianceweek.com/regulatory-enforcement/william-hill-fined-record-237m-for-social-responsibility-aml-failures/32893.article [Search-excerpt] (Gamesys via search excerpt)
- **Agent design:** Assemble case file, draft SAR narrative and customer contact. MLRO decides.
- **Open source today:** IBM/AML-Data (108 stars, Apache-2.0 code with CDLA-Sharing-1.0 data, not archived, last push 2025-09-17; README read: yes, synthetic AML transaction datasets; adjacent only, a dataset not an agent).
- **Demo path:** Synthetic transactions.
- **Verification:** 2026-11-06, Verified, repos checked yes

### 10. Accessibility compliance for video services (EAA)
- **Tier:** B Enterprise: needs figure
- **Enterprise check:** Buyer: streamer/broadcaster. Systems: MAM, caption/AD vendors. Regulation: Directive 2019/882 from 28 June 2025. Human gate: accessibility lead approves.
- **Problem and today's workflow:** Staff audit catalogs for captions and audio description.
- **Evidence:** Taylor Wessing page returned 403. Search excerpts attribute to it that the European Accessibility Act came into effect on 28 June 2025 and takes its audiovisual media service definition from the AVMS Directive; sources disagree on transition periods for older content. No financial figure found. https://www.taylorwessing.com/en/interface/2025/media-hot-topics-2025/access-to-audiovisual-media-services-under-the-european-accessibility-act [Search-excerpt] (search excerpt only)
- **Agent design:** Audit catalog, queue missing assets, check quality.
- **Open source today:** none found (gh search "EAA accessibility captions", stars>=20, not archived: no relevant hit).
- **Demo path:** Open Blender Foundation films.
- **Verification:** 2026-11-06, Verified (search excerpt), repos checked yes

## Sources
- https://www.billboard.com/?p=9526741
- https://emails.themlc.com/february-2025-member-updates
- https://arxiv.org/abs/2404.02894
- https://www.adl.org/resources/report/hate-no-game-hate-and-harassment-online-games-2023
- https://www.broadbandtvnews.com/2023/10/05/europeans-are-consuming-more-pirated-tv-shows-and-live-sports/
- https://csimagazine.com/csi/Poor-localisation-is-hurting-streamers-EGA.php
- https://ana.net/programmatic
- https://sagaftra.org/sag-aftra-members-approve-2023-tvtheatrical-contracts-tentative-agreement
- https://complianceweek.com/regulatory-enforcement/william-hill-fined-record-237m-for-social-responsibility-aml-failures/32893.article
- https://www.taylorwessing.com/en/interface/2025/media-hot-topics-2025/access-to-audiovisual-media-services-under-the-european-accessibility-act
