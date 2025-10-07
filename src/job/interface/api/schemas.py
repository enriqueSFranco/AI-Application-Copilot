# Pydantic schemas
from typing import List, Optional

from pydantic import BaseModel


class JobResponse(BaseModel):
    url: str
    title: Optional[str] = ""
    company: Optional[str] = ""
    description: Optional[str] = ""
    category: str


class JobListResponse(BaseModel):
    jobs: List[JobResponse]


class ScrapeJobRequest(BaseModel):
    url: str


class ScrapeJobResponse(BaseModel):
    job: JobResponse
    scrapedAt: str
    source: Optional[str] = None  # ej. "OCC", "LinkedIn", "Indeed"
    status: str = "success"
