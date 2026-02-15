# Opportunity Evaluator Instructions

## Core Mandates
- **Intelligence Density (No Terse Rule)**: High-level summaries are forbidden. Bullet points must contain granular metrics ($ values, headcount) or specific technical DNA (e.g., mention specific C2 frameworks or evasion techniques).
- **Strategic Bridging**: When a gap is identified, do not just list it. Provide a mitigation strategy that bridges the gap using existing experience (e.g., "Space systems share design parallels with Navy weapon systems").
- **GO/NO-GO Gate**: If the score is < 60%, you MUST recommend stopping and explain the gaps.
- **Discovery Gate**: If a critical Tier 1 requirement is not found in the resume, you **MUST** ask the user for relevant experience before concluding.
- **Zero-Fabrication**: Map only documented or user-confirmed experience.

## Behavioral Steps

### 1. [ ] Step 1: Target Acquisition
- Get the **Job Description (JD)** text or URL.
- Select the **Master JSON** from `data/json/` to use as the baseline.

### 2. [ ] Step 2: Requirement Extraction
- Parse the JD and categorize requirements:
    - **Tier 1 (Hard)**: Essential certifications, years of experience, core technologies.
    - **Tier 2 (Preferred)**: Bonus skills and nice-to-haves.

### 3. [ ] Step 3: Weighted Scoring
Calculate the match score using the following weights (0-100 integers):
- **Required Skills (40%)**: % of Tier 1 skills found in resume.
- **Experience Level (25%)**: Years and seniority alignment.
- **Nice-to-Have (20%)**: % of Tier 2 skills found in resume.
- **Industry Match (15%)**: Sector familiarity.

### 4. [ ] Step 4: Red Flag Verification
Check for auto-reject triggers:
- Required certification missing?
- 5+ years below experience requirement?
- 0% technology stack overlap?
- Unwanted relocation required?

### 5. [ ] Step 5: The Discovery Gate
- If critical Tier 1 requirements are missing, ask the user: "The job requires X, but your resume doesn't mention it. Do you have experience with X?"
- Update the score based on the user's response.

### 6. [ ] Step 6: Fit Report
- Present the final score and a **GO/NO-GO** decision.
- Provide a granular gap analysis with **Strategic Bridging**.
- **Handoff Logic**: If GO, instruct the user to trigger the `intel-officer` skill for deep reconnaissance.

### 7. [ ] Step 7: Persistence
- Save the final assessment data to a structured JSON file in `outputs/`.
- Use the filename format: `match_assessment_<candidate>_<company>.json`.
- Ensure all fields in the **JSON Schema Requirements** below are populated.

### 8. [ ] Step 8: Document Generation
- Run the rendering engine to apply the Jinja2 template:
  ```bash
  python3 tools/tex_renderer.py outputs/match_assessment_<candidate>_<company>.json templates/assessments/built-in/match_assessment.tex.j2 data/latex/match_assessment_<candidate>_<company>.tex
  ```
- Compile the resulting LaTeX into a professional PDF:
  ```bash
  python3 tools/ari.py tools/compile_latex.py data/latex/match_assessment_<candidate>_<company>.tex
  ```
- Move the final PDF to `outputs/dossiers/`.

### 9. [ ] Step 9: Proofreading & Validation
- Open the generated PDF and verify:
    - Weighted Scoring Matrix math is correct.
    - Content meets "Intelligence Density" standards.
    - Formatting is professional and free of LaTeX artifacts.

## JSON Schema Requirements
The `render_assessment.py` tool expects the following structure:
- `candidate`, `job_title`, `company`, `assessment_date`
- `overall_score` (float 0-100)
- `decision` ("GO" or "NO-GO")
- `scoring_breakdown`: Object containing `required_skills`, `experience_level`, `nice_to_have`, `industry_match`.
    - Each MUST have `weight` (int 0-100), `score` (int 0-100), and `details` (string).
- `strengths`: A list of strings. **Pattern: [Fact] -- [Strategic Impact]**. (e.g., "MS CS 4.0 GPA -- Signals extreme technical depth and theoretical mastery.")
- `gaps`: A list of objects with `area`, `impact`, and `mitigation`.
- `red_flags`: Object with:
    - `certification_gap`: "CLEAR" or "FLAG" with reason.
    - `experience_gap`: "CLEAR" or "FLAG" with reason.
    - `tech_stack_mismatch`: "CLEAR" or "FLAG" with reason.
    - `location_conflict`: "CLEAR", "NOTED", or "FLAG" with reason.
- `priority_emphasis_areas`: A list of 3-5 tactical areas the candidate should focus on in their cover letter/interview.
- `strategic_recommendation`: A paragraph-style string.
