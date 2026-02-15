#!/usr/bin/env python3
import shutil
import argparse
from pathlib import Path
import sys

def setup_workspace(gemini_sync=False):
    project_root = Path(__file__).parent.parent.resolve()
    
    # 1. Ensure standard directories exist
    dirs = [
        "imports", 
        "data/json", 
        "data/latex", 
        "templates/resumes/built-in", 
        "templates/resumes/bespoke",
        "templates/cover-letters/built-in",
        "templates/dossiers/built-in",
        "templates/assessments/built-in",
        "outputs/resume", 
        "outputs/dossiers", 
        ".tmp"
    ]
    print("Initializing workspace directories...")
    for d in dirs:
        target = project_root / d
        target.mkdir(parents=True, exist_ok=True)
        gitkeep = target / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()
        print(f"  - Verified: {d}/")

    # 2. Gemini-specific skill sync
    if gemini_sync:
        source_skills = project_root / "skills"
        target_skills = project_root / ".gemini" / "skills"
        
        if not source_skills.exists():
            print(f"Warning: Source skills directory not found at {source_skills}")
            return

        print(f"Syncing skills to {target_skills}...")
        try:
            target_skills.mkdir(parents=True, exist_ok=True)
            for item in source_skills.iterdir():
                if item.is_dir():
                    dest = target_skills / item.name
                    if dest.exists():
                        shutil.rmtree(dest)
                    shutil.copytree(item, dest)
                    print(f"    - Synced: {item.name}")
        except Exception as e:
            print(f"Failed to sync skills: {e}")

    # 3. Generate Bootstrap DNA for agents
    print("\nGenerating Bootstrap DNA...")
    dna_file = project_root / ".tmp" / "BOOTSTRAP_DNA.md"
    agent_md = project_root / "AGENT.md"
    arch_md = project_root / "ARCHITECTURE.md"
    
    try:
        with open(dna_file, "w") as f:
            f.write("# ARI BOOTSTRAP DNA\n\n")
            if agent_md.exists():
                f.write(f"## FROM: {agent_md.name}\n")
                f.write(agent_md.read_text())
                f.write("\n\n---\n\n")
            if arch_md.exists():
                f.write(f"## FROM: {arch_md.name}\n")
                f.write(arch_md.read_text())
                f.write("\n")
        print(f"  - Created: .tmp/{dna_file.name}")
    except Exception as e:
        print(f"Failed to generate DNA: {e}")

    print("\nWorkspace setup complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize the ARI workspace.")
    parser.add_argument("--gemini", action="store_true", help="Sync skills for Gemini CLI.")
    args = parser.parse_args()
    
    setup_workspace(gemini_sync=args.gemini)