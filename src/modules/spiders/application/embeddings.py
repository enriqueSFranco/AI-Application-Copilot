from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class ScrapedSalary:
    min: Optional[float] = None
    max: Optional[float] = None
    currency: Optional[str] = None


@dataclass
class ScrapedVacancy:
    source_url: str
    source_name: str  # occ | linkedin | glassdoor | etc
    scraped_at: datetime

    title: str
    company: Optional[str]
    location: Optional[str]
    description: Optional[str]

    raw_html: Optional[str]

    salary: Optional[ScrapedSalary] = None
    skills_extracted: List[str] = None
    metadata: Dict[str, Any] = None
