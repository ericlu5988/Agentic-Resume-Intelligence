---
domain: career
skill: career
agent: advisor
model: sonnet
mode: multi-agent
agents: [advisor, researcher, writer]
complexity: medium
chain_position: first
---

# Career Workflow Orchestrator

## IDENTITY

**Agent:** `agents/advisor.md` (loaded automatically from METADATA `agent:` field)

**Phase-specific role:** Orchestrate the 5-phase career analysis pipeline. Detect current state, load the correct phase, enforce gates between phases, and route to the correct agent for each phase.

**Additional constraints:** This is a multi-agent workflow. Phases 2 and 4 delegate to specialized agents (researcher and writer). The orchestrator manages agent transitions.

---

## INPUT CONTRACT

**Receives:**
- Job posting text or URL (from user via `/career` command)
- Resume file path (auto-detected from `skills/career/input/` — any format: `.md`, `.pdf`, `.docx`, `.txt`)
- Output directory path: `skills/career/output/{company}-{role}-{date}/`

**Prerequisites:**
- Job posting available (text pasted or URL provided)
- Resume accessible (auto-detected or user provides path)

**Source:** `skills/career/commands/career.md` (command prompt)

---

## OBJECTIVE

**Goal:** Execute the 5-phase career analysis pipeline in order, enforcing gates between phases.

**Success criteria:**
- All 5 phases execute in order (or STOP at Phase 1 if NO-GO)
- Gate criteria verified between each phase
- 6 deliverable files produced in output directory
- User receives submission strategy at Phase 5

**Failure criteria:**
- Phase 1 returns NO-GO (score <60%) → STOP, do not proceed
- Required inputs missing and user declines to provide → STOP

---

## METHODOLOGY

**State detection:** Check which files exist in the output directory to determine current phase. This enables resume capability — if a previous run was interrupted, pick up where it left off.

**Gate enforcement:** Each phase has explicit exit criteria. Do not advance to the next phase until all criteria are met. If a gate fails, loop back to the failing step within that phase.

**Phase 1 is the hard gate.** A NO-GO decision means the opportunity isn't worth pursuing. Respect this — don't let the user override without explicitly acknowledging the gaps.

---

## EXECUTION

### Step 1: Detect Current State

**Tool:** Glob
**Pattern:** `skills/career/output/{company}-{role}-{date}/*`

Check which deliverable files exist:

```
IF match-assessment.md NOT EXISTS       → Load 01-assess.md
ELSE IF match-assessment.md shows NO-GO → STOP (do not proceed)
ELSE IF company-research.md NOT EXISTS  → Load 02-research.md
ELSE IF interview-prep.md NOT EXISTS    → Load 03-prepare.md
ELSE IF resume.md OR cover-letter.md OR job-posting.md NOT EXISTS → Load 04-generate.md
ELSE IF all 6 files exist              → Load 05-deliver.md
ELSE                                    → Workflow complete
```

**Expected output:** Current phase identified
**On failure:** Default to Phase 1 (fresh start)

### Step 2: Load Phase Prompt

**Tool:** Read
**Reference:** `skills/career/phases/0{N}-{phase}.md`

Load the phase file identified in Step 1.

**Expected output:** Phase instructions loaded, execution begins

### Step 3: Execute Phase

Follow the loaded phase prompt exactly. Each phase has its own IDENTITY, EXECUTION steps, and CHECKPOINTS.

**Agent routing per phase:**
- Phase 1 (01-assess.md): `agent: advisor` — execute directly
- Phase 2 (02-research.md): `agent: researcher` — delegate via `Task(subagent_type="researcher")`
- Phase 3 (03-prepare.md): `agent: advisor` — execute directly
- Phase 4 (04-generate.md): `agent: writer` — delegate via `Task(subagent_type="writer")`
- Phase 5 (05-deliver.md): `agent: advisor` — execute directly

**Expected output:** Phase deliverables produced

### Step 4: Verify Gate

Check that all exit criteria from the completed phase are met before advancing.

**Expected output:** Gate PASSED or gate FAILED with specific blocker

### Step 5: Show Checkpoint

Display phase completion to user:

```
PHASE {N} COMPLETE: {Phase Name}
Files: {list of output files created}
{Phase-specific metrics}
Gate: PASSED

→ Ready for Phase {N+1}: {Next Phase Name}
```

**If Phase 1 = NO-GO:**
```
PHASE 1 RESULT: NO-GO
Score: {XX}% (threshold: 60%)
Reason: {specific gaps or red flags}

→ Workflow stopped. This opportunity is not a good fit.
  Recommendation: {what to look for instead}

→ Want to close the gaps? /mentorship can create a development plan
  for the missing skills identified above.
```

### Step 6: Advance or Stop

If gate passed → return to Step 2 with next phase.
If NO-GO or final phase → stop.

---

## OUTPUT CONTRACT

**Produces:**
- Phase orchestration (no files created by workflow itself)
- All output managed by individual phases in `skills/career/output/{company}-{role}-{date}/`

**Final output (after all 5 phases):**
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

**On all phases complete:** → Workflow finished. Display final summary to user.

**On NO-GO at Phase 1:** → STOP. Display NO-GO message. Do not proceed.

**On gate failure:** → Loop back to failing step within current phase.

---

## CHECKPOINTS

**Exit criteria (ALL must be true):**
- [ ] All phases executed in order (1→2→3→4→5) or stopped at Phase 1 NO-GO
- [ ] Gate criteria verified between each phase transition
- [ ] 6 deliverable files exist in output directory (if workflow completed)
- [ ] User received checkpoint summary after each phase

**Error recovery:**
- If resume not found: Prompt user for path or paste content
- If WebSearch fails during research: Use WebFetch on known company URLs
- If phase produces incomplete output: Loop back to incomplete step, don't advance

---

## Phase Reference

| Phase | File | Agent | Gate | Output |
|-------|------|-------|------|--------|
| 1 | `01-assess.md` | advisor | GO/NO-GO decision (≥60%) | match-assessment.md |
| 2 | `02-research.md` | researcher | 10+ sources collected | company-research.md |
| 3 | `03-prepare.md` | advisor | 5 priority areas + 10-12 Q&A | interview-prep.md |
| 4 | `04-generate.md` | writer | All 6 deliverables created | job-posting.md, resume.md, cover-letter.md |
| 5 | `05-deliver.md` | advisor | Submission strategy provided | (verbal guidance) |

---

## Critical Rules

1. **NEVER skip phases** — Execute in order 1→2→3→4→5
2. **STOP on NO-GO** — If Phase 1 score <60%, STOP workflow entirely
3. **ALWAYS show checkpoint** — User must see phase completion summary
4. **Files stay in output directory** — Never move between folders
5. **Each phase is self-contained** — Load prompt, execute, verify gate, show checkpoint

---

**Framework:** Intelligence Adjacent (IA)
**Structure:** Universal Prompt Structure v2.0
