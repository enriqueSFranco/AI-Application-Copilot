from typing import Literal, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel, HttpUrl

from ...application.service import ScraperService
from ..dependencies import get_scraper_service

router = APIRouter(prefix="/scraper", tags=["Scraper"])


class ScrapeRequest(BaseModel):
    url: HttpUrl


class ScrapeResponseDTO(BaseModel):
    status: Literal["queued", "ok", "error"]
    data: Optional[dict] = None
    message: Optional[str] = None


@router.post(
    "/run",
    response_model=ScrapeResponseDTO,
    status_code=202,
    summary="Ejecuta scraping en background.",
    description="Detecta automáticamente qué scraper usar según la URL y lo ejecuta sin bloquear la petición.",
)
async def scrape_endpoint(
    req: ScrapeRequest,
    background: BackgroundTasks,
    scraper_service: ScraperService = Depends(get_scraper_service),
):
    """
    Endpoint de scraping
    - procesa la url recibida
    - no bloque la petición gracia a BackgroundTasks
    - retorno inmediatamente el estado de queued

    Usamos inyección de dependencias para desacoplar:
    - el endpoint no crea servicios
    - FastAPI se encarga de resolver dependencias.
    """
    try:
        # encolamos el scraping en segundo plano para evitar bloquear al cliente
        # mientras playwright abre el navegador, carga la página y ejecuta scripts.
        background.add_task(scraper_service.scrape_url, req.url)
        scraper_service.logger.info(f"[SCRAPER] Scraping encolado para URL: {req.url}")
        return ScrapeResponseDTO(
            status="queued", message="scraping iniciado en background"
        )
    except ValueError as e:
        scraper_service.logger.warning("[SCRAPER]: Error controlado: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        scraper_service.logger.error(f"[SCRAPER] Error inesperado: {e}")
        raise HTTPException(status_code=500, detail="Error interno en el scraper")
