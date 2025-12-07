# 🔄 MIGRATION GUIDE
**Integrating External Tools from OneDrive to Repository**

**Last Updated**: December 7, 2025
**Status**: Ready for Migration

---

## 🎯 OVERVIEW

This guide helps you migrate your existing NACFE tools from OneDrive to this organized repository structure.

**OneDrive Location**: `C:\Users\aztec\OneDrive\AI Finder_Veteran Fleet Technologies\NACFE Tools\`

**Repository Location**: `500-AI-Agents-Projects/Tools/`

---

## 📋 TOOLS TO MIGRATE

### ✅ Already Migrated (Complete)

1. **Agent Creator Enterprise V2.0**
   - Location: `Tools/Agent_Creator/`
   - Status: ✅ Complete with modular structure

2. **Agent Migration Enforcer**
   - Location: `Tools/Agent_Migration_Enforcer/`
   - Status: ✅ Complete with modular structure

3. **Perplexity Researcher (Enhanced)**
   - Location: `Tools/Perplexity_Researcher/`
   - Status: ✅ Complete with modular structure

---

### ⏳ Pending Migration (High Priority)

#### 1. GPT Writer V3

**Source**: `C:\Users\aztec\OneDrive\AI Finder_Veteran Fleet Technologies\NACFE Tools\Latest Test\GPT Writer Prompt V3.txt`

**Destination**: `Tools/Writer/`

**Priority**: 🔴 High (core FSM generation tool)

**Migration Steps**:
1. Copy `GPT Writer Prompt V3.txt` to `Tools/Writer/`
2. Create `PROMPT.md` (extract quick commands)
3. Create `GPT_Writer_V3_Full.md` (complete system)
4. Test FSM generation workflow
5. Update `CLAUDE.MD` catalog

**Time Estimate**: 30-45 minutes

---

#### 2. Claude Validator

**Source**: `C:\Users\aztec\OneDrive\AI Finder_Veteran Fleet Technologies\NACFE Tools\3.0 Tools\Claude\Validator\Claude NACFE Validator & Gap Analyst.txt`

**Destination**: `Tools/Research/`

**Priority**: 🔴 High (critical validation tool)

**Migration Steps**:
1. Copy `Claude NACFE Validator & Gap Analyst.txt` to `Tools/Research/`
2. Create `PROMPT.md` (L1-L4 quick reference)
3. Create `Claude_Validator_Full.md` (complete framework)
4. Test gap analysis workflow
5. Update `CLAUDE.MD` catalog

**Time Estimate**: 30-45 minutes

---

#### 3. Citation Mapper

**Source**: `C:\Users\aztec\OneDrive\AI Finder_Veteran Fleet Technologies\NACFE Tools\3.0 Tools\GPT Citation Mapper\citation_mapper_main.md`

**Destination**: `Tools/Mapper/`

**Priority**: 🔴 High (MLA 9 formatting essential)

**Migration Steps**:
1. Copy `citation_mapper_main.md` to `Tools/Mapper/`
2. Create `PROMPT.md` (quick citation commands)
3. Create `Citation_Mapper_Full.md` (complete system)
4. Test MLA 9 formatting
5. Update `CLAUDE.MD` catalog

**Time Estimate**: 30-45 minutes

---

### 📝 Optional Migration (Low Priority)

#### 4. Perplexity Research (Original)

**Source**: `C:\Users\aztec\OneDrive\AI Finder_Veteran Fleet Technologies\NACFE Tools\3.0 Tools\Perplexity Research\New folder\perplexity_research_main.md`

**Destination**: `Tools/Research/Archive/` (for reference only)

**Priority**: 🟡 Low (enhanced version already active)

**Reason**: Enhanced version at `Tools/Perplexity_Researcher/` is superior

**Action**: Archive original for comparison/reference

---

## 🚀 QUICK MIGRATION WORKFLOW

### Step 1: Batch Copy Files (Windows)

```powershell
# From Windows PowerShell in your repository directory:

# Copy GPT Writer V3
Copy-Item "C:\Users\aztec\OneDrive\AI Finder_Veteran Fleet Technologies\NACFE Tools\Latest Test\GPT Writer Prompt V3.txt" -Destination "Tools\Writer\"

# Copy Claude Validator
Copy-Item "C:\Users\aztec\OneDrive\AI Finder_Veteran Fleet Technologies\NACFE Tools\3.0 Tools\Claude\Validator\Claude NACFE Validator & Gap Analyst.txt" -Destination "Tools\Research\"

# Copy Citation Mapper
Copy-Item "C:\Users\aztec\OneDrive\AI Finder_Veteran Fleet Technologies\NACFE Tools\3.0 Tools\GPT Citation Mapper\citation_mapper_main.md" -Destination "Tools\Mapper\"
```

---

### Step 2: Convert to Modular Format

For **each** tool copied:

1. **Read the full file** to understand structure
2. **Extract quick commands** → Create `PROMPT.md` (3-5KB)
3. **Preserve complete system** → Rename/create `[Tool]_Full.md` (15-25KB)
4. **Add constitutional headers** (if missing):
   - Universal directives
   - Tier system enforcement
   - Self-critique protocol
   - MLA 9 standards

---

### Step 3: Test Each Tool

```bash
# For each migrated tool:

1. Load PROMPT.md into appropriate AI (ChatGPT/Claude)
2. Run sample command
3. Verify output quality
4. Check constitutional compliance
5. Document any issues
```

---

### Step 4: Update Catalog

Add entries to `CLAUDE.MD` under **Active Agents** section:

```markdown
### [Tool Name]
**Location**: `Tools/[Folder]/`
**Status**: ✅ Active
**Created**: [Date]

**Files**:
- `PROMPT.md` - Quick commands ([size]KB)
- `[Tool]_Full.md` - Complete system ([size]KB)

**Purpose**: [Description]

**Key Features**:
- [Feature 1]
- [Feature 2]
- [Feature 3]

**Quick Start**:
```
[Quick commands here]
```
```

---

### Step 5: Commit to Repository

```bash
# From Git Bash or terminal:

git add Tools/Writer/ Tools/Mapper/ Tools/Research/
git commit -m "Migrate GPT Writer V3, Claude Validator, and Citation Mapper from OneDrive"
git push -u origin claude/review-ai-tools-01UUG2cfVXh5Vi4khxQwu1wA
```

---

## 📊 MIGRATION CHECKLIST

### Pre-Migration

- [ ] Backup OneDrive folder (just in case)
- [ ] Verify repository structure exists (`Tools/Writer/`, `Tools/Mapper/`, `Tools/Research/`)
- [ ] Read this migration guide completely

### During Migration

#### GPT Writer V3
- [ ] Copy file from OneDrive
- [ ] Create PROMPT.md
- [ ] Create GPT_Writer_V3_Full.md
- [ ] Test FSM generation
- [ ] Verify 7-element paragraph output
- [ ] Check quality score ≥8.0/10

#### Claude Validator
- [ ] Copy file from OneDrive
- [ ] Create PROMPT.md
- [ ] Create Claude_Validator_Full.md
- [ ] Test L1-L4 gap analysis
- [ ] Verify classification accuracy
- [ ] Check validation protocols

#### Citation Mapper
- [ ] Copy file from OneDrive
- [ ] Create PROMPT.md
- [ ] Create Citation_Mapper_Full.md
- [ ] Test MLA 9 formatting
- [ ] Verify tier classification
- [ ] Check citation accuracy

### Post-Migration

- [ ] Update CLAUDE.MD catalog
- [ ] Update Tools/README.md
- [ ] Test complete FSM workflow (end-to-end)
- [ ] Commit changes to repository
- [ ] Push to remote (GitHub)
- [ ] Verify OneDrive backup still intact
- [ ] Document any issues encountered

---

## 🔧 TROUBLESHOOTING

### Issue: File Not Found

**Problem**: Can't find tool in OneDrive location

**Solution**:
1. Search OneDrive for file name
2. Check `AI Slop\` folder for older versions
3. Check `Latest Test\` folder
4. Review CLAUDE.MD for correct path

---

### Issue: Tool Too Large

**Problem**: Full tool file is >50KB

**Solution**:
1. Split into logical modules
2. Create `PROMPT.md` with only essential commands
3. Create `[Tool]_Core.md` with main protocols
4. Create `[Tool]_Examples.md` with examples
5. Create `[Tool]_Advanced.md` with edge cases

---

### Issue: Missing Constitutional Headers

**Problem**: Old tool doesn't have constitutional compliance

**Solution**:
1. Use **Agent Migration Enforcer** (`Tools/Agent_Migration_Enforcer/PROMPT.md`)
2. Paste old tool prompt
3. Receive updated version with constitutional headers
4. Save as new file

---

### Issue: Workflow Integration Breaks

**Problem**: New tool doesn't connect with existing pipeline

**Solution**:
1. Review input/output formats
2. Check if tool expects specific format
3. Update workflow diagram in CLAUDE.MD
4. Create adapter/bridge if needed
5. Test end-to-end workflow

---

## 📞 SUPPORT

### Before Migration
- Review `Tools/README.md`
- Review `CLAUDE.MD` catalog
- Check constitutional principles in `Base/framework/`

### During Migration
- Use **Agent Migration Enforcer** for automatic conversion
- Reference existing tools (`Agent_Creator`, `Perplexity_Researcher`) as templates
- Test incrementally (one tool at a time)

### After Migration
- Update all documentation
- Test complete FSM workflow
- Verify OneDrive backup unchanged
- Archive old versions if needed

---

## ✅ SUCCESS CRITERIA

Migration is complete when:

1. ✅ All high-priority tools copied to repository
2. ✅ Each tool has PROMPT.md + Full.md structure
3. ✅ Constitutional compliance verified (100%)
4. ✅ All tools tested and working
5. ✅ CLAUDE.MD catalog updated
6. ✅ Changes committed to repository
7. ✅ End-to-end FSM workflow tested
8. ✅ OneDrive backup intact

---

## 🎯 ESTIMATED TIME

| Task | Time Required |
|------|---------------|
| **Pre-Migration Prep** | 15 minutes |
| **Copy Files** | 5 minutes |
| **GPT Writer V3 Conversion** | 30-45 minutes |
| **Claude Validator Conversion** | 30-45 minutes |
| **Citation Mapper Conversion** | 30-45 minutes |
| **Testing & QA** | 30-45 minutes |
| **Documentation Updates** | 15-30 minutes |
| **Git Commit & Push** | 5 minutes |
| **TOTAL** | **2.5 - 3.5 hours** |

**Recommendation**: Block 4 hours, complete in one session

---

## 🔮 NEXT STEPS AFTER MIGRATION

1. **Week 1**: Use migrated tools in daily workflow
2. **Week 2**: Collect performance data
3. **Week 3**: Optimize based on usage patterns
4. **Month 1**: Integrate advanced use cases from `500-AI-Agents-Projects`
5. **Ongoing**: Maintain constitutional standards, version control

---

## 📝 NOTES

- **OneDrive remains backup**: Don't delete original files
- **Git provides version history**: Can always revert if needed
- **Modular structure optional**: Can keep original file if preferred
- **Constitutional compliance mandatory**: All tools must follow principles

---

*Ready to migrate? Start with Step 1 above!*

---

**Questions?** Review CLAUDE.MD or Tools/README.md
**Issues?** Check Troubleshooting section
**Support**: Constitutional principles in Base/framework/

---

*Last Updated: December 7, 2025*
*Status: Ready for immediate migration*
