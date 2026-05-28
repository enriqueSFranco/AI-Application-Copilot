# Caso de uso: analizar con ML/NLP
from job.domain.ports.classifier_port import ClassifierPort
from job.domain.value_objects.enums import JobBoard


class ClassifyJobUseCase:
    def __init__(self, repo: ClassifierPort):
        self.repo = repo

    async def execute(self, description: str) -> JobBoard:
        return await self.repo.classify(description)
