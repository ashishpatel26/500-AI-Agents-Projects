# MOSIP Multi-Agent Digital Identity Verification System (`mosip-id-verification-agent`)

A parallel multi-agent system designed for automated identity claim verification and compliance auditing against **MOSIP (Modular Open Source Identity Platform)** standards using **LangGraph**.

---

## 📌 Overview

MOSIP (Modular Open Source Identity Platform) is a foundational digital identity framework used internationally for national ID systems. Third-party relying systems (e.g., banks, telecom operators, public services) need to verify user-submitted identity claims against official MOSIP identity records.

This agent implements a multi-agent orchestration architecture that:
1. Validates input claims against official MOSIP UIN/VID structural format specifications.
2. Runs **3 specialized parallel worker agents**:
   - **Demographic Worker**: Analyzes name transliterations, middle-name omissions, DOB, and gender matches.
   - **Address & Spatial Worker**: Analyzes address structure, street abbreviations, and postal code alignment.
   - **Security & Compliance Worker**: Audits UIN checksum validity, active status, and credential integrity.
3. Synthesizes all worker evaluations into a weighted confidence score and routes the decision (`APPROVED`, `FLAGGED_FOR_MANUAL_REVIEW`, or `REJECTED`).

---

## 🏗️ Multi-Agent Architecture

```text
                               ┌────────────────────────────────┐
                               │     Master Orchestrator        │
                               └───────────────┬────────────────┘
                                               │ (Parallel Fan-Out)
                   ┌───────────────────────────┼───────────────────────────┐
                   ▼                           ▼                           ▼
       ┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────────┐
       │  Demographic Worker  │    │  Address/Spatial     │    │  Security/Compliance │
       │  (Name, DOB, Gender) │    │  Worker (Postal/St)  │    │  Worker (UIN Check)  │
       └───────────┬──────────┘    └───────────┬──────────┘    └───────────┬──────────┘
                   │                           │                           │
                   └───────────────────────────┼───────────────────────────┘
                                               │ (Fan-In Aggregation)
                                               ▼
                               ┌────────────────────────────────┐
                               │     Synthesis Aggregator       │
                               └────────────────────────────────┘
```

---

## ⚡ Quick Start

### 1. Installation
Clone the repository and install the dependencies:
```bash
pip install -r requirements.txt
```

### 2. Environment Setup (Optional)
Copy the example environment file:
```bash
cp .env.example .env
```
Add your OpenAI API Key to `.env` for LLM-powered fuzzy evaluation. If no key is provided, the agent automatically runs in deterministic fallback mode.

### 3. Run the Agent
```bash
python agent.py
```

**Rough Runtime**: ~5 to 10 seconds.

---

## 💻 Real Sample Output

```text
================================================================================
MOSIP MULTI-AGENT DIGITAL IDENTITY VERIFICATION SYSTEM
Framework: LangGraph (Enabled)
Architecture: Parallel Multi-Worker Orchestration Layer
================================================================================

▶ RUNNING TEST: CLM-101 (Valid claim with minor name spelling variation & address format difference)

--- Execution Logs ---
  [Orchestrator] Received verification claim ID: CLM-101
  [Orchestrator] Found active MOSIP record for UIN: UIN-9876543210
  [Address Worker] Analyzing address & location structural match...
  [Demographic Worker] Analyzing demographic match...
  [Security Worker] Auditing MOSIP UIN format and security risk...
  [Aggregator] Synthesizing multi-agent outputs into final MOSIP decision...

--- Verification Summary ---
  Overall Score : 74.5%
  Final Decision: FLAGGED_FOR_MANUAL_REVIEW
  Recommendation: Moderate identity match. Human operator review required for address/name variations.
  Score Breakdown: Demographic (52%), Address (82%), Security (100%)
--------------------------------------------------------------------------------

▶ RUNNING TEST: CLM-102 (Invalid UIN format (Security Failure Test))

--- Execution Logs ---
  [Orchestrator] Received verification claim ID: CLM-102
  [Orchestrator] WARNING: No reference record found for UIN: UIN-INVALID-99
  [Address Worker] Analyzing address & location structural match...
  [Demographic Worker] Analyzing demographic match...
  [Security Worker] Auditing MOSIP UIN format and security risk...
  [Aggregator] Synthesizing multi-agent outputs into final MOSIP decision...

--- Verification Summary ---
  Overall Score : 0.0%
  Final Decision: REJECTED
  Recommendation: Security check failed. Invalid UIN format or inactive record.
  Score Breakdown: Demographic (0%), Address (0%), Security (0%)
--------------------------------------------------------------------------------

▶ RUNNING TEST: CLM-103 (Mismatching Demographic Data Claim)

--- Execution Logs ---
  [Orchestrator] Received verification claim ID: CLM-103
  [Orchestrator] Found active MOSIP record for UIN: UIN-1122334455
  [Address Worker] Analyzing address & location structural match...
  [Demographic Worker] Analyzing demographic match...
  [Security Worker] Auditing MOSIP UIN format and security risk...
  [Aggregator] Synthesizing multi-agent outputs into final MOSIP decision...

--- Verification Summary ---
  Overall Score : 31.9%
  Final Decision: REJECTED
  Recommendation: Low identity match score across demographic and spatial fields.
  Score Breakdown: Demographic (12%), Address (6%), Security (100%)
--------------------------------------------------------------------------------
```

---

## 🔒 Safety, Ethics & Privacy Notes

1. **Synthetic & Mock Data Only**: This demo uses mock synthetic data. Never use real PII (Personally Identifiable Information) or production government identity databases in test environments.
2. **Human-in-the-Loop Default**: Verification claims falling between 65% and 84% confidence are automatically routed to `FLAGGED_FOR_MANUAL_REVIEW` to ensure human oversight for borderline identity cases.
3. **Data Protection**: In production deployments, identity claims must be transmitted over encrypted channels (TLS 1.3) and comply with local data protection regulations (e.g., GDPR, India DPDP Act).
