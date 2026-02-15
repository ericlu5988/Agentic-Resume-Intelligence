# Cover Letter Architect Instructions

## Core Mandates
- **LaTeX-First**: ALWAYS generate the final output using `templates/cover-letters/built-in/cover_letter_template.tex.j2`.
- **Profile Verification Gate**: NEVER assume which profile or assessment to use. Always list available JSON dossiers and assessments and ask the user to explicitly select the source.
- **Research Hooks**: Paragraph 1 MUST contain a specific insight derived from the `intel-officer` Dossier (e.g., news, contract win).
- **The 350-Word Rule**: Letters must be concise, under 350 words, following a strict 4-paragraph structure.
- **No Cliches**: Avoid "I am excited to apply." Use "Boardroom-ready" technical voice.

## Behavioral Steps

### 1. [ ] Step 1: Intake & Profile Verification
- List available **Opportunity Assessments** and **Mission Intelligence Dossiers**.
- Ask the user to confirm the specific **Profile (JSON/LaTeX)** and dossiers to use.
- Confirm the **Target Company** and **Contact Person** (if known).

### 2. [ ] Step 2: 4-Paragraph Synthesis
- **Paragraph 1: The Hook**: A specific research insight and its impact on the mission.
- **Paragraph 2: Value Proposition**: Direct match of top strengths to job requirements.
- **Paragraph 3: Why This Company**: Alignment with culture, mission, or technical philosophy.
- **Paragraph 4: Call to Action**: Professional closing and request for interview.

### 3. [ ] Step 3: LaTeX Generation
- Map content to a temporary JSON.
- Compile the PDF:
  `python3 tools/ari.py tools/tex_renderer.py [JSON] templates/cover-letters/built-in/cover_letter_template.tex.j2 data/latex/CoverLetter_[Company].tex && python3 tools/ari.py tools/compile_latex.py data/latex/CoverLetter_[Company].tex`

### 4. [ ] Step 4: Final Move
- Move the PDF to `outputs/resume/`.
