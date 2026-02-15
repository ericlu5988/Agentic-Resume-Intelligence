#!/usr/bin/env python3
import subprocess
import os
import sys
import shutil
from pathlib import Path

# Import shared utils
sys.path.append(str(Path(__file__).parent))
from lib.utils import log_security_event

def run_ari():
    script_dir = Path(__file__).parent.resolve()
    project_root = script_dir.parent.resolve()
    
    # Tool container name
    image_name = "resume-tools:latest"

    # Securely find docker path
    docker_bin = shutil.which("docker")
    if not docker_bin:
        print("Error: Docker is not installed or not in PATH.")
        sys.exit(1)

    # Check if docker is available
    try:
        subprocess.run([docker_bin, "--version"], capture_output=True, check=True)  # nosec B603
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: Docker is not responding correctly.")
        sys.exit(1)

    # Build the image if it doesn't exist
    try:
        check_image = subprocess.run([docker_bin, "images", "-q", image_name], capture_output=True, text=True)  # nosec B603
        if not check_image.stdout.strip():
            print(f"Building tool container {image_name}...")
            subprocess.run([docker_bin, "build", "-t", "resume-tools", str(script_dir)], check=True)  # nosec B603
    except subprocess.CalledProcessError as e:
        print(f"Failed to build or check Docker image: {e}")
        sys.exit(1)

    # Prepare Docker command
    docker_cmd = [
        docker_bin, "run", "--rm",
        "-v", f"{project_root}:/app",
        "-w", "/app",
        "--user", f"{os.getuid() if hasattr(os, 'getuid') else 1000}:{os.getgid() if hasattr(os, 'getgid') else 1000}",
        "resume-tools"
    ]
    
    # --- PHASE 1: Secure Tool Interface (Allowlist & Validation) ---
    args = sys.argv[1:]
    if not args:
        print("Usage: ari.py <script|module> [args...]")
        sys.exit(1)

    executable = args[0]
    
    # Approved tools and modules
    ALLOWLIST = {
        # Core Engines
                "tools/tex_renderer.py",
         
        "tools/compile_latex.py",
        "tools/pdf_parser.py",
        "tools/docx_parser.py",
        "tools/fidelity_auditor.py",
        "tools/job_discovery.py",
        "tools/setup.py",
        # Security & Testing Modules
        "-m", "pytest", "bandit", "semgrep", "id", "/usr/local/bin/semgrep"
    }

    # Validation logic
    is_module_call = executable == "-m" and len(args) > 1
    target = args[1] if is_module_call else executable

    if target not in ALLOWLIST:
        print(f"SECURITY ERROR: '{target}' is not in the execution allowlist.")
        sys.exit(1)

    # Path Traversal Check for all arguments
    for arg in args:
        if ".." in arg or arg.startswith("/etc") or arg.startswith("/var"):
            print(f"SECURITY ERROR: Path traversal or unauthorized access detected in argument: {arg}")
            sys.exit(1)

    # Append the arguments passed to this script
    docker_cmd.extend(args)

    try:
        # Run the command and pass through all IO
        result = subprocess.run(docker_cmd)  # nosec B603
        log_security_event(target, args, result.returncode)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"An error occurred while running ARI: {e}")
        log_security_event(target, args, 1)
        sys.exit(1)

if __name__ == "__main__":
    run_ari()
