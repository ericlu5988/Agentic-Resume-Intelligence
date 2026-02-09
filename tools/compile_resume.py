#!/usr/bin/env python3
import subprocess
import os
import sys
import argparse
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

    # Detect if running inside docker
    in_docker = os.path.exists('/.dockerenv')

    if in_docker:
        print("Detected Docker environment, running xelatex locally...")
        local_cmd = [
            "xelatex", "-interaction=nonstopmode", f"-jobname={jobname}", filename
        ]
        try:
            result = subprocess.run(local_cmd, cwd=work_dir, capture_output=True, text=True)
            if result.returncode != 0:
                print("LaTeX compilation failed.")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
                return False
        except Exception as e:
            print(f"An error occurred during local compilation: {e}")
            return False
    else:
        # Check if docker is available
        try:
            subprocess.run(["docker", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Error: Docker is not installed or not in PATH.")
            return False

        docker_cmd = [
            "docker", "run", "--rm",
            "-v", f"{work_dir}:/work",
            "-w", "/work",
            "texlive/texlive",
            "xelatex", "-interaction=nonstopmode", f"-jobname={jobname}", filename
        ]
        try:
            print("Running LaTeX compilation via Docker...")
            result = subprocess.run(docker_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print("LaTeX compilation failed.")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
                return False
        except Exception as e:
            print(f"An error occurred during docker compilation: {e}")
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
    parser = argparse.ArgumentParser(description="Compile a LaTeX file using Docker.")
    parser.add_argument("tex_file", help="Path to the .tex file to compile")
    args = parser.parse_args()

    if compile_latex(args.tex_file):
        sys.exit(0)
    else:
        sys.exit(1)
