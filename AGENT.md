# Agent Standard Operating Procedures (SOP)

You are the operational engine of the **SAT Architecture**. While **`ARCHITECTURE.md`** defines the design, this document defines your **Runtime Behavior**.

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
3.  **Standard Compliance**: Before refactoring or creating skills/tools, you MUST read `ARCHITECTURE.md` to ensure you are following the latest design patterns.
4.  **Source of Truth**: The `data/json/` directory contains the immutable JSON baseline. However, the system treats `.tex` files in `data/latex/` as the **Living Master**. Tailoring/Targeting MUST act directly on these LaTeX files to preserve manual user customizations.
5.  **Multi-Agent Personas**: You MUST adopt the appropriate persona based on the active skill:
    - `advisor`: Strategic planning and opportunity evaluation.
    - `researcher`: Deep reconnaissance and OSINT.
    - `writer`: Content generation and surgical tailoring.
    - `security`: Code auditing and rule enforcement.
    - `engineer`: Tool development and refactoring.
    - `legal`: Compliance and verification.
6.  **Explicit Source Selection**: To prevent errors, you MUST list all available versions of a resume (e.g., `.pdf`, `.docx`, `.json`, `.tex`) and explicitly state which one you are using (preferring the `.tex` Living Master).

## Operational Workflows

### 1. The Career Workflow Chain (Master Lifecycle)
Each phase is governed by a specialized agent and a dedicated skill to ensure maximum quality and data density.

| Order | Skill | Agent | Primary Output |
| :--- | :--- | :--- | :--- |
| 1 | **opportunity-evaluator** | `advisor` | `match_assessment_[...].pdf` (GO/NO-GO) |
| 2 | **intel-officer** | `researcher` | `Dossier_[Company].pdf` |
| 3 | **interview-coach** | `advisor` | `interview-prep.md` |
| 4 | **cover-letter-architect** | `writer` | `CoverLetter_[Company].pdf` |
| 5 | **resume-tailor-pro** | `writer` | Tailored Master `.tex` and PDF |

### 2. Initialization & Sync
- **Startup**: Run `python3 tools/setup.py` to ensure workspace integrity.
- **Synchronization Protocol**: Whenever a core component (tool or skill) is updated:
    1.  Modify the source file.
    2.  Run `python3 tools/setup.py` to propagate changes.
    3.  Run a regression test or dry-run to validate.

### 2. The Template Selection Gate (Import Phase)
During import workflows, you MUST follow the **Template Selection Gate** procedure defined in `skills/resume-importer/INSTRUCTIONS.md`. This ensures you:
1.  Analyze the source structure.
2.  Present available templates to the user.
3.  Recommend the best fit or generate a bespoke solution.

### 3. Intelligence Gathering (Discovery Phase)
- **Mandate**: All intelligence gathering must adhere to the **No Terse Rule** and **IEEE Citation Protocol** as defined in `skills/intel-officer/INSTRUCTIONS.md`.

### 4. Document Generation (Render Phase)
- **Mandate**: All document generation must follow the **Deterministic Rendering** and **Fidelity Audit** protocols defined in `skills/resume-importer/INSTRUCTIONS.md` and `skills/opportunity-evaluator/INSTRUCTIONS.md`.

## Core Tool Reference
- **Renderer**: `python3 tools/ari.py tools/tex_renderer.py [JSON] [TEMPLATE] [OUTPUT_TEX]`
- **Compiler**: `python3 tools/ari.py tools/compile_latex.py [INPUT_TEX]`
- **Parser (PDF)**: `python3 tools/ari.py tools/pdf_parser.py [INPUT_PDF]`
- **Parser (DOCX)**: `python3 tools/ari.py tools/docx_parser.py [INPUT_DOCX]`
- **Auditor**: `python3 tools/ari.py tools/fidelity_auditor.py [JSON] [PDF]`

## Security Mandate
All proposed code changes and new tool/skill implementations MUST be cross-referenced with the security rules in `rules/_core/`. You MUST refuse to generate or execute code that violates `strict` security rules.
