# Job Analysis — Definition of Done

**Verification checklist to ensure job analysis meets quality standards.**

---

## Phase Gate Summary

| Phase | Gate Question | Pass Criteria |
|-------|---------------|---------------|
| ASSESS | Is this opportunity worth pursuing? | Match score calculated, GO/NO-GO decided |
| RESEARCH | Do we have enough information? | 10+ sources, all categories covered |
| PREPARE | Can user walk into interview prepared? | 5 priority areas, 10-12 Q&A |
| GENERATE | Are deliverables ready for submission? | All 6 files created, ethics followed |
| DELIVER | Does user have everything needed? | Strategy provided, next steps clear |

---

## Pre-Execution Checklist

- [ ] Job posting provided by user
- [ ] Resume available in `skills/career/input/` (any format)
- [ ] User understands GO/NO-GO may stop workflow early

---

## Phase 1: ASSESS Verification

- [ ] Job posting parsed with structured requirements
- [ ] Resume loaded and analyzed
- [ ] Match score calculated with breakdown:
  - [ ] Required skills (40%)
  - [ ] Experience level (25%)
  - [ ] Nice-to-have skills (20%)
  - [ ] Industry match (15%)
- [ ] Red flags checked (certifications, experience, tech stack, location)
- [ ] GO/NO-GO decision made with justification
- [ ] If NO-GO: Workflow stopped, user informed why, `/mentorship` offered
- [ ] `match-assessment.md` written to output directory

---

## Phase 2: RESEARCH Verification

- [ ] 10+ sources collected with URLs
- [ ] All 6 research categories covered:
  - [ ] Company basics
  - [ ] Leadership
  - [ ] Security/Compliance posture
  - [ ] Culture/Sentiment
  - [ ] Tech stack
  - [ ] Social media intel
- [ ] Sources cited inline per section
- [ ] `company-research.md` written to output directory
- [ ] Key insights identified for interview prep

---

## Phase 3: PREPARE Verification

- [ ] 5 priority areas identified, each with:
  - [ ] Why it matters (evidence from research)
  - [ ] Their need (from job posting)
  - [ ] Your position (from resume)
  - [ ] Talking points (2-3 per area)
- [ ] 10-12 interview questions with answers:
  - [ ] 3-4 technical questions
  - [ ] 3-4 behavioral questions (STAR format)
  - [ ] 3-4 scenario questions
- [ ] 5-7 strategic questions to ask (not generic)
- [ ] Quick reference card completed
- [ ] `interview-prep.md` written to output directory

---

## Phase 4: GENERATE Verification

- [ ] `job-posting.md` created with working application URL
- [ ] `match-assessment.md` finalized
- [ ] `company-research.md` finalized
- [ ] `interview-prep.md` finalized
- [ ] `resume.md` created:
  - [ ] 1-2 pages maximum
  - [ ] Reverse chronological order (verified)
  - [ ] Tailored professional summary
  - [ ] No fabricated content
  - [ ] No emojis, AI cliches, or decorative elements
- [ ] `cover-letter.md` created:
  - [ ] Under 350 words
  - [ ] 4 paragraphs (hook, value, why company, CTA)
  - [ ] Company-specific references (not generic)
- [ ] All 6 files in output directory
- [ ] All filenames lowercase-hyphen
- [ ] Resume ethics followed (no fabrication)

---

## Phase 5: DELIVER Verification

- [ ] Deliverables summary presented to user
- [ ] Submission timing guidance provided:
  - [ ] Optimal day/time for company timezone
  - [ ] Application method identified
- [ ] Follow-up timeline established:
  - [ ] Week 1: LinkedIn connection template
  - [ ] Week 2: Follow-up email template
  - [ ] Week 4: Final check-in guidance
- [ ] Networking opportunities identified
- [ ] User has clear numbered next steps
- [ ] Application URL confirmed and highlighted

---

## Output Structure Verification

```
skills/career/output/{company}-{role}-{date}/
├── job-posting.md           Original job description + application URL
├── match-assessment.md      GO/NO-GO analysis
├── company-research.md      Company intelligence (10+ sources)
├── interview-prep.md        Priority areas, Q&A, questions to ask
├── resume.md                Tailored resume (reverse chronological)
└── cover-letter.md          Cover letter (<350 words)
```

- [ ] Directory follows naming convention: `{company}-{role}-{date}` (lowercase-hyphen)
- [ ] All 6 files present
- [ ] All filenames lowercase-hyphen
- [ ] Files use consistent formatting
- [ ] No extra files beyond the 6 specified

---

## Quality Standards

### Research Quality
- [ ] 10+ unique sources (not variations of same article)
- [ ] Sources from different categories
- [ ] URLs are valid and accessible

### Resume Quality
- [ ] No fabricated experience or skills
- [ ] Keywords match job posting (only if actually possessed)
- [ ] Reverse chronological order verified
- [ ] No emojis, AI cliches, or decorative symbols
- [ ] Professional business tone

### Cover Letter Quality
- [ ] References specific company research
- [ ] Connects experience to stated needs
- [ ] Not a form letter (company-specific)
- [ ] Under 350 words, 4 paragraphs
- [ ] Ends at signature — no extra content

### Interview Prep Quality
- [ ] Questions based on research findings
- [ ] Answers include specific examples from resume
- [ ] Questions to ask are strategic, not generic
- [ ] All content tied to this specific role

---

## Error Conditions

| Condition | Required Action |
|-----------|-----------------|
| Resume not found | Ask user for path before proceeding |
| Match score <60% | Stop workflow, explain why, offer `/mentorship` |
| Resume gap detected | Stop and ask user before proceeding |
| <10 research sources | Note limitation, proceed if critical categories covered |
| Grok unavailable | Use WebSearch for social media instead |

---

**Version:** 2.0
**Last Updated:** 2026-02-08
**Structure:** Universal Prompt Structure v1.0
