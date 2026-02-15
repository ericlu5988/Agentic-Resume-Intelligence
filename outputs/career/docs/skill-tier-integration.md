# Career Skill - Model Tier Integration

**How the career skill routes between model tiers for cost-optimal execution.**

---

## Overview

The career skill uses the three-tier orchestration engine to balance cost and quality. Most career analysis benefits from assumption challenging and logic validation, making Tier 2a (Grok 3 Mini) the optimal choice.

---

## Routing Decision Tree

| Query Type | Tier | Cost | Example |
|------------|------|------|---------|
| Career advice and guidance | Tier 1 (Free) | $0.00 | "What's the market for X role?" |
| Job posting GO/NO-GO analysis | Tier 2a (Grok 3 Mini) | $0.80/1M | "Should I apply for this role?" |
| Complex fit validation | Tier 2a (Grok 3 Mini) | $0.80/1M | Role fit with assumption testing |
| Tailored deliverable generation | Tier 2a (Grok 3 Mini) | $0.80/1M | Resume and cover letter |

---

## Why Tier 2a for Career Analysis?

**Primary Benefits:**
- **Assumption challenging** - Validates role fit before recommending
- **Logic validation** - Ensures GO/NO-GO scoring is sound
- **Gap detection** - Identifies missing qualifications or red flags
- **Cost savings** - 67% cheaper than Sonnet ($0.80 vs $2.40 per 1M tokens)

**Use Cases:**
- Evaluating whether you should apply
- Scoring match percentage
- Identifying skill gaps
- Challenging unstated assumptions in job descriptions

---

## How It Works

1. **User invokes `/career`** with a job posting or career question
2. **Base Claude's tier selector** analyzes the request complexity
3. **Guidance queries** route to Tier 1 (free)
   - "What should I look for in a job offer?"
   - "How do I negotiate salary?"
4. **Job analysis queries** route to Tier 2a for assumption testing
   - "Should I apply for this role?"
   - "What's my match score for this position?"
5. **GO/NO-GO score** challenges assumptions before recommending
   - Tests implicit requirements
   - Validates experience alignment
   - Identifies show-stoppers

---

## Cost Model

| Phase | Primary Model | Estimated Cost | Notes |
|-------|--------------|----------------|-------|
| 1: Assess (GO/NO-GO) | Tier 2a | ~$0.30 | Assumption testing critical |
| 2: Research (Company) | Tier 2a | ~$0.20 | Pattern detection in market data |
| 3: Prepare (Interview) | Tier 1/2a Hybrid | ~$0.20 | Guidance (Tier 1) + scenario prep (Tier 2a) |
| 4: Generate (Deliverables) | Tier 2a | ~$0.30 | Resume/cover letter tailoring |
| 5: Deliver (Strategy) | Tier 1 | ~$0.10 | Tactical advice |
| **Total (Full Workflow)** | Mixed | **~$1.10** | Compare to Sonnet-only: ~$3.30 (67% savings) |

**Note:** Costs are estimates based on average job posting analysis. Complex roles or extensive research may increase costs.

---

## When to Override Tier Selection

**Force Tier 1 (Free):**
- General career advice
- Resume formatting questions
- Industry overview requests

**Force Tier 3 (Sonnet):**
- Extremely complex role negotiations
- High-stakes opportunity evaluation (C-suite, critical career pivot)
- Multi-variable trade-off analysis

**Force Tier 2a (Grok 3 Mini):**
- Standard job application analysis (default)
- GO/NO-GO assessment
- Resume/cover letter generation

---

## Integration with Career Workflow

### Phase 1: Assess (GO/NO-GO)
**Model:** Tier 2a (Grok 3 Mini)
**Why:** Assumption testing prevents false positives in match scoring

### Phase 2: Research (Company Intelligence)
**Model:** Tier 2a (Grok 3 Mini) or Tier 1 (Free)
**Why:** Pattern detection in market data, fallback to free for basic research

### Phase 3: Prepare (Interview Prep)
**Model:** Hybrid (Tier 1 + Tier 2a)
**Why:** General advice uses Tier 1, scenario prep uses Tier 2a

### Phase 4: Generate (Deliverables)
**Model:** Tier 2a (Grok 3 Mini)
**Why:** Tailoring requires assumption testing (e.g., "What skills should I emphasize?")

### Phase 5: Deliver (Strategy)
**Model:** Tier 1 (Free)
**Why:** Tactical advice and timing don't require complex reasoning

---

## Monitoring and Optimization

**Track these metrics:**
- Cost per job analysis
- GO/NO-GO accuracy (false positive rate)
- User satisfaction with deliverable quality
- Tier override frequency

**Optimization opportunities:**
- If Tier 1 handles assumptions well, route more there
- If Tier 2a quality drops, escalate to Tier 3
- Monitor cost vs quality trade-offs per phase

---

**Last Updated:** 2026-02-01
**Version:** 1.0
