import re
import json
import sys

def sanitize_prompt_input(text):
    """
    Sanitizes user-provided text to mitigate prompt injection.
    """
    if not isinstance(text, str):
        return text
    
    # Common injection patterns
    patterns = [
        r'ignore\s+previous\s+instructions',
        r'disregard\s+system\s+prompt',
        r'you\s+are\s+now\s+an\s+admin',
        r'new\s+instructions:',
        r'system\s+override'
    ]
    
    sanitized = text
    for pattern in patterns:
        sanitized = re.sub(pattern, '[FILTERED_INJECTION]', sanitized, flags=re.IGNORECASE)
    
    return sanitized

def validate_dossier_schema(data):
    """
    Deterministic validation of Career Strategist Dossier JSON.
    Returns (is_valid, error_message)
    """
    required_keys = [
        "company", "location", "candidate_name", "date", 
        "executive_summary", "local_mission_portfolio", 
        "enterprise_bi", "strategic_context", "technical_stack_dna", 
        "strategic_fit", "sources"
    ]
    
    for key in required_keys:
        if key not in data:
            return False, f"Missing required dossier key: {key}"
        
    # Validate list-of-objects structure for research sections
    list_keys = [
        "local_mission_portfolio", "enterprise_bi", 
        "strategic_context", "technical_stack_dna", "strategic_fit"
    ]
    
    for key in list_keys:
        if not isinstance(data[key], list):
            return False, f"Key '{key}' must be a list of objects."
        for item in data[key]:
            if not isinstance(item, dict) or "label" not in item or "text" not in item:
                return False, f"Invalid object in '{key}'. Expected {{'label': '...', 'text': '...'}}"
                
    return True, ""

def redact_pii(text):
    """
    Basic PII redaction for emails and phone numbers.
    """
    if not isinstance(text, str):
        return text
        
    # Redact Emails
    text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[REDACTED_EMAIL]', text)
    # Redact Phone Numbers (Basic US/Intl)
    text = re.sub(r'(\+?\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}', '[REDACTED_PHONE]', text)
    
    return text
