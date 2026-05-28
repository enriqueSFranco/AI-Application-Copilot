import re
from typing import Dict

SECTION_PATTERNS = {
    "responsabilidades": r"(responsabilidades|qué harás|tareas principales)",
    "requisitos": r"(requisitos|lo que buscamos|perfil deseado)",
    "ofrecemos": r"(beneficios|ofrecemos|qué obtienes)",
}


def split_description_sections(text: str) -> Dict[str, str]:
    out = {}

    for key, pat in SECTION_PATTERNS.items():
        found = re.search(
            pat + r":?(.*?)(?=\n[A-ZÁÉÍÓÚ]|$)", text, re.IGNORECASE | re.DOTALL
        )
        out[key] = found.group(1).strip() if found else None

    return out
