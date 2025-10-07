from typing import TYPE_CHECKING, Protocol, Set

from job.domain.value_objects.job_categories import JobCategory

if TYPE_CHECKING:
    from job.domain.job_entity import Job


class JobRepositoryPort(Protocol):
    async def save(self, job: "Job") -> None: ...
    async def get_by_category(self, category: JobCategory) -> Set["Job"]: ...
    async def get_unique_categories_by_user(self, user_id: str) -> Set["Job"]:
        """
        Obtiene una lista de categorías únicas asociadas a las postulaciones de un usuario.
        """
        ...
