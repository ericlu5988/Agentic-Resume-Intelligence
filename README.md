# Agentic Resume Intelligence

> **Stop manually editing LaTeX. Start winning interviews with research-backed resumes.**

**Agentic Resume Intelligence** is a native AI agent skill-set designed to surgically tailor LaTeX resumes for specific job descriptions or networking scenarios. Unlike simple GPT wrappers, this system uses a formal **SAT (Skills, Agents, Tools) Architecture** that performs real-time research, enforces hard-requirement verification, and maintains 100% formatting integrity.

---

## 🚀 The Hook: Why this is different
Most AI resume tools rewrite your history or hallucinate experience. **Agentic Resume Intelligence** operates on three core principles within this agentic framework:
1. **The "Sprinkle" Rule**: It maintains 90% of your original narrative, only replacing or appending high-impact technical terms and metrics.
2. **The Discovery Gate**: If a job requirement is missing, the agent is **forbidden from guessing**. It will stop and ask you targeted questions to "tease out" relevant experience.
3. **Intelligence-Driven**: It researches local company contracts, mission priorities, and leadership DNA to align your resume with a company's specific footprint.

---

## ✨ Features
- **High-Fidelity Digitization**: 
    - **PDF Importer**: Geometric-aware extraction for digital PDFs.
    - **DOCX Importer**: Topological extraction (bold, italics, alignment) for Word documents.
- **JD Mode**: Precision alignment with "Required" vs. "Preferred" qualifications from any Job Description.
- **Networking Mode**: Tailor for a company and location even without a JD using real-time intelligence.
- **Career Strategist**: Deep-dive intelligence gathering to assess company fit, contract stability, and interview "Attack Vectors."
- **Dockerized Compilation**: One-click PDF generation using a standardized LaTeX environment via ARI.
- **Privacy-First**: Automatically ignores your personal data and tailored outputs from version control.

---

## 🧩 The SAT Architecture
This repository separates concerns to ensure accuracy and reproducibility. For a deep dive into the design philosophy, development standards, and cross-platform logic, see **[ARCHITECTURE.md](./ARCHITECTURE.md)**.

- **Skills (The Instructions)**: Domain-specific SOPs (Standard Operating Procedures) in `skills/`.
- **Agents (The Decision-Maker)**: Coordination logic (Gemini CLI, Claude Code, Windsurf, etc.).
- **Tools (The Execution)**: Deterministic Python scripts in `tools/` executed via the **Agent Run Interface (ARI)**.

### The Agent Run Interface (ARI)
ALL tools MUST be executed via the ARI wrapper to ensure LaTeX and Python dependencies are met:
```bash
python3 tools/ari.py [tool_name.py] [args]
```

---

## 🏗️ Standardized Data Flow
The system distinguishes between **digitization** (one-time) and **tailoring** (per job).

`imports/ -> Digitization -> data/latex/ (The Living Master) -> Tailoring -> outputs/resume/`

1.  **Digitization (Entry Points)**:
    - **Legacy**: Place existing PDF/DOCX resumes in `imports/` to be converted.
    - **LaTeX Native**: If you already have a LaTeX resume, place it directly in `data/latex/`.
2.  **The Living Master**: Your `.tex` file in `data/latex/` is your primary workspace. **You should tweak this file to match exactly how you want your resume to look before any tailoring occurs.**
3.  **Tailoring (Targeting)**: When targeting a specific job, the agent surgically edits your "Living Master" LaTeX to match the job description, saving the result to `outputs/resume/`.

---

## 🏗️ Complementary Skills
This repository provides distinct agentic skills designed to be used in sequence:

1. **Strategic Intelligence (`career-strategist`)**: The "Brain." Performs deep research into a company's financial health, contracts, and technical footprint.
2. **Surgical Tailoring (`resume-tailor-pro`)**: The "Scalpel." Takes gathered intelligence and surgically "sprinkles" keywords into your LaTeX template.
3. **Resume Importers (`pdf-resume-importer` & `docx-resume-importer`)**: The "Bridge." Converts legacy resumes into the structured JSON and LaTeX formats required by the system.

---

## 🤖 For AI Agents
This repository is optimized for use with AI agents. 
- **Skills**: AI agents should use the metadata in `skills/*/SKILL.md` and follow the procedures in `skills/*/INSTRUCTIONS.md`.
- **Context**: Agent-specific instructions are provided in `GEMINI.md` and `CLAUDE.md`.

---

## 🛠️ Installation & Setup

### Prerequisites
- **AI Agent Framework**: Gemini CLI, Claude Code, or any agent capable of following markdown-based instructions.
- **Docker**: Required for deterministic tool execution and LaTeX compilation.

### Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ericlu5988/Agentic-Resume-Intelligence.git
   cd Agentic-Resume-Intelligence
   ```
2. **Initialize Workspace**:
   ```bash
   python3 tools/setup.py --gemini  # Use --gemini flag if using Gemini CLI
   ```
3. **Build the Tool Container**:
   The ARI auto-builds on first run, but you can pre-build it:
   ```bash
   python3 tools/ari.py --help
   ```

---

## 🧪 Testing
Verify the deterministic logic of the tools using the integrated test suite via ARI:
```bash
python3 tools/ari.py -m unittest discover tools/tests
```

---

## 📖 How to Use

### 1. Import Your Existing Resume
Place your resume in `imports/` and ask the agent to start the import:
> *"Import my_resume.pdf from the imports folder"*
The agent will perform a **Template Selection Gate**, recommending the best blueprint (Default, Minimalist, or Federal) or creating a **Bespoke Template** for you.

### 2. Gather Intelligence (Optional but Recommended)
Ask the agent to start a research mission using the **Career Strategist** skill:
> *"I'm targeting a role at [Company]. Let's start the Career Strategist workflow."*
Strategy dossiers are saved to `outputs/dossiers/`.

### 3. Tailor Your Resume
Ask the agent to start a tailoring session using the **Resume Tailor Pro** skill:
> *"I'm ready to tailor my resume. Let's start the Resume Tailor Pro workflow."*

### 4. Review & Compile
The agent will present proposed changes. Once approved, it will generate a new `.tex` file in `data/latex/` and automatically compile it into a professional `.pdf` in `outputs/resume/`.

---

## 🔒 Privacy & Safety
- **JSON Lockdown**: All personal content is stored in `data/json/` and is protected by `.gitignore`.
- **Anti-Fabrication**: Hard-coded rules ensure your resume remains 100% honest.
- **Ligature-Aware Auditing**: Every PDF is validated against its JSON source to ensure character-perfect fidelity (Score ≥ 95%).

---
*Created by Eric Lu for professionals who value precision over automation.*