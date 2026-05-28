# Usamos pydantic para DTOs

from typing import List, Optional

from pydantic import BaseModel, HttpUrl


class VacancyIngestDTO(BaseModel):
    url: Optional[HttpUrl] = None
    soruce_type: str = "scraper"  # manual | scraper | api


class VacancyCreateDTO(BaseModel):
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    description: str
    source_url: Optional[HttpUrl] = None
    source_type: str = "manual"


class VacancyResponseDTO(BaseModel):
    id: str
    title: str
    company: Optional[str]
    skills_extracted: List[str] = []
    risk_level: str
    priority_score: int
    created_at: str
    updated_at: str
