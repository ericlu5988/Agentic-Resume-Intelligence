# System Architecture & Design Philosophy

This document defines the core "DNA" of the **Agentic Resume Intelligence** system. All future development, refactoring, and skill creation MUST adhere to these standards to ensure system integrity and cross-platform reliability.

## 1. The SAT Architecture
The system is built on the **SAT (Skills, Agents, Tools)** framework, which enforces a strict separation between probabilistic reasoning and deterministic execution.

- **Skills (The Instructions)**: Domain-specific SOPs (Standard Operating Procedures). They define *how* a task should be approached but do not perform the execution themselves.
- **Agents (The Decision-Maker)**: The AI (Gemini, Claude, etc.) that interprets user intent and orchestrates the skills and tools.
- **Tools (The Execution)**: Deterministic Python scripts that perform heavy lifting. Tools are environment-agnostic and logic-pure.

## 2. Core Philosophies

### The "Living Master" (LaTeX-First)
While the initial import generates a JSON "Source of Truth," the system treats the generated `.tex` file in `data/latex/` as the **Living Master**. Users are encouraged to manually perfect the layout and wording in LaTeX. Subsequent tailoring (targeting for jobs) acts directly on this LaTeX file to preserve all manual customizations.

### Fidelity-First & The "Sprinkle" Rule
We prioritize maintaining original visual/textual intent. Tailoring is additive (90% original content preserved).

### Agent-Led Mapping (Context over Rigidity)
Tools provide **Rich Raw Data**. The Agent uses its contextual intelligence to map that data into the schema.

### Schema Governance (Extensibility Guideline)
The system maintains a **Master Resume Schema** (`rules/_core/master-resume-schema.md`) which acts as a reference guideline for the Agent. This is primarily used during bespoke template generation and for the topological preservation of novel resume sections via the `custom_sections` catch-all protocol.

### Intelligence Density (The "No Terse" Rule)
High-level summaries are considered a failure state. The system prioritizes data density, requiring granular metrics, cited sources, and specific technical DNA in all mission intelligence dossiers.

### Security-First & Governance
The system incorporates a robust security framework located in `rules/`. All development MUST adhere to the standards defined in `rules/_core/` (OWASP 2025, AI Security, Agent Security) and language-specific rules. Security is not an afterthought but a prerequisite for every plan.

## 3. Structural Standards

### Directory Hierarchy
- **`data/json/`**: Git-ignored. Stores the immutable JSON snapshot from the initial import.
- **`data/latex/`**: Git-ignored. Stores the **Living Master** `.tex` files (User's primary playground).
- **`rules/`**: Version-tracked. Security governance framework and rules.
- **`skills/`**: Version-tracked. Agentic capabilities and SOPs.
- **`tools/`**: Version-tracked. Deterministic cross-platform scripts.
- **`templates/built-in/`**: Version-tracked. Immutable core blueprints used for the initial digitization.
- **`templates/`**: Git-ignored (except `built-in/`). Bespoke/Custom templates.
- **`outputs/resume/`**: Git-ignored. Final compiled PDF resumes.
- **`outputs/dossiers/`**: Git-ignored. High-fidelity PDF strategy dossiers generated from the `strategy_dossier_template.tex`.
- **`.tmp/`**: Git-ignored. Temporary processing scratchpad.

## 4. The Template Selection Gate
During the import process, agents MUST implement a Selection Gate:
1. **Analyze**: Examine the source resume for structural cues (Federal keywords, Word-style formatting).
2. **Present**: List all available templates in `templates/` and `templates/built-in/`.
3. **Recommend**: Mark the recommended template with a reason.
4. **Bespoke Action**: If built-in options are insufficient, analyze unique source features and generate a new `.tex` file in `templates/` using standard LaTeX packages.

## 5. Development Standards

### Tool Standards
- **Python-First**: All new tools must be written in Python for cross-platform compatibility.
- **ARI-Wrapped**: Tools must not contain internal Docker logic. They assume they are running in a standardized environment provided by the `tools/ari.py` wrapper.
- **Logic Purity**: Tools should output structured JSON and avoid printing conversational text to stdout.

### Skill Standards (The Checklist Rule)
All new skills MUST include a `Behavioral Steps` section formatted as a markdown checklist `[ ]`. This allows agents to maintain state and avoid skipping steps during complex workflows.

## 4. Synchronization Protocol
The system follows a strict **Propagation Path**. Whenever a core component is updated, the change must be synchronized across the repository:

1. **Modify Source**: Update the tool in `tools/` or the skill in `skills/`.
2. **Initialize Workspace**: Run `python3 tools/setup.py` (or `--gemini` for Gemini users).
3. **Validate**: Run the relevant test suite or a dry-run of the affected skill.

**Requirement**: Every `PLAN:` involving file modifications MUST include a "Synchronization Step" to ensure the agent's runtime environment matches the repository source.
