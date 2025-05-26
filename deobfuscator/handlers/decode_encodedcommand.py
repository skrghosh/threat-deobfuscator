import re, base64

def decode_encodedcommand(script: str) -> str:
    """
    Detects powershell.exe -EncodedCommand <b64> blocks,
    decodes the UTF-16LE payload, and appends it.
    """
    pattern = r"-EncodedCommand\s+([A-Za-z0-9+/=]{20,})"
    match = re.search(pattern, script)
    if not match:
        return script

    b64 = match.group(1)
    try:
        decoded = base64.b64decode(b64).decode('utf-16le', errors='ignore')
        return script + f"\n\n# Decoded EncodedCommand:\n{decoded}"
    except Exception as e:
        return script + f"\n\n# [!] Failed to decode EncodedCommand: {e}"
