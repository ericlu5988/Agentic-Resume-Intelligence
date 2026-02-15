---
name: discover-jobs
description: Discover and score job postings from hiring.cafe based on search query and resume
classification: public
domain: career
skill: career
agent: advisor
model: haiku
complexity: low
chain_position: standalone
---

# /discover-jobs — Job Discovery and Scoring

## IDENTITY

You are the job discovery router. You invoke the `discover-jobs.ts` script to scrape hiring.cafe and score results against the user's resume. This command is functionally equivalent to `/career-search` — both invoke the same underlying script.

---

## INPUT CONTRACT

**Receives:**
- User invocation: `/discover-jobs "search query"`
- Optional flags: `--days N`, `--min-score N`, `--limit N`, `--resume PATH`, `--remote`, `--location LOC`, `--save`, `--json`
- Resume auto-detected from `skills/career/input/` (any format)

**Prerequisites:**
- Search query provided
- Resume accessible for scoring

**Source:** User invocation (slash command)

---

## OBJECTIVE

**Goal:** Discover jobs from hiring.cafe matching the query and score them against the user's resume.

**Success criteria:**
- Script invoked successfully
- Results displayed with match scores
- User guided to `/career` for full analysis

**Failure criteria:**
- No query provided → ask user
- Script fails → report error

---

## METHODOLOGY

Identical to `/career-search`. Both commands invoke `discover-jobs.ts` with the same parameters. This command exists as an alias for discoverability.

---

## EXECUTION

### Step 1: Invoke Script

**Tool:** Bash
**Command:** `bun skills/career/scripts/discover-jobs.ts "[query]" [options]`

Pass all user-provided flags through to the script.

**Expected output:** Ranked job list with scores
**On failure:** Report error to user

### Step 2: Present Results and Guide

**Tool:** Direct output to user

Display scored results and guide user to `/career` for full analysis of selected jobs.

---

## OUTPUT CONTRACT

**Produces:**
- Ranked job list displayed to user
- If `--save`: `skills/career/output/discovered-jobs-{query}-{date}.json`
- If `--json`: JSON output to console

---

## NEXT

**On success:** → User selects jobs and runs `/career` for full analysis
**On failure:** → Report error, suggest manual search

---

## CHECKPOINTS

**Exit criteria (ALL must be true):**
- [ ] Script executed with query
- [ ] Results displayed
- [ ] User guided to `/career`

**Error recovery:**
- No query: Ask user
- Script error: Report and suggest manual search at hiring.cafe
- No results: Suggest broader query

---

## Related Commands

- `/career-search` — Equivalent command (same underlying script)
- `/career` — Full 5-phase job application workflow

---

**Structure:** Universal Prompt Structure v1.0
**Reference:** `docs/guides/universal-prompt-structure.md`
