import re
from urllib.parse import urlparse


def extract_pattern(text: str, pattern: str, group: int = 1) -> str | None:
    """Extract matching group from text using regex pattern."""
    if not text:
        return None
    
    try:
        match = re.search(pattern, text)
        if match:
            return match.group(group)
        return None
    except (ValueError, AttributeError):
        return None


def extract_year(text: str, min_year: int = 1880, max_year: int = 2030) -> int | None:
    """Extract year from string - supports parenthesis (2023), slug -2023, or loose formats."""
    if not text:
        return None
    
    try:
        # 1. Search in parenthesis first: "(YYYY)"
        year_str = extract_pattern(text, r'\((\d{4})\)')
        if year_str:
            year = int(year_str)
            if min_year <= year <= max_year:
                return year
        
        # 2. Search slug format: "-YYYY" (at end)
        year_str = extract_pattern(text, r'-(\d{4})$')
        if year_str:
            year = int(year_str)
            if min_year <= year <= max_year:
                return year
        
        # 3. Fallback: Search any 4-digit number in range
        year_matches = re.findall(r'\b(19\d{2}|20[0-3]\d)\b', text)
        if year_matches:
            year = int(year_matches[-1])
            if min_year <= year <= max_year:
                return year
            
        return None
    except (ValueError, AttributeError):
        return None


def extract_number_from_text(text: str) -> int | None:
    """Extract the first number found in text."""
    number_str = extract_pattern(text, r'(\d+)')
    
    if number_str:
        try:
            return int(number_str)
        except ValueError:
            pass
    
    return None


def clean_whitespace(text: str) -> str:
    """Clean excessive whitespace from text."""
    if not text:
        return ""
    
    # Reduce multiple spaces to single space
    text = re.sub(r'\s+', ' ', text)
    # Strip leading/trailing whitespace
    return text.strip()


def is_valid_url(url: str) -> bool:
    """Validate if the string is a properly formatted URL with scheme (http/https) and netloc."""
    if not url or not isinstance(url, str):
        return False
    
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        return False
    
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False
