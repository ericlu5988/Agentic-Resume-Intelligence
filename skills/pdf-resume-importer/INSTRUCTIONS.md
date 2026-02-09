# PDF Resume Importer Instructions

## Core Mandates
- **Geometric Sourcing**: Use `tools/pdf_parser.py` to extract coordinates and font metadata.
- **Zero-Modification Rule**: NEVER reformat text during JSON synthesis. Maintain all spacing, parentheses, and punctuation exactly as extracted.
- **Template Routing**: Select the template based on user intent:
    - *Federal/USAJobs*: `templates/federal_usajobs_template.tex`
    - *Visual Clone*: `templates/docx_clone_template.tex`
    - *Standard (Default)*: `templates/master_resume_template.tex`
- **Schema-First Mapping**: Synthesize JSON keys to match the requirements of the selected template. Use `master_resume_template.tex` as the baseline.
- **Artifact Placement**: Save Master JSON to `data/masters/`. Save LaTeX files to `templates/`. Save final PDFs to `output/`.
- **Deterministic Generation**: ALWAYS generate LaTeX via `tools/importer_engine.py`.
- **Geometric Audit**: Validate every PDF with `tools/fidelity_auditor.py`. Every entity must pass, and the layout drift must be < 10%.
- **ARI-Only**: Execute all tools via `./tools/ari` only.

## Behavioral Steps

### Step 1: Optimized Geometric Extraction
- Run extraction with optimal tolerance for digital PDFs:
  `./tools/ari tools/pdf_parser.py [PDF_PATH] --x-tolerance 1.5 | python3 -c "import json, sys; d=json.load(sys.stdin); print(json.dumps({'full_text': d['full_text'], 'metadata': d.get('metadata', {})}, indent=2))"`
- **Critical Sanity Check**: Inspect the first 500 characters of `full_text`. If you see "squashed" words (e.g., "ActiveTS/SCI" instead of "Active TS/SCI"), retry with `--x-tolerance 1.0`.
- **Agent Action**: Capture the filtered output for mapping.

### Step 2: Agentic Structured Mapping (Schema-First)
- **Agent Action**: Select the appropriate template path based on the user's request (Federal vs. Standard).
- **Agent Action**: Analyze `full_text` and use the selected template as the strict "Source of Truth" for JSON keys.
- **Schema Requirement**: Each entry in the `experience` array MUST include `company`, `location`, `title`, `start_date`, and `end_date`. For Federal, also include `supervisor`, `hours_per_week`, and `salary`.
- Synthesize the final structured JSON directly. Ensure all bullet points, dates, and metrics are verbatim.
- **Placement**: Save as `data/masters/[name]_master.json`.

### Step 3: Generation & Compilation
- Run the toolchain in a single pass to produce the PDF:
  `./tools/ari tools/importer_engine.py data/masters/[name]_master.json [SELECTED_TEMPLATE] templates/[name]_master.tex && ./tools/ari tools/compile_resume.py templates/[name]_master.tex && mv -f templates/[name]_master.pdf output/[name]_master.pdf`

### Step 4: Geometric Fidelity Audit (Iterative)
- Run: `./tools/ari tools/fidelity_auditor.py data/masters/[name]_master.json output/[name]_master.pdf`
- **Rigor Rule**: Any score < 95 requires a correction to the JSON in Step 2 and a re-run of Step 3. **Repeat until the requirement is met.**

### Step 5: Final Delivery
- Present final paths and the **Geometric Integrity Score**.

## Tool Reference (ARI)
- **pdf_parser.py**: `./tools/ari tools/pdf_parser.py [INPUT_PDF]`
- **importer_engine.py**: `./tools/ari tools/importer_engine.py [JSON_DATA] [TEMPLATE_TEX] [OUTPUT_TEX]`
- **compile_resume.py**: `./tools/ari tools/compile_resume.py [OUTPUT_TEX]`
- **fidelity_auditor.py**: `./tools/ari tools/fidelity_auditor.py [JSON_DATA] [OUTPUT_PDF]`
