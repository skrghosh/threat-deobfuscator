import re

def flatten_string_concat(script: str) -> str:
    """
    Removes loose '+' used to break up strings.
    """
    return re.sub(r"\s*\+\s*", "", script)
