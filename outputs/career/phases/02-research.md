---
domain: career
skill: career
agent: researcher
model: sonnet
mode: multi-agent
complexity: medium
chain_position: middle
---

# Phase 2: RESEARCH (Company Intelligence)

## IDENTITY

**Agent:** `agents/researcher.md` (loaded automatically from METADATA `agent:` field)

**Phase-specific role:** Gather company intelligence across 6 categories to inform career interview preparation and validate the Phase 1 GO decision.

**Additional constraints:** Focus on role-relevant research. Adapt depth by company size (startup vs enterprise). Minimum 10 sources. Never fabricate company information — if data isn't available, say so.

---

## INPUT CONTRACT

**Receives:**
- `match-assessment.md` from Phase 1 (GO or CONDITIONAL GO decision confirmed)
- Output directory: `skills/career/output/{company}-{role}-{date}/`
- Company name and role title (extracted from Phase 1 output)

**Prerequisites:**
- Phase 1 completed with GO or CONDITIONAL GO decision
- `match-assessment.md` exists in output directory

**Source:** `skills/career/phases/01-assess.md`

---

## OBJECTIVE

**Goal:** Gather 10+ cited sources of company intelligence across 6 categories to inform interview preparation.

**Success criteria:**
- 10+ unique sources collected with URLs
- All 6 research categories covered (basics, leadership, security/compliance, culture, tech stack, social media)
- Sources cited inline per section
- Key insights identified for interview prep

**Failure criteria:**
- Company too new/small for 10 sources → proceed with available, note limitation
- WebSearch completely unavailable → STOP, report to user

---

## METHODOLOGY

Company research serves two purposes: (1) inform the interview preparation with specific talking points, and (2) validate Phase 1's GO decision with real company data. A company that looked good on paper but has terrible Glassdoor reviews or recent layoffs changes the calculation.

**Research priority order:**
1. **Company basics** — foundation for everything else
2. **Leadership and team structure** — directly affects interview experience
3. **Recent news and developments** — conversation starters, red flag detection
4. **Security/compliance posture** — role-specific relevance (especially for security roles)
5. **Culture signals** — validate whether this is truly a good fit
6. **Tech stack** — verify alignment with resume skills

**Adaptation by company size:**
- **Startup (<50 employees):** Skip formal org research. Focus on founder backgrounds, funding stage, growth signals, burn rate indicators. Crunchbase and LinkedIn are primary sources.
- **Mid-market (50-1000):** Balance between formal and startup. Look for engineering blog, recent press, key hires.
- **Enterprise (1000+):** Emphasize compliance posture, team size, reporting structure, recent incidents, formal initiatives.

**Source quality hierarchy:**
Official company pages > Press releases > News articles > Glassdoor reviews > Social media chatter > LinkedIn job postings (for team structure inference)

---

## EXECUTION

### Step 1: Company Basics

**Tool:** WebSearch
**Query pattern:** `"[Company Name]" company overview headquarters founded employees`

Search for foundational company information: founded year, headquarters, employee count, industry, funding stage, public/private status.

**Expected output:** Company profile with 2+ sources
**Success indicator:** At least company size and industry identified
**On failure:** Try `"[Company Name]" about us` or `"[Company Name]" crunchbase`

### Step 2: Leadership Research

**Tool:** WebSearch
**Query pattern:** `"[Company Name]" [CISO|CTO|CIO|VP Engineering] leadership team`

Search for relevant leadership — prioritize the reporting chain for the target role.

**Expected output:** Key leaders identified with backgrounds and priorities
**Success indicator:** At least 1 relevant leader identified
**On failure:** Search LinkedIn company page for leadership section

### Step 3: Security & Compliance Posture

**Tool:** WebSearch
**Query pattern:** `"[Company Name]" [SOC 2|ISO 27001|security|breach|compliance]`

Search for security certifications, breach history, compliance environment, bug bounty programs.

**Expected output:** Security posture summary with sources
**Success indicator:** At least compliance environment or certification status identified
**On failure:** Note as "limited public security information" — not a red flag for non-security companies

### Step 4: Culture & Sentiment

**Tool:** WebSearch
**Query pattern:** `"[Company Name]" glassdoor reviews culture work-life balance`

Search Glassdoor, LinkedIn, news for culture indicators.

**Expected output:** Culture indicators with Glassdoor rating (if available), key themes, any red flags
**Success indicator:** At least 2 culture data points collected
**On failure:** Note as "limited culture data" — small/private companies may have few reviews

### Step 5: Tech Stack Discovery

**Tool:** WebSearch
**Query pattern:** `"[Company Name]" engineering blog tech stack [languages|cloud|tools]`

Search for engineering blog, StackShare, job postings that reveal technology.

**Expected output:** Technology stack overview with sources
**Success indicator:** At least cloud provider or primary language identified
**On failure:** Infer from similar job postings at the company

### Step 6: Social Media Intelligence

**Tool:** WebSearch
**Query pattern:** `site:twitter.com "[Company Name]" OR site:x.com "[Company Name]"`

Search for recent social media presence, employee sentiment, public perception.

If OpenRouter is available, use Grok for real-time X/Twitter analysis:
```
Model: x-ai/grok-beta
Prompt: Search X/Twitter for recent posts about [Company Name] focusing on:
employee sentiment, recent announcements, customer feedback, hiring/layoff signals
```

**Expected output:** Social media findings with dates
**Success indicator:** At least 1 social media data point collected
**On failure:** Note as "limited social media presence" — use web search results instead

### Step 7: Compile and Write Output

**Tool:** Write
**Reference:** Output format below

Compile all research into `company-research.md` with inline citations and source index.

---

## OUTPUT CONTRACT

**Produces:**
- `company-research.md` → written to `skills/career/output/{company}-{role}-{date}/company-research.md`

**Format:**

```markdown
# Company Research: [Company Name]

**Role:** [Job Title]
**Date:** [YYYY-MM-DD]
**Sources Collected:** [X]

---

## Company Profile
[Content from Step 1 with inline source citations]

## Leadership
[Content from Step 2 with inline source citations]

## Security & Compliance Posture
[Content from Step 3 with inline source citations]

## Culture & Sentiment
[Content from Step 4 with inline source citations]

## Technology Stack
[Content from Step 5 with inline source citations]

## Social Media Intelligence
[Content from Step 6 with dates]

---

## Source Index

1. [Title] - [URL]
2. [Title] - [URL]
...
[Minimum 10 sources]

---

## Key Insights for Interview

1. [Insight that should inform interview prep — specific, actionable]
2. [Insight that should inform interview prep]
3. [Insight that should inform interview prep]
```

**Size:** 200-400 lines

---

## NEXT

**On success:** → Return to advisor agent for Phase 3 (Prepare):

```
Task(subagent_type="advisor", prompt="Execute career Phase 3 (Prepare). Load skills/career/phases/03-prepare.md. Output dir: {output_dir}")
```

  Pass: `company-research.md` (this phase's output) + `match-assessment.md` (Phase 1 output)
  Both files in `skills/career/output/{company}-{role}-{date}/`

**On source shortage (<10):** → Proceed if all 6 categories attempted, note limitation in output

---

## CHECKPOINTS

**Exit criteria (ALL must be true):**
- [ ] 10+ sources collected (or limitation noted if company too small/new)
- [ ] All 6 research categories attempted
- [ ] Sources cited inline with URLs throughout
- [ ] Key insights section populated with 3+ actionable insights
- [ ] `company-research.md` written to output directory
- [ ] Source index with numbered URLs at bottom

**Error recovery:**
- If company very small/new: Note limited info, proceed with available data
- If Grok/OpenRouter unavailable: Use WebSearch for social media instead
- If <10 sources after all categories: Note limitation, proceed if critical categories covered
- If leadership info unavailable: Search LinkedIn, infer from job postings

---

**Framework:** Intelligence Adjacent (IA)
**Structure:** Universal Prompt Structure v2.0
