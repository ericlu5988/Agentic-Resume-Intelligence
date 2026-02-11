# Agentic Resume Intelligence

> **From legacy documents to boardroom-ready intelligence. Win interviews with data-backed resumes.**

**Agentic Resume Intelligence (ARI)** is a specialized AI agent framework designed to automate the most painful parts of the job search: digitization, deep research, and surgical tailoring. It moves you beyond generic AI rewrites into a high-fidelity **LaTeX-First** workflow where you maintain 100% control over your design while the agent handles the targeting.

---

## ⚡ High-Impact Features

### 1. Pain-Free Digitization
Move your legacy resumes into the modern era instantly. Our geometric-aware parsers extract every detail from your **PDF** or **DOCX** files, preserving bolding, alignment, and structure to establish your "Living Master" LaTeX resume.

### 2. Executive Intelligence Dossiers
Don't just apply—dominate the conversation. The agent performs real-time research into your target company's contracts (TITAN, Maven, etc.), technical stack, and leadership DNA, outputting a **beautiful, boardroom-ready PDF dossier** with full IEEE-style citations for verification.

### 3. Surgical Targeting (Tailoring)
Target specific roles without losing your voice. The agent surgically "sprinkles" high-impact keywords and metrics into your **Living Master LaTeX** file, ensuring you pass the ATS while maintaining 90% of your original narrative and 100% of your custom formatting.

### 4. Deterministic Fidelity Audit
Character-perfect accuracy. Every generated document is validated by a deterministic Python auditor to ensure a **Fidelity Score of 100**, guaranteeing that the AI never hallucinates your experience or breaks your layout.

---

## 🏗️ The SAT Architecture
This repository is built on the **SAT (Skills, Agents, Tools)** framework. For a deep dive into the design philosophy and development standards, see **[ARCHITECTURE.md](./ARCHITECTURE.md)**.

---

## 🏗️ Standardized Data Flow
The system distinguishes between **digitization** (one-time) and **targeting** (per job).

`imports/ -> Digitization -> data/latex/ (The Living Master) -> Targeting -> outputs/resume/`

1.  **Digitization (Entry Points)**:
    - **Legacy**: Place existing PDF/DOCX resumes in `imports/` to be converted.
    - **LaTeX Native**: If you already have a LaTeX resume, place it directly in `data/latex/`.
2.  **The Living Master**: Your `.tex` file in `data/latex/` is your primary workspace. **Perfect your design here once; it serves as the baseline for all future targeting.**
3.  **Targeting (Tailoring)**: When targeting a job, the agent surgically edits your "Living Master" LaTeX to match the company's specific mission profile.

---

## 🛠️ Installation & Setup

### Prerequisites
- **AI Agent Framework**: Gemini CLI, Claude Code, or any markdown-capable agent.
- **Docker**: Required for deterministic tool execution and LaTeX compilation.

### Setup
1. **Initialize Workspace**:
   ```bash
   python3 tools/setup.py --gemini  # Use --gemini flag if using Gemini CLI
   ```
2. **Build Tool Container**:
   ```bash
   python3 tools/ari.py --help
   ```

---

## 🧪 Testing
Verify the deterministic logic using the integrated test suite:
```bash
python3 tools/ari.py -m unittest discover tools/tests
```

---

## 📖 How to Use

### 1. Digitize
Place your resume in `imports/` and say: *"Import my resume."* The agent will guide you through the **Template Selection Gate**.

### 2. Research
Identify a target and say: *"I have an interview at Palantir. Run the Career Strategist mission."* Strategy dossiers are saved to `outputs/dossiers/`.

### 3. Target
Once you have the intel, say: *"Target my resume for this Palantir role."* The agent will surgically update your LaTeX master and save the final PDF to `outputs/resume/`.

---
*Created by Eric Lu for professionals who value precision over automation.*
