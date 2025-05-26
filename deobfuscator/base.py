# deobfuscator/base.py

from typing import Callable, List

class Deobfuscator:
    """
    Runs a series of handler functions over the script text.
    Each handler takes & returns a script string.
    """
    def __init__(self, handlers: List[Callable[[str], str]]):
        self.handlers = handlers

    def deobfuscate(self, script: str) -> str:
        result = script
        for handler in self.handlers:
            try:
                result = handler(result)
            except Exception as e:
                # If a handler fails, log or ignore and continue
                result += f"\n\n# [!] Handler {handler.__name__} error: {e}"
        return result.strip()
