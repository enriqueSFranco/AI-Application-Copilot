from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

# Usamos dataclasses para el dominio


@dataclass
class SalaryRange:
    min: Optional[float] = None
    max: Optional[float] = None
    currency: Optional[str] = None


@dataclass
class RiskSignals:
    missing_company: bool = False
    suspicious_description: bool = False
    salary_too_low: bool = False
    url_not_secure: bool = False
    no_corporate_site: bool = False
    pattern_similar_to_fraud: float = 0.0


@dataclass
class Vacancy:
    id: str
    source_url: Optional[str]
    source_type: str  # manual | scraper | api

    title: str
    company: Optional[str]
    location: Optional[str]
    description: str
    raw_html: Optional[str] = None

    skills_extracted: List[str] = field(default_factory=list)
    salary: Optional[SalaryRange] = None
    seniority_detected: Optional[str] = None
    job_type: Optional[str] = None
    contract_type: Optional[str] = None

    ai_category: Optional[str] = None
    ai_subcategory: List[str] = field(default_factory=list)
    ai_embedding: Optional[List[float]] = None

    risk_level: str = "low"  # low | medium | high
    risk_reasons: List[str] = field(default_factory=list)
    risk_signals: RiskSignals = field(default_factory=RiskSignals)

    priority_score: int = 0
    priority_reasons: List[str] = field(default_factory=list)
    recommended_action: Optional[str] = None

    found_at: datetime = field(default_factory=datetime.now)
    scraped_at: Optional[datetime] = None
    last_checked_at: Optional[datetime] = None
    is_active: bool = True
    status: str = "unknown"  # open | closed | unknown

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    version: int = 1

    def bump_version(self):
        self.version += 1
        self.updated_at = datetime.now()
