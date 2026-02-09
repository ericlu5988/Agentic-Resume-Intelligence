#!/usr/bin/env python3
import sys
import json
import argparse
import re
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("Error: 'pdfplumber' is required. Install it with: pip install pdfplumber")
    sys.exit(1)

def extract_detailed_layout(pdf_path, x_tolerance=3):
    """
    Extracts text with precise geometric coordinates and font metadata.
    """
    results = {
        "metadata": {},
        "pages": [],
        "full_text": ""
    }

    try:
        with pdfplumber.open(pdf_path) as pdf:
            results["metadata"] = pdf.metadata
            full_text_list = []

            for i, page in enumerate(pdf.pages):
                page_data = {
                    "page_number": i + 1,
                    "width": float(page.width),
                    "height": float(page.height),
                    "text": page.extract_text(x_tolerance=x_tolerance),
                    "objects": []
                }
                
                # Extract words with their bounding boxes and font info
                words = page.extract_words(
                    extra_attrs=["fontname", "size"],
                    keep_blank_chars=False,
                    x_tolerance=x_tolerance
                )
                
                for word in words:
                    page_data["objects"].append({
                        "text": word["text"],
                        "x0": float(word["x0"]),
                        "top": float(word["top"]),
                        "x1": float(word["x1"]),
                        "bottom": float(word["bottom"]),
                        "font": word.get("fontname"),
                        "size": float(word.get("size", 0)),
                        "bold": "bold" in (word.get("fontname", "").lower())
                    })
                
                results["pages"].append(page_data)
                if page_data["text"]:
                    full_text_list.append(page_data["text"])
            
            results["full_text"] = "\n".join(full_text_list)

    except Exception as e:
        return {"error": str(e)}

    return results

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Detailed geometric PDF extraction.")

    parser.add_argument("input_file", help="Path to the input PDF")

    parser.add_argument("--x-tolerance", type=float, default=3.0, help="Horizontal tolerance for word grouping")

    args = parser.parse_args()



    data = extract_detailed_layout(args.input_file, x_tolerance=args.x_tolerance)

    print(json.dumps(data, indent=2))
