from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from job.domain.job_entity import Job


class JobRepositoryPort(Protocol):
    async def save(self, job: "Job") -> None: ...
