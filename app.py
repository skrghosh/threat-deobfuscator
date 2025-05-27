# app.py

import streamlit as st
import openai
from deobfuscator import powershell, javascript
from ai_explainer import gpt_explainer
from utils import scoring

st.set_page_config(page_title="Threat Deobfuscator", layout="wide")

# —————————————————————————————————————————————
# 1) API Key Handling
# —————————————————————————————————————————————

st.sidebar.header("🔑 OpenAI API Key")
api_key = st.sidebar.text_input(
    "Enter your OpenAI API Key",
    type="password",
    help="You must paste your key here every time you load the app."
).strip()

if not api_key:
    st.sidebar.error("Please enter your OpenAI API key to analyze scripts.")
else:
    openai.api_key = api_key

# —————————————————————————————————————————————
# 2) Main UI
# —————————————————————————————————————————————

st.title("🕵️ Threat Deobfuscator")
st.markdown("""
Upload or paste an obfuscated script and get:
1. **Static deobfuscation**
2. **LLM refactor** (clean code)
3. **AI summary**
4. **Threat score** & **MITRE tags**
5. **Downloadable report**

> **NOTE**: The JavaScript deobfuscator is still in development and will be released soon.
""")

# Sidebar for script type & input
script_type   = st.sidebar.selectbox("Script Language", ["PowerShell", "JavaScript"])
input_method  = st.sidebar.radio("Input method:", ("Upload file", "Paste code"))

code = ""
if input_method == "Upload file":
    f = st.sidebar.file_uploader("Upload script", type=["ps1", "js", "txt"])
    if f:
        code = f.read().decode("utf-8", errors="ignore")
else:
    code = st.sidebar.text_area("Paste code here", height=200)

# Analyze button
analyze = st.sidebar.button("🔍 Analyze")

if analyze:
    if not code:
        st.sidebar.error("Please upload or paste your script.")
    elif not api_key:
        st.sidebar.error("Please provide your OpenAI API key.")
    else:
        # 1) Full deobfuscation (static + LLM)
        full_deob = powershell.deobfuscate(code) if script_type=="PowerShell" \
                    else javascript.deobfuscate(code)

        # 2) Split static vs. LLM
        marker = "# === LLM Refactor Suggestion ==="
        if marker in full_deob:
            static_part, llm_part = full_deob.split(marker, 1)
            llm_part = llm_part.strip()
        else:
            static_part, llm_part = full_deob, None

        # 3) Show Static Deobfuscated Code
        st.subheader("🔓 Static Deobfuscated Code")
        st.code(static_part,
                language="powershell" if script_type=="PowerShell" else "javascript")
        if st.button("📋 Copy Static Code"):
            st.text_area("Copy below:", static_part, height=200)

        # 4) LLM Refactor (collapsed)
        if llm_part:
            with st.expander("🤖 LLM Refactor Suggestion", expanded=False):
                st.code(llm_part, language="powershell")

        # 5) AI Summary
        st.subheader("🧠 AI-Powered Summary")
        combined = static_part + (("\n\n"+llm_part) if llm_part else "")
        summary = gpt_explainer.explain_script(combined, script_type)
        st.write(summary)

        # 6) Threat Score & Tags
        st.subheader("⚠️ Threat Score & MITRE Tags")
        score, ttp_tags = scoring.analyze_script(combined, script_type)
        st.metric("Threat Score", f"{score}/10")
        tag_html = "".join(
            f"<span style='display:inline-block; padding:3px 8px; margin:2px;"
            f"background-color:#2E86C1; color:white; border-radius:4px;'>{tag}</span>"
            for tag in ttp_tags
        )
        st.markdown(tag_html, unsafe_allow_html=True)

        # 7) Downloadable report
        report_md = (
            f"# Threat Deobfuscator Report\n\n"
            f"## Original Script\n```{script_type.lower()}\n{code}\n```\n\n"
            f"## Static Deobfuscated Code\n```{script_type.lower()}\n{static_part}\n```\n\n"
        )
        if llm_part:
            report_md += (
                f"## LLM Refactor Suggestion\n```{script_type.lower()}\n{llm_part}\n```\n\n"
            )
        report_md += (
            f"## AI Summary\n{summary}\n\n"
            f"## Threat Score\n{score}/10\n\n"
            f"## MITRE Tags\n{', '.join(ttp_tags)}\n"
        )

        st.download_button(
            label="📥 Download Report as Markdown",
            data=report_md,
            file_name="deobfuscator_report.md",
            mime="text/markdown"
        )
