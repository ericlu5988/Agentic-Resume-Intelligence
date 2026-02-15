#!/usr/bin/env bun
/**
 * JobScorer - Match and score job postings against resume/skills
 *
 * Uses the same GO/NO-GO scoring methodology from Phase 1 (Assess)
 * to evaluate discovered jobs without running full 5-phase workflow.
 */

import type { JobPosting, JobMatchScore } from './base/types';
import { readFileSync, existsSync } from 'fs';
import { join } from 'path';

interface Resume {
  skills: string[];
  experience_years?: number;
  location_preferences?: string[];
  remote_preference?: boolean;
  raw_content?: string;
}

export class JobScorer {
  private resume: Resume;

  constructor(resumePath?: string) {
    this.resume = this.loadResume(resumePath);
  }

  /**
   * Load resume from file or default location
   */
  private loadResume(resumePath?: string): Resume {
    const FRAMEWORK_ROOT = process.env.IA_FRAMEWORK_ROOT || join(process.env.HOME || '', '.claude');

    // Try multiple possible paths
    const possiblePaths = [
      resumePath,
      join(process.env.HOME || '', 'ia-framework-private', 'skills', 'career', 'input', 'chris_resume.md'),
      join(FRAMEWORK_ROOT, 'skills', 'career', 'input', 'chris_resume.md'),
      'skills/career/input/chris_resume.md',
    ].filter(p => p) as string[];

    let path: string | undefined;
    for (const p of possiblePaths) {
      if (existsSync(p)) {
        path = p;
        break;
      }
    }

    if (!path) {
      throw new Error(
        `Resume not found. Tried:\n${possiblePaths.map(p => `  - ${p}`).join('\n')}\n\n` +
        `Provide resume path with --resume option.`
      );
    }

    const content = readFileSync(path, 'utf-8');
    return this.parseResume(content);
  }

  /**
   * Parse resume to extract skills and preferences
   */
  private parseResume(content: string): Resume {
    const skills: string[] = [];
    let experienceYears = 0;

    // Extract skills from various sections
    const skillPatterns = [
      /(?:Skills?|Technologies?|Tools?|Expertise|Core Competencies):\s*([^\n]+)/gi,
      /(?:Proficient in|Experience with):\s*([^\n]+)/gi,
      /##\s*(?:Skills?|Technologies?|Tools?|Expertise|Core Competencies)\s*\n([^\n#]+)/gi,
    ];

    for (const pattern of skillPatterns) {
      let match;
      while ((match = pattern.exec(content)) !== null) {
        const skillsText = match[1];
        const extracted = skillsText
          .split(/[,;•\|]/)
          .map((s) => s.trim())
          .filter((s) => s.length > 0);
        skills.push(...extracted);
      }
    }

    // Extract years of experience
    const yearsMatch = content.match(/(\d+)\+?\s*years?/i);
    if (yearsMatch) {
      experienceYears = parseInt(yearsMatch[1]);
    }

    // Normalize skills (lowercase, dedupe)
    const normalizedSkills = Array.from(
      new Set(skills.map((s) => s.toLowerCase().trim()))
    );

    return {
      skills: normalizedSkills,
      experience_years: experienceYears,
      remote_preference: content.toLowerCase().includes('remote'),
      raw_content: content,
    };
  }

  /**
   * Score a single job posting against resume
   */
  scoreJob(job: JobPosting): JobMatchScore {
    const matchedSkills: string[] = [];
    const missingSkills: string[] = [];

    // Extract required skills from job description
    const jobSkills = this.extractJobSkills(job.description);

    // Calculate skill match
    for (const jobSkill of jobSkills) {
      const matched = this.resume.skills.some((resumeSkill) =>
        this.skillsMatch(resumeSkill, jobSkill)
      );

      if (matched) {
        matchedSkills.push(jobSkill);
      } else {
        missingSkills.push(jobSkill);
      }
    }

    // Calculate skill match percentage (40% weight)
    const skillMatchScore =
      jobSkills.length > 0 ? (matchedSkills.length / jobSkills.length) * 40 : 0;

    // Experience match (25% weight)
    const experienceMatch = this.matchExperience(job, this.resume);
    const experienceScore = experienceMatch ? 25 : 0;

    // Location match (15% weight)
    const locationMatch = this.matchLocation(job, this.resume);
    const locationScore = locationMatch ? 15 : 0;

    // Nice-to-have/bonus points (20% weight)
    const bonusScore = this.calculateBonusPoints(job, this.resume);

    // Total score
    const score = Math.min(
      100,
      skillMatchScore + experienceScore + locationScore + bonusScore
    );

    // Determine recommendation
    let recommendation: JobMatchScore['recommendation'];
    if (score >= 75) {
      recommendation = 'strong-fit';
    } else if (score >= 60) {
      recommendation = 'good-fit';
    } else if (score >= 45) {
      recommendation = 'conditional-fit';
    } else {
      recommendation = 'poor-fit';
    }

    return {
      jobId: job.id,
      score: Math.round(score),
      matchedSkills,
      missingSkills,
      experienceMatch,
      locationMatch,
      recommendation,
    };
  }

  /**
   * Score multiple jobs and return sorted by score
   */
  scoreJobs(jobs: JobPosting[]): Array<JobPosting & { matchScore: JobMatchScore }> {
    const scored = jobs.map((job) => ({
      ...job,
      matchScore: this.scoreJob(job),
    }));

    // Sort by score descending
    return scored.sort((a, b) => b.matchScore.score - a.matchScore.score);
  }

  /**
   * Filter jobs by minimum score threshold
   */
  filterByScore(
    jobs: JobPosting[],
    minScore: number = 60
  ): Array<JobPosting & { matchScore: JobMatchScore }> {
    const scored = this.scoreJobs(jobs);
    return scored.filter((job) => job.matchScore.score >= minScore);
  }

  /**
   * Extract skills from job description
   */
  private extractJobSkills(description: string): string[] {
    const skills = new Set<string>();
    const lowerDesc = description.toLowerCase();

    // Common skill keywords
    const skillKeywords = [
      'python', 'javascript', 'typescript', 'react', 'node', 'aws', 'azure', 'gcp',
      'docker', 'kubernetes', 'terraform', 'ansible', 'jenkins', 'ci/cd',
      'sql', 'nosql', 'postgresql', 'mongodb', 'redis',
      'linux', 'bash', 'git', 'api', 'rest', 'graphql',
      'security', 'pentest', 'penetration testing', 'vulnerability', 'siem',
      'nist', 'iso 27001', 'compliance', 'gdpr', 'hipaa',
      'incident response', 'threat intelligence', 'osint',
      'burp suite', 'metasploit', 'wireshark', 'nmap',
      'soc', 'blue team', 'red team', 'purple team',
    ];

    for (const keyword of skillKeywords) {
      if (lowerDesc.includes(keyword)) {
        skills.add(keyword);
      }
    }

    return Array.from(skills);
  }

  /**
   * Check if two skills match (handles variations)
   */
  private skillsMatch(resumeSkill: string, jobSkill: string): boolean {
    const r = resumeSkill.toLowerCase();
    const j = jobSkill.toLowerCase();

    // Exact match
    if (r === j) return true;

    // Partial match (contains)
    if (r.includes(j) || j.includes(r)) return true;

    // Common variations
    const variations: Record<string, string[]> = {
      javascript: ['js', 'ecmascript', 'node', 'nodejs'],
      typescript: ['ts'],
      python: ['py'],
      kubernetes: ['k8s'],
      'penetration testing': ['pentest', 'pentesting', 'pen test'],
      cybersecurity: ['security', 'infosec', 'cyber security'],
    };

    for (const [base, alts] of Object.entries(variations)) {
      if ((r === base || alts.includes(r)) && (j === base || alts.includes(j))) {
        return true;
      }
    }

    return false;
  }

  /**
   * Match experience level
   */
  private matchExperience(job: JobPosting, resume: Resume): boolean {
    if (!resume.experience_years) return true; // Can't determine, assume match

    const desc = job.description.toLowerCase();

    // Extract required years from job
    const yearsMatches = [
      desc.match(/(\d+)\+?\s*years?/i),
      desc.match(/minimum\s+of\s+(\d+)\s*years?/i),
      desc.match(/at\s+least\s+(\d+)\s*years?/i),
    ];

    for (const match of yearsMatches) {
      if (match) {
        const required = parseInt(match[1]);
        if (resume.experience_years >= required) {
          return true;
        }
      }
    }

    // If no years specified, check seniority level
    if (desc.includes('senior') && resume.experience_years >= 5) return true;
    if (desc.includes('lead') && resume.experience_years >= 7) return true;
    if (desc.includes('principal') && resume.experience_years >= 10) return true;
    if (desc.includes('director') && resume.experience_years >= 10) return true;
    if (desc.includes('junior') || desc.includes('entry level')) return false; // Overqualified

    // Default: assume match if we can't determine
    return true;
  }

  /**
   * Match location preferences
   */
  private matchLocation(job: JobPosting, resume: Resume): boolean {
    // If resume prefers remote and job is remote, match
    if (resume.remote_preference && job.locationTypes?.includes('remote')) {
      return true;
    }

    // If job is remote, it's generally flexible
    if (job.locationTypes?.includes('remote')) {
      return true;
    }

    // Default: assume match
    return true;
  }

  /**
   * Calculate bonus points
   */
  private calculateBonusPoints(job: JobPosting, resume: Resume): number {
    let bonus = 0;

    const desc = job.description.toLowerCase();
    const resumeContent = resume.raw_content?.toLowerCase() || '';

    // Salary bonus (if competitive)
    if (job.salary && job.salary.min && job.salary.min >= 120000) {
      bonus += 5;
    }

    // Remote work bonus (if preferred)
    if (resume.remote_preference && job.locationTypes?.includes('remote')) {
      bonus += 5;
    }

    // Company keywords (startups, tech companies, etc.)
    if (desc.includes('startup') || desc.includes('venture backed')) {
      bonus += 2;
    }

    // Benefits keywords
    if (desc.includes('equity') || desc.includes('stock options')) {
      bonus += 2;
    }

    // Modern tech stack
    if (desc.includes('modern') || desc.includes('cutting edge')) {
      bonus += 2;
    }

    return Math.min(20, bonus); // Cap at 20%
  }
}

// CLI usage
if (import.meta.main) {
  console.log('JobScorer - Test mode\n');

  const scorer = new JobScorer();

  // Test job
  const testJob: JobPosting = {
    id: 'test-1',
    title: 'Senior Cybersecurity Engineer',
    company: 'Test Corp',
    location: 'Remote',
    locationTypes: ['remote'],
    description: `
      We're looking for a Senior Cybersecurity Engineer with 5+ years of experience.

      Required skills:
      - Penetration testing and vulnerability assessment
      - Python, Bash scripting
      - AWS security, Docker, Kubernetes
      - NIST, ISO 27001 compliance
      - Incident response and threat intelligence

      Nice to have:
      - Red team experience
      - Bug bounty participation
      - Security tool development
    `,
    url: 'https://example.com/job/test-1',
    datePosted: new Date().toISOString(),
    source: 'test',
    scraped_at: new Date().toISOString(),
    salary: {
      min: 140000,
      max: 180000,
      currency: 'USD',
      period: 'year',
    },
  };

  const score = scorer.scoreJob(testJob);

  console.log('Job:', testJob.title);
  console.log('Score:', score.score, '/100');
  console.log('Recommendation:', score.recommendation);
  console.log('\nMatched Skills:', score.matchedSkills.join(', '));
  console.log('Missing Skills:', score.missingSkills.join(', '));
  console.log('Experience Match:', score.experienceMatch ? 'Yes' : 'No');
  console.log('Location Match:', score.locationMatch ? 'Yes' : 'No');
}
