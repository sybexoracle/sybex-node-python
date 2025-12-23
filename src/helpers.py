from datetime import datetime

# minimize string
def minimize_string(input_string: str, max_length: int = 50) -> str:
    """
    Minimizes a string to a specified maximum length by truncating and adding ellipsis if necessary.

    Args:
        input_string (str): The string to minimize.
        max_length (int): The maximum allowed length of the string.

    Returns:
        str: The minimized string.
    """
    if len(input_string) <= max_length:
        return input_string
    return input_string[: max_length - 3] + "..."

# time to datetime conversion
def timestamp_to_datetime(timestamp: int) -> datetime:
    """
    Converts a UNIX timestamp to a datetime object.

    Args:
        timestamp (int): The UNIX timestamp to convert.

    Returns:
        datetime: The corresponding datetime object.
    """
    return datetime.fromtimestamp(timestamp)