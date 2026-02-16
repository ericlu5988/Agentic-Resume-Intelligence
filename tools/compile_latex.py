#!/usr/bin/env python3
import subprocess
import os
import sys
import argparse
import shutil
from pathlib import Path

def compile_latex(tex_file_path):
    tex_path = Path(tex_file_path).resolve()
    if not tex_path.exists(): return False
    work_dir = tex_path.parent
    filename = tex_path.name
    jobname = tex_path.stem
    xelatex_bin = shutil.which("xelatex") or "xelatex"
    env = os.environ.copy()
    project_root = Path(__file__).resolve().parent.parent
    templates_root = str(project_root / "templates")
    env["TEXINPUTS"] = f".:{templates_root}//:{env.get('TEXINPUTS', '')}"
    local_cmd = [xelatex_bin, "-interaction=nonstopmode", f"-jobname={jobname}", filename]
    try:
        subprocess.run(local_cmd, cwd=work_dir, capture_output=True, text=True, env=env)
        return (work_dir / f"{jobname}.pdf").exists()
    except: return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tex_file")
    args = parser.parse_args()
    sys.exit(0 if compile_latex(args.tex_file) else 1)
