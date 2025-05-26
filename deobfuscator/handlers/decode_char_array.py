import re

def decode_char_array(script: str) -> str:
    """
    Finds hex arrays like (0x49,0x6E,...) and replaces with the decoded string.
    """
    def repl(match):
        hexes = re.findall(r"0x([0-9A-Fa-f]{2})", match.group())
        try:
            decoded = "".join(chr(int(h,16)) for h in hexes)
            return f'"{decoded}"'
        except:
            return match.group()

    pattern = r"\(\s*0x[0-9A-Fa-f]{2}(?:\s*,\s*0x[0-9A-Fa-f]{2})+\s*\)"
    return re.sub(pattern, repl, script)
