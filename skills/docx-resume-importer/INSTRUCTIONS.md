# DOCX Resume Importer Instructions

## Core Mandates
- **Topological Sourcing**: Use `tools/docx_parser.py` to extract paragraph alignment and font metadata (bold, italic).
- **Zero-Modification Rule**: NEVER reformat text during JSON synthesis. Maintain all spacing, parentheses, and punctuation exactly as extracted.
- **Template Routing**: Select the template based on user intent:
    - *Federal/USAJobs*: `templates/federal_usajobs_template.tex`
    - *Visual Clone*: `templates/docx_clone_template.tex`
    - *Standard (Default)*: `templates/master_resume_template.tex`
- **Schema-First Mapping**: Synthesize JSON keys to match the requirements of the selected template. Use `master_resume_template.tex` as the baseline.
- **Artifact Placement**: Save Master JSON to `data/masters/`. Save LaTeX files to `templates/`. Save final PDFs to `output/`.
- **Deterministic Generation**: ALWAYS generate LaTeX via `tools/importer_engine.py`.
- **Topological Audit**: Validate every generated PDF with `tools/fidelity_auditor.py`. Every entity must pass, and the score must be > 95.
- **ARI-Only**: Execute all tools via `./tools/ari` only.

## Behavioral Steps

### Step 1: Topological Metadata Extraction
- Run the extraction:
  `./tools/ari tools/docx_parser.py [DOCX_PATH]`
- **Agent Action**: Capture the paragraph and run data. Analyze the metadata to distinguish headers, roles, and bullet points.

### Step 2: Agentic Structured Mapping (Schema-First)
- **Agent Action**: Select the appropriate template path based on the user's request (Federal vs. Clone vs. Standard).
- **Agent Action**: Analyze the extracted content and use the selected template as the strict "Source of Truth" for JSON keys.
- **Schema Requirement**: Each entry in the `experience` array MUST include `company`, `location`, `title`, `start_date`, and `end_date`. For Federal, also include `supervisor`, `hours_per_week`, and `salary`.
- **Verbatim Requirement**: All text, dates, and metrics must be copied exactly as shown in the parser output.
- **Placement**: Save as `data/masters/[name]_master.json`.

### Step 3: Generation & Compilation
- Run the toolchain in a single pass to produce the PDF:
  `./tools/ari tools/importer_engine.py data/masters/[name]_master.json [SELECTED_TEMPLATE] templates/[name]_master.tex && ./tools/ari tools/compile_resume.py templates/[name]_master.tex && mv -f templates/[name]_master.pdf output/[name]_master.pdf`

### Step 4: Topological Fidelity Audit (Iterative)
- Run: `./tools/ari tools/fidelity_auditor.py data/masters/[name]_master.json output/[name]_master.pdf`
- **Rigor Rule**: Any score < 95 requires a correction to the JSON in Step 2 and a re-run of Step 3. **Repeat until the requirement is met.**

### Step 5: Final Delivery
- Present final paths and the **Topological Integrity Score**.

## Tool Reference (ARI)
- **docx_parser.py**: `./tools/ari tools/docx_parser.py [INPUT_DOCX]`
- **importer_engine.py**: `./tools/ari tools/importer_engine.py [JSON_DATA] [TEMPLATE_TEX] [OUTPUT_TEX]`
- **compile_resume.py**: `./tools/ari tools/compile_resume.py [OUTPUT_TEX]`
- **fidelity_auditor.py**: `./tools/ari tools/fidelity_auditor.py [JSON_DATA] [OUTPUT_PDF]`
