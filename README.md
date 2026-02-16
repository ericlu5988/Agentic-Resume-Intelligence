# Agentic Resume Intelligence

> **From legacy documents to boardroom-ready intelligence. Win interviews with data-backed resumes.**

**Agentic Resume Intelligence (ARI)** is a specialized AI agent framework designed to automate the most painful parts of the job search: digitization, deep research, and surgical tailoring. It moves you beyond generic AI rewrites into a high-fidelity **LaTeX-First** workflow where you maintain 100% control over your design while the agent handles the targeting.

---

## ⚡ High-Impact Features

### 1. Pain-Free Digitization
Move your legacy resumes into the modern era instantly. Our geometric-aware parsers extract every detail from your **PDF** or **DOCX** files, preserving bolding, alignment, and structure to establish your "Living Master" LaTeX resume.

### 2. Executive Intelligence Reports
Don't just apply—dominate the conversation. The agent performs real-time research into your target company's contracts (TITAN, Maven, etc.), technical stack, and leadership DNA, outputting a **beautiful, boardroom-ready PDF intelligence report** with full IEEE-style citations for verification.

### 3. Surgical Targeting (Tailoring)
Target specific roles without losing your voice. The agent surgically "sprinkles" high-impact keywords and metrics into your **Living Master LaTeX** file, ensuring you pass the ATS while maintaining 90% of your original narrative and 100% of your custom formatting.

### 4. Deterministic Fidelity Audit
Character-perfect accuracy. Every generated document is validated by a deterministic Python auditor to ensure a **Fidelity Score of 100**, guaranteeing that the AI never hallucinates your experience or breaks your layout.

### 5. Security-First Governance
Hardened for high-stakes environments. The system includes an integrated **Security Conscience** (Core rules for OWASP, RAG, and AI Safety) and automated SAST scanning to ensure your data and code remain secure.

---

## 🛠️ Installation & Setup

### Prerequisites
- **AI Agent**: Gemini CLI (preferred), Claude Code, or Windsurf.
- **Docker**: Required for deterministic tool execution and LaTeX compilation.
- **Python 3.10+**: Required for workspace orchestration.

### Initial Setup
1. **Initialize Workspace**:
   ```bash
   python3 tools/setup.py --gemini  # Use --gemini flag for Gemini CLI
   ```
2. **Build Tool Container**:
   ```bash
   python3 tools/ari.py --help
   ```

---

## 🚀 Quick Start: The Career Workflow
ARI operates as a chain of specialized agents. Follow this sequence to transform your application from a raw document into a high-fidelity submission.

| Phase | Skill Triggers | What the Agent Does | Output |
| :--- | :--- | :--- | :--- |
| **1. Digitize** | "Import my resume", "Convert PDF to LaTeX" | Extracts geometric data and creates your **Living Master**. | `data/resume/tex/` |
| **2. Assess** | "Should I apply?", "Analyze this job description" | Performs a **Weighted Match Score** and GO/NO-GO gate. | `outputs/match-assessment/` |
| **3. Research** | "Gather mission intel", "/company-researcher" | Deep-dives into OSINT, leadership DNA, and technical stack. | `outputs/company-research/` |
| **4. Tailor** | "Tailor my resume", "/resume-tailor-pro" | Surgically targets your resume for the specific mission. | `outputs/resume/` |
| **5. Architect** | "Write a cover letter", "/cover-letter-architect" | Hooks your letter using research and tailored strengths. | `outputs/cover-letter/` |
| **6. Prepare** | "Prepare me for interview", "/interview-coach" | Synthesizes all data into talking points and STAR Q&A. | `outputs/interview-prep/` |

---

## 📂 Categorical Data Flow
The system distinguishes between **Data** (interim artifacts) and **Outputs** (final deliverables).

`imports/ -> Digitization -> data/resume/tex/ (Living Master) -> Targeting -> outputs/resume/`

- **`data/`**: Stores immutable JSON snapshots and editable LaTeX masters.
- **`outputs/`**: Dedicated strictly to final, boardroom-ready **PDF** artifacts.
- **`templates/`**: Professional blueprints for resumes, research reports, and assessments.

---

## 🧪 Mission Showcase: Johnny Silverhand vs. Palantir
Experience the full ARI transformation using the combat-hardened **Johnny Silverhand** example persona targeting a **Security Controller** role at **Palantir**.

1.  **Original Source**: [imports/johnny_silverhand.pdf](./imports/johnny_silverhand.pdf) (Legacy PDF)
2.  **Assessment**: [Opportunity Assessment PDF](./outputs/match-assessment/match_assessment_johnny_silverhand_palantir.pdf) | [JSON](./data/match-assessment/json/match_assessment_johnny_silverhand_palantir.json)
3.  **Intelligence**: [Mission Intelligence Report (PDF)](./outputs/company-research/Strategy_Report_Palantir_Silverhand.pdf) | [JSON](./data/company-research/json/Strategy_Report_Palantir_Silverhand.json)
4.  **Tailored Master**: [Targeted Resume (PDF)](./outputs/resume/Resume_JohnnySilverhand_Palantir_20260215.pdf) | [LaTeX Master](./outputs/resume/Resume_JohnnySilverhand_Palantir_20260215.tex)
5.  **Architecture**: [Research-Hooked Cover Letter](./outputs/cover-letter/CoverLetter_Palantir_Silverhand.pdf) | [LaTeX](./data/cover-letter/tex/CoverLetter_Palantir_Silverhand.tex)
6.  **Preparation**: [Interview Coaching Guide](./outputs/interview-prep/interview_prep_johnny_silverhand_palantir.pdf) | [JSON](./data/interview-prep/json/interview_prep_johnny_silverhand_palantir.json)

---

## 🏗️ Architecture & Security
ARI is built on the **SAT (Skills, Agents, Tools)** framework, enforcing a strict separation between AI reasoning and deterministic execution. Security is Prerequisite—every action is cross-referenced against our **Security Governance** framework (`rules/`) to ensure AI safety and RAG integrity.

For a deep dive, see **[ARCHITECTURE.md](./ARCHITECTURE.md)** and **[AGENT.md](./AGENT.md)**.

---
*Created by Eric Lu for professionals who value precision over automation.*
