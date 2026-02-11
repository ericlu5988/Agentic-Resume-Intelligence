#!/usr/bin/env python3
import json
import sys
import argparse
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# Import shared utils
sys.path.append(str(Path(__file__).parent))
from lib.utils import escape_latex, validate_master_path

def run_engine(data_path, template_path, output_path):
    # Path Validation: Enforce Source of Truth
    data_p = validate_master_path(data_path)

    # Load data
    with open(data_p, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Self-healing
    if "resume" in data and len(data) == 1:
        data = data["resume"]

    # Setup Jinja2 environment
    template_file = Path(template_path).resolve()
    env = Environment(
        loader=FileSystemLoader(str(template_file.parent)),
        block_start_string='((%',
        block_end_string='%))',
        variable_start_string='(((',
        variable_end_string=')))',
        comment_start_string='((#',
        comment_end_string='#))'
    )
    env.filters['latex_escape'] = escape_latex

    template = env.get_template(Path(template_path).name)
    
    # Render
    rendered = template.render(resume=data)

    # Save
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered)
    print(f"Successfully generated: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deterministic LaTeX Resume Generator.")
    parser.add_argument("json_data", help="Path to structured resume JSON")
    parser.add_argument("template", help="Path to LaTeX Jinja2 template")
    parser.add_argument("output", help="Path to save generated .tex file")

    args = parser.parse_args()
    run_engine(args.json_data, args.template, args.output)
