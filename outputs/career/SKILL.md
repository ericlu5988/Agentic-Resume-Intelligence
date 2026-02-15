---
name: career
description: Career analysis - job application assessment with GO/NO-GO scoring, company research, interview prep, and production-ready deliverables. Resume ethics mandatory - never fabricate.
agent: advisor
version: 2.1
classification: public
last_updated: 2026-02-08
effort_default: STANDARD
mode: multi-agent
agents: [advisor, researcher, writer]
---

> **⛔ MULTI-AGENT ROUTING - READ THIS FIRST**
>
> **STOP.** This skill uses multiple agents across its pipeline:
>
> | Phase | Agent | Work Type |
> |-------|-------|-----------|
> | 1 - Assess | `advisor` | GO/NO-GO scoring, career strategy |
> | 2 - Research | `researcher` | Company intelligence gathering |
> | 3 - Prepare | `advisor` | Interview prep synthesis |
> | 4 - Generate | `writer` | Resume + cover letter creation |
> | 5 - Deliver | `advisor` | Submission strategy |
>
> **STOP.** This skill requires the `advisor` agent as primary orchestrator.
>
> **Identity check:** If you are NOT the advisor agent AND your request is complex
> (opportunity evaluation, GO/NO-GO analysis, application strategy) → DELEGATE NOW.
>
> **DO NOT** proceed without the correct agent for the current phase → DELEGATE:
>
> ```typescript
> Task(subagent_type="[correct-agent]", prompt="Execute career Phase [N]. Context: {phase_context}")
> ```
>
> **Path 1 - Simple (Tier 1/Haiku):** General career information
> - "What's important in evaluating a job offer?"
> - Routes directly, no delegation needed
>
> **Path 2 - Complex (Multi-Agent):** Opportunity evaluation
> - "Should I apply for this role?"
> - Requires full pipeline with agent routing per phase

---

# Career Skill

**Analyze job opportunities with GO/NO-GO assessment, company research, and tailored application materials.**

---

## Chain Map

```
/career-search → discover-jobs.ts → ranked results → user picks → /career
                                                                     │
/career → phases/00-workflow.md ─┬→ 01-assess.md (GO/NO-GO gate)     [advisor]
                                 │     │
                                 │     ├─ NO-GO → STOP
                                 │     │
                                 │     ├─ GO ───────────────────┐
                                 │                              ▼
                                 ├→ 02-research.md (10+ sources)      [researcher]
                                 ├→ 03-prepare.md (priority areas)    [advisor]
                                 ├→ 04-generate.md (6 deliverables)   [writer]
                                 └→ 05-deliver.md (submission)        [advisor]
                                          │
                                          ▼
                                 output/{company}-{role}-{date}/
                                 ├── job-posting.md
                                 ├── match-assessment.md
                                 ├── company-research.md
                                 ├── interview-prep.md
                                 ├── resume.md
                                 └── cover-letter.md

Agent boundaries:
  advisor ──→ researcher ──→ advisor ──→ writer ──→ advisor
  (assess)    (research)     (prepare)   (generate)  (deliver)
```

**All files follow the universal prompt structure:** `docs/guides/universal-prompt-structure.md`

---

## Supporting Documentation (READ FIRST)

**⚠️ MANDATORY: Read these supporting documents BEFORE executing this skill:**

1. **`docs/professional-tone-requirements.md`** - Formatting standards for all deliverables (resumes, cover letters)
2. **`docs/skill-tier-integration.md`** - Model tier routing and cost optimization

**These documents contain critical requirements** that MUST be followed during execution. Failure to read them will result in deliverables that violate formatting standards or use incorrect model tiers.

---

## Model Tier Routing

This skill uses the three-tier orchestration engine for cost-optimal execution:

**Routing Decision Tree:**
- **Career advice/guidance:** Tier 1 (Free) - $0.00 (e.g., "How to evaluate a job offer?")
- **Job analysis (GO/NO-GO assessment):** Tier 2a (Grok 3 Mini) - $0.80/1M ← Primary
- **Full workflow cost:** ~$1.10 (67% savings vs Sonnet-only)

**Why Tier 2a (not Tier 2b)?**
- Tier 2a (Grok 3 Mini) specializes in "assumption challenging"
- $0.80/1M (vs $0.70/1M for Grok 4.1 Fast)
- Premium for adversarial reasoning on high-stakes career decisions:
  - Challenge job fit assumptions before applying
  - Validate company culture claims before committing
  - Test compensation assumptions against market data
  - Similar to wellness skill - both use Tier 2a for assumption testing on personal decisions
- Differs from other skills which use Tier 2b for orchestration efficiency

**How it works:**
1. User provides opportunity details or posts resume
2. Base Claude analyzes request type (advice vs. full analysis)
3. Guidance queries route to Tier 1, GO/NO-GO analysis routes to Tier 2a
4. Tier 2a's assumption-challenging helps validate before user commits time to applications

**See `docs/skill-tier-integration.md` for complete routing logic and cost breakdown.**

---

## Pre-flight Checklist (MANDATORY)

**STOP! Before executing this skill:**

- [ ] Read this SKILL.md completely
- [ ] Understand the 5-phase workflow
- [ ] Phase 1 (Assess) is the CRITICAL GATE - NO-GO = stop entirely
- [ ] Resume ethics: NEVER fabricate experience, skills, or achievements
- [ ] Professional tone requirements: No AI cliches, emojis, or icons
- [ ] Resume chronology: Present to past (reverse chronological)

---

## Core Philosophy

**GO/NO-GO First:** Don't waste time on poor-fit roles. Phase 1 determines if you proceed.

**Evidence-Based:** All claims backed by research with cited sources.

**Ethics Mandatory:** Optimization = highlighting relevant experience. Fabrication = changing what you did. Never cross that line.

---

## USE WHEN

**Use for:** Job opportunity evaluation, GO/NO-GO assessment, company research, interview prep, tailored deliverables, job search (`/career-search`)

**Don't use for:** General career advice, resume formatting only, non-application company info

---

## Environment Setup

No external APIs or authentication required. Job discovery uses web scraping, research uses built-in WebSearch/WebFetch tools. Optional: place resume at `skills/career/input/resume.md`.

---

## Job Discovery Mode (NEW)

Automatically search and score jobs from hiring.cafe using `/career-search` command or the scraper script directly.

**Features:** Web scraping (no API keys), GO/NO-GO scoring, ranked results, parallel analysis of top matches.

**See:** `commands/career-search.md` for search workflow.

---

## Critical Rules

1. **GO/NO-GO is the Gate** - Score <60% = STOP
2. **Resume Ethics** - NEVER fabricate experience/skills
3. **Cite Sources** - All research cited inline with URLs
4. **No Guessing** - If resume gaps exist, ASK USER
5. **Professional Tone** - No AI cliches/emojis/icons
6. **Resume Chronology** - Reverse chronological (present to past)

---

## Professional Tone Requirements (MANDATORY)

**READ `docs/professional-tone-requirements.md` for complete formatting standards.**

Key: No emojis/icons/AI cliches, formal business tone, resumes reverse chronological (2 pages max), cover letters 4 paragraphs (350 words max).

---

## Resource Auto-Detection

Auto-detects resume from `skills/career/input/` (supports `.md`, `.pdf`, `.docx`). Prompts user if multiple/none found.

---

## 5-Phase Workflow

```
┌─────────┐     ┌──────────┐     ┌─────────┐     ┌──────────┐     ┌─────────┐
│ ASSESS  │────▶│ RESEARCH │────▶│ PREPARE │────▶│ GENERATE │────▶│ DELIVER │
│ (Gate)  │     │          │     │         │     │          │     │         │
└────┬────┘     └────┬─────┘     └────┬────┘     └────┬─────┘     └────┬────┘
     │               │                │               │               │
     ▼               ▼                ▼               ▼               ▼
  GO/NO-GO      10+ Sources      5 Priority      6 Files         Strategy
  Decision      Collected        Areas + Q&A     Created         Provided
```

| Phase | Name | Gate Criteria | Output |
|-------|------|---------------|--------|
| 1 | **ASSESS** | GO/NO-GO decision made (≥60% = GO) | Match score, decision |
| 2 | **RESEARCH** | 10+ sources collected | Company intelligence |
| 3 | **PREPARE** | 5 priority areas, 10-12 Q&A | Interview prep |
| 4 | **GENERATE** | All 6 files created | Deliverables |
| 5 | **DELIVER** | User has next steps | Submission strategy |

**CRITICAL:** If Phase 1 results in NO-GO (<60%), STOP. Do not proceed to Phase 2.

---

## Phase 1: ASSESS (GO/NO-GO Gate)

**The most important phase. Determines if this opportunity is worth pursuing.**

### Scoring Methodology

| Category | Weight | Criteria |
|----------|--------|----------|
| Required Skills Match | 40% | Direct match to job requirements |
| Experience Level | 25% | Years and seniority alignment |
| Nice-to-Have Skills | 20% | Preferred qualifications |
| Industry/Domain Match | 15% | Sector familiarity |

### Decision Gates

| Score | Decision | Action |
|-------|----------|--------|
| ≥75% | **GO** | Strong fit - proceed with full workflow |
| 60-74% | **CONDITIONAL GO** | Gaps exist - proceed but note gaps clearly |
| <60% | **NO-GO** | Poor fit - STOP, recommend user look elsewhere |

### Red Flags (Auto NO-GO)

- Required certification not held (and can't obtain quickly)
- Experience 5+ years below requirement
- Technology stack 0% overlap
- Location requires unwanted relocation

**Phase File:** `phases/01-assess.md`

---

## Phase 2: RESEARCH (Company Intelligence)

**Gather comprehensive intelligence on the target company.**

### Research Sources

| Source | Tool | Purpose |
|--------|------|---------|
| Web Search | WebSearch | Company basics, leadership, news, tech stack |
| Social Intel | Grok via OpenRouter | Real-time X/Twitter sentiment, employee chatter |

### Research Categories

1. **Company Basics** - Size, HQ, industry, funding, recent news
2. **Leadership** - CISO/CIO/CTO backgrounds, priorities
3. **Security/Compliance** - Breach history, certifications, posture
4. **Culture & Sentiment** - Glassdoor, employee reviews
5. **Tech Stack** - Languages, frameworks, cloud providers
6. **Recent Developments** - Funding, acquisitions, hiring trends

### Gate Criteria

- [ ] 10+ sources collected with URLs
- [ ] All 6 research categories covered
- [ ] Sources cited inline per section

**Phase File:** `phases/02-research.md`

---

## Phase 3: PREPARE (Interview Preparation)

**Develop priority areas and interview Q&A based on research.**

### Priority Areas (5)

For each priority area:
- **Why It Matters** - Evidence from research
- **Their Need** - What they're seeking
- **Your Position** - How to leverage your experience
- **Talking Points** - 2-3 key points to emphasize

### Interview Q&A (10-12 Questions)

| Category | Count | Focus |
|----------|-------|-------|
| Technical | 3-4 | Role-specific technical depth |
| Behavioral | 3-4 | STAR method responses |
| Scenario | 3-4 | Problem-solving approach |

### Questions to Ask (5-7)

Strategic questions that demonstrate research and genuine interest.

**Phase File:** `phases/03-prepare.md`

---

## Phase 4: GENERATE (Create Deliverables)

**Create EXACTLY 6 focused deliverable files.**

**CRITICAL:** All deliverables MUST follow Professional Tone Requirements (see section above).

### Deliverables

**All filenames lowercase-hyphen following Unix standards. NO CAPS, NO SPACES, NO NUMBERS.**

| File | Size | Content |
|------|------|---------|
| `job-posting.md` | 50-150 lines | Original job description, **APPLICATION URL** (critical!), metadata |
| `match-assessment.md` | 100-200 lines | GO/NO-GO score, decision, strengths, gaps, recommendation |
| `company-research.md` | 200-400 lines | Company intel, culture, leadership, sources (10+ cited) |
| `interview-prep.md` | 300-500 lines | Priority areas (5), Q&A (10-12), questions to ask (5-7) |
| `resume.md` | 1-2 pages | Resume optimized for this role (reverse chronological) |
| `cover-letter.md` | <350 words | 4-paragraph cover letter (no cliches) |

**Requirements:** Each file standalone and focused. NO 900+ line executive summaries, NO multiple versions, NO ALL CAPS/numbered/spaced filenames, NO extra files beyond the 6 specified.

### job-posting.md Template

```markdown
# [Company] - [Position Title]

## ⚠️ Application Information (CRITICAL)

**Application URL:** [Full clickable URL - TEST THIS LINK]
**Job ID/Requisition:** [ID if available - helps find posting if URL breaks]
**Application Deadline:** [Date if specified]

**Source:** [Indeed, LinkedIn, company careers page, referral]
**Date Found:** [YYYY-MM-DD]
**Posting Date:** [YYYY-MM-DD if available]
**Location:** [City, State]

---

## Job Description

[Full original job posting text - complete, unedited]

---

## Application Requirements

- [Requirement 1: e.g., resume, cover letter]
- [Requirement 2: e.g., portfolio, references]
- [Any specific application instructions]

---

## Additional Notes

[Any relevant notes about the application process, contacts, referrals, etc.]
```

**CRITICAL REQUIREMENTS:**
- Application URL must be complete and functional (test the link!)
- Include Job ID/requisition number if available (backup way to find posting)
- Original job text must be complete (postings often get removed later)
- This file is THE source of truth for applying - without it, user cannot apply

### Resume Ethics (MANDATORY)

**ALLOWED:**
- Reorder bullets to emphasize relevant experience
- Reorder positions to ensure reverse chronological order (most recent first)
- Rewrite Professional Summary for this role
- Remove irrelevant positions
- Add keywords from job posting (if you actually have the skill)

**FORBIDDEN:**
- Change job titles
- Fabricate experience or achievements
- Add technologies you didn't actually use
- Guess at undocumented experience

**If gaps exist:** STOP and ASK USER before proceeding.

### Formatting Enforcement

Before finalizing deliverables, verify:
- [ ] **EXACTLY 6 .md files** with lowercase-hyphen names
- [ ] **job-posting.md has working Application URL** (test the link!)
- [ ] **No files exceed size limits** (match: 200, company: 400, interview: 500 lines)
- [ ] **No "executive summary" file** that duplicates everything
- [ ] Resume work experience is reverse chronological - VERIFY: First position has most recent end date, last position has oldest end date
- [ ] Resume and cover letter have current date (YYYY-MM-DD format)
- [ ] Resume uses bullet points with proper spacing - no squished dense paragraphs
- [ ] No emojis, icons, or decorative symbols in any file
- [ ] No AI cliches or buzzwords
- [ ] All bullet points are complete sentences or detailed phrases
- [ ] Professional business tone throughout
- [ ] Cover letter is under 350 words with 4 paragraphs
- [ ] Cover letter ends at signature line with NO extra content below
- [ ] Resume has NO extra notes or instructions below main content
- [ ] Both documents are ready to print/send as-is

### Output Validation Checklist

Before marking Phase 4 complete, validate:

```python
# Validation requirements
required_files = [
    "job-posting.md",      # Must have Application URL with http/https
    "match-assessment.md", # Max 200 lines
    "company-research.md", # Max 400 lines
    "interview-prep.md",   # Max 500 lines
    "resume.md",           # 1-2 pages
    "cover-letter.md"      # <350 words
]

# Exactly 6 .md files (no extras, no PDFs unless requested)
# All filenames match regex: ^[a-z-]+\.md$
# job-posting.md contains "Application URL:" and "http"
# No file named "executive-summary.md" or "1-EXECUTIVE-SUMMARY.md"
```

**Phase File:** `phases/04-generate.md`

---

## Phase 5: DELIVER (Submission Strategy)

**Provide actionable next steps for the user.**

### Submission Timing
- Best days: Tuesday-Thursday
- Best time: 7-9 AM in company timezone
- Avoid: Friday afternoon, weekends, holidays

### Follow-Up Timeline
- Day 3-5: LinkedIn connection to hiring manager
- Week 2: Follow-up email if no response
- Week 4: Final check-in, then move on

### Networking Strategy
- Identify 2nd-degree connections
- Informational interview opportunities
- Internal referral possibilities

**Phase File:** `phases/05-deliver.md`

---

## Deliverable Finalization Standards

**CRITICAL: All output files must be production-ready.**

### Output Requirements
- Lowercase-hyphen filenames only: `resume.md` not `RESUME.md`
- Production-ready: Copy/paste to Word/PDF with no editing needed
- Current dates, clean formatting, no markdown artifacts or AI comments

---

## Output Structure

**EXACTLY 6 files. No more, no less.**

**Naming Convention:** All lowercase-hyphen following Unix standards.

```
skills/career/output/{company}-{role}-{date}/
├── job-posting.md           # Original job description and APPLICATION URL (critical!)
├── match-assessment.md      # GO/NO-GO analysis (100-200 lines, concise)
├── company-research.md      # Company intelligence (200-400 lines)
├── interview-prep.md        # Priority areas and Q&A (300-500 lines - the bulk)
├── resume.md                # Resume optimized for role (1-2 pages)
└── cover-letter.md          # Cover letter (<350 words)
```

**File Naming Rules:** All lowercase-hyphen (Unix standards). NO caps, spaces, numbers, versions, or mixed case.

**DO NOT create:** README/executive-summary files, phases/ subdirectory, multiple versions, PDFs (unless requested), or anything beyond the 6 files listed above.

### Content Distribution (IMPORTANT)

**DO NOT create a massive "executive summary" that duplicates everything.** Content should be distributed as follows:

- **job-posting.md**: Job description + application URL (THE critical file for applying)
- **match-assessment.md**: GO/NO-GO decision ONLY (concise, 2 pages max)
- **company-research.md**: Company intelligence with sources
- **interview-prep.md**: Priority areas + Q&A + questions (this gets the bulk of interview content)
- **resume.md**: Production-ready resume
- **cover-letter.md**: Production-ready cover letter

Each file is **standalone, focused, and manageable** - no 900+ line monsters.

---

## Progress Tracking

**Progress is tracked via phase checkpoint output displayed to user after each phase completes.**

Phase flow: ASSESS → RESEARCH → PREPARE → GENERATE → DELIVER

Each phase: Load prompt → Execute → Verify gate → Show checkpoint → Advance or stop.

---

## Model Selection

**Default:** Sonnet (analysis, document generation)
**Research:** WebSearch + Grok via OpenRouter (social intel)

---

## Error Recovery

| Error | Recovery |
|-------|----------|
| Resume not found | Ask user to provide path |
| NO-GO result | Stop gracefully, explain why, suggest alternatives |
| Research gaps | Note what couldn't be found, proceed with available info |
| Major resume gaps | STOP, ask user before assuming |

---
**Version:** 2.1 | **Last Updated:** 2026-02-08 | **Status:** Active | **Structure:** Universal Prompt Structure v2.0