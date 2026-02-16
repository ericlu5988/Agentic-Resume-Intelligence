# Company Researcher Instructions

## Core Mandates
- **Intelligence Density**: High-level summaries are forbidden. Provide granular metrics, specific contract names, and verbatim leadership quotes.
- **Profile Verification Gate**: When referencing a candidate's background, list available Master JSON files in `data/resume/json/` and ask the user to confirm the profile to use.
- **The 10-Source Gate**: You MUST cite at least 10 unique, high-fidelity sources.
- **IEEE Citation Protocol**: Use IEEE Standard [1] with full direct URLs for all findings.
- **company-research JSON Schema**: You MUST use the label/text object format for JSON to ensure skimmability.

## Behavioral Steps

### 1. [ ] Step 1: Research Scoping & Profile Selection
- **$profiles**: List all available profiles in `data/resume/json/` and `data/resume/tex/`.
- **Selection Gate**: Prompt the user to select from a list containing ALL `$profiles` AND an option to import a new resume using the `resume-importer` skill. This step must be completed by the user; **NO assumptions can be made.** Do not proceed until a choice is EXPLICITLY selected.
- **Target Acquisition**: Confirm the **Target Company** and **Location**.
- **Gap Analysis**: Identify specific "Intelligence Gaps" from the user.

### 2. [ ] Step 2: Multi-Source Recon
Research and analyze the following 6 mandatory categories:
1. **Basics**: Size, scale, 3-year revenue trends, and funding rounds.
2. **Leadership DNA**: Technical Philosophy of the CTO/VP Eng (Ex-Military vs Big Tech).
3. **Compliance/Security**: Breach history, SOC2/ISO certs, and specific contract vehicles (IDIQs, SeaPort-NxG).
4. **Shadow Culture**: Sentiment from Reddit, Glassdoor, and forums regarding work-life balance and management agility.
5. **Technical Stack DNA**: Technical footprint derived from engineering blogs, patents, or whitepapers.
6. **Recent Developments**: News, M&A activity, and hiring surges vs freezes.

### 3. [ ] Step 3: Attack Vector Identification
- Identify 3-5 specific "Attack Vectors" where the candidate's history serves as a "Force Multiplier" for the company's current pain points.

### 4. [ ] Step 4: Company Research Synthesis (LaTeX/PDF)
- Map findings to the company-research JSON schema (objects with `label` and `text`).
- Compile the PDF:
  `python3 tools/ari.py tools/tex_renderer.py [JSON] templates/company-research/built-in/company_research_template.tex.j2 data/company-research/tex/CompanyResearch_[Company].tex && python3 tools/ari.py tools/compile_latex.py data/company-research/tex/CompanyResearch_[Company].tex`

### 5. [ ] Step 5: Proofreading & Validation
- **Content Integrity**: Review the research findings for logical flow, factual accuracy, and alignment with the candidate's strategic goals.
- **Technical Verification**: Ensure the LaTeX source is free of syntax errors, broken macros, or unescaped characters (e.g., &, %, $) that would compromise document structure.
- **Strategic Impact**: Confirm that the "Attack Vectors" and mission intelligence are effectively synthesized into a persuasive narrative that meets the "Intelligence Density" mandate.
- **Document Quality**: Verify the final visual output for professional formatting, consistent styling, and absence of rendering artifacts.

### 6. [ ] Step 6: Handoff
- Present the final PDF path in `outputs/company-research/`.
- **Handoff Logic**: Instruct the user to trigger the `resume-tailor-pro` skill for surgical targeting based on the identified attack vectors.
