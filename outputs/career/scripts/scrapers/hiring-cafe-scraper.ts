#!/usr/bin/env bun
/**
 * HiringCafeScraper - Scrape job postings from hiring.cafe
 *
 * hiring.cafe displays job links on search results, then requires
 * navigating to individual job pages to get full details.
 *
 * Strategy:
 * 1. Load search page and collect all /viewjob/ links
 * 2. For each link (limited to avoid rate limiting), navigate to detail page
 * 3. Extract job information from detail page
 */

import { BaseJobScraper } from './base/base-job-scraper';
import type { JobPosting, JobSearchQuery, ScraperOptions } from './base/types';
import type { Page } from 'playwright';

interface HiringCafeSearchState {
  locations?: Array<{
    formatted_address: string;
    types: string[];
    geometry?: {
      location: {
        lat: string;
        lon: string;
      };
    };
    id: string;
    address_components: Array<{
      long_name: string;
      short_name: string;
      types: string[];
    }>;
    options?: {
      flexible_regions?: string[];
    };
  }>;
  searchQuery: string;
  dateFetchedPastNDays: number;
}

export class HiringCafeScraper extends BaseJobScraper {
  readonly source = 'hiring-cafe';

  constructor(options?: ScraperOptions) {
    super({
      ...options,
      delay: options?.delay ?? 3000, // Increased delay to be respectful
    });
  }

  /**
   * Search for jobs on hiring.cafe
   */
  async search(query: JobSearchQuery): Promise<JobPosting[]> {
    console.log(`[${this.source}] Starting job search: "${query.query}"`);
    console.log(`[${this.source}] Date range: ${query.dateRange ?? 14} days`);

    const url = this.buildSearchUrl(query);
    const page = await this.navigate(url);

    try {
      // Step 1: Get all job links from search page
      console.log(`[${this.source}] Waiting for job links to load...`);
      await this.sleep(5000); // Wait for React to hydrate

      const jobLinks = await this.collectJobLinks(page);
      console.log(`[${this.source}] Found ${jobLinks.length} job links`);

      await page.close();

      if (jobLinks.length === 0) {
        return [];
      }

      // Step 2: Extract details from job pages (limit to avoid rate limiting)
      const limit = Math.min(query.limit ?? 20, jobLinks.length);
      const limitedLinks = jobLinks.slice(0, limit);

      console.log(`[${this.source}] Extracting details from ${limitedLinks.length} jobs...`);

      const jobs = await this.concurrentMap(
        limitedLinks,
        async (link, index) => {
          console.log(`[${this.source}] Processing job ${index + 1}/${limitedLinks.length}: ${link}`);
          return await this.extractJobDetails(link);
        },
        {
          concurrency: 3, // Conservative concurrency
          delay: this.options.delay,
        }
      );

      // Filter out null results (failed extractions)
      const validJobs = jobs.filter((job): job is JobPosting => job !== null);

      console.log(`[${this.source}] Successfully extracted ${validJobs.length} jobs`);
      return validJobs;
    } catch (error) {
      console.error(`[${this.source}] Error during search:`, error);
      await page.close();
      throw error;
    }
  }

  /**
   * Build search URL with encoded state
   */
  private buildSearchUrl(query: JobSearchQuery): string {
    const searchState: HiringCafeSearchState = {
      searchQuery: query.query,
      dateFetchedPastNDays: query.dateRange ?? 14,
    };

    // Add location if specified
    if (query.location) {
      searchState.locations = [
        {
          formatted_address: query.location,
          types: ['locality'],
          id: 'user_location',
          address_components: [
            {
              long_name: query.location,
              short_name: query.location,
              types: ['locality'],
            },
          ],
        },
      ];
    } else if (query.remote) {
      // Default to US with flexible regions for remote jobs
      searchState.locations = [
        {
          formatted_address: 'United States',
          types: ['country'],
          geometry: {
            location: {
              lat: '37.0902',
              lon: '-95.7129',
            },
          },
          id: 'user_country',
          address_components: [
            {
              long_name: 'United States',
              short_name: 'US',
              types: ['country'],
            },
          ],
          options: {
            flexible_regions: ['anywhere_in_continent', 'anywhere_in_world'],
          },
        },
      ];
    }

    const encodedState = encodeURIComponent(JSON.stringify(searchState));
    return `https://hiring.cafe/?searchState=${encodedState}`;
  }

  /**
   * Collect all job links from search page
   */
  private async collectJobLinks(page: Page): Promise<string[]> {
    const links = await page.evaluate(() => {
      const jobLinks = Array.from(
        document.querySelectorAll('a[href*="/viewjob/"]')
      );
      return jobLinks
        .map((link) => (link as HTMLAnchorElement).href)
        .filter((href) => href && href.includes('/viewjob/'));
    });

    // Deduplicate
    return Array.from(new Set(links));
  }

  /**
   * Extract job details from individual job page
   */
  private async extractJobDetails(jobUrl: string): Promise<JobPosting | null> {
    try {
      const page = await this.retry(
        async () => await this.navigate(jobUrl),
        `navigate to ${jobUrl}`
      );

      await this.sleep(2000); // Wait for content to load

      // Extract job details
      const jobData = await page.evaluate(() => {
        // Title from h1 or h2
        const titleEl =
          document.querySelector('h1') || document.querySelector('h2');
        const title = titleEl?.textContent?.trim() || '';

        // Description from article or main content
        const descEl =
          document.querySelector('article') ||
          document.querySelector('main') ||
          document.querySelector('[class*="description" i]');
        const description = descEl?.textContent?.trim() || '';

        // Company - usually near the title
        const companyEl = document.querySelector('[class*="company" i]');
        let company = companyEl?.textContent?.trim() || '';

        // If no specific company element, try to extract from description
        if (!company && description) {
          const companyMatch = description.match(/(?:at|for|with)\s+([A-Z][A-Za-z\s&]+?)(?:\s+is|\s+seeks|\.|,)/);
          company = companyMatch?.[1]?.trim() || 'Unknown Company';
        }

        // Location
        const locationEl = document.querySelector('[class*="location" i]');
        let location = locationEl?.textContent?.trim() || '';

        // Check title for Remote indicator
        if (!location || !location.toLowerCase().includes('remote')) {
          if (title.toLowerCase().includes('remote')) {
            location = 'Remote';
          }
        }

        // Salary
        const salaryEl = document.querySelector('[class*="salary" i]');
        const salary = salaryEl?.textContent?.trim() || '';

        // Date posted
        const dateEl = document.querySelector('time') || document.querySelector('[datetime]');
        const datePosted = dateEl?.getAttribute('datetime') || dateEl?.textContent?.trim() || '';

        return {
          title,
          company,
          location,
          description,
          salary,
          datePosted,
        };
      });

      await page.close();

      // Validate we got meaningful data
      if (!jobData.title || !jobData.description) {
        console.warn(`[${this.source}] Incomplete data for ${jobUrl}`);
        return null;
      }

      const now = new Date().toISOString();

      const posting: JobPosting = {
        id: this.generateJobId(jobData.company, jobData.title, jobUrl),
        title: jobData.title,
        company: jobData.company || 'Unknown Company',
        location: jobData.location || 'Remote',
        description: jobData.description,
        shortDescription: jobData.description.substring(0, 300),
        url: jobUrl,
        applyUrl: jobUrl,
        datePosted: this.parseDate(jobData.datePosted),
        source: this.source,
        scraped_at: now,
      };

      // Parse location types
      const locationLower = posting.location.toLowerCase();
      if (locationLower.includes('remote') || locationLower.includes('anywhere')) {
        posting.locationTypes = ['remote'];
      } else if (locationLower.includes('hybrid')) {
        posting.locationTypes = ['hybrid'];
      } else {
        posting.locationTypes = ['onsite'];
      }

      // Parse salary if available
      if (jobData.salary) {
        posting.salary = this.parseSalary(jobData.salary);
      }

      return posting;
    } catch (error) {
      console.error(`[${this.source}] Error extracting ${jobUrl}:`, error);
      return null;
    }
  }

  /**
   * Parse date string to ISO format
   */
  private parseDate(dateStr: string | undefined): string {
    if (!dateStr) {
      return new Date().toISOString();
    }

    const now = new Date();

    // "X days ago"
    const daysMatch = dateStr.match(/(\d+)\s*days?\s*ago/i);
    if (daysMatch) {
      const days = parseInt(daysMatch[1]);
      const date = new Date(now);
      date.setDate(date.getDate() - days);
      return date.toISOString();
    }

    // "X hours ago"
    const hoursMatch = dateStr.match(/(\d+)\s*hours?\s*ago/i);
    if (hoursMatch) {
      const hours = parseInt(hoursMatch[1]);
      const date = new Date(now);
      date.setHours(date.getHours() - hours);
      return date.toISOString();
    }

    // Try to parse as ISO date
    try {
      const parsed = new Date(dateStr);
      if (!isNaN(parsed.getTime())) {
        return parsed.toISOString();
      }
    } catch {
      // Ignore
    }

    return now.toISOString();
  }

  /**
   * Parse salary string to structured format
   */
  private parseSalary(salaryStr: string): JobPosting['salary'] {
    const salary: JobPosting['salary'] = {
      currency: 'USD',
      period: 'year',
    };

    // Extract currency
    if (salaryStr.includes('$')) {
      salary.currency = 'USD';
    } else if (salaryStr.includes('€')) {
      salary.currency = 'EUR';
    } else if (salaryStr.includes('£')) {
      salary.currency = 'GBP';
    }

    // Extract min/max values
    const rangeMatch = salaryStr.match(/[\$€£]?\s*(\d+(?:,\d+)?(?:k|K)?)\s*-\s*[\$€£]?\s*(\d+(?:,\d+)?(?:k|K)?)/);
    if (rangeMatch) {
      salary.min = this.parseAmount(rangeMatch[1]);
      salary.max = this.parseAmount(rangeMatch[2]);
    } else {
      // Single amount
      const amountMatch = salaryStr.match(/[\$€£]?\s*(\d+(?:,\d+)?(?:k|K)?)/);
      if (amountMatch) {
        const amount = this.parseAmount(amountMatch[1]);
        salary.min = amount;
        salary.max = amount;
      }
    }

    // Determine period
    if (salaryStr.toLowerCase().includes('hour')) {
      salary.period = 'hour';
    } else if (salaryStr.toLowerCase().includes('month')) {
      salary.period = 'month';
    }

    return salary;
  }

  /**
   * Parse amount string to number (handles "150k" format)
   */
  private parseAmount(amountStr: string): number {
    const cleaned = amountStr.replace(/,/g, '');
    if (cleaned.toLowerCase().endsWith('k')) {
      return parseInt(cleaned.slice(0, -1)) * 1000;
    }
    return parseInt(cleaned);
  }
}

// CLI usage
if (import.meta.main) {
  const scraper = new HiringCafeScraper({ delay: 3000, timeout: 30000 });

  const query: JobSearchQuery = {
    query: 'cybersecurity engineer remote',
    remote: true,
    dateRange: 14,
    limit: 5, // Limit for testing
  };

  try {
    const jobs = await scraper.search(query);

    console.log('\n' + '='.repeat(60));
    console.log(`Found ${jobs.length} jobs`);
    console.log('='.repeat(60) + '\n');

    for (const job of jobs) {
      console.log(`${job.title} at ${job.company}`);
      console.log(`  Location: ${job.location}`);
      console.log(`  Posted: ${new Date(job.datePosted).toLocaleDateString()}`);
      console.log(`  URL: ${job.url}`);
      if (job.salary?.min) {
        console.log(`  Salary: $${job.salary.min.toLocaleString()}-$${job.salary.max?.toLocaleString()}/${job.salary.period}`);
      }
      console.log('');
    }

    await scraper.cleanup();
    await scraper.browserManager.close();
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}
