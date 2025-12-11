# Cleaners, salary parsers, date parsers

import re
from typing import List, Optional, Tuple

from ...vacancies.domain.models import Vacancy

SKILLS_CATALOG = [
    "react",
    "react native",
    "reactjs",
    "react.js",
    "next.js",
    "nextjs",
    "javascript",
    "typescript",
    "node",
    "nodejs",
    "express",
    "graphql",
    "docker",
    "kubernetes",
    "aws",
    "firebase",
    "postgresql",
    "mysql",
    "redux",
    "zod",
    "prisma",
    "tailwind",
    "expo",
    "flutter",
    "swift",
    "objective-c",
    "java",
    "spring",
    "android",
    "ios",
]

SENIORITY_KEYWORDS = {
    "junior": ["junior", "jr", "jr.", "júnior"],
    "mid": ["semi-senior", "semi senior", "mid", "mid-level", "mid level"],
    "senior": ["senior", "sr", "sr.", "lead", "principal"],
}


# input = "$15,000 - $18,000 Mensuales"
# Extrae números y moneda del salary string. Usa regex y heurísticas.
def normalize_salary(salary_string: str):
    """
    Normaliza un string de salario a {min, max, currency}
    Heurístico: busca rangos "10,000 - 15,000 MXN" o "$10,000" o "USD 20k".
    """
    if not salary_string:
        return {"currency": None, "min": None, "max": None}

    regex = re.compile(
        r"""
        (?P<currency>[\$€£]|(?:[A-Z]{3})\s)?
        \s*
        (?P<number1>[0-9,.]+)
        \s*
        (?:[-\s]*(?:a|o)?\s
            (?:(?P<currency2>[\$€£]|(?:[A-Z]{3})\s?)?\s*)
            (?P<number2>[0-9,.]+)?
        )?
        """,
        re.VERBOSE | re.IGNORECASE,
    )

    match = regex.search(salary_string)

    if not match:
        return {
            "min": salary_string.strip() or None,
            "max": salary_string.strip() or None,
            "currency": None,
        }

    groups = match.groupdict()

    currency_str = groups.get("currency", groups.get("currency2"))
    number1_str = groups.get("number1")
    number2_str = groups.get("number2")
    # periodicity_str = groups.get("periodicity")

    if not currency_str:
        currency_str = groups.get("currency") or groups.get("currency2")

    salary_range = []

    def clean_and_convert(num_str: Optional[str]) -> Optional[float]:
        """Limpia el string de números (elimina comas, etc.) y convierte a float."""
        if not num_str:
            return None
        num_str_cleaned = num_str.replace(",", "")

        # Si tiene punto, lo convertimos a float.
        try:
            return float(num_str_cleaned)
        except ValueError:
            return None

    salary1 = clean_and_convert(number1_str)
    if salary1 is not None:
        salary_range.append(salary1)

    salary2 = clean_and_convert(number2_str)
    if salary2 is not None:
        salary_range.append(salary2)

    # ordenar los rangos
    if len(salary_range) == 2:
        salary_range.sort()

    # Resultado final
    min_salary = salary_range[0] if len(salary_range) >= 1 else None
    max_salary = salary_range[1] if len(salary_range) == 2 else None
    return {
        "min": min_salary,
        "max": max_salary,
        "currency": currency_str.strip() if currency_str else None,
    }


def extract_skills(text: str, catalog: List[str] = SKILLS_CATALOG) -> List[str]:
    """
    Heurístico: búsqueda de palabras clave en el texto.
    Retorna lista de skills únicas encontradas en el texto.
    """
    if not text:
        return []
    t = text.lower()
    found = set()

    for s in catalog:
        s_norm = s.lower()
        if s_norm in t:
            found.add(s_norm)

    mapping = {
        "reactjs": "react",
        "react.js": "react",
        "nextjs": "next.js",
        "typescript": "typescript",
    }

    normalized = [mapping.get(x, x) for x in found]
    return sorted(set(normalized))


def detect_seniority(title: Optional[str], description: Optional[str]) -> Optional[str]:
    """
    Detecta keywords de seniority en title + description.
    Devuelve 'junior'|'mid'|'senior' o None.
    """
    text = " ".join(filter(None, [title or "", description or ""])).lower()

    for level, keywords in SENIORITY_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return level
    return None


def detect_risk_signals(vacancy: Vacancy) -> dict:
    """
    Heurística simple para detectar señales de riesgo:
    - falta de empresa
    - descripción demasiado breve
    - presencia de patrones sospechosos
    - url no segura
    """

    rs = {
        "missing_company": False,
        "suspicious_description": False,
        "salary_too_low": False,
        "url_not_secure": False,
        "no_corporate_site": False,
        # "pattern_similar_to_fraud": 0.0,
    }

    MIN_SIZE_DESCRIPTION = 120
    if not vacancy.company or vacancy.company.strip() == "":
        rs["missing_company"] = True

    if not vacancy.description or len(vacancy.description) < MIN_SIZE_DESCRIPTION:
        rs["suspicious_description"] = True

    try:
        if vacancy.salary:
            smin = getattr(vacancy.salary, "min", None) or (
                vacancy.salary.get("min") if isinstance(vacancy.salary, dict) else None
            )
            if smin is not None and smin < 2000:
                rs["salary_too_low"] = True
    except Exception:
        pass

    if vacancy.source_url and vacancy.source_url.startswith("http://"):
        rs["url_not_secure"] = True

    return rs


def compute_priority_score(vacancy) -> Tuple[int, List[str]]:
    """
    Score heurístico que prioriza vacantes:
    - más skills match -> +X
    - salario presente -> +Y
    - seniority compatible -> +Z
    - riesgo -> penaliza
    """
