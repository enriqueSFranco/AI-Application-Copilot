import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from psycopg_pool import AsyncConnectionPool

from job.domain.ports.job_repository_port import JobRepositoryPort

# from job.domain.value_objects.job_url import JobUrl
from job.infraestructure.classifiers.huggingface_classifier import HuggingFaceClassifier
from job.infraestructure.db.config import load_config
from job.infraestructure.playwright.browser_manager import BrowserManager
from job.infraestructure.repositories.in_memory_repository import InMemoryRepository
from job.infraestructure.repositories.postgresql_repository import PostgresRepository

classifier_adapter = HuggingFaceClassifier()

db_pool: AsyncConnectionPool | None = None
_browser_manager: BrowserManager | None = None
_classifier_instance: HuggingFaceClassifier | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_pool, _browser_manager, _classifier_instance

    # DB Pool
    if REPO_STRATEGY == "postgres":
        db_config = load_config()  # <-- solo se ejecuta si usas postgres
        db_pool = AsyncConnectionPool(conninfo=db_config)
        await db_pool.open()
        print("✅ Pool de conexiones PostgreSQL creado")

    # Browser Manager
    _browser_manager = BrowserManager.get_instance()
    print("Browser List")

    yield

    if _browser_manager:
        await _browser_manager.close_browser()
        print("Browser cerrado")

    if db_pool:
        await db_pool.close()
        print("Pool de conexiones a la base de datos cerrado.")


REPO_STRATEGY = os.getenv(
    "REPO_STRATEGY", "memory"
)  # memory, postgres, mysql, redis, oracle, etc.


def get_repo() -> JobRepositoryPort:
    if REPO_STRATEGY == "postgres":
        if not db_pool:
            raise Exception("Database connection pool not initialized.")
        return PostgresRepository(conn_pool=db_pool)
    return InMemoryRepository()


# --- Hugging Face lazy loader ---
_classifier_instance: HuggingFaceClassifier | None = None


def get_classifier_adapter() -> HuggingFaceClassifier:
    global _classifier_instance
    if _classifier_instance is None:
        print("Cargando el modelo de Hugging Face...")
        _classifier_instance = HuggingFaceClassifier()
        print("Modelo de Hugging Face cargado con éxito.")
    return classifier_adapter
