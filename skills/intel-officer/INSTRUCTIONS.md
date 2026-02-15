# Intel Officer Instructions

## Core Mandates
- **Intelligence Density**: High-level summaries are forbidden. provide granular metrics, specific contract names, and verbatim leadership quotes.
- **The 10-Source Gate**: You MUST cite at least 10 unique, high-fidelity sources.
- **IEEE Citation Protocol**: Use IEEE Standard [1] with full direct URLs for all findings.
- **Dossier JSON Schema**: You MUST use the label/text object format for Dossier JSON to ensure skimmability.

## Behavioral Steps

### 1. [ ] Step 1: Intel Scoping
- Confirm the **Target Company** and **Location**.
- Identify specific "Intelligence Gaps" from the user.

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

### 4. [ ] Step 4: Dossier Synthesis (LaTeX/PDF)
- Map findings to the Dossier JSON schema (objects with `label` and `text`).
- Compile the PDF:
  `python3 tools/ari.py tools/tex_renderer.py [JSON] templates/dossiers/built-in/strategy_dossier_template.tex.j2 data/latex/Dossier_[Company].tex && python3 tools/ari.py tools/compile_latex.py data/latex/Dossier_[Company].tex`

### 5. [ ] Step 5: Handoff
- Present the final PDF path.
- **Handoff Logic**: Instruct the user to trigger the `interview-coach` skill for performance preparation.
