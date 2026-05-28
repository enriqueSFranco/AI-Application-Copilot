import uuid
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from vacancies.domain.models import RiskSignals, SalaryRange, Vacancy
from vacancies.infrastructure.db.models import VacancyORM

# from psycopg_pool import AsyncConnectionPool
from modules.vacancies.domain.ports.vacancy_repository_port import VacancyRepositoryPort


class VacancyRepositorySQL(VacancyRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_unique_categories(self, user_id: str) -> List["Vacancy"]: ...

    async def get_by_id(self, vacancy_id: str) -> "Vacancy" | None:
        r = await self.session.execute(
            select(VacancyORM).where(VacancyORM.id == uuid.UUID(vacancy_id))
        )
        orm = r.scalar_one_or_none()

        if not orm:
            return None
        return self._orm_to_domain(orm)

    async def save(self, vacancy: "Vacancy") -> "Vacancy":
        orm = None
        if vacancy.id:
            r = await self.session.execute(
                select(VacancyORM).where(VacancyORM.id == uuid.UUID(vacancy.id))
            )
            orm = r.scalar_one_or_none()
        if orm is None:
            orm = VacancyORM(id=uuid.UUID(vacancy.id)) if vacancy.id else uuid.uuid4()
            self.session.add(orm)

        # map fields (partial)
        orm.source_url = vacancy.source_url
        orm.source_type = vacancy.source_type
        orm.title = vacancy.title
        orm.company = vacancy.company
        orm.location = vacancy.location
        orm.description = vacancy.description
        orm.raw_html = vacancy.raw_html
        orm.skills_extracted = vacancy.skills_extracted
        if vacancy.salary:
            orm.salary_min = vacancy.salary.min
            orm.salary_max = vacancy.salary.max
            orm.salary_currency = vacancy.salary.currency
        orm.seniority_detected = vacancy.seniority_detected
        orm.job_type = vacancy.job_type
        orm.contract_type = vacancy.contract_type
        orm.ai_category = vacancy.ai_category
        orm.ai_subcategory = vacancy.ai_subcategory
        orm.ai_embedding = vacancy.ai_embedding
        orm.risk_level = vacancy.risk_level
        orm.risk_reasons = vacancy.risk_reasons
        orm.risk_signals = vars(vacancy.risk_signals)
        orm.priority_score = vacancy.priority_score
        orm.priority_reasons = vacancy.priority_reasons
        orm.recommended_action = vacancy.recommended_action
        orm.found_at = vacancy.found_at
        orm.scraped_at = vacancy.scraped_at
        orm.last_checked_at = vacancy.last_checked_at
        orm.is_active = vacancy.is_active
        orm.status = vacancy.status
        orm.updated_at = vacancy.updated_at
        orm.version = vacancy.version

        await self.session.commit()
        await self.session.refresh(orm)
        self._orm_to_domain(orm)

    def _orm_to_domain(orm: VacancyORM) -> "Vacancy":
        salary = None
        if orm.salary_min is not None or orm.salary_max is not None:
            salary = SalaryRange(orm.salary_min, orm.salary_max)
        risk_signals = RiskSignals(**(orm.risk_signals or {}))

        return Vacancy(
            id=orm.id,
            source_url=orm.source_url,
            source_type=orm.source_type,
            title=orm.title,
            company=orm.company,
            location=orm.location,
            description=orm.description,
            raw_html=orm.raw_html,
            skills_extracted=orm.skills_extracted or [],
            salary=salary,
            seniority_detected=orm.seniority_detected,
            job_type=orm.job_type,
            contract_type=orm.contract_type,
            ai_category=orm.ai_category,
            ai_subcategory=orm.ai_subcategory or [],
            ai_embedding=orm.ai_embedding,
            risk_level=orm.risk_level,
            risk_reasons=orm.risk_reasons or [],
            risk_signals=risk_signals,
            priority_score=orm.priority_score,
            priority_reasons=orm.priority_reasons or [],
            recommended_action=orm.recommended_action,
            found_at=orm.found_at,
            scraped_at=orm.scraped_at,
            last_checked_at=orm.last_checked_at,
            is_active=orm.is_active,
            status=orm.status,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
            version=orm.version or 1,
        )


# async def main():
#     db_config = load_config()

#     pool = AsyncConnectionPool(db_config, open=False)
#     await pool.open()

#     repo = PostgresRepository(pool)

#     await pool.close()


# if __name__ == "__main__":
#     asyncio.run(main())
