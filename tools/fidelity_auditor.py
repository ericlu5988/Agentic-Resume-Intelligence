#!/usr/bin/env python3
import json
import argparse
import sys
from pathlib import Path
from rapidfuzz import fuzz
import pdfplumber

# Import shared utils
sys.path.append(str(Path(__file__).parent))
from lib.utils import normalize_text, validate_master_path

def extract_geo_text(pdf_path):
    """Extracts text with coordinates."""
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            words = page.extract_words()
            for w in words:
                data.append({
                    "text": w["text"],
                    "x0": float(w["x0"]),
                    "top": float(w["top"]),
                    "page": page.page_number
                })
    return data

def audit(source_json_path, target_pdf_path):
    # Path Validation: Enforce Source of Truth
    source_p = validate_master_path(source_json_path)

    with open(source_p, 'r', encoding='utf-8') as f:
        source_data = json.load(f)
    
    target_geo = extract_geo_text(target_pdf_path)
    target_text_full = "".join([w["text"] for w in target_geo])
    target_norm = normalize_text(target_text_full)
    
    issues = []
    
    # 1. Textual Integrity (Entity Check)
    def check_exists(val, label):
        if not val: return
        if isinstance(val, list):
            for i, item in enumerate(val):
                check_exists(item, f"{label}[{i}]")
            return
        if isinstance(val, dict):
            for k, v in val.items():
                check_exists(v, f"{label}.{k}")
            return
        
        norm_val = normalize_text(str(val))
        if norm_val not in target_norm:
            score = fuzz.partial_ratio(str(val).lower(), target_text_full.lower())
            if score < 85:
                issues.append(f"MISSING CONTENT [{label}]: '{val}' (Fuzzy: {score:.1f})")

    check_exists(source_data.get('name'), "Name")
    for i, exp in enumerate(source_data.get('experience', [])):
        check_exists(exp.get('company'), f"Exp[{i}].company")
        check_exists(exp.get('bullets'), f"Exp[{i}].bullets")

    # Check custom sections if they exist
    for i, section in enumerate(source_data.get('custom_sections', [])):
        check_exists(section.get('title'), f"Custom[{i}].title")
        check_exists(section.get('content'), f"Custom[{i}].content")

    report = {
        "status": "PASS" if not issues else "FAIL",
        "integrity_score": max(0, 100 - len(issues)*5),
        "issues": issues,
        "metrics": {
            "target_word_count": len(target_geo),
            "source_experience_count": len(source_data.get('experience', []))
        }
    }
    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Geometric Fidelity Auditor.")
    parser.add_argument("source_json", help="Structured JSON source")
    parser.add_argument("target_pdf", help="Generated PDF")
    args = parser.parse_args()

    results = audit(args.source_json, args.target_pdf)
    print(json.dumps(results, indent=2))