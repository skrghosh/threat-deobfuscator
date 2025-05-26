# ai_explainer/gpt_explainer.py

import os
from openai import OpenAI, APIError

def explain_script(code: str, script_type: str = "PowerShell") -> str:
    """
    Send the cleaned script to GPT-4 for a behavioral explanation.
    Expects OPENAI_API_KEY in the environment (injected by app.py).
    """
    # 1) Grab the key from env
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "[!] No OpenAI API key found. Please set it in the sidebar or as an environment variable."

    # 2) Instantiate the v1+ client
    client = OpenAI(api_key=api_key)

    # 3) Build prompts
    system_prompt = (
        "You are a cybersecurity analyst. Explain what this script does in simple, "
        "step-by-step terms, highlighting any suspicious or malicious behavior and "
        "mapping to known MITRE ATT&CK techniques."
    )
    user_prompt = f"Script (language: {script_type}):\n\n```{script_type}\n{code}\n```"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": user_prompt},
    ]

    # 4) Call the chat completion endpoint
    try:
        resp = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.2,
            max_tokens=700
        )
        return resp.choices[0].message.content.strip()

    except APIError as e:
        return f"[!] Error contacting OpenAI API: {e}"
    except Exception as e:
        return f"[!] Unexpected error: {e}"
