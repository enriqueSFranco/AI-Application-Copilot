import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, HttpUrl, field_validator

from ...spiders.application.validators import normalize_salary


class SalaryRangeDTO(BaseModel):
    min: Optional[float] = None
    max: Optional[float] = None
    currency: Optional[str] = None


class ScrapedVacancyDTO(BaseModel):
    source_url: Optional[HttpUrl] = None
    source_name: Optional[HttpUrl] = None  # occ, linkedin, glassdoor
    scraped_at: Optional[datetime.datetime] = None

    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    description: str
    raw_html: Optional[str] = None

    skills_extracted: Optional[List[str]] = []
    salary: Optional[SalaryRangeDTO]

    metadata: Optional[Dict[str, Any]] = {}

    @field_validator("salary", mode="before")
    def normalize_salary_field(cls, v):
        if isinstance(v, str):
            return normalize_salary(v)
        return v
