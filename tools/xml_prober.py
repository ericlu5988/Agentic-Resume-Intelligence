#!/usr/bin/env python3
import sys
import argparse
from docx import Document
from lxml import etree

def probe_xml(docx_path):
    """
    Exhaustively scans the DOCX XML for layout-defining tags.
    """
    try:
        doc = Document(docx_path)
        # Use lxml to parse the raw body XML
        xml_str = doc._element.xml
        root = etree.fromstring(xml_str.encode('utf-8'))
        
        # Namespace map for Word
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        
        results = {
            "Borders (Lines)": root.xpath('//w:pBdr', namespaces=ns),
            "Drawings (Shapes)": root.xpath('//w:drawing', namespaces=ns),
            "Legacy Picts": root.xpath('//w:pict', namespaces=ns),
            "Section Columns": root.xpath('//w:cols', namespaces=ns),
            "Tab Stops": root.xpath('//w:tabs', namespaces=ns),
            "Table Layouts": root.xpath('//w:tbl', namespaces=ns),
            "Page Breaks": root.xpath('//w:br[@w:type="page"]', namespaces=ns)
        }

        print(f"--- XML PROBE RESULTS: {docx_path} ---")
        for key, elements in results.items():
            print(f"{key}: {len(elements)} instances found.")
            if elements:
                # Show first instance for mapping analysis
                print(f"  Example XML: {etree.tostring(elements[0], pretty_print=True).decode('utf-8')[:300]}...")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Probe DOCX Visual DNA.")
    parser.add_argument("input_file", help="Path to the input DOCX")
    args = parser.parse_args()
    probe_xml(args.input_file)
