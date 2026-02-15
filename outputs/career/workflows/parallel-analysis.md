# Parallel Job Analysis Workflow

**Purpose:** When /career-search finds multiple matching jobs (≥60%), automatically launch parallel analysis agents.

---

## Workflow Steps

### 1. Discovery Phase (Already Complete)
- Jobs discovered via hiring.cafe
- Scored against resume
- Top matches identified (≥60%)

### 2. Parallel Launch (Advisor Agent)

For each job in top matches (up to 5):

```typescript
// Launch parallel Task agents - ALL in a single message
Task(subagent_type="advisor", model="haiku", prompt="Run /career analysis for: {job_url}\n\nJob Details:\nTitle: {title}\nCompany: {company}\nScore: {score}%\n\nExecute full 5-phase workflow and save to: {output_dir}")
Task(subagent_type="advisor", model="haiku", prompt="Run /career analysis for: {job_url2}...")
Task(subagent_type="advisor", model="haiku", prompt="Run /career analysis for: {job_url3}...")
```

**CRITICAL:** All Task calls MUST be in a single message for parallel execution.

### 3. Output Structure

```
~/.claude/skills/career/output/
└── batch-{query}-{date}/
    ├── SUMMARY.md                 # Overview of all analyses
    ├── {job-1-slug}/
    │   ├── job-posting.json
    │   ├── 01-assess.md
    │   ├── 02-research.md
    │   ├── 03-prepare.md
    │   ├── 04-generate.md
    │   └── 05-deliver.md
    ├── {job-2-slug}/
    │   └── ...
    └── {job-3-slug}/
        └── ...
```

### 4. Agent Instructions

Each spawned agent receives:
- Job URL for analysis
- Pre-scored match data (for context)
- Output directory path
- Instruction to run full 5-phase /career workflow

### 5. User Experience

User runs:
```bash
/career-search penetration tester remote
```

Output:
```
Found 20 jobs, 8 match criteria

Top 3 matches:
1. 🟢 Senior Penetration Tester - 78%
2. 🟡 Security Consultant - 67%
3. 🟡 Offensive Security Engineer - 64%

Launching parallel analysis (3 agents)...
✓ Agent 1: Senior Penetration Tester
✓ Agent 2: Security Consultant
✓ Agent 3: Offensive Security Engineer

Results: ~/.claude/skills/career/output/batch-pentest-2026-01-31/
```

Each agent runs independently and saves results to its job folder.

---

## Implementation Notes

**Model Selection:** Use `model="haiku"` for cost efficiency
- Each /career analysis is straightforward execution
- No complex reasoning needed
- Haiku handles 5-phase workflow perfectly
- Cost: ~$0.25 per job vs ~$3.00 with Sonnet

**Concurrency:** Max 5 parallel agents
- Prevents overwhelming the system
- Balances speed vs resource usage
- If >5 matches, analyze top 5 first

**Error Handling:**
- If agent fails, log to job directory
- Continue with remaining analyses
- User can re-run failed jobs individually

---

## Usage from Advisor Agent

When advisor agent receives `/career-search`:

1. Run discovery script (discover-jobs.ts or discover-and-analyze.ts)
2. Parse results JSON
3. For each top match (up to 5), prepare Task prompt
4. Launch ALL Task agents in single message (parallel execution)
5. Return summary to user with output paths

**Example:**

```typescript
// After discovery returns 3 matches at 78%, 67%, 64%
// Launch all 3 in parallel:

Task(subagent_type="advisor", model="haiku", prompt=`
Execute /career analysis for this job:

URL: https://hiring.cafe/viewjob/abc123
Title: Senior Penetration Tester
Company: SecureCorp
Match Score: 78%

Run full 5-phase workflow:
1. Assess (GO/NO-GO)
2. Research company
3. Prepare interview questions
4. Generate resume/cover letter
5. Deliver final package

Save all outputs to:
~/.claude/skills/career/output/batch-pentest-2026-01-31/senior-penetration-tester/
`)

Task(subagent_type="advisor", model="haiku", prompt=`
Execute /career analysis for this job:

URL: https://hiring.cafe/viewjob/def456
Title: Security Consultant
Company: TechStartup
Match Score: 67%

...
`)

Task(subagent_type="advisor", model="haiku", prompt=`
Execute /career analysis for this job:

URL: https://hiring.cafe/viewjob/ghi789
Title: Offensive Security Engineer
Company: BigCorp
Match Score: 64%

...
`)
```

All three agents start immediately and run concurrently.
