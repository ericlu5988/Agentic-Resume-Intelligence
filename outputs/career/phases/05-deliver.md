---
domain: career
skill: career
agent: advisor
model: sonnet
mode: single-agent
complexity: low
chain_position: last
---

# Phase 5: DELIVER (Submission Strategy)

## IDENTITY

**Agent:** `agents/advisor.md` (loaded automatically from METADATA `agent:` field)

**Phase-specific role:** Provide submission strategy, follow-up timeline, and networking guidance. Ensure the user leaves with clear, specific next actions.

**Additional constraints:** Provide actionable templates, not vague advice. Calculate specific submission timing. Every recommendation should be date-specific and actionable.

---

## INPUT CONTRACT

**Receives:**
- All 6 deliverable files from Phase 4 in `skills/career/output/{company}-{role}-{date}/`
- Match score and decision from Phase 1
- Company research and key insights from Phase 2
- Output directory path

**Prerequisites:**
- All 6 deliverable files exist and pass validation
- Phase 4 quality checks passed

**Source:** `skills/career/phases/04-generate.md`

---

## OBJECTIVE

**Goal:** Provide the user with submission strategy, follow-up timeline, networking guidance, and a clear summary of everything created.

**Success criteria:**
- Deliverables summary presented to user
- Optimal submission timing calculated
- Follow-up timeline with templates provided
- Networking opportunities identified
- User has clear, numbered next steps

**Failure criteria:**
- User identifies issues with deliverables → return to Phase 4 to fix
- Application URL missing from job-posting.md → flag prominently

---

## METHODOLOGY

Phase 5 is the handoff. The user should walk away knowing exactly what was created, where to find it, when to submit, and what to do after submitting. Everything should be actionable with specific dates and templates — not "follow up later."

**Timing matters more than people think.** Tuesday-Thursday submissions at 7-9 AM in the company's timezone get more attention than Friday afternoon or weekend submissions. Calculate the specific optimal window for this company.

**Follow-up cadence prevents ghosting.** Most applicants give up after submitting. A structured follow-up plan (LinkedIn connection → email follow-up → final check-in) significantly increases response rates.

---

## EXECUTION

### Step 1: Deliverables Summary

**Tool:** Read (re-read output directory listing)

Present a clear summary of what was created and where to find it:

```
Deliverables Created

Location: skills/career/output/{company}-{role}-{date}/

| File                  | Purpose                       | Status |
|-----------------------|-------------------------------|--------|
| job-posting.md        | Job description + apply URL   | Ready  |
| match-assessment.md   | GO/NO-GO analysis             | Ready  |
| company-research.md   | Company intelligence          | Ready  |
| interview-prep.md     | Priority areas and Q&A        | Ready  |
| resume.md             | Tailored resume               | Ready  |
| cover-letter.md       | Cover letter                  | Ready  |
```

**Expected output:** Summary table with all 6 files confirmed ready
**On failure:** If any file missing or incomplete, flag and return to Phase 4

### Step 2: Submission Strategy

**Tool:** Direct analysis

Calculate optimal submission timing:

- **Best days:** Tuesday, Wednesday, Thursday
- **Best time:** 7-9 AM in company's timezone
- **Avoid:** Friday afternoon, weekends, holidays
- **Reason:** Early-week morning submissions appear at top of inbox when hiring managers have full attention

For this specific role:
- Determine company timezone (from research)
- Calculate specific recommended submission window
- Note any urgency (posting close date, "applying immediately" language)

Determine application method:
- Primary method from job posting (website, email, referral)
- Application URL from `job-posting.md`
- Any special instructions from the posting

**Expected output:** Specific submission timing recommendation and method

### Step 3: Follow-Up Timeline

**Tool:** Direct analysis

Create a follow-up plan with templates:

**Week 1 (Days 3-5): LinkedIn Connection**
Template:
> Hi [Name], I recently applied for the [Role] position at [Company]. I'm excited about [specific from research] and would welcome the opportunity to discuss how my experience in [relevant area] could contribute to your team. — [Your Name]

**Week 2 (Day 10-14): Follow-Up Email**
Subject: Following Up: [Role] Application — [Your Name]
Template:
> Dear [Hiring Manager/Team],
>
> I wanted to follow up on my application for the [Role] position submitted on [Date]. I remain interested in this opportunity and believe my experience in [relevant area] aligns well with your needs.
>
> I would welcome the chance to discuss how I could contribute to [specific initiative from research].
>
> Best regards,
> [Your Name]

**Week 4 (Day 25-28): Final Check-In**
If no response: Application likely not progressing. Continue job search.

**Expected output:** Timeline with filled-in templates

### Step 4: Networking Opportunities

**Tool:** Direct analysis (from company research)

Identify:
- 1st degree connections at company (if any mentioned)
- 2nd degree connections (inferred from LinkedIn if discussed in research)
- Potential internal referral paths
- Informational interview opportunities
- Hiring manager name (if found in research)

**Expected output:** Networking strategy with specific targets

### Step 5: Present Final Summary

**Tool:** Direct output to user

Display comprehensive final summary:

```
Job Analysis Complete

Role: [Job Title] at [Company]
Match Score: [XX]% — [GO/CONDITIONAL GO]
Deliverables: 6 files ready in output/{company}-{role}-{date}/

Next Steps:
1. Review deliverables — read all 6 files, make personal adjustments
2. Submit application — [Optimal day/time], via [method]
3. LinkedIn outreach — connect with [hiring manager] by Day 3-5
4. Follow up — email if no response by Day 10-14
5. Interview prep — review interview-prep.md before any calls

Key Strengths to Emphasize:
1. [Top strength]
2. [Top strength]
3. [Top strength]

Gaps to Address Proactively:
1. [Gap — how to frame]

Application URL: [URL from job-posting.md]
```

---

## OUTPUT CONTRACT

**Produces:**
- Verbal delivery to user (no additional files created by this phase)
- All deliverables from Phase 4 remain in `skills/career/output/{company}-{role}-{date}/`

**Format:** Structured summary displayed to user with numbered next steps

---

## NEXT

**On success:** → Workflow complete. No further phases.

**On user requesting changes:** → Return to Phase 4 to edit specific deliverables.

**On user requesting additional analysis:** → Start new workflow for different role.

---

## CHECKPOINTS

**Exit criteria (ALL must be true):**
- [ ] All 6 deliverables presented to user
- [ ] Submission timing guidance provided (specific day/time)
- [ ] Follow-up timeline with templates provided
- [ ] Networking opportunities identified (or noted as none found)
- [ ] User has clear numbered next steps
- [ ] Application URL confirmed and highlighted

**Error recovery:**
- If user wants changes to deliverables: Return to Phase 4, edit specific file
- If company timezone unknown: Use user's timezone, note assumption
- If no networking opportunities found: Focus on direct application strategy
- If application URL missing: Flag prominently, ask user to add manually

---

## Post-Workflow

After Phase 5, the user may:
- Request adjustments to any deliverable
- Ask for additional interview prep
- Request analysis of a different role (start new `/career` workflow)
- Provide feedback on the workflow

---

**Framework:** Intelligence Adjacent (IA)
**Structure:** Universal Prompt Structure v2.0
