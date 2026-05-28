from job.domain.ports.job_repository_port import JobRepositoryPort


class CreateVacancyUseCase:
    def __init__(self, repo: JobRepositoryPort):
        self.repo = repo

    async def execute(self, id: str):
        return await self.repo.get(id)
