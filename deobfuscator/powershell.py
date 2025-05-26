# deobfuscator/powershell.py

from .base import Deobfuscator
from .handlers.decode_encodedcommand import decode_encodedcommand
from .handlers.flatten_string_concat import flatten_string_concat
from .handlers.decode_char_array import decode_char_array
from .handlers.decode_base64_blocks import decode_base64_blocks
from .handlers.normalize_aliases import normalize_aliases
from .handlers.strip_noise import strip_noise
from .handlers.llm_refactor import llm_refactor 

HANDLERS = [
    decode_encodedcommand,
    flatten_string_concat,
    decode_char_array,
    decode_base64_blocks,
    normalize_aliases,
    strip_noise,
    llm_refactor,  
]

_deobf = Deobfuscator(HANDLERS)

def deobfuscate(script: str) -> str:
    return _deobf.deobfuscate(script)
