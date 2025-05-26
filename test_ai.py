# test_ai.py
from ai_explainer import gpt_explainer

test_code = '''
Invoke-Expression ([System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String("aGVsbG8gd29ybGQ=")))
'''

print(gpt_explainer.explain_script(test_code, "PowerShell"))
