# deobfuscator/handlers/normalize_aliases.py

def normalize_aliases(script: str) -> str:
    """
    Replace common PowerShell aliases or escape‐sequences with their full forms.
    """
    replacements = {
        # escape sequences
        '`n': '\n',
        '`r': '\r',
        '`t': '\t',

        # dangerous‐looking aliases → full cmdlets
        'IEX': 'Invoke-Expression',
        'iex': 'Invoke-Expression',

        # common downloader alias
        'New-Object Net.WebClient': 'Download via WebClient',
        'Invoke-WebRequest': 'Invoke-WebRequest',

        # you can add more aliases here as needed
    }

    for alias, full in replacements.items():
        script = script.replace(alias, full)

    return script
