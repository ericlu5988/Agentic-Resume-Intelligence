# Gemini CLI Instructions

Refer to **AGENT.md** for the core SAT Architecture, file structure, and project-wide operational logic.

## Gemini-Specific Operations



### 1. Planning & Execution

- **The PLAN: Protocol**: When the user requests a plan or starts a prompt with `PLAN:`, you must provide a detailed strategy following the **Planning Protocol** and **Stateful Checklist Mandate** in `AGENT.md`.

- **CLI Warning**: DO NOT use `/plan` (it is a reserved Gemini CLI command). Always use `PLAN:` or natural language.

- **Approval**: NEVER execute multi-step modifications without a "Proceed" or "Approved" from the user.





### 2. Skill Management & Bootstrapping



Before starting, ensure your workspace and skills are initialized:

- **Initialization**: Run `python3 tools/setup.py --gemini`. This creates necessary directories and syncs skills to `.gemini/skills/`.

- **Reloading**: Use `/skills reload` after initialization to update the agent's internal state.

- **Enabling**: Use `/skills enable <skill-name>` to activate a specific capability.





### 2. Coordination

- Gemini will autonomously activate skills based on natural language triggers.

- Always check `tools/` before building anything new.

- Use `python3 tools/ari.py [script] [args]` for all tool executions.
