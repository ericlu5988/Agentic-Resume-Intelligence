#!/usr/bin/env python3
import argparse
import json
import sys
import os
import random
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

class JobDiscovery:
    def __init__(self, resume_path=None, delay=3000):
        self.resume_path = resume_path
        self.delay = delay
        self.resume_data = self._load_resume(resume_path) if resume_path else None

    def _load_resume(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self._parse_resume(content)
        except Exception as e:
            print(f"Error loading resume: {e}", file=sys.stderr)
            return None

    def _parse_resume(self, content):
        # Basic parsing for scoring
        skills = []
        import re
        skill_patterns = [
            r"(?:Skills?|Technologies?|Tools?|Expertise):\s*([^
]+)",
            r"(?:Proficient in|Experience with):\s*([^
]+)"
        ]
        for pattern in skill_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for m in matches:
                skills.extend([s.strip().lower() for s in re.split(r'[,;•|]', m)])
        
        years_match = re.search(r"(\d+)\+?\s*years?", content, re.IGNORECASE)
        years = int(years_match.group(1)) if years_match else 0
        
        return {
            "skills": list(set(skills)),
            "experience_years": years,
            "raw": content.lower()
        }

    def search_hiring_cafe(self, query, days=14, limit=10):
        results = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            # Build search URL
            search_state = {
                "searchQuery": query,
                "dateFetchedPastNDays": days
            }
            import urllib.parse
            encoded = urllib.parse.quote(json.dumps(search_state))
            url = f"https://hiring.cafe/?searchState={encoded}"
            
            print(f"Searching: {url}", file=sys.stderr)
            page.goto(url, wait_until="networkidle")
            time.sleep(5) # Wait for React hydration
            
            # Collect job links
            links = page.eval_on_selector_all('a[href*="/viewjob/"]', "elements => elements.map(e => e.href)")
            links = list(set(links))[:limit]
            
            print(f"Found {len(links)} jobs. Extracting details...", file=sys.stderr)
            
            for link in links:
                try:
                    page.goto(link, wait_until="networkidle")
                    time.sleep(2)
                    
                    job_data = page.evaluate("""() => {
                        const title = document.querySelector('h1, h2')?.textContent?.trim() || '';
                        const desc = document.querySelector('article, main, [class*="description" i]')?.textContent?.trim() || '';
                        const company = document.querySelector('[class*="company" i]')?.textContent?.trim() || '';
                        const location = document.querySelector('[class*="location" i]')?.textContent?.trim() || '';
                        return { title, description: desc, company, location };
                    }""")
                    
                    if job_data['title'] and job_data['description']:
                        job_data['url'] = link
                        if self.resume_data:
                            job_data['match_score'] = self._score_job(job_data)
                        results.append(job_data)
                    
                    time.sleep(random.uniform(self.delay/1000, (self.delay*1.3)/1000))
                except Exception as e:
                    print(f"Error extracting {link}: {e}", file=sys.stderr)
            
            browser.close()
        return results

    def _score_job(self, job):
        if not self.resume_data:
            return 0
        
        score = 0
        desc = job['description'].lower()
        
        # 1. Skills Match (40%)
        # Identify "required" skills in job desc (heuristic)
        # For simplicity, we'll just check overlap
        job_skills = []
        keywords = ["python", "aws", "security", "linux", "docker", "kubernetes", "typescript", "node"]
        for k in keywords:
            if k in desc:
                job_skills.append(k)
        
        matched = [s for s in job_skills if s in self.resume_data['skills']]
        if job_skills:
            score += (len(matched) / len(job_skills)) * 40
            
        # 2. Experience Match (25%)
        import re
        years_match = re.search(r"(\d+)\+?\s*years?", desc)
        if years_match:
            required = int(years_match.group(1))
            if self.resume_data['experience_years'] >= required:
                score += 25
        else:
            score += 20 # Assume partial match if unspecified
            
        # 3. Location/Remote (15%)
        if "remote" in desc or "remote" in job['location'].lower():
            score += 15
            
        # 4. Bonus (20%)
        if "startup" in desc: score += 5
        if "equity" in desc: score += 5
        
        return min(100, round(score))

def main():
    parser = argparse.ArgumentParser(description="ARI Job Discovery Tool")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--resume", help="Path to resume JSON or TeX (converted to text)")
    parser.add_argument("--days", type=int, default=14, help="Days back")
    parser.add_argument("--limit", type=int, default=5, help="Limit results")
    args = parser.parse_args()

    discovery = JobDiscovery(resume_path=args.resume)
    results = discovery.search_hiring_cafe(args.query, days=args.days, limit=args.limit)
    
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
