import asyncio
from typing import Dict, Set

from job.domain.job_entity import Job
from job.domain.ports.job_repository_port import JobRepositoryPort
from job.domain.value_objects.job_categories import JobCategory


class VacancyRepositoryInMemory(JobRepositoryPort):
    def __init__(self):
        self.fake_db: Dict[str, "Job"] = {}  # {"uuidv4_1": Job(), "uuuidv4_2": Job()}

        self.category_idx: Dict[
            "JobCategory", Set["Job"]
        ] = {}  # {"backend": [], "frontend react": [], "mobile developer": []}
        self.company_idx: Dict[
            str, Set["Job"]
        ] = {}  # {"puerto de liverpool": [], "ntt data": [], "ticket master": []}

        # Lock para proteger escritura concurrente
        self._lock = asyncio.Lock()

    async def save(self, job: "Job") -> None:
        existing_job = self.fake_db.get(job.id)
        async with self._lock:
            if existing_job:
                if existing_job.category != job.category:
                    self.category_idx[existing_job.category].discard(existing_job)
                    if not self.category_idx[existing_job.category]:
                        del self.category_idx[existing_job.category]
                    self.category_idx.setdefault(job.category, set).add(job)

                if existing_job.company != job.company:
                    self.company_idx[existing_job.company].discard(existing_job)
                    if not self.company_idx[existing_job.company]:
                        del self.company_idx[existing_job.company]
                    self.company_idx.setdefault(job.company, set()).add(job)
            else:
                self.fake_db[job.id] = job
                if job.category not in self.category_idx:
                    self.category_idx[job.category] = set()
                self.category_idx.get(job.category).add(job)
                if job.company not in self.company_idx:
                    self.company_idx[job.company] = set()
                self.company_idx.get(job.company).add(job)

            self.fake_db[job.id] = job

    async def get_by_category(self, category: "JobCategory") -> Set["Job"]:
        return self.category_idx.get(category, set())

    async def get_by_company(self, company: str) -> Set["Job"]:
        return self.company_idx.get(company, set())

    async def get_by_id(self, id: str) -> "Job":
        return self.fake_db.get(id)

    async def get_unique_categories_by_user(self, user_id: str) -> Set["Job"]:
        """
        Obtiene una lista de categorías únicas asociadas a las postulaciones de un usuario.
        """
        ...
