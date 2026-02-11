#!/usr/bin/env python3
import subprocess
import os
import sys
from pathlib import Path

def run_ari():
    script_dir = Path(__file__).parent.resolve()
    project_root = script_dir.parent.resolve()
    
    # Tool container name
    image_name = "resume-tools:latest"

    # Check if docker is available
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: Docker is not installed or not in PATH.")
        sys.exit(1)

    # Build the image if it doesn't exist
    try:
        check_image = subprocess.run(["docker", "images", "-q", image_name], capture_output=True, text=True)
        if not check_image.stdout.strip():
            print(f"Building tool container {image_name}...")
            subprocess.run(["docker", "build", "-t", "resume-tools", str(script_dir)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to build or check Docker image: {e}")
        sys.exit(1)

    # Prepare Docker command
    # Windows paths need to be handled carefully by Docker, but Path().resolve() handles most of it.
    docker_cmd = [
        "docker", "run", "--rm",
        "-v", f"{project_root}:/app",
        "-w", "/app",
        "--user", f"{os.getuid() if hasattr(os, 'getuid') else 0}:{os.getgid() if hasattr(os, 'getgid') else 0}",
        "resume-tools"
    ]
    
    # Append the arguments passed to this script
    docker_cmd.extend(sys.argv[1:])

    try:
        # Run the command and pass through all IO
        result = subprocess.run(docker_cmd)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"An error occurred while running ARI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_ari()
