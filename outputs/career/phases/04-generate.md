---
domain: career
skill: career
agent: writer
model: sonnet
mode: multi-agent
complexity: high
chain_position: middle
---

# Phase 4: GENERATE (Create Deliverables)

## IDENTITY

**Agent:** `agents/writer.md` (loaded automatically from METADATA `agent:` field)

**Phase-specific role:** Create production-ready resume and cover letter from assessment and research data. Transform analysis into submission-ready application materials.

**Additional constraints:** Follow `docs/professional-tone-requirements.md`. Never fabricate experience, skills, or achievements. No emojis, AI cliches, or decorative elements. If resume gaps require fabrication to fill, STOP and ask user.

---

## INPUT CONTRACT

**Receives:**
- `match-assessment.md` from Phase 1 (strengths, gaps, scoring)
- `company-research.md` from Phase 2 (company intelligence)
- `interview-prep.md` from Phase 3 (priority areas, talking points)
- Resume from `skills/career/input/` (`.md`, `.pdf`, `.docx`, or other format)
- Job posting text (from Phase 1 parsing)
- Output directory: `skills/career/output/{company}-{role}-{date}/`

**Prerequisites:**
- Phases 1-3 completed
- All three output files exist in output directory
- Resume accessible

**Source:** `skills/career/phases/03-prepare.md`

---

## OBJECTIVE

**Goal:** Create 6 production-ready deliverable files: job posting archive, match assessment (finalize), company research (finalize), interview prep (finalize), tailored resume, and cover letter.

**Success criteria:**
- All 6 files exist in output directory
- Resume is 1-2 pages, reverse chronological, ATS-compliant
- Cover letter is <350 words, 4 paragraphs, company-specific
- No fabricated content in any file
- All filenames lowercase-hyphen
- All files production-ready (copy/paste to submit)

**Failure criteria:**
- Resume gaps require fabrication to fill → STOP, ask user
- Missing company research for cover letter → Return to Phase 2

---

## METHODOLOGY

Phase 4 is where analysis becomes output. The first 3 phases gathered intelligence; this phase transforms it into submission-ready materials.

**Resume optimization philosophy:**
Optimization means HIGHLIGHTING relevant experience, not FABRICATING it. Reorder bullets to lead with relevant achievements. Rewrite the professional summary for this specific role. Remove irrelevant positions to stay within 1-2 pages. Add keywords from the job posting — but ONLY for skills you actually have.

**Cover letter strategy:**
A cover letter proves you did research. Paragraph 1 hooks with something specific about THIS company. Paragraph 2 connects YOUR experience to THEIR needs. Paragraph 3 explains why THIS company (not just this role). Paragraph 4 is the call to action. Every paragraph should reference something from Phase 2 research.

**The job-posting.md file is critical.** Job postings get removed. The archived posting with application URL is the user's backup way to find the application. Always verify the URL works.

**Quality over quantity:** Each file should be standalone, focused, and manageable. No 900+ line executive summaries. No duplicate content across files. Each file serves one purpose.

---

## EXECUTION

### Step 1: Archive Job Posting

**Tool:** Write

Create `job-posting.md` with the complete original job description and application URL.

**Template:**
```markdown
# [Company] — [Position Title]

## Application Information

**Application URL:** [Full clickable URL — TEST THIS LINK]
**Job ID/Requisition:** [ID if available]
**Application Deadline:** [Date if specified]

**Source:** [Where posting was found]
**Date Found:** [YYYY-MM-DD]
**Posting Date:** [YYYY-MM-DD if available]
**Location:** [City, State / Remote]

---

## Job Description

[Full original job posting text — complete, unedited]

---

## Application Requirements

- [Requirement 1]
- [Requirement 2]

---

## Notes

[Any relevant notes about process, contacts, referrals]
```

**Expected output:** `job-posting.md` with working application URL
**Success indicator:** Application URL contains `http` and is testable
**On failure:** If URL not available, note prominently: "APPLICATION URL NEEDED — add before submitting"

### Step 2: Finalize Phase 1-3 Documents

**Tool:** Read + Write

Review `match-assessment.md`, `company-research.md`, and `interview-prep.md`. Ensure they're complete and consistent. Fix any formatting issues.

**Expected output:** All 3 files finalized
**Success indicator:** No TODOs, placeholders, or incomplete sections

### Step 3: Create Tailored Resume

**Tool:** Read + Write
**Reference:** `skills/career/templates/resume-template.md`

Load the resume template first. Then create the tailored resume.

**Resume Ethics (MANDATORY):**

| ALLOWED | FORBIDDEN |
|---------|-----------|
| Reorder bullets to emphasize relevant experience | Change job titles |
| Rewrite Professional Summary for this role | Fabricate experience or achievements |
| Remove irrelevant positions | Add technologies you didn't use |
| Add keywords (if you actually have the skill) | Guess at undocumented experience |
| Adjust formatting for readability | Inflate metrics or scope |

**If resume gaps exist:** STOP and ask user before proceeding.

**ATS Compliance:**
- **Order:** REVERSE CHRONOLOGICAL — most recent position FIRST, oldest LAST
- **Layout:** Single column, no tables/graphics/text boxes
- **Contact:** In body text, not header/footer
- **Length:** 1-2 pages maximum
- **Bullets:** Simple hyphens or standard bullets

**MANDATORY ordering verification:**
1. Extract all positions with their dates
2. Sort by end date — most recent first
3. Verify: first position has most recent end date, last has oldest
4. If source resume is in wrong order, REORDER it

**Keyword optimization:**
- Match job description language exactly
- Include both acronym AND full form: "Amazon Web Services (AWS)"
- Mirror skills section to job posting requirements

**Expected output:** `resume.md` — 1-2 pages, reverse chronological, ATS-compliant
**Success indicator:** First position has most recent date, no fabricated content
**On failure:** If gaps found, ask user for clarification before proceeding

### Step 4: Create Cover Letter

**Tool:** Read + Write
**Reference:** `skills/career/templates/cover-letter-template.md`

Load the cover letter template first. Then create the cover letter.

**Structure (4 paragraphs, 250-350 words):**

```markdown
[Date]

[Hiring Manager Name if known]
[Company Name]

Dear [Hiring Manager / Hiring Team],

**Paragraph 1: Hook + Position**
[Why you're excited about THIS role at THIS company. Reference something specific from research.]

**Paragraph 2: Value Proposition**
[Your most relevant experience. Connect YOUR background to THEIR needs. Specific examples.]

**Paragraph 3: Why This Company**
[What attracts you specifically. Reference research findings — culture, mission, news.]

**Paragraph 4: Call to Action**
[Express enthusiasm, note availability, thank them.]

Sincerely,
[Your Name]
[Phone]
[Email]
```

**Quality criteria:**
- References company-specific research (not generic)
- Connects experience to stated needs
- Shows genuine interest (not form letter)
- Professional but personable tone
- Under 350 words
- No content after signature line

**Expected output:** `cover-letter.md` — <350 words, 4 paragraphs, company-specific
**On failure:** If too generic, add specific research references

### Step 5: Quality Validation

**Tool:** Direct review

Before finalizing, verify ALL deliverables:

**File validation:**
- [ ] Exactly 6 `.md` files with lowercase-hyphen names
- [ ] `job-posting.md` has application URL with `http`
- [ ] No files exceed size guidance (assessment: ~200, research: ~400, prep: ~500 lines)
- [ ] No "executive summary" or duplicate files

**Resume validation:**
- [ ] No emojis, icons, or decorative symbols
- [ ] No AI cliches ("leverage", "dynamic", "passionate", "proven track record", "results-driven", "synergy")
- [ ] Reverse chronological order VERIFIED (first position = most recent)
- [ ] No fabricated experience — all content from source resume
- [ ] 1-2 pages, complete sentences, professional tone
- [ ] Current date in YYYY-MM-DD format

**Cover letter validation:**
- [ ] Under 350 words
- [ ] 4 paragraphs
- [ ] Company-specific references from research
- [ ] No AI cliches
- [ ] Ends at signature — no extra content below
- [ ] Current date

**Overall:**
- [ ] All files production-ready (no TODOs, placeholders, notes)
- [ ] Consistent formatting across all files
- [ ] Ethical standards met

**If ANY check fails:** Fix before proceeding to Phase 5.

---

## OUTPUT CONTRACT

**Produces:**
All files written to `skills/career/output/{company}-{role}-{date}/`:

| File | Description | Size |
|------|-------------|------|
| `job-posting.md` | Original job description + application URL | 50-150 lines |
| `match-assessment.md` | GO/NO-GO score, decision, strengths, gaps | 100-200 lines |
| `company-research.md` | Company intel with 10+ cited sources | 200-400 lines |
| `interview-prep.md` | Priority areas, Q&A, questions to ask | 300-500 lines |
| `resume.md` | Resume tailored for role (reverse chronological) | 1-2 pages |
| `cover-letter.md` | Company-specific cover letter | <350 words |

**Format:** All filenames lowercase-hyphen. All content production-ready.

**DO NOT create:** Executive summary files, phases/ subdirectory, multiple versions, PDFs (unless requested), or anything beyond the 6 files listed.

---

## NEXT

**On success:** → Return to advisor agent for Phase 5 (Deliver):

```
Task(subagent_type="advisor", prompt="Execute career Phase 5 (Deliver). Load skills/career/phases/05-deliver.md. Output dir: {output_dir}")
```

  Pass: All 6 deliverable files in `skills/career/output/{company}-{role}-{date}/`

**On validation failure:** → Fix failing items, re-validate before proceeding

**On resume gap:** → STOP, ask user for clarification, then continue

---

## CHECKPOINTS

**Exit criteria (ALL must be true):**
- [ ] All 6 files exist in output directory
- [ ] All filenames are lowercase-hyphen
- [ ] `job-posting.md` has application URL
- [ ] Resume is reverse chronological (verified)
- [ ] Resume has no fabricated content
- [ ] Cover letter is <350 words with 4 paragraphs
- [ ] No emojis, AI cliches, or decorative elements in any file
- [ ] All files are production-ready

**Error recovery:**
- If resume gaps require fabrication: STOP, ask user for clarification
- If missing research for cover letter: Return to Phase 2 for more intel
- If resume too long: Prioritize relevant experience, remove older roles
- If cover letter too generic: Add company-specific research references

---

**Framework:** Intelligence Adjacent (IA)
**Structure:** Universal Prompt Structure v2.0
