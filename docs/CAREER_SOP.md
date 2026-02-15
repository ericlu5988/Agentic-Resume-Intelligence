# Career Intelligence SOP (Modular Workflow)

This document defines the master workflow for the modular career capabilities. Each phase is governed by a specialized agent and a dedicated skill to ensure maximum quality and data density.

## The Workflow Chain

| Order | Skill | Agent | Primary Output |
| :--- | :--- | :--- | :--- |
| 1 | **job-scout** | `advisor` | Ranked Leads Report |
| 2 | **opportunity-evaluator** | `advisor` | `match-assessment.md` (GO/NO-GO) |
| 3 | **intel-officer** | `researcher` | `Dossier_[Company].pdf` |
| 4 | **interview-coach** | `advisor` | `interview-prep.md` |
| 5 | **cover-letter-architect** | `writer` | `CoverLetter_[Company].pdf` |
| 6 | **resume-tailor-pro** | `writer` | Tailored Master `.tex` and PDF |

## Core Principles across Modules

### 1. Intelligence Density (The "No Terse" Rule)
High-level summaries are forbidden. Every module must provide maximum possible detail, citing sources using IEEE Standard [1] with full URLs.

### 2. The Living Master (LaTeX-First)
The system treats the `.tex` files in `data/latex/` as the final source of truth. All generation modules (`architect`, `tailor`) must act directly on these files.

### 3. The Discovery Gate
If information is missing, the agent **MUST** stop and ask the user rather than skipping or fabricating.

### 4. Specialized Persona Adoption
The CLI agent will adopt the specialized persona (`advisor`, `researcher`, `writer`) defined in the `agents/` directory based on the active skill.
