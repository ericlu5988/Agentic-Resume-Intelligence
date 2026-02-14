#!/usr/bin/env python3
import subprocess
import os
import sys
import argparse
import shutil
from pathlib import Path

def compile_latex(tex_file_path):
    tex_path = Path(tex_file_path).resolve()
    if not tex_path.exists():
        print(f"Error: File {tex_path} not found.")
        return False

    work_dir = tex_path.parent
    filename = tex_path.name
    jobname = tex_path.stem

    print(f"Compiling {filename} in {work_dir}...")

    # Securely find xelatex path
    xelatex_bin = shutil.which("xelatex") or "xelatex"

    # Assumes we are running in an environment with xelatex (via ARI)
    local_cmd = [
        xelatex_bin, "-interaction=nonstopmode", f"-jobname={jobname}", filename
    ]
    
    try:
        # Run twice for cross-references if needed
        result = subprocess.run(local_cmd, cwd=work_dir, capture_output=True, text=True)
        if result.returncode != 0:
            print("LaTeX compilation failed.")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
    except Exception as e:
        print(f"An error occurred during compilation: {e}")
        return False

    pdf_file = work_dir / f"{jobname}.pdf"
    if pdf_file.exists():
        print(f"Successfully compiled: {pdf_file.name}")
        # Cleanup auxiliary files
        for ext in ['.log', '.aux', '.out']:
            aux_file = work_dir / f"{jobname}{ext}"
            if aux_file.exists():
                aux_file.unlink()
        return True
    else:
        print("PDF file was not generated.")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compile a LaTeX file.")
    parser.add_argument("tex_file", help="Path to the .tex file to compile")
    args = parser.parse_args()

    if compile_latex(args.tex_file):
        sys.exit(0)
    else:
        sys.exit(1)