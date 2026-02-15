/**
 * Base types for career job scrapers
 */

export interface JobPosting {
  id: string;
  title: string;
  company: string;
  companyUrl?: string;
  location: string;
  locationTypes?: ('remote' | 'hybrid' | 'onsite')[];
  description: string;
  shortDescription?: string;
  url: string;
  applyUrl?: string;
  datePosted: string;
  employmentType?: ('full-time' | 'part-time' | 'contract' | 'internship')[];
  salary?: {
    min?: number;
    max?: number;
    currency?: string;
    period?: 'year' | 'hour' | 'month';
  };
  skills?: string[];
  experienceLevel?: string;
  source: string;
  scraped_at: string;
}

export interface ScraperOptions {
  concurrency?: number;
  delay?: number;
  maxRetries?: number;
  timeout?: number;
}

export interface JobSearchQuery {
  query: string;
  location?: string;
  remote?: boolean;
  employmentType?: string[];
  experienceLevel?: string[];
  dateRange?: number; // days
  limit?: number;
}

export interface JobMatchScore {
  jobId: string;
  score: number;
  matchedSkills: string[];
  missingSkills: string[];
  experienceMatch: boolean;
  locationMatch: boolean;
  recommendation: 'strong-fit' | 'good-fit' | 'conditional-fit' | 'poor-fit';
}
