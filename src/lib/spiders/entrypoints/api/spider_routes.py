from typing import Literal, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel, HttpUrl

from lib.spiders.application.dto import ScrapedVacancyDTO
from src.lib.spiders.application.service import ScraperService

router = APIRouter(prefix="/scraper", tags=["Scraper"])


class ScrapeRequest(BaseModel):
    url: HttpUrl


class ScrapeResponseDTO(BaseModel):
    status: Literal["queued", "ok", "error"]
    data: Optional[ScrapedVacancyDTO] = None
    message: Optional[str] = None


def get_scraper_service():
    return ScraperService()


@router.post(
    "/run",
    response_model=ScrapeResponseDTO,
    status_code=202,
    summary="Scrapea una oferta laboral desde URLs soportadas.",
    description="Detecta el scraper adecuado, ejecuta Playwright y enviar el resultado al pipeline ETL/AI,",
)
async def scrape_endpoint(
    req: ScrapeRequest,
    background: BackgroundTasks,
    scrape_service: ScraperService = Depends(get_scraper_service),
):
    try:
        # svc = scrape_service()
        # dto = await svc.scrape_url(req.url)
        background.add_task(scrape_service.scrape_url, req.url)
        return {"status": "queued"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
