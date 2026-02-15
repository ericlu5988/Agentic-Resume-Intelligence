/**
 * BaseJobScraper - Abstract base class for all job board scrapers
 * Provides common browser operations, retry logic, and concurrency control
 */

import type { Page, BrowserContext } from 'playwright';
import { BrowserManager } from '@/tools/automation/browser-manager';
import type { JobPosting, ScraperOptions, JobSearchQuery } from './types';

export abstract class BaseJobScraper {
  protected browserManager: BrowserManager;
  protected context: BrowserContext | null = null;
  protected options: Required<ScraperOptions>;

  abstract readonly source: string;

  constructor(options: ScraperOptions = {}) {
    this.browserManager = BrowserManager.getInstance();
    this.options = {
      concurrency: options.concurrency ?? 5,
      delay: options.delay ?? 2000,
      maxRetries: options.maxRetries ?? 3,
      timeout: options.timeout ?? 30000,
    };
  }

  /**
   * Main search method - must be implemented by platform scrapers
   */
  abstract search(query: JobSearchQuery): Promise<JobPosting[]>;

  /**
   * Initialize browser context
   */
  protected async init(): Promise<void> {
    if (!this.context) {
      this.context = await this.browserManager.getContext(this.source);
    }
  }

  /**
   * Navigate to a URL and return page
   */
  protected async navigate(url: string): Promise<Page> {
    await this.init();

    const page = await this.context!.newPage();

    await page.goto(url, {
      waitUntil: 'networkidle',
      timeout: this.options.timeout,
    });

    return page;
  }

  /**
   * Extract text content from a single element
   */
  protected async extractText(
    page: Page,
    selector: string
  ): Promise<string | null> {
    try {
      const text = await page.$eval(
        selector,
        (el) => el.textContent?.trim() || null
      );
      return text;
    } catch {
      return null;
    }
  }

  /**
   * Extract text from all matching elements
   */
  protected async extractAll(
    page: Page,
    selector: string
  ): Promise<string[]> {
    try {
      const texts = await page.$$eval(selector, (elements) =>
        elements.map((el) => el.textContent?.trim() || '').filter((t) => t)
      );
      return texts;
    } catch {
      return [];
    }
  }

  /**
   * Extract attribute from element
   */
  protected async extractAttribute(
    page: Page,
    selector: string,
    attribute: string
  ): Promise<string | null> {
    try {
      const value = await page.$eval(
        selector,
        (el, attr) => el.getAttribute(attr),
        attribute
      );
      return value;
    } catch {
      return null;
    }
  }

  /**
   * Wait for selector with timeout
   */
  protected async waitFor(
    page: Page,
    selector: string,
    timeout?: number
  ): Promise<boolean> {
    try {
      await page.waitForSelector(selector, {
        timeout: timeout ?? this.options.timeout,
        state: 'visible',
      });
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Retry function with exponential backoff
   */
  protected async retry<R>(
    fn: () => Promise<R>,
    context: string = 'operation'
  ): Promise<R> {
    let lastError: Error | null = null;

    for (let attempt = 1; attempt <= this.options.maxRetries; attempt++) {
      try {
        return await fn();
      } catch (error) {
        lastError = error instanceof Error ? error : new Error(String(error));

        if (attempt === this.options.maxRetries) {
          break;
        }

        const delay = this.options.delay * attempt;
        console.log(
          `[${this.source}] Retry ${attempt}/${this.options.maxRetries} for ${context}: ${lastError.message}`
        );
        console.log(`[${this.source}] Waiting ${delay}ms before retry...`);

        await this.sleep(delay);
      }
    }

    throw lastError!;
  }

  /**
   * Process items concurrently in batches
   */
  protected async concurrentMap<I, R>(
    items: I[],
    fn: (item: I, index: number) => Promise<R>,
    options?: { concurrency?: number; delay?: number }
  ): Promise<R[]> {
    const concurrency = options?.concurrency ?? this.options.concurrency;
    const delay = options?.delay ?? this.options.delay;
    const results: R[] = [];

    console.log(
      `[${this.source}] Processing ${items.length} items with concurrency ${concurrency}`
    );

    for (let i = 0; i < items.length; i += concurrency) {
      const batch = items.slice(i, i + concurrency);
      const batchNum = Math.floor(i / concurrency) + 1;
      const totalBatches = Math.ceil(items.length / concurrency);

      console.log(
        `[${this.source}] Processing batch ${batchNum}/${totalBatches} (${batch.length} items)`
      );

      const batchResults = await Promise.all(
        batch.map((item, idx) => fn(item, i + idx))
      );

      results.push(...batchResults);

      // Delay between batches (except for last batch)
      if (i + concurrency < items.length && delay > 0) {
        // Add random jitter (±30%) to avoid detection
        const jitter = Math.random() * 0.6 - 0.3; // -30% to +30%
        const actualDelay = Math.floor(delay * (1 + jitter));
        console.log(`[${this.source}] Waiting ${actualDelay}ms before next batch...`);
        await this.sleep(actualDelay);
      }
    }

    return results;
  }

  /**
   * Sleep for specified milliseconds
   */
  protected sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  /**
   * Generate unique ID from job data
   */
  protected generateJobId(company: string, title: string, url: string): string {
    const input = `${company}-${title}-${url}`.toLowerCase().replace(/\s+/g, '-');
    return Buffer.from(input).toString('base64').slice(0, 16);
  }

  /**
   * Cleanup resources
   */
  async cleanup(): Promise<void> {
    if (this.context) {
      await this.browserManager.closeContext(this.source);
      this.context = null;
    }
  }
}
