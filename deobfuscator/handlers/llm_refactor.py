# deobfuscator/handlers/llm_refactor.py

import os
from openai import OpenAI, APIError

def llm_refactor(script: str) -> str:
    """
    Final pass: ask GPT-4 to refactor any remaining obfuscation into clean PowerShell code.
    Expects OPENAI_API_KEY in the environment (injected by app.py).
    """
    # 1) Grab the key from env
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return script + "\n\n# === LLM Refactor Suggestion ===\n[!] No OpenAI API key provided."

    # 2) Instantiate the v1+ client
    client = OpenAI(api_key=api_key)

    # 3) Build prompts
    system_prompt = (
        "You are a PowerShell de-obfuscator. Your job is to take the following obfuscated snippet "
        "and output ONLY the equivalent, fully-resolved PowerShell command(s), with no comments "
        "or explanation."
    )
    messages = [
        {"role": "system",  "content": system_prompt},
        {"role": "user",    "content": script},
    ]

    # 4) Call the chat completion endpoint
    try:
        resp = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.0,
            max_tokens=500
        )
        cleaned = resp.choices[0].message.content.strip()
    except APIError as e:
        cleaned = f"[!] LLM refactor error: {e}"
    except Exception as e:
        cleaned = f"[!] Unexpected error: {e}"

    # 5) Return original + cleaned suggestion
    return script + "\n\n# === LLM Refactor Suggestion ===\n" + cleaned
