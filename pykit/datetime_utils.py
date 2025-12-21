from datetime import datetime


def parse_datetime(date_string: str | None, formats: list[str] | None = None) -> datetime | None:
    """
    Parse date string to datetime object with support for multiple formats.
    
    Args:
        date_string: Date string to parse
        formats: Optional list of custom formats to try. If None, uses common formats.
        
    Returns:
        datetime object or None if parsing fails
        
    Examples:
        >>> parse_datetime("2025-09-12T22:33:05.358621")
        datetime(2025, 9, 12, 22, 33, 5, 358621)
        >>> parse_datetime("2025-09-28 07:15:21")
        datetime(2025, 9, 28, 7, 15, 21)
        >>> parse_datetime("12/25/2024", formats=["%m/%d/%Y"])
        datetime(2024, 12, 25, 0, 0)
    """
    if not date_string:
        return None
    
    # Default common formats
    default_formats = [
        "%Y-%m-%d %H:%M:%S",           # 2025-09-28 07:15:21
        "%Y-%m-%d",                     # 2025-09-28
        "%d/%m/%Y",                     # 28/09/2025
        "%m/%d/%Y",                     # 09/28/2025
        "%d-%m-%Y",                     # 28-09-2025
        "%Y/%m/%d",                     # 2025/09/28
        "%d.%m.%Y",                     # 28.09.2025
        "%Y-%m-%d %H:%M:%S.%f",        # 2025-09-28 07:15:21.123456
    ]
    
    formats_to_try = formats if formats else default_formats
    
    # Try ISO format first (most common)
    if 'T' in date_string:
        try:
            return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        except (ValueError, TypeError):
            pass
    
    # Try each format
    for fmt in formats_to_try:
        try:
            return datetime.strptime(date_string, fmt)
        except (ValueError, TypeError):
            continue
    
    return None


def format_datetime(dt: datetime | None, format_string: str = "%Y-%m-%d %H:%M:%S") -> str | None:
    """
    Format datetime object to string.
    
    Args:
        dt: datetime object to format
        format_string: Output format (default: "YYYY-MM-DD HH:MM:SS")
        
    Returns:
        Formatted string or None
    """
    if not dt:
        return None
    
    try:
        return dt.strftime(format_string)
    except (ValueError, AttributeError):
        return None


def now() -> datetime:
    """Get current datetime."""
    return datetime.now()


def today() -> datetime:
    """Get today's date at midnight."""
    return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
