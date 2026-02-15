# Career Job Scrapers

**Self-contained job scraping framework for the /career skill**

## Overview

This directory contains a browser-based job scraping framework built specifically for the career skill. It includes:

- **Base framework** (`base/`) - Browser management, retry logic, and common scraping utilities
- **Job scrapers** - Platform-specific implementations (currently hiring.cafe)
- **Job scorer** - Resume matching and GO/NO-GO scoring engine
- **CLI tools** - discover-jobs.ts for end-to-end job discovery

## Structure

```
scrapers/
├── base/
│   ├── types.ts              # TypeScript interfaces for jobs, queries, scores
│   ├── browser-manager.ts    # Singleton Playwright browser manager
│   └── base-job-scraper.ts   # Abstract base class for scrapers
│
├── hiring-cafe-scraper.ts    # hiring.cafe implementation
├── job-scorer.ts             # Resume matching and scoring
└── README.md                 # This file
```

## Usage

### discover-jobs.ts - Job Discovery CLI

```bash
# Basic usage
bun skills/career/scripts/discover-jobs.ts "cybersecurity engineer remote"

# With options
bun skills/career/scripts/discover-jobs.ts "security architect" \
  --days 7 \
  --min-score 60 \
  --limit 10 \
  --remote \
  --save

# With custom resume
bun skills/career/scripts/discover-jobs.ts "pentest" \
  --resume /path/to/resume.md \
  --min-score 70
```

### Options

- `--days N` - Search jobs from past N days (default: 14)
- `--min-score N` - Minimum match score 0-100 (default: 60)
- `--limit N` - Max jobs to return (default: 20)
- `--resume PATH` - Path to resume file (auto-detects from input/ if not specified)
- `--remote` - Only remote jobs
- `--location LOC` - Specific location
- `--save` - Save results to output folder as JSON
- `--json` - Output as JSON instead of human-readable

## How It Works

### 1. Scraping Strategy

hiring.cafe uses a two-step process:

1. **Search page** - Load search results and collect job links
2. **Detail pages** - Navigate to each job page to extract full details

The scraper uses conservative concurrency (3 parallel requests) and random jitter delays (±30%) to avoid detection and be respectful of the site.

### 2. Scoring Methodology

Jobs are scored using the same GO/NO-GO criteria from Phase 1 (Assess):

| Category | Weight | Criteria |
|----------|--------|----------|
| Required Skills Match | 40% | Keywords found in job description |
| Experience Level | 25% | Years and seniority alignment |
| Bonus Points | 20% | Salary, remote work, benefits |
| Location Match | 15% | Remote/hybrid/onsite preference |

**Score Ranges:**
- ≥75% = 🟢 Strong fit (GO)
- 60-74% = 🟡 Good fit (CONDITIONAL GO)
- 45-59% = 🟠 Conditional fit (gaps exist)
- <45% = 🔴 Poor fit (NO-GO)

### 3. Resume Parsing

The job scorer automatically extracts:
- Skills (from "Skills:", "Technologies:", "Tools:" sections)
- Years of experience (from "X years" patterns)
- Remote preference (from resume content)
- Location preferences

Supports `.md`, `.pdf`, and `.docx` formats.

## Adding New Job Boards

To add a new job board scraper:

1. Create `{board}-scraper.ts` extending `BaseJobScraper`
2. Implement `search(query: JobSearchQuery): Promise<JobPosting[]>`
3. Use base class utilities:
   - `navigate(url)` - Navigate with retry
   - `extractText(page, selector)` - Extract text content
   - `retry(fn, context)` - Retry with exponential backoff
   - `concurrentMap(items, fn)` - Process items in batches
4. Return array of `JobPosting` objects

Example:

```typescript
export class MyJobBoardScraper extends BaseJobScraper {
  readonly source = 'my-job-board';

  async search(query: JobSearchQuery): Promise<JobPosting[]> {
    const url = this.buildUrl(query);
    const page = await this.navigate(url);

    const jobs = await this.extractJobs(page);
    await page.close();

    return jobs;
  }

  private async extractJobs(page: Page): Promise<JobPosting[]> {
    // Implementation here
  }
}
```

## Browser Management

The framework uses a singleton BrowserManager that:
- Reuses browser instance across all scrapers
- Creates separate contexts per scraper source
- Handles cleanup automatically
- Configures anti-detection headers

## Performance

**Typical Performance:**
- Search + 20 job details: ~60-90 seconds
- Concurrency: 3 parallel detail page loads
- Delay between batches: 3 seconds ±30% jitter
- Retry attempts: 3 per operation

## Error Handling

The framework includes:
- Automatic retry with exponential backoff
- Graceful degradation (skips failed jobs)
- Detailed logging with source prefix
- Browser cleanup on error

## Dependencies

- `playwright` - Browser automation
- `bun` - TypeScript runtime

No external API keys or authentication required.

## Known Limitations

1. **hiring.cafe only** - Currently single source
2. **Company extraction** - May extract incorrect company names from job descriptions
3. **Rate limiting** - Conservative delays mean slower scraping
4. **No caching** - Re-scrapes on each run
5. **Resume parsing** - Simple keyword extraction, not NLP-based

## Future Enhancements

- [ ] Add Indeed scraper (via ts-jobspy or official API if available)
- [ ] Add LinkedIn scraper (via official API if partnership approved)
- [ ] Add Adzuna API integration (free tier)
- [ ] Implement caching layer (Redis or file-based)
- [ ] Improve company name extraction
- [ ] Add NLP-based resume parsing
- [ ] Support bulk job discovery (cron job mode)

## Related Documentation

- **Career skill**: `skills/career/SKILL.md`
- **Job posting APIs research**: `skills/career/docs/job-posting-apis-research-2026.md`
- **Tool catalog**: `docs/catalogs/tool-catalog.md`

---

**Version:** 1.0
**Created:** 2026-01-29
**Framework:** Intelligence Adjacent (IA)
