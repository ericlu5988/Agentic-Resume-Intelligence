# Job Discovery Workflow

**Complete technical documentation for the /career-search command and job discovery scraper.**

---

## Overview

The job discovery system automatically finds and scores job opportunities from hiring.cafe, eliminating the manual search process. It uses browser automation (Playwright) to scrape job listings, then scores them against your resume using the same GO/NO-GO methodology from Phase 1 (Assess).

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      /career-search Command                      │
│                                                                   │
│  User Query: "cybersecurity engineer remote"                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    discover-jobs.ts (CLI)                        │
│                                                                   │
│  • Parse query and options                                       │
│  • Initialize scraper and scorer                                 │
│  • Orchestrate workflow                                          │
└────────────────┬──────────────────────────────┬─────────────────┘
                 │                              │
                 ▼                              ▼
┌────────────────────────────┐    ┌───────────────────────────────┐
│   HiringCafeScraper        │    │      JobScorer                │
│                            │    │                               │
│  Step 1: Search Page       │    │  • Load resume                │
│  • Build search URL        │    │  • Extract skills             │
│  • Collect job links       │    │  • Score each job             │
│  • Found: 40 links         │    │  • Filter by threshold        │
│                            │    │                               │
│  Step 2: Detail Pages      │    │  Scoring Weights:             │
│  • Navigate to each job    │    │  - Skills Match: 40%          │
│  • Extract full details    │    │  - Experience: 25%            │
│  • Concurrency: 3          │    │  - Bonus: 20%                 │
│  • Delay: 3s ±30% jitter   │    │  - Location: 15%              │
└────────────┬───────────────┘    └───────────┬───────────────────┘
             │                                │
             ▼                                │
┌─────────────────────────────────────────────┴───────────────────┐
│                      Job Postings (10)                           │
│                                                                   │
│  [{ id, title, company, location, description, url, ... }]       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Scored & Ranked Results                       │
│                                                                   │
│  1. 🟠 Senior Security Engineer - 42%                           │
│     Company: TechCorp | Remote                                   │
│     Matched: python, aws, kubernetes                             │
│     URL: https://hiring.cafe/viewjob/abc123                     │
│                                                                   │
│  2. 🟠 Penetration Tester - 40%                                 │
│     ...                                                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### 1. discover-jobs.ts (CLI Orchestrator)

**Location:** `skills/career/scripts/discover-jobs.ts`

**Purpose:** Command-line interface that coordinates scraping and scoring.

**Flow:**
```typescript
1. Parse command-line arguments
   ├─ Query: "cybersecurity engineer remote"
   ├─ Options: --days 14 --min-score 35 --limit 10
   └─ Resume path (auto-detected)

2. Initialize scraper
   └─ new HiringCafeScraper({ delay: 3000, timeout: 30000 })

3. Execute search
   └─ scraper.search(query)

4. Initialize scorer
   └─ new JobScorer(resumePath)

5. Score and filter jobs
   ├─ scorer.scoreJobs(jobs)
   └─ Filter by minScore threshold

6. Display results
   ├─ Human-readable: Colored output with scores
   └─ JSON: Machine-readable format

7. Optional: Save to output folder
   └─ If --save flag present
```

**Options:**
- `--days N` - Past N days (default: 14)
- `--min-score N` - Minimum score 0-100 (default: 35)
- `--limit N` - Max jobs to process (default: 10)
- `--resume PATH` - Resume file path
- `--remote` - Only remote jobs
- `--location LOC` - Specific location
- `--save` - Save results as JSON
- `--json` - JSON output format

---

### 2. HiringCafeScraper (Browser Automation)

**Location:** `skills/career/scripts/scrapers/hiring-cafe-scraper.ts`

**Purpose:** Scrapes job listings from hiring.cafe using Playwright.

**Two-Step Strategy:**

#### Step 1: Search Page - Collect Links
```typescript
// Build URL with encoded search state
const searchState = {
  searchQuery: "cybersecurity engineer remote",
  dateFetchedPastNDays: 14,
  locations: [{ /* US with flexible regions */ }]
};

// Navigate to search page
await page.goto(`https://hiring.cafe/?searchState=${encoded}`);

// Wait for React to hydrate (5 seconds)
await page.waitForTimeout(5000);

// Extract all /viewjob/ links
const links = await page.evaluate(() => {
  return Array.from(
    document.querySelectorAll('a[href*="/viewjob/"]')
  ).map(link => link.href);
});

// Result: ~40 job links
```

#### Step 2: Detail Pages - Extract Jobs
```typescript
// Process links in batches (concurrency: 3)
for (const link of links.slice(0, limit)) {
  // Navigate to job detail page
  const page = await navigate(link);

  // Extract structured data
  const job = await page.evaluate(() => {
    const title = document.querySelector('h1, h2')?.textContent;
    const description = document.querySelector('article')?.textContent;
    const company = /* extracted from description or element */;
    const location = /* check for "Remote" in title */;
    // ... more extraction

    return { title, company, location, description, ... };
  });

  await page.close();

  // Delay before next (3s ±30% jitter)
  await sleep(randomDelay());
}
```

**Rate Limiting:**
- **Concurrency:** 3 parallel requests maximum
- **Batch delay:** 3000ms with ±30% jitter (2100-3900ms)
- **Total time:** ~30-45 seconds for 10 jobs

**Browser Configuration:**
- Headless Chromium via Playwright
- User-Agent: Chrome 120 on Windows
- Viewport: 1920x1080
- Locale: en-US
- Timezone: America/New_York

---

### 3. JobScorer (Resume Matching)

**Location:** `skills/career/scripts/scrapers/job-scorer.ts`

**Purpose:** Scores jobs against resume using GO/NO-GO methodology.

#### Resume Parsing
```typescript
// Extract skills from resume
const skills = [];
const patterns = [
  /(?:Skills?|Technologies?|Tools?):\s*([^\n]+)/gi,
  /(?:Proficient in|Experience with):\s*([^\n]+)/gi
];

for (const pattern of patterns) {
  const matches = resume.matchAll(pattern);
  for (const match of matches) {
    const skillsText = match[1];
    const extracted = skillsText
      .split(/[,;•|]/)
      .map(s => s.trim().toLowerCase());
    skills.push(...extracted);
  }
}

// Extract years of experience
const yearsMatch = resume.match(/(\d+)\+?\s*years?/i);
const experienceYears = yearsMatch ? parseInt(yearsMatch[1]) : 0;
```

#### Scoring Algorithm
```typescript
function scoreJob(job: JobPosting): JobMatchScore {
  let score = 0;

  // 1. Skills Match (40%)
  const jobSkills = extractJobSkills(job.description);
  const matchedSkills = jobSkills.filter(js =>
    resumeSkills.some(rs => skillsMatch(rs, js))
  );
  const skillScore = (matchedSkills.length / jobSkills.length) * 40;
  score += skillScore;

  // 2. Experience Level (25%)
  const experienceMatch = matchExperience(job, resume);
  score += experienceMatch ? 25 : 0;

  // 3. Location Match (15%)
  const locationMatch = matchLocation(job, resume);
  score += locationMatch ? 15 : 0;

  // 4. Bonus Points (20%)
  let bonus = 0;
  if (job.salary?.min >= 120000) bonus += 5;
  if (job.locationTypes?.includes('remote')) bonus += 5;
  if (job.description.includes('equity')) bonus += 2;
  // ... more bonuses
  score += Math.min(20, bonus);

  return {
    score: Math.round(score),
    matchedSkills,
    missingSkills,
    experienceMatch,
    locationMatch,
    recommendation: getRecommendation(score)
  };
}
```

**Skill Matching:**
```typescript
// Handles variations
skillsMatch('javascript', 'js') → true
skillsMatch('kubernetes', 'k8s') → true
skillsMatch('penetration testing', 'pentest') → true

// Common variations map
const variations = {
  'javascript': ['js', 'ecmascript', 'node', 'nodejs'],
  'typescript': ['ts'],
  'python': ['py'],
  'kubernetes': ['k8s'],
  'penetration testing': ['pentest', 'pentesting'],
  // ...
};
```

**Experience Matching:**
```typescript
// Extract required years from job description
const patterns = [
  /(\d+)\+?\s*years?/i,
  /minimum\s+of\s+(\d+)\s*years?/i,
  /at\s+least\s+(\d+)\s*years?/i
];

// Check seniority level
if (desc.includes('senior') && resume.years >= 5) return true;
if (desc.includes('lead') && resume.years >= 7) return true;
if (desc.includes('director') && resume.years >= 10) return true;
```

**Recommendation Thresholds:**
- **≥75%:** 🟢 Strong fit (GO)
- **60-74%:** 🟡 Good fit (CONDITIONAL GO)
- **45-59%:** 🟠 Conditional fit
- **<45%:** 🔴 Poor fit (NO-GO)

---

### 4. Base Framework (Reusable Components)

**Location:** `skills/career/scripts/scrapers/base/`

#### BrowserManager (Singleton)
```typescript
// Reuses browser across all scrapers
class BrowserManager {
  private browser: Browser | null = null;
  private contexts: Map<string, BrowserContext> = new Map();

  async getBrowser(): Promise<Browser> {
    if (!this.browser) {
      this.browser = await chromium.launch({ headless: true });
    }
    return this.browser;
  }

  async getContext(name: string): Promise<BrowserContext> {
    if (!this.contexts.has(name)) {
      const browser = await this.getBrowser();
      const context = await browser.newContext({
        userAgent: 'Mozilla/5.0 ...',
        viewport: { width: 1920, height: 1080 },
        // ... anti-detection config
      });
      this.contexts.set(name, context);
    }
    return this.contexts.get(name)!;
  }
}
```

#### BaseJobScraper (Abstract Class)
```typescript
abstract class BaseJobScraper {
  abstract readonly source: string;
  abstract search(query: JobSearchQuery): Promise<JobPosting[]>;

  // Reusable utilities
  protected async navigate(url: string): Promise<Page> { }
  protected async extractText(page: Page, selector: string): Promise<string> { }
  protected async retry<R>(fn: () => Promise<R>): Promise<R> { }
  protected async concurrentMap<I, R>(items: I[], fn): Promise<R[]> { }
  protected sleep(ms: number): Promise<void> { }
}
```

**Benefits:**
- Single browser instance (memory efficient)
- Consistent configuration
- Automatic retry logic
- Concurrent processing with delays
- Easy to extend for new job boards

---

## Data Flow

### Input to Output Pipeline

```
┌────────────────────────────────────────────────────────────────┐
│ INPUT: User Query                                              │
│                                                                │
│  "cybersecurity engineer remote"                              │
│  --days 14 --min-score 35 --limit 10                          │
└──────────────────────────┬─────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────────┐
│ STEP 1: Build Search URL                                       │
│                                                                │
│  searchState = {                                               │
│    searchQuery: "cybersecurity engineer remote",              │
│    dateFetchedPastNDays: 14,                                  │
│    locations: [{ US + flexible regions }]                     │
│  }                                                             │
│  url = `https://hiring.cafe/?searchState=${encoded}`          │
└──────────────────────────┬─────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────────┐
│ STEP 2: Scrape Search Page                                     │
│                                                                │
│  Navigate → Wait 5s → Extract links                           │
│  Result: ['viewjob/abc', 'viewjob/def', ...]  (40 links)     │
└──────────────────────────┬─────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────────┐
│ STEP 3: Extract Job Details (Concurrent)                       │
│                                                                │
│  Batch 1 (3 jobs): [─────] 3s delay                           │
│  Batch 2 (3 jobs): [─────] 3s delay                           │
│  Batch 3 (3 jobs): [─────] 3s delay                           │
│  Batch 4 (1 job):  [─]                                         │
│                                                                │
│  Each job extracts:                                            │
│  {                                                             │
│    id: "abc123",                                               │
│    title: "Senior Security Engineer",                         │
│    company: "TechCorp",                                        │
│    location: "Remote",                                         │
│    description: "...",                                         │
│    url: "https://hiring.cafe/viewjob/abc123",                │
│    datePosted: "2026-01-28T00:00:00Z",                        │
│    source: "hiring-cafe",                                      │
│    scraped_at: "2026-01-29T20:00:00Z"                         │
│  }                                                             │
└──────────────────────────┬─────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────────┐
│ STEP 4: Score Against Resume                                   │
│                                                                │
│  For each job:                                                 │
│    1. Extract job skills from description                      │
│    2. Match against resume skills                              │
│    3. Calculate experience match                               │
│    4. Calculate location match                                 │
│    5. Add bonus points                                         │
│    6. Generate total score (0-100)                             │
│                                                                │
│  Result:                                                       │
│  {                                                             │
│    jobId: "abc123",                                            │
│    score: 42,                                                  │
│    matchedSkills: ['python', 'aws', 'kubernetes'],           │
│    missingSkills: ['splunk', 'terraform'],                    │
│    experienceMatch: true,                                      │
│    locationMatch: true,                                        │
│    recommendation: 'conditional-fit'                           │
│  }                                                             │
└──────────────────────────┬─────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────────┐
│ STEP 5: Filter & Sort                                          │
│                                                                │
│  • Filter: score >= 35                                         │
│  • Sort: descending by score                                   │
│  • Limit: top 10                                               │
└──────────────────────────┬─────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────────┐
│ OUTPUT: Ranked Results                                         │
│                                                                │
│  1. 🟠 Senior Security Engineer - 42%                         │
│     TechCorp | Remote                                          │
│     Matched: python, aws, kubernetes                           │
│     Missing: splunk, terraform                                 │
│     https://hiring.cafe/viewjob/abc123                        │
│                                                                │
│  2. 🟠 Penetration Tester - 40%                               │
│     ...                                                        │
└────────────────────────────────────────────────────────────────┘
```

---

## Performance Metrics

### Timing Breakdown

```
Total Time: ~30-45 seconds (for 10 jobs)

┌─────────────────────────┬──────────┬────────────┐
│ Step                    │ Time     │ Details    │
├─────────────────────────┼──────────┼────────────┤
│ 1. Search page          │ 5-8s     │ Navigate + │
│                         │          │ React load │
├─────────────────────────┼──────────┼────────────┤
│ 2. Collect links        │ <1s      │ Evaluate   │
├─────────────────────────┼──────────┼────────────┤
│ 3. Extract job details  │ 20-35s   │ Concurrent │
│    • 10 jobs            │          │ batches:   │
│    • 3 concurrent       │          │ 4 batches  │
│    • 3s delays          │          │ × 3s each  │
├─────────────────────────┼──────────┼────────────┤
│ 4. Score jobs           │ <1s      │ Fast       │
├─────────────────────────┼──────────┼────────────┤
│ 5. Display results      │ <1s      │ Format     │
└─────────────────────────┴──────────┴────────────┘
```

### Concurrency Example

```
Time →

Batch 1:  [Job 1] [Job 2] [Job 3]
          └─2s──┘ └─2s──┘ └─2s──┘
                                   [Delay 3s]

Batch 2:                              [Job 4] [Job 5] [Job 6]
                                      └─2s──┘ └─2s──┘ └─2s──┘
                                                               [Delay 3s]

Batch 3:                                                          [Job 7] [Job 8] [Job 9]
                                                                  └─2s──┘ └─2s──┘ └─2s──┘
                                                                                           [Delay 3s]

Batch 4:                                                                                      [Job 10]
                                                                                              └─2s───┘

Total: ~20-25 seconds (vs 50-60s if sequential)
```

---

## Error Handling

### Scraper Errors

```typescript
// Automatic retry with exponential backoff
try {
  return await fn();
} catch (error) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    const delay = baseDelay * attempt;
    await sleep(delay);
    try {
      return await fn();
    } catch (e) {
      if (attempt === maxRetries) throw e;
    }
  }
}
```

**Handled Scenarios:**
- Network timeouts → Retry 3x
- Page load failures → Retry 3x
- Element not found → Return null, skip job
- Invalid data → Skip job, continue
- Rate limiting → Exponential backoff

### Scorer Errors

```typescript
// Graceful degradation
try {
  const score = scoreJob(job);
} catch (error) {
  console.warn(`Failed to score job ${job.id}:`, error);
  // Return minimal score instead of crashing
  return {
    score: 0,
    recommendation: 'poor-fit',
    error: error.message
  };
}
```

---

## Extensibility

### Adding New Job Boards

**Example: Adding Indeed Scraper**

```typescript
// 1. Create scraper class
export class IndeedScraper extends BaseJobScraper {
  readonly source = 'indeed';

  async search(query: JobSearchQuery): Promise<JobPosting[]> {
    // Indeed-specific implementation
    const url = this.buildIndeedUrl(query);
    const page = await this.navigate(url);
    const jobs = await this.extractIndeedJobs(page);
    return jobs;
  }

  private buildIndeedUrl(query: JobSearchQuery): string {
    // Indeed URL format
  }

  private async extractIndeedJobs(page: Page): Promise<JobPosting[]> {
    // Indeed DOM structure
  }
}
```

```typescript
// 2. Update discover-jobs.ts
const scrapers = [
  new HiringCafeScraper(),
  new IndeedScraper(),  // Add here
];

const allJobs = await Promise.all(
  scrapers.map(s => s.search(query))
);

const merged = deduplicateJobs(allJobs.flat());
```

**Benefits of Base Framework:**
- Automatic retry logic
- Browser management handled
- Concurrent processing built-in
- Consistent error handling
- Only implement `search()` method

---

## Security & Privacy

### Data Handling
- **No storage:** Jobs not persisted unless `--save` flag used
- **Local processing:** All scoring done locally
- **No tracking:** No analytics or telemetry
- **Resume privacy:** Resume never leaves local machine

### Rate Limiting Ethics
- Conservative delays (3s between batches)
- Random jitter to avoid detection patterns
- Respects site resources
- Limited to 10-20 jobs per search

### User-Agent Transparency
- Identifies as Chrome browser (standard UA)
- No attempt to hide automation
- Could be blocked if detected

---

## Future Enhancements

### Near Term
- [ ] Cache results (1 hour TTL)
- [ ] Support multiple job boards simultaneously
- [ ] Better company name extraction
- [ ] Salary parsing improvements
- [ ] Export to CSV/JSON

### Long Term
- [ ] Add Indeed scraper (via API or ts-jobspy)
- [ ] Add LinkedIn scraper (if API access granted)
- [ ] Integrate Adzuna API (free tier)
- [ ] NLP-based resume parsing
- [ ] Machine learning for better scoring
- [ ] Cron job mode for daily discoveries
- [ ] Email notifications for new matches

---

**Version:** 1.0
**Created:** 2026-01-29
**Last Updated:** 2026-01-29
