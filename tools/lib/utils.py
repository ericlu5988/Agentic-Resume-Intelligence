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
        '~': r'	extasciitilde{}',
        '^': r'	extasciicircum{}',
        '': r'	extbackslash{}',
        '|': r'	extbar{}',
    }
    
    # Apply mapping
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

def validate_master_path(path_str):
    """
    Enforces the 'Source of Truth' standard for JSON files.
    """
    p = Path(path_str).resolve()
    if "data/masters" not in str(p):
        print(f"WARNING: Path '{path_str}' is outside 'data/masters/'.", file=sys.stderr)
        print("This violates the 'Source of Truth' standard.", file=sys.stderr)
    return p

def normalize_text(text):
    """
    Normalizes text for comparison (removing artifacts, ligatures, etc.)
    """
    if not text: return ""
    text = text.replace('	extbullet', '').replace('•', '').replace('\u2022', '')
    text = text.replace('	extbar', '|').replace('	extbar', '|')
    text = text.replace('’', "'").replace('‘', "'")
    text = text.replace('“', '"').replace('”', '"')
    text = text.replace('—', '--').replace('–', '-')
    
    ligatures = {'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬃ': 'ffi', 'ﬄ': 'ffl'}
    for k, v in ligatures.items():
        text = text.replace(k, v)
        
    return re.sub(r'\s+', '', text).lower()
