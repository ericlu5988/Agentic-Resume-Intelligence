# Agent Instructions

You're working inside the **SAT Architecture** (Skills, Agents, Tools). This architecture separates concerns so that probabilistic AI handles reasoning while deterministic code handles execution.

## The SAT Architecture

**Layer 1: Skills (The Instructions)**
- Specialized instruction sets stored in `skills/`
- Each skill is defined by a `SKILL.md` (metadata/triggers) and `INSTRUCTIONS.md` (procedure).
- Written in plain language to define high-fidelity SOPs.

**Layer 2: Agents (The Decision-Maker)**
- This is your role. You're responsible for intelligent coordination.
- Use `/skills list` and `/skills enable <skill-name>` to load capabilities.
- Gemini will autonomously activate the skill based on the user's natural language request.
- You connect intent to execution without trying to do everything yourself.

**Layer 3: Tools (The Execution)**
- Python scripts in `tools/` that do the actual work (e.g., LaTeX compilation).
- These scripts are consistent, testable, and fast.

**Why this matters:** When AI tries to handle every step directly, accuracy drops fast. By offloading execution to deterministic skills and tools, you stay focused on orchestration and decision-making where you excel.

## How to Operate

**1. Enable and Trigger Skills**
Before starting a complex task, ensure the relevant skill is enabled. Act on the user's request by following the expert instructions provided in the skill's directory.

**2. Look for existing tools first**
Before building anything new, check `tools/` based on what your instructions require. Only create new scripts when nothing exists for that task.

**3. Learn and adapt when things fail**
When you hit an error:
- Read the full error message and trace.
- Fix the tool/instruction and retest.
- Document what you learned in the instruction set.

## File Structure

**Directory layout:**
```
data/masters/   # JSON Sources of Truth (Protected Baseline)
output/         # Strategy Dossiers & Final PDF Resumes
skills/         # Packaged capabilities (Metadata + Instructions)
tools/          # Python scripts for deterministic execution
templates/      # LaTeX Resume Blueprints (.tex and .cls)
.env            # API keys and secrets
```

**Core principle:** `data/masters/` contains the immutable JSON baseline. `templates/` contains the presentation logic. All versioned artifacts live in `output/`.

## Bottom Line

You sit between what the user wants (skills) and what actually gets done (tools). Your job is to read instructions, make smart decisions, call the right tools, recover from errors, and keep improving the system.

Stay pragmatic. Stay reliable. Keep learning.
