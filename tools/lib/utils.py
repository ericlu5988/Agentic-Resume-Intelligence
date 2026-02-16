import re
import sys
from pathlib import Path

def sanitize_text(text):
    """
    Standardizes text by replacing smart quotes and dashes.
    """
    if not isinstance(text, str):
        return text
    
    # Smart Quotes
    text = text.replace('’', "'").replace('‘', "'")
    text = text.replace('“', '"').replace('”', '"')
    
    # Dashes
    text = text.replace('—', '--').replace('–', '-')
    
    return text

def escape_latex(text):
    """
    Standard LaTeX escaping for user data.
    """
    if not isinstance(text, str):
        return text
    
    text = sanitize_text(text)
    
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
    
    return "".join(mapping.get(c, c) for c in text)

def validate_master_path(path_str):
    """
    Enforces the 'Source of Truth' standard.
    """
    p = Path(path_str).resolve()
    root = Path(__file__).parent.parent.parent.resolve()
    if not str(p).startswith(str(root)):
        raise PermissionError(f"Access denied: Path '{path_str}' is outside project root.")
    return p

def normalize_text(text):
    if not text: return ""
    text = text.replace('’', "'").replace('‘', "'")
    return re.sub(r'\s+', '', text).lower()

def log_security_event(tool, args, exit_code):
    pass
