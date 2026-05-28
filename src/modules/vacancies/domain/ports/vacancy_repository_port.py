from typing import TYPE_CHECKING, List, Protocol

if TYPE_CHECKING:
    from vacancy.domain.Vacancy import Vacancy


class VacancyRepositoryPort(Protocol):
    async def get_by_id(self, vacancy_id: str) -> Vacancy: ...

    async def save(self, vacancy: Vacancy) -> Vacancy:
        """Insert or update a vacancy (persist domain object)"""
        ...

    async def find_similar(self, embedding: list, limit: int = 10) -> List[Vacancy]: ...

    async def list_stale(self, older_than_minutes: int) -> List[Vacancy]:
        pass
