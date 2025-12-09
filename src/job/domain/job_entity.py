import uuid
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Job:
    id: str
    url: str
    title: str
    company: str | None
    description: str
    category: Optional[str]

    @staticmethod
    def create(
        url: str, title: str, company: str, description: str, category: str
    ) -> "Job":
        """Genera un Job con ID UUID v4 único."""
        return Job(
            id=str(uuid.uuid4()),
            url=url,
            title=title,
            company=company,
            description=description,
            category=category,
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "url": self.url,
            "title": self.title,
            "company": self.company,
            "description": self.description,
            "category": self.category,
        }
