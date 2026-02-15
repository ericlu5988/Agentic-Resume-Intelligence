# career Status

**Last Updated:** 2026-02-08
**Session:** universal-prompt-structure-standardization
**Readiness:** Ready (Standardized)

---

## Session Changes (Reverse Chronological)

### 2026-02-08 — Universal Prompt Structure Standardization (COMPLETE)

**Major Update:**
- All phase files rewritten to universal prompt structure (METADATA, IDENTITY, INPUT/OUTPUT CONTRACT, METHODOLOGY, EXECUTION, NEXT, CHECKPOINTS)
- All command files rewritten to universal prompt structure
- SKILL.md updated with chain map
- README.md, VERIFY.md cleaned of stale references
- career-advancement.md archived (outdated, replaced by phases/)
- Fixed: 5 vs 6 deliverable count inconsistency
- Fixed: CAPS filenames → lowercase-hyphen throughout
- Fixed: TodoWrite references → removed (deprecated)
- Fixed: Resume path now accepts any format in `skills/career/input/`
- Added: NO-GO routing to `/mentorship` for skill development
- Added: Broader resume format support (.md, .pdf, .docx, .txt)

### 2026-01-29 — Job Discovery Implementation (COMPLETE)

**Feature Added:**
- Job discovery scraper with hiring.cafe integration
- `/career-search` command for automated job searching
- Resume-based scoring engine (GO/NO-GO methodology)

**Changes:**
- New command: `/career-search <query>`
- New CLI tool: `scripts/discover-jobs.ts`
- New scraper framework: `scripts/scrapers/`

### 2026-01-14 — Skill Review (VALIDATED)

- Status upgraded from Development to Ready
- All phases and workflows verified complete

---

## Readiness Assessment

| Component | Status | Notes |
|-----------|--------|-------|
| SKILL.md | Ready | v2.0, chain map added |
| Phases (00-05) | Ready | All follow universal prompt structure |
| Commands (3) | Ready | career, career-search, discover-jobs |
| Scripts | Ready | discover-jobs.ts + scraper framework |
| Templates | Ready | resume-template.md, cover-letter-template.md |
| Documentation | Ready | Updated for v2.0 |

---

## Workflow Summary

**Mode 1: Manual Analysis (`/career`)**
- User provides job posting
- 5-phase workflow: ASSESS → RESEARCH → PREPARE → GENERATE → DELIVER
- Output: 6 deliverable files in `output/{company}-{role}-{date}/`

**Mode 2: Automated Discovery (`/career-search`)**
- User provides search query
- Script scrapes hiring.cafe, scores against resume
- Output: Ranked job list with match percentages
- User then runs `/career` on selected jobs

---

**Skill:** career
**Classification:** public
**Version:** 2.0
