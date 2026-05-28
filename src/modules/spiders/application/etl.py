# ETL pipeline: normalize, enrich, upsert
import hashlib
from datetime import datetime

from modules.vacancies.domain.models import Vacancy


def fingerprint_url(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def map_dto_to_vacancy(dto: dict) -> Vacancy:
    vacancy = Vacancy(
        id=fingerprint_url(dto.get("source_url") or str(datetime.now())),
        source_url=dto.get("source_url"),
        source_type=dto.get("source_type") or "scraper",
        title=dto.get("title"),
        company=dto.get("company") or "",
        location=dto.get("location") or "",
        description=dto.get("description") or "",
        raw_html=dto.get("raw_html"),
        skills_extracted=dto.get("skills_extracted") or [],
        scraped_at=dto.get("scraped_at"),
        found_at=dto.get("found_at"),
    )
    return vacancy


def enrich_and_persist(dto: dict):
    # map
    vacancy = map_dto_to_vacancy(dto)

    # normalizar el salario
    # extraer las skills (heuristic + basic NLP)
    # detectar el seniority
    # embeddings (optional heavy)
    # risk signals
    # compute priority_score
    # limpiar la descrición
    # upsert into DB
    pass
