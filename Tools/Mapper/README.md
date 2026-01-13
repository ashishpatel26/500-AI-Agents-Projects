# 🗺️ Citation Mapper Tools
**MLA 9 Citation Formatting & Reference Management**

---

## 🎯 PURPOSE

This folder contains tools for formatting citations to MLA 9 standards and managing references with the Authority Tier System.

---

## 📁 TOOLS IN THIS DIRECTORY

### 1. Citation Mapper (To Be Migrated)

**Current Location**: `C:\Users\aztec\OneDrive\AI Finder_Veteran Fleet Technologies\NACFE Tools\3.0 Tools\GPT Citation Mapper\citation_mapper_main.md`

**Purpose**: MLA citation formatting and reference management

**Key Features**:
- Authority Tier System (Tier-1/2/3 classification)
- Citation Format Standards (MLA 9)
- QA Benchmarks
- Automatic reference formatting
- Source quality validation

**Migration Status**: ⏳ Pending
**Priority**: High (essential for FSM compliance)

---

## 📋 MIGRATION INSTRUCTIONS

### Step 1: Copy Files from OneDrive

```bash
# From your local Windows machine:
# Copy citation_mapper_main.md to this folder

Source: C:\Users\aztec\OneDrive\AI Finder_Veteran Fleet Technologies\NACFE Tools\3.0 Tools\GPT Citation Mapper\citation_mapper_main.md
Destination: Tools/Mapper/
```

### Step 2: Convert to Modular Format

Once copied, create:
- `PROMPT.md` - Quick citation commands (3-5KB)
- `Citation_Mapper_Full.md` - Complete system (15-25KB)

### Step 3: Enhance with Tier System

Ensure integration with:
- ✅ Tier-1 (Government, Standards, Regulatory)
- ✅ Tier-2 (OEM, Peer-reviewed, Trade associations)
- ✅ Tier-3 rejection (Forums, blogs, social media)

### Step 4: Test & Deploy

1. Test with sample source list
2. Verify MLA 9 formatting
3. Check tier classification accuracy
4. Update CLAUDE.MD catalog

---

## 🔄 WORKFLOW INTEGRATION

```
Research Phase (Perplexity)
    ↓
Drafting Phase (GPT Writer V3)
    ↓
Validation Phase (Claude Validator)
    ↓
Citation Phase (Citation Mapper) ← You are here
    ↓
Final Integration (GPT Writer V3)
```

---

## 📊 AUTHORITY TIER SYSTEM

### Tier-1 (>60% target)
**Government & Regulatory**:
- DOE (energy.gov)
- NREL (nrel.gov)
- EPA (epa.gov)
- DOT (transportation.gov)
- CFR (Code of Federal Regulations)

**Standards Organizations**:
- SAE International (sae.org)
- ISO (iso.org)
- ASTM (astm.org)

### Tier-2 (<40% target)
**OEM & Technical**:
- OEM service manuals (PDF downloads)
- Technical bulletins (direct from manufacturer)

**Academic & Industry**:
- Peer-reviewed journals
- SAE Technical Papers
- IEEE publications
- NACFE reports (nacfe.org)
- TMC (tmc.trucking.org)

### Tier-3 (PROHIBITED)
- Forums (Reddit, Stack Exchange)
- Blogs and personal websites
- Social media posts
- Wikipedia
- Marketing materials
- Unverified sources

---

## 📝 MLA 9 CITATION FORMAT

### Government Document
```
U.S. Department of Energy. "Electric Vehicle Benefits and Considerations."
    Office of Energy Efficiency & Renewable Energy, 2024,
    www.energy.gov/eere/electricvehicles/electric-vehicle-benefits.
    Accessed 7 Dec. 2025.
```

### SAE Standard
```
SAE International. "J1772: SAE Electric Vehicle and Plug in Hybrid Electric
    Vehicle Conductive Charge Coupler." SAE Standards, 2017.
```

### OEM Manual
```
Tesla, Inc. "Model 3 Service Manual." Tesla Motors, 2024.
```

### Peer-Reviewed Journal
```
Smith, John, and Jane Doe. "Battery Thermal Management in Electric Vehicles."
    Journal of Power Sources, vol. 450, 2024, pp. 227-245.
```

---

## 🚀 QUICK START (After Migration)

```bash
# 1. Load quick prompt
Use: Tools/Mapper/PROMPT.md

# 2. Format citations
INPUT: [List of sources from Perplexity Researcher]
COMMAND: FORMAT CITATIONS

# 3. Receive formatted output
Output: MLA 9 formatted references with tier classification

# 4. Integrate into FSM
Copy formatted citations to GPT Writer V3
```

---

## ✅ QUALITY CHECKLIST

Before delivery, Citation Mapper verifies:
- [ ] MLA 9 format compliance
- [ ] Author/organization attribution
- [ ] Publication date included
- [ ] URL accessibility (for online sources)
- [ ] Tier classification accurate
- [ ] Access date included (web sources)
- [ ] Proper alphabetization

---

## 📞 SUPPORT

**Documentation**: See CLAUDE.MD for complete workflow
**External Location**: OneDrive backup maintained
**MLA 9 Reference**: Purdue OWL MLA Guide

---

*Status: Awaiting migration from OneDrive*
*Last Updated: December 7, 2025*
