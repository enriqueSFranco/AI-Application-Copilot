import asyncio
from concurrent.futures import ThreadPoolExecutor

import torch
from transformers import pipeline

from job.domain.ports.classifier_port import ClassifierPort
from job.domain.value_objects.job_categories import JOB_LABELS

executor = ThreadPoolExecutor(max_workers=2)


class HuggingFaceClassifier(ClassifierPort):
    def __init__(self):
        print("Cargando el modelo de Hugging Face...")
        device = 0 if torch.backends.mps.is_available() else -1
        self.classifier = pipeline(
            "zero-shot-classification", model="facebook/bart-large-mnli", device=device
        )
        print("Modelo de Hugging Face cargado con éxito.")

    async def classify_job_description(self, description: str) -> dict:
        if not description:
            return {"category": None, "confidence": None}

        loop = asyncio.get_running_loop()

        result = await loop.run_in_executor(
            executor, lambda: self.classifier(description, JOB_LABELS)
        )
        best_category = result["labels"][0]
        confidence_score = float(result["scores"][0])

        return {"predicted_category": best_category, "confidence": confidence_score}
