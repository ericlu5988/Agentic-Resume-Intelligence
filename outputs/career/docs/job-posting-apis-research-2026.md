# Job Posting APIs and Scraping Solutions - Research Report 2026

**Research Date:** 2026-01-16
**Purpose:** Evaluate available APIs and scraping solutions for programmatic job posting retrieval
**Target Implementation:** TypeScript-based career analysis tool

---

## Executive Summary

The job posting API landscape in 2026 is characterized by **restricted official APIs** requiring partnership agreements, **paid third-party aggregators** offering multi-board access, and **legally questionable scraping solutions**. Most major job boards (Indeed, LinkedIn) have shifted to partnership-only models with strict usage policies and spending requirements. Free, open access to job posting data is increasingly rare.

**Key Finding:** For a practical TypeScript implementation in 2026, the most viable approaches are:
1. **Third-party aggregator APIs** (Adzuna, JobDataAPI) - Paid but legitimate
2. **ATS APIs** (Greenhouse, Lever) - Access to company job postings
3. **Google Cloud Talent Solution** - Enterprise ML-powered search
4. **Scraping libraries** (ts-jobspy) - Legal risks, high maintenance

---

## 1. Major Job Board APIs

### 1.1 Indeed

**Status:** Partnership-only with strict spending requirements
**API Types:**
- **Job Sync API** (GraphQL) - For ATS partners only
- **Sponsored Jobs API** - Requires minimum spending

**Key Details:**
- **Authentication:** Partner credentials via Partner Console
- **Rate Limits:** Configurable per partner, throttles high-volume requests
- **Cost Requirements:** As of February 1, 2026, requires €3 (EU) or $3 (USD) in sponsored job spending per API call in previous 3 months
- **Access:** 6-week integration process for approved partners
- **Data Quality:** High - direct access to Indeed's job database

**Practical Assessment:**
❌ **Not viable** for independent developers or small projects due to partnership requirements and mandatory spending thresholds.

**Sources:**
- [Job Sync API guide | Indeed Partner Docs](https://docs.indeed.com/job-sync-api/job-sync-api-guide)
- [Indeed's API](https://docs.indeed.com/)
- [Sponsored Jobs API usage policy | Indeed Partner Docs](https://docs.indeed.com/sponsored-jobs-api/sponsored-jobs-api-usage-policy)

### 1.2 LinkedIn

**Status:** Closed - Not accepting new partnerships
**API Types:**
- **Job Posting API** - Restricted to existing partners
- **Apply Connect** - Request-based access

**Key Details:**
- **Authentication:** LinkedIn Partner Program approval required
- **Access Process:** Must apply through LinkedIn Relationship Manager or Business Development contact
- **Restrictions:** API agreement with data restrictions, compliance review required
- **Current Status:** "Currently not accepting new partnerships for LinkedIn's Job Posting API"

**Practical Assessment:**
❌ **Not viable** for new developers - partnership program closed to new applicants.

**Sources:**
- [Job Posting API Overview - LinkedIn | Microsoft Learn](https://learn.microsoft.com/en-us/linkedin/talent/job-postings/api/overview?view=li-lts-2025-10)
- [Guide to LinkedIn API and Alternatives](https://scrapfly.io/blog/posts/guide-to-linkedin-api-and-alternatives)
- [LinkedIn Developer Solutions](https://developer.linkedin.com/)

### 1.3 ZipRecruiter, Dice, Monster

**Status:** No public API documentation found
**Access:** Appears to be partner/employer-only

**Key Details:**
- Third-party libraries exist (JobApis on GitHub, Jobs Common for PHP)
- No official developer portals or public API documentation
- Primarily focused on employer job posting and candidate management tools

**Practical Assessment:**
❌ **Not viable** - Would require direct business contact for API access, likely employer-focused only.

**Sources:**
- [Accessing Job Board APIs in PHP - Karl Hughes](https://www.karllhughes.com/posts/access-job-apis-php)
- [JobApis · GitHub](https://github.com/jobapis)
- [25 Best Job Search Sites in 2026 | FlexJobs](https://www.flexjobs.com/blog/post/best-job-search-sites)

---

## 2. Applicant Tracking System (ATS) APIs

### 2.1 Greenhouse

**Status:** Open API with authentication
**API Type:** Harvest API (RESTful)

**Key Details:**
- **Authentication:** API key with endpoint-specific permissions
- **Access Requirements:** "Can manage ALL organization's API Credentials" permission
- **Rate Limits:** Not specified in search results
- **Cost:** Free for GET endpoints (public job board data)
- **Integrations:** 500+ pre-built integrations
- **Data Access:** Job postings from companies using Greenhouse ATS

**Practical Assessment:**
✅ **Viable** for accessing job postings from companies that use Greenhouse. No authentication required for public job board GET endpoints.

**Sources:**
- [Greenhouse API overview – Greenhouse Support](https://support.greenhouse.io/hc/en-us/articles/10568627186203-Greenhouse-API-overview)
- [Harvest API | Greenhouse](https://developers.greenhouse.io/harvest.html)
- [Job Board API | Greenhouse](https://developers.greenhouse.io/job-board.html)

### 2.2 Lever

**Status:** Open API with 300+ integrations
**Platform:** LeverTRM suite (ATS + CRM)

**Key Details:**
- API access available
- Fewer integrations than Greenhouse (300 vs 500+)
- Focuses on combining ATS and CRM capabilities

**Practical Assessment:**
✅ **Viable** for accessing job postings from Lever-using companies.

**Sources:**
- [Ultimate Guide – The Best ATS Integration of 2025](https://www.mokahr.io/articles/en/the-best-ats-integration)
- [How to Build a Job Board That Connects to Greenhouse, Lever, and 60+ ATS Platforms](https://unified.to/blog/how_to_build_a_job_board_that_connects_to_greenhouse_lever_and_60_ats_platforms_with_a_unified_api)

### 2.3 SmartRecruiters

**Status:** Open platform with marketplace
**Focus:** Enterprise Talent Acquisition Suite

**Key Details:**
- Extensive third-party integration marketplace
- API available for partners
- Developer-friendly platform

**Practical Assessment:**
✅ **Viable** for accessing job postings from SmartRecruiters-using companies.

**Sources:**
- [Ultimate Guide – The Best ATS Integration of 2025](https://www.mokahr.io/articles/en/the-best-ats-integration)
- [Job Board API](https://developers.smartrecruiters.com/docs/partners-job-board-api)

---

## 3. Third-Party Job Aggregator APIs

### 3.1 Adzuna

**Status:** Public API with authentication
**Coverage:** 16+ countries, millions of job listings

**Key Details:**
- **Authentication:** API Key (HTTPS)
- **Access:** Free developer account on Adzuna Developer Website
- **Data Sources:** Aggregates from employer websites, job boards, recruitment networks
- **Features:** Historical data, full job details, standardized job titles/skills
- **Platforms:** Available via RapidAPI and direct API

**Practical Assessment:**
✅ **Viable** - Appears to be the most accessible legitimate job aggregator API in 2026.

**Sources:**
- [Adzuna API](https://developer.adzuna.com/)
- [Adzuna API — Free Public API | Public APIs Directory](https://publicapis.io/adzuna-api)
- [Adzuna](https://rapidapi.com/baskarm28/api/adzuna)

### 3.2 The Muse

**Status:** Public API available
**Focus:** Job listings + company profiles + career advice

**Key Details:**
- **Authentication:** API key (X-Muse-Api-Key header)
- **Endpoints:** Jobs and companies
- **Data Format:** JSON
- **Rate Limits:** Not publicly documented
- **Cost:** Unknown - requires API key signup for details

**Practical Assessment:**
⚠️ **Potentially viable** - Smaller dataset, unclear pricing/limits. Good for supplementary data.

**Sources:**
- [The Muse - Developers API](https://www.themuse.com/developers/api/v2)
- [The Muse API — Free Public API | Public APIs Directory](https://publicapis.io/the-muse-api)

### 3.3 JobDataAPI.com

**Status:** Commercial API with free testing tier

**Key Details:**
- **Free Tier:** Hourly rate limit, handful of requests
- **Paid Tier:** Unlimited access, no hourly rate limits
- **Data Coverage:** 50,000+ companies
- **Updates:** Daily with thousands of new jobs
- **Authentication:** API key from dashboard

**Practical Assessment:**
✅ **Viable** for production use with paid subscription. Free tier suitable for testing only.

**Sources:**
- [Pricing plans | jobdataapi.com](https://jobdataapi.com/accounts/pricing/)
- [Simple Job Data API | jobdataapi.com](https://jobdataapi.com/)

### 3.4 Coresignal Jobs API

**Status:** Large-scale commercial API

**Key Details:**
- **Data Points:** 65+ fields per job posting
- **Advanced Fields:** Department, management level, seniority, remote acceptance, shift schedule
- **Salary Data:** Structured with min/max values, currency, pay type
- **Company Data:** Comprehensive company information

**Practical Assessment:**
✅ **Viable** for enterprise applications requiring comprehensive data.

**Sources:**
- [Jobs API: Access a Large-Scale Jobs Database](https://coresignal.com/solutions/jobs-data-api/)

---

## 4. Google Cloud Solutions

### 4.1 Google Cloud Talent Solution (CTS)

**Status:** Enterprise ML-powered job search API

**Key Details:**
- **Technology:** Machine Learning for job matching
- **Features:**
  - Interprets vague job descriptions and search queries
  - Confidence scoring by occupation families
  - Automatic detection of titles, seniority, industry
  - Commute search by time and transit mode
- **Access:** Enable via Google Cloud Console
- **Use Case:** Talent technology providers and enterprises
- **Documentation:** REST API available

**Practical Assessment:**
✅ **Viable** for enterprise applications with ML requirements. Requires Google Cloud account and billing.

**Sources:**
- [Cloud Talent Solution Job Matching APIs | Google Cloud](https://cloud.google.com/solutions/talent-solution)
- [APIs and References | Job Search | Google Cloud Documentation](https://cloud.google.com/talent-solution/job-search/docs/apis)

### 4.2 Third-Party Google Jobs APIs

**Services:** SerpApi, SearchAPI, Scrapingdog, OpenWeb Ninja

**Key Details:**
- Extract job listing data from Google's job search results
- Commercial services with API access
- Not official Google APIs - scraping-based

**Practical Assessment:**
⚠️ **Use with caution** - Third-party scraping services, potential TOS violations.

**Sources:**
- [Google Jobs API - SerpApi](https://serpapi.com/google-jobs-api)
- [Google Jobs API](https://www.searchapi.io/google-jobs)
- [Google Jobs API – Extract Job Listings Data | Scrapingdog](https://www.scrapingdog.com/google-jobs-api/)

---

## 5. TypeScript/Node.js Scraping Libraries

### 5.1 ts-jobspy (Recommended)

**Status:** Active - Published 7 days ago (as of search date)
**Version:** 2.0.2

**Key Details:**
- **Platforms:** LinkedIn, Indeed, Glassdoor, ZipRecruiter, Google, Bayt, Naukri, BDJobs
- **Currently Working:** LinkedIn and Indeed only (others "coming soon")
- **Technology:** TypeScript port of python-jobspy
- **Output:** Structured job data as array of objects
- **Rate Limiting:**
  - Indeed: Minimal rate limiting (best performer)
  - LinkedIn: Rate limits around 10th page
  - All boards: ~1000 jobs max per search
- **Concurrency:** Scrapes multiple boards simultaneously

**Practical Assessment:**
⚠️ **Use with caution** - Violates job board TOS. Active maintenance is good, but legal risks remain.

**Sources:**
- [ts-jobspy - npm Package Security Analysis - Socket](https://socket.dev/npm/package/ts-jobspy)
- [GitHub - speedyapply/JobSpy](https://github.com/speedyapply/JobSpy)

### 5.2 linkedin-jobs-scraper

**Status:** Maintained
**Technology:** Puppeteer + RxJS

**Key Details:**
- **Mode:** Headless browser scraping
- **Authentication:** Anonymous mode (no login required)
- **Data Fields:** jobId, title, company, companyLink, companyImgLink, place, date, link, applyLink, description, descriptionHTML, insights
- **Filters:** Relevance, time, job type, experience level, remote/hybrid/onsite
- **Language:** TypeScript
- **Warning:** LinkedIn TOS explicitly prohibits data extraction

**Practical Assessment:**
❌ **High legal risk** - Direct TOS violation, potential for account bans and legal action from LinkedIn.

**Sources:**
- [GitHub - llorenspujol/linkedin-jobs-scraper](https://github.com/llorenspujol/linkedin-jobs-scraper)
- [linkedin-jobs-scraper - npm](https://www.npmjs.com/package/linkedin-jobs-scraper)

### 5.3 indeed-scraper

**Status:** ⚠️ Outdated - Last published 4 years ago
**Version:** 3.1.4

**Practical Assessment:**
❌ **Not recommended** - Unmaintained, likely broken due to Indeed website changes.

**Sources:**
- [GitHub - rynobax/indeed-scraper](https://github.com/rynobax/indeed-scraper)
- [indeed-scraper - npm](https://www.npmjs.com/package/indeed-scraper)

### 5.4 Commercial Scraping APIs

**Services Compared (2026):**
- **Bright Data:** 100% success rate, 6.36s avg response time
- **Scrapingdog:** 100% success rate, 14.47s avg response time
- **ScraperAPI, ZenRows, ScrapingBee:** Various performance metrics
- **Apify:** Templates in Python, JavaScript, TypeScript

**Practical Assessment:**
✅ **Viable** if legal compliance is handled by service provider. Check each service's TOS and legal indemnification.

**Sources:**
- [5 Best Indeed Scrapers To Test Out in 2026](https://www.scrapingdog.com/blog/best-indeed-scrapers/)
- [💼 Indeed Scraper · Apify](https://apify.com/misceres/indeed-scraper)

---

## 6. Legal and Practical Considerations

### 6.1 Legal Landscape in 2026

The legal environment for web scraping has evolved significantly:

**Key Legal Developments:**
- **Meta v. Bright Data (2024):** Scraping in violation of TOS can be breach of contract, BUT scraping public data while logged out may not be bound by TOS you never agreed to
- **hiQ Labs v. LinkedIn:** Scraping publicly available data doesn't violate Computer Fraud and Abuse Act (CFAA) if no security measures are bypassed
- **2026 Shift:** New lawsuits involving AI training and technical circumvention are "redrawing the lines of what is permissible"

**Platform-Specific Restrictions:**
- **LinkedIn:** TOS explicitly prohibits data extraction, history of legal action against scrapers
- **Indeed:** TOS prohibits scraping
- **Glassdoor:** TOS prohibits scraping, have taken legal action

**Sources:**
- [Is Web Scraping Legal? Laws, Ethics, and Best Practices](https://research.aimultiple.com/is-web-scraping-legal/)
- [Job Board Scraping: The Complete 2025 Guide | Job Boardly](https://www.jobboardly.com/blog/job-board-scraping-complete-guide-2025)
- [Is web scraping legal? Yes, if you know the rules.](https://blog.apify.com/is-web-scraping-legal/)

### 6.2 Best Practices for Legal Compliance

**If Pursuing Scraping Approach:**

1. **Respect TOS:** Avoid sites that explicitly forbid automated access
2. **Follow robots.txt:** Indicates website owner's preferences
3. **Logged-out scraping only:** Scrape publicly available data without login
4. **Rate limiting:** Implement delays to avoid overwhelming servers
5. **User-Agent transparency:** Identify your scraper honestly
6. **No credential bypass:** Never circumvent authentication or paywalls

**Safer Alternatives:**
- Use official APIs where available
- Partner with platforms for legitimate access
- Use third-party aggregators that handle compliance
- Focus on ATS APIs (Greenhouse, Lever) for public job data

**Sources:**
- [Web Scraping for Job Postings: Best Practices and Ethical Guide](https://www.propellum.com/blog/web-scraping-for-job-postings-best-practices-and-ethical-guide/)
- [Ethical & Compliant Web Data Benchmark in 2026](https://research.aimultiple.com/web-scraping-ethics/)

### 6.3 Rate Limits and Costs

**Free Tier Options:**
- **Adzuna:** Free developer account (limits not publicly specified)
- **The Muse:** API key required, limits not public
- **Greenhouse:** Free for public job board data (GET endpoints)
- **JobDataAPI:** Free testing with hourly limits

**Paid Tiers:**
- **Indeed Sponsored Jobs API:** Minimum $3/€3 spending per API call requirement
- **JobDataAPI:** Unlimited monthly subscription (price not public)
- **Commercial scrapers:** Vary by provider (Bright Data, Scrapingdog, etc.)

**Rate Limit Patterns:**
- **Scraping-based:** LinkedIn ~10 pages, all boards ~1000 jobs max per search
- **Official APIs:** Configured per partner (Indeed), or unspecified
- **Aggregators:** Varies by service tier

**Sources:**
- [Pricing plans | jobdataapi.com](https://jobdataapi.com/accounts/pricing/)
- [Job Sync API guide | Indeed Partner Docs](https://docs.indeed.com/job-sync-api/job-sync-api-guide)

---

## 7. Data Quality and Structure

### 7.1 Standard Schema (Schema.org JobPosting)

**Core Fields:**
- `title` - Job title
- `description` - Detailed job description (responsibilities, qualifications)
- `datePosted` - Posting date
- `employmentType` - Full-time, part-time, contract, freelance, internship
- `jobLocation` - Geographical location with nested address details
- `hiringOrganization` - Company information
- `baseSalary` - Structured salary data (see below)

**Advanced Fields:**
- `educationRequirements` - Required education level
- `experienceRequirements` - Required experience
- `jobBenefits` - Benefits offered
- `incentiveCompensation` - Bonuses, stock options
- `industry` - Industry classification
- `seniority` - Job level
- `validThrough` - Application deadline
- `applicantLocationRequirements` - Geographic restrictions
- `jobLocationType` - Remote, hybrid, onsite

**Sources:**
- [JobPosting - Schema.org Type](https://schema.org/JobPosting)
- [Job Posting Schema: Structuring Job Data | Medium](https://akshaybhopani.medium.com/job-posting-schema-structuring-job-data-for-enhanced-accessibility-and-efficiency-e7fd472a4199)

### 7.2 Salary Structure

**Schema.org Format:**
```json
{
  "baseSalary": {
    "@type": "MonetaryAmount",
    "currency": "USD",
    "value": {
      "@type": "QuantitativeValue",
      "minValue": 80000,
      "maxValue": 120000,
      "unitText": "YEAR"
    }
  }
}
```

**Advanced APIs (65+ data points):**
- Structured salary with min/max values
- Currency specification
- Pay type (annual, hourly, etc.)
- Department
- Management level
- Seniority
- Remote work acceptance
- Shift schedule
- Company information

**Sources:**
- [Jobs API: Access a Large-Scale Jobs Database](https://coresignal.com/solutions/jobs-data-api/)
- [Learn About Job Posting Schema Markup | Google Search Central](https://developers.google.com/search/docs/appearance/structured-data/job-posting)

### 7.3 Data Completeness

**Typical Completeness Issues:**
- **Salary:** Often omitted or shown as range/estimate
- **Remote status:** Inconsistently specified
- **Application deadlines:** Rarely included
- **Experience requirements:** May be in description text, not structured
- **Benefits:** Usually in unstructured description text

**Best Data Quality:**
1. **ATS APIs** - Most structured, company-controlled data
2. **Paid aggregators** - Standardized, enhanced with ML
3. **Scraping** - Raw, inconsistent, requires heavy parsing

---

## 8. Recommendations for TypeScript Implementation

### 8.1 Production-Ready Approach (Legal, Reliable)

**Recommended Stack:**

1. **Primary:** Adzuna API
   - Free developer tier for testing
   - Multi-country coverage
   - Legitimate, legal access

2. **Secondary:** Greenhouse/Lever/SmartRecruiters Job Board APIs
   - Free access to public job data
   - High-quality structured data
   - No authentication needed for GET endpoints

3. **Enterprise (if budget allows):** Google Cloud Talent Solution
   - ML-powered matching
   - Advanced features
   - Scalable infrastructure

4. **Fallback/Supplementary:** JobDataAPI or Coresignal
   - Paid tiers for unlimited access
   - Comprehensive data fields

**Implementation Pattern:**
```typescript
import axios from 'axios';

interface JobPosting {
  id: string;
  title: string;
  company: string;
  location: string;
  description: string;
  employmentType: string;
  salary?: {
    min: number;
    max: number;
    currency: string;
    period: 'YEAR' | 'HOUR';
  };
  datePosted: string;
  url: string;
}

class JobAggregator {
  private adzunaApiKey: string;

  async searchJobs(query: string, location: string): Promise<JobPosting[]> {
    // Primary: Adzuna API
    const adzunaJobs = await this.fetchFromAdzuna(query, location);

    // Secondary: ATS APIs (Greenhouse, Lever)
    const atsJobs = await this.fetchFromATS(query);

    // Merge and deduplicate
    return this.mergeResults([...adzunaJobs, ...atsJobs]);
  }

  private async fetchFromAdzuna(query: string, location: string): Promise<JobPosting[]> {
    // Implementation using Adzuna API
  }

  private async fetchFromATS(query: string): Promise<JobPosting[]> {
    // Implementation for Greenhouse/Lever public APIs
  }

  private mergeResults(jobs: JobPosting[]): JobPosting[] {
    // Deduplication logic
  }
}
```

### 8.2 Development/Testing Approach (Higher Risk)

**For Development Only:**

1. **ts-jobspy** for rapid prototyping
   - Active maintenance
   - Concurrent multi-board scraping
   - Understanding: TOS violations, may break at any time

2. **Commercial scraping APIs** (Bright Data, Scrapingdog)
   - If they provide legal indemnification
   - Check their TOS carefully
   - Higher cost than aggregator APIs

**NOT Recommended:**
- ❌ linkedin-jobs-scraper (direct TOS violation)
- ❌ indeed-scraper (outdated, unmaintained)
- ❌ Building custom scrapers (maintenance burden, legal risk)

### 8.3 Decision Matrix

| Approach | Cost | Legal Risk | Data Quality | Maintenance | Recommended Use |
|----------|------|------------|--------------|-------------|-----------------|
| Adzuna API | Free/Low | ✅ None | ⭐⭐⭐⭐ | ✅ Low | **Production** |
| ATS APIs (Greenhouse) | Free | ✅ None | ⭐⭐⭐⭐⭐ | ✅ Low | **Production** |
| Google Cloud Talent | $$$ | ✅ None | ⭐⭐⭐⭐⭐ | ⭐⭐ Medium | Enterprise |
| JobDataAPI / Coresignal | $$ | ✅ None | ⭐⭐⭐⭐ | ✅ Low | Production |
| ts-jobspy | Free | ⚠️ High | ⭐⭐⭐ | ⚠️ High | Dev/Testing Only |
| Commercial Scrapers | $$$ | ⚠️ Medium | ⭐⭐⭐⭐ | ⭐⭐ Medium | If legally vetted |
| linkedin-jobs-scraper | Free | ❌ Very High | ⭐⭐⭐ | ⚠️ High | **Avoid** |
| Custom Scrapers | Free | ❌ Very High | ⭐⭐ | ❌ Very High | **Avoid** |

---

## 9. Key Takeaways

### What Changed in 2026

1. **Major boards closed APIs:** Indeed and LinkedIn now require partnerships and/or spending requirements
2. **Legal landscape evolved:** Meta v. Bright Data, AI training lawsuits changing precedents
3. **Aggregators matured:** Adzuna, JobDataAPI, Coresignal offer legitimate alternatives
4. **ATS APIs stable:** Greenhouse, Lever, SmartRecruiters continue offering public access
5. **Scraping libraries active:** ts-jobspy is maintained, but linkedin-jobs-scraper and indeed-scraper are outdated

### Critical Success Factors

**For Production Systems:**
- ✅ Use legitimate APIs (Adzuna, ATS APIs, paid aggregators)
- ✅ Implement proper error handling and rate limiting
- ✅ Monitor for API changes and deprecations
- ✅ Have fallback data sources
- ✅ Cache aggressively to minimize API calls

**For Legal Compliance:**
- ✅ Review TOS for every data source
- ✅ Stay logged out when scraping public data
- ✅ Respect robots.txt
- ✅ Implement rate limiting
- ✅ Consider legal review for commercial applications

**For Data Quality:**
- ✅ Use Schema.org JobPosting standard for internal data model
- ✅ Normalize data from multiple sources
- ✅ Handle missing fields gracefully (especially salary)
- ✅ Implement deduplication across sources
- ✅ Validate and sanitize all external data

### Recommended Implementation Path

**Phase 1 - MVP:**
1. Implement Adzuna API integration
2. Add Greenhouse public job board API
3. Build Schema.org-compliant data model
4. Create basic deduplication

**Phase 2 - Scale:**
1. Add Lever and SmartRecruiters APIs
2. Implement caching layer (Redis)
3. Add JobDataAPI or Coresignal for broader coverage
4. Enhance deduplication algorithm

**Phase 3 - Enterprise (Optional):**
1. Integrate Google Cloud Talent Solution
2. Add ML-powered job matching
3. Implement advanced search features
4. Consider commercial scraping APIs with legal vetting

---

## Sources

### Major Job Boards
- [Job Sync API guide | Indeed Partner Docs](https://docs.indeed.com/job-sync-api/job-sync-api-guide)
- [Indeed's API](https://docs.indeed.com/)
- [Sponsored Jobs API usage policy | Indeed Partner Docs](https://docs.indeed.com/sponsored-jobs-api/sponsored-jobs-api-usage-policy)
- [Job Posting API Overview - LinkedIn | Microsoft Learn](https://learn.microsoft.com/en-us/linkedin/talent/job-postings/api/overview?view=li-lts-2025-10)
- [Guide to LinkedIn API and Alternatives](https://scrapfly.io/blog/posts/guide-to-linkedin-api-and-alternatives)
- [LinkedIn Developer Solutions](https://developer.linkedin.com/)
- [Accessing Job Board APIs in PHP - Karl Hughes](https://www.karllhughes.com/posts/access-job-apis-php)
- [JobApis · GitHub](https://github.com/jobapis)
- [25 Best Job Search Sites in 2026 | FlexJobs](https://www.flexjobs.com/blog/post/best-job-search-sites)

### ATS APIs
- [Greenhouse API overview – Greenhouse Support](https://support.greenhouse.io/hc/en-us/articles/10568627186203-Greenhouse-API-overview)
- [Harvest API | Greenhouse](https://developers.greenhouse.io/harvest.html)
- [Job Board API | Greenhouse](https://developers.greenhouse.io/job-board.html)
- [Ultimate Guide – The Best ATS Integration of 2025](https://www.mokahr.io/articles/en/the-best-ats-integration)
- [How to Build a Job Board That Connects to Greenhouse, Lever, and 60+ ATS Platforms](https://unified.to/blog/how_to_build_a_job_board_that_connects_to_greenhouse_lever_and_60_ats_platforms_with_a_unified_api)
- [Job Board API](https://developers.smartrecruiters.com/docs/partners-job-board-api)

### Aggregator APIs
- [Adzuna API](https://developer.adzuna.com/)
- [Adzuna API — Free Public API | Public APIs Directory](https://publicapis.io/adzuna-api)
- [Adzuna](https://rapidapi.com/baskarm28/api/adzuna)
- [The Muse - Developers API](https://www.themuse.com/developers/api/v2)
- [The Muse API — Free Public API | Public APIs Directory](https://publicapis.io/the-muse-api)
- [Pricing plans | jobdataapi.com](https://jobdataapi.com/accounts/pricing/)
- [Simple Job Data API | jobdataapi.com](https://jobdataapi.com/)
- [Jobs API: Access a Large-Scale Jobs Database](https://coresignal.com/solutions/jobs-data-api/)

### Google Cloud
- [Cloud Talent Solution Job Matching APIs | Google Cloud](https://cloud.google.com/solutions/talent-solution)
- [APIs and References | Job Search | Google Cloud Documentation](https://cloud.google.com/talent-solution/job-search/docs/apis)
- [Google Jobs API - SerpApi](https://serpapi.com/google-jobs-api)
- [Google Jobs API](https://www.searchapi.io/google-jobs)
- [Google Jobs API – Extract Job Listings Data | Scrapingdog](https://www.scrapingdog.com/google-jobs-api/)

### TypeScript/Node.js Libraries
- [ts-jobspy - npm Package Security Analysis - Socket](https://socket.dev/npm/package/ts-jobspy)
- [GitHub - speedyapply/JobSpy](https://github.com/speedyapply/JobSpy)
- [GitHub - llorenspujol/linkedin-jobs-scraper](https://github.com/llorenspujol/linkedin-jobs-scraper)
- [linkedin-jobs-scraper - npm](https://www.npmjs.com/package/linkedin-jobs-scraper)
- [GitHub - rynobax/indeed-scraper](https://github.com/rynobax/indeed-scraper)
- [indeed-scraper - npm](https://www.npmjs.com/package/indeed-scraper)
- [5 Best Indeed Scrapers To Test Out in 2026](https://www.scrapingdog.com/blog/best-indeed-scrapers/)
- [💼 Indeed Scraper · Apify](https://apify.com/misceres/indeed-scraper)

### Legal and Ethics
- [Is Web Scraping Legal? Laws, Ethics, and Best Practices](https://research.aimultiple.com/is-web-scraping-legal/)
- [Job Board Scraping: The Complete 2025 Guide | Job Boardly](https://www.jobboardly.com/blog/job-board-scraping-complete-guide-2025)
- [Is web scraping legal? Yes, if you know the rules.](https://blog.apify.com/is-web-scraping-legal/)
- [Web Scraping for Job Postings: Best Practices and Ethical Guide](https://www.propellum.com/blog/web-scraping-for-job-postings-best-practices-and-ethical-guide/)
- [Ethical & Compliant Web Data Benchmark in 2026](https://research.aimultiple.com/web-scraping-ethics/)
- [The Ethics of Web Scraping: Why We Don't Scrape Job Boards](https://www.webspidermount.com/the-ethics-of-web-scraping-why-we-dont-scrape-job-boards/)

### Data Standards
- [JobPosting - Schema.org Type](https://schema.org/JobPosting)
- [Job Posting Schema: Structuring Job Data | Medium](https://akshaybhopani.medium.com/job-posting-schema-structuring-job-data-for-enhanced-accessibility-and-efficiency-e7fd472a4199)
- [Learn About Job Posting Schema Markup | Google Search Central](https://developers.google.com/search/docs/appearance/structured-data/job-posting)
- [Google Jobs Schema Markup Guide | Job Boardly](https://www.jobboardly.com/blog/google-jobs-schema-markup-guide)

---

**Document Version:** 1.0
**Last Updated:** 2026-01-16
**Next Review:** Quarterly (APIs change frequently)
