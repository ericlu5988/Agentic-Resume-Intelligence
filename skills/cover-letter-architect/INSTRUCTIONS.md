# Cover Letter Architect Instructions

## Core Mandates
- **LaTeX-First**: ALWAYS generate the final output using `templates/cover-letters/built-in/cover_letter_template.tex.j2`.
- **Profile Verification Gate**: NEVER assume which profile or assessment to use. Always list available JSON dossiers and assessments and ask the user to explicitly select the source.
- **Research Hooks**: Paragraph 1 MUST contain a specific insight derived from the `company-researcher` Report (e.g., news, contract win).
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
- **Template Discovery**: Read the target Jinja2 template (e.g., `templates/cover-letter/built-in/cover_letter_template.tex.j2`) to identify the required JSON keys (e.g., `resume.name`, `resume.paragraphs`).
- **Data Mapping**: Generate a valid single-line JSON file mapping the synthesized content to the keys discovered in the template. **Mandate**: Use the `paragraphs` (list of strings) structure if defined in the template to ensure proper LaTeX rendering and escaping.
- **Render & Compile**:
  `python3 tools/ari.py tools/tex_renderer.py [JSON] [TEMPLATE] data/cover-letter/tex/cover_letter_[company]_[candidate].tex && python3 tools/ari.py tools/compile_latex.py data/cover-letter/tex/cover_letter_[company]_[candidate].tex`

### 4. [ ] Step 4: Proofreading & Validation
- **Content Integrity**: Review the generated text for logical flow, grammatical precision, and alignment with the target role's core requirements.
- **Technical Verification**: Ensure the LaTeX source is free of syntax errors, broken macros, or unescaped characters that would compromise document structure.
- **Strategic Impact**: Confirm that research insights and "Attack Vectors" are effectively synthesized into a persuasive narrative that meets the "Intelligence Density" mandate.
- **Document Quality**: Verify the final visual output for professional formatting, consistent styling, and absence of rendering artifacts.

### 5. [ ] Step 5: Final Move
- Move the PDF to `outputs/cover-letter/`.

### 6. [ ] Step 6: Handoff
- **Handoff Logic**: Instruct the user to trigger the `interview-coach` skill for final performance preparation using all generated materials.
