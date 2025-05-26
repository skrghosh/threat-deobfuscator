import re, base64

def decode_base64_blocks(script: str) -> str:
    """
    Finds Convert::FromBase64String(...) payloads and decodes them.
    Flags PE binaries if detected.
    """
    def repl(match):
        b64 = match.group(1)
        try:
            raw = base64.b64decode(b64)
            if raw.startswith(b"MZ") or raw.startswith(b"TVqQ"):
                return match.group(0) + "\n\n# [!] PE payload detected"
            text = raw.decode("utf-8", errors="ignore")
            return match.group(0) + f"\n\n# Decoded Base64 Block:\n{text}"
        except Exception as e:
            return match.group(0) + f"\n\n# [!] Base64 decode failed: {e}"

    pattern = r'FromBase64String\(["\']?([A-Za-z0-9+/=]{8,})["\']?\)'
    return re.sub(pattern, repl, script)
