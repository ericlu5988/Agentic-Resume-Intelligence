# Job Analysis Skill

**Analyze job opportunities with GO/NO-GO assessment, company research, and tailored application materials.**

---

## The Problem

Applying to jobs is time-consuming. Most applications fail because:
- Poor fit with requirements (wasted effort)
- Generic materials (no differentiation)
- Lack of company research (unprepared for interviews)
- No follow-up strategy (applications disappear)

## The Solution

This skill provides a **structured 5-phase workflow** that:
1. **Assesses fit first** — Don't waste time on poor-fit roles
2. **Gathers intelligence** — Comprehensive company research with citations
3. **Prepares for interviews** — Priority areas and Q&A based on research
4. **Creates tailored materials** — Resume and cover letter for THIS role
5. **Provides strategy** — Submission timing and follow-up plan

---

## Quick Start

### Option 1: Discover Jobs
```bash
# Search and score jobs from hiring.cafe
/career-search "cybersecurity engineer remote"
/career-search "penetration tester"
```

### Option 2: Analyze Specific Job
```bash
# Full 5-phase analysis
/career [paste job description or URL]
```

---

## Prerequisites

**Resume:** Place in `skills/career/input/` (any format: `.md`, `.pdf`, `.docx`, `.txt`).

---

## What You Get

6 deliverable files in `skills/career/output/{company}-{role}-{date}/`:

| Deliverable | Description |
|-------------|-------------|
| `job-posting.md` | Original job description + application URL |
| `match-assessment.md` | GO/NO-GO score with strengths and gaps |
| `company-research.md` | Company intel with 10+ cited sources |
| `interview-prep.md` | Priority areas, Q&A, questions to ask |
| `resume.md` | Tailored resume for this role |
| `cover-letter.md` | Company-specific cover letter |

---

## The 5-Phase Workflow

```
ASSESS (GO/NO-GO) → RESEARCH → PREPARE → GENERATE → DELIVER
```

| Phase | What Happens |
|-------|--------------|
| **ASSESS** | Calculate match score, make GO/NO-GO decision |
| **RESEARCH** | Gather company intelligence (WebSearch + Grok) |
| **PREPARE** | Develop 5 priority areas, 10-12 interview Q&A |
| **GENERATE** | Create tailored resume and cover letter |
| **DELIVER** | Provide submission timing and follow-up plan |

### GO/NO-GO Gate

Phase 1 determines if this role is worth pursuing:

| Score | Decision | What Happens |
|-------|----------|--------------|
| >=75% | **GO** | Strong fit — full workflow proceeds |
| 60-74% | **CONDITIONAL GO** | Gaps exist but proceed |
| <60% | **NO-GO** | Stop — offer `/mentorship` for skill development |

**Red Flags (Auto NO-GO):**
- Required certification you don't have
- 5+ years below experience requirement
- Zero tech stack overlap
- Unwanted relocation required

---

## Resume Ethics

This skill will **never** fabricate experience.

**Allowed:** Emphasizing relevant experience, using keywords (you actually have), removing irrelevant positions, tailoring professional summary.

**Forbidden:** Changing job titles, adding skills you don't have, inflating achievements, guessing at undocumented experience.

---

## Job Discovery

Search and score jobs from hiring.cafe automatically.

```bash
/career-search "cybersecurity director remote"
```

1. Scrapes hiring.cafe with your query
2. Scores against your resume using GO/NO-GO methodology
3. Returns ranked results with match percentages
4. You pick top matches and run `/career` for full analysis

---

## Related Skills

- `/career-search` — Discover and rank job opportunities
- `/mentorship` — Learning roadmaps and career development
- `/clifton` — CliftonStrengths analysis

---

**Version:** 2.0
**Agent:** advisor
**Classification:** public
**Structure:** Universal Prompt Structure v1.0
