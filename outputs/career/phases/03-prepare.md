---
domain: career
skill: career
agent: advisor
model: sonnet
mode: single-agent
complexity: medium
chain_position: middle
---

# Phase 3: PREPARE (Interview Preparation)

## IDENTITY

**Agent:** `agents/advisor.md` (loaded automatically from METADATA `agent:` field)

**Phase-specific role:** Synthesize job requirements, resume strengths, and company research into actionable interview preparation with specific, evidence-backed talking points.

**Additional constraints:** Every question and answer must tie to actual research findings or resume experience. No generic advice — if it could apply to any company in the industry, it's too generic.

---

## INPUT CONTRACT

**Receives:**
- `match-assessment.md` from Phase 1 (strengths, gaps, score breakdown)
- `company-research.md` from Phase 2 (company intelligence, key insights)
- Resume content (from `skills/career/input/resume.md`)
- Output directory: `skills/career/output/{company}-{role}-{date}/`

**Prerequisites:**
- Phase 1 and Phase 2 completed
- Both `match-assessment.md` and `company-research.md` exist in output directory

**Source:** `skills/career/phases/02-research.md`

---

## OBJECTIVE

**Goal:** Create comprehensive interview preparation materials with 5 priority areas, 10-12 Q&A items, and 5-7 strategic questions to ask.

**Success criteria:**
- 5 priority areas identified with evidence-backed talking points
- 10-12 interview questions with prepared answers (technical, behavioral, scenario)
- 5-7 strategic questions to ask that demonstrate research
- All preparation tied to specific research findings or resume experience
- Quick reference card for day-of-interview review

**Failure criteria:**
- Research too thin to generate specific talking points → Return to Phase 2 for more intel
- Questions too generic (answerable via basic Google) → Revise with company-specific context

---

## METHODOLOGY

Interview prep serves one goal: make the candidate walk in with specific, evidence-backed talking points that demonstrate research and genuine fit.

**Priority area selection:**
Choose 5 areas where the candidate's experience INTERSECTS with the company's stated needs. Each area should have:
- Evidence from research (why it matters to them)
- Evidence from resume (why you're qualified)
- Specific talking points (what to say, not just "mention your experience")

**Question development strategy:**
- **Technical questions (3-4):** Derived from must-have requirements in the job posting. Answers should reference specific projects/achievements from the resume.
- **Behavioral questions (3-4):** Use STAR method. Choose situations that demonstrate the skills most relevant to THIS role. Reference specific companies/projects from resume.
- **Scenario questions (3-4):** Based on likely challenges at THIS company (from research). Approach should reference relevant frameworks or methodologies from resume experience.

**Question quality test:** If a question and answer could apply to any company in the industry, it's too generic. Every answer should reference something specific to THIS company or THIS role.

---

## EXECUTION

### Step 1: Identify Priority Areas

**Tool:** Read (re-read match-assessment.md and company-research.md)
**Reference:** `skills/career/output/{company}-{role}-{date}/match-assessment.md` and `company-research.md`

Cross-reference job requirements, resume strengths, and company research to identify 5 areas where candidate experience aligns with company needs.

For each priority area, develop:
- **Why It Matters** — evidence from research (what tells us this is important to them)
- **Their Need** — specific requirement from job posting or research
- **Your Position** — how your experience aligns (specific resume examples)
- **Talking Points** — 2-3 specific points to emphasize in conversation

**Expected output:** 5 priority areas with full talking point content
**Success indicator:** Each area has specific evidence from both research and resume
**On failure:** If research too thin for specific areas, return to Phase 2

### Step 2: Develop Technical Questions (3-4)

**Tool:** Direct analysis based on job requirements

Create anticipated technical questions based on must-have skills in the job posting.

For each question:
- Structured answer referencing specific resume experience
- Key points to hit
- Concrete example from past work

**Expected output:** 3-4 technical Q&A items
**Success indicator:** Each answer references a specific project or achievement

### Step 3: Develop Behavioral Questions (3-4)

**Tool:** Direct analysis based on role requirements

Create behavioral questions using STAR method (Situation, Task, Action, Result).

Choose situations that demonstrate the most relevant skills for THIS role. Prefer examples that also show knowledge relevant to THIS company's challenges.

**Expected output:** 3-4 behavioral Q&A items in STAR format
**Success indicator:** Each answer has quantifiable results and ties to the target role

### Step 4: Develop Scenario Questions (3-4)

**Tool:** Direct analysis based on company research

Create scenario questions based on likely challenges at THIS company (derived from research findings).

For each scenario:
- Structured approach (first step, second step, etc.)
- Considerations and stakeholders
- Expected outcome

**Expected output:** 3-4 scenario Q&A items
**Success indicator:** Each scenario is company-specific (not generic industry scenarios)

### Step 5: Create Questions to Ask (5-7)

**Tool:** Direct analysis based on company research

Create strategic questions that demonstrate research and genuine interest.

**Quality criteria:**
- Shows you did research (references specific finding)
- Demonstrates strategic thinking
- Reveals genuine interest
- NOT answerable via basic Google search

Categories:
- About the Role (2 questions)
- About the Team (2 questions)
- About the Company (2-3 questions, reference specific research findings)

**Expected output:** 5-7 strategic questions
**Success indicator:** Each question references a specific research finding or company detail

### Step 6: Create Quick Reference Card

**Tool:** Direct synthesis

Summarize the most important preparation points for day-of-interview quick review:
- Top 3 strengths to emphasize
- Top 3 gaps to address proactively (with framing language)
- Company-specific hooks (recent news, leadership priorities, initiatives)

**Expected output:** Quick reference card section

### Step 7: Write Output

**Tool:** Write
**Reference:** Output format below

Compile all preparation materials into `interview-prep.md`.

---

## OUTPUT CONTRACT

**Produces:**
- `interview-prep.md` → written to `skills/career/output/{company}-{role}-{date}/interview-prep.md`

**Format:**

```markdown
# Interview Preparation: [Role] at [Company]

**Date:** [YYYY-MM-DD]
**Based on:** Match Assessment (Phase 1) + Company Research (Phase 2)

---

## Priority Areas

### Priority 1: [Area Name]
**Why It Matters:** [Evidence from research]
**Their Need:** [Specific from job posting]
**Your Position:** [Resume evidence]
**Talking Points:**
1. [Specific point]
2. [Specific point]
3. [Specific point]

[Repeat for Priorities 2-5]

---

## Anticipated Questions

### Technical Questions
[3-4 Q&A items with structured answers]

### Behavioral Questions
[3-4 Q&A items in STAR format]

### Scenario Questions
[3-4 Q&A items with structured approach]

---

## Questions to Ask

### About the Role
1. [Question referencing specific finding]
2. [Question about success metrics]

### About the Team
3. [Question about team structure]
4. [Question about growth]

### About the Company
5. [Question tied to research finding]
6. [Question about strategic direction]
7. [Question about timeline/process]

---

## Quick Reference Card

**Top 3 Strengths to Emphasize:**
1. [Strength with brief talking point]
2. [Strength with brief talking point]
3. [Strength with brief talking point]

**Top 3 Gaps to Address Proactively:**
1. [Gap — how to frame it positively]
2. [Gap — how to frame it]
3. [Gap — how to frame it]

**Company-Specific Hooks:**
- [Reference to recent news/achievement]
- [Reference to leadership priority]
- [Reference to tech/security initiative]
```

**Size:** 300-500 lines

---

## NEXT

**On success:** → DELEGATE to writer agent for deliverable creation:

```
Task(subagent_type="writer", prompt="Execute career Phase 4 (Generate). Load skills/career/phases/04-generate.md. Output dir: {output_dir}. Resume: skills/career/input/resume.md")
```

  Pass: `interview-prep.md` + all previous phase outputs
  All files in `skills/career/output/{company}-{role}-{date}/`

**On failure:** → Return to Phase 2 for additional research if prep materials too thin

---

## CHECKPOINTS

**Exit criteria (ALL must be true):**
- [ ] 5 priority areas with evidence-backed talking points
- [ ] 10-12 Q&A items (3-4 technical + 3-4 behavioral + 3-4 scenario)
- [ ] 5-7 strategic questions to ask (referencing research findings)
- [ ] Quick reference card completed
- [ ] All content tied to specific research findings or resume experience
- [ ] `interview-prep.md` written to output directory

**Error recovery:**
- If research too thin for specific talking points: Return to Phase 2 for more intel
- If questions too generic: Revise to include company-specific context
- If missing gap coverage: Add section on addressing gaps proactively

---

**Framework:** Intelligence Adjacent (IA)
**Structure:** Universal Prompt Structure v2.0
