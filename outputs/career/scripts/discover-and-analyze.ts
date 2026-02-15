#!/usr/bin/env bun
/**
 * discover-and-analyze.ts - Enhanced job discovery with parallel analysis
 *
 * Workflow:
 * 1. Search hiring.cafe for matching jobs
 * 2. Score jobs against resume
 * 3. For jobs ≥60% match, launch parallel Haiku agents to run full /career analysis
 * 4. Return immediately with background task tracking
 *
 * Usage:
 *   bun skills/career/scripts/discover-and-analyze.ts "penetration tester remote"
 *   bun skills/career/scripts/discover-and-analyze.ts "cybersecurity director" --min-score 70 --max-parallel 3
 */

import { HiringCafeScraper } from './scrapers/hiring-cafe-scraper';
import { JobScorer } from './scrapers/job-scorer';
import type { JobSearchQuery, JobPosting } from './scrapers/base/types';
import { spawn } from 'child_process';
import { writeFileSync, mkdirSync, existsSync } from 'fs';
import { join } from 'path';

interface AnalyzeOptions {
  days: number;
  minScore: number;
  limit: number;
  resume?: string;
  remote: boolean;
  location?: string;
  maxParallel: number; // Max jobs to analyze in parallel
  save: boolean;
}

function parseArgs(): { query: string; options: AnalyzeOptions } {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0].startsWith('--')) {
    console.error('Usage: discover-and-analyze.ts "search query" [options]');
    console.error('\nOptions:');
    console.error('  --days N          Search jobs from past N days (default: 14)');
    console.error('  --min-score N     Minimum match score (default: 60)');
    console.error('  --limit N         Max jobs to discover (default: 20)');
    console.error('  --max-parallel N  Max jobs to analyze in parallel (default: 5)');
    console.error('  --resume PATH     Path to resume file');
    console.error('  --remote          Only remote jobs');
    console.error('  --location LOC    Specific location');
    console.error('  --save            Save results to output folder');
    process.exit(1);
  }

  const query = args[0];
  const options: AnalyzeOptions = {
    days: 14,
    minScore: 60,
    limit: 20,
    remote: false,
    maxParallel: 5,
    save: true, // Default to saving results
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
      case '--max-parallel':
        options.maxParallel = parseInt(args[++i]);
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
      default:
        console.error(`Unknown option: ${arg}`);
        process.exit(1);
    }
  }

  return { query, options };
}

/**
 * Launch background /career analysis for a job
 */
function launchCareerAnalysis(job: JobPosting, outputDir: string): Promise<string> {
  return new Promise((resolve) => {
    const sanitizedTitle = job.title
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/-+$/, '');

    const jobDir = join(outputDir, sanitizedTitle);

    // Create job-specific directory
    if (!existsSync(jobDir)) {
      mkdirSync(jobDir, { recursive: true });
    }

    // Write job details for reference
    writeFileSync(
      join(jobDir, 'job-posting.json'),
      JSON.stringify(job, null, 2)
    );

    const logFile = join(jobDir, 'analysis.log');
    const outputFile = join(jobDir, 'analysis-output.txt');

    // Spawn Claude Code process to run /career analysis
    // This will run in the background and complete asynchronously
    const child = spawn(
      'claude',
      [
        'code',
        '--message',
        `/career analyze ${job.url}`,
        '--output',
        outputFile,
      ],
      {
        detached: true,
        stdio: ['ignore', 'pipe', 'pipe'],
      }
    );

    // Write logs
    const logStream = require('fs').createWriteStream(logFile);
    child.stdout?.pipe(logStream);
    child.stderr?.pipe(logStream);

    child.unref(); // Allow parent to exit while child runs

    resolve(jobDir);
  });
}

async function main() {
  const { query, options } = parseArgs();

  console.log('\n' + '='.repeat(70));
  console.log('JOB DISCOVERY + PARALLEL ANALYSIS - hiring.cafe');
  console.log('='.repeat(70));
  console.log(`Query: "${query}"`);
  console.log(`Date Range: Past ${options.days} days`);
  console.log(`Min Score: ${options.minScore}%`);
  console.log(`Max Parallel Analysis: ${options.maxParallel} jobs`);
  console.log('='.repeat(70) + '\n');

  // Step 1: Scrape jobs
  console.log('[1/4] Scraping hiring.cafe...');
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

  // Step 2: Score jobs
  console.log('[2/4] Scoring jobs against resume...');
  const scorer = new JobScorer(options.resume);
  const scored = scorer.filterByScore(jobs, options.minScore);

  console.log(`      ${scored.length} jobs match criteria (≥${options.minScore}%)\n`);

  if (scored.length === 0) {
    console.log('No jobs meet the minimum score threshold.');
    console.log('Try lowering --min-score or adjusting your search.\n');
    await scraper.cleanup();
    await scraper.browserManager.close();
    return;
  }

  // Step 3: Display top matches
  console.log('[3/4] Top matches:\n');
  console.log('='.repeat(70));

  const jobsToAnalyze = scored.slice(0, options.maxParallel);

  for (let i = 0; i < jobsToAnalyze.length; i++) {
    const job = jobsToAnalyze[i];
    const match = job.matchScore;

    let scoreColor = '';
    if (match.score >= 75) scoreColor = '🟢';
    else if (match.score >= 60) scoreColor = '🟡';
    else scoreColor = '🟠';

    console.log(`\n${i + 1}. ${scoreColor} ${job.title} - ${match.score}%`);
    console.log(`   Company: ${job.company}`);
    console.log(`   Location: ${job.location}`);
    console.log(`   URL: ${job.url}`);
    console.log(`   Recommendation: ${match.recommendation.toUpperCase().replace('-', ' ')}`);

    if (match.matchedSkills.length > 0) {
      console.log(`   Matched: ${match.matchedSkills.slice(0, 5).join(', ')}`);
    }

    console.log('   ' + '-'.repeat(68));
  }

  console.log('\n' + '='.repeat(70) + '\n');

  // Step 4: Launch parallel analysis
  console.log(`[4/4] Launching parallel analysis for top ${jobsToAnalyze.length} jobs...\n`);

  const timestamp = new Date().toISOString().split('T')[0];
  const sanitizedQuery = query.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');
  const outputDir = join(
    process.env.HOME || '',
    '.claude',
    'skills',
    'career',
    'output',
    `batch-${sanitizedQuery}-${timestamp}`
  );

  if (!existsSync(outputDir)) {
    mkdirSync(outputDir, { recursive: true });
  }

  // Launch analysis for each job
  const analysisPromises = jobsToAnalyze.map(async (job) => {
    const jobDir = await launchCareerAnalysis(job, outputDir);
    console.log(`✓ Launched analysis: ${job.title}`);
    console.log(`  Output: ${jobDir}/`);
    return jobDir;
  });

  await Promise.all(analysisPromises);

  console.log('\n' + '='.repeat(70));
  console.log(`\n✅ Launched ${jobsToAnalyze.length} background analyses`);
  console.log(`\nResults will be saved to:\n  ${outputDir}/\n`);
  console.log('Each job has its own subdirectory with:');
  console.log('  - job-posting.json (original job data)');
  console.log('  - analysis.log (progress log)');
  console.log('  - analysis-output.txt (final results)');
  console.log('  - 01-assess.md, 02-research.md, etc. (phase outputs)\n');

  // Save summary
  const summaryPath = join(outputDir, 'SUMMARY.md');
  const summary = `# Job Discovery + Analysis Summary

**Query:** ${query}
**Date:** ${new Date().toISOString()}
**Total Found:** ${jobs.length} jobs
**Matched Criteria:** ${scored.length} jobs (≥${options.minScore}%)
**Analyzed:** ${jobsToAnalyze.length} jobs

## Top Matches

${jobsToAnalyze
  .map((job, i) => {
    const score = job.matchScore.score;
    const icon = score >= 75 ? '🟢' : score >= 60 ? '🟡' : '🟠';
    return `${i + 1}. ${icon} **${job.title}** - ${score}%
   - Company: ${job.company}
   - URL: ${job.url}
   - Analysis: ./${job.title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/-+$/, '')}/`;
  })
  .join('\n\n')}

## Analysis Status

Check individual job directories for progress.
Each analysis runs in the background using Claude Code.
`;

  writeFileSync(summaryPath, summary);
  console.log(`Summary saved to: ${summaryPath}\n`);

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
