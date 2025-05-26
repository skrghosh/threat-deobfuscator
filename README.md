# Threat Deobfuscator

_A web-based AI + static analysis tool to automatically de-obfuscate PowerShell and JavaScript scripts, explain their behavior, and score their maliciousness._

---

## 🔍 Features

- **Static Deobfuscation**  
  • Base64 payload decoding (`FromBase64String`, `-EncodedCommand`)  
  • String-concatenation flattening (`'h'+'ello' → 'hello'`)  
  • Char-array/hex decoding (`(0x68,0x65,0x6C,0x6C,0x6F) → "hello"`)  
  • Alias normalization & noise stripping  

- **LLM “Catch-All” Refactor**  
  • Uses OpenAI GPT-4 (or your own API key) to clean up any remaining obfuscation  
  • Produces fully-expanded, ready-to-read code  

- **AI-Powered Behavioral Summary**  
  • Step-by-step explanation of what the script does  
  • Identification of suspicious or malicious behaviors  
  • MITRE ATT&CK technique mapping  

- **Threat Scoring (0–10)**  
  • Data-driven, category-based scoring (Execution, Obfuscation, Networking, Persistence, Defense‐Evasion)  
  • Configurable via JSON—no Python changes needed to add new rules  

- **Slick Streamlit UI**  
  • File upload or paste-in editor  
  • Collapsible LLM output panel  
  • Copy-to-clipboard buttons  
  • Markdown report download  

---

## 🛠️ Tech Stack

- **Frontend / UI:** [Streamlit](https://streamlit.io/)  
- **Backend logic:** Python 3.8+  
- **AI/LLM:** OpenAI GPT-4 (configurable)  
- **Static analysis:** Python `re`, `ast`, custom handlers  
- **Configuration:** JSON rule files under `config/`  
- **Deployment:** Streamlit Community Cloud or any Docker-based host  


