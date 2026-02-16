#!/usr/bin/env python3
import json
import sys
import argparse
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# Import shared utils
sys.path.append(str(Path(__file__).parent))
from lib.utils import escape_latex, validate_master_path
from lib.ai_safety import validate_dossier_schema

def run_engine(data_path, template_path, output_path):
    data_p = validate_master_path(data_path)
    with open(data_p, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if any(keyword in str(data_p) for keyword in ["Strategy_Dossier", "Strategy_Report", "Company_Research"]):
        is_valid, error = validate_dossier_schema(data)
        if not is_valid:
            print(f"SECURITY/SCHEMA ERROR: {error}", file=sys.stderr)
            sys.exit(1)

    if "resume" in data and len(data) == 1:
        data = data["resume"]

    template_file = Path(template_path).resolve()
    env = Environment(
        loader=FileSystemLoader(str(template_file.parent)),
        autoescape=lambda _: False,
        block_start_string='((%',
        block_end_string='%))',
        variable_start_string='(((',
        variable_end_string=')))',
        comment_start_string='((#',
        comment_end_string='#))'
    )
    env.filters['latex_escape'] = escape_latex
    template = env.get_template(Path(template_path).name)
    rendered = template.render(resume=data)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered)
    print(f"Successfully generated: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("json_data")
    parser.add_argument("template")
    parser.add_argument("output")
    args = parser.parse_args()
    run_engine(args.json_data, args.template, args.output)
