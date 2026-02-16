#!/usr/bin/env python3
import sys
import json
import argparse
from pathlib import Path

# Import shared utils
sys.path.append(str(Path(__file__).parent))
from lib.utils import sanitize_text

try:
    import pdfplumber
except ImportError:
    print("Error: 'pdfplumber' is required. Install it with: pip install pdfplumber")
    sys.exit(1)

def extract_rich_layout(pdf_path, x_tolerance=3, y_tolerance=3):
    """
    Extracts text grouped by lines with rich metadata.
    """
    results = {
        "metadata": {},
        "pages": []
    }

    try:
        with pdfplumber.open(pdf_path) as pdf:
            results["metadata"] = pdf.metadata

            for i, page in enumerate(pdf.pages):
                page_data = {
                    "page_number": i + 1,
                    "width": float(page.width),
                    "height": float(page.height),
                    "lines": []
                }
                
                # Extract words with their bounding boxes and font info
                words = page.extract_words(
                    extra_attrs=["fontname", "size"],
                    keep_blank_chars=False,
                    x_tolerance=x_tolerance,
                    y_tolerance=y_tolerance
                )
                
                if not words:
                    results["pages"].append(page_data)
                    continue

                # Group words into lines based on 'top' coordinate
                words.sort(key=lambda x: (x["top"], x["x0"]))
                
                current_line = []
                last_top = words[0]["top"]
                
                for word in words:
                    if abs(word["top"] - last_top) > y_tolerance:
                        # Process the finished line
                        page_data["lines"].append(process_line(current_line))
                        current_line = []
                        last_top = word["top"]
                    
                    current_line.append(word)
                
                if current_line:
                    page_data["lines"].append(process_line(current_line))
                
                results["pages"].append(page_data)

    except Exception as e:
        return {"error": str(e)}

    return results

def process_line(words):
    """
    Combines words in a line and calculates average metadata.
    """
    text = sanitize_text(" ".join([w["text"] for w in words]))
    avg_size = sum([float(w.get("size", 0)) for w in words]) / len(words)
    fonts = list(set([w.get("fontname", "unknown") for w in words]))
    is_bold = any("bold" in f.lower() for f in fonts)
    
    return {
        "text": text,
        "x0": min([float(w["x0"]) for w in words]),
        "top": min([float(w["top"]) for w in words]),
        "size": avg_size,
        "bold": is_bold,
        "fonts": fonts
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rich geometric PDF extraction.")
    parser.add_argument("input_file", help="Path to the input PDF")
    parser.add_argument("--x-tolerance", type=float, default=3.0)
    parser.add_argument("--y-tolerance", type=float, default=3.0)
    args = parser.parse_args()

    data = extract_rich_layout(args.input_file, x_tolerance=args.x_tolerance, y_tolerance=args.y_tolerance)
    print(json.dumps(data, indent=2))