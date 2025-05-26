# ai_explainer/gpt_explainer.py

import os
import openai
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def explain_script(code: str, script_type: str = "PowerShell") -> str:
    if not os.getenv("OPENAI_API_KEY"):
        return "[!] No OpenAI API key found. Please set OPENAI_API_KEY in your environment."

    prompt = (
        f"You are a senior cybersecurity researcher. Explain what this {script_type} script is doing in simple, step-by-step terms. "
        "Identify any suspicious or malicious behavior, and mention if it uses any known techniques like obfuscation, command execution, or network calls.\n\n"
        "Script:\n"
        "```\n"
        f"{code}\n"
        "```"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=700
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"[!] Error contacting OpenAI API: {str(e)}"
