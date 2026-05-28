from typing import Protocol


class ClassifierPort(Protocol):
    async def classify_job_description(self, description: str) -> dict[str, float]:
        """Clasifica una descripción de una vacante

        Args:
            description (str): La descripción de la vacante a clasificar

        Returns:
            dict: Un diccionario con la clasificación y el puntaje de confianza.
        """
        ...
