import re
from typing import Optional


def clean_text(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    raw = re.sub(r"[ \r\t]+", " ", raw)
    raw = re.sub(r"^[ \t]+|[ \t]+$", "", raw, flags=re.MULTILINE)
    raw = re.sub(r"\n\s*\n+", "\n", raw)

    raw = raw.strip()

    return raw
