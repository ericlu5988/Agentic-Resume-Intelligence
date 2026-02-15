---
name: career
description: Job posting analysis with GO/NO-GO assessment, company research, and tailored deliverables
domain: career
skill: career
agent: advisor
model: sonnet
complexity: medium
chain_position: first
---

# /career — Job Application Analysis

## IDENTITY

**Agent:** Base Claude (orchestrator — no specialized agent needed)

**Role:** Career workflow router. Validate user input (job posting), detect resume, determine fresh start vs resume, and load the career workflow orchestrator.

**Note:** This command routes to `phases/00-workflow.md`, which handles multi-agent delegation across the 5-phase pipeline (advisor → researcher → advisor → writer → advisor).

---

## INPUT CONTRACT

**Receives:**
- User invocation: `/career [job posting text or URL]`
- Resume auto-detected from `skills/career/input/` (any format: `.md`, `.pdf`, `.docx`, `.txt`)

**Prerequisites:**
- User has invoked `/career`
- Job posting text available (pasted or URL)

**Source:** User invocation (slash command)

---

## OBJECTIVE

**Goal:** Route user's job analysis request to the career 5-phase workflow.

**Success criteria:**
- Job posting text extracted (from paste or URL fetch)
- Resume located in `skills/career/input/`
- Workflow loaded from `skills/career/phases/00-workflow.md`

**Failure criteria:**
- No job posting provided and user declines to provide → STOP with guidance
- Resume not found and user declines to provide → STOP with guidance

---

## METHODOLOGY

Check for existing work first. If `skills/career/output/` contains a directory matching this company/role, the user may be resuming a prior analysis. Ask before overwriting.

For fresh starts: create output directory as `{company}-{role}-{date}` (lowercase-hyphen, e.g., `acme-security-engineer-2026-02-08`).

Resume detection: check `skills/career/input/` for any file (not just `.md`). The user may have a PDF, Word doc, or markdown resume.

---

## EXECUTION

### Step 1: Extract Job Posting

**Tool:** Direct analysis or WebFetch (if URL provided)

If user pasted text: use directly.
If user provided URL: fetch content with WebFetch.
If neither: ask user to paste job description.

**Expected output:** Job posting text available for analysis
**On failure:** Ask user to paste text directly

### Step 2: Detect Resume

**Tool:** Glob
**Pattern:** `skills/career/input/*`

Check for any resume file in the input directory.

**Expected output:** Resume file path confirmed
**On failure:** Ask user: "No resume found in `skills/career/input/`. Please place your resume there (any format) or provide the path."

### Step 3: Check for Existing Work

**Tool:** Glob
**Pattern:** `skills/career/output/*{company}*`

Check if output directory already exists for this company.

**Expected output:** Fresh start or resume decision
**On failure:** Default to fresh start

### Step 4: Load Workflow

**Tool:** Read
**Reference:** `skills/career/phases/00-workflow.md`

Load the career workflow orchestrator with:
- Job posting text
- Resume file path
- Output directory path

**Expected output:** Workflow loaded, Phase 1 begins

---

## OUTPUT CONTRACT

**Produces:**
- Output directory created: `skills/career/output/{company}-{role}-{date}/`
- Workflow execution initiated (no files created by command itself)

**Final output (after workflow completes):**
```
skills/career/output/{company}-{role}-{date}/
├── job-posting.md
├── match-assessment.md
├── company-research.md
├── interview-prep.md
├── resume.md
└── cover-letter.md
```

---

## NEXT

**On success:** → Load `skills/career/phases/00-workflow.md`
  Pass: Job posting text, resume file path, output directory path

**On resume (existing work):** → Load `skills/career/phases/00-workflow.md`
  Workflow will detect current phase from existing files

**On failure:** → STOP
  Guide user: what they need to provide (job posting and/or resume)

---

## CHECKPOINTS

**Exit criteria (ALL must be true):**
- [ ] Job posting text available
- [ ] Resume file path confirmed
- [ ] Output directory path determined
- [ ] Workflow prompt loaded from `phases/00-workflow.md`

**Error recovery:**
- If job posting URL unreachable: Ask user to paste text directly
- If resume not found: Ask user for path or to place file in `skills/career/input/`
- If existing output found: Ask user if resuming or starting fresh

---

## Usage

```bash
/career
/career [paste job description]
/career https://example.com/job/12345
```

## When to Use

**Use /career when:**
- You have a specific job posting to analyze
- You want to know if a role is worth applying to
- You need company research before applying
- You want tailored resume and cover letter for a specific role

**Don't use if:**
- Need career development guidance → `/mentorship`
- Want strengths analysis → `/clifton`
- Want to search for jobs → `/career-search`
- Need general resume review without a specific job

## Related Commands

- `/career-search` — Discover and rank job opportunities, then feed results into `/career`
- `/clifton` — CliftonStrengths analysis
- `/mentorship` — Career development and learning roadmaps

---

**Framework:** Intelligence Adjacent (IA)
**Structure:** Universal Prompt Structure v2.0
