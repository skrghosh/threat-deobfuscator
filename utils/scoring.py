# utils/scoring.py

import json
import re
from pathlib import Path
from typing import Tuple, List

class RuleSet:
    def __init__(self, config_path: Path):
        cfg = json.loads(config_path.read_text())
        # categories: { "execution": {"severity":3, "ttps":[...]}, ... }
        self._cats = cfg["categories"]
        # patterns: [(compiled_regex, category), ...]
        self._patterns = [
            (re.compile(p["pattern"], re.IGNORECASE), p["category"])
            for p in cfg["patterns"]
        ]

    def analyze(self, code: str) -> Tuple[int, List[str]]:
        """
        Returns:
          - score (0–10): sum of severities for each matched category, capped at 10
          - ttp_tags: sorted list of unique MITRE TTP IDs from matched categories
        """
        matched = set()
        for regex, cat in self._patterns:
            if regex.search(code):
                matched.add(cat)

        # sum up severities
        total = sum(self._cats[cat]["severity"] for cat in matched)
        score = min(total, 10)

        # gather all TTPs
        ttps = set()
        for cat in matched:
            ttps.update(self._cats[cat]["ttps"])

        return score, sorted(ttps)


# instantiate for each language
_RULESETS = {
    "PowerShell": RuleSet(Path("config/rules_powershell.json")),
    "JavaScript": RuleSet(Path("config/rules_javascript.json")),
}


def analyze_script(code: str, script_type: str = "PowerShell") -> Tuple[int, List[str]]:
    """
    Public API: analyze deobfuscated code.
    """
    if not code or script_type not in _RULESETS:
        return 0, []
    return _RULESETS[script_type].analyze(code)
