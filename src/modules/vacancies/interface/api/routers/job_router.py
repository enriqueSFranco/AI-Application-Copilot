from datetime import datetime, timezone

from fastapi import APIRouter, Body, Depends, Header, HTTPException, status

from job.application.use_cases.get_jobs_by_category import GetJobsByCategoryUseCase
from job.application.use_cases.list_jobs import ListJobsUseCase
from job.application.use_cases.scrape_job import ScrapeJobUseCase
from job.domain.ports.classifier_port import ClassifierPort
from job.domain.ports.job_repository_port import JobRepositoryPort
from job.domain.value_objects.job_categories import JobCategory
from job.domain.value_objects.job_url import InvalidUrlError
from job.infraestructure.spiders.scraper_factory import ScraperFactory
from job.interface.api.dependencies import (
    get_classifier_adapter,
    get_repo,
)
from job.interface.api.schemas import (
    JobResponse,
    ScrapeJobRequest,
    ScrapeJobResponse,
)

router = APIRouter(prefix="/jobs", tags=["jobs"])


# Endpoints:
async def get_current_user_id(x_user_id: str = Header(...)) -> str:
    # En una aplicación real, aquí validarías el token JWT y obtendrías el ID
    return x_user_id


# Para obtener todos los trabajos: GET /jobs
# Para filtrar por categoría: GET /jobs?category=frontend
@router.get("/", response_model=list[JobResponse])
async def get_jobs_list(
    category: JobCategory | None,
    repo: JobRepositoryPort = Depends(get_repo),
):
    """
    Obtiene una lista de todas las categorías de trabajo disponibles.
    """
    if category:
        use_case = GetJobsByCategoryUseCase(repo)
        jobs = await use_case.execute(category)
        return jobs
    else:
        use_case = ListJobsUseCase(repo)
        jobs = await use_case.execute()
        return jobs


# POST /jobs/scrape: Para iniciar el proceso de scraping de un trabajo.
@router.post(
    "/scrape", response_model=ScrapeJobResponse, status_code=status.HTTP_201_CREATED
)
async def scrape_job(
    request: ScrapeJobRequest = Body(...),
    repo: JobRepositoryPort = Depends(get_repo),
    classifier: ClassifierPort = Depends(get_classifier_adapter),
):
    try:
        scraper_factory = ScraperFactory.create_scraper(request.url)
        use_case = ScrapeJobUseCase(scraper_factory, repo, classifier)

        (job, confidence) = await use_case.execute(request.url)
        source = scraper_factory.__class__.__name__.replace("Scraper", "")

        return ScrapeJobResponse(
            job=JobResponse(**job.to_dict()),
            confidence=confidence,
            scrapedAt=datetime.now(timezone.utc).isoformat(),
            source=source,
        )

    except InvalidUrlError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        # Esto podría ser lanzado si el scraper no es compatible con la URL
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception:
        import traceback

        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error inesperado al procesar la solicitud.",
        )
