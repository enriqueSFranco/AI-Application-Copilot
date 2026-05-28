from typing import List

from job.domain.ports.job_repository_port import JobRepositoryPort


class RecalcPipelineUseCase:
    def __init__(self, repo: JobRepositoryPort):
        self._repo = repo

    async def execute(self, user_id: str) -> List[str]:
        """
        Ejecuta la lógica para obtener las categorías únicas de un usuario.
        """
        return await self._repo.get_unique_categories_by_user(user_id)
