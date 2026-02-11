# PDF Resume Importer Instructions

## Core Mandates
- **Geometric Sourcing**: Use `tools/pdf_parser.py` to extract coordinates and font metadata.
- **Zero-Modification Rule**: NEVER reformat text during JSON synthesis. Maintain all spacing, parentheses, and punctuation exactly as extracted.
- **Template Routing**: Use the **Template Selection Gate** to choose between:
    - *Federal/USAJobs*: `templates/built-in/federal_usajobs_template.tex`
    - *Minimalist*: `templates/built-in/minimalist_template.tex`
    - *Default*: `templates/built-in/default_template.tex`
    - *Bespoke*: Generate a custom template based on source structure.
- **Schema-First Mapping**: Synthesize JSON keys to match the requirements of the selected template.
- **Artifact Placement**: Save Master JSON to `data/json/`. Save LaTeX files to `data/latex/`. Save final PDFs to `outputs/resume/`.
- **Deterministic Generation**: ALWAYS generate LaTeX via `tools/importer_engine.py`.
- **Geometric Audit**: Validate every PDF with `tools/fidelity_auditor.py`. Every entity must pass, and the layout drift must be < 10%.
- **ARI-Only**: Execute all tools via `python3 tools/ari.py` only.
- **Stateful Checklist**: You MUST output and maintain a checklist of the Behavioral Steps below.

## Behavioral Steps

### 1. [ ] Step 1: Optimized Geometric Extraction
- **Discovery**: Check the `imports/` directory for any PDF files if the user hasn't provided a specific path.
- Run extraction with optimal tolerance for digital PDFs:
  `python3 tools/ari.py tools/pdf_parser.py [PDF_PATH] --x-tolerance 1.5 | python3 -c "import json, sys; d=json.load(sys.stdin); print(json.dumps({'full_text': d['full_text'], 'metadata': d.get('metadata', {})}, indent=2))"`
- **Critical Sanity Check**: Inspect the first 500 characters of `full_text`. If you see "squashed" words (e.g., "ActiveTS/SCI" instead of "Active TS/SCI"), retry with `--x-tolerance 1.0`.
- **Agent Action**: Capture the filtered output for mapping.

### 2. [ ] Step 2: Template Selection Gate
- **List**: Show the user all templates in `templates/built-in/` and any in `templates/`.
- **Recommend**: Analyze the extracted metadata and recommend a template (e.g., "Federal" if salary/supervisor data is found).
- **Custom Choice**: If the user asks for a bespoke template, analyze the source structure and create a new `.tex` file in `templates/`.

### 3. [ ] Step 3: Agentic Structured Mapping (Schema-First)
- **Agent Action**: Analyze `full_text` and use the selected template as the strict "Source of Truth" for JSON keys.
- **Schema Requirement**: Each entry in the `experience` array MUST include `company`, `location`, `title`, `start_date`, and `end_date`.
- Synthesize the final structured JSON directly. Ensure all bullet points, dates, and metrics are verbatim.
- **Placement**: Save as `data/json/[name]_master.json`.

### 4. [ ] Step 4: Generation & Compilation
- Run the toolchain in a single pass:
  `python3 tools/ari.py tools/importer_engine.py data/json/[name]_master.json [SELECTED_TEMPLATE] data/latex/[name]_master.tex && python3 tools/ari.py tools/compile_resume.py data/latex/[name]_master.tex && mv -f data/latex/[name]_master.pdf outputs/resume/[name]_master.pdf`

### 5. [ ] Step 5: Geometric Fidelity Audit (Iterative)
- Run: `python3 tools/ari.py tools/fidelity_auditor.py data/json/[name]_master.json outputs/resume/[name]_master.pdf`
- **Rigor Rule**: Any score < 95 requires a correction to the JSON in Step 3 and a re-run of Step 4. **Repeat until the requirement is met.**

### 6. [ ] Step 6: Final Delivery
- Present final paths and the **Geometric Integrity Score**.

## Tool Reference (ARI)
- **pdf_parser.py**: `python3 tools/ari.py tools/pdf_parser.py [INPUT_PDF]`
- **importer_engine.py**: `python3 tools/ari.py tools/importer_engine.py [JSON_DATA] [TEMPLATE_TEX] [OUTPUT_TEX]`
- **compile_resume.py**: `python3 tools/ari.py tools/compile_resume.py [OUTPUT_TEX]`
- **fidelity_auditor.py**: `python3 tools/ari.py tools/fidelity_auditor.py [JSON_DATA] [OUTPUT_PDF]`
