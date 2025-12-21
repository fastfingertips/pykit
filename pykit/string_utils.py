import re
from urllib.parse import urlparse
import unicodedata


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


def is_domain_url(url: str, domains: str | list[str], must_contain: str | list[str] | None = None) -> bool:
    """Check if URL belongs to domain(s) and optionally contains specific path segments."""
    if not is_valid_url(url):
        return False
    
    url_lower = url.lower()
    
    # 1. Check domains (ANY match)
    if isinstance(domains, str):
        domains = [domains]
    if not any(d.lower() in url_lower for d in domains):
        return False
        
    # 2. Check required content (ANY match from the list)
    if must_contain:
        if isinstance(must_contain, str):
            must_contain = [must_contain]
        return any(c.lower() in url_lower for c in must_contain)
    
    return True


def validate_url(url: str, allowed_domains: str | list[str] | None = None, must_contain: str | list[str] | None = None) -> tuple[bool, str]:
    """
    Validate URL with optional domain and content checks.
    
    Returns:
        tuple[bool, str]: (is_valid, error_message) - if valid, error_message is empty string.
    """
    if not url:
        return False, "URL is required"
    
    url = url.strip()
    
    if not is_valid_url(url):
        return False, "Invalid URL format (must start with http:// or https://)"
    
    if allowed_domains or must_contain:
        if not is_domain_url(url, allowed_domains or [], must_contain):
            domain_msg = f" ({allowed_domains})" if allowed_domains else ""
            return False, f"URL does not match required domain/content criteria{domain_msg}"
            
    return True, ""


def build_url(base: str, *paths, trailing_slash: bool = True) -> str:
    """
    Construct a URL from base and path segments, handling slashes automatically.
    
    Args:
        base: Base URL/Domain (e.g. "https://example.com")
        *paths: Path segments (e.g. "user", "profile")
        trailing_slash: Whether to end the URL with a slash
        
    Returns:
        Joined URL
    """
    # Remove trailing slash from base
    url = base.rstrip('/')
    
    for path in paths:
        # Remove leading/trailing slashes from segments
        clean_path = str(path).strip('/')
        if clean_path:
            url = f"{url}/{clean_path}"
            
    if trailing_slash and not url.endswith('/'):
        url += '/'
    elif not trailing_slash:
        url = url.rstrip('/')
        
    return url


def slugify(text: str, separator: str = '-', lowercase: bool = True) -> str:
    """
    Convert text to URL-friendly slug format.
    Handles accented characters from all languages (Turkish, French, Spanish, etc.)
    
    Args:
        text: Text to slugify
        separator: Character to use as separator (default: '-')
        lowercase: Convert to lowercase (default: True)
        
    Returns:
        Slugified text
    """
    if not text:
        return ""
    
    # Normalize Unicode characters (é -> e, ğ -> g, ñ -> n, etc.)
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    # Convert to lowercase if requested
    if lowercase:
        text = text.lower()
    
    # Replace non-alphanumeric characters with separator
    text = re.sub(r'[^a-zA-Z0-9]+', separator, text)
    
    # Remove leading/trailing separators
    text = text.strip(separator)
    
    # Collapse multiple separators into one
    text = re.sub(f'{re.escape(separator)}+', separator, text)
    
    return text
