from datetime import datetime
import re


def extract_and_format_date(raw_text: str) -> str:
    """
    Extracts a date from a given text string and converts it to a MySQL-compatible format (YYYY-MM-DD).

    Args:
        raw_text (str): The text containing the date.

    Returns:
        str: The formatted date (YYYY-MM-DD) or None if no valid date is found.

    Raises:
        ValueError: If the extracted date does not match known formats.
    """
    if not raw_text:
        return None

    # Extract potential date using regex (handles both MM/DD/YYYY and DD/MM/YYYY)
    match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', raw_text)
    if not match:
        return None  # No valid date found

    date_str = match.group(1).strip()

    # Try parsing with both common formats
    for fmt in ('%d/%m/%Y', '%m/%d/%Y'):
        try:
            return datetime.strptime(date_str, fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue

    raise ValueError(f"Date format not recognized: {date_str}")
