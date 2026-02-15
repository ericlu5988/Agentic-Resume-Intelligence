#!/usr/bin/env bun
/**
 * discover-jobs.ts - Job discovery and scoring CLI
 *
 * Usage:
 *   bun skills/career/scripts/discover-jobs.ts "cybersecurity director remote"
 *   bun skills/career/scripts/discover-jobs.ts "security engineer" --days 7 --min-score 70
 *   bun skills/career/scripts/discover-jobs.ts "pentest" --resume path/to/resume.md --limit 10
 *
 * Options:
 *   --days N          Search jobs from past N days (default: 14)
 *   --min-score N     Minimum match score (default: 60)
 *   --limit N         Max jobs to return (default: 20)
 *   --resume PATH     Path to resume file
 *   --remote          Only remote jobs
 *   --location LOC    Specific location
 *   --save            Save results to output folder
 *   --json            Output as JSON
 */

import { HiringCafeScraper } from './scrapers/hiring-cafe-scraper';
import { JobScorer } from './scrapers/job-scorer';
import type { JobSearchQuery } from './scrapers/base/types';
import { writeFileSync } from 'fs';
import { join } from 'path';

interface DiscoverOptions {
  days: number;
  minScore: number;
  limit: number;
  resume?: string;
  remote: boolean;
  location?: string;
  save: boolean;
  json: boolean;
}

function parseArgs(): { query: string; options: DiscoverOptions } {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0].startsWith('--')) {
    console.error('Usage: discover-jobs.ts "search query" [options]');
    console.error('\nOptions:');
    console.error('  --days N          Search jobs from past N days (default: 14)');
    console.error('  --min-score N     Minimum match score (default: 60)');
    console.error('  --limit N         Max jobs to return (default: 20)');
    console.error('  --resume PATH     Path to resume file');
    console.error('  --remote          Only remote jobs');
    console.error('  --location LOC    Specific location');
    console.error('  --save            Save results to output folder');
    console.error('  --json            Output as JSON');
    process.exit(1);
  }

  const query = args[0];
  const options: DiscoverOptions = {
    days: 14,
    minScore: 60,
    limit: 20,
    remote: false,
    save: false,
    json: false,
  };

  for (let i = 1; i < args.length; i++) {
    const arg = args[i];
    switch (arg) {
      case '--days':
        options.days = parseInt(args[++i]);
        break;
      case '--min-score':
        options.minScore = parseInt(args[++i]);
        break;
      case '--limit':
        options.limit = parseInt(args[++i]);
        break;
      case '--resume':
        options.resume = args[++i];
        break;
      case '--remote':
        options.remote = true;
        break;
      case '--location':
        options.location = args[++i];
        break;
      case '--save':
        options.save = true;
        break;
      case '--json':
        options.json = true;
        break;
      default:
        console.error(`Unknown option: ${arg}`);
        process.exit(1);
    }
  }

  return { query, options };
}

async function main() {
  const { query, options } = parseArgs();

  console.log('\n' + '='.repeat(70));
  console.log('JOB DISCOVERY - hiring.cafe');
  console.log('='.repeat(70));
  console.log(`Query: "${query}"`);
  console.log(`Date Range: Past ${options.days} days`);
  console.log(`Min Score: ${options.minScore}%`);
  console.log(`Limit: ${options.limit} jobs`);
  if (options.remote) console.log('Remote: Yes');
  if (options.location) console.log(`Location: ${options.location}`);
  console.log('='.repeat(70) + '\n');

  // Step 1: Scrape jobs from hiring.cafe
  console.log('[1/3] Scraping hiring.cafe...');
  const scraper = new HiringCafeScraper({ delay: 2000, timeout: 30000 });

  const searchQuery: JobSearchQuery = {
    query,
    dateRange: options.days,
    remote: options.remote,
    location: options.location,
    limit: options.limit,
  };

  let jobs;
  try {
    jobs = await scraper.search(searchQuery);
    console.log(`      Found ${jobs.length} jobs\n`);
  } catch (error) {
    console.error('Error scraping jobs:', error);
    await scraper.cleanup();
    await scraper.browserManager.close();
    process.exit(1);
  }

  if (jobs.length === 0) {
    console.log('No jobs found. Try adjusting your search parameters.\n');
    await scraper.cleanup();
    await scraper.browserManager.close();
    return;
  }

  // Step 2: Score jobs against resume
  console.log('[2/3] Scoring jobs against resume...');
  const scorer = new JobScorer(options.resume);
  const scored = scorer.filterByScore(jobs, options.minScore);

  console.log(`      ${scored.length} jobs match criteria (≥${options.minScore}%)\n`);

  // Step 3: Display results
  console.log('[3/3] Top matches:\n');

  if (scored.length === 0) {
    console.log('No jobs meet the minimum score threshold.');
    console.log('Try lowering --min-score or adjusting your search.\n');
    await scraper.cleanup();
    await scraper.browserManager.close();
    return;
  }

  // Limit results
  const topJobs = scored.slice(0, options.limit);

  if (options.json) {
    // JSON output
    console.log(JSON.stringify(topJobs, null, 2));
  } else {
    // Human-readable output
    console.log('='.repeat(70));

    for (let i = 0; i < topJobs.length; i++) {
      const job = topJobs[i];
      const match = job.matchScore;

      // Color coding for score
      let scoreColor = '';
      if (match.score >= 75) scoreColor = '🟢'; // Green - strong fit
      else if (match.score >= 60) scoreColor = '🟡'; // Yellow - good fit
      else scoreColor = '🟠'; // Orange - conditional fit

      console.log(`\n${i + 1}. ${scoreColor} ${job.title} - ${match.score}%`);
      console.log(`   Company: ${job.company}`);
      console.log(`   Location: ${job.location} ${job.locationTypes?.join(', ') || ''}`);

      if (job.salary?.min) {
        console.log(`   Salary: $${job.salary.min.toLocaleString()}-$${job.salary.max?.toLocaleString()}/${job.salary.period}`);
      }

      console.log(`   Posted: ${new Date(job.datePosted).toLocaleDateString()}`);
      console.log(`   URL: ${job.url}`);

      // Show match details
      console.log(`\n   Match Details:`);
      console.log(`   - Recommendation: ${match.recommendation.toUpperCase().replace('-', ' ')}`);

      if (match.matchedSkills.length > 0) {
        console.log(`   - Matched Skills: ${match.matchedSkills.slice(0, 5).join(', ')}${match.matchedSkills.length > 5 ? '...' : ''}`);
      }

      if (match.missingSkills.length > 0 && match.missingSkills.length <= 3) {
        console.log(`   - Missing Skills: ${match.missingSkills.join(', ')}`);
      }

      console.log('   ' + '-'.repeat(68));
    }

    console.log('\n' + '='.repeat(70));
    console.log(`\nShowing ${topJobs.length} of ${scored.length} matching jobs`);
    console.log('='.repeat(70) + '\n');
  }

  // Step 4: Save results if requested
  if (options.save) {
    const timestamp = new Date().toISOString().split('T')[0];
    const sanitizedQuery = query.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');
    const outputDir = join(process.env.HOME || '', '.claude', 'skills', 'career', 'output');
    const filename = `discovered-jobs-${sanitizedQuery}-${timestamp}.json`;
    const filepath = join(outputDir, filename);

    writeFileSync(
      filepath,
      JSON.stringify(
        {
          query,
          searchDate: new Date().toISOString(),
          totalFound: jobs.length,
          totalMatching: scored.length,
          minScore: options.minScore,
          jobs: topJobs,
        },
        null,
        2
      )
    );

    console.log(`\nResults saved to: ${filename}\n`);
  }

  // Cleanup
  await scraper.cleanup();
  await scraper.browserManager.close();
}

if (import.meta.main) {
  main().catch((error) => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}
