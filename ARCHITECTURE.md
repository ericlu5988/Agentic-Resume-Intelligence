# System Architecture & Design Philosophy

This document defines the core **"DNA"** of the **Agentic Resume Intelligence (ARI)** system. It serves as the immutable reference for system design, structural integrity, and security governance.

**Note**: For operational procedures, tool usage, and runtime protocols, refer to **`AGENT.md`**.

## 1. The SAT Architecture
The system is built on the **SAT (Skills, Agents, Tools)** framework, enforcing a strict separation between probabilistic reasoning and deterministic execution.

### Components
- **Skills (The Instructions)**: Passive Markdown files defining *how* a task should be approached. They contain Standard Operating Procedures (SOPs) but no executable code.
- **Agents (The Decision-Maker)**: The AI model (Gemini, Claude, etc.) operating under specialized personas (`advisor`, `researcher`, `writer`). Agents orchestrate the lifecycle by reading Skills and invoking Tools.
- **Tools (The Execution)**: Deterministic Python scripts that perform heavy lifting (parsing, rendering, compilation). Tools are logic-pure and environment-agnostic.

## 2. Core Philosophies

### The "Living Master" (LaTeX-First)
While the initial import generates a JSON "Source of Truth," the system treats the generated `.tex` file in `data/latex/` as the **Living Master**. Users are encouraged to manually perfect the layout and wording in LaTeX. Subsequent tailoring (targeting for jobs) acts directly on this LaTeX file to preserve all manual customizations.

### Fidelity-First & The "Sprinkle" Rule
We prioritize maintaining original visual/textual intent. Tailoring is additive—at least 90% of the original content must be preserved. We do not rewrite resumes; we *sprinkle* targeted keywords into them.

### Agent-Led Mapping (Context over Rigidity)
Tools provide **Rich Raw Data**. The Agent uses its contextual intelligence to map that data into the schema. We favor flexible mapping over rigid programmatic parsers.

### Schema Governance (Extensibility Guideline)
The system maintains a **Master Resume Schema** (`rules/_core/master-resume-schema.md`) which acts as the Golden Path for data structure. This ensures consistency for built-in templates and provides a blueprint for bespoke customizations.

### Intelligence Density (The "No Terse" Rule)
High-level summaries are considered a failure state. The system prioritizes data density, requiring granular metrics, cited sources (IEEE Standard), and specific technical DNA in all mission intelligence dossiers.

### Security-First Governance
Security is not an afterthought but a prerequisite. The system incorporates a robust security framework located in `rules/`. All development MUST adhere to the standards defined in `rules/_core/` (OWASP 2025, AI Security, Agent Security).

## 3. Structural Standards

### Directory Hierarchy
- **`data/json/`**: Git-ignored. Stores the immutable JSON snapshot from the initial import.
- **`data/latex/`**: Git-ignored. Stores the **Living Master** `.tex` files.
- **`rules/`**: Version-tracked. Security governance framework and rules.
- **`skills/`**: Version-tracked. Agentic capabilities and SOPs.
- **`tools/`**: Version-tracked. Deterministic cross-platform scripts.
- **`templates/resumes/built-in/`**: Version-tracked. Immutable core resume blueprints.
- **`templates/resumes/bespoke/`**: Git-ignored. Custom resume templates.
- **`templates/assessments/built-in/`**: Version-tracked. Opportunity assessment blueprints.
- **`outputs/`**: Git-ignored. Final compiled PDF artifacts.
- **`.tmp/`**: Git-ignored. Temporary processing scratchpad.

## 4. Development Standards

### Tool Standards
- **Python-First**: All new tools must be written in Python for cross-platform compatibility.
- **ARI-Wrapped**: Tools must not contain internal Docker logic. They assume they are running in a standardized environment provided by the `tools/ari.py` wrapper.
- **Logic Purity**: Tools should output structured JSON and avoid printing conversational text to stdout.

### Skill Standards
All new skills MUST include a `Behavioral Steps` section formatted as a markdown checklist `[ ]`. This allows agents to maintain state and avoid skipping steps during complex workflows.
