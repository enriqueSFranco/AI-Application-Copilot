from job.domain.ports.job_repository_port import JobRepositoryPort


class ListJobsUseCase:
    def __init__(self, repo: JobRepositoryPort):
        self.repo = repo

    async def execute(self):
        return await self.repo.list()
