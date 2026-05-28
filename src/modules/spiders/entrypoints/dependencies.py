# FACTORY DE DEPENDENCIA

from ..application.service import ScraperService


def get_scraper_service() -> ScraperService:
    """
    FastAPI inyecta esta dependencia cuando un endpoint la necesita.
    Permite:
      - reemplazar servicio en tests
      - configurar singletons si quieres
      - respetar arquitectura hexagonal
    """
    return ScraperService()
