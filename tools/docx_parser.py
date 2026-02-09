#!/usr/bin/env python3
import sys
import json
import argparse
import re
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn

FONT_MAP = {
    "Garamond": "EB Garamond",
    "Calibri": "Carlito",
    "Arial": "Liberation Sans",
    "Times New Roman": "Liberation Serif",
    "DejaVu Sans": "DejaVu Sans"
}

def escape_latex(text):
    if not isinstance(text, str): return text
    mapping = {
        '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_',
        '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}',
        '\\': r'\textbackslash{}', '|': r'\textbar{}',
    }
    return "".join(mapping.get(c, c) for c in text)

def get_run_latex(run, default_font):
    if run._element.xpath('.//w:tab'):
        return " TAB_MARKER "
    
    content = escape_latex(run.text)
    if not content: return ""
    
    size = run.font.size.pt if run.font.size else 10
    raw_name = run.font.name if run.font.name else default_font
    font_name = FONT_MAP.get(raw_name, "DejaVu Sans")
    
    res = f"{{\\fontspec{{{font_name}}}\\fontsize{{{size}}}{{{size*1.2}}}\\selectfont "
    if run.font.color and run.font.color.rgb:
        res += f"\\color[HTML]{{{run.font.color.rgb}}}"
    
    # FORMATTING
    if run.bold: content = f"\\textbf{{{content}}}"
    if run.italic: content = f"\\textit{{{content}}}"
    if run.underline: content = f"\\underline{{{content}}}"
    
    res += content + "}"
    return res

def parse_docx_total_fidelity(docx_path):
    try:
        doc = Document(docx_path)
        section = doc.sections[0]
        
        data = {
            "page_setup": {
                "margin_left": section.left_margin.pt,
                "margin_right": section.right_margin.pt,
                "margin_top": section.top_margin.pt,
                "margin_bottom": section.bottom_margin.pt,
                "primary_font": "EB Garamond"
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

                # Tab Consolidation
                raw_tex = "".join(get_run_latex(run, "Garamond") for run in para.runs)
                rich_content = re.sub(r'( TAB_MARKER )+', r'\\hfill ', raw_tex)

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
                    "space_before": fmt.space_before.pt if fmt.space_before else 0,
                    "space_after": fmt.space_after.pt if fmt.space_after else 2,
                    "left_indent": fmt.left_indent.pt if fmt.left_indent else 0,
                    "first_line_indent": fmt.first_line_indent.pt if fmt.first_line_indent else 0,
                    "is_list": is_list,
                    "border_height": border_height,
                    "rich_content": rich_content
                })

            elif item.tag.endswith('tbl'):
                table = Table(item, doc)
                table_block = {"type": "table", "rows": []}
                for row in table.rows:
                    row_data = ["".join(get_run_latex(run, "Garamond") for p in cell.paragraphs for run in p.runs) for cell in row.cells]
                    table_block["rows"].append(row_data)
                data["blocks"].append(table_block)

        return data
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="High Fidelity DOCX mirroring.")
    parser.add_argument("input_file", help="Path to the input DOCX")
    args = parser.parse_args()
    print(json.dumps(parse_docx_total_fidelity(args.input_file), indent=2))
