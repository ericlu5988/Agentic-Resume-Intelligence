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

## File Structure

```
imports/            # Staging area for raw resumes
data/json/          # [Ignored] Master JSON Sources
data/latex/         # [Ignored] Generated TeX files
skills/             # Packaged capabilities (Metadata + Instructions)
tools/              # Python scripts for deterministic execution
templates/built-in/ # Core LaTeX Blueprints (default, minimalist, federal)
templates/          # Bespoke/Custom LaTeX templates
outputs/resume/     # [Ignored] Final PDF Resumes
outputs/dossiers/   # [Ignored] Strategic dossiers
.tmp/               # [Ignored] Temporary artifacts
```

## How to Operate
- **Initialize Workspace**: Run `python3 tools/setup.py` on startup to ensure directories are present.
- **Activate Skills**: Ensure the relevant skill is enabled/loaded before proceeding.
- **Fail Gracefully**: If a tool fails, read the error, fix the input or the tool, and retry.
- **Debug Proactively**: Use output logs or debug statements during iterative development.