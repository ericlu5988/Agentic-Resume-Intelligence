#!/usr/bin/env python3
import json
import sys
import argparse
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def escape_latex(text):
    """
    Escapes special LaTeX characters using raw string literals to prevent 
    backslash collisions (e.g., \t interpreted as tab).
    """
    if not isinstance(text, str):
        return text
    
    # We remove the bullet from here because modern LaTeX handles UTF-8 bullets
    # and we want to join skills with literal bullets in the template.
    mapping = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '\\': r'\textbackslash{}',
        '|': r'\textbar{}',
    }
    text = "".join(mapping.get(c, c) for c in text)
    
    # Disable problematic ligatures for fidelity audit matching
    ligature_map = {
        'ff': 'f{f}',
        'fi': 'f{i}',
        'fl': 'f{l}',
        'ffi': 'f{f}{i}',
        'ffl': 'f{f}{l}',
    }
    for k, v in ligature_map.items():
        text = text.replace(k, v)
        
    return text

def run_engine(data_path, template_path, output_path):
    # Path Validation: Enforce Source of Truth
    data_p = Path(data_path).resolve()
    if "data/masters" not in str(data_p):
        print(f"WARNING: Source JSON '{data_path}' is outside 'data/masters/'.", file=sys.stderr)
        print("This violates the 'Source of Truth' standard.", file=sys.stderr)

    # Load data with explicit UTF-8
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Self-healing: Unwrap "resume" key if it's the sole root to prevent nesting errors
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

    # Save with explicit UTF-8
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