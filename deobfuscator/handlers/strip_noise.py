# deobfuscator/handlers/strip_noise.py

import re

def strip_noise(script: str) -> str:
    """
    Remove comments, trailing whitespace, and blank lines to declutter.
    """
    # 1) Remove any PowerShell comments
    script = re.sub(r'#.*', '', script)

    # 2) Strip trailing spaces/tabs on each line
    script = re.sub(r'[ \t]+$', '', script, flags=re.MULTILINE)

    # 3) Drop empty lines
    lines = [line for line in script.splitlines() if line.strip()]
    return "\n".join(lines)
