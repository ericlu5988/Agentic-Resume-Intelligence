#!/usr/bin/env python3
import sys
import json
import argparse
import re
from pathlib import Path
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn

# Import shared utils
sys.path.append(str(Path(__file__).parent))
from lib.utils import escape_latex, sanitize_text

FONT_MAP = {
    "Garamond": "EB Garamond",
    "Calibri": "Carlito",
    "Arial": "Liberation Sans",
    "Times New Roman": "Liberation Serif",
    "DejaVu Sans": "DejaVu Sans"
}

def get_rich_run(run):
    """
    Extracts text and metadata from a docx run.
    """
    if run._element.xpath('.//w:tab'):
        return {"text": " TAB_MARKER ", "metadata": {}}
    
    text = sanitize_text(run.text)
    if not text: return None
    
    metadata = {
        "size": run.font.size.pt if run.font.size else 10,
        "bold": bool(run.bold),
        "italic": bool(run.italic),
        "underline": bool(run.underline),
        "color": str(run.font.color.rgb) if run.font.color and run.font.color.rgb else None,
        "font": run.font.name if run.font.name else None
    }
    
    return {"text": text, "metadata": metadata}

def parse_docx_rich(docx_path):
    try:
        doc = Document(docx_path)
        section = doc.sections[0]
        
        data = {
            "page_setup": {
                "margin_left": section.left_margin.pt,
                "margin_right": section.right_margin.pt,
                "margin_top": section.top_margin.pt,
                "margin_bottom": section.bottom_margin.pt,
            },
            "blocks": []
        }

        for item in doc.element.body.iterchildren():
            if item.tag.endswith('p'):
                para = Paragraph(item, doc)
                if not para.text.strip() and not para.runs:
                    data["blocks"].append({"type": "space", "value": 8})
                    continue
                
                fmt = para.paragraph_format
                
                # List Check
                is_list = False
                pPr = item.find(qn('w:pPr'))
                if pPr is not None and pPr.find(qn('w:numPr')) is not None:
                    is_list = True

                runs_data = []
                for run in para.runs:
                    rich_run = get_rich_run(run)
                    if rich_run:
                        runs_data.append(rich_run)

                # Border Check
                border_height = 0
                if pPr is not None:
                    pBdr = pPr.find(qn('w:pBdr'))
                    if pBdr is not None:
                        bottom = pBdr.find(qn('w:bottom'))
                        if bottom is not None:
                            sz = bottom.get(qn('w:sz'))
                            if sz: border_height = int(sz) / 8.0

                data["blocks"].append({
                    "type": "paragraph",
                    "alignment": "center" if para.alignment == WD_ALIGN_PARAGRAPH.CENTER else "flushleft",
                    "is_list": is_list,
                    "border_height": border_height,
                    "text": sanitize_text(para.text),
                    "runs": runs_data
                })

            elif item.tag.endswith('tbl'):
                table = Table(item, doc)
                table_block = {"type": "table", "rows": []}
                for row in table.rows:
                    row_data = [sanitize_text(cell.text) for cell in row.cells]
                    table_block["rows"].append(row_data)
                data["blocks"].append(table_block)

        return data
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rich Metadata DOCX Parser.")
    parser.add_argument("input_file", help="Path to the input DOCX")
    args = parser.parse_args()
    print(json.dumps(parse_docx_rich(args.input_file), indent=2))