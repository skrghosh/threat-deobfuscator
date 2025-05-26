# deobfuscator/handlers/llm_refactor.py

import os
from openai import OpenAI  # for openai>=1.0.0

# initialize client
_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def llm_refactor(script: str) -> str:
    """
    Final pass: ask the LLM to refactor any obfuscated PowerShell
    into clean equivalent code. Returns original + cleaned code.
    """
    system_prompt = (
        "You are a PowerShell de-obfuscator. Your job is to take the following obfuscated snippet "
        "and output ONLY the equivalent, fully-resolved PowerShell command(s), with no comments "
        "or explanation."
    )

    # Build the message sequence
    messages = [
        {"role": "system",  "content": system_prompt},
        {"role": "user",    "content": script},
    ]

    try:
        resp = _client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.0,
            max_tokens=500
        )
        cleaned = resp.choices[0].message.content.strip()
    except Exception as e:
        cleaned = f"[!] LLM refactor error: {e}"

    return script + "\n\n# === LLM Refactored De-obfuscation ===\n" + cleaned
