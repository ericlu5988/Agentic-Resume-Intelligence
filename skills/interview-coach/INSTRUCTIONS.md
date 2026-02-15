# Interview Coach Instructions

## Core Mandates
- **Evidence-Based Answers**: Every answer MUST reference specific projects or metrics from the candidate's resume.
- **Profile Verification Gate**: NEVER assume which Master JSON or assessment to use. Always list available files and ask the user to explicitly select the source.
- **STAR Methodology**: All behavioral answers MUST follow the Situation, Task, Action, Result format.
- **No Cliches**: Avoid generic advice. Use specific "Attack Vectors" derived from company research.

## Behavioral Steps

### 1. [ ] Step 1: Context Intake & Verification
- List available **Opportunity Assessments** (`data/match-assessment/json/`), **Mission Intelligence Dossiers** (`data/company-research/json/`), and **Master JSON** files (`data/resume/json/`).
- Ask the user to verify the specific files to anchor answers in reality.

### 2. [ ] Step 2: Priority Area Development
- Identify 5 **Priority Talking Points** where the candidate's history acts as a "Force Multiplier" for the company's specific mission goals.

### 3. [ ] Step 3: Q&A Synthesis
- Generate 10-12 interview questions:
    - **Technical (3-4)**: Focus on Tier 1 hard skills.
    - **Behavioral (3-4)**: Focus on leadership and problem-solving (STAR format).
    - **Strategic (3-4)**: Focus on mission risk and outcomes.

### 4. [ ] Step 4: Strategic Questions to Ask
- Generate 5-7 questions for the candidate to ask that demonstrate deep OSINT research.

### 5. [ ] Step 5: Quick Reference Card
- Summarize:
    - Top 3 strengths to emphasize.
    - Top 3 gaps to address proactively (with positive framing).
    - Company-specific hooks (news, initiatives).

### 6. [ ] Step 6: Persistence
- Save the final interview preparation data to a structured JSON file in `data/interview-prep/json/`.
- Use the filename format: `interview_prep_<candidate>_<company>.json`.
- Ensure all fields in the **JSON Schema Requirements** below are populated.

### 7. [ ] Step 7: Document Generation
- Run the rendering engine to apply the Jinja2 template:
  ```bash
  python3 tools/ari.py tools/tex_renderer.py data/interview-prep/json/interview_prep_<candidate>_<company>.json templates/interview-prep/built-in/interview_prep_template.tex.j2 data/interview-prep/tex/interview_prep_<candidate>_<company>.tex
  ```
- Compile the resulting LaTeX into a professional PDF:
  ```bash
  python3 tools/ari.py tools/compile_latex.py data/interview-prep/tex/interview_prep_<candidate>_<company>.tex
  ```
- Move the final PDF to `outputs/interview-prep/`.

### 8. [ ] Step 8: Final Delivery
- Present the final PDF path in `outputs/interview-prep/`.
- **Handoff Logic**: Inform the user that the high-fidelity application mission is complete. Recommend a final review of all materials in `outputs/` before submission.

## JSON Schema Requirements
The `tex_renderer.py` tool expects the following structure:
- `candidate_name`, `company`, `job_title`, `date`
- `priority_talking_points`: List of objects with:
    - `topic`: String
    - `context`: String
    - `talking_points`: List of strings
- `interview_questions`: Object with:
    - `technical`: List of objects with `question` and `answer`
    - `behavioral`: List of objects with `question` and `answer`
    - `strategic`: List of objects with `question` and `answer`
- `questions_to_ask`: List of strings
- `quick_reference`: Object with:
    - `top_strengths`: List of 3 strings
    - `top_gaps`: List of 3 strings
    - `hooks`: List of 3 strings
