import datetime
import uuid

from sqlalchemy import (
    ARRAY,
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import declarative_base
from sympy import Array

Base = declarative_base()


class VacancyORM(Base):
    __tablename__ = "vacancies"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_url = Column(Text, nullable=False)
    source_type = Column(String, default="manula")

    title = Column(Text, nullable=False)
    company = Column(Text, nullable=True)
    location = Column(Text, nullable=True)
    description = Column(Text, nullable=False)
    raw_html = Column(Text, nullable=True)

    skills_extracted = Column(ARRAY(String), default=[])
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    salary_currency = Column(String, nullable=True)
    seniority_detected = Column(String, nullable=True)
    job_type = Column(String, nullable=True)
    contract_type = Column(String, nullable=True)

    ai_category = Column(String, nullable=True)
    ai_subcategory = Column(ARRAY(String), default=[])
    ai_embedding = Column(JSONB, nullable=True)

    risk_level = Column(String, default="low")  # low | medium | high
    risk_reasons = Column(Array(String), default=[])
    risk_signals = Column(JSONB, default={})

    priority_score = Column(Integer, default=0)
    priority_reasons = Column(ARRAY(String), default=[])
    recommended_action = Column(String, nullable=True)

    found_at = Column(DateTime, default=datetime.datetime.now)
    scraped_at = Column(DateTime, nullable=True)
    last_checked_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    status = Column(String, default="unknow")  # open | closed | unknown

    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)
    version = Column(Integer, default=1)
