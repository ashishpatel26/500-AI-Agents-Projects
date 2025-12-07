# 🛠️ TOOLS DIRECTORY
**Fleet Technology Intelligence System - Agent Tools**

---

## 📁 STRUCTURE

Each tool has its own folder with modular files:

```
Tools/
├── README.md (this file)
│
├── Agent_Creator/
│   ├── PROMPT.md (3KB - quick commands)
│   └── Agent_Creator_Universal.md (18KB - full system)
│
├── Perplexity_Researcher/
│   ├── PROMPT.md (5KB - quick commands)
│   └── Perplexity_Researcher_Agent.md (24KB - full system)
│
├── Mapper/
│   └── [Citation mapping tools - to be organized]
│
├── Research/
│   └── [Additional research utilities - to be organized]
│
└── Writer/
    └── [FSM writing tools - to be organized]
```

---

## 🎯 MODULAR PHILOSOPHY

### Two-File System

**PROMPT.md** (Quick Reference):
- Small file (3-5KB)
- Fast load (15-30 seconds)
- Daily commands and common use cases
- No clutter, just what you need
- **Use this 90% of the time**

**[Tool]_Full.md** (Complete System):
- Large file (15-25KB)
- Detailed protocols and examples
- Edge cases and troubleshooting
- Complete documentation
- **Reference when needed**

---

## 🚀 QUICK START

### For Daily Use

1. Navigate to tool folder: `Tools/[ToolName]/`
2. Open `PROMPT.md`
3. Copy activation prompt
4. Paste into AI (ChatGPT, Claude, Perplexity)
5. Use quick commands

**Time**: 30 seconds to activate

### For Deep Work

1. Navigate to tool folder: `Tools/[ToolName]/`
2. Open `[ToolName]_Full.md`
3. Load complete system into AI
4. Access full protocols and examples

**Time**: 1-2 minutes to activate

---

## 📊 AVAILABLE TOOLS

### ✅ Active Tools

#### 1. Agent Creator
**Folder**: `Agent_Creator/`
**Purpose**: Build new AI agents with constitutional governance
**Quick Command**: `CREATE AGENT: [Name] PURPOSE: [Mission]`
**Load**: `PROMPT.md` for daily use

#### 2. Agent Migration Enforcer
**Folder**: `Agent_Migration_Enforcer/`
**Purpose**: Convert agents from any platform to Claude format
**Quick Command**: `CONVERT AGENT: [paste agent prompt]`
**Load**: `PROMPT.md` for conversions

#### 3. Perplexity Researcher
**Folder**: `Perplexity_Researcher/`
**Purpose**: Find exact sources with verified links (zero time waste)
**Quick Commands**:
- `QUICK MODE: [topic] keywords [terms]`
- `COMPREHENSIVE: [full research topic]`
- `VALIDATION: [verify claim]`
**Load**: `PROMPT.md` for searches

#### 4. Citation Mapper ⭐ NEW
**Folder**: `Mapper/`
**Purpose**: MLA 9 citation formatting with tier verification
**Quick Commands**:
- `MAP: [URL or source]`
- `BATCH MAP: [list of sources]`
- `BUILD WORKS CITED: [all sources]`
**Load**: `PROMPT.md` for daily citation tasks
**Features**: URL verification, duplicate detection, tier classification

#### 5. Advanced Research Agent ⭐ NEW
**Folder**: `Research/`
**Purpose**: Multi-agent RAG-powered comprehensive research
**Quick Commands**:
- `RESEARCH: [topic] MODE: QUICK`
- `RESEARCH: [topic] MODE: COMPREHENSIVE`
- `VALIDATE: [claim]`
- `GAP ANALYSIS: [draft]`
**Load**: `PROMPT.md` for research tasks
**Features**: Web scraper, academic searcher, standards navigator sub-agents

#### 6. FSM Content Writer ⭐ NEW
**Folder**: `Writer/`
**Purpose**: Generate FSM content with 7-element paragraph model
**Quick Commands**:
- `FSM: [topic] SOURCES: [research packet]`
- `VERIFY: [draft content]`
- `REVISE: [feedback]`
- `COLLAB: [task] AGENTS: [agent list]`
**Load**: `PROMPT.md` for writing tasks
**Features**: Self-assessment (≥8.0/10), multi-agent collaboration

---

## 🧩 ADDING NEW TOOLS

### Standard Process

**Step 1: Create Folder**
```bash
mkdir Tools/[ToolName]/
```

**Step 2: Create Quick Prompt**
```
Tools/[ToolName]/PROMPT.md
- Activation prompt
- Quick commands
- Common use cases
- 3-5KB max
```

**Step 3: Create Full System**
```
Tools/[ToolName]/[ToolName]_Full.md
- Complete protocols
- Examples and edge cases
- Troubleshooting
- 15-25KB
```

**Step 4: Update Catalog**
- Add to `CLAUDE.MD` catalog
- Document in this README
- Test both files

---

## 📋 TOOL NAMING CONVENTIONS

### Folders
```
PascalCase with underscores
Examples:
- Agent_Creator
- Perplexity_Researcher
- Chart_Generator
```

### Files
```
PROMPT.md (always this name)
[ToolName]_Full.md (matches folder name)

Examples:
- Agent_Creator/PROMPT.md
- Agent_Creator/Agent_Creator_Universal.md
- Chart_Generator/PROMPT.md
- Chart_Generator/Chart_Generator_Full.md
```

---

## ✅ QUALITY STANDARDS

### Every Tool Must Have

**PROMPT.md Requirements**:
- [ ] Quick activation prompt (copy/paste ready)
- [ ] 3-5 common commands
- [ ] When to use / when not to use
- [ ] Quick start (3 steps max)
- [ ] Reference to full file
- [ ] File size: 3-5KB

**Full.md Requirements**:
- [ ] System identity and mission
- [ ] Workflow integration
- [ ] Constitutional foundation
- [ ] Complete protocols
- [ ] Quality assurance checklist
- [ ] Examples (minimum 2)
- [ ] Activation triggers
- [ ] File size: 15-25KB

---

## 🔄 WORKFLOW INTEGRATION

### How Tools Connect

```
┌─────────────────────────────────────────────────┐
│            FSM TOOL WORKFLOW                     │
└─────────────────────────────────────────────────┘

Research Need
    ↓
Perplexity_Researcher (find sources)
    ↓
Writer (generate FSM content)
    ↓
Mapper (format citations)
    ↓
Validator (check quality)
    ↓
Agent_Creator (build new tools as needed)
```

---

## 📚 DOCUMENTATION

### For Each Tool

**Minimum Documentation**:
1. PROMPT.md (quick reference)
2. [ToolName]_Full.md (complete system)
3. Entry in CLAUDE.MD catalog
4. Entry in this README

**Optional Documentation**:
- Examples/ subfolder (example outputs)
- Modules/ subfolder (sub-modules)
- Tests/ subfolder (validation tests)

---

## 🎓 TRAINING GUIDE

### New Users - Day 1

**Learn the Structure** (15 minutes):
1. Read this README
2. Browse CLAUDE.MD catalog
3. Understand PROMPT.md vs Full.md concept

**Try First Tool** (30 minutes):
1. Open `Perplexity_Researcher/PROMPT.md`
2. Copy activation prompt
3. Paste into Perplexity Pro
4. Run a QUICK MODE search
5. Review output

**Understand Modular Benefits** (15 minutes):
1. Try loading PROMPT.md (fast)
2. Try loading Full.md (detailed)
3. Compare experience
4. Decide which to use when

---

## 🐛 TROUBLESHOOTING

### Common Issues

**Issue**: Tool not working as expected
**Solution**: Check if you loaded PROMPT.md or Full.md - some tasks need full system

**Issue**: Can't find a command
**Solution**: Check PROMPT.md for common commands, Full.md for advanced

**Issue**: Tool folder messy
**Solution**: Follow naming conventions, keep only PROMPT.md + Full.md in root

**Issue**: Adding new tool breaks workflow
**Solution**: Use Agent_Creator to build with constitutional compliance

---

## 📞 SUPPORT

### Internal Resources
- Main Catalog: `../CLAUDE.MD`
- Constitutional Principles: `../Base/framework/`
- Examples: `../Base/Examples/`

### External Resources
- OneDrive: `C:\Users\aztec\OneDrive\AI Finder_Veteran Fleet Technologies\NACFE Tools\`

---

## 🔮 ROADMAP

### Planned Tools

1. **Transcript_Analyzer** (Planned)
   - Process interview recordings
   - Extract technical claims
   - MLA citation formatting

2. **Chart_Generator** (Planned)
   - Visualize research data
   - Publication-ready charts
   - Integration with Perplexity output

3. **Standards_Navigator** (Planned)
   - SAE/ISO specification lookup
   - Regulatory compliance tracking
   - OEM manual parsing

### Organize Existing

1. **Mapper/** - Create modular structure
2. **Research/** - Audit and organize
3. **Writer/** - Create PROMPT.md

---

## 📝 CHANGELOG

### December 5, 2025
- ✅ Created modular structure (PROMPT.md + Full.md)
- ✅ Organized Agent_Creator tool
- ✅ Organized Perplexity_Researcher tool
- ✅ Created Tools README
- ✅ Updated CLAUDE.MD catalog

### December 7, 2025
- ✅ Organized Mapper/ tool (Citation Mapper with MLA 9 formatting)
- ✅ Organized Research/ tool (Advanced Research Agent with RAG)
- ✅ Organized Writer/ tool (FSM Content Writer with 7-element model)
- ✅ Updated CLAUDE.MD catalog with new tools
- ✅ Enhanced workflow V3.0 (Research → Mapper → Writer)

---

## 🎯 QUICK REFERENCE

```
┌───────────────────────────────────────────────────────────────────┐
│              TOOLS QUICK REFERENCE V3.0                            │
├───────────────────────────────────────────────────────────────────┤
│ NEED                  │ TOOL                  │ FILE              │
├───────────────────────┼───────────────────────┼──────────────────┤
│ Build new agent       │ Agent_Creator         │ PROMPT.md        │
│ Convert agents        │ Agent_Migration       │ PROMPT.md        │
│ Quick source finding  │ Perplexity_Researcher │ PROMPT.md        │
│ Deep research + RAG   │ Advanced_Research ⭐  │ PROMPT.md        │
│ Format citations      │ Citation_Mapper ⭐    │ PROMPT.md        │
│ Write FSM content     │ FSM_Content_Writer ⭐ │ PROMPT.md        │
├───────────────────────────────────────────────────────────────────┤
│ Daily use:            │ Load PROMPT.md        │ ~15-30 seconds   │
│ Deep work:            │ Load Full.md          │ ~1-2 minutes     │
│                                                                    │
│ ENHANCED WORKFLOW: Research → Mapper → Writer (45-60 min)        │
└───────────────────────────────────────────────────────────────────┘
```

---

**Remember**:
- PROMPT.md for speed (90% of tasks)
- Full.md for depth (complex work)
- Keep folders organized
- Update catalog when adding tools

---

*For complete system documentation, see CLAUDE.MD in parent directory*
