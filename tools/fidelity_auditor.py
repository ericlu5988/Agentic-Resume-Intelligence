#!/usr/bin/env python3
import json
import argparse
import re
import sys
from pathlib import Path
from rapidfuzz import fuzz
import pdfplumber

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

def normalize(text):
    if not text: return ""
    # Normalize formatting artifacts
    text = text.replace('\\textbullet', '').replace('•', '').replace('\u2022', '')
    text = text.replace('\\textbar', '|').replace('\textbar', '|')
    
    # Normalize smart quotes and dashes
    text = text.replace('’', "'").replace('‘', "'")
    text = text.replace('“', '"').replace('”', '"')
    text = text.replace('—', '--').replace('–', '-')
    
    # Normalize ligatures
    ligatures = {
        'ﬀ': 'ff',
        'ﬁ': 'fi',
        'ﬂ': 'fl',
        'ﬃ': 'ffi',
        'ﬄ': 'ffl',
    }
    for k, v in ligatures.items():
        text = text.replace(k, v)
        
    return re.sub(r'\s+', '', text).lower()

def audit(source_json_path, target_pdf_path):
    # Path Validation: Enforce Source of Truth
    source_p = Path(source_json_path).resolve()
    if "data/masters" not in str(source_p):
        print(f"WARNING: Source JSON '{source_json_path}' is outside 'data/masters/'.", file=sys.stderr)
        print("This violates the 'Source of Truth' standard.", file=sys.stderr)

    # Enforce UTF-8 for JSON source
    with open(source_json_path, 'r', encoding='utf-8') as f:
        source_data = json.load(f)
    
    target_geo = extract_geo_text(target_pdf_path)
    target_text_full = "".join([w["text"] for w in target_geo])
    target_norm = normalize(target_text_full)
    
    issues = []
    
    # 1. Textual Integrity (Entity Check)
    def check_exists(val, label):
        if not val: return
        if isinstance(val, list):
            for i, item in enumerate(val):
                check_exists(item, f"{label}[{i}]")
            return
        
        norm_val = normalize(str(val))
        if norm_val not in target_norm:
            score = fuzz.partial_ratio(str(val).lower(), target_text_full.lower())
            if score < 85:
                issues.append(f"MISSING CONTENT [{label}]: '{val}' (Fuzzy: {score:.1f})")

    check_exists(source_data.get('name'), "Name")
    for i, exp in enumerate(source_data.get('experience', [])):
        check_exists(exp.get('company'), f"Exp[{i}].company")
        check_exists(exp.get('bullets'), f"Exp[{i}].bullets")

    # 2. Geometric Consistency
    name = source_data.get('name')
    if name:
        target_name_objs = [w for w in target_geo if normalize(name) in normalize(w['text'])]
        if target_name_objs:
            avg_top = sum(w['top'] for w in target_name_objs) / len(target_name_objs)
            if avg_top > 150: 
                issues.append(f"GEOMETRIC DRIFT: Name '{name}' found at Y={avg_top:.1f} (Expected < 150)")

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
