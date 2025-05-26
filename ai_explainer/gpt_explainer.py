# ai_explainer/gpt_explainer.py

import os
import openai

def explain_script(code: str, script_type: str = "PowerShell") -> str:
    """
    Send the cleaned script to GPT-4 for explanation of behavior.
    Requires that openai.api_key was already set (in app.py).
    """
    # Ensure we have an API key at runtime
    api_key = os.getenv("OPENAI_API_KEY") or openai.api_key
    if not api_key:
        return "[!] No OpenAI API key found. Please set it in the sidebar or as an environment variable."

    # At this point, app.py has already assigned openai.api_key = api_key
    system_prompt = (
        "You are a cybersecurity analyst. Explain what this script does in simple, "
        "step-by-step terms, highlighting any suspicious or malicious behavior and "
        "mapping to known MITRE ATT&CK techniques."
    )

    messages = [
        {"role": "system",  "content": system_prompt},
        {"role": "user",    "content": f"Script (language: {script_type}):\n\n{code}"}
    ]

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.2,
            max_tokens=700
        )
        return resp.choices[0].message.content.strip()

    except Exception as e:
        return f"[!] Error contacting OpenAI API: {e}"
