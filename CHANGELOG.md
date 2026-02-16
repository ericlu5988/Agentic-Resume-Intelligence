# Changelog

All notable changes to the **Agentic Resume Intelligence** project during the February 2026 refactoring and improvement session.

## [1.3.0] - 2026-02-15

### 🧠 Core Agentic Skills Rollout
- **Mission Workflow Integration**: Formally rolled out the complete 6-step mission chain, providing specialized agents for each phase of the job application lifecycle.
- **resume-importer**: Unified PDF/DOCX geometric extraction with automated template selection and high-fidelity LaTeX generation.
- **opportunity-evaluator**: Implemented rigorous weighted scoring (40/25/20/15) and "Strategic Bridging" for gap analysis.
- **company-researcher**: Introduced OSINT-driven reconnaissance with a mandatory 10-source gate and IEEE-standard citation protocol.
- **resume-tailor-pro**: Engineered surgical, additive targeting for LaTeX masters, enforcing the 90%+ "Sprinkle Rule" for original content preservation.
- **cover-letter-architect**: Developed a research-hooked generation engine for boardroom-ready applications.
- **interview-coach**: Synthesized all mission data into priority talking points, strategic questions, and STAR-formatted preparation dossiers.

### 🧠 Methodology & Governance
- **Standardized Proofreading Methodology**: Applied a unified, high-fidelity **"Proofreading & Validation"** behavioral step across all six skills, focusing on Content Integrity, Technical Verification, Strategic Impact, and Document Quality.
- **SAT Framework Hardening**: Codified the **Skills, Agents, Tools** logic in `ARCHITECTURE.md` and `AGENT.md` to ensure strict separation of probabilistic reasoning and deterministic execution.
- **Architectural Alignment**: Evolved `intel-officer` into `company-researcher` and standardized built-in template naming conventions.

### 🛠️ System Hardening & Fidelity
- **Absolute Straight Quote Enforcement**: Systemically disabled TeX ligatures at the template level (`fontspec` update) to prevent automatic conversion of straight quotes (`'`) into smart quotes (`’`) during compilation.
- **Template Integrity Restoration**: Manually scrubbed and hardened all LaTeX templates to eliminate literal tab characters that were breaking table environments (`tabularx`).
- **Stabilized LaTeX Escaping**: Refactored `escape_latex` and `sanitize_text` in `tools/lib/utils.py` to provide a stable, non-aggressive character mapping that preserves standard LaTeX commands (e.g., `\par`, `\textwidth`) while protecting user data.
- **Automated Paragraph Normalization**: Implemented a systemic fix to automatically convert standard newlines (`\n`) in JSON sources into proper LaTeX paragraph breaks (`\par`) during rendering.
- **Unicode Scrubber**: Enhanced `sanitize_text` with Unicode escape sequences to robustly handle smart quotes, dashes, and non-breaking spaces across different environments.
- **Pre-Compilation Sanitation Gate**: Integrated an automated cleanup pass into `compile_latex.py` to identify and remove character artifacts immediately before PDF generation.

### 🧪 Showcase & Maintenance
- **Palantir Mission Showcase**: Whitelisted a complete suite of high-fidelity artifacts for the **Johnny Silverhand vs. Palantir** campaign, demonstrating high-fidelity digitization and tactical re-targeting.
- **README Revamp**: Integrated a dedicated "Mission Showcase" section linking directly to whitelisted JSON, LaTeX, and PDF deliverables.
- **Repository Hygiene**: 
    - Purged legacy `TODO` tracking from git history.
    - Deleted obsolete `intel-officer` instruction files.
    - Fixed file extension inconsistencies (standardized on `.tex.j2` for templates).

## [1.2.0] - 2026-02-14

### 🛡️ Security & Governance
- **Security Governance Framework**: Integrated `rules/` directory with standardized security rules for OWASP 2025, AI Security, and RAG operations.
- **Automated SAST Integration**: Enabled `bandit` and `semgrep` scanning within the ARI toolset.
- **Security Testing Suite**: Added `rules/tests/` to validate the structural integrity and effectiveness of security rules.

### 🛠️ Infrastructure & Hardening
- **LaTeX Search Path Resolution**: Updated `compile_latex.py` to automatically include `templates/` and `templates/built-in/` in the `TEXINPUTS` environment variable, ensuring custom `.cls` and `.sty` files are found during compilation.
- **Fidelity Auditor Schema Hardening**: Enhanced `fidelity_auditor.py` to support nested `resume` keys in source JSON, ensuring accurate experience counting and content validation for all template types.
- **Container Hardening**: Switched to the non-root `texlive` user for all Docker executions to mitigate root-escape risks.
- **Subprocess Sanitization**: Refactored `ari.py` and `compile_latex.py` to use `shutil.which()` for absolute path resolution, preventing command hijacking.
- **Jinja2 SSTI Protection**: Hardened `tex_renderer.py` with `autoescape` and custom LaTeX-safe escaping logic.
- **Path Traversal Shield**: Hardened `validate_master_path` in `lib/utils.py` to strictly prevent filesystem access outside the project root.

### 🧠 Agentic Skills
- **Universal Resume Importer**: Unified the PDF and DOCX importer skills into a single, high-fidelity `resume-importer` skill that autonomously handles hybrid sourcing and format-specific extraction logic.
- **Obsolete Skill Removal**: Deprecated and removed the standalone `pdf-resume-importer` and `docx-resume-importer` skills to reduce architectural redundancy.

## [1.1.1] - 2026-02-13

### 🏗️ Architecture & Philosophy
- **Bootstrap Mandate**: Enforced architectural alignment across all agents by requiring the reading of `AGENT.md` and `ARCHITECTURE.md` at session start.

### 🛠️ Infrastructure & Tools
- **Fidelity Auditor Optimization**: 
    - Implemented vertical-first (Y-then-X) word sorting to accurately preserve reading order in both single and multi-column layouts.
    - Enhanced matching logic with `token_set_ratio` and `partial_ratio` to robustly handle squashed or justified PDF text layers.
- **Dossier Schema Validation**: Codified the `career-strategist` dossier JSON schema to prevent downstream LaTeX compilation errors.
- **Deterministic Generation**: Enforced the use of `tex_renderer.py` for career dossiers to ensure consistent LaTeX output.

### 🧠 Agentic Skills
- **Modern Blue Template**: Added `modern_blue_template.tex.j2` to the built-in library, offering a modern, high-density layout with dynamic highlight labels.

## [1.1.0] - 2026-02-11

### 🏗️ Architecture & Philosophy
- **SAT Framework Integration**: Formally codified the **Skills, Agents, Tools** architecture in `ARCHITECTURE.md` and `AGENT.md`.
- **"Living Master" Philosophy**: Shifted the system to a LaTeX-first workflow. The `.tex` files in `data/latex/` are now the primary workspace, preserving manual user tweaks during tailoring.
- **Stateful Checklist Protocol**: Implemented a mandatory `[ ]` checklist mandate for all agent skills to ensure 100% instruction adherence.
- **Agent-Led Mapping**: Refactored parsers to provide "Rich Raw Data," empowering the AI agent to handle semantic mapping and custom resume sections instead of relying on rigid scripts.

### 🛠️ Infrastructure & Tools
- **Cross-Platform ARI**: Replaced the Bash-based Agent Run Interface with a universal Python version (`tools/ari.py`) for Linux, macOS, and Windows compatibility.
- **Automated Setup**: Created `tools/setup.py` to initialize workspace directories and synchronize agent skills.
- **Shared Utils Library**: Centralized LaTeX escaping, text normalization, and path validation into `tools/lib/utils.py`.
- **Streamlined Compilation**: Simplified `compile_latex.py` to run natively within the containerized environment.
- **Test Suite Restoration**: Repaired and expanded the unit test suite, ensuring all core utilities and parsers pass in the ARI environment.

### 🧠 Agentic Skills
- **Career Strategist Professionalization**:
    - Upgraded output to boardroom-ready PDF intelligence dossiers.
    - Implemented **IEEE Standard [1]** citations with full verification URLs.
    - Mandated high-density research including "Technical Stack DNA" and "Local Mission Portfolios."
- **Resume Importers (PDF/DOCX)**:
    - Implemented the **Template Selection Gate** (Analyze -> Present -> Recommend).
    - Added support for **Bespoke Template** creation during the import process.
- **Resume Tailor Pro**:
    - Refactored to act directly on LaTeX source files.
    - Enforced a "Zero Overhaul" policy to preserve user-defined macros and formatting.

### 📂 Structural Reorganization
- **Directory Overhaul**: Implemented a strict, intuitive hierarchy:
    - `imports/`: Staging area for raw resumes.
    - `data/json/`: Snapshot of initial import data.
    - `data/latex/`: The "Living Master" workspace.
    - `templates/built-in/`: Immutable core blueprints.
    - `outputs/resume/` & `outputs/dossiers/`: Final products.
- **Security & Privacy**: Overhauled `.gitignore` to protect personal data while whitelisting test personas.

### 🧪 Test Data & Documentation
- **Johnny Silverhand Baseline**: Established a high-fidelity, lore-accurate test persona (Robert John Linder) as the whitelisted system baseline.
- **README Revamp**: Refocused the main documentation on high-impact features: Pain-Free Digitization, Strategic Intelligence, and Surgical Targeting.
- **Architecture Documentation**: Created `ARCHITECTURE.md` to codify the project's DNA for future developers and agents.

---
*Generated by the ARI Agent.*
