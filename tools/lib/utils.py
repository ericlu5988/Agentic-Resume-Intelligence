import re
import sys
from pathlib import Path

def escape_latex(text):
    """
    Escapes special LaTeX characters using raw string literals.
    """
    if not isinstance(text, str):
        return text
    
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
    
    # Apply mapping character by character
    text = "".join(mapping.get(c, c) for c in text)

    # Normalize smart quotes and dashes for LaTeX compatibility
    text = text.replace('’', "'").replace('‘', "'")
    text = text.replace('“', '"').replace('”', '"')
    text = text.replace('—', '--').replace('–', '-')
    
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

def validate_master_path(path_str):
    """
    Enforces the 'Source of Truth' standard and prevents path traversal.
    """
    p = Path(path_str).resolve()
    root = Path(__file__).parent.parent.parent.resolve()
    
    # Check for path traversal or access outside project root
    if not str(p).startswith(str(root)):
        raise PermissionError(f"Access denied: Path '{path_str}' is outside the project root.")

    if "data/json" not in str(p):
        print(f"WARNING: Path '{path_str}' is outside 'data/json/'.", file=sys.stderr)
        print("This violates the 'Source of Truth' standard.", file=sys.stderr)
    return p

def normalize_text(text):
    """
    Normalizes text for comparison (removing artifacts, ligatures, etc.)
    """
    if not text: return ""
    # Remove common LaTeX markers that might be in the source
    text = text.replace('\\textbullet', '').replace('•', '').replace('\u2022', '')
    text = text.replace('\\textbar', '|').replace('\textbar', '|')
    
    text = text.replace('’', "'").replace('‘', "'")
    text = text.replace('“', '"').replace('”', '"')
    text = text.replace('—', '--').replace('–', '-')
    
    ligatures = {'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬃ': 'ffi', 'ﬄ': 'ffl'}
    for k, v in ligatures.items():
        text = text.replace(k, v)
        
    return re.sub(r'\s+', '', text).lower()