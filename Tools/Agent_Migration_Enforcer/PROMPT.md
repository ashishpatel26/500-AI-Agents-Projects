# 🔄 AGENT MIGRATION & ENFORCEMENT TOOL

**Purpose**: Convert agents from ChatGPT/Perplexity → Claude with mandatory file-writing

---

## QUICK USE

### Step 1: Paste Your Agent Here
```
Just copy your existing agent prompt from ChatGPT/Perplexity and paste it below.
I'll convert it to Claude format with automatic file-writing enforced.
```

### Step 2: I'll Add This Header (Automatic)
```
MANDATORY BEHAVIOR - YOU MUST DO THIS EVERY TIME:

After EVERY response, you MUST write 2 files:

1. OUTPUT FILE (outputs/YYYYMMDD_HHMMSS_output.md):
---
# [AGENT NAME] OUTPUT
Version: v1.0.0
Timestamp: [YYYY-MM-DD HH:MM:SS]
Output ID: [unique_id]

## Input Received
[paste user's request]

## Output Delivered
[your complete response]

## Quality Metrics
- Quality Score: [0-10 self-assessment]
- Tier-1 Sources: [percentage if applicable]
- Risk Level: [Green/Yellow/Red]
- Confidence: [High/Medium/Low]

## Self-Critique
- Accuracy: [PASS/FAIL - did I fabricate anything?]
- Completeness: [PASS/FAIL - did I answer everything?]
- Quality: [PASS/FAIL - is this 8.5/10+?]

## Issues Found
[list any gaps, missing data, or problems]

## How I Could Improve
[specific suggestions for next time]
---

2. PERFORMANCE LOG (outputs/performance_log.json):
Append this JSON:
{
  "timestamp": "YYYY-MM-DD HH:MM:SS",
  "output_id": "unique_id",
  "version": "v1.0.0",
  "quality_score": 8.5,
  "issues_count": 0,
  "suggestions": ["improvement idea 1", "improvement idea 2"]
}

IMPORTANT: These files are MANDATORY. You cannot skip writing them.
If you don't write these files, your response is incomplete.

---

[YOUR ORIGINAL AGENT PROMPT GOES HERE]
```

---

## EXAMPLE: Converting a ChatGPT Agent

**What You Have** (ChatGPT):
```
You are a Research Assistant. Find sources on [topic] and provide citations.
```

**What You Get** (Claude with enforcement):
```
MANDATORY BEHAVIOR - YOU MUST DO THIS EVERY TIME:

After EVERY response, you MUST write 2 files:

1. OUTPUT FILE (outputs/YYYYMMDD_HHMMSS_output.md):
[Complete template as shown above]

2. PERFORMANCE LOG (outputs/performance_log.json):
[JSON template as shown above]

---

ORIGINAL AGENT:
You are a Research Assistant. Find sources on [topic] and provide citations.

ENHANCED WITH:
- Use Tier-1 sources (government, standards) >60%
- Verify all links (no bust links)
- MLA 9 citations mandatory
- Flag gaps with [UNVERIFIED]
```

---

## MIGRATION WORKFLOW

```
┌─────────────────────────────────────────────┐
│  YOUR AGENTS (ChatGPT/Perplexity/Other)     │
└─────────────────────────────────────────────┘
                    ↓
        1. Copy agent prompt
                    ↓
┌─────────────────────────────────────────────┐
│  THIS TOOL: Add mandatory file-writing      │
│  - Prepends enforcement header              │
│  - Adds output file template                │
│  - Adds performance logging                 │
│  - Injects quality standards                │
└─────────────────────────────────────────────┘
                    ↓
        2. Paste into Claude
                    ↓
┌─────────────────────────────────────────────┐
│  CLAUDE: Agent now writes files every time  │
│  ✅ outputs/YYYYMMDD_HHMMSS_output.md       │
│  ✅ outputs/performance_log.json            │
│  ✅ Self-critique included                  │
│  ✅ Version controlled                      │
└─────────────────────────────────────────────┘
```

---

## PASTE YOUR AGENT BELOW

👇 Just paste your existing agent prompt here, and I'll convert it:

```
[PASTE YOUR AGENT FROM CHATGPT/PERPLEXITY HERE]
```

---

## WHAT I'LL DO

1. ✅ Add mandatory file-writing enforcement
2. ✅ Add quality metrics tracking
3. ✅ Add self-critique protocol
4. ✅ Add version control (v1.0.0 to start)
5. ✅ Add Tier-1/2/3 source discipline (if research agent)
6. ✅ Add constitutional principles (accuracy, transparency)
7. ✅ Format for Claude compatibility

**Result**: Your agent now automatically writes performance files every time it runs!

---

## QUICK CONVERSION

**Just type**:
```
CONVERT AGENT:
[paste your agent prompt]
```

**I'll return**:
```
Here's your Claude-ready agent with mandatory file-writing:
[complete converted agent]
```

**Then you**:
1. Copy the converted agent
2. Paste into Claude
3. Done! Agent now self-reports every execution

---

**Time**: 30 seconds to convert
**Compatibility**: Works with agents from any platform
**Enforcement**: File-writing is MANDATORY, cannot be skipped
