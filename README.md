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

### 5. Security-First Governance
Hardened for high-stakes environments. The system includes an integrated **Security Conscience** (Core rules for OWASP, RAG, and AI Safety) and automated SAST scanning to ensure your data and code remain secure.

---

## 🛡️ Security Governance
ARI is built on a **Security-First** philosophy. Every agent action is cross-referenced against a strict governance framework located in the `rules/` directory.

- **Core Rules**: OWASP 2025, AI Security, and Agentic Agency.
- **RAG Safety**: Input sanitization and indirect prompt injection prevention.
- **Hardened Runtime**: Tools run in an isolated, non-root Docker container with path-traversal protection.

---

## 🏗️ The SAT Architecture
This repository is built on the **SAT (Skills, Agents, Tools)** framework. For a deep dive into the design philosophy and development standards, see **[ARCHITECTURE.md](./ARCHITECTURE.md)**.

---

## 🏗️ Standardized Data Flow
The system distinguishes between **digitization** (one-time) and **targeting** (per job).

`imports/ -> Digitization -> data/resume/tex/ (The Living Master) -> Targeting -> outputs/resume/`

1.  **Digitization (Entry Points)**:
    - **Legacy**: Place existing PDF/DOCX resumes in `imports/` to be converted.
    - **LaTeX Native**: If you already have a LaTeX resume, place it directly in `data/resume/tex/`.
2.  **The Living Master**: Your `.tex` file in `data/resume/tex/` is your primary workspace. **Perfect your design here once; it serves as the baseline for all future targeting.**
3.  **Targeting (Tailoring)**: When targeting a job, the agent surgically edits your "Living Master" LaTeX to match the company's specific mission profile.

---

## 🧪 System Baseline & Example
To demonstrate the system's full capability, we provide a complete end-to-end example using the **Johnny Silverhand** persona. This showcases the transformation from a legacy document into a surgically-tailored executive output.

1.  **Original Source**: [imports/johnny_silverhand.pdf](./imports/johnny_silverhand.pdf) (Raw document)
2.  **Extracted JSON**: [data/resume/json/johnny_silverhand.json](./data/resume/json/johnny_silverhand.json) (Geometric-aware data)
3.  **Living Master (LaTeX)**: [data/resume/tex/johnny_silverhand.tex](./data/resume/tex/johnny_silverhand.tex) (The editable master)
4.  **Strategic Intelligence**: [outputs/company-research/Strategy_Dossier_Palantir_Silverhand.pdf](./outputs/company-research/Strategy_Dossier_Palantir_Silverhand.pdf) (Research)
5.  **Tailored Result**: [outputs/resume/Resume_Johnny_Silverhand_Lockheed_Martin_2026-02-12.pdf](./outputs/resume/Resume_Johnny_Silverhand_Lockheed_Martin_2026-02-12.pdf) (Surgical output)

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
Verify the deterministic logic and security posture using the integrated suite:

### Functional Tests
```bash
python3 tools/ari.py -m pytest tools/tests/
```

### Security Scans (SAST)
```bash
python3 tools/ari.py -m bandit -r .
python3 tools/ari.py /usr/local/bin/semgrep scan --config auto .
```

### Rule Validation
```bash
python3 tools/ari.py -m pytest rules/tests/
```

---
*Created by Eric Lu for professionals who value precision over automation.*
