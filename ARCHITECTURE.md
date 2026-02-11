# System Architecture & Design Philosophy

This document defines the core "DNA" of the **Agentic Resume Intelligence** system. All future development, refactoring, and skill creation MUST adhere to these standards to ensure system integrity and cross-platform reliability.

## 1. The SAT Architecture
The system is built on the **SAT (Skills, Agents, Tools)** framework, which enforces a strict separation between probabilistic reasoning and deterministic execution.

- **Skills (The Instructions)**: Domain-specific SOPs (Standard Operating Procedures). They define *how* a task should be approached but do not perform the execution themselves.
- **Agents (The Decision-Maker)**: The AI (Gemini, Claude, etc.) that interprets user intent and orchestrates the skills and tools.
- **Tools (The Execution)**: Deterministic Python scripts that perform heavy lifting. Tools are environment-agnostic and logic-pure.

## 2. Core Philosophies

### Fidelity-First
The primary goal is 100% visual and textual fidelity. We prioritize maintaining the user's original intent over "AI-driven improvements" that might hallucinate experience or break formatting.

### The "Sprinkle" Rule
When tailoring a resume, the system is **additive**. We maintain 90% of the original narrative, only "sprinkling" in high-impact keywords or metrics derived from the Job Description.

### Agent-Led Mapping (Context over Rigidity)
We avoid building rigid "classification" scripts for resume data. Instead, tools provide **Rich Raw Data** (text + metadata like bolding/alignment), and the **Agent** uses its contextual intelligence to map that data into the schema. This ensures unique resume sections are never lost.

## 3. Development Standards

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
