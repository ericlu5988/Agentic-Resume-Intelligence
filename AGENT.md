# Agent Standard Operating Procedures (SOP)

You are operating within the **SAT Architecture** (Skills, Agents, Tools). Refer to **ARCHITECTURE.md** for the deep design philosophy, development standards, and the "DNA" of the system.

## Core Operational Principles

1.  **Planning Protocol (The PLAN: Rule)**: For any non-trivial task, you MUST present a structured plan before execution. The plan should include:
    - **Objective**: What is the goal?
    - **Affected Files**: Which files will be read or modified?
    - **Steps**: A markdown checklist `[ ]`.
    - **Sync Step**: A final step to run `python3 tools/setup.py`.
    - **Verification**: How will we know it worked?
    Wait for explicit user approval before acting.
2.  **Stateful Checklist Mandate**: Upon activating a skill or starting a plan, you MUST:
    - Extract all steps into a markdown checklist `[ ]`.
    - Output this checklist at the start of the turn.
    - Mark steps as `[x]` as they are completed.
3.  **Standard Compliance**: Before refactoring or creating skills/tools, you MUST read `ARCHITECTURE.md` to ensure you are following the latest design patterns (Checklist Rule, Python-First, Structural Hierarchy).
4.  **Template Selection Gate**: During import workflows, you must present available templates and recommend one before proceeding to generation.
5.  **Source of Truth**: The `data/json/` directory contains the immutable JSON baseline from the initial import. However, the system treats `.tex` files in `data/latex/` as the **Living Master**. Tailoring/Targeting MUST act directly on these LaTeX files to preserve manual user customizations.
6.  **Schema Governance (The Guideline Rule)**: When the user requests a **bespoke (custom) template**, or when mapping novel resume sections, you MUST consult the `rules/_core/master-resume-schema.md` reference guideline. This ensures data consistency and structural extensibility across all custom outputs.
7.  **Intelligence Density (The "No Terse" Rule)**: In all career intelligence gathering, high-level summaries are forbidden. You MUST provide maximum possible detail, citing sources using IEEE Standard [1]. Every bullet point must contain granular metrics ($ values, headcount) or verbatim leadership quotes.
8.  **Surgical Tailoring (The Sprinkle Rule)**: When targeting resumes, you MUST preserve at least 90% of the original Living Master text. Use "Discovery Gates" to ask the user for missing information rather than fabricating or skipping critical requirements.
9.  **Security Mandate**: All proposed code changes and new tool/skill implementations MUST be cross-referenced with the security rules in `rules/_core/` and `rules/languages/`. You MUST refuse to generate or execute code that violates `strict` security rules.

## File Structure

```
imports/            # Staging area for raw resumes
data/json/          # [Ignored] Master JSON Sources
data/latex/         # [Ignored] Generated TeX files
rules/              # [NEW] Security governance framework (OWASP, AI, RAG)
skills/             # Packaged capabilities (Metadata + Instructions)
tools/              # Python scripts for deterministic execution
templates/built-in/ # Core LaTeX Blueprints (default, minimalist, federal, dossier, cover_letter)
templates/          # Bespoke/Custom LaTeX templates
outputs/resume/     # [Ignored] Final PDF Resumes
outputs/dossiers/   # [Ignored] Strategic dossiers
.tmp/               # [Ignored] Temporary artifacts
```

## Core Capabilities
- **Job Discovery**: Use `python3 tools/ari.py tools/job_discovery.py` to search and score opportunities.
- **Career Analysis**: The `career` skill handles the full 5-phase application lifecycle.
- **Master Digitization**: The `resume-importer` converts PDF/DOCX to LaTeX.
- **Surgical Tailoring**: The `resume-tailor-pro` targets specific jobs.


## How to Operate
- **Initialize Workspace**: Run `python3 tools/setup.py` on startup to ensure directories are present.
- **Activate Skills**: Ensure the relevant skill is enabled/loaded before proceeding.
- **Fail Gracefully**: If a tool fails, read the error, fix the input or the tool, and retry.
- **Debug Proactively**: Use output logs or debug statements during iterative development.