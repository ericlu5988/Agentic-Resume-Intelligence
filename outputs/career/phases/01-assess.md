---
domain: career
skill: career
agent: advisor
model: sonnet
mode: single-agent
complexity: medium
chain_position: first
---

# Phase 1: ASSESS (GO/NO-GO Gate)

## IDENTITY

**Agent:** `agents/advisor.md` (loaded automatically from METADATA `agent:` field)

**Phase-specific role:** Evaluate job opportunity fit by scoring candidate against job requirements using weighted methodology. Make GO/NO-GO decision.

**Additional constraints:** Score <60% = mandatory NO-GO. Never inflate scores. Never fabricate resume content. A poor-fit role gets NO-GO regardless of user preference.

---

## INPUT CONTRACT

**Receives:**
- Job posting (text pasted by user or fetched from URL)
- Resume from `skills/career/input/` (any format: `.md`, `.pdf`, `.docx`, `.txt` — or user-provided path)
- Output directory: `skills/career/output/{company}-{role}-{date}/`

**Prerequisites:**
- Job posting text is available
- Resume is accessible and readable

**Source:** `skills/career/phases/00-workflow.md` (workflow orchestrator)

---

## OBJECTIVE

**Goal:** Determine if this job opportunity is worth pursuing by calculating a weighted match score and making a GO/NO-GO decision.

**Success criteria:**
- Job posting parsed into structured requirements (must-have, nice-to-have, certifications, experience level)
- Resume loaded and relevant experience mapped to requirements
- Match score calculated using weighted methodology
- Red flags checked (auto NO-GO triggers)
- GO/NO-GO decision made with justification

**Failure criteria:**
- Resume not found and user declines to provide → STOP
- Job posting too vague to extract requirements → Ask user for clarification
- Score <60% → NO-GO, stop entire workflow

---

## METHODOLOGY

**Phase 1 is the most important phase.** It prevents wasting time on poor-fit roles. Be honest about gaps — the user benefits more from a truthful NO-GO than from proceeding with a weak application.

**Scoring approach:**
The weighted scoring system prioritizes what actually matters for getting past screening. Required skills match carries 40% because ATS/recruiters filter on these first. Experience level is 25% because seniority mismatch is a common auto-reject. Nice-to-have skills at 20% are differentiators, not dealbreakers. Industry match at 15% matters for domain conversations but won't block an otherwise strong candidate.

**Red flag detection:**
Some gaps are so severe that no score can overcome them. Check these BEFORE calculating the weighted score — any one of them is an automatic NO-GO regardless of total percentage.

**Borderline handling (58-62%):**
Present the score with detailed gap analysis and let the user make the final call. Frame it as: "Here are the specific gaps. If you can address [X] in your cover letter, this becomes viable. If not, your time is better spent elsewhere."

---

## EXECUTION

### Step 1: Parse Job Posting

**Tool:** Direct analysis (no external tool needed)

Extract structured information from the job posting:

- **Company name, role title, location, level, type** (full-time/contract)
- **Must-have requirements** — skills, experience, certifications explicitly marked required
- **Nice-to-have requirements** — preferred qualifications
- **Experience level** — minimum and preferred years
- **Any red flag triggers** — required certifications, specific years, tech stack requirements, relocation

**Expected output:** Structured job requirements list
**Success indicator:** At least 3 must-have requirements identified
**On failure:** If posting is too vague, ask user to provide clarification on requirements

### Step 2: Load Resume

**Tool:** Read
**Reference:** `skills/career/input/*` (Glob for any resume file)

Check `skills/career/input/` for any resume file. Accept `.md`, `.pdf`, `.docx`, `.txt`, or any other format.

**Expected output:** Resume content loaded and readable
**On failure:** Ask user: "No resume found in `skills/career/input/`. Please place your resume there (any format) or provide the path."

### Step 3: Map Experience to Requirements

**Tool:** Direct analysis

For each must-have and nice-to-have requirement:
- Find matching experience in resume (direct match, related experience, or gap)
- Note: match quality — exact match, partial match, or no match
- Document specific resume bullets that demonstrate each matched skill

**Expected output:** Requirement-to-experience mapping
**Success indicator:** Every requirement has a classification (match/partial/gap)

### Step 4: Check Red Flags

**Tool:** Direct analysis

Check for automatic NO-GO conditions:

| Red Flag | Condition |
|----------|-----------|
| Certification gap | Required cert not held AND can't obtain quickly |
| Experience gap | 5+ years below minimum requirement |
| Tech stack mismatch | 0% overlap with required technologies |
| Location conflict | Requires unwanted relocation |

**Expected output:** Red flag status (clear or triggered)
**On failure:** If any red flag triggers → automatic NO-GO, skip scoring

### Step 5: Calculate Match Score

**Tool:** Direct calculation

| Category | Weight | How to Score |
|----------|--------|--------------|
| Required Skills Match | 40% | % of required skills you have (direct or strong partial) |
| Experience Level | 25% | 100% if within 2 years of requirement, scale down for larger gaps |
| Nice-to-Have Skills | 20% | % of preferred skills you have |
| Industry/Domain Match | 15% | Prior work in same/similar sector |

```
Final Score = (Required × 0.40) + (Experience × 0.25) + (NiceToHave × 0.20) + (Industry × 0.15)
```

**Expected output:** Weighted score with category breakdown

### Step 6: Make Decision

| Score | Decision | Action |
|-------|----------|--------|
| ≥75% | **GO** | Strong fit — proceed with full workflow |
| 60-74% | **CONDITIONAL GO** | Gaps exist — proceed but note gaps clearly |
| <60% | **NO-GO** | Poor fit — STOP HERE, explain why |

**Expected output:** Decision with justification

### Step 7: Write Output

**Tool:** Write
**Reference:** Output format below

Write `match-assessment.md` to the output directory.

---

## OUTPUT CONTRACT

**Produces:**
- `match-assessment.md` → written to `skills/career/output/{company}-{role}-{date}/match-assessment.md`

**Format:**

```markdown
# Match Assessment

**Job:** [Role] at [Company]
**Date:** [YYYY-MM-DD]
**Score:** [XX]%
**Decision:** [GO / CONDITIONAL GO / NO-GO]

## Scoring Breakdown

| Category | Weight | Score | Weighted |
|----------|--------|-------|----------|
| Required Skills | 40% | XX% | XX% |
| Experience Level | 25% | XX% | XX% |
| Nice-to-Have | 20% | XX% | XX% |
| Industry Match | 15% | XX% | XX% |
| **TOTAL** | **100%** | - | **XX%** |

## Strengths
- [Strength 1 — specific resume evidence]
- [Strength 2 — specific resume evidence]

## Gaps
- [Gap 1 — and how to address in cover letter/interview]
- [Gap 2 — and how to address]

## Red Flags Checked
- Certification gap: [CLEAR / TRIGGERED — detail]
- Experience gap: [CLEAR / TRIGGERED — detail]
- Tech stack mismatch: [CLEAR / TRIGGERED — detail]
- Location conflict: [CLEAR / TRIGGERED — detail]

## Recommendation
[Detailed recommendation based on score and gaps]
```

**Size:** 100-200 lines

---

## NEXT

**On GO (score ≥60%):** → DELEGATE to researcher agent for company intelligence:

```
Task(subagent_type="researcher", prompt="Execute career Phase 2 (Research). Load skills/career/phases/02-research.md. Company: {company}. Role: {role}. Output dir: {output_dir}")
```

  Pass: `match-assessment.md` with GO decision, output directory path

**On NO-GO (score <60%):** → STOP, then offer `/mentorship`
  Display NO-GO message to user with score, gaps, and recommendations.
  Do NOT proceed to Phase 2.

  After displaying the NO-GO analysis, offer the user a path forward:
  ```
  This role requires skills you don't currently have documented. Would you
  like to use /mentorship to create a development plan for the missing skills?

  Missing skills identified:
  - [Gap 1 from assessment]
  - [Gap 2 from assessment]

  /mentorship can create a learning roadmap with specific goals, resources,
  and timelines to close these gaps for future opportunities.
  ```

  If user accepts → route to `/mentorship` with the gap analysis as context.
  If user declines → workflow ends.

**On borderline (58-62%):** → Present to user, let them decide
  If user says proceed → treat as CONDITIONAL GO
  If user says stop → treat as NO-GO (offer `/mentorship` as above)

---

## CHECKPOINTS

**Exit criteria (ALL must be true):**
- [ ] Job posting parsed into structured requirements
- [ ] Resume loaded and analyzed
- [ ] Match score calculated with category breakdown
- [ ] Red flags checked (all 4 categories)
- [ ] GO/NO-GO decision made with justification
- [ ] `match-assessment.md` written to output directory

**Error recovery:**
- If resume not found: Ask user for path or paste content
- If job posting too vague: Ask user for structured requirements
- If score borderline (58-62%): Present analysis, let user decide

---

**Framework:** Intelligence Adjacent (IA)
**Structure:** Universal Prompt Structure v2.0
