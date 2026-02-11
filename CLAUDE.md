# Claude Code Instructions

Refer to **AGENT.md** for the core SAT Architecture, file structure, and project-wide operational logic.

## Claude-Specific Operations

### 1. Planning & Execution
- **Planning-First**: Adhere strictly to the **Planning Protocol** in `AGENT.md`. For any request that isn't a simple question, provide a plan and wait for approval.

### 2. Workspace Initialization
- **Setup**: Run `python3 tools/setup.py` on startup to ensure `imports/`, `data/masters/`, and `output/` directories are present.

### 2. Skill Utilization
- Claude treats skills as markdown files in the `skills/` directory.
- You must manually read the `SKILL.md` and `INSTRUCTIONS.md` for the relevant skill when a trigger is matched.
- Strictly adhere to the procedures defined in the `INSTRUCTIONS.md`.

### 2. Tool Execution
- Always use the `./tools/ari` wrapper for executing any script in the `tools/` directory to ensure the Docker environment is utilized.
- Follow the "Understand -> Plan -> Implement -> Verify" workflow.