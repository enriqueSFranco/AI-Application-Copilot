from typing import List

from job.domain.job_entity import Job
from job.domain.ports.job_repository_port import JobRepositoryPort
from job.domain.value_objects.job_categories import JobCategory


class UpdateVacancyUseCase:
    def __init__(self, repo: JobRepositoryPort):
        self.repo = repo

    async def execute(self, category: JobCategory) -> List["Job"]:
        return await self.repo.get_by_category(category)
