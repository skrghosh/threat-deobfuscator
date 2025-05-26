# deobfuscator/handlers/llm_refactor.py

import openai

def llm_refactor(script: str) -> str:
    """
    Final pass: ask the LLM to refactor any obfuscated PowerShell
    into clean, equivalent code. Returns original + cleaned code.
    """
    # At this point, app.py has already set openai.api_key
    system_prompt = (
        "You are a PowerShell de-obfuscator. Your job is to take the following obfuscated snippet "
        "and output ONLY the equivalent, fully-resolved PowerShell command(s), with no comments "
        "or explanation."
    )

    messages = [
        {"role": "system",  "content": system_prompt},
        {"role": "user",    "content": script},
    ]

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.0,
            max_tokens=500
        )
        cleaned = resp.choices[0].message.content.strip()
    except Exception as e:
        cleaned = f"[!] LLM refactor error: {e}"

    return script + "\n\n# === LLM Refactor Suggestion ===\n" + cleaned
